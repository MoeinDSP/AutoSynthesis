"""Backend-agnostic run execution -- Phase 4 of the infrastructure migration.

This module owns "what a run actually does": the four execute_* functions
below are dashboard.py's original `_run_pipeline`/`_continue_pipeline`/
`_upload_missing_fulltext_and_continue`/`_run_downstream` thread-target
functions, moved here VERBATIM (their bodies/control-flow/log messages are
byte-for-byte unchanged from Phase 3 -- only the module they live in and
their names changed, per the plan's "dashboard.py's thread-targets become
~4-line calls into run_service" design). Two callers now use them:

  - dashboard.py's routes, via `threading.Thread(target=run_service.execute_run, ...)`
    when RUN_EXECUTION_BACKEND=thread (the default, unchanged since Phase 3).
  - tasks.py's Celery tasks, which call these functions directly (a Celery
    task body already runs in a background worker process -- no Thread
    needed) when RUN_EXECUTION_BACKEND=celery.

Also owns the per-session in-memory pipeline-state dicts (`_pipelines`,
`_log_queues`) and the SSE logging-handler machinery (`_SSEHandler`,
`_attach_handler`/`_detach_handler`) that used to live in dashboard.py --
moved here for the same reason. dashboard.py re-imports every one of these
names so its own code (routes, agent-detail page rendering) is unchanged.

**The one real behavioral fork this phase adds** (not present in the moved
code below, added at the dashboard.py route layer instead -- see
dashboard.py's /status, /results, /continue_pipeline, /upload_missing_fulltext,
/run_analysis): under RUN_EXECUTION_BACKEND=celery, a run's actual execution
happens in a SEPARATE OS process (the celery worker), so that process's own
`_get_pipeline(session_id)` call below returns a DIFFERENT dict instance
than the API process's -- writes to `pipeline["running"]`/`"done"`/
`"results"` inside execute_run etc. are real (used for this-process
diagnostics and the /stream fallback) but invisible to the API process.
Postgres (`_run_store`) is therefore the only cross-process source of truth
for status/results/pause-state under the celery backend; dashboard.py reads
it directly in that case via `status_from_run_row()`/`results_from_run_row()`
below. Under the (default, and currently the only one actually deployed)
thread backend, execution happens in-process, so the in-memory dict IS live
and dashboard.py's routes keep reading it exactly as before -- zero
behavior change for the default deployment.
"""

from __future__ import annotations

import json
import logging
import queue as _queue_module
import re
import shutil
import threading
import time
import traceback
from pathlib import Path
from typing import Optional

from utils.outcome_grouping import safe_filename_fragment
from utils import thread_tracking as _thread_tracking
from persistence import run_store as _run_store
import config as _config

logger = logging.getLogger(__name__)

# ── Per-session pipeline state (moved from dashboard.py, Phase 4) ──────────

_state_lock = threading.Lock()
_pipelines: dict[str, dict] = {}
_log_queues: dict[str, _queue_module.Queue] = {}


def _new_pipeline_state() -> dict:
    return {
        "running":          False,
        "done":             False,
        "cancelled":        False,
        "error":            None,
        "results":          None,
        "current_stage_id": None,
        "stage_logs":       {sid: [] for sid in STAGE_ORDER},
        "awaiting_review":  False,
        "awaiting_paper_selection": False,
        "awaiting_fulltext_upload": False,
        "pending_graph_state": None,
        "mode":             "auto",
        "run_id":           None,
    }


def _get_pipeline(session_id: str) -> dict:
    with _state_lock:
        pipeline = _pipelines.get(session_id)
        if pipeline is None:
            pipeline = _new_pipeline_state()
            _pipelines[session_id] = pipeline
        return pipeline


def _get_log_queue(session_id: str) -> _queue_module.Queue:
    with _state_lock:
        q = _log_queues.get(session_id)
        if q is None:
            q = _queue_module.Queue()
            _log_queues[session_id] = q
        return q


# ── Stage-log bucketing (moved from dashboard.py, Phase 4 -- unchanged) ────

# Ordered so "STAGE 3b" is checked before "STAGE 3"
STAGE_PATTERNS = [
    # Longer/more-specific patterns first to avoid prefix collisions
    ("STAGE 3b", "s3b"),
    ("STAGE 3A", "s4"),   # Study Detector — bucket with Data Extraction (no dedicated slot)
    ("STAGE 4B", "s4"),   # Cross-Paper Mapper — bucket with Data Extraction
    ("STAGE 4C", "s4"),   # Coding Table Export — bucket with Data Extraction
    ("STAGE 0",  "s0"),
    ("STAGE 1",  "s1"),
    ("STAGE 2",  "s2"),
    ("STAGE 3",  "s3"),
    ("STAGE 4",  "s4"),
    ("STAGE 5",  "s5"),
    ("STAGE 6",  "s6"),
    ("STAGE 7",  "s7"),
    ("STAGE 8B", "s8b"),
    ("STAGE 8",  "s8"),
    ("STAGE 9",  "s9"),
]

STAGE_ORDER = ["s0", "s1", "s2", "s3b", "s3", "s4", "s5", "s6", "s7", "s8", "s8b", "s9"]


