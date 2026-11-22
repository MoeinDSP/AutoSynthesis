"""The ONLY module the rest of the app calls into for persistence. Every
public function here is `@db.safe()`-wrapped: if DATABASE_URL is empty, or
the database is unreachable, or a query fails, the function logs a warning
and returns a safe default instead of raising -- a persistence outage must
never break a pipeline run. See persistence/db.py's `safe()` docstring.

No file under agents/ imports this module. All calls happen from
run_service.py (Phase 3) at run-lifecycle phase boundaries, and from
caching/pdf_text_cache.py for pdf_extraction_events.
"""

from __future__ import annotations

import datetime as _dt
import logging
from typing import Any, Dict, List, Optional

from persistence.db import safe, connection
from persistence import schema as sc
from persistence.graph_state_codec import dump_graph_state, load_graph_state
from persistence import snapshot as snap

logger = logging.getLogger(__name__)


def _now():
    return _dt.datetime.now(_dt.timezone.utc)


# ── Run lifecycle ────────────────────────────────────────────────────────────

@safe(default=None)
def create_run(
    run_id: str,
    prompt: str,
    output_dir: str,
    *,
    mode: str = "manual",
    source: str = "dashboard",
    execution_backend: str = "thread",
    session_id: Optional[str] = None,
    run_group_id: Optional[str] = None,
    run_variant: Optional[str] = None,
    external_ref: Optional[str] = None,
    external_ref_kind: Optional[str] = None,
    model_name: Optional[str] = None,
    vision_model_name: Optional[str] = None,
    config_snapshot: Optional[Dict[str, Any]] = None,
    paper_files: Optional[List[str]] = None,
) -> None:
    with connection() as conn:
        conn.execute(sc.runs.insert().values(
            run_id=run_id, prompt=prompt, output_dir=output_dir,
            mode=mode, source=source, execution_backend=execution_backend,
            status="queued", session_id=session_id,
            run_group_id=run_group_id, run_variant=run_variant,
            external_ref=external_ref, external_ref_kind=external_ref_kind,
            model_name=model_name, vision_model_name=vision_model_name,
            config_snapshot=config_snapshot, paper_files_json=paper_files,
            created_at=_now(), queued_at=_now(),
        ))


@safe(default=False)
def claim_run(run_id: str, *, from_status: str = "queued", worker_id: Optional[str] = None,
              celery_task_id: Optional[str] = None) -> bool:
    """Conditional UPDATE that doubles as the duplicate-execution guard: a
    duplicate delivery / accidental double-submit only succeeds in claiming
    the run ONCE. Returns True iff this call was the one that claimed it."""
    with connection() as conn:
        result = conn.execute(
            sc.runs.update()
            .where(sc.runs.c.run_id == run_id, sc.runs.c.status == from_status)
            .values(status="running", started_at=_now(), heartbeat_at=_now(),
                    attempt=sc.runs.c.attempt + 1,
                    worker_id=worker_id, celery_task_id=celery_task_id)
        )
        return result.rowcount > 0


@safe(default=False)
def retry_run(run_id: str) -> bool:
    """Conditional UPDATE, same shape as claim_run: only a `failed` row can
    be retried, and only one caller can win the race back to `queued` --
    the subsequent claim_run(from_status="queued") then increments
    `attempt` normally, so a retried run's second execution naturally shows
    attempt=2."""
    with connection() as conn:
        result = conn.execute(
            sc.runs.update()
            .where(sc.runs.c.run_id == run_id, sc.runs.c.status == "failed")
            .values(status="queued", queued_at=_now(), error_message=None,
                    error_traceback=None, failure_stage=None)
        )
        return result.rowcount > 0


@safe(default=None)
def set_status(run_id: str, status: str, **extra_fields: Any) -> None:
    values: Dict[str, Any] = {"status": status, **extra_fields}
    with connection() as conn:
        conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(**values))


@safe(default=None)
def heartbeat(run_id: str) -> None:
    with connection() as conn:
        conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(heartbeat_at=_now()))


@safe(default=None)
def record_stage_event(run_id: str, stage_id: str, event: str,
                        stage_name: Optional[str] = None, detail: Optional[dict] = None) -> None:
    with connection() as conn:
        conn.execute(sc.run_stage_events.insert().values(
            run_id=run_id, stage_id=stage_id, event=event, stage_name=stage_name,
            detail=detail, at=_now(),
        ))
        if event in ("start", "end"):
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id)
                         .values(current_stage=stage_id))


