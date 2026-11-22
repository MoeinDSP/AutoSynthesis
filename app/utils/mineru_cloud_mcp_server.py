#!/usr/bin/env python3
"""Standalone MCP server that wraps the MinerU cloud REST API.

Exposes the same 'parse_pdf' tool interface as mcp-mineru (local), but
delegates processing to the mineru.net cloud API instead of a local pipeline.

This script is launched as a subprocess by the MCP client (stdio transport).
It reads MinerU_API_KEY from the environment.

Usage (stdio MCP protocol — used by mineru_mcp_extractor.py):
    python utils/mineru_cloud_mcp_server.py

Required env var:
    MinerU_API_KEY  — Bearer token from mineru.net/apiManage
"""

import io
import logging
import os
import time
import zipfile

import requests
from mcp.server.fastmcp import FastMCP

_BASE_URL = "https://mineru.net"
_POLL_INTERVAL = 5   # seconds between status polls
_MAX_WAIT = 300      # 10-minute timeout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp_server = FastMCP("mineru-cloud")


def _api_key() -> str:
    key = os.getenv("MinerU_API_KEY") or os.getenv("MINERU_API_KEY", "")
    if not key:
        raise RuntimeError("MinerU_API_KEY not set in environment")
    return key.strip()


def _auth_headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _poll_batch_until_done(batch_id: str, key: str) -> dict:
    """Poll GET /api/v4/extract-results/batch/{batch_id} until first file is done.

    Temporarily logging every poll at INFO (not just unrecognized states at DEBUG, which the
    server's own WARNING-level basicConfig was silently dropping) -- diagnosing a 100%-timeout
    pattern where we can't currently tell whether MinerU is genuinely stuck pending/running the
    whole window, or whether it's actually completing under a state value (e.g. "success"
    instead of "done") that this code doesn't recognize, which would misreport a real success
    as a timeout failure. Revert to DEBUG/WARNING once that's established."""
    url = f"{_BASE_URL}/api/v4/extract-results/batch/{batch_id}"
    deadline = time.monotonic() + _MAX_WAIT
    poll_num = 0
    while time.monotonic() < deadline:
        poll_num += 1
        resp = requests.get(url, headers=_auth_headers(key), timeout=30)
        resp.raise_for_status()
        body = resp.json()
        if body.get("code") != 0:
            raise RuntimeError(f"MinerU API error: {body.get('msg', body)}")
        results = body.get("data", {}).get("extract_result", [])
        if not results:
            logger.info(f"[MinerU poll #{poll_num}] Batch {batch_id}: no extract_result entries yet. Raw data: {body.get('data')}")
        else:
            file_result = results[0]
            state = file_result.get("state", "")
            logger.info(f"[MinerU poll #{poll_num}] Batch {batch_id}: state={state!r} full_result={file_result}")
            if state == "done":
                return file_result
            if state == "failed":
                raise RuntimeError(f"MinerU task failed: {file_result.get('err_msg', 'unknown')}")
        time.sleep(_POLL_INTERVAL)
    raise TimeoutError(f"Batch {batch_id} did not finish within {_MAX_WAIT}s")


def _markdown_from_zip(zip_url: str) -> str:
    resp = requests.get(zip_url, timeout=60)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        md_files = [n for n in zf.namelist() if n.endswith(".md")]
        if not md_files:
            raise RuntimeError("No .md file found in MinerU result zip")
        md_name = next((n for n in md_files if "/" not in n), md_files[0])
        return zf.read(md_name).decode("utf-8")


@mcp_server.tool()
def parse_pdf(
    file_path: str,
    is_ocr: bool = False,
    enable_formula: bool = True,
    enable_table: bool = True,
    language: str = "en",
) -> str:
    """Parse a PDF using the MinerU cloud API and return structured Markdown.

    Args:
        file_path:      Absolute path to the PDF file.
        is_ocr:         Force OCR even for text-layer PDFs.
        enable_formula: Extract LaTeX formulas.
        enable_table:   Extract tables as Markdown.
        language:       Document language hint (e.g. 'en', 'de', 'ch').

    Returns:
        Structured Markdown with tables, formulas, and body text,
        or an '❌ Error …' string on failure.
    """
    try:
        key = _api_key()
    except RuntimeError as exc:
        return f"❌ Error: {exc}"

    filename = os.path.basename(file_path)

    try:
        with open(file_path, "rb") as fh:
            pdf_bytes = fh.read()
    except OSError as exc:
        return f"❌ Error reading file: {exc}"

    try:
        # Step 1: register batch → get pre-signed upload URL
        batch_resp = requests.post(
            f"{_BASE_URL}/api/v4/file-urls/batch",
            headers=_auth_headers(key),
            json={
                "files": [{"name": filename, "is_ocr": is_ocr}],
                "model_version": "vlm",
                "enable_formula": enable_formula,
                "enable_table": enable_table,
                "language": language,
            },
            timeout=30,
        )
        batch_resp.raise_for_status()
        batch_body = batch_resp.json()
        if batch_body.get("code") != 0:
            return f"❌ Error registering batch: {batch_body.get('msg', batch_body)}"

        batch_id   = batch_body["data"]["batch_id"]
        upload_url = batch_body["data"]["file_urls"][0]

        # Step 2: PUT file bytes to pre-signed OSS URL.
        # Do NOT add headers (e.g. Content-Type) — the URL signature only covers
        # headers that were included at signing time; extra headers → 403.
        put_resp = requests.put(
            upload_url,
            data=pdf_bytes,
            timeout=120,
        )
        put_resp.raise_for_status()

        # Step 3: poll until done (batch endpoint, automatic task submission)
        result_data = _poll_batch_until_done(batch_id, key)

        zip_url = result_data.get("full_zip_url")
        if not zip_url:
            return f"❌ Error: task done but no full_zip_url in response"

        # Step 4: download zip and extract Markdown
        return _markdown_from_zip(zip_url)

    except Exception as exc:
        return f"❌ Error parsing PDF: {exc}"


if __name__ == "__main__":
    mcp_server.run(transport="stdio")