# ── Run cancellation ────────────────────────────────────────────────────────
# A run executes in a daemon thread, which Python cannot kill from outside, so
# cancellation is cooperative:
#   1. request_cancel() flags the session and raises RunCancelled inside the
#      run's thread at its next Python instruction (PyThreadState_SetAsyncExc).
#      A thread blocked in C (an HTTP read, an R subprocess) receives it as soon
#      as that call returns.
#   2. Backstop: if the run is still logging CANCEL_GRACE_S seconds later (the
#      signal was swallowed somewhere), the run's own log calls raise it.
# RunCancelled derives from BaseException so the agents' broad
# `except Exception` blocks cannot swallow it; each execute_* entry point
# catches it and records the run as "cancelled" (not "failed").
CANCEL_GRACE_S = 10.0


class RunCancelled(BaseException):
    """Raised inside a run's thread when the user cancels the run."""


def _interrupt_thread(ident: int) -> bool:
    import ctypes
    n = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(ident), ctypes.py_object(RunCancelled))
    if n > 1:      # should never happen; undo rather than hit several threads
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(ident), None)
        return False
    return n == 1


def _start_cancellable(pipeline: dict) -> None:
    """Called at the start of every execute_* run thread."""
    pipeline["run_thread"] = threading.get_ident()
    pipeline["cancel_requested_at"] = None
    pipeline["cancelled"] = False


def _mark_cancelled(pipeline: dict, log_queue, run_id: Optional[str]) -> None:
    pipeline["cancelled"] = True
    pipeline["cancel_requested_at"] = None
    pipeline["done"] = True
    pipeline["error"] = None
    pipeline["results"] = None
    pipeline["awaiting_review"] = False
    pipeline["awaiting_paper_selection"] = False
    pipeline["awaiting_fulltext_upload"] = False
    pipeline["pending_graph_state"] = None
    if run_id:
        _run_store.set_status(run_id, "cancelled")
    log_queue.put(json.dumps({"level": "WARNING", "msg": "Run cancelled by user.",
                              "time": time.strftime("%H:%M:%S")}))


def request_cancel(session_id: str) -> str:
    """Cancel this session's run. Returns "cancelling" (a running run will stop
    at its next step), "cancelled" (a paused run was discarded immediately),
    or "none" (nothing to cancel)."""
    pipeline = _get_pipeline(session_id)
    if pipeline.get("running"):
        if pipeline.get("cancel_requested_at") is None:
            pipeline["cancel_requested_at"] = time.time()
            ident = pipeline.get("run_thread")
            if ident:
                _interrupt_thread(ident)
        return "cancelling"
    if pipeline.get("awaiting_review") or pipeline.get("awaiting_paper_selection") \
            or pipeline.get("awaiting_fulltext_upload"):
        _mark_cancelled(pipeline, _get_log_queue(session_id), pipeline.get("run_id"))
        return "cancelled"
    return "none"


class _SSEHandler(logging.Handler):
    def __init__(self, session_id: str, thread_id: int, run_id: str = None):
        super().__init__()
        self.session_id = session_id
        self.thread_id = thread_id
        self.run_id = run_id

    def emit(self, record: logging.LogRecord) -> None:
        if record.thread == self.thread_id or _thread_tracking.is_descendant(record.thread, self.thread_id):
            asked = _get_pipeline(self.session_id).get("cancel_requested_at")
            if asked and time.time() - asked > CANCEL_GRACE_S:
                raise RunCancelled()
        try:
            if record.thread != self.thread_id and not _thread_tracking.is_descendant(
                record.thread, self.thread_id
            ):
                return
            msg = self.format(record)
            pipeline = _get_pipeline(self.session_id)
            log_queue = _get_log_queue(self.session_id)
            # Detect stage transitions and bucket the log
            previous_stage = pipeline["current_stage_id"]
            for pattern, sid in STAGE_PATTERNS:
                if pattern in msg:
                    pipeline["current_stage_id"] = sid
                    break
            sid = pipeline["current_stage_id"]
            if self.run_id and sid and sid != previous_stage:
                # Only on an actual transition (not every log line within
                # the same stage) -- record_stage_event is a Postgres write,
                # no need for one per log line. Safe no-op if persistence
                # is disabled (see persistence/db.py's @safe decorator).
                _run_store.record_stage_event(self.run_id, sid, "start")
            if sid and sid in pipeline["stage_logs"]:
                pipeline["stage_logs"][sid].append({
                    "time":  time.strftime("%H:%M:%S", time.localtime(record.created)),
                    "level": record.levelname,
                    "msg":   msg,
                })
            payload = json.dumps({
                "level": record.levelname,
                "msg":   msg,
                "time":  time.strftime("%H:%M:%S", time.localtime(record.created)),
            })
            log_queue.put(payload)
        except Exception:
            pass


def _attach_handler(session_id: str, run_id: str = None):
    root = logging.getLogger()
    handler = _SSEHandler(session_id, threading.get_ident(), run_id=run_id)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    return handler


def _detach_handler(handler: logging.Handler):
    root = logging.getLogger()
    if handler in root.handlers:
        root.removeHandler(handler)
    # Drop this run's spawned-worker-thread bookkeeping (see
    # utils/thread_tracking.py) now that its SSEHandler is going away --
    # keeps the registry from growing unbounded across many runs.
    _thread_tracking.clear_descendants(handler.thread_id)


# ── Heartbeat (Phase 4 -- new) ──────────────────────────────────────────────
# A worker crash under the celery backend leaves a `running` row with a
# frozen heartbeat_at; sweep_stale_runs() (persistence/run_store.py, already
# built in Phase 1) uses that to mark it failed. The thread backend gets
# this for free too (harmless -- a completed/thread-backend run just stops
# heartbeating when the thread exits, same as it always has).

