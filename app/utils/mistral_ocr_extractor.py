"""
Mistral OCR extractor — converts a PDF to structured markdown using Mistral OCR 3.

The Mistral OCR API processes each page and returns markdown that preserves
tables, equations, and inline formatting — far richer than plain pypdf text.

Usage:
    from utils.mistral_ocr_extractor import extract_text_mistral_ocr, extract_text_mistral_ocr_from_bytes
"""

import base64
import logging
import tempfile
import os
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from mistralai.client import Mistral
    _MISTRAL_AVAILABLE = True
except ImportError:
    _MISTRAL_AVAILABLE = False
    logger.warning("[MistralOCR] mistralai package not installed — run: pip install mistralai")

_MISTRAL_OCR_MODEL = "mistral-ocr-latest"


def _pages_to_markdown(ocr_response) -> str:
    """Join per-page markdown from an OCR response into a single string."""
    parts = []
    for i, page in enumerate(ocr_response.pages, start=1):
        md = (page.markdown or "").strip()
        if md:
            parts.append(f"<!-- page {i} -->\n\n{md}")
    return "\n\n".join(parts)


def extract_text_mistral_ocr(pdf_path: str, api_key: str) -> str:
    """
    Extract structured markdown from a PDF file using Mistral OCR 3.

    Sends the PDF as a base64 data-URL to the Mistral OCR API.
    Returns full-document markdown with tables, equations, and formatting intact.
    Returns empty string on failure.
    """
    if not _MISTRAL_AVAILABLE:
        raise RuntimeError(
            "[MistralOCR] mistralai not installed. Run: pip install mistralai"
        )

    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
    except OSError as exc:
        logger.error(f"[MistralOCR] Cannot read file {pdf_path}: {exc}")
        return ""

    return extract_text_mistral_ocr_from_bytes(pdf_bytes, api_key)


def extract_text_mistral_ocr_from_bytes(pdf_bytes: bytes, api_key: str) -> str:
    """
    Extract structured markdown from raw PDF bytes using Mistral OCR 3.

    Returns full-document markdown. Returns empty string on failure.
    """
    if not _MISTRAL_AVAILABLE:
        raise RuntimeError(
            "[MistralOCR] mistralai not installed. Run: pip install mistralai"
        )

    if not api_key:
        logger.error("[MistralOCR] No Mistral API key provided.")
        return ""

    try:
        b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
        data_url = f"data:application/pdf;base64,{b64}"

        client = Mistral(api_key=api_key)
        response = client.ocr.process(
            model=_MISTRAL_OCR_MODEL,
            document={
                "type": "document_url",
                "document_url": data_url,
            },
        )

        markdown = _pages_to_markdown(response)
        logger.info(
            f"[MistralOCR] Extracted {len(markdown):,} chars "
            f"({len(response.pages)} pages)"
        )
        return markdown

    except Exception as exc:
        logger.error(f"[MistralOCR] OCR failed: {exc}")
        return ""
