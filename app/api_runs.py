"""Run-history / run-id-addressed API -- Phase 3 (read-only) + Phase 4
(adds POST /runs/{id}/retry) of the infrastructure migration. Mounted into
dashboard.py's FastAPI app via `app.include_router`.

Still no cookie-less POST /runs "submit a new run" endpoint: that needs
paper bytes to already be server-side (via /upload) with no natural
run_id-addressed equivalent yet, and isn't required by anything in the
plan's checkpoints -- unlike /retry, which the Phase 4 checkpoint
explicitly calls for (recovering a worker-killed run without a session).

The 5 existing session-cookie routes in dashboard.py (`/run`, `/status`,
`/results`, `/review_tracking`, `/continue_pipeline`) are UNCHANGED in
contract and remain how n8n's existing 4 workflows submit/poll runs; this
router adds `run_id`-addressed alternatives for reading run history/
metrics (and, as of Phase 4, retrying a failed run), which n8n's newer
workflows (or anything else) can use today without needing a session
cookie at all.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from persistence import run_store

router = APIRouter(prefix="/api", tags=["runs"])


def _maybe_sweep() -> None:
    # Lazy import -- avoids a module-load-order dependency between this
    # router (mounted by dashboard.py) and run_service.py (imported BY
    # dashboard.py); see run_service.maybe_sweep_stale_runs()'s docstring.
    import run_service
    run_service.maybe_sweep_stale_runs()


def _not_found(run_id: str) -> dict:
    return {"ok": False, "error": f"run '{run_id}' not found (or persistence is disabled)"}


@router.get("/runs")
def list_runs(
    status: Optional[str] = None,
    mode: Optional[str] = None,
    external_ref: Optional[str] = None,
    run_group_id: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """Run-history / comparison list -- the n8n "log/compare runs" primitive:
    one call gives a benchmark comparison table (pooled_effect/CI/k/etc. per
    run). Returns {"ok": False, "runs": [], ...} rather than an error when
    persistence is disabled -- an empty history is a valid, expected state,
    not a failure."""
    _maybe_sweep()
    rows = run_store.list_runs(
        status=status, mode=mode, external_ref=external_ref,
        run_group_id=run_group_id, limit=limit, offset=offset,
    )
    summarized = [
        {
            "run_id": r["run_id"], "status": r["status"], "mode": r["mode"],
            "prompt": r["prompt"], "external_ref": r.get("external_ref"),
            "run_group_id": r.get("run_group_id"), "run_variant": r.get("run_variant"),
            "created_at": r["created_at"], "started_at": r.get("started_at"),
            "finished_at": r.get("finished_at"),
            "failure_stage": r.get("failure_stage"), "error": r.get("error_message"),
            "output_dir": r["output_dir"],
            "n_papers_eligible": r.get("n_papers_eligible"), "n_studies": r.get("n_studies"),
            "n_effect_sizes": r.get("n_effect_sizes"),
            **_pooled_summary(r.get("results_json")),
        }
        for r in rows
    ]
    return {"ok": True, "total": len(summarized), "runs": summarized}


def _pooled_summary(results_json: Optional[dict]) -> dict:
    if not results_json:
        return {}
    return {
        "pooled_effect": results_json.get("pooled_g"),
        "ci_lower": results_json.get("ci_lower"),
        "ci_upper": results_json.get("ci_upper"),
        "p_value": results_json.get("p_value"),
        "i_squared": results_json.get("i_squared"),
        "tau": results_json.get("tau"),
        "k": results_json.get("k"),
        "effect_measure": results_json.get("measure_label"),
    }


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    row = run_store.get_run(run_id)
    if row is None:
        return _not_found(run_id)
    return {"ok": True, "run": row}


@router.get("/runs/{run_id}/status")
def get_run_status(run_id: str):
    row = run_store.get_run(run_id)
    if row is None:
        return _not_found(run_id)
    status_value = row["status"]
    return {
        "ok": True,
        "run_id": run_id,
        "status": status_value,
        "mode": row["mode"],
        "current_stage": row.get("current_stage"),
        "failure_stage": row.get("failure_stage"),
        "error": row.get("error_message"),
        "attempt": row.get("attempt"),
        "queued_at": row.get("queued_at"), "started_at": row.get("started_at"),
        "finished_at": row.get("finished_at"), "heartbeat_at": row.get("heartbeat_at"),
        # Legacy boolean shape, for anything ported from the /status contract
        # by just changing the URL -- same derivation dashboard.py's
        # _derive_run_status() uses in reverse.
        "running": status_value in ("queued", "running"),
        "done": status_value in ("completed", "failed", "cancelled"),
        "awaiting_review": status_value == "awaiting_review",
        "awaiting_paper_selection": status_value == "awaiting_paper_selection",
        "awaiting_fulltext_upload": status_value == "awaiting_fulltext_upload",
    }


@router.get("/runs/{run_id}/results")
def get_run_results(run_id: str, flat: bool = False):
    row = run_store.get_run(run_id)
    if row is None:
        return _not_found(run_id)
    results = row.get("results_json") or {}
    if flat:
        return results  # bare legacy dict, drop-in parity with GET /results
    return {"ok": True, "run_id": run_id, "status": row["status"],
            "output_dir": row["output_dir"], "results": results}


@router.get("/runs/{run_id}/events")
def get_run_events(run_id: str):
    return {"ok": True, "events": run_store.list_stage_events(run_id)}


@router.post("/runs/{run_id}/retry")
def retry_run(run_id: str):
    """Re-dispatches a `failed` run from the beginning (not from its
    failure point -- pause/resume only exists for the auto-search
    awaiting_* gates, not for arbitrary mid-pipeline failures). Uses the
    SAME dispatch decision (thread vs. celery) as the routes that started
    the run originally -- see dashboard.py's RUN_EXECUTION_BACKEND
    branches, mirrored here since this endpoint has no session/pipeline
    dict of its own to consult."""
    row = run_store.get_run(run_id)
    if row is None:
        return _not_found(run_id)
    if row["status"] != "failed":
        return {"ok": False, "error": f"run is '{row['status']}', not 'failed' -- nothing to retry"}

    claimed = run_store.retry_run(run_id)
    if not claimed:
        # Lost a race with another retry/claim between the read above and
        # here -- not this caller's job to retry twice.
        return {"ok": False, "error": "run was already retried or claimed by another request"}

    import config as _config
    prompt = row["prompt"]
    output_dir = row["output_dir"]
    session_id = row.get("session_id") or run_id
    mode = row["mode"]
    paper_files = row.get("paper_files_json")

    if _config.RUN_EXECUTION_BACKEND == "celery":
        if mode == "downstream":
            from tasks import run_downstream_task
            run_downstream_task.apply_async(args=[prompt, output_dir, session_id, run_id])
        else:
            from tasks import run_pipeline_task
            run_pipeline_task.apply_async(args=[prompt, output_dir, session_id, paper_files, run_id])
    else:
        import threading
        import run_service
        if mode == "downstream":
            threading.Thread(target=run_service.execute_downstream,
                              args=(prompt, output_dir, session_id, run_id), daemon=True).start()
        else:
            threading.Thread(target=run_service.execute_run,
                              args=(prompt, output_dir, session_id, paper_files, run_id), daemon=True).start()
    return {"ok": True, "run_id": run_id, "status": "queued"}


@router.get("/metrics")
def get_metrics():
    _maybe_sweep()
    return {"ok": True, **run_store.metrics()}