class _Heartbeat:
    def __init__(self, run_id: str):
        self._run_id = run_id
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self):
        while not self._stop.wait(_config.RUN_HEARTBEAT_SECONDS):
            _run_store.heartbeat(self._run_id)

    def __enter__(self):
        if self._run_id:
            _run_store.heartbeat(self._run_id)
            self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()


# ── Results shaping (moved from dashboard.py, Phase 4 -- unchanged) ────────

def _meta_analysis_measure_fields(ma) -> dict:
    """effect_measure/computation_scale/whether native pooling or the
    Hedges' g/SMD fallback was used -- reuses agents/report_agent.py's own
    labeling helpers so the dashboard and the generated report never
    disagree about what a result should be called. `ma` is a
    MetaAnalysisResult (models.py) -- always has these fields now, so no
    wrapper (MetaAnalysisGroupResult) access is needed here."""
    from utils.effect_measures import measure_label as _measure_label, native_pooling_used as _native_pooling_used
    native = _native_pooling_used(ma.effect_measure, ma.computation_scale)
    return {
        "pooled_effect": round(ma.pooled_effect, 4),
        "effect_measure": ma.effect_measure.value,
        "computation_scale": ma.computation_scale.value,
        "measure_label": _measure_label(ma.computation_scale),
        "native_pooling_used": native,
        "effect_measure_source": ma.effect_measure_source,
        "effect_measure_conflict": ma.effect_measure_conflict,
    }


def _favors_label(result, plan) -> str:
    """Plain-text answer to "which side does the pooled estimate favour",
    reusing MetaAnalysisResult.favors_treatment and the plan's own treatment/
    control labels -- the same logic agents/pipeline_audit_agent.py uses for
    the "Favors" row of final_results_summary.csv, so the dashboard table and
    that CSV never disagree. Empty string when there is no pooled result."""
    if result is None:
        return ""
    if result.favors_treatment is True:
        return (plan.treatment_label if plan else None) or "Treatment"
    if result.favors_treatment is False:
        return (plan.control_label if plan else None) or "Control"
    return "Neither (tie or undetermined)"


