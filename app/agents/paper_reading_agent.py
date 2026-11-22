"""
Paper reading nodes — pure Python, no LLM.

Provides two graph nodes:
  manual_ingest_node   — reads uploaded PDF files (Stage 1, manual mode)
  fetch_fulltext_node  — downloads PDFs for search-retrieved papers (Stage 3b)
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import uuid
import csv
from difflib import SequenceMatcher
from html.parser import HTMLParser
from typing import List, Optional, Tuple, TYPE_CHECKING
from urllib.parse import urljoin, urlparse

import requests as _requests

from config import (
    DOWNLOADED_PDF_DIR,
    FULL_TEXT_FETCH_BUDGET,
    FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS,
    FULL_TEXT_USE_BROWSER_FALLBACKS,
    FULL_TEXT_USE_DATABASE_FALLBACKS,
    FULL_TEXT_USE_WEB_SEARCH_FALLBACKS,
    KEENABLE_API_KEY,
    MISTRAL_API_KEY,
    LLAMA_CLOUD_API_KEY,
)
from database_search import fetch_pmc_fulltext, fetch_open_access_pdf_url, keenable_fetch_markdown
from models import PaperRecord
from utils import thread_tracking as _thread_tracking

if TYPE_CHECKING:
    from pipeline_graph import GraphState

logger = logging.getLogger(__name__)


# ── HTML table → Markdown table converter ────────────────────────────────────

class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list = []
        self._row: list = []
        self._cell: list = []
        self._in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"):
            self._in_cell = True
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self._row.append(" ".join(self._cell).strip())
            self._in_cell = False
        elif tag == "tr":
            if self._row:
                self.rows.append(self._row)
            self._row = []

    def handle_data(self, data):
        if self._in_cell:
            self._cell.append(data)


def _html_table_to_md(table_html: str) -> str:
    parser = _TableParser()
    parser.feed(table_html)
    rows = parser.rows
    if not rows:
        return table_html
    col_count = max(len(r) for r in rows)
    rows = [r + [""] * (col_count - len(r)) for r in rows]
    widths = [max(max(len(r[i]) for r in rows), 3) for i in range(col_count)]

    def _row_line(row):
        return "| " + " | ".join(row[i].ljust(widths[i]) for i in range(col_count)) + " |"

    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    lines = [_row_line(rows[0]), sep] + [_row_line(r) for r in rows[1:]]
    return "\n".join(lines)


def _convert_html_tables(text: str) -> str:
    return re.sub(
        r"<table\b[^>]*>.*?</table>",
        lambda m: _html_table_to_md(m.group()),
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


# Telltale phrasing from bot-verification / CAPTCHA / access-denied
# interstitials (Cloudflare, Wiley, Tandfonline, etc.). These pages return a
# 200 with real (short) text, so a plain "did we get non-empty text back?"
# check accepts them as if they were the paper. Length-gated so a genuine,
# much longer article that happens to mention e.g. "CAPTCHA" in passing is
# never rejected on phrase match alone.
_BOT_CHECK_PHRASES = (
    "checking if you are a bot",
    "checking if the site connection is secure",
    "verify you are a human",
    "verify you are not a bot",
    "are not a bot",
    "performing security verification",
    "just a moment",
    "attention required",
    "please enable javascript and cookies",
    "enable javascript to continue",
    "ddos protection by",
    "access denied",
    "cloudflare ray id",
    "please complete the security check",
    "checking your browser before accessing",
    "unusual traffic from your computer",
)


def _looks_like_bot_check_or_error_page(text: str) -> bool:
    """True if `text` is a bot-verification/CAPTCHA/access-denied placeholder
    rather than real article content. Confirmed real-world case: Keenable's
    markdown crawler and raw landing-page fetches both happily return
    Wiley's/Cloudflare's "Performing security verification..." interstitial
    as if it were successfully-fetched full text."""
    if not text:
        return False
    stripped = text.strip()
    if len(stripped) > 1500:
        return False
    lowered = stripped.lower()
    return any(phrase in lowered for phrase in _BOT_CHECK_PHRASES)


class _PdfLinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k.lower(): v for k, v in attrs if k and v}
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])
        if tag == "meta":
            name = (attrs_dict.get("name") or attrs_dict.get("property") or "").lower()
            if name in {"citation_pdf_url", "dc.identifier", "og:pdf"} and attrs_dict.get("content"):
                self.links.append(attrs_dict["content"])


def _is_probable_pdf_url(url: str) -> bool:
    parsed = urlparse(url or "")
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()
    return (
        path.endswith(".pdf")
        or "/pdf/" in path
        or path.endswith("/pdf")
        or "download=pdf" in query
        or "type=pdf" in query
    )


def _extract_pdf_links(html: str, base_url: str) -> list[str]:
    parser = _PdfLinkParser()
    parser.feed(html or "")
    seen: set[str] = set()
    candidates: list[str] = []

    for href in parser.links:
        url = urljoin(base_url, href.strip())
        if not url or url in seen:
            continue
        seen.add(url)
        if _is_probable_pdf_url(url):
            candidates.append(url)

    candidates.sort(key=lambda url: (not urlparse(url).path.lower().endswith(".pdf"), url))
    return candidates[:5]


def _arxiv_pdf_url_from_text(value: str) -> Optional[str]:
    """Return an arXiv PDF URL from an arXiv URL, arXiv: identifier, or record id."""
    text = (value or "").strip()
    if not text:
        return None

    patterns = [
        r"arxiv\.org/(?:abs|pdf)/([^?#\s]+)",
        r"\barxiv:([A-Za-z-]+/\d{7}|\d{4}\.\d{4,5}(?:v\d+)?)\b",
        r"^arxiv:([A-Za-z-]+/\d{7}|\d{4}\.\d{4,5}(?:v\d+)?)$",
        r"^([A-Za-z-]+/\d{7}|\d{4}\.\d{4,5}(?:v\d+)?)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        arxiv_id = match.group(1).strip().removesuffix(".pdf")
        if arxiv_id:
            return f"https://arxiv.org/pdf/{arxiv_id}"
    return None


def _norm_title(title: str) -> str:
    title = re.sub(r"[^\w\s]", " ", (title or "").lower())
    return re.sub(r"\s+", " ", title).strip()


def _metadata_hit_matches_paper(paper: PaperRecord, hit: dict) -> bool:
    paper_title = _norm_title(getattr(paper, "title", ""))
    hit_title = _norm_title(hit.get("title", ""))
    if not paper_title or not hit_title:
        return False
    if paper_title == hit_title:
        return True
    if paper_title in hit_title or hit_title in paper_title:
        shorter = min(len(paper_title), len(hit_title))
        longer = max(len(paper_title), len(hit_title))
        return shorter >= 24 and shorter / longer >= 0.72
    return SequenceMatcher(None, paper_title, hit_title).ratio() >= 0.86


def _dedupe_hits(labeled_hits: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    """Merges candidate hits from every full-text discovery source (arXiv,
    Semantic Scholar, CrossRef, OSF, PubMed, Deep Research, Keenable) into
    one deduplicated pool -- by normalized open-access-PDF/landing-page URL
    and by DOI, in the order given (earlier sources' duplicates of a later
    one are dropped, not the reverse, so the structured academic connectors
    keep priority over general web search when two sources agree on the
    same paper). First occurrence wins; label is kept for logging."""
    seen_urls: set[str] = set()
    seen_dois: set[str] = set()
    out: list[tuple[str, dict]] = []
    for label, hit in labeled_hits:
        url = (hit.get("url") or "").strip().rstrip("/").lower()
        oa = (hit.get("open_access_pdf") or "").strip().rstrip("/").lower()
        doi = (hit.get("doi") or "").strip().lower()
        url_keys = {u for u in (url, oa) if u}
        if doi and doi in seen_dois:
            continue
        if url_keys and url_keys & seen_urls:
            continue
        seen_urls |= url_keys
        if doi:
            seen_dois.add(doi)
        out.append((label, hit))
    return out


try:
    from utils.mineru_mcp_extractor import (
        extract_text_mineru_cloud, extract_text_mineru_cloud_from_bytes,
        extract_text_mineru, extract_text_mineru_from_bytes,
        _UVX as _MINERU_UVX,
    )
    _MINERU_CLOUD_MCP_AVAILABLE = True
    _MINERU_LOCAL_MCP_AVAILABLE = _MINERU_UVX is not None
    if not _MINERU_LOCAL_MCP_AVAILABLE:
        logger.info("[PaperReading] MinerU local MCP skipped: uvx not found (install uv to enable)")
except ImportError as _mineru_import_err:
    logger.warning(f"[PaperReading] MinerU MCP extractor not available: {_mineru_import_err}")
    _MINERU_CLOUD_MCP_AVAILABLE = False
    _MINERU_LOCAL_MCP_AVAILABLE = False

try:
    from utils.llamaparse_extractor import extract_text_llamaparse_from_bytes
    _LLAMAPARSE_AVAILABLE = True
except ImportError:
    _LLAMAPARSE_AVAILABLE = False

try:
    from utils.mistral_ocr_extractor import extract_text_mistral_ocr, extract_text_mistral_ocr_from_bytes
    _MISTRAL_OCR_AVAILABLE = True
except ImportError:
    _MISTRAL_OCR_AVAILABLE = False


def _mineru_api_key() -> str:
    """Read MinerU API key at call time (not at import time) so hot-reloads work."""
    return (
        os.getenv("MinerU_API_KEY")
        or os.getenv("MINERU_API_KEY")
        or ""
    )


def _extract_text_from_path_uncached(path: str) -> str:
    _mineru_key = _mineru_api_key()
    logger.info(
        f"[PaperReading] Extractors: MinerU-cloud={'✓' if _MINERU_CLOUD_MCP_AVAILABLE and _mineru_key else '✗'} "
        f"MinerU-local={'✓' if _MINERU_LOCAL_MCP_AVAILABLE else '✗'} "
        f"LlamaParse={'✓' if _LLAMAPARSE_AVAILABLE and LLAMA_CLOUD_API_KEY else '✗'}"
    )
    # 1. MinerU cloud via MCP (primary — mineru.net REST API, best quality)
    if _MINERU_CLOUD_MCP_AVAILABLE and _mineru_key:
        try:
            text = extract_text_mineru_cloud(path)
            if text and text.strip():
                logger.info("[PaperReading] MinerU cloud MCP succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] MinerU cloud MCP failed: {exc}")

    # 2. MinerU local MCP (offline fallback — local pipeline via uvx)
    if _MINERU_LOCAL_MCP_AVAILABLE:
        try:
            text = extract_text_mineru(path)
            if text and text.strip():
                logger.info("[PaperReading] MinerU local MCP succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] MinerU local MCP failed: {exc}")

    # 3. LlamaParse (cloud fallback)
    if _LLAMAPARSE_AVAILABLE and LLAMA_CLOUD_API_KEY:
        try:
            with open(path, "rb") as f:
                pdf_bytes = f.read()
            text = extract_text_llamaparse_from_bytes(pdf_bytes, api_key=LLAMA_CLOUD_API_KEY)
            if text and text.strip():
                logger.info("[PaperReading] LlamaParse succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] LlamaParse failed: {exc}")

    # 4. Mistral OCR (cloud fallback)
    if _MISTRAL_OCR_AVAILABLE and MISTRAL_API_KEY:
        try:
            text = extract_text_mistral_ocr(pdf_path=path, api_key=MISTRAL_API_KEY)
            if text and text.strip():
                logger.info("[PaperReading] Mistral OCR succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] Mistral OCR failed: {exc}")

    # 5. pypdf fallback
    return _pypdf_from_path(path)


def _extract_text_from_bytes_uncached(pdf_bytes: bytes) -> str:
    _mineru_key = _mineru_api_key()
    # 1. MinerU cloud via MCP (primary)
    if _MINERU_CLOUD_MCP_AVAILABLE and _mineru_key:
        try:
            text = extract_text_mineru_cloud_from_bytes(pdf_bytes)
            if text and text.strip():
                logger.info("[PaperReading] MinerU cloud MCP succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] MinerU cloud MCP (bytes) failed: {exc}")

    # 2. MinerU local MCP (offline fallback)
    if _MINERU_LOCAL_MCP_AVAILABLE:
        try:
            text = extract_text_mineru_from_bytes(pdf_bytes)
            if text and text.strip():
                logger.info("[PaperReading] MinerU local MCP succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] MinerU local MCP (bytes) failed: {exc}")

    # 3. LlamaParse (cloud fallback)
    if _LLAMAPARSE_AVAILABLE and LLAMA_CLOUD_API_KEY:
        try:
            text = extract_text_llamaparse_from_bytes(pdf_bytes, api_key=LLAMA_CLOUD_API_KEY)
            if text and text.strip():
                logger.info("[PaperReading] LlamaParse succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] LlamaParse failed: {exc}")

    # 4. Mistral OCR (cloud fallback)
    if _MISTRAL_OCR_AVAILABLE and MISTRAL_API_KEY:
        try:
            text = extract_text_mistral_ocr_from_bytes(pdf_bytes, api_key=MISTRAL_API_KEY)
            if text and text.strip():
                logger.info("[PaperReading] Mistral OCR succeeded.")
                return text
        except Exception as exc:
            logger.warning(f"[PaperReading] Mistral OCR (bytes) failed: {exc}")

    # 5. pypdf fallback
    return _pypdf_from_bytes(pdf_bytes)


def _pypdf_from_path(path: str) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        return "\n\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as exc:
        logger.error(f"[PaperReading] pypdf failed on {path}: {exc}")
        return ""


def _pypdf_from_bytes(pdf_bytes: bytes) -> str:
    try:
        import io
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        return "\n\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as exc:
        logger.error(f"[PaperReading] pypdf (bytes) failed: {exc}")
        return ""


# ── PDF-text cache (Phase 2 of the infrastructure migration) ────────────────
# Wraps the two dispatch functions above with a Redis cache keyed by content
# hash + a code/config fingerprint -- see caching/pdf_text_cache.py's module
# docstring for the full key scheme and invalidation rules. The extractor
# cascade itself (both _uncached functions' bodies, unchanged above) and all
# 8 call sites elsewhere in this file are untouched -- they call
# `_extract_text_from_path`/`_extract_text_from_bytes`, which now resolve to
# the cached wrappers defined below instead of the raw dispatchers, with no
# change needed at the call sites themselves.

_PDF_CACHE_CODE_HASH = None  # computed lazily on first use, see _pdf_cache_code_hash()


def _pdf_cache_code_hash() -> str:
    global _PDF_CACHE_CODE_HASH
    if _PDF_CACHE_CODE_HASH is None:
        from caching.pdf_text_cache import compute_code_hash
        _PDF_CACHE_CODE_HASH = compute_code_hash(
            _extract_text_from_path_uncached, _extract_text_from_bytes_uncached,
            _pypdf_from_path, _pypdf_from_bytes,
        )
    return _PDF_CACHE_CODE_HASH


def _pdf_cache_cascade() -> list:
    """The ordered list of extractor names actually enabled right now
    (booleans only -- API key VALUES are never part of this, so cache keys
    stay safely loggable). Recomputed per call (cheap) rather than cached
    at import time, matching _mineru_api_key()'s own "read at call time so
    hot-reloads work" convention."""
    key = _mineru_api_key()
    names = []
    if _MINERU_CLOUD_MCP_AVAILABLE and key:
        names.append("mineru_cloud")
    if _MINERU_LOCAL_MCP_AVAILABLE:
        names.append("mineru_local")
    if _LLAMAPARSE_AVAILABLE and LLAMA_CLOUD_API_KEY:
        names.append("llamaparse")
    if _MISTRAL_OCR_AVAILABLE and MISTRAL_API_KEY:
        names.append("mistral_ocr")
    names.append("pypdf")
    return names


