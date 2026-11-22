"""MinerU cloud REST API extractor (Precise Parsing API v4).

Uploads the PDF to mineru.net, polls for completion, and returns Markdown.

Environment variable: MinerU_API_KEY (Bearer token from mineru.net)

Flow:
  1. POST /api/v4/file-urls/batch  → get batch_id + pre-signed upload URL
  2. PUT  <pre-signed URL>          → upload raw PDF bytes
  3. GET  /api/v4/extract/task/{batch_id} → poll until state == "done"
  4. GET  full_zip_url              → download zip, extract .md content
"""

import io
import logging
import os
import time
import zipfile
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_BASE_URL = "https://mineru.net"
_POLL_INTERVAL = 5    # seconds between status polls
_MAX_WAIT = 600       # max total wait (10 min — large papers can be slow)


def _get_api_key() -> Optional[str]:
    key = os.getenv("MinerU_API_KEY") or os.getenv("MINERU_API_KEY")
    return key.strip() if key else None


def _auth_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _poll_batch_until_done(batch_id: str, api_key: str) -> dict:
    """Poll /api/v4/extract-results/batch/{batch_id} until first file is done."""
    url = f"{_BASE_URL}/api/v4/extract-results/batch/{batch_id}"
    deadline = time.monotonic() + _MAX_WAIT
    while time.monotonic() < deadline:
        resp = requests.get(url, headers=_auth_headers(api_key), timeout=30)
        resp.raise_for_status()
        body = resp.json()
        if body.get("code") != 0:
            raise RuntimeError(f"MinerU API error: {body.get('msg', body)}")
        results = body.get("data", {}).get("extract_result", [])
        if results:
            file_result = results[0]
            state = file_result.get("state", "")
            if state == "done":
                return file_result
            if state == "failed":
                raise RuntimeError(f"MinerU task failed: {file_result.get('err_msg', 'unknown')}")
            logger.debug(f"[MinerU API] Batch {batch_id}: {state}")
        time.sleep(_POLL_INTERVAL)
    raise TimeoutError(f"MinerU batch {batch_id} did not finish within {_MAX_WAIT}s")


def _extract_markdown_from_zip(zip_url: str) -> str:
    """Download the result zip and return the first .md file contents."""
    resp = requests.get(zip_url, timeout=120)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        md_files = [n for n in zf.namelist() if n.endswith(".md")]
        if not md_files:
            raise RuntimeError("No Markdown file in MinerU result zip")
        # prefer a root-level .md over ones inside subdirectories
        md_name = next((n for n in md_files if "/" not in n), md_files[0])
        return zf.read(md_name).decode("utf-8")


def extract_text_mineru_api_from_bytes(
    pdf_bytes: bytes,
    filename: str = "paper.pdf",
) -> str:
    """Upload PDF bytes to MinerU cloud API and return extracted Markdown.

    Args:
        pdf_bytes: Raw PDF file contents.
        filename:  Suggested filename (used server-side for naming outputs).

    Returns:
        Structured Markdown string with tables, formulas, and body text.

    Raises:
        RuntimeError: API key missing, upload failed, or task failed.
        TimeoutError: Task did not complete within _MAX_WAIT seconds.
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "MinerU_API_KEY not set. Add it to .env to use the cloud API."
        )

    # Step 1: register batch → get pre-signed upload URL
    logger.info(f"[MinerU API] Requesting upload slot for {filename!r} ({len(pdf_bytes)} bytes)")
    batch_resp = requests.post(
        f"{_BASE_URL}/api/v4/file-urls/batch",
        headers=_auth_headers(api_key),
        json={
            "files": [{"name": filename, "is_ocr": False}],
            "model_version": "vlm",
            "enable_formula": True,
            "enable_table": True,
        },
        timeout=30,
    )
    batch_resp.raise_for_status()
    batch_body = batch_resp.json()
    if batch_body.get("code") != 0:
        raise RuntimeError(f"MinerU batch registration failed: {batch_body.get('msg', batch_body)}")

    batch_data = batch_body["data"]
    batch_id   = batch_data["batch_id"]
    upload_url = batch_data["file_urls"][0]

    # Step 2: PUT file bytes to the pre-signed OSS URL.
    # No extra headers — the URL signature only covers the bare PUT;
    # adding Content-Type or Authorization causes a 403 signature mismatch.
    logger.info(f"[MinerU API] Uploading to pre-signed URL (batch_id={batch_id})")
    put_resp = requests.put(
        upload_url,
        data=pdf_bytes,
        timeout=120,
    )
    put_resp.raise_for_status()

    # Step 3: poll for completion via batch results endpoint
    logger.info(f"[MinerU API] Polling batch {batch_id}")
    result_data = _poll_batch_until_done(batch_id, api_key)

    zip_url = result_data.get("full_zip_url")
    if not zip_url:
        raise RuntimeError(f"MinerU returned done but no full_zip_url: {result_data}")

    # Step 4: download zip and extract Markdown
    logger.info(f"[MinerU API] Downloading result zip")
    text = _extract_markdown_from_zip(zip_url)
    logger.info(f"[MinerU API] Extracted {len(text)} chars from {filename!r}")
    return text


def extract_text_mineru_api(pdf_path: str) -> str:
    """Extract text from a local PDF using the MinerU cloud API.

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        Structured Markdown string.
    """
    abs_path = os.path.abspath(pdf_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")

    filename = os.path.basename(abs_path)
    with open(abs_path, "rb") as fh:
        pdf_bytes = fh.read()

    return extract_text_mineru_api_from_bytes(pdf_bytes, filename=filename)
