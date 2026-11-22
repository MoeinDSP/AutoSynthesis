"""Celery task wrappers -- Phase 4 of the infrastructure migration.

Each task is a thin shim: claim the run (the REAL anti-duplicate-execution
guard for this backend -- see celery_app.py's `task_acks_late=False`
comment for why Postgres's atomic conditional UPDATE, not broker
redelivery semantics, is what's authoritative here), then call straight
into run_service's backend-agnostic execute_* functions -- the exact same
code dashboard.py's threading.Thread calls under the (default) thread
backend. See run_service.py's module docstring for the full architecture.

Payloads are deliberately just a run_id plus the same small set of
primitive args dashboard.py's routes already pass to threading.Thread --
never the multi-MB GraphState itself, which lives in Postgres
(run_pause_states), not RabbitMQ. `orchestrator`/`agents`/`run_service`
(which pulls in rpy2/LangGraph/Playwright) are imported lazily inside each
task body, not at module level, to keep celery_app.py's prefork parent
process import-light -- matching the pattern run_service.py's own
execute_* functions already use for `orchestrator`.
"""

from __future__ import annotations

import logging

from celery_app import app
from persistence import run_store
from persistence.db import enabled as _db_enabled

logger = logging.getLogger(__name__)


def _claim_or_skip(run_id: str, from_status: str, task_id: str) -> bool:
    """Returns True iff this task invocation should proceed with real work.

    Unlike the thread backend (guarded by dashboard.py's in-memory
    `pipeline["running"]` check, single-process only), a celery worker is a
    separate OS process with no shared in-memory state -- Postgres's atomic
    conditional UPDATE (`run_store.claim_run`) is the only thing that can
    stop two deliveries of the same run_id (a redelivery, a race between
    two enqueues, a manual retry racing the original) from both executing
    and burning a second LLM bill."""
    if not run_id:
        return True  # no persistence context at all -- nothing to guard
    if not _db_enabled():
        logger.warning(
            "[Celery] DATABASE_URL not set -- the duplicate-execution guard "
            "is a no-op and pause/resume across the worker-process boundary "
            "will not work correctly (pending_graph_state has nowhere durable "
            "to live). The celery backend requires Postgres to be configured "
            "for correct operation; proceeding anyway (fail-open, matching "
            "this project's general 'infra failures never block a run' rule)."
        )
        return True
    claimed = run_store.claim_run(run_id, from_status=from_status, celery_task_id=task_id)
    if not claimed:
        logger.warning(
            f"[Celery] run {run_id} was not in status={from_status!r} (already "
            f"claimed/executed by another delivery, or in an unexpected state) "
            f"-- skipping duplicate execution."
        )
    return claimed


@app.task(name="autosynthesis.run_pipeline", bind=True)
def run_pipeline_task(self, prompt: str, output_dir: str, session_id: str,
                       paper_files: list = None, run_id: str = None) -> None:
    if not _claim_or_skip(run_id, "queued", self.request.id):
        return
    import run_service
    run_service.execute_run(prompt, output_dir, session_id, paper_files, run_id)


@app.task(name="autosynthesis.continue_after_search", bind=True)
def continue_after_search_task(self, output_dir: str, session_id: str, excluded_ids: list,
                                pdf_paths: list, run_id: str = None) -> None:
    if not _claim_or_skip(run_id, "awaiting_paper_selection", self.request.id):
        return
    import run_service
    run_service.execute_search_selection_and_continue(output_dir, session_id, excluded_ids, pdf_paths, run_id)


@app.task(name="autosynthesis.continue_after_fulltext", bind=True)
def continue_after_fulltext_task(self, output_dir: str, session_id: str, pdf_paths: list,
                                  run_id: str = None) -> None:
    if not _claim_or_skip(run_id, "awaiting_fulltext_upload", self.request.id):
        return
    import run_service
    run_service.execute_upload_and_continue(output_dir, session_id, pdf_paths, run_id)


@app.task(name="autosynthesis.continue_after_review", bind=True)
def continue_after_review_task(self, output_dir: str, session_id: str, run_id: str = None) -> None:
    if not _claim_or_skip(run_id, "awaiting_review", self.request.id):
        return
    import run_service
    run_service.execute_continue(output_dir, session_id, run_id)


@app.task(name="autosynthesis.run_downstream", bind=True)
def run_downstream_task(self, prompt: str, output_dir: str, session_id: str, run_id: str = None) -> None:
    if not _claim_or_skip(run_id, "queued", self.request.id):
        return
    import run_service
    run_service.execute_downstream(prompt, output_dir, session_id, run_id)