def _pdf_cache_lookup_key(raw_bytes: bytes):
    """Returns (sha256_hex, cache_key), or (None, None) if caching is
    disabled -- callers treat that as "skip the cache entirely"."""
    from config import PDF_TEXT_CACHE_ENABLED
    from caching.client import enabled as _redis_enabled
    if not (PDF_TEXT_CACHE_ENABLED and _redis_enabled()):
        return None, None

    import hashlib
    from caching.pdf_text_cache import fingerprint, key_for, installed_versions

    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    fp = fingerprint(_pdf_cache_code_hash(), _pdf_cache_cascade(), installed_versions())
    return sha256_hex, key_for(sha256_hex, fp)


def _extract_text_from_path(path: str) -> str:
    import time
    from config import PDF_TEXT_CACHE_MAX_BYTES
    from caching import pdf_text_cache
    from runctx import current_run_id

    try:
        with open(path, "rb") as f:
            raw_bytes = f.read()
    except Exception:
        # Can't even read the file to hash it -- let the uncached path
        # handle (and report) whatever's wrong with it, exactly as before
        # this cache existed.
        return _extract_text_from_path_uncached(path)

    if len(raw_bytes) > PDF_TEXT_CACHE_MAX_BYTES:
        return _extract_text_from_path_uncached(path)

    sha256_hex, cache_key = _pdf_cache_lookup_key(raw_bytes)
    if cache_key is None:
        return _extract_text_from_path_uncached(path)

    run_id = current_run_id()
    cached = pdf_text_cache.get(cache_key)
    if cached is not None:
        pdf_text_cache.record_event(
            run_id=run_id, content_sha256=sha256_hex, cache_key=cache_key, cache_hit=True,
            extractor=cached.get("extractor"), text_chars=cached.get("chars"),
        )
        return cached["text"]

    t0 = time.monotonic()
    text = _extract_text_from_path_uncached(path)
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    pdf_text_cache.put(cache_key, text)
    pdf_text_cache.record_event(
        run_id=run_id, content_sha256=sha256_hex, cache_key=cache_key, cache_hit=False,
        text_chars=len(text) if text else 0, elapsed_ms=elapsed_ms,
    )
    return text


