"""The mechanism by which background work (PDF-cache events today; run
lifecycle logging in Phase 3/4) gets attributed to a `run_id` without any
call site needing an explicit run_id parameter threaded through it -- e.g.
agents/paper_reading_agent.py's PDF extractors call caching code that reads
this ContextVar, with no run_id in their own signature and no awareness
that runs/caching/Postgres exist at all.

A ContextVar (not a plain global) so this is safe under both today's
threading.Thread-per-run execution and Celery's per-task execution --
each run's context is isolated from any other run's, including concurrent
ones on the same process.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from typing import Iterator, Optional

_current_run_id: ContextVar[Optional[str]] = ContextVar("current_run_id", default=None)


def current_run_id() -> Optional[str]:
    return _current_run_id.get()


@contextlib.contextmanager
def run_context(run_id: Optional[str]) -> Iterator[None]:
    """Sets the current run id for the duration of the `with` block (and
    anything it calls, including across thread-pool boundaries that copy
    context, but NOT across a brand-new thread started without copying
    context -- see threading.Thread's run() using contextvars.copy_context()
    if that ever matters for a future call site)."""
    token = _current_run_id.set(run_id)
    try:
        yield
    finally:
        _current_run_id.reset(token)