def _results_from_pipeline_state(state, output_dir: str) -> dict:
    results: dict = {}
    if state.plan:
        results["research_question"] = state.plan.research_question
        results["treatment"]         = state.plan.treatment_label
        results["control"]           = state.plan.control_label

    results["n_retrieved"] = state.search_n_retrieved
    results["n_screened"]  = state.screening_n_included
    results["n_eligible"]  = state.eligibility_n_included
    results["n_studies"]   = len(state.included_studies)
    results["n_effects"]   = len(state.effect_sizes)

    if state.meta_analysis:
        ma = state.meta_analysis
        results["pooled_g"]  = round(ma.pooled_g,  4)  # backward-compat name -- see pooled_effect below
        results["ci_lower"]  = round(ma.ci_lower,  3)
        results["ci_upper"]  = round(ma.ci_upper,  3)
        results["p_value"]   = round(ma.p_value,   4)
        results["i_squared"] = round(ma.i_squared, 1)
        results["tau"]       = round(ma.tau,       4)
        results["k"]         = ma.k
        results["n_total"]   = ma.n_total
        results["favors"]    = _favors_label(ma, state.plan)
        from statistics.metafor_engine import POOLING_MODELS
        results["pooling_model"] = ma.method
        results["pooling_model_label"] = POOLING_MODELS.get(ma.method, ma.method)
        results.update(_meta_analysis_measure_fields(ma))

    if state.stats_engine_info:
        results["stats_engine"] = state.stats_engine_info

    if state.bias_result:
        results["bias_risk"]    = state.bias_result.bias_risk
        results["eggers_p"]     = round(state.bias_result.eggers_p_value, 4)
        results["trim_fill_k0"] = state.bias_result.trim_fill_k0
        br = state.bias_result
        # Ratio measures are tested on the log scale; show adjusted estimates as ratios.
        import math as _math
        _show = (lambda x: round(_math.exp(x), 3)) if "log scale" in (br.scale or "") else (lambda x: round(x, 3))
        results["trim_fill_estimate"] = _show(br.trim_fill_g)
        if br.rank_test_p_value is not None:
            results["rank_test_p"] = round(br.rank_test_p_value, 4)
        if br.pet_peese_estimate is not None:
            results["pet_peese_estimate"] = _show(br.pet_peese_estimate)
            results["pet_peese_selected"] = br.pet_peese_selected
            results["pet_p"] = br.pet_p_value
            results["pet_peese_note"] = br.pet_peese_note
        results["bias_scale"] = br.scale

    if state.rob_assessments:
        n_rob2    = sum(1 for a in state.rob_assessments if a.tool_used == "RoB2")
        n_robinsi = sum(1 for a in state.rob_assessments if a.tool_used == "ROBINS-I")
        n_elevated = sum(1 for a in state.rob_assessments if a.overall_risk != "low")
        n_high     = sum(1 for a in state.rob_assessments if a.overall_risk in ("high", "serious", "critical"))
        results["rob_n_assessed"] = len(state.rob_assessments)
        results["rob_n_rob2"]     = n_rob2
        results["rob_n_robinsi"]  = n_robinsi
        results["rob_n_elevated"] = n_elevated
        results["rob_n_high"]     = n_high

    results["report_path"] = state.report_path or ""
    if Path(output_dir, "meta_analysis_summary.csv").exists():
        results["audit_summary_csv"] = "meta_analysis_summary.csv"
    if Path(output_dir, "study_screening.csv").exists():
        results["audit_screening_csv"] = "study_screening.csv"
    if Path(output_dir, "paper_tracking.csv").exists():
        results["audit_tracking_csv"] = "paper_tracking.csv"
    if Path(output_dir, "rob_assessments.json").exists():
        results["rob_assessments_json"] = "rob_assessments.json"

    plots = {}
    for name, fname in [
        ("forest",       "forest_plot.png"),
        ("funnel",       "funnel_plot.png"),
        ("cumulative",   "cumulative_plot.png"),
        ("distribution", "effect_distribution.png"),
        ("bubble",       "bubble_chart.png"),
        ("heterogeneity", "heterogeneity_summary.png"),
        ("rob_rob2",     "rob_traffic_light_rob2.png"),
        ("rob_robins_i", "rob_traffic_light_robins_i.png"),
        ("prisma",       "prisma_flowchart.png"),
    ]:
        if Path(output_dir, fname).exists():
            plots[name] = fname
    results["plots"] = plots
    flow_path = Path(output_dir, "prisma_flowchart.json")
    if flow_path.exists():
        try:
            results["prisma_flow"] = json.loads(flow_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass

    # ── Per-outcome-group breakdown ─────────────────────────────────────────
    # meta_analysis/pooled_g/plots above are ALWAYS just an alias for ONE
    # group -- the "primary" one picked by agents/meta_analysis_agent.py
    # (see its outcome_group_key selection). A run with more than one
    # distinct outcome family/timepoint produces several independently
    # pooled MetaAnalysisGroupResults (state.meta_analysis_groups), each
    # with its own already-generated, suffixed plot files on disk -- but
    # until now nothing here ever surfaced them, so the UI only ever showed
    # the single primary card no matter how many outcomes the review
    # actually had. This list lets the frontend offer the rest.
    groups = []
    # Identify the primary group by matching its result object identity to
    # state.meta_analysis (the alias set by meta_analysis_node) rather than
    # re-deriving the selection rule here -- one source of truth.
    for g in (state.meta_analysis_groups or []):
        is_primary = bool(state.meta_analysis) and g.result is state.meta_analysis
        entry = {
            "key":              g.outcome_group_key,
            "label":            g.label,
            "outcome_family":   g.outcome_family,
            "follow_up_timepoint": g.follow_up_timepoint,
            "comparison_family": g.comparison_family,
            "k":                g.k,
            "n_total":          g.n_total,
            "insufficient_data": g.insufficient_data,
            "is_primary":       is_primary,
        }
        if g.result:
            entry["pooled_g"]  = round(g.result.pooled_g, 4)
            entry["ci_lower"]  = round(g.result.ci_lower, 3)
            entry["ci_upper"]  = round(g.result.ci_upper, 3)
            entry["p_value"]   = round(g.result.p_value, 4)
            entry["i_squared"] = round(g.result.i_squared, 1)
            entry["tau"]       = round(g.result.tau, 4)
            entry["favors"]    = _favors_label(g.result, state.plan)
            entry.update(_meta_analysis_measure_fields(g.result))
        suffix = "" if is_primary else safe_filename_fragment(g.outcome_group_key)
        group_plots = {}
        for name, base in [
            ("forest", "forest_plot"), ("funnel", "funnel_plot"),
            ("cumulative", "cumulative_plot"), ("distribution", "effect_distribution"),
            ("bubble", "bubble_chart"), ("heterogeneity", "heterogeneity_summary"),
        ]:
            fname = f"{base}.png" if not suffix else f"{base}__{suffix}.png"
            if Path(output_dir, fname).exists():
                group_plots[name] = fname
        entry["plots"] = group_plots
        groups.append(entry)
    # Largest-first, matching the same ordering meta_analysis_node uses to
    # pick "primary" (default-rooted groups already excluded there -- see
    # agents/meta_analysis_agent.py) -- so the list reads sensibly with no
    # further client-side re-sorting needed.
    groups.sort(key=lambda e: (not e["is_primary"], e["insufficient_data"], -e["k"]))
    results["meta_groups"] = groups
    return results


def _missing_fulltext_papers(graph_state: dict) -> list:
    """PaperRecord objects for papers dropped by fetch_fulltext_node, looked up
    by id in all_retrieved_papers (the full-metadata snapshot search_node keeps)."""
    ids = set(graph_state.get("papers_no_fulltext", []))
    if not ids:
        return []
    by_id = {p.id: p for p in graph_state.get("all_retrieved_papers", [])}
    return [by_id[pid] for pid in ids if pid in by_id]


# ── Cross-process status/results (Phase 4 -- new; used only under the
#    celery backend, see dashboard.py's /status, /results routes) ──────────

_last_sweep_at = 0.0
_sweep_lock = threading.Lock()


def maybe_sweep_stale_runs() -> None:
    """No Celery Beat is deployed (one more moving part not worth it for a
    handful of long-running jobs) -- instead this piggybacks on read routes
    that are polled regularly anyway (dashboard.py's /status, api_runs.py's
    /runs and /metrics), throttled to at most once every 60s per process so
    a busy dashboard doesn't turn every poll into a table scan. Marks
    `running` rows with a stale heartbeat_at, and `queued` rows that waited
    too long, as failed -- see persistence/run_store.py's sweep_stale_runs()
    (built in Phase 1, unused until now)."""
    global _last_sweep_at
    now = time.monotonic()
    with _sweep_lock:
        if now - _last_sweep_at < 60:
            return
        _last_sweep_at = now
    result = _run_store.sweep_stale_runs(
        stale_seconds=_config.RUN_STALE_SECONDS,
        queue_timeout_seconds=_config.RUN_QUEUE_TIMEOUT_SECONDS,
    )
    if result.get("failed_running") or result.get("failed_queued"):
        logger.warning(f"[Sweep] marked stale runs failed: {result}")


# cochrane_benchmark/ lives at the repo root, one level up from this file.
BENCHMARK_RUNS_DIR = Path(__file__).resolve().parent / "cochrane_benchmark" / "runs"


_ARCHIVE_MARKER_FILES = (
    "effect_sizes.json", "meta_analysis_result.json", "paper_tracking.csv", "plan.json",
)


def _archive_to_benchmark_runs(run_id: Optional[str], output_dir: str) -> None:
    """Mirrors a completed run's full output directory -- extracted results,
    effect sizes, plots, the generated report, everything the pipeline
    produced -- into cochrane_benchmark/runs/<label>/<model_tag>/, matching
    the model-named-subfolder convention every other benchmark case already
    uses (e.g. cochrane_benchmark/runs/CD007130/gemini-3.8-flash_manual_
    download_run_.../).

    <label> is the run's external_ref (a Cochrane review id like
    "CD013591", set via the dashboard's optional "Review ID" field) when
    one was given, else the run_id itself, so every completed run gets
    archived somewhere even without a review id attached. <label>/ is also
    where the review's source PDF and "Included studies/" input folder
    already live for benchmark cases -- this function only ever writes
    inside <label>/<model_tag>/, never touching those input-side files.

    <model_tag> is whichever model (config.MODEL_NAME) actually produced
    the run, read fresh at archive time -- never hardcoded to one provider
    -- so a review directory can hold runs from multiple different models
    side by side, each clearly labeled, instead of colliding in one folder.

    If <label>/<model_tag>/ already contains output from a PRIOR archived
    run (detected via _ARCHIVE_MARKER_FILES -- effect_sizes.json,
    meta_analysis_result.json, paper_tracking.csv, plan.json), this refuses
    to archive and logs a warning instead of merging/overwriting: re-running
    the same case with the same model must not silently mix a new run's
    files with a stale run's leftovers (this is exactly the class of bug
    that produced a creativity-topic contaminated result for what was
    supposed to be a fresh CD015968 run). Delete that model's existing
    output files first if you deliberately want to redo it with the same
    model, or archive under a different model name.

    Purely an archival COPY -- never touches or moves the original
    output_dir dashboard.py's routes still serve files from -- and never
    raises into the pipeline, matching every other persistence call's
    fail-open convention in this codebase (a full disk or a permissions
    problem here must never fail an otherwise-successful run)."""
    if not run_id:
        return
    try:
        row = _run_store.get_run(run_id)
        label = (row.get("external_ref") if row else None) or run_id
        label = re.sub(r"[^A-Za-z0-9_.\-]", "_", label)  # filesystem-safe
        src = Path(output_dir)
        if not src.is_dir():
            return
        model_name = getattr(_config, "MODEL_NAME", "") or ""
        model_tag = model_name.rsplit("/", 1)[-1]  # "google/gemini-3.8-flash" -> "gemini-3.8-flash"
        model_tag = re.sub(r"[^A-Za-z0-9_.\-]", "_", model_tag) or "unknown_model"
        dest = BENCHMARK_RUNS_DIR / label / model_tag
        if dest.is_dir() and any((dest / m).exists() for m in _ARCHIVE_MARKER_FILES):
            logger.warning(
                f"[Archive] {dest} already holds output from a previously archived run "
                f"-- refusing to overwrite it with run {run_id}. Delete its existing "
                "pipeline-output files first if you want to re-run this case/model combination."
            )
            return
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest, dirs_exist_ok=True)
        logger.info(f"[Archive] run {run_id} -> {dest}")
    except Exception as exc:
        logger.warning(f"[Archive] Failed to archive run {run_id} to cochrane_benchmark/runs: {exc}")


