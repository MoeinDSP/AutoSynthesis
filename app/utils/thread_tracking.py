"""Parent/child thread registry used to keep the live SSE pipeline log
working across worker threads spawned mid-pipeline (e.g. paper_reading_agent's
per-paper full-text-fetch timeout worker, see FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS).

run_service.py's `_SSEHandler` forwards a log record to a session's log
stream only if the record was emitted by that session's pipeline thread
(`record.thread == self.thread_id`) -- this is what keeps two users' runs
from bleeding into each other's live log. But a pipeline stage that offloads
work to a plain `threading.Thread(...).start()` produces log records whose
`record.thread` is that *new* thread's id, which never matches and gets
silently dropped by `_SSEHandler.emit` -- the UI's Pipeline Log panel then
looks stuck (e.g. at "STAGE 3b: Full-Text Fetch") even though the backend is
working fine (visible in `docker logs`, which isn't filtered this way).

Fix: spawn such worker threads via `spawn_tracked_thread` below instead of
bare `threading.Thread(...).start()`. It records the parent->child link so
`_SSEHandler.emit` can also accept records from any (transitive) descendant
of its owning thread, not just that exact thread.
"""

from __future__ import annotations

import threading
from typing import Optional

_lock = threading.Lock()
_children: dict[int, set[int]] = {}


def spawn_tracked_thread(
    target,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    daemon: bool = True,
    name: Optional[str] = None,
) -> threading.Thread:
    """Start `target` in a new thread, registered as a logging child of the
    calling thread. Use this for any thread spawned from inside a pipeline
    stage so its log records still reach the run's live log stream -- see
    module docstring."""
    parent = threading.get_ident()
    ready = threading.Event()
    ident_box: dict = {}

    def _wrapper(*a, **kw):
        # Block until the parent has recorded our thread id -- otherwise a
        # log line emitted right at the top of `target` could race
        # registration below and get silently dropped by _SSEHandler.
        ready.wait()
        try:
            return target(*a, **kw)
        finally:
            # De-register as soon as our actual work is done, not only when
            # the whole run eventually detaches (clear_descendants). OS
            # thread idents get recycled quickly (observed within the same
            # test process), so leaving a finished child's ident registered
            # for the rest of the run risks a LATER, unrelated thread that
            # happens to reuse that exact id being misread as our
            # descendant -- i.e. its log lines leaking into this session.
            with _lock:
                _children.get(parent, set()).discard(ident_box["ident"])

    thread = threading.Thread(
        target=_wrapper, args=args, kwargs=kwargs or {}, daemon=daemon, name=name
    )
    thread.start()  # CPython blocks here until thread.ident is populated
    ident_box["ident"] = thread.ident
    with _lock:
        _children.setdefault(parent, set()).add(thread.ident)
    ready.set()
    return thread


def is_descendant(thread_ident: int, ancestor_ident: int) -> bool:
    """True if `thread_ident` was spawned (directly or transitively via
    further spawn_tracked_thread calls) from a call chain rooted at
    `ancestor_ident`."""
    with _lock:
        seen: set[int] = set()
        stack = [ancestor_ident]
        while stack:
            cur = stack.pop()
            for child in _children.get(cur, ()):
                if child == thread_ident:
                    return True
                if child not in seen:
                    seen.add(child)
                    stack.append(child)
    return False


def clear_descendants(ancestor_ident: int) -> None:
    """Drop all tracked descendants rooted at `ancestor_ident` -- call once
    the owning pipeline run has finished (e.g. alongside
    run_service.py's `_detach_handler`) so the registry doesn't grow
    unbounded across many runs over a long-lived server process."""
    with _lock:
        seen: set[int] = set()
        stack = [ancestor_ident]
        while stack:
            cur = stack.pop()
            for child in _children.pop(cur, ()):
                if child not in seen:
                    seen.add(child)
                    stack.append(child)