def _extract_text_from_bytes(pdf_bytes: bytes) -> str:
    import time
    from config import PDF_TEXT_CACHE_MAX_BYTES
    from caching import pdf_text_cache
    from runctx import current_run_id

    if len(pdf_bytes) > PDF_TEXT_CACHE_MAX_BYTES:
        return _extract_text_from_bytes_uncached(pdf_bytes)

    sha256_hex, cache_key = _pdf_cache_lookup_key(pdf_bytes)
    if cache_key is None:
        return _extract_text_from_bytes_uncached(pdf_bytes)

    run_id = current_run_id()
    cached = pdf_text_cache.get(cache_key)
    if cached is not None:
        pdf_text_cache.record_event(
            run_id=run_id, content_sha256=sha256_hex, cache_key=cache_key, cache_hit=True,
            extractor=cached.get("extractor"), text_chars=cached.get("chars"),
        )
        return cached["text"]

    t0 = time.monotonic()
    text = _extract_text_from_bytes_uncached(pdf_bytes)
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    pdf_text_cache.put(cache_key, text)
    pdf_text_cache.record_event(
        run_id=run_id, content_sha256=sha256_hex, cache_key=cache_key, cache_hit=False,
        text_chars=len(text) if text else 0, elapsed_ms=elapsed_ms,
    )
    return text