def status_from_run_row(row: dict) -> dict:
    """Same shape as dashboard.py's /status route -- derived from a Postgres
    `runs` row instead of the in-memory pipeline dict, for a run whose
    execution happened in a different OS process (a celery worker)."""
    status_value = row["status"]
    return {
        "running": status_value in ("queued", "running"),
        "done": status_value in ("completed", "failed", "cancelled"),
        "error": row.get("error_message"),
        "awaiting_review": status_value == "awaiting_review",
        "awaiting_paper_selection": status_value == "awaiting_paper_selection",
        "awaiting_fulltext_upload": status_value == "awaiting_fulltext_upload",
        "run_id": row["run_id"],
        "status": status_value,
    }


# ── Execute functions (moved from dashboard.py, Phase 4 -- bodies verbatim
#    from end of Phase 3, wrapped in a heartbeat context) ──────────────────

def _after_fulltext_stage(orch, graph_state: dict, pipeline: dict, log_queue, run_id) -> None:
    """Shared tail of the search-mode start-up: given the state right after
    full-text fetch, either pause for a manual full-text upload (some papers
    could not be retrieved) or continue through eligibility to the
    paper-tracking review gate."""
    if graph_state.get("papers_no_fulltext"):
        # One or more relevant papers could not be retrieved automatically --
        # pause here so the user can upload PDFs manually before eligibility runs.
        pipeline["pending_graph_state"] = graph_state
        pipeline["awaiting_fulltext_upload"] = True
        pipeline["done"] = False
        if run_id:
            _run_store.save_pause_state(run_id, "after_fulltext", graph_state)
            _run_store.set_status(run_id, "awaiting_fulltext_upload")
        n_missing = len(graph_state["papers_no_fulltext"])
        log_queue.put(json.dumps({
            "level": "SUCCESS",
            "msg":   f"{n_missing} paper(s) could not be retrieved automatically — "
                     f"upload PDFs or continue without them.",
            "time":  time.strftime("%H:%M:%S"),
        }))
        return

    # Nothing was dropped -- continue straight through, unchanged from
    # the pre-existing behavior (no dialog shown to the user).
    graph_state = orch.continue_after_fulltext_review(graph_state)
    pipeline["pending_graph_state"] = graph_state
    pipeline["awaiting_review"] = True
    pipeline["done"] = False
    pipeline["results"] = {
        "n_retrieved": graph_state.get("n_search_retrieved", 0),
        "n_screened": len(graph_state.get("papers_eligible", [])),
        "n_eligible": len(graph_state.get("papers_eligible", [])),
        "audit_tracking_csv": "paper_tracking.csv",
    }
    if run_id:
        _run_store.save_pause_state(run_id, "after_eligibility", graph_state)
        _run_store.set_status(run_id, "awaiting_review")
        _run_store.persist_snapshot(run_id, graph_state)
    log_queue.put(json.dumps({
        "level": "SUCCESS",
        "msg":   "Paper tracking review ready — approve to continue.",
        "time":  time.strftime("%H:%M:%S"),
    }))


