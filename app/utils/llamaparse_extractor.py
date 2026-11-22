"""
LlamaParse extractor — converts a PDF to structured markdown via the
LlamaIndex Cloud REST API (no SDK dependency).

API flow:
  1. POST /api/parsing/upload       → job_id
  2. Poll GET /api/parsing/job/{id} → status in {PENDING, SUCCESS, ERROR}
  3. GET /api/parsing/job/{id}/result/markdown → full markdown text

Usage:
    from utils.llamaparse_extractor import extract_text_llamaparse, extract_text_llamaparse_from_bytes
"""

import logging
import os
import tempfile
import time

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.cloud.llamaindex.ai"
_UPLOAD_PATH = "/api/parsing/upload"
_JOB_PATH = "/api/parsing/job/{job_id}"
_RESULT_PATH = "/api/parsing/job/{job_id}/result/markdown"

_POLL_INTERVAL = 3   # seconds between status checks
_POLL_TIMEOUT  = 120 # seconds before giving up


def _post_upload(pdf_bytes: bytes, api_key: str) -> str:
    """Upload PDF bytes and return the job_id."""
    import requests
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": ("paper.pdf", pdf_bytes, "application/pdf")}
    data = {"result_type": "markdown", "premium_mode": "false"}
    resp = requests.post(
        _BASE_URL + _UPLOAD_PATH,
        headers=headers,
        files=files,
        data=data,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def _poll_job(job_id: str, api_key: str) -> str:
    """Poll until job is SUCCESS, then return the markdown result."""
    import requests
    headers = {"Authorization": f"Bearer {api_key}"}
    status_url = _BASE_URL + _JOB_PATH.format(job_id=job_id)
    result_url = _BASE_URL + _RESULT_PATH.format(job_id=job_id)

    deadline = time.monotonic() + _POLL_TIMEOUT
    while time.monotonic() < deadline:
        resp = requests.get(status_url, headers=headers, timeout=30)
        resp.raise_for_status()
        status = resp.json().get("status", "")

        if status == "SUCCESS":
            r = requests.get(result_url, headers=headers, timeout=60)
            r.raise_for_status()
            return r.json().get("markdown", "")

        if status == "ERROR":
            raise RuntimeError(f"LlamaParse job {job_id} failed: {resp.json()}")

        logger.debug(f"[LlamaParse] job {job_id} status={status}, waiting…")
        time.sleep(_POLL_INTERVAL)

    raise TimeoutError(f"LlamaParse job {job_id} timed out after {_POLL_TIMEOUT}s")


def extract_text_llamaparse_from_bytes(pdf_bytes: bytes, api_key: str) -> str:
    """
    Extract structured markdown from raw PDF bytes via the LlamaParse REST API.

    Returns full-document markdown. Returns empty string on failure.
    """
    if not api_key:
        logger.error("[LlamaParse] No LlamaCloud API key provided.")
        return ""

    try:
        job_id = _post_upload(pdf_bytes, api_key)
        logger.info(f"[LlamaParse] Job submitted: {job_id}")
        markdown = _poll_job(job_id, api_key)
        logger.info(f"[LlamaParse] Extracted {len(markdown):,} chars (job {job_id})")
        return markdown
    except Exception as exc:
        logger.error(f"[LlamaParse] API call failed: {exc}")
        return ""


def extract_text_llamaparse(pdf_path: str, api_key: str) -> str:
    """
    Extract structured markdown from a PDF file via the LlamaParse REST API.

    Returns full-document markdown. Returns empty string on failure.
    """
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
    except OSError as exc:
        logger.error(f"[LlamaParse] Cannot read file {pdf_path}: {exc}")
        return ""

    return extract_text_llamaparse_from_bytes(pdf_bytes, api_key)
