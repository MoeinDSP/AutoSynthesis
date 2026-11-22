"""AutoSynthesis caching layer (Redis) -- Phase 2 of the infrastructure
migration. Currently one cache: `pdf_text_cache` (parsed-PDF full text,
keyed by content hash + a code/config fingerprint -- see its own module
docstring).

Public surface: `from caching import pdf_text_cache`. Everything degrades
to a safe no-op / cache-miss when `config.REDIS_URL` is empty or Redis is
unreachable -- see `caching/client.py`'s `safe_*` helpers. No file under
`agents/` imports Redis directly; only `pdf_text_cache`'s functions.
"""

from caching.client import enabled  # noqa: F401
from caching import pdf_text_cache  # noqa: F401

__all__ = ["enabled", "pdf_text_cache"]