def manual_ingest_node(state: GraphState) -> dict:
    """Stage 1 (manual mode): extract text from each uploaded PDF file."""
    logger.info("=== STAGE 1: Manual Ingest ===")
    papers: List[PaperRecord] = []
    for path in state.get("paper_files", []):
        path = path.strip()
        if not path or not os.path.isfile(path):
            logger.warning(f"[ManualIngest] File not found: {path}")
            continue
        filename = os.path.basename(path)
        title    = os.path.splitext(filename)[0]
        text     = _convert_html_tables(_extract_text_from_path(path))
        if text.strip():
            output_dir = state.get("output_dir", "")
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in os.path.splitext(filename)[0])[:80]
                with open(os.path.join(output_dir, f"fulltext_{safe_name}.md"), "w", encoding="utf-8") as _fh:
                    _fh.write(text)
        papers.append(PaperRecord(
            id=f"manual:{uuid.uuid4().hex[:8]}",
            title=title, abstract="", authors=[],
            year=0, url=None, source="manual",
            full_text=text.strip() or None,
        ))
        logger.info(f"[ManualIngest] {filename}: {len(text)} chars")
    logger.info(f"[ManualIngest] {len(papers)} PDFs loaded.")
    return {"papers_eligible": papers}


_DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>)]+", flags=re.IGNORECASE)


def _extract_doi_from_text(text: str) -> Optional[str]:
    match = _DOI_PATTERN.search(text or "")
    if not match:
        return None
    return match.group(0).rstrip(".,;)")


def match_uploaded_pdf(extracted_text: str, missing_papers: List[PaperRecord]) -> Optional[PaperRecord]:
    """Match a manually-uploaded PDF's extracted text to one of the papers the
    pipeline couldn't retrieve full text for -- DOI first (found anywhere in
    the PDF text), falling back to fuzzy title matching against the PDF's
    opening text (where a paper's title normally appears)."""
    doi = _extract_doi_from_text(extracted_text)
    if doi:
        for p in missing_papers:
            paper_doi = (getattr(p, "doi", None) or "").strip().lower()
            if paper_doi and paper_doi == doi.lower():
                return p

    head = _norm_title(extracted_text[:3000])
    if not head:
        return None
    best, best_score = None, 0.0
    for p in missing_papers:
        title_norm = _norm_title(p.title)
        if not title_norm:
            continue
        if title_norm in head:
            return p  # exact substring match -- strongest signal
        score = SequenceMatcher(None, title_norm, head[:len(title_norm) + 40]).ratio()
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= 0.6 else None


def ingest_uploaded_fulltext_pdfs(
    pdf_paths: List[str],
    missing_papers: List[PaperRecord],
    output_dir: str,
) -> tuple[List[PaperRecord], List[str]]:
    """Human-in-the-loop paper upload: extract text from manually-uploaded
    PDFs and match each to a paper the pipeline flagged as missing full text.

    Matched papers are returned with `full_text` populated so they can be
    injected into papers_eligible and continue through the normal pipeline
    exactly as if fetch_fulltext_node had retrieved them automatically.
    Returns (matched_papers, unmatched_pdf_paths).
    """
    matched: List[PaperRecord] = []
    unmatched: List[str] = []
    remaining = list(missing_papers)

    for path in pdf_paths:
        if not remaining:
            unmatched.append(path)
            continue
        if not path or not os.path.isfile(path):
            unmatched.append(path)
            continue
        text = _convert_html_tables(_extract_text_from_path(path))
        if not text.strip():
            unmatched.append(path)
            continue
        hit = match_uploaded_pdf(text, remaining)
        if not hit:
            unmatched.append(path)
            continue
        remaining.remove(hit)
        hit.full_text = text[:120_000]
        _save_fulltext(hit.full_text, hit.id, output_dir)
        matched.append(hit)

    return matched, unmatched


USER_DECLINED_REASON = "declined by the user at the paper-selection review"
USER_ADDED_REASON = "added manually by the user at the paper-selection review"


def apply_paper_selection(
    graph_state: dict,
    excluded_ids: List[str],
    pdf_paths: List[str],
    output_dir: str,
) -> tuple[dict, dict]:
    """Human-in-the-loop paper selection right after the search agent.

    * Papers whose id is in `excluded_ids` are removed from papers_eligible
      (they never reach full-text retrieval) and recorded as screened out in
      screening_decisions, so paper_tracking.csv / the PRISMA counts show them
      as declined by the user rather than silently losing them.
    * Each uploaded PDF is text-extracted. If it matches a paper that is still
      selected (by DOI, or by title at the start of the text) the text is
      attached to that paper, so no duplicate is created. Otherwise it becomes
      a new "manual" paper alongside the found ones. Papers that already carry
      full_text skip the automatic full-text fetch.

    Returns (new_graph_state, summary) where summary has the counts
    {"declined", "added", "attached", "unreadable"}.
    """
    state = dict(graph_state)
    excluded = {pid for pid in (excluded_ids or []) if pid}

    papers: List[PaperRecord] = list(state.get("papers_eligible", []))
    screening = dict(state.get("screening_decisions", {}))
    all_retrieved: List[PaperRecord] = list(state.get("all_retrieved_papers", []))

    declined = [p for p in papers if p.id in excluded]
    kept: List[PaperRecord] = [p for p in papers if p.id not in excluded]
    for p in declined:
        screening[p.id] = {"decision": "exclude", "reason": USER_DECLINED_REASON, "title": p.title}

    added = attached = unreadable = 0
    for path in pdf_paths or []:
        path = (path or "").strip()
        if not path or not os.path.isfile(path):
            unreadable += 1
            continue
        text = _convert_html_tables(_extract_text_from_path(path))
        if not text.strip():
            unreadable += 1
            logger.warning(f"[PaperSelection] No text could be extracted from {os.path.basename(path)}.")
            continue
        text = text[:120_000]
        candidates = [p for p in kept if not p.full_text]
        hit = match_uploaded_pdf(text, candidates)
        if hit is not None:
            hit.full_text = text
            _save_fulltext(text, hit.id, output_dir)
            attached += 1
            logger.info(f"[PaperSelection] {os.path.basename(path)} attached to found paper {hit.id}.")
            continue
        title = os.path.splitext(os.path.basename(path))[0]
        # drop the "<8-hex>_" prefix the upload endpoint adds to avoid collisions
        title = re.sub(r"^[0-9a-f]{8}_", "", title)
        paper = PaperRecord(
            id=f"manual:{uuid.uuid4().hex[:8]}",
            title=title, abstract="", authors=[], year=0, url=None,
            source="manual", full_text=text,
        )
        _save_fulltext(text, paper.id, output_dir)
        kept.append(paper)
        all_retrieved.append(paper)
        screening[paper.id] = {"decision": "include", "reason": USER_ADDED_REASON, "title": paper.title}
        added += 1
        logger.info(f"[PaperSelection] {os.path.basename(path)} added as manual paper {paper.id}.")

    state["papers_eligible"] = kept
    state["screening_decisions"] = screening
    state["all_retrieved_papers"] = all_retrieved
    n_scr = state.get("n_screened_excluded", 0)
    if isinstance(n_scr, int) and n_scr >= 0:
        state["n_screened_excluded"] = n_scr + len(declined)
    summary = {"declined": len(declined), "added": added, "attached": attached, "unreadable": unreadable}
    logger.info(f"[PaperSelection] {summary}")
    return state, summary