def execute_run(prompt: str, output_dir: str, session_id: str, paper_files: list = None,
                 run_id: str = None, pooling_model: str = None) -> None:
    handler = None
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    _start_cancellable(pipeline)
    try:
        from orchestrator import MetaAnalysisOrchestrator
        from core_utils import setup_logging
        setup_logging(logging.INFO)
        handler = _attach_handler(session_id, run_id=run_id)
        if run_id:
            _run_store.claim_run(run_id)

        pipeline["running"]          = True
        pipeline["done"]             = False
        pipeline["error"]            = None
        pipeline["results"]          = None
        pipeline["current_stage_id"] = None
        pipeline["stage_logs"]       = {sid: [] for sid in STAGE_ORDER}
        pipeline["awaiting_review"]  = False
        pipeline["awaiting_paper_selection"] = False
        pipeline["awaiting_fulltext_upload"] = False
        pipeline["pending_graph_state"] = None
        # Drives the "s1" stage label in the sidebar/agent-detail page: manual
        # uploads skip the Search Agent entirely (pipeline_graph.py routes
        # manual_ingest_node -> study_detection_node directly), so stage 1 is
        # really "Manual Ingest", not "Search" -- see dashboard.py's
        # _render_agent_page().
        pipeline["mode"] = "manual" if paper_files else "auto"

        with _Heartbeat(run_id):
            orch  = MetaAnalysisOrchestrator(output_dir=output_dir)

            if not paper_files:
                if _config.PAPER_SELECTION_GATE:
                    # Pause right after the search agent: the user can decline
                    # found papers and add further PDFs before full-text fetch.
                    graph_state = orch.run_until_search_review(prompt, paper_files=None, pooling_model=pooling_model)
                    pipeline["pending_graph_state"] = graph_state
                    pipeline["awaiting_paper_selection"] = True
                    pipeline["done"] = False
                    if run_id:
                        _run_store.save_pause_state(run_id, "after_search", graph_state)
                        _run_store.set_status(run_id, "awaiting_paper_selection")
                    n_found = len(graph_state.get("papers_eligible", []))
                    log_queue.put(json.dumps({
                        "level": "SUCCESS",
                        "msg":   f"{n_found} paper(s) found — review the selection, "
                                 f"decline papers or add your own PDFs, then continue.",
                        "time":  time.strftime("%H:%M:%S"),
                    }))
                    return

                graph_state = orch.run_until_fulltext_review(prompt, paper_files=None, pooling_model=pooling_model)
                _after_fulltext_stage(orch, graph_state, pipeline, log_queue, run_id)
                return

            state = orch.run(prompt, paper_files=paper_files or None, pooling_model=pooling_model)

            results = _results_from_pipeline_state(state, output_dir)

            pipeline["results"] = results
            pipeline["done"]    = True
            if run_id:
                if orch.last_graph_state is not None:
                    _run_store.persist_snapshot(run_id, orch.last_graph_state,
                                                 included_studies=state.included_studies)
                _run_store.finish_run(run_id, results_json=results,
                                       pipeline_state_json=state.model_dump(mode="json"))
                _archive_to_benchmark_runs(run_id, output_dir)

            log_queue.put(json.dumps({
                "level": "SUCCESS",
                "msg":   "=== Pipeline complete ===",
                "time":  time.strftime("%H:%M:%S"),
            }))

    except RunCancelled:
        _mark_cancelled(pipeline, log_queue, run_id)
    except Exception as exc:
        logger.error(f"Pipeline error: {exc}", exc_info=True)
        pipeline["error"] = str(exc)
        pipeline["done"]  = True
        if run_id:
            _run_store.fail_run(run_id, str(exc), error_traceback=traceback.format_exc(),
                                 failure_stage=pipeline.get("current_stage_id"))
        log_queue.put(json.dumps({
            "level": "ERROR",
            "msg":   f"Pipeline failed: {exc}",
            "time":  time.strftime("%H:%M:%S"),
        }))
    finally:
        pipeline["running"] = False
        log_queue.put(json.dumps({"level": "DONE", "msg": "__done__", "time": ""}))
        if handler is not None:
            _detach_handler(handler)


