"""AutoSynthesis persistence layer (PostgreSQL) -- Phase 1 of the
infrastructure migration described in the plan this session implemented.

Public surface -- nothing outside this package should reach past it:
    from persistence import run_store
    from persistence.db import enabled

Every function in `run_store` is a no-op (returns None / does nothing) when
`config.DATABASE_URL` is empty, so callers never need to branch on whether
persistence is configured -- see db.py's `@safe` decorator. No file under
`agents/` imports anything from this package; all writes happen at run
lifecycle boundaries in `run_service.py` (Phase 3), reading the `GraphState`
dict the graph already returns.
"""

from persistence.db import enabled  # noqa: F401
from persistence import run_store  # noqa: F401

__all__ = ["enabled", "run_store"]