@safe(default=[])
def list_stage_events(run_id: str) -> List[Dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute(
            sc.run_stage_events.select()
            .where(sc.run_stage_events.c.run_id == run_id)
            .order_by(sc.run_stage_events.c.at)
        ).mappings().all()
    return [dict(r) for r in rows]


@safe(default=None)
def finish_run(run_id: str, *, results_json: Optional[dict] = None,
               pipeline_state_json: Optional[dict] = None) -> None:
    values: Dict[str, Any] = {"status": "completed", "finished_at": _now()}
    if results_json is not None:
        values["results_json"] = results_json
    if pipeline_state_json is not None:
        values["pipeline_state_json"] = pipeline_state_json
    with connection() as conn:
        conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(**values))


@safe(default=None)
def fail_run(run_id: str, error_message: str, *, error_traceback: Optional[str] = None,
             failure_stage: Optional[str] = None) -> None:
    with connection() as conn:
        conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(
            status="failed", finished_at=_now(),
            error_message=error_message, error_traceback=error_traceback,
            failure_stage=failure_stage,
        ))


# ── Pause / resume (durable replacement for pipeline["pending_graph_state"]) ─

@safe(default=None)
def save_pause_state(run_id: str, phase: str, graph_state: Dict[str, Any]) -> None:
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    payload = dump_graph_state(graph_state)
    stmt = pg_insert(sc.run_pause_states).values(
        run_id=run_id, phase=phase, payload=payload, created_at=_now(),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["run_id", "phase"],
        set_={"payload": stmt.excluded.payload, "created_at": stmt.excluded.created_at},
    )
    with connection() as conn:
        conn.execute(stmt)


@safe(default=None)
def load_pause_state(run_id: str, phase: str) -> Optional[Dict[str, Any]]:
    with connection() as conn:
        row = conn.execute(
            sc.run_pause_states.select().where(
                sc.run_pause_states.c.run_id == run_id,
                sc.run_pause_states.c.phase == phase,
            )
        ).mappings().first()
    if row is None:
        return None
    return load_graph_state(dict(row["payload"]))


# ── Snapshots ────────────────────────────────────────────────────────────────

@safe(default=None)
def persist_snapshot(run_id: str, graph_state: Dict[str, Any],
                      included_studies: Optional[List[Any]] = None) -> None:
    """Idempotent by construction: DELETE-then-bulk-INSERT every child table
    for this run_id, inside one transaction. Safe to call at every pause AND
    at completion -- calling it twice with the same graph_state produces the
    same rows, not duplicates."""
    paper_rows = snap.build_paper_rows(graph_state)
    study_rows = snap.build_study_rows(included_studies)
    effect_size_rows = snap.build_effect_size_rows(graph_state)
    group_rows, pooled_rows = snap.build_outcome_group_and_pooled_rows(graph_state)
    moderator_rows = snap.build_moderator_rows(graph_state)
    bias_rows = snap.build_bias_rows(graph_state)
    rob_rows = snap.build_rob_rows(graph_state)
    flag_rows = snap.build_validation_flag_rows(graph_state)
    run_summary = snap.derive_run_summary(graph_state)
    if included_studies:
        run_summary["n_studies"] = len(included_studies)

    child_tables = [
        (sc.run_papers, paper_rows),
        (sc.run_studies, study_rows),
        (sc.run_effect_sizes, effect_size_rows),
        (sc.run_outcome_groups, group_rows),
        (sc.run_pooled_results, pooled_rows),
        (sc.run_moderator_results, moderator_rows),
        (sc.run_bias_results, bias_rows),
        (sc.run_rob_assessments, rob_rows),
        (sc.run_validation_flags, flag_rows),
    ]

    with connection() as conn:
        for table, rows in child_tables:
            conn.execute(table.delete().where(table.c.run_id == run_id))
            if rows:
                conn.execute(table.insert(), [{"run_id": run_id, **r} for r in rows])
        if run_summary:
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(**run_summary))


@safe(default=None)
def record_artifact(run_id: str, name: str, relative_path: str,
                     kind: Optional[str] = None, size_bytes: Optional[int] = None) -> None:
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    stmt = pg_insert(sc.run_artifacts).values(
        run_id=run_id, name=name, relative_path=relative_path,
        kind=kind, size_bytes=size_bytes, created_at=_now(),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["run_id", "relative_path"],
        set_={"size_bytes": stmt.excluded.size_bytes},
    )
    with connection() as conn:
        conn.execute(stmt)


# ── PDF cache event recording (Phase 2 uses this) ───────────────────────────