def _load_pending_graph_state(pipeline: dict, run_id: Optional[str], phase: str):
    """Prefer the in-memory pipeline dict (fast path, same-process -- the
    thread backend always hits this) and fall back to Postgres (the ONLY
    path available when the pausing execution and this resume happened in
    different OS processes -- always true for the celery backend, and also
    a resilience bonus for the thread backend across an API restart)."""
    graph_state = pipeline.get("pending_graph_state")
    if graph_state:
        return graph_state
    if run_id:
        return _run_store.load_pause_state(run_id, phase)
    return None


def execute_continue(output_dir: str, session_id: str, run_id: str = None) -> None:
    handler = None
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    _start_cancellable(pipeline)
    try:
        from orchestrator import MetaAnalysisOrchestrator
        from core_utils import setup_logging
        setup_logging(logging.INFO)
        handler = _attach_handler(session_id, run_id=run_id)
        if run_id:
            _run_store.claim_run(run_id, from_status="awaiting_review")

        graph_state = _load_pending_graph_state(pipeline, run_id, "after_eligibility")
        if not graph_state:
            raise RuntimeError("No paused paper-review state found for this session.")

        pipeline["running"] = True
        pipeline["done"] = False
        pipeline["error"] = None
        pipeline["awaiting_review"] = False

        with _Heartbeat(run_id):
            orch = MetaAnalysisOrchestrator(output_dir=output_dir)
            state = orch.continue_after_review(graph_state)
            pipeline["pending_graph_state"] = None
            pipeline["results"] = _results_from_pipeline_state(state, output_dir)
            pipeline["done"] = True
            if run_id:
                if orch.last_graph_state is not None:
                    _run_store.persist_snapshot(run_id, orch.last_graph_state,
                                                 included_studies=state.included_studies)
                _run_store.finish_run(run_id, results_json=pipeline["results"],
                                       pipeline_state_json=state.model_dump(mode="json"))
                _archive_to_benchmark_runs(run_id, output_dir)

            log_queue.put(json.dumps({
                "level": "SUCCESS",
                "msg":   "=== Pipeline complete ===",
                "time":  time.strftime("%H:%M:%S"),
            }))

    except RunCancelled:
        _mark_cancelled(pipeline, log_queue, run_id)
    except Exception as exc:
        logger.error(f"Pipeline resume error: {exc}", exc_info=True)
        pipeline["error"] = str(exc)
        pipeline["done"] = True
        if run_id:
            _run_store.fail_run(run_id, str(exc), error_traceback=traceback.format_exc(),
                                 failure_stage=pipeline.get("current_stage_id"))
        log_queue.put(json.dumps({
            "level": "ERROR",
            "msg":   f"Pipeline resume failed: {exc}",
            "time":  time.strftime("%H:%M:%S"),
        }))
    finally:
        pipeline["running"] = False
        log_queue.put(json.dumps({"level": "DONE", "msg": "__done__", "time": ""}))
        if handler is not None:
            _detach_handler(handler)


def execute_search_selection_and_continue(output_dir: str, session_id: str, excluded_ids: list,
                                           pdf_paths: list, run_id: str = None) -> None:
    """Apply the user's paper selection (declined papers, extra PDFs), run
    full-text retrieval, then continue exactly like a run that never paused:
    full-text upload pause if some papers could not be retrieved, otherwise
    eligibility and the paper-tracking review gate."""
    handler = None
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    _start_cancellable(pipeline)
    try:
        from orchestrator import MetaAnalysisOrchestrator
        from core_utils import setup_logging
        setup_logging(logging.INFO)
        handler = _attach_handler(session_id, run_id=run_id)
        if run_id:
            _run_store.claim_run(run_id, from_status="awaiting_paper_selection")

        graph_state = _load_pending_graph_state(pipeline, run_id, "after_search")
        if not graph_state:
            raise RuntimeError("No paused paper-selection state found for this session.")

        pipeline["running"] = True
        pipeline["done"] = False
        pipeline["error"] = None
        pipeline["awaiting_paper_selection"] = False

        with _Heartbeat(run_id):
            orch = MetaAnalysisOrchestrator(output_dir=output_dir)
            graph_state = orch.continue_after_search_review(
                graph_state, excluded_ids=excluded_ids or [], pdf_paths=pdf_paths or [])
            _after_fulltext_stage(orch, graph_state, pipeline, log_queue, run_id)

    except RunCancelled:
        _mark_cancelled(pipeline, log_queue, run_id)
    except Exception as exc:
        logger.error(f"Paper selection error: {exc}", exc_info=True)
        pipeline["error"] = str(exc)
        pipeline["done"] = True
        if run_id:
            _run_store.fail_run(run_id, str(exc), error_traceback=traceback.format_exc(),
                                 failure_stage=pipeline.get("current_stage_id"))
        log_queue.put(json.dumps({
            "level": "ERROR",
            "msg":   f"Paper selection failed: {exc}",
            "time":  time.strftime("%H:%M:%S"),
        }))
    finally:
        pipeline["running"] = False
        log_queue.put(json.dumps({"level": "DONE", "msg": "__done__", "time": ""}))
        if handler is not None:
            _detach_handler(handler)