def _save_fulltext(text: str, paper_id: str, output_dir: str) -> None:
    if not output_dir:
        return
    os.makedirs(output_dir, exist_ok=True)
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in paper_id)[:80]
    with open(os.path.join(output_dir, f"fulltext_{safe_id}.md"), "w", encoding="utf-8") as fh:
        fh.write(text)


def _pdf_output_dir(output_dir: str) -> str:
    if os.path.isabs(DOWNLOADED_PDF_DIR):
        return DOWNLOADED_PDF_DIR
    return os.path.join(output_dir, DOWNLOADED_PDF_DIR)


def _save_pdf(pdf_bytes: bytes, paper_id: str, output_dir: str) -> Optional[str]:
    if not output_dir or not pdf_bytes:
        return None
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in paper_id)[:80] or "paper"
    pdf_dir = _pdf_output_dir(output_dir)
    os.makedirs(pdf_dir, exist_ok=True)
    path = os.path.join(pdf_dir, f"{safe_id}.pdf")
    with open(path, "wb") as fh:
        fh.write(pdf_bytes)
    logger.info(f"[FetchFulltext] saved PDF: {path}")
    return path


def _downloaded_pdf_path(paper_id: str, output_dir: str, suffix: str = "") -> Optional[str]:
    if not output_dir:
        return None
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in paper_id)[:80] or "paper"
    if suffix:
        safe_id = f"{safe_id}_{suffix}"
    pdf_dir = _pdf_output_dir(output_dir)
    os.makedirs(pdf_dir, exist_ok=True)
    return os.path.join(pdf_dir, f"{safe_id}.pdf")


