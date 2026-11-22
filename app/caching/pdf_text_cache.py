"""PDF full-text extraction cache -- the highest-priority cache in the
infrastructure migration plan. Wraps agents/paper_reading_agent.py's two
extractor dispatch functions (see that file's `_extract_text_from_path`/
`_extract_text_from_bytes`) so an identical PDF is never re-parsed twice.

Key scheme:
    autosynthesis:pdf_text:{PDF_TEXT_CACHE_VERSION}:{fingerprint}:{sha256}

`fingerprint` is a 16-hex-char digest over:
  - code_hash: sha256 of the extractor dispatch functions' OWN source (via
    inspect.getsource, computed once at import by the caller) -- the
    AUTOMATIC half of "code changes must not return stale results": edit
    the cascade order or any inline extractor logic, every key changes.
  - cascade: the ordered list of *enabled* extractor names (booleans only
    -- e.g. "mineru_cloud" is present or absent depending on whether its
    API key is set, but the key's VALUE is never hashed, so cache keys stay
    safely loggable).
  - module_versions: best-effort installed versions of the extractor
    libraries (pypdf/pymupdf/mistralai/mcp) -- catches a library upgrade
    changing behavior even when this repo's own code didn't change.
  - PDF_TEXT_CACHE_VERSION (config.py): the MANUAL half -- bump it whenever
    utils/mineru_*.py, utils/llamaparse_extractor.py, or
    utils/mistral_ocr_extractor.py change in a way that alters extracted
    text (those helper modules aren't covered by code_hash, which only
    hashes the DISPATCH functions in agents/paper_reading_agent.py).

TTL: none. Content-and-code-addressed keys can never go stale by
definition -- an entry is either an exact match for this exact input under
this exact code, or it isn't found at all. Memory is bounded by Redis's own
`maxmemory` + `allkeys-lru` (see docker-compose.yml's redis service)
instead -- evicting a cache entry only costs a re-parse; a wrong TTL
guess would either waste memory or force needless re-parses.

Never caches LLM outputs -- see this package's __init__ docstring and the
migration plan's explicit non-goal: no reliable way to version
model/prompt changes to invalidate on, so caching them risks silently
returning stale results.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
from typing import Any, Callable, Dict, List, Optional

import config
from caching.client import safe_get, safe_set, safe_incr

logger = logging.getLogger(__name__)

_KEY_PREFIX = "autosynthesis:pdf_text"
_STATS_HITS_KEY = "autosynthesis:stats:pdf_cache:hits"
_STATS_MISSES_KEY = "autosynthesis:stats:pdf_cache:misses"


def compute_code_hash(*functions: Callable) -> str:
    """sha256 over the concatenated source of every function passed in.
    Called ONCE at import time by agents/paper_reading_agent.py with its
    own extractor dispatch functions -- see that file."""
    import inspect

    parts = []
    for fn in functions:
        try:
            parts.append(inspect.getsource(fn))
        except (OSError, TypeError):
            # Can't read source (e.g. running from a frozen/compiled
            # build) -- fall back to the function's qualified name so the
            # hash is still deterministic, just less precise.
            parts.append(getattr(fn, "__qualname__", str(fn)))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def installed_versions(package_names: Optional[List[str]] = None) -> Dict[str, str]:
    """Best-effort installed version of each named package (empty string if
    not found/not installed) -- part of the fingerprint so a library
    upgrade invalidates old cache entries even without a code change."""
    import importlib.metadata

    names = package_names or ["pypdf", "pymupdf", "mistralai", "mcp"]
    out = {}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            out[name] = ""
    return out


def fingerprint(code_hash: str, cascade: List[str], module_versions: Dict[str, str]) -> str:
    payload = {"code_hash": code_hash, "cascade": cascade, "module_versions": module_versions}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def key_for(sha256_hex: str, fingerprint_str: str) -> str:
    return f"{_KEY_PREFIX}:{config.PDF_TEXT_CACHE_VERSION}:{fingerprint_str}:{sha256_hex}"


def get(key: str) -> Optional[Dict[str, Any]]:
    """Returns the stored {"text","extractor","chars","created_at",...}
    dict on a hit, or None on a miss (including a disabled/unreachable
    cache -- indistinguishable from a genuine miss to the caller, by
    design: the caller always just falls through to re-extraction)."""
    raw = safe_get(key, db=config.REDIS_CACHE_DB)
    if raw is None:
        return None
    try:
        return json.loads(gzip.decompress(raw))
    except Exception as exc:  # noqa: BLE001 -- a corrupt/foreign value must never crash a run
        logger.warning("[PDFCache] Failed to decode cached value for %s, treating as a miss: %s", key, exc)
        return None


def put(key: str, text: str, extractor: Optional[str] = None) -> None:
    if not text or not text.strip():
        return  # never cache an empty/failed extraction
    import datetime as dt

    value = {
        "text": text, "extractor": extractor, "chars": len(text),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    payload = gzip.compress(json.dumps(value).encode("utf-8"))
    ttl = config.PDF_TEXT_CACHE_TTL_SECONDS or None
    safe_set(key, payload, db=config.REDIS_CACHE_DB, ex=ttl)


def record_event(
    *, run_id: Optional[str], content_sha256: str, cache_key: str, cache_hit: bool,
    extractor: Optional[str] = None, text_chars: Optional[int] = None, elapsed_ms: Optional[int] = None,
) -> None:
    """Records a hit/miss 3 ways, per the migration plan: (1) a structured
    log line (flows into the existing SSE/stage-log mechanism for free --
    no new UI work needed to see cache activity in a run's log), (2) a
    Redis counter (best-effort, for a quick global rate), (3) a
    pdf_extraction_events Postgres row (the durable source for the measured
    speedup number -- safe no-op if persistence is disabled, see
    persistence/db.py's @safe decorator)."""
    label = "hit" if cache_hit else "miss"
    logger.info(
        "[PDFCache] %s sha=%s chars=%s elapsed_ms=%s key=%s",
        label, content_sha256[:12], text_chars, elapsed_ms, cache_key,
    )
    safe_incr(_STATS_HITS_KEY if cache_hit else _STATS_MISSES_KEY, db=config.REDIS_EVENTS_DB)

    try:
        from persistence import run_store
        run_store.record_pdf_extraction_event(
            content_sha256, cache_key, cache_hit,
            run_id=run_id, extractor=extractor, text_chars=text_chars, elapsed_ms=elapsed_ms,
        )
    except Exception as exc:  # noqa: BLE001 -- persistence is optional, must never break extraction
        logger.debug("[PDFCache] record_pdf_extraction_event skipped: %s", exc)