@safe(default=None)
def record_pdf_extraction_event(
    content_sha256: str, cache_key: str, cache_hit: bool, *,
    run_id: Optional[str] = None, extractor: Optional[str] = None,
    text_chars: Optional[int] = None, elapsed_ms: Optional[int] = None,
) -> None:
    with connection() as conn:
        conn.execute(sc.pdf_extraction_events.insert().values(
            run_id=run_id, content_sha256=content_sha256, cache_key=cache_key,
            cache_hit=cache_hit, extractor=extractor, text_chars=text_chars,
            elapsed_ms=elapsed_ms, created_at=_now(),
        ))
        if run_id:
            col = sc.runs.c.pdf_cache_hits if cache_hit else sc.runs.c.pdf_cache_misses
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id).values(
                **{col.name: col + 1}
            ))


# ── Reads ────────────────────────────────────────────────────────────────────

@safe(default=None)
def get_run(run_id: str) -> Optional[Dict[str, Any]]:
    with connection() as conn:
        row = conn.execute(sc.runs.select().where(sc.runs.c.run_id == run_id)).mappings().first()
    return dict(row) if row is not None else None


@safe(default=None)
def latest_run_for_session(session_id: str) -> Optional[Dict[str, Any]]:
    with connection() as conn:
        row = conn.execute(
            sc.runs.select()
            .where(sc.runs.c.session_id == session_id)
            .order_by(sc.runs.c.created_at.desc())
            .limit(1)
        ).mappings().first()
    return dict(row) if row is not None else None


@safe(default=[])
def list_runs(*, status: Optional[str] = None, mode: Optional[str] = None,
              external_ref: Optional[str] = None, run_group_id: Optional[str] = None,
              since: Optional[_dt.datetime] = None, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    query = sc.runs.select().order_by(sc.runs.c.created_at.desc()).limit(limit).offset(offset)
    if status:
        query = query.where(sc.runs.c.status == status)
    if mode:
        query = query.where(sc.runs.c.mode == mode)
    if external_ref:
        query = query.where(sc.runs.c.external_ref == external_ref)
    if run_group_id:
        query = query.where(sc.runs.c.run_group_id == run_group_id)
    if since:
        query = query.where(sc.runs.c.created_at >= since)
    with connection() as conn:
        rows = conn.execute(query).mappings().all()
    return [dict(r) for r in rows]


@safe(default={})
def metrics() -> Dict[str, Any]:
    from sqlalchemy import func, select

    with connection() as conn:
        total = conn.execute(select(func.count()).select_from(sc.runs)).scalar_one()
        by_status_rows = conn.execute(
            select(sc.runs.c.status, func.count()).group_by(sc.runs.c.status)
        ).all()
        hits, misses = conn.execute(
            select(func.coalesce(func.sum(sc.runs.c.pdf_cache_hits), 0),
                   func.coalesce(func.sum(sc.runs.c.pdf_cache_misses), 0))
        ).one()

    by_status = {status: count for status, count in by_status_rows}
    total_pdf_events = hits + misses
    return {
        "runs": {"total": total, "by_status": by_status},
        "pdf_cache": {
            "hits": int(hits), "misses": int(misses),
            "hit_rate": (hits / total_pdf_events) if total_pdf_events else None,
        },
    }


# ── Stale-run sweep (no Celery Beat -- called opportunistically, see
#    dashboard.py's status/list/metrics routes) ─────────────────────────────

@safe(default={"failed_running": 0, "failed_queued": 0})
def sweep_stale_runs(*, stale_seconds: int, queue_timeout_seconds: int) -> Dict[str, int]:
    cutoff_running = _now() - _dt.timedelta(seconds=stale_seconds)
    cutoff_queued = _now() - _dt.timedelta(seconds=queue_timeout_seconds)
    with connection() as conn:
        running_result = conn.execute(
            sc.runs.update()
            .where(sc.runs.c.status == "running", sc.runs.c.heartbeat_at < cutoff_running)
            .values(status="failed", finished_at=_now(),
                    error_message="worker lost (no heartbeat)",
                    failure_stage=sc.runs.c.current_stage)
        )
        queued_result = conn.execute(
            sc.runs.update()
            .where(sc.runs.c.status == "queued", sc.runs.c.created_at < cutoff_queued)
            .values(status="failed", finished_at=_now(),
                    error_message="timed out waiting to start (queued too long)")
        )
    return {"failed_running": running_result.rowcount, "failed_queued": queued_result.rowcount}