def execute_upload_and_continue(output_dir: str, session_id: str, pdf_paths: list,
                                 run_id: str = None) -> None:
    """Match any uploaded PDFs to missing papers, inject matches, then resume
    exactly like execute_continue (stops again at the paper-tracking review gate).
    Called with an empty pdf_paths list for "Continue Without Uploading"."""
    handler = None
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    _start_cancellable(pipeline)
    try:
        from orchestrator import MetaAnalysisOrchestrator
        from agents.paper_reading_agent import ingest_uploaded_fulltext_pdfs
        from core_utils import setup_logging
        setup_logging(logging.INFO)
        handler = _attach_handler(session_id, run_id=run_id)
        if run_id:
            _run_store.claim_run(run_id, from_status="awaiting_fulltext_upload")

        graph_state = _load_pending_graph_state(pipeline, run_id, "after_fulltext")
        if not graph_state:
            raise RuntimeError("No paused full-text-upload state found for this session.")

        pipeline["running"] = True
        pipeline["done"] = False
        pipeline["error"] = None
        pipeline["awaiting_fulltext_upload"] = False

        with _Heartbeat(run_id):
            matched: list = []
            if pdf_paths:
                missing_papers = _missing_fulltext_papers(graph_state)
                matched, unmatched = ingest_uploaded_fulltext_pdfs(pdf_paths, missing_papers, output_dir)
                if matched:
                    logger.info(f"[FulltextUpload] Matched {len(matched)} uploaded PDF(s) to missing papers.")
                if unmatched:
                    logger.warning(
                        f"[FulltextUpload] {len(unmatched)} uploaded PDF(s) could not be "
                        f"matched to a missing paper by DOI or title."
                    )

            orch = MetaAnalysisOrchestrator(output_dir=output_dir)
            graph_state = orch.continue_after_fulltext_review(graph_state, uploaded_papers=matched)
            pipeline["pending_graph_state"] = graph_state
            pipeline["awaiting_review"] = True
            pipeline["done"] = False
            pipeline["results"] = {
                "n_retrieved": graph_state.get("n_search_retrieved", 0),
                "n_screened": len(graph_state.get("papers_eligible", [])),
                "n_eligible": len(graph_state.get("papers_eligible", [])),
                "audit_tracking_csv": "paper_tracking.csv",
            }
            if run_id:
                _run_store.save_pause_state(run_id, "after_eligibility", graph_state)
                _run_store.set_status(run_id, "awaiting_review")
                _run_store.persist_snapshot(run_id, graph_state)

            log_queue.put(json.dumps({
                "level": "SUCCESS",
                "msg":   "Paper tracking review ready — approve to continue.",
                "time":  time.strftime("%H:%M:%S"),
            }))

    except RunCancelled:
        _mark_cancelled(pipeline, log_queue, run_id)
    except Exception as exc:
        logger.error(f"Full-text upload error: {exc}", exc_info=True)
        pipeline["error"] = str(exc)
        pipeline["done"] = True
        if run_id:
            _run_store.fail_run(run_id, str(exc), error_traceback=traceback.format_exc(),
                                 failure_stage=pipeline.get("current_stage_id"))
        log_queue.put(json.dumps({
            "level": "ERROR",
            "msg":   f"Full-text upload failed: {exc}",
            "time":  time.strftime("%H:%M:%S"),
        }))
    finally:
        pipeline["running"] = False
        log_queue.put(json.dumps({"level": "DONE", "msg": "__done__", "time": ""}))
        if handler is not None:
            _detach_handler(handler)


def execute_downstream(prompt: str, output_dir: str, session_id: str, run_id: str = None) -> None:
    """Run only stages 5–9 on an already-existing meta_ready_results.json."""
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    _start_cancellable(pipeline)
    handler = None
    try:
        from orchestrator import MetaAnalysisOrchestrator
        from core_utils import setup_logging
        setup_logging(logging.INFO)
        handler = _attach_handler(session_id, run_id=run_id)
        if run_id:
            _run_store.claim_run(run_id)

        pipeline["running"]          = True
        pipeline["done"]             = False
        pipeline["error"]            = None
        pipeline["results"]          = None
        pipeline["current_stage_id"] = None
        pipeline["stage_logs"]       = {sid: [] for sid in STAGE_ORDER}

        with _Heartbeat(run_id):
            orch  = MetaAnalysisOrchestrator(output_dir=output_dir)
            state = orch.run_downstream(prompt)

            results = _results_from_pipeline_state(state, output_dir)

            pipeline["results"] = results
            pipeline["done"]    = True
            if run_id:
                if orch.last_graph_state is not None:
                    _run_store.persist_snapshot(run_id, orch.last_graph_state,
                                                 included_studies=state.included_studies)
                _run_store.finish_run(run_id, results_json=results,
                                       pipeline_state_json=state.model_dump(mode="json"))
                _archive_to_benchmark_runs(run_id, output_dir)

            log_queue.put(json.dumps({
                "level": "SUCCESS",
                "msg":   "=== Downstream analysis complete ===",
                "time":  time.strftime("%H:%M:%S"),
            }))

    except RunCancelled:
        _mark_cancelled(pipeline, log_queue, run_id)
    except Exception as exc:
        logger.error(f"Downstream analysis error: {exc}", exc_info=True)
        pipeline["error"] = str(exc)
        pipeline["done"]  = True
        if run_id:
            _run_store.fail_run(run_id, str(exc), error_traceback=traceback.format_exc(),
                                 failure_stage=pipeline.get("current_stage_id"))
        log_queue.put(json.dumps({
            "level": "ERROR",
            "msg":   f"Downstream analysis failed: {exc}",
            "time":  time.strftime("%H:%M:%S"),
        }))
    finally:
        pipeline["running"] = False
        log_queue.put(json.dumps({"level": "DONE", "msg": "__done__", "time": ""}))
        if handler is not None:
            _detach_handler(handler)
