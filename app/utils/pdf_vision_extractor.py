"""
PDF Vision Extractor — renders PDF pages as images and uses a vision LLM
to extract statistical content, tables, and quantitative data.
"""

import base64
import logging
import tempfile
import os
from typing import List

from openai import OpenAI

logger = logging.getLogger(__name__)

try:
    import fitz  # pymupdf
    _FITZ_AVAILABLE = True
except ImportError:
    _FITZ_AVAILABLE = False
    logger.warning("[VisionExtractor] pymupdf not installed — vision extraction unavailable.")


# Focused on data extraction, not verbatim transcription — avoids copyright refusals.
_EXTRACTION_PROMPT = (
    "You are a research data extraction assistant analyzing a page from an academic paper.\n\n"
    "Your task: identify and report ALL quantitative and statistical information on this page.\n\n"
    "Extract the following:\n"
    "1. TABLES — reproduce every table as a markdown table with all column headers and cell values. "
    "Include the table caption and any footnotes below the table.\n"
    "2. STATISTICS IN TEXT — extract every number linked to a statistical result: "
    "means (M), standard deviations (SD), sample sizes (n, N), "
    "t-values, F-values, p-values, confidence intervals (CI), "
    "effect sizes (d, g, η², r, OR, RR), regression coefficients (b, β).\n"
    "3. GROUP LABELS — record the exact names of all experimental groups, conditions, "
    "or models being compared (e.g. 'GPT-4', 'Human raters', 'Control group').\n"
    "4. SECTION HEADERS — mark them with ## so the reader knows the context "
    "(e.g. ## Results, ## Method, ## Participants).\n\n"
    "FORMAT:\n"
    "- Use markdown tables for any tabular data.\n"
    "- For inline statistics write them as: outcome_name: group=X, M=X, SD=X, n=X, t(df)=X, p=X\n"
    "- If a page contains no statistical data, write: [No statistical data on this page]\n\n"
    "Do NOT copy large blocks of non-quantitative prose. Focus entirely on numbers and their context."
)


def _pdf_to_images(pdf_path: str, dpi: int = 120) -> List[bytes]:
    """Render each PDF page to a PNG image (bytes)."""
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=matrix)
        images.append(pix.tobytes("png"))
    doc.close()
    return images


def extract_text_vision(
    pdf_path: str,
    api_key: str,
    base_url: str,
    model: str,
    max_pages: int = 30,
    batch_size: int = 2,
) -> str:
    """
    Extract statistical content from a PDF using a vision model.

    Processes pages in small batches to maximize output token budget per page.
    Returns structured markdown with tables and inline statistics.
    """
    if not _FITZ_AVAILABLE:
        raise RuntimeError(
            "pymupdf is not installed. Run: pip install pymupdf"
        )

    images = _pdf_to_images(pdf_path)
    images = images[:max_pages]
    total = len(images)

    if total == 0:
        logger.warning(f"[VisionExtractor] No pages rendered from {pdf_path}")
        return ""

    logger.info(f"[VisionExtractor] {total} pages to process: {pdf_path}")

    client = OpenAI(api_key=api_key, base_url=base_url)
    extracted_parts: List[str] = []

    for start in range(0, total, batch_size):
        batch = images[start : start + batch_size]
        end = start + len(batch)
        label = f"pages {start + 1}–{end}"

        content: list = [
            {
                "type": "text",
                "text": f"{_EXTRACTION_PROMPT}\n\nNow extract from {label}:",
            }
        ]

        for img_bytes in batch:
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64}",
                    "detail": "high",
                },
            })

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=8192,
            )
            chunk = response.choices[0].message.content or ""
            extracted_parts.append(f"\n\n--- {label} ---\n\n{chunk}")
            logger.info(
                f"[VisionExtractor] {label}: extracted {len(chunk)} chars "
                f"(finish={response.choices[0].finish_reason})"
            )
            # Log first 200 chars to help diagnose refusals
            if len(chunk) < 300:
                logger.warning(
                    f"[VisionExtractor] Short response for {label}: {chunk!r}"
                )
        except Exception as exc:
            logger.warning(f"[VisionExtractor] Failed on {label}: {exc}")

    return "\n".join(extracted_parts)


def extract_text_vision_from_bytes(
    pdf_bytes: bytes,
    api_key: str,
    base_url: str,
    model: str,
    max_pages: int = 30,
    batch_size: int = 2,
) -> str:
    """
    Same as extract_text_vision but accepts PDF as raw bytes.
    Writes to a temporary file and cleans up afterwards.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        return extract_text_vision(
            pdf_path=tmp_path,
            api_key=api_key,
            base_url=base_url,
            model=model,
            max_pages=max_pages,
            batch_size=batch_size,
        )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