def _download_and_extract(pdf_url: str, paper_id: str = "", output_dir: str = "") -> Optional[str]:
    try:
        resp = _requests.get(pdf_url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        content_type = (resp.headers.get("Content-Type") or "").lower()
        if "pdf" not in content_type and not (resp.content or b"").lstrip().startswith(b"%PDF"):
            logger.warning(
                f"[FetchFulltext] URL did not return a PDF "
                f"(content-type={content_type or 'unknown'}): {pdf_url}"
            )
            return None
        pdf_path = _save_pdf(resp.content, paper_id, output_dir)
        text = _extract_text_from_path(pdf_path) if pdf_path else _extract_text_from_bytes(resp.content)
        if text and text.strip():
            if _looks_like_bot_check_or_error_page(text):
                logger.warning(f"[FetchFulltext] Bot-check/error page, not a real PDF: {pdf_url}")
                return None
            return _convert_html_tables(text.strip())
        logger.warning(f"[FetchFulltext] PDF downloaded but text extraction was empty: {pdf_url}")
    except Exception as exc:
        logger.warning(f"[FetchFulltext] Download failed for {pdf_url}: {exc}")
    return None


def _download_from_returned_url(url: str, paper_id: str = "", output_dir: str = "") -> Optional[str]:
    """Download a PDF from a Deep Research-returned URL or its landing page."""
    if not url:
        return None

    if "arxiv.org/abs/" in url:
        text = _download_and_extract(_arxiv_pdf_url_from_text(url) or "", paper_id, output_dir)
        if text:
            return text

    if _is_probable_pdf_url(url):
        text = _download_and_extract(url, paper_id, output_dir)
        if text:
            return text

    try:
        resp = _requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as exc:
        logger.warning(f"[FetchFulltext] Landing-page fetch failed for {url}: {exc}")
        return None

    content_type = (resp.headers.get("Content-Type") or "").lower()
    if "pdf" in content_type:
        pdf_path = _save_pdf(resp.content, paper_id, output_dir)
        text = _extract_text_from_path(pdf_path) if pdf_path else _extract_text_from_bytes(resp.content)
        if text and text.strip() and not _looks_like_bot_check_or_error_page(text):
            return _convert_html_tables(text.strip())

    if "html" not in content_type and not resp.text:
        return None

    for pdf_url in _extract_pdf_links(resp.text, url):
        text = _download_and_extract(pdf_url, paper_id, output_dir)
        if text:
            return text
    return None


def _keenable_fetch_and_extract(url: str) -> Optional[str]:
    """Extract a landing page's content as clean markdown via Keenable's
    /v1/fetch (see database_search.keenable_fetch_markdown) -- one HTTP
    call, no headless browser. Tried BEFORE the Playwright browser fallback
    below (cheaper, faster); Playwright still runs if this doesn't produce
    usable text, since Keenable's crawler may not clear the same JS
    rendering / bot-check obstacles a real browser does."""
    if not KEENABLE_API_KEY or not url:
        return None
    content = keenable_fetch_markdown(url)
    if not content:
        return None
    if _looks_like_bot_check_or_error_page(content):
        logger.warning(f"[FetchFulltext] Keenable fetch returned a bot-check/error page, not the article: {url}")
        return None
    return _convert_html_tables(content)


def _event_loop_already_running() -> bool:
    """True if the current thread has a running asyncio event loop.

    Playwright's sync API cannot run in that situation -- it doesn't just
    raise "This event loop is already running" cleanly, it can leave its
    internal driver dispatcher in a broken state so a LATER call from the
    same thread hangs indefinitely instead of raising. This dashboard runs
    the pipeline via threading.Thread inside a FastAPI/uvicorn app, a known
    trigger for this even from a background thread. Detect and skip instead
    of risking that hang."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return False
    return loop.is_running()


def _browser_download_and_extract(url: str, paper_id: str = "", output_dir: str = "") -> Optional[str]:
    """Render an open landing page and try normal browser-visible PDF downloads."""
    if not FULL_TEXT_USE_BROWSER_FALLBACKS or not url:
        return None

    if _event_loop_already_running():
        logger.warning(
            f"[FetchFulltext] Browser fallback skipped for {url} -- an asyncio "
            f"event loop is already running in this thread, which Playwright's "
            f"sync API can't handle safely."
        )
        return None

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        logger.warning(f"[FetchFulltext] Browser fallback unavailable: {exc}")
        return None

    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context(
                accept_downloads=True,
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                ),
            )
            page = context.new_page()
            response = page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_timeout(1500)

            if response:
                content_type = (response.headers.get("content-type") or "").lower()
                if "pdf" in content_type:
                    body = response.body()
                    pdf_path = _save_pdf(body, paper_id, output_dir)
                    text = _extract_text_from_path(pdf_path) if pdf_path else _extract_text_from_bytes(body)
                    if text and text.strip() and not _looks_like_bot_check_or_error_page(text):
                        return _convert_html_tables(text.strip())

            candidates = page.evaluate(
                """() => {
                    const urls = [];
                    for (const meta of document.querySelectorAll(
                        'meta[name="citation_pdf_url"], meta[property="citation_pdf_url"], meta[name="dc.identifier"], meta[property="og:pdf"]'
                    )) {
                        const value = meta.getAttribute('content');
                        if (value) urls.push(value);
                    }
                    for (const a of document.querySelectorAll('a[href]')) {
                        const href = a.getAttribute('href');
                        const text = (a.innerText || a.getAttribute('aria-label') || '').toLowerCase();
                        if (href && (/pdf|download|full.?text/.test(href.toLowerCase()) || /pdf|download|full text/.test(text))) {
                            urls.push(href);
                        }
                    }
                    return Array.from(new Set(urls)).slice(0, 12);
                }"""
            ) or []

            for raw_url in candidates:
                candidate = urljoin(page.url or url, str(raw_url))
                text = _download_and_extract(candidate, paper_id, output_dir)
                if text:
                    logger.info(f"[FetchFulltext] [{paper_id}] via browser-discovered PDF link")
                    return text

            click_selectors = [
                "a:has-text('PDF')",
                "a:has-text('Download')",
                "a:has-text('Full text')",
                "button:has-text('PDF')",
                "button:has-text('Download')",
            ]
            for selector in click_selectors:
                loc = page.locator(selector)
                count = min(loc.count(), 5)
                for idx in range(count):
                    try:
                        with page.expect_download(timeout=7_000) as download_info:
                            loc.nth(idx).click(timeout=5_000)
                        download = download_info.value
                        pdf_path = _downloaded_pdf_path(paper_id, output_dir, "browser")
                        if not pdf_path:
                            return None
                        download.save_as(pdf_path)
                        text = _extract_text_from_path(pdf_path)
                        if text and text.strip() and not _looks_like_bot_check_or_error_page(text):
                            logger.info(f"[FetchFulltext] [{paper_id}] via browser download click")
                            return _convert_html_tables(text.strip())
                    except PlaywrightTimeoutError:
                        continue
                    except Exception as exc:
                        logger.debug(f"[FetchFulltext] Browser click failed ({selector}): {exc}")
                        continue

            return None
    except Exception as exc:
        logger.warning(f"[FetchFulltext] Browser fallback failed for {url}: {exc}")
        return None
    finally:
        try:
            if browser:
                browser.close()
        except Exception:
            pass


def _doi_from_paper(paper: PaperRecord) -> str:
    doi = (getattr(paper, "doi", None) or "").strip()
    if not doi and paper.url and "doi.org/" in (paper.url or ""):
        doi = paper.url.split("doi.org/")[-1].strip()
    return doi


def _append_fetch_attempt(output_dir: str, rows: list[dict]) -> None:
    """Append full-text retrieval attempts for debugging empty download folders."""
    if not output_dir or not rows:
        return
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "fulltext_fetch_attempts.csv")
    header = ["paper_id", "title", "strategy", "url", "success"]
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in header})


def _web_search_fulltext_candidates(paper: PaperRecord) -> list[dict]:
    """Use Deep Research web search as a last-resort full-text finder."""
    if not FULL_TEXT_USE_WEB_SEARCH_FALLBACKS or not paper.title:
        return []
    try:
        from database_search import search_deep_research
        start_year = max(1900, (paper.year or 0) - 1) if paper.year else 1900
        query = f'"{paper.title}" PDF full text'
        return search_deep_research(query, max_results=3, start_year=start_year)
    except Exception as exc:
        logger.debug(f"[FetchFulltext] Web-search full-text fallback failed: {exc}")
        return []


def fetch_fulltext_node(state: GraphState) -> dict:
    """Stage 3b (search mode): download full text for each paper using multiple strategies.

    Papers for which no full text can be located are dropped — they do not
    proceed to eligibility/extraction; abstract-only papers are no longer
    carried forward.
    """
    logger.info("=== STAGE 3b: Full-Text Fetch ===")
    papers: List[PaperRecord] = list(state.get("papers_eligible", []))
    output_dir = state.get("output_dir", "")
    if output_dir:
        os.makedirs(_pdf_output_dir(output_dir), exist_ok=True)
    fetched = 0
    attempted = 0
    kept: List[PaperRecord] = []
    no_fulltext: List[str] = []  # paper_ids dropped because no full text could be found
    no_fulltext_reasons: dict[str, str] = {}

    for paper in papers:
        if paper.full_text:
            kept.append(paper)
            continue

        pid = paper.id

        if FULL_TEXT_FETCH_BUDGET >= 0 and attempted >= FULL_TEXT_FETCH_BUDGET:
            no_fulltext.append(pid)
            no_fulltext_reasons[pid] = (
                f"full-text fetch budget exhausted before attempt "
                f"(budget={FULL_TEXT_FETCH_BUDGET})"
            )
            logger.info(
                f"[FetchFulltext] [{pid}] skipped — full-text fetch budget "
                f"exhausted ({FULL_TEXT_FETCH_BUDGET} attempted)."
            )
            continue

        attempted += 1

        # Run this paper's whole retrieval cascade in its own thread with a
        # hard wall-clock cap -- see FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS.
        # Python threads can't be forcibly killed, so a timed-out worker is
        # simply abandoned (left running as a daemon thread) rather than
        # joined again; the pipeline moves on immediately either way instead
        # of one wedged paper stalling every paper after it.
        result_box: dict = {"done": False}
        # spawn_tracked_thread (not a bare threading.Thread) so this
        # worker's log records still reach the run's live SSE log stream --
        # see utils/thread_tracking.py's docstring for why a plain thread
        # here made Stage 3b's progress invisible in the UI.
        worker = _thread_tracking.spawn_tracked_thread(
            target=_fetch_fulltext_worker,
            args=(paper, output_dir, result_box),
            daemon=True,
        )
        worker.join(timeout=FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS)

        if result_box.get("done"):
            text = result_box["text"]
            fetch_attempts = result_box["fetch_attempts"]
        else:
            logger.warning(
                f"[FetchFulltext] [{pid}] exceeded the "
                f"{FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS}s per-paper timeout -- "
                "abandoning this paper (its fetch thread may still be running "
                "in the background) and moving on to the next one."
            )
            text = None
            fetch_attempts = [{
                "paper_id": pid,
                "title": paper.title,
                "strategy": "per-paper timeout",
                "url": "",
                "success": False,
            }]

        if text:
            paper.full_text = text[:120_000]
            fetched += 1
            _save_fulltext(paper.full_text, pid, output_dir)
            kept.append(paper)
        else:
            no_fulltext.append(pid)
            no_fulltext_reasons[pid] = (
                f"exceeded {FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS}s per-paper timeout"
                if fetch_attempts and fetch_attempts[-1]["strategy"] == "per-paper timeout"
                else "no full text available from any retrieval strategy"
            )
            logger.debug(f"[FetchFulltext] [{pid}] no full text found — dropping paper")
        _append_fetch_attempt(output_dir, fetch_attempts)

    logger.info(
        f"[FetchFulltext] {fetched}/{len(papers)} papers got full text "
        f"({attempted} fetch attempts, budget={FULL_TEXT_FETCH_BUDGET}; "
        f"{len(no_fulltext)} dropped — no full text available or budgeted out)."
    )
    return {
        "papers_eligible": kept,
        "papers_no_fulltext": no_fulltext,
        "papers_no_fulltext_reasons": no_fulltext_reasons,
    }


def _fetch_fulltext_worker(paper: PaperRecord, output_dir: str, result_box: dict) -> None:
    """Runs _fetch_fulltext_for_paper() and writes its outcome into
    result_box rather than returning it, so fetch_fulltext_node's caller can
    read whatever's there after a bounded wait even if this thread itself
    never finishes."""
    text, fetch_attempts = _fetch_fulltext_for_paper(paper, output_dir)
    result_box["text"] = text
    result_box["fetch_attempts"] = fetch_attempts
    result_box["done"] = True


def _fetch_fulltext_for_paper(paper: PaperRecord, output_dir: str) -> Tuple[Optional[str], list[dict]]:
    """The full multi-strategy full-text retrieval cascade for one paper --
    extracted from fetch_fulltext_node so it can be run in a timeout-bounded
    background thread (see _fetch_fulltext_worker) instead of inline in the
    main per-paper loop. Behavior is unchanged from before the split."""
    text: Optional[str] = None
    pid = paper.id
    tried_urls: set = set()  # avoid retrying the same URL within one paper
    fetch_attempts: list[dict] = []
    # Populated by Strategy 1's structured-academic-connector lookups
    # (gated by FULL_TEXT_USE_DATABASE_FALLBACKS) AND by Keenable/Deep
    # Research below (each independently gated) -- one shared pool so
    # every search-based discovery source is merged/validated/
    # deduplicated together. Declared here, not inside either gate, so
    # neither source's presence depends on the other's flag.
    labeled_hits: list[tuple[str, dict]] = []

    def _try_url(url: str, label: str) -> Optional[str]:
        if not url or url in tried_urls:
            return None
        tried_urls.add(url)
        result = _download_and_extract(url, pid, output_dir)
        fetch_attempts.append({
            "paper_id": pid,
            "title": paper.title,
            "strategy": label,
            "url": url,
            "success": bool(result),
        })
        if result:
            logger.info(f"[FetchFulltext] [{pid}] via {label}")
        return result

    # ── Strategy 1: database/index lookups from metadata ──────────────────
    if FULL_TEXT_USE_DATABASE_FALLBACKS:
        arxiv_pdf = (
            _arxiv_pdf_url_from_text(paper.url or "")
            or _arxiv_pdf_url_from_text(pid)
        )
        if arxiv_pdf:
            text = _try_url(arxiv_pdf, "arXiv metadata")

        if not text and pid.startswith("pubmed:"):
            pmid = pid.split("pubmed:")[-1]
            try:
                pmc_text = fetch_pmc_fulltext(pmid)
                if pmc_text and pmc_text.strip():
                    text = _convert_html_tables(pmc_text.strip())
                    logger.info(f"[FetchFulltext] [{pid}] via PMC full text")
            except Exception as exc:
                logger.debug(f"[FetchFulltext] PMC not available for {pmid}: {exc}")

        if not text and paper.title:
            try:
                from database_search import (
                    search_arxiv,
                    search_semantic_scholar,
                    search_crossref,
                    search_osf,
                    search_pubmed,
                )
                db_searchers = [
                    ("arXiv", search_arxiv),
                    ("Semantic Scholar", search_semantic_scholar),
                    ("CrossRef", search_crossref),
                    ("OSF", search_osf),
                    ("PubMed", search_pubmed),
                ]
                start_year = max(1900, (paper.year or 0) - 1) if paper.year else 1900
                for db_label, db_searcher in db_searchers:
                    try:
                        hits = db_searcher(paper.title, max_results=3, start_year=start_year)
                    except Exception as exc:
                        logger.debug(f"[FetchFulltext] {db_label} metadata lookup failed: {exc}")
                        continue
                    for hit in hits:
                        if _metadata_hit_matches_paper(paper, hit):
                            labeled_hits.append((db_label, hit))
            except Exception as exc:
                logger.debug(f"[FetchFulltext] Database metadata lookup failed: {exc}")

        if not text:
            doi = _doi_from_paper(paper)
            if doi:
                oa_url = fetch_open_access_pdf_url(doi)
                if oa_url:
                    text = _try_url(oa_url, f"Unpaywall ({doi})")

    # ── Strategy 1b: merged search-based discovery pool ────────────────────
    # Every search-based discovery source -- the structured academic
    # connectors collected into labeled_hits above (gated by
    # FULL_TEXT_USE_DATABASE_FALLBACKS) AND general web search (Deep
    # Research, Keenable, each independently gated by its own flag/key,
    # deliberately NOT coupled to FULL_TEXT_USE_DATABASE_FALLBACKS) --
    # feeds ONE merged candidate pool: validated with the same
    # title-match check (_metadata_hit_matches_paper) and deduplicated
    # by URL/DOI (_dedupe_hits), rather than the general web-search
    # sources only running once every structured source has failed.
    if not text and paper.title:
        try:
            from database_search import search_keenable
            start_year = max(1900, (paper.year or 0) - 1) if paper.year else 1900
            for hit in search_keenable(paper.title, max_results=3, start_year=start_year):
                if _metadata_hit_matches_paper(paper, hit):
                    labeled_hits.append(("Keenable", hit))
        except Exception as exc:
            logger.debug(f"[FetchFulltext] Keenable metadata lookup failed: {exc}")
        for hit in _web_search_fulltext_candidates(paper):
            if _metadata_hit_matches_paper(paper, hit):
                labeled_hits.append(("Deep Research", hit))

    if not text and labeled_hits:
        _GENERAL_WEB_SEARCH_LABELS = ("Deep Research", "Keenable")
        for db_label, hit in _dedupe_hits(labeled_hits):
            if hit.get("open_access_pdf"):
                text = _try_url(hit["open_access_pdf"], f"{db_label} PDF lookup")
            if not text and hit.get("url") and "arxiv.org/abs/" in hit["url"]:
                text = _download_from_returned_url(hit["url"], pid, output_dir)
                fetch_attempts.append({
                    "paper_id": pid,
                    "title": paper.title,
                    "strategy": f"{db_label} arXiv URL",
                    "url": hit["url"],
                    "success": bool(text),
                })
                if text:
                    logger.info(f"[FetchFulltext] [{pid}] via {db_label} arXiv URL")
            hit_id = hit.get("id") or ""
            if not text and hit_id.startswith("pubmed:"):
                pmid = hit_id.split("pubmed:")[-1]
                pmc_text = fetch_pmc_fulltext(pmid)
                if pmc_text and pmc_text.strip():
                    text = _convert_html_tables(pmc_text.strip())
                    logger.info(f"[FetchFulltext] [{pid}] via {db_label} PMC lookup")
            if not text and hit.get("doi"):
                oa_url = fetch_open_access_pdf_url(hit["doi"])
                if oa_url:
                    text = _try_url(oa_url, f"{db_label} DOI lookup")
            if not text and hit.get("url") and db_label in _GENERAL_WEB_SEARCH_LABELS:
                # General-web-search hits (not structured academic
                # metadata) also try their bare returned URL/landing
                # page -- the old Deep-Research-only "web-search
                # fallback" strategy's behavior, now extended to Keenable.
                text = _download_from_returned_url(hit["url"], pid, output_dir)
                fetch_attempts.append({
                    "paper_id": pid,
                    "title": paper.title,
                    "strategy": f"{db_label} URL",
                    "url": hit["url"],
                    "success": bool(text),
                })
                if text:
                    logger.info(f"[FetchFulltext] [{pid}] via {db_label} URL")
            if text:
                break

    # ── Strategy 2: explicit PDF URL returned by the paper finder ─────────
    pdf_url = getattr(paper, "pdf_url", None)
    if not text and pdf_url:
        text = _try_url(pdf_url, "pdf_url")

    # ── Strategy 3: URL returned by Deep Research / search result ─────────
    returned_url = getattr(paper, "url", None)
    if not text and returned_url and returned_url not in tried_urls:
        tried_urls.add(returned_url)
        text = _download_from_returned_url(returned_url, pid, output_dir)
        fetch_attempts.append({
            "paper_id": pid,
            "title": paper.title,
            "strategy": "returned URL",
            "url": returned_url,
            "success": bool(text),
        })
        if text:
            logger.info(f"[FetchFulltext] [{pid}] via returned URL")

    # (Deep Research / Keenable web-search candidates are now merged
    # into Strategy 1's pool above, not a separate later stage --
    # see _dedupe_hits() and the comment there.)

    # ── Strategy 4: Keenable landing-page extraction (no browser) ─────────
    if not text and KEENABLE_API_KEY:
        keenable_urls = []
        if returned_url:
            keenable_urls.append(returned_url)
        doi = _doi_from_paper(paper)
        if doi:
            keenable_urls.append(f"https://doi.org/{doi}")
        for k_url in dict.fromkeys(keenable_urls):
            text = _keenable_fetch_and_extract(k_url)
            fetch_attempts.append({
                "paper_id": pid,
                "title": paper.title,
                "strategy": "Keenable fetch",
                "url": k_url,
                "success": bool(text),
            })
            if text:
                logger.info(f"[FetchFulltext] [{pid}] via Keenable fetch")
                break

    # ── Strategy 5: browser fallback for JS-rendered open PDF links ───────
    if not text and FULL_TEXT_USE_BROWSER_FALLBACKS:
        browser_urls = []
        if returned_url:
            browser_urls.append(returned_url)
        doi = _doi_from_paper(paper)
        if doi:
            browser_urls.append(f"https://doi.org/{doi}")
        for browser_url in dict.fromkeys(browser_urls):
            text = _browser_download_and_extract(browser_url, pid, output_dir)
            fetch_attempts.append({
                "paper_id": pid,
                "title": paper.title,
                "strategy": "browser fallback",
                "url": browser_url,
                "success": bool(text),
            })
            if text:
                logger.info(f"[FetchFulltext] [{pid}] via browser fallback")
                break

    # ── Strategy 6: DOI lookup if database fallbacks are disabled ─────────
    if not text and not FULL_TEXT_USE_DATABASE_FALLBACKS:
        doi = _doi_from_paper(paper)
        if doi:
            oa_url = fetch_open_access_pdf_url(doi)
            if oa_url:
                text = _try_url(oa_url, f"Unpaywall ({doi})")

    return text, fetch_attempts
