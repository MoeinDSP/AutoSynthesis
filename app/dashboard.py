"""
AutoSynthesis — Web Dashboard

Run:
    python dashboard.py
Then open: http://localhost:8000
"""

import json
import logging
import os
import queue
import secrets
import shutil
import threading
import time
import traceback
import uuid
import csv
from pathlib import Path
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from utils.outcome_grouping import safe_filename_fragment
import config as _config
from persistence import run_store as _run_store
from api_runs import router as _api_runs_router

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(title="AutoSynthesis")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")

# SESSION_SECRET: falling back to a fresh random value on every process
# restart silently invalidates every existing session cookie (every client
# pinned to a run via that cookie, including n8n's HTTP-node cookie jars,
# loses its session). Harmless when restarts are rare; once Celery/Docker
# make restarts routine this becomes a real, confusing failure mode. Pin a
# real value via SESSION_SECRET in .env for any deployment that restarts
# more than once per session lifetime -- see .env.example.
_session_secret = os.getenv("SESSION_SECRET", "")
if not _session_secret:
    _session_secret = secrets.token_hex(32)
    logging.getLogger(__name__).warning(
        "[Session] SESSION_SECRET not set -- using a random value for this process "
        "only. Every existing session cookie will stop working on the next restart. "
        "Set SESSION_SECRET in .env for any deployment that restarts more than once "
        "per session lifetime."
    )
app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
    same_site="lax",
)
app.include_router(_api_runs_router)

# ── Agent metadata (descriptions, output files, relevant stats) ────────────────

AGENT_INFO: dict = {
    "s0": {
        "num": "Stage 0", "title": "Planning Agent", "color": "#7c3aed",
        "emoji": "🗺",
        "role": "Converts your free-text question into a structured analysis plan.",
        "description": (
            "The Planning Agent is the entry point of the pipeline. It sends your research "
            "question to an LLM which produces a <strong>MetaAnalysisPlan</strong> object "
            "containing:<br><br>"
            "• <b>Research question</b> — reformulated as a precise scientific claim<br>"
            "• <b>Keywords</b> — 3–5 search terms used across all 6 databases<br>"
            "• <b>Treatment &amp; control labels</b> — what is being compared<br>"
            "• <b>Inclusion / exclusion criteria</b> — PICO-style (Population, Intervention, "
            "Comparison, Outcome)<br>"
            "• <b>Moderators</b> — variables to test in subgroup analysis "
            "(e.g. age group, study design, country)<br>"
            "• <b>Outcome measure</b> — what is being measured<br><br>"
            "This plan is passed to every downstream agent and controls search terms, "
            "screening criteria, data extraction fields, and moderator analyses."
        ),
        "output_files": ["plan.json"],
        "stats_keys": ["research_question", "treatment", "control"],
    },
    "s1": {
        "num": "Stage 1", "title": "Search Agent", "color": "#1d4ed8",
        "emoji": "🔍",
        "role": "Queries 6 academic databases in parallel and deduplicates results.",
        "description": (
            "The Search Agent queries multiple databases simultaneously using the keywords "
            "from the plan:<br><br>"
            "• <b>arXiv</b> — open-access preprints (CS, physics, biology, psychology)<br>"
            "• <b>PubMed</b> — biomedical literature via NCBI Entrez API (with API key)<br>"
            "• <b>Semantic Scholar</b> — broad academic coverage across many disciplines<br>"
            "• <b>CrossRef</b> — metadata for Springer, Elsevier, Wiley publications<br>"
            "• <b>OSF Preprints</b> — 10 providers: PsyArXiv, SocArXiv, MetaArXiv, etc.<br><br>"
            "Results are merged and deduplicated by title similarity. Each paper gets a "
            "unique ID (<code>arxiv:XXXX</code>, <code>pubmed:XXXX</code>, etc.) and a source label."
        ),
        "output_files": ["papers_01_retrieved.json", "search_queries.json"],
        "stats_keys": ["n_retrieved"],
    },
    "s2": {
        "num": "Stage 2", "title": "Screening Agent", "color": "#0891b2",
        "emoji": "🔬",
        "role": "Screens papers by title and abstract with liberal inclusion criteria.",
        "description": (
            "The Screening Agent performs the first PRISMA filter: title and abstract screening.<br><br>"
            "For each paper the LLM reads the title and abstract and decides: "
            "<b>include</b> or <b>exclude</b>.<br><br>"
            "The screening is <b>deliberately liberal</b> — the agent errs on the side of inclusion. "
            "A false exclusion here is unrecoverable (the paper is gone forever), while false "
            "inclusions are caught at the stricter eligibility stage.<br><br>"
            "Exclusion reasons: clearly off-topic, wrong population, clearly wrong study "
            "design (editorial, opinion, systematic review). Papers without abstracts are "
            "usually included to be safe."
        ),
        "output_files": ["papers_02_screened.json"],
        "stats_keys": ["n_screened"],
    },
    "s3b": {
        "num": "Stage 3b", "title": "Full-Text Fetcher", "color": "#0369a1",
        "emoji": "📥",
        "role": "Downloads full-text PDFs/XML using 5 fallback retrieval strategies.",
        "description": (
            "The Full-Text Fetcher is a retrieval module (not an LLM agent) that downloads "
            "complete article text for retrieved papers, trying each strategy in order until "
            "one succeeds:<br><br>"
            "1. Direct <code>pdf_url</code> on the record (Semantic Scholar open-access PDF, OSF)<br>"
            "2. Derived arXiv PDF URL from the abstract page URL<br>"
            "3. PubMed Central (PMC) full text via the NCBI eLink API<br>"
            "4. Unpaywall open-access PDF lookup by DOI<br>"
            "5. Semantic Scholar title lookup for an open-access PDF<br><br>"
            "HTML tables in the extracted text are converted to Markdown. Output is capped at "
            "120,000 characters to stay within LLM context limits.<br><br>"
            "<b>Papers for which no strategy succeeds are dropped here</b> — they do not "
            "continue to eligibility or extraction. This is tracked in the audit CSVs under the "
            "<code>full_text_fetch</code> exclusion stage."
        ),
        "output_files": [],
        "stats_keys": [],
    },
    "s3": {
        "num": "Stage 3", "title": "Eligibility Agent", "color": "#7c3aed",
        "emoji": "✅",
        "role": "Strict full-text eligibility using PICO criteria from the plan.",
        "description": (
            "The Eligibility Agent performs the second PRISMA filter: strict full-text "
            "eligibility assessment.<br><br>"
            "The LLM reads the full text (or abstract if unavailable) and applies the "
            "plan's inclusion criteria:<br><br>"
            "• Correct study design (RCT, quasi-experimental, controlled study)<br>"
            "• Correct population matching the plan<br>"
            "• Correct intervention vs. control<br>"
            "• Quantitative outcome data present (means, SDs, t/F-values, or proportions)<br><br>"
            "Exclusion categories:<br>"
            "• <code>insufficient_design</code> — wrong study type (review, opinion, case study)<br>"
            "• <code>missing_data</code> — no usable statistics to compute an effect size<br>"
            "• <code>wrong_population</code> / <code>wrong_intervention</code> / <code>other</code>"
        ),
        "output_files": ["papers_03_eligible.json"],
        "stats_keys": ["n_eligible"],
    },
    "s4": {
        "num": "Stage 4", "title": "Data Extraction Agent", "color": "#b45309",
        "emoji": "📊",
        "role": "Extracts means, SDs, sample sizes, t/F-values, and moderator variables.",
        "description": (
            "The Data Extraction Agent reads each eligible paper and extracts all quantitative "
            "data needed to compute effect sizes:<br><br>"
            "<b>Primary statistics (priority order):</b><br>"
            "1. Means + standard deviations for treatment and control groups<br>"
            "2. t-value from an independent-samples t-test<br>"
            "3. F-value from a one-way ANOVA<br>"
            "4. Proportions (for binary outcomes)<br><br>"
            "<b>Sample sizes:</b> n_treatment, n_control (or total n_participants)<br><br>"
            "<b>Moderator variables:</b> up to 5 variables from the plan (e.g. age_group, "
            "study_design, country, intervention_duration) extracted as categorical or numeric.<br><br>"
            "Each paper can contribute multiple StudyData records (multiple outcomes, time "
            "points, or subgroups). Output is saved to <code>studies.json</code> and "
            "<code>extracted_data.csv</code>."
        ),
        "output_files": ["studies.json", "extracted_data.csv"],
        "stats_keys": ["n_studies"],
    },
    "s5": {
        "num": "Stage 5", "title": "Effect Size Agent", "color": "#15803d",
        "emoji": "📐",
        "role": "Computes Hedges' g from extracted statistics using a priority cascade.",
        "description": (
            "The Effect Size Agent converts raw statistics into <b>Hedges' g</b> — a "
            "standardised effect size that corrects for small-sample bias (unlike Cohen's d).<br><br>"
            "<b>Computation priority cascade:</b><br>"
            "1. Means + SDs → pooled SD → Cohen's d → Hedges' g (× correction factor J)<br>"
            "2. t-value + sample sizes → d = t × √(1/n₁ + 1/n₂) → g<br>"
            "3. F-value (1 df) → t = √F → same as above<br>"
            "4. Proportions → arcsine transformation → g<br><br>"
            "Correction factor J = 1 − 3 / (4(n₁+n₂−2) − 1) reduces bias for small samples.<br><br>"
            "Each <code>EffectSizeRecord</code> stores: g, variance, standard error, 95% CI, "
            "and moderator metadata. Variance is used as the inverse weight in the meta-analysis model."
        ),
        "output_files": [],
        "stats_keys": ["n_effects"],
    },
    "s6": {
        "num": "Stage 6", "title": "Meta-Analysis Agent", "color": "#0f766e",
        "emoji": "🌲",
        "role": "Pools the studies with the chosen model (R metafor) and generates forest + distribution plots.",
        "description": (
            "The Meta-Analysis Agent pools effect sizes in R with <b>metafor</b>, using the model "
            "chosen for the run: a <b>fixed-effect</b> model, a <b>random-effects</b> model with any "
            "of metafor's τ² estimators (REML, DL, ML, HE, HS, SJ, PM, EB), or <b>unrestricted "
            "weighted least squares (UWLS)</b>. The model is picked in the <i>Pooling model</i> menu "
            "or named in the question; otherwise random effects with REML is used.<br><br>"
            "<b>Statistical outputs:</b><br>"
            "• Pooled effect with 95% CI — the main result. Usually Hedges' g, but pooled "
            "natively on Risk Ratio/Odds Ratio/Mean Difference when the outcome's own effect "
            "measure is confidently resolved (see utils/effect_measures.py) — the stat card "
            "below is always labeled with whichever measure was actually used.<br>"
            "• p-value (two-tailed, H₀: g = 0)<br>"
            "• I² — percentage of variance due to heterogeneity<br>"
            "• τ² and τ — between-study variance<br>"
            "• Q-statistic and its p-value<br><br>"
            "<b>Plots generated:</b> forest plot, cumulative forest plot, effect size "
            "distribution (violin + KDE), bubble chart (g vs. sample size), "
            "heterogeneity summary (I² donut + Q/τ²/H² statistics)."
        ),
        "output_files": ["forest_plot.png", "cumulative_plot.png",
                         "effect_distribution.png", "bubble_chart.png",
                         "heterogeneity_summary.png"],
        "stats_keys": ["pooled_g", "ci_lower", "ci_upper", "p_value", "i_squared", "tau", "k"],
    },
    "s7": {
        "num": "Stage 7", "title": "Moderator Agent", "color": "#9333ea",
        "emoji": "🔀",
        "role": "Tests moderator variables to explain between-study heterogeneity.",
        "description": (
            "The Moderator Agent tests whether categorical/numeric variables explain the "
            "heterogeneity (I²) found in the overall model.<br><br>"
            "For each moderator (e.g. age_group, study_design, intervention_type):<br><br>"
            "<b>Subgroup analysis:</b> Studies split by moderator value; a separate pooled "
            "effect size is computed per group. Q_between tests whether groups differ significantly.<br><br>"
            "<b>Meta-regression:</b> Moderator used as a predictor in weighted linear regression. "
            "Outputs: regression coefficient (how much g changes per unit), R² (variance "
            "explained), and residual I².<br><br>"
            "<b>Combined model:</b> All moderators entered simultaneously. The combined R² "
            "tells you what fraction of between-study variance all moderators together explain.<br><br>"
            "Plots: a bar/scatter moderator plot and a violin subgroup plot per moderator."
        ),
        "output_files": [],   # dynamic: violin_*.png, moderator_*.png
        "stats_keys": [],
    },
    "s8": {
        "num": "Stage 8", "title": "Bias Agent", "color": "#dc2626",
        "emoji": "⚖",
        "role": "Assesses publication bias via Egger's test, Begg's rank test, trim-and-fill, PET-PEESE and the funnel plot.",
        "description": (
            "The Bias Agent assesses <b>publication bias</b> — the tendency for positive "
            "results to be published more than null results, inflating pooled effect sizes.<br><br>"
            "<b>Egger's test:</b> Weighted linear regression of effect size / SE on 1/SE. "
            "A significant intercept (p &lt; 0.10) suggests funnel plot asymmetry.<br><br>"
            "<b>Trim-and-fill:</b> Iteratively removes extreme studies, estimates the true "
            "center, then 'fills in' mirror-image studies that would be missing under bias. "
            "k₀ = estimated number of missing studies.<br><br>"
            "<b>Begg's rank test:</b> Kendall's τ between standardized effects and their "
            "variances (metafor <code>ranktest</code>).<br><br>"
            "<b>PET-PEESE:</b> Weighted least squares meta-regressions of the effect on its "
            "SE (PET) and on its variance (PEESE); the intercept is the effect corrected for "
            "small-study effects. If PET's intercept is significant (p &lt; 0.05), PEESE is used, "
            "otherwise PET. Unreliable with fewer than 10 studies.<br><br>"
            "<b>Funnel plot:</b> Scatter of effect size vs. standard error (SE). Symmetric "
            "scatter = no bias; asymmetry = possible bias.<br><br>"
            "Bias risk classification: <b>low</b> (Egger p ≥ 0.10, k₀ = 0), "
            "<b>moderate</b>, or <b>high</b>."
        ),
        "output_files": ["funnel_plot.png"],
        "stats_keys": ["bias_risk", "eggers_p", "trim_fill_k0"],
    },
    "s8b": {
        "num": "Stage 8B", "title": "Risk of Bias Agent", "color": "#b45309",
        "emoji": "🚦",
        "role": "Assesses per-study risk of bias using RoB 2 (randomized) or ROBINS-I (non-randomized).",
        "description": (
            "The Risk of Bias Agent judges internal validity <b>per included study</b>, "
            "following the two standard Cochrane tools.<br><br>"
            "<b>Step 1 — Design classification:</b> the LLM reads the Methods section and "
            "classifies the study as randomized or non-randomized, from explicit evidence "
            "of random allocation only.<br><br>"
            "<b>Step 2 — Domain judgments:</b> randomized studies are assessed on the 5 "
            "RoB 2 domains (low / some_concerns / high); non-randomized studies are assessed "
            "on the 7 ROBINS-I domains (low / moderate / serious / critical / no_information). "
            "Each domain judgment includes a rationale and, where possible, a verbatim "
            "evidence quote.<br><br>"
            "<b>Step 3 — Overall judgment:</b> at least as severe as the single worst domain "
            "judgment, per standard Cochrane convention.<br><br>"
            "Output: one traffic-light plot per tool actually used, plus "
            "<code>rob_assessments.json</code> with full per-domain rationale."
        ),
        "output_files": ["rob_traffic_light_rob2.png", "rob_traffic_light_robins_i.png", "rob_assessments.json"],
        "stats_keys": [],
    },
    "s9": {
        "num": "Stage 9", "title": "Report Agent", "color": "#475569",
        "emoji": "📝",
        "role": "Generates a structured Markdown report following PRISMA 2020 guidelines.",
        "description": (
            "The Report Agent compiles all results into a structured Markdown report "
            "following PRISMA 2020 reporting guidelines.<br><br>"
            "<b>Report sections:</b><br>"
            "1. Research Question &amp; Analysis Plan<br>"
            "2. PRISMA Flow — retrieved → screened → eligible → included → effects<br>"
            "3. Study Characteristics — table of included studies<br>"
            "4. Main Result — pooled g, 95% CI, p-value, narrative interpretation<br>"
            "5. Heterogeneity — I², τ², Q-statistic<br>"
            "6. Moderator Analyses — per-moderator results (g, Q_between, R²)<br>"
            "7. Publication Bias — Egger's test, trim-and-fill, funnel plot interpretation<br>"
            "8. Forest Plot — reference to generated image<br>"
            "9. Conclusions — plain-language summary<br><br>"
            "The LLM provides narrative interpretations of the main result and bias assessment, "
            "translating statistics into scientific language."
        ),
        "output_files": ["report.md", "extracted_data.csv", "results.json", "final_results_summary.csv"],
        "stats_keys": [],
    },
}

# Manual-upload runs skip the Search Agent entirely (pipeline_graph.py routes
# manual_ingest_node -> study_detection_node directly, no database query ever
# happens) but its log lines still start with "=== STAGE 1: ... ===", so they
# land in the same "s1" slot as the Search Agent. Swap this in for stage 1's
# sidebar label/detail page whenever pipeline["mode"] == "manual" (see
# _render_agent_page()) so the UI doesn't imply a database search ran.
MANUAL_INGEST_INFO: dict = {
    "num": "Stage 1", "title": "Manual Ingest", "color": "#1d4ed8",
    "emoji": "📥",
    "role": "Reads your uploaded PDFs directly — no database search happens in this mode.",
    "description": (
        "In manual-upload mode, Search/Screening/Eligibility (stages 1–3) are skipped "
        "entirely -- every paper you uploaded is treated as already-included, and its text "
        "is extracted straight from the PDF via MinerU (cloud, then local) or LlamaParse "
        "as a fallback.<br><br>"
        "No academic database is queried in this mode."
    ),
    "output_files": [],
    "stats_keys": [],
}

# ── Pipeline execution (Phase 4: moved to run_service.py so both the thread
#    backend below AND tasks.py's Celery tasks call the exact same code --
#    see run_service.py's module docstring). Re-imported here under their
#    original names so nothing else in this file needs to change. ──────────
import run_service
from run_service import (       # noqa: F401 -- re-exported for anything importing these from dashboard
    STAGE_PATTERNS, STAGE_ORDER,
    _state_lock, _pipelines, _log_queues,
    _new_pipeline_state, _get_pipeline, _get_log_queue,
    _SSEHandler, _attach_handler, _detach_handler,
    _meta_analysis_measure_fields, _results_from_pipeline_state,
    _missing_fulltext_papers, status_from_run_row,
)
_run_pipeline = run_service.execute_run
_continue_pipeline = run_service.execute_continue
_upload_missing_fulltext_and_continue = run_service.execute_upload_and_continue
_continue_after_paper_selection = run_service.execute_search_selection_and_continue
_run_downstream = run_service.execute_downstream


def _new_run_id() -> str:
    return secrets.token_urlsafe(16)


def _derive_run_status(pipeline: dict) -> str:
    """Canonical status string (matches persistence's `runs.status` CHECK
    constraint) derived from today's boolean flags -- the in-memory dict
    stays the source of truth through Phase 3 (Postgres is written
    alongside it, additively); this mapping is what lets /status expose a
    single `status` string without changing any existing boolean's
    meaning."""
    if pipeline.get("cancelled"):
        return "cancelled"
    if pipeline.get("awaiting_paper_selection"):
        return "awaiting_paper_selection"
    if pipeline.get("awaiting_fulltext_upload"):
        return "awaiting_fulltext_upload"
    if pipeline.get("awaiting_review"):
        return "awaiting_review"
    if pipeline.get("running"):
        return "running"
    if pipeline.get("error"):
        return "failed"
    if pipeline.get("done"):
        return "completed"
    return "queued"


def _get_session_id(request: Request) -> str:
    session_id = request.session.get("session_id")
    if not session_id:
        session_id = secrets.token_urlsafe(16)
        request.session["session_id"] = session_id
    return session_id


def _get_output_dir(session_id: str) -> Path:
    return Path(OUTPUT_DIR) / session_id


def _celery_backend() -> bool:
    return _config.RUN_EXECUTION_BACKEND == "celery"


def _run_row_if_celery(pipeline: dict):
    """A celery-backed run's execution happens in a separate OS process (a
    worker) -- this API process's in-memory `pipeline` dict is never
    mutated by it, so Postgres is the only place its live state can be
    read from. Returns None (falls back to the in-memory dict, today's
    exact thread-backend behavior) when the backend is "thread" or no run
    has started yet."""
    if not _celery_backend():
        return None
    run_id = pipeline.get("run_id")
    if not run_id:
        return None
    return _run_store.get_run(run_id)


# ── API endpoints ──────────────────────────────────────────────────────────────

class RunRequest(BaseModel):
    prompt: str
    paper_files: list = []    # empty = automatic search mode; server-side PDF paths from /upload
    model: str = ""           # optional: one of config.AVAILABLE_MODELS ids; "" = server default
    pooling_model: str = ""   # optional: one of statistics.metafor_engine.POOLING_MODELS keys;
                               # "" = whatever the prompt asks for, else REML random effects
    external_ref: str = ""    # optional Cochrane review id (e.g. "CD013591") -- when set, this run's
                               # full output is archived under cochrane_benchmark/runs/<external_ref>/
                               # once it completes; see run_service._archive_to_benchmark_runs().


@app.get("/models")
def list_models():
    from statistics.metafor_engine import POOLING_MODELS, DEFAULT_POOLING_MODEL
    return {"models": _config.AVAILABLE_MODELS, "current": _config.MODEL_NAME,
            "pooling_models": [{"id": k, "label": v} for k, v in POOLING_MODELS.items()],
            "default_pooling_model": DEFAULT_POOLING_MODEL}


# ── Landing-page extras: paper link, logo, demo, imprint ─────────────────────
_HERE = Path(__file__).resolve().parent
DEMO_DIR = _HERE / "demo"
ASSETS_DIR = _HERE / "assets"
_ASSET_TYPES = {".png", ".jpg", ".jpeg", ".svg", ".pdf"}


@app.get("/site_info")
def site_info():
    """Paper banner + demo availability. A PDF dropped at assets/paper.pdf is
    used as the paper link when PAPER_URL is not set."""
    paper_url = _config.PAPER_URL
    if not paper_url and (ASSETS_DIR / "paper.pdf").is_file():
        paper_url = "/assets/paper.pdf"
    return {
        "paper_title": _config.PAPER_TITLE,
        "paper_url": paper_url,
        "demo_available": bool(_demo_examples()),
        "demos": [{"id": d["id"], "title": d["title"], "subtitle": d["subtitle"]} for d in _demo_examples()],
    }


def _demo_examples() -> list:
    """Installed demo examples: every demo/<id>/ folder holding results.json
    and files/. meta.json supplies title, subtitle, prompt, note and order."""
    out = []
    if not DEMO_DIR.is_dir():
        return out
    for d in DEMO_DIR.iterdir():
        if not (d.is_dir() and (d / "results.json").is_file() and (d / "files").is_dir()):
            continue
        meta = {}
        if (d / "meta.json").is_file():
            try:
                meta = json.loads((d / "meta.json").read_text())
            except ValueError:
                meta = {}
        out.append({"id": d.name, "path": d, "title": meta.get("title") or d.name,
                    "subtitle": meta.get("subtitle", ""), "prompt": meta.get("prompt", ""),
                    "note": meta.get("note", ""), "order": meta.get("order", 99)})
    return sorted(out, key=lambda e: (e["order"], e["id"]))


@app.get("/assets/{name}")
def serve_asset(name: str):
    path = ASSETS_DIR / name
    if "/" in name or "\\" in name or path.suffix.lower() not in _ASSET_TYPES or not path.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(str(path))


class DemoLoadRequest(BaseModel):
    id: str = ""   # demo/<id> folder; "" = the first example


_DEMO_MANIFEST = ".demo_files.json"


@app.post("/demo/load")
def load_demo(request: Request, req: Optional[DemoLoadRequest] = None):
    """Show a pre-computed, real pipeline run -- no LLM, search or R is invoked.
    The chosen example's files (demo/<id>/files + results.json) are copied into
    this session's output directory and the session is marked as a finished
    run, so the normal results view renders it unchanged. Files copied by a
    previously loaded example are removed first so examples never mix."""
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    if pipeline["running"] or pipeline.get("awaiting_review") or pipeline.get("awaiting_paper_selection") \
            or pipeline.get("awaiting_fulltext_upload"):
        return {"ok": False, "error": "A pipeline is in progress. Finish or wait for it before loading the demo."}
    examples = _demo_examples()
    if not examples:
        return {"ok": False, "error": "No demo data is installed on this server."}
    want = (req.id if req else "").strip()
    ex = next((e for e in examples if e["id"] == want), None) if want else examples[0]
    if ex is None:
        return {"ok": False, "error": "Unknown demo example."}
    results = json.loads((ex["path"] / "results.json").read_text())
    results["report_path"] = os.path.basename(results.get("report_path") or "")
    results["demo"] = True
    flow_file = ex["path"] / "files" / "prisma_flowchart.json"
    if "prisma_flow" not in results and flow_file.is_file():
        try:
            results["prisma_flow"] = json.loads(flow_file.read_text())
        except ValueError:
            pass
    out = _get_output_dir(session_id)
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / _DEMO_MANIFEST
    if manifest.is_file():
        try:
            for name in json.loads(manifest.read_text()):
                p = out / os.path.basename(name)
                if p.is_file():
                    p.unlink()
        except ValueError:
            pass
    copied = []
    for f in (ex["path"] / "files").iterdir():
        if f.is_file():
            shutil.copy2(f, out / f.name)
            copied.append(f.name)
    manifest.write_text(json.dumps(copied))
    pipeline.update({
        "running": False, "done": True, "error": None, "results": results,
        "current_stage_id": None, "awaiting_review": False, "awaiting_paper_selection": False,
        "awaiting_fulltext_upload": False, "pending_graph_state": None, "mode": "auto", "run_id": None, "cancelled": False,
    })
    return {"ok": True, "id": ex["id"], "title": ex["title"], "prompt": ex["prompt"], "note": ex["note"]}


_IMPRINT_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imprint | AutoSynthesis</title>
<style>
 body{margin:0;background:#f5f7fa;color:#1f2937;font-family:'Segoe UI',system-ui,sans-serif;line-height:1.65}
 header{background:#fff;border-bottom:1px solid #dbe2ea;padding:12px 32px;display:flex;align-items:center;gap:14px}
 header a{color:#2563eb;text-decoration:none;font-weight:600;font-size:.9rem}
 header .sp{margin-left:auto}
 header img{height:48px}
 main{max-width:820px;margin:0 auto;padding:32px 24px 60px}
 h1{font-size:1.6rem;margin:0 0 6px} h2{font-size:1.05rem;margin:28px 0 6px}
 p{margin:6px 0} .muted{color:#5b6776;font-size:.9rem}
</style></head><body>
<header><a href="/">&larr; AutoSynthesis</a><span class="sp"></span><img src="/assets/berd-nfdi-logo.png" alt="BERD@NFDI"></header>
<main>
<h1>Imprint</h1>
<p class="muted">Provider information pursuant to Section 5 of the German Digital Services Act (DDG) and Section 18(2) of the German Interstate Media Treaty (MStV).</p>

<h2>Service provider</h2>
<p>Ludwig-Maximilians-Universit&auml;t M&uuml;nchen<br>Geschwister-Scholl-Platz 1<br>80539 Munich, Germany</p>
<p>Ludwig-Maximilians-Universit&auml;t M&uuml;nchen is a state institution of the Free State of Bavaria and a corporation under public law. It is legally represented by its President, Universit&auml;tsprofessor Dr. med. Dr. h.c. Matthias H. Tsch&ouml;p.</p>

<h2>Project and technical contact</h2>
<p>Institute of Artificial Intelligence (AI) in Management<br>Prof. Stefan Feuerriegel<br>Ludwigstr. 28 / RG<br>80539 Munich, Germany</p>

<h2>Contact</h2>
<p>Phone: +49 89 2180-0<br>Email: poststelle@verwaltung.uni-muenchen.de<br>Project contact: feuerriegel@lmu.de</p>
<p class="muted">Information on S/MIME-encrypted communication and the special electronic authority mailbox is available in the central LMU legal notice.</p>

<h2>Supervisory authority</h2>
<p>Bavarian State Ministry of Science and the Arts (Bayerisches Staatsministerium f&uuml;r Wissenschaft und Kunst)<br>Salvatorstra&szlig;e 2, 80327 Munich, Germany<br>www.stmwk.bayern.de</p>

<h2>VAT identification number</h2>
<p>Pursuant to Section 27a of the German VAT Act: DE811205325</p>

<h2>Responsible for content (Section 18(2) MStV)</h2>
<p>Ludwig-Maximilians-Universit&auml;t M&uuml;nchen, Dr. Christoph M&uuml;lke, Vice President for Economic and Personnel Administration, Geschwister-Scholl-Platz 1, 80539 Munich, Germany.</p>
<p>For project-specific content: Prof. Stefan Feuerriegel, Institute of Artificial Intelligence (AI) in Management, Ludwigstr. 28 / RG, 80539 Munich, Germany.</p>

<h2>Liability for content</h2>
<p>The content of this service was prepared with reasonable care. No guarantee is given for its accuracy, completeness or timeliness.</p>

<h2>Consumer dispute resolution</h2>
<p>This service does not conclude online purchase or service contracts with consumers. The EU online dispute resolution platform was discontinued on 20 July 2025, so no link to it is provided. We are not obliged and not willing to take part in dispute resolution proceedings before a consumer arbitration board.</p>

<h2>Notice on the service</h2>
<p>AutoSynthesis is an experimental research prototype for automated meta-analysis. Its outputs are generated automatically by language models and statistical software, may contain errors, and are not medical, clinical or other professional advice. Please verify results against the original studies before using them.</p>

<p>Information on data protection: <a href="/privacy" style="color:#2563eb">Privacy policy</a>.</p>
<p class="muted" style="margin-top:28px">The <a href="https://www.lmu.de/de/footer/impressum/index.html" style="color:#2563eb">central LMU M&uuml;nchen legal notice</a> also applies.</p>
</main></body></html>
"""


_PRIVACY_HTML = _IMPRINT_HTML[:_IMPRINT_HTML.index("<main>")].replace(
    "<title>Imprint | AutoSynthesis</title>", "<title>Privacy | AutoSynthesis</title>") + """<main>
<h1>Privacy policy</h1>
<p class="muted">Information pursuant to Articles 13 and 14 of the General Data Protection Regulation (GDPR).</p>

<h2>Controller</h2>
<p>Ludwig-Maximilians-Universit&auml;t M&uuml;nchen, Geschwister-Scholl-Platz 1, 80539 Munich, Germany,
legally represented by its President. Project contact: Prof. Stefan Feuerriegel, Institute of Artificial
Intelligence (AI) in Management, Ludwigstr. 28 / RG, 80539 Munich, Germany, feuerriegel@lmu.de.
See also the <a href="/imprint">Imprint</a>.</p>

<h2>Data protection officer</h2>
<p>Data Protection Officer of LMU Munich, Geschwister-Scholl-Platz 1, 80539 Munich, Germany,
datenschutz@lmu.de.</p>

<h2>What we store</h2>
<p><b>When you run an analysis:</b> the research question you enter, the PDF files you upload, the
settings of the run (e.g. the language model), and everything the pipeline produces: the analysis plan,
the papers found, screening and eligibility decisions, extracted data, statistics, plots and the report.</p>
<p><b>When you only look at the website or a demo:</b> no content you enter is stored; opening a demo only
copies the example's files into a folder for your browser session.</p>
<p><b>Technical data:</b> a session cookie that links your browser to your run (it contains no personal
information and is needed for the site to work), and technical request data (such as IP address and time) that the
web server may record for security and error analysis. Your browser's local storage remembers
whether you have already confirmed the full-run notice; this stays on your device.</p>
<p>Please do not enter personal, patient or other confidential information in your question or uploads.</p>

<h2>Purposes and legal basis</h2>
<p>We process this data to run the analysis you request, to show you the results, and for scientific research
on automated evidence synthesis and to improve AutoSynthesis (e.g. analysing which questions are asked and
where the pipeline fails). The legal basis is Art. 6(1)(e) GDPR in conjunction with Art. 4(1) of the Bavarian
Data Protection Act (BayDSG): the performance of LMU's public tasks in research and teaching. Results of the
research are published only in aggregated or anonymised form.</p>

<h2>Recipients</h2>
<ul>
<li><b>Hosting:</b> Hetzner Online GmbH, Gunzenhausen, Germany, with servers in the EU. Hetzner processes
the data on our behalf.</li>
<li><b>Language models:</b> to analyse your question and the papers, your question, the text of the papers
(including uploaded PDFs) and intermediate results are sent via OpenRouter, Inc. (USA) to the provider of the
selected model (e.g. Google for Gemini, OpenAI or Anthropic). These providers may be located outside the
EU, in particular in the USA. Where available, transfers rely on the EU-U.S. Data Privacy Framework or on
EU standard contractual clauses.</li>
<li><b>Scientific databases:</b> search queries derived from your question are sent to literature
databases and full-text services (e.g. PubMed, Semantic Scholar, Elsevier, arXiv) to find and download
papers.</li>
</ul>

<h2>How long we keep it</h2>
<p>Runs, uploads and results are kept for as long as they are needed for the research purposes above and are
then deleted. You can ask us to delete your run at any time (see below).</p>

<h2>Your rights</h2>
<p>You have the right to access (Art. 15 GDPR), rectification (Art. 16), erasure (Art. 17), restriction of
processing (Art. 18) and to object to the processing (Art. 21). To exercise them, contact
feuerriegel@lmu.de; it helps if you tell us roughly when you ran the analysis and what you asked. You also
have the right to lodge a complaint with a supervisory authority, for LMU the Bavarian State Commissioner for
Data Protection (Bayerischer Landesbeauftragter f&uuml;r den Datenschutz), Wagm&uuml;llerstra&szlig;e 18,
80538 Munich, Germany, www.datenschutz-bayern.de.</p>

<p class="muted" style="margin-top:28px">Last updated: November 2026.</p>
</main></body></html>
"""


@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return _PRIVACY_HTML


@app.get("/imprint", response_class=HTMLResponse)
def imprint():
    return _IMPRINT_HTML


@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    upload_dir = os.path.join(OUTPUT_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    saved = []
    for f in files:
        ext = os.path.splitext(f.filename or "")[1].lower()
        if ext != ".pdf":
            continue
        uid = uuid.uuid4().hex[:8]
        safe_name = f"{uid}_{f.filename}"
        dest = os.path.join(upload_dir, safe_name)
        with open(dest, "wb") as out:
            shutil.copyfileobj(f.file, out)
        saved.append({"name": f.filename, "path": dest})
    return {"ok": True, "files": saved}


# ── Server-wide run limit ─────────────────────────────────────────────────────
# A full run needs a few GB of RAM (Docker + R/metafor + PDF parsers), and the
# active model is a process-wide setting, so by default only one run may be
# active on the server at a time. Other visitors get a "please wait" pop-up.
MAX_CONCURRENT_RUNS = max(1, int(os.getenv("MAX_CONCURRENT_RUNS", "1") or "1"))
_run_slot_lock = threading.Lock()
SERVER_BUSY_MSG = ("Another analysis is currently running on the server. "
                   "Please wait until it finishes and try again.")


def _active_runs_elsewhere(session_id: str) -> int:
    """Number of runs currently executing in sessions other than this one."""
    if _celery_backend():
        rows = (_run_store.list_runs(status="running", limit=100) or []) + \
               (_run_store.list_runs(status="queued", limit=100) or [])
        return sum(1 for r in rows if r.get("session_id") != session_id)
    with _state_lock:
        return sum(1 for sid, p in _pipelines.items() if sid != session_id and p.get("running"))


def _server_busy(session_id: str) -> bool:
    return _active_runs_elsewhere(session_id) >= MAX_CONCURRENT_RUNS


@app.get("/server_busy")
def server_busy(request: Request):
    return {"busy": _server_busy(_get_session_id(request))}


@app.post("/run")
def run_pipeline(req: RunRequest, request: Request):
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    output_dir = _get_output_dir(session_id)
    existing_row = _run_row_if_celery(pipeline)
    if pipeline["running"] or (existing_row and existing_row["status"] in ("queued", "running")):
        return {"ok": False, "error": "A pipeline is already running."}
    if not req.prompt.strip():
        return {"ok": False, "error": "Please enter a research question."}
    with _run_slot_lock:
        if _server_busy(session_id):
            return {"ok": False, "busy": True, "error": SERVER_BUSY_MSG}
        if not _celery_backend():
            pipeline["running"] = True   # reserve the slot before the worker thread starts
    if req.model:
        if req.model not in [m["id"] for m in _config.AVAILABLE_MODELS]:
            pipeline["running"] = False
            return {"ok": False, "error": f"Unknown model: {req.model}"}
        if _celery_backend():
            return {"ok": False, "error": "Model selection needs RUN_EXECUTION_BACKEND=thread."}
        _config.set_active_model(req.model)
    from statistics.metafor_engine import POOLING_MODELS
    pooling_model = req.pooling_model.strip().upper() or None
    if pooling_model and pooling_model not in POOLING_MODELS:
        pipeline["running"] = False
        return {"ok": False, "error": f"Unknown pooling model: {req.pooling_model}"}
    files  = [f.strip() for f in req.paper_files  if f.strip()]
    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break
    run_id = _new_run_id()
    pipeline["run_id"]   = run_id
    pipeline["cancelled"] = False
    pipeline["done"]  = False
    pipeline["error"] = None
    pipeline["results"]          = None
    pipeline["current_stage_id"] = None
    pipeline["stage_logs"]       = {sid: [] for sid in AGENT_INFO}
    pipeline["awaiting_review"]  = False
    pipeline["awaiting_paper_selection"] = False
    pipeline["awaiting_fulltext_upload"] = False
    pipeline["pending_graph_state"] = None
    # Created synchronously (not inside the thread/task) so run_id is valid
    # and queryable via /api/runs/{run_id} the instant this response
    # returns -- a safe no-op when persistence is disabled (see
    # persistence/db.py).
    _run_store.create_run(
        run_id, req.prompt.strip(), str(output_dir),
        mode="manual" if files else "search", source="dashboard", session_id=session_id,
        execution_backend=_config.RUN_EXECUTION_BACKEND, paper_files=files or None,
        external_ref=req.external_ref.strip() or None,
    )
    if _celery_backend():
        from tasks import run_pipeline_task
        run_pipeline_task.apply_async(
            args=[req.prompt.strip(), str(output_dir), session_id, files or None, run_id, pooling_model])
    else:
        threading.Thread(target=_run_pipeline,
                         args=(req.prompt.strip(), str(output_dir), session_id, files or None, run_id,
                               pooling_model),
                         daemon=True).start()
    return {"ok": True, "run_id": run_id}


def _pending_search_state(pipeline: dict):
    """Paused graph state of a run waiting at the paper-selection gate, or
    None. Mirrors /missing_fulltext's thread-vs-celery handling."""
    row = _run_row_if_celery(pipeline)
    if row is not None:
        if row["status"] != "awaiting_paper_selection":
            return None
        return _run_store.load_pause_state(row["run_id"], "after_search")
    if not pipeline.get("awaiting_paper_selection"):
        return None
    return pipeline.get("pending_graph_state")


@app.get("/found_papers")
def found_papers(request: Request):
    pipeline = _get_pipeline(_get_session_id(request))
    graph_state = _pending_search_state(pipeline)
    if not graph_state:
        return {"ok": False, "error": "No pending paper selection for this session."}
    rows = [{
        "id":      p.id,
        "title":   p.title,
        "authors": ", ".join(p.authors or []) or "—",
        "year":    p.year or "—",
        "source":  p.source,
        "doi":     p.doi or "—",
        "url":     p.url or "",
    } for p in graph_state.get("papers_eligible", [])]
    return {"ok": True, "rows": rows, "total_rows": len(rows)}


@app.post("/submit_paper_selection")
async def submit_paper_selection(request: Request,
                                 excluded_ids: str = Form(default="[]"),
                                 files: List[UploadFile] = File(default=[])):
    """Continue after the paper-selection gate. `excluded_ids` is a JSON list
    of paper ids the user declined; `files` are extra PDFs to add."""
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    output_dir = _get_output_dir(session_id)
    row = _run_row_if_celery(pipeline)

    if row is None and pipeline["running"]:
        return {"ok": False, "error": "A pipeline is already running."}
    graph_state = _pending_search_state(pipeline)
    if not graph_state:
        return {"ok": False, "error": "There is no pending paper selection to continue."}

    try:
        excluded = json.loads(excluded_ids or "[]")
        if not isinstance(excluded, list):
            raise ValueError
        excluded = [str(x) for x in excluded]
    except ValueError:
        return {"ok": False, "error": "excluded_ids must be a JSON list of paper ids."}

    pdf_paths: list = []
    upload_dir = os.path.join(str(output_dir), "uploads")
    for f in files or []:
        ext = os.path.splitext(f.filename or "")[1].lower()
        if ext != ".pdf":
            continue
        os.makedirs(upload_dir, exist_ok=True)
        uid = uuid.uuid4().hex[:8]
        dest = os.path.join(upload_dir, f"{uid}_{f.filename}")
        with open(dest, "wb") as out:
            shutil.copyfileobj(f.file, out)
        pdf_paths.append(dest)

    found_ids = {p.id for p in graph_state.get("papers_eligible", [])}
    n_kept = len(found_ids - set(excluded))
    if n_kept == 0 and not pdf_paths:
        return {"ok": False,
                "error": "Every paper was declined and no PDF was added. "
                         "Keep at least one paper or upload a PDF to continue."}

    log_queue = _get_log_queue(session_id)
    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break

    pipeline["done"] = False
    pipeline["error"] = None
    run_id = pipeline.get("run_id")
    if _celery_backend():
        from tasks import continue_after_search_task
        continue_after_search_task.apply_async(args=[str(output_dir), session_id, excluded, pdf_paths, run_id])
    else:
        threading.Thread(
            target=_continue_after_paper_selection,
            args=(str(output_dir), session_id, excluded, pdf_paths, run_id),
            daemon=True,
        ).start()
    return {"ok": True, "run_id": run_id}


@app.get("/missing_fulltext")
def missing_fulltext(request: Request):
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    row = _run_row_if_celery(pipeline)
    if row is not None:
        # celery backend: the pause happened in a worker process -- this
        # API process's in-memory pending_graph_state was never set.
        if row["status"] != "awaiting_fulltext_upload":
            return {"ok": False, "error": "No pending full-text review for this session."}
        graph_state = _run_store.load_pause_state(row["run_id"], "after_fulltext")
    else:
        graph_state = pipeline.get("pending_graph_state")
        if not pipeline.get("awaiting_fulltext_upload"):
            graph_state = None
    if not graph_state:
        return {"ok": False, "error": "No pending full-text review for this session."}

    papers = _missing_fulltext_papers(graph_state)
    reasons = graph_state.get("papers_no_fulltext_reasons", {})
    rows = [{
        "title":   p.title,
        "authors": ", ".join(p.authors or []) or "—",
        "year":    p.year or "—",
        "source":  p.source,
        "doi":     p.doi or "—",
        "reason":  reasons.get(p.id, "no full text available from any retrieval strategy"),
    } for p in papers]
    return {"ok": True, "rows": rows, "total_rows": len(rows)}


@app.post("/upload_missing_fulltext")
async def upload_missing_fulltext(request: Request, files: List[UploadFile] = File(default=[])):
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    output_dir = _get_output_dir(session_id)
    row = _run_row_if_celery(pipeline)

    if row is not None:
        if row["status"] != "awaiting_fulltext_upload":
            return {"ok": False, "error": "There is no pending full-text review to continue."}
    else:
        if pipeline["running"]:
            return {"ok": False, "error": "A pipeline is already running."}
        if not pipeline.get("awaiting_fulltext_upload") or not pipeline.get("pending_graph_state"):
            return {"ok": False, "error": "There is no pending full-text review to continue."}

    pdf_paths: list = []
    if files:
        upload_dir = os.path.join(str(output_dir), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        for f in files:
            ext = os.path.splitext(f.filename or "")[1].lower()
            if ext != ".pdf":
                continue
            uid = uuid.uuid4().hex[:8]
            dest = os.path.join(upload_dir, f"{uid}_{f.filename}")
            with open(dest, "wb") as out:
                shutil.copyfileobj(f.file, out)
            pdf_paths.append(dest)

    log_queue = _get_log_queue(session_id)
    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break

    pipeline["done"] = False
    pipeline["error"] = None
    run_id = pipeline.get("run_id")
    if _celery_backend():
        from tasks import continue_after_fulltext_task
        continue_after_fulltext_task.apply_async(args=[str(output_dir), session_id, pdf_paths, run_id])
    else:
        threading.Thread(
            target=_upload_missing_fulltext_and_continue,
            args=(str(output_dir), session_id, pdf_paths, run_id),
            daemon=True,
        ).start()
    return {"ok": True, "run_id": run_id}


@app.get("/review_tracking")
def review_tracking(request: Request):
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    output_dir = _get_output_dir(session_id)
    path = output_dir / "paper_tracking.csv"
    if not path.exists():
        return {"ok": False, "error": "paper_tracking.csv is not ready yet."}

    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for row in reader:
            rows.append(row)

    run_row = _run_row_if_celery(pipeline)
    awaiting_review = (run_row["status"] == "awaiting_review") if run_row is not None \
        else pipeline.get("awaiting_review", False)
    return {
        "ok": True,
        "awaiting_review": awaiting_review,
        "filename": "paper_tracking.csv",
        "headers": headers,
        "rows": rows,
        "total_rows": len(rows),
    }


@app.post("/continue_pipeline")
def continue_pipeline(request: Request):
    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    log_queue = _get_log_queue(session_id)
    output_dir = _get_output_dir(session_id)
    row = _run_row_if_celery(pipeline)

    if row is not None:
        if row["status"] != "awaiting_review":
            return {"ok": False, "error": "There is no paused paper review to continue."}
    else:
        if pipeline["running"]:
            return {"ok": False, "error": "A pipeline is already running."}
        if not pipeline.get("awaiting_review") or not pipeline.get("pending_graph_state"):
            return {"ok": False, "error": "There is no paused paper review to continue."}

    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break

    pipeline["done"] = False
    pipeline["error"] = None
    run_id = pipeline.get("run_id")
    if _celery_backend():
        from tasks import continue_after_review_task
        continue_after_review_task.apply_async(args=[str(output_dir), session_id, run_id])
    else:
        threading.Thread(
            target=_continue_pipeline,
            args=(str(output_dir), session_id, run_id),
            daemon=True,
        ).start()
    return {"ok": True, "run_id": run_id}


class RunAnalysisRequest(BaseModel):
    prompt: str


@app.post("/run_analysis")
def run_analysis(req: RunAnalysisRequest, request: Request):
    """Run stages 5–9 (effect size → meta-analysis → moderators → bias → report)
    on the already-extracted meta_ready_results.json."""
    session_id = _get_session_id(request)
    pipeline   = _get_pipeline(session_id)
    log_queue  = _get_log_queue(session_id)
    output_dir = _get_output_dir(session_id)
    existing_row = _run_row_if_celery(pipeline)

    if pipeline["running"] or (existing_row and existing_row["status"] in ("queued", "running")):
        return {"ok": False, "error": "A pipeline is already running."}
    if not req.prompt.strip():
        return {"ok": False, "error": "Please enter the research question."}
    if _server_busy(session_id):
        return {"ok": False, "busy": True, "error": SERVER_BUSY_MSG}

    meta_ready_path = os.path.join(str(output_dir), "meta_ready_results.json")
    if not os.path.exists(meta_ready_path):
        return {
            "ok": False,
            "error": (
                "meta_ready_results.json not found. "
                "Run the full pipeline first to extract papers."
            ),
        }

    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break

    run_id = _new_run_id()
    pipeline["run_id"] = run_id
    pipeline["cancelled"] = False
    pipeline["done"]  = False
    pipeline["error"] = None
    pipeline["results"]          = None
    pipeline["current_stage_id"] = None
    pipeline["stage_logs"]       = {sid: [] for sid in AGENT_INFO}
    _run_store.create_run(
        run_id, req.prompt.strip(), str(output_dir),
        mode="downstream", source="dashboard", session_id=session_id,
        execution_backend=_config.RUN_EXECUTION_BACKEND,
    )

    if _celery_backend():
        from tasks import run_downstream_task
        run_downstream_task.apply_async(args=[req.prompt.strip(), str(output_dir), session_id, run_id])
    else:
        threading.Thread(
            target=_run_downstream,
            args=(req.prompt.strip(), str(output_dir), session_id, run_id),
            daemon=True,
        ).start()
    return {"ok": True, "run_id": run_id}


@app.post("/cancel")
def cancel_run(request: Request):
    """Cancel this visitor's own run. A running run stops at its next step
    (state "cancelling"); a run paused at a review step is discarded at once
    (state "cancelled")."""
    if _celery_backend():
        return {"ok": False, "error": "Cancelling is not available with the Celery backend."}
    state = run_service.request_cancel(_get_session_id(request))
    if state == "none":
        return {"ok": False, "error": "There is no run to cancel."}
    return {"ok": True, "state": state}


@app.get("/stream")
def stream(request: Request):
    session_id = _get_session_id(request)
    log_queue = _get_log_queue(session_id)

    def generate():
        yield 'data: {"level":"INFO","msg":"Connected — waiting for pipeline...","time":""}\n\n'
        while True:
            try:
                payload = log_queue.get(timeout=25)
                data = json.loads(payload)
                yield f"data: {payload}\n\n"
                if data.get("level") == "DONE":
                    break
            except queue.Empty:
                yield 'data: {"level":"PING","msg":"","time":""}\n\n'
    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache",
                                      "X-Accel-Buffering": "no",
                                      "Access-Control-Allow-Origin": "*"})


@app.get("/api/health")
def api_health():
    """Reports each optional infrastructure subsystem's status: "disabled"
    (its *_URL is empty -- the default, fully-supported deployment mode,
    identical to the app's behaviour before these subsystems existed), "ok"
    (configured AND a live check succeeded), or "error" (configured but the
    live check failed -- e.g. Postgres unreachable). Never raises regardless
    of subsystem state. Used by docker-compose's healthcheck and as an n8n
    preflight."""
    db_status = "disabled"
    if _config.DATABASE_URL:
        try:
            from persistence.db import verify_schema
            db_status = "ok" if verify_schema() else "error"
        except Exception:
            db_status = "error"

    redis_status = "configured" if _config.REDIS_URL else "disabled"
    broker_status = "configured" if _config.CELERY_BROKER_URL else "disabled"
    return {
        "ok": True,
        "version": _config.APP_VERSION or None,
        "role": _config.APP_ROLE,
        "backend": _config.RUN_EXECUTION_BACKEND,
        "db": db_status,
        "redis": redis_status,
        "broker": broker_status,
    }


@app.get("/status")
def status(request: Request):
    run_service.maybe_sweep_stale_runs()
    pipeline = _get_pipeline(_get_session_id(request))
    row = _run_row_if_celery(pipeline)
    if row is not None:
        # celery backend: execution happened in a separate OS process (a
        # worker) -- this API process's in-memory `pipeline` dict was never
        # touched by it, so Postgres is the only place live status can be
        # read from. See run_service.status_from_run_row()'s docstring.
        return run_service.status_from_run_row(row)
    # run_id/status are purely additive keys (see _derive_run_status) --
    # every key present before this session's infra work keeps its exact
    # existing meaning and type.
    return {"running": pipeline["running"], "done": pipeline["done"],
            "error": pipeline["error"],
            "awaiting_review": pipeline.get("awaiting_review", False),
            "awaiting_paper_selection": pipeline.get("awaiting_paper_selection", False),
            "awaiting_fulltext_upload": pipeline.get("awaiting_fulltext_upload", False),
            "cancelled": pipeline.get("cancelled", False),
            "run_id": pipeline.get("run_id"),
            "status": _derive_run_status(pipeline)}


@app.get("/results")
def results(request: Request):
    pipeline = _get_pipeline(_get_session_id(request))
    row = _run_row_if_celery(pipeline)
    if row is not None:
        return row.get("results_json") or {}
    return pipeline["results"] or {}


@app.get("/files")
def list_files(request: Request):
    files = []
    output_path = _get_output_dir(_get_session_id(request))
    if output_path.exists():
        for f in sorted(output_path.iterdir()):
            if f.is_file() and not f.name.startswith(".") and f.suffix in {".json", ".md", ".csv", ".png", ".pdf"}:
                st = f.stat()
                files.append({
                    "name":     f.name,
                    "size":     st.st_size,
                    "modified": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
                    "type":     f.suffix.lstrip("."),
                })
    return files


@app.get("/outputs/{filename}")
def serve_output(filename: str, request: Request):
    path = _get_output_dir(_get_session_id(request)) / filename
    if path.exists() and path.suffix in {".png", ".md", ".json", ".csv", ".pdf"}:
        return FileResponse(str(path), headers={"Cache-Control": "no-store"})
    raise HTTPException(status_code=404, detail="File not found")


# ── Agent detail page ──────────────────────────────────────────────────────────

def _fmt_size(n: int) -> str:
    if n < 1024:        return f"{n} B"
    if n < 1024**2:     return f"{n/1024:.1f} KB"
    return f"{n/1024**2:.1f} MB"


def _render_agent_page(stage_id: str, request: Request) -> str:
    info = AGENT_INFO.get(stage_id)
    if not info:
        return "<h1>Agent not found</h1>"

    session_id = _get_session_id(request)
    pipeline = _get_pipeline(session_id)
    # Manual-upload runs skip the Search Agent -- stage 1 is Manual Ingest
    # instead (both log under "STAGE 1" so they share the s1 slot; see
    # STAGE_PATTERNS above). Swap the label/description so this page doesn't
    # claim a database search happened when it didn't.
    if stage_id == "s1" and pipeline.get("mode") == "manual":
        info = MANUAL_INGEST_INFO
    logs    = pipeline["stage_logs"].get(stage_id, [])
    results = pipeline["results"] or {}

    # ── Output files for this stage
    out_path = _get_output_dir(session_id)
    file_rows = ""
    known_files = list(info["output_files"])
    if stage_id == "s7":
        for p in sorted(out_path.glob("*.png")):
            if p.name.startswith(("violin_", "moderator_")):
                known_files.append(p.name)

    for fname in known_files:
        p = out_path / fname
        ext = Path(fname).suffix.lstrip(".")
        icons = {"json": "📄", "md": "📝", "csv": "📋", "png": "🖼", "pdf": "📕"}
        icon = icons.get(ext, "📄")
        if p.exists():
            size = _fmt_size(p.stat().st_size)
            preview = ""
            if ext == "png":
                ts = int(p.stat().st_mtime * 1000)
                preview = f'<img src="/outputs/{fname}?t={ts}" style="width:100%;border-radius:6px;margin-top:10px;background:#fff">'
            file_rows += f"""
            <div class="frow">
              <span class="ficon">{icon}</span>
              <div class="fmeta"><div class="fname">{fname}</div><div class="fsize">{size}</div></div>
              <a class="dbtn" href="/outputs/{fname}" download>Download</a>
            </div>{preview}"""
        else:
            file_rows += f"""
            <div class="frow fmissing">
              <span class="ficon">{icon}</span>
              <div class="fmeta"><div class="fname">{fname}</div><div class="fsize">not yet generated</div></div>
            </div>"""

    files_section = file_rows if file_rows else "<p style='color:#64748b'>No output files for this stage.</p>"

    # ── Stats cards
    stat_map = {
        "research_question": ("Research Question", None),
        "treatment":         ("Treatment",         None),
        "control":           ("Control",           None),
        "n_retrieved":       ("Papers Retrieved",  None),
        "n_screened":        ("Papers Screened in", None),
        "n_eligible":        ("Papers Eligible",   None),
        "n_studies":         ("Studies Included",  None),
        "n_effects":         ("Effect Sizes",      None),
        "pooled_g":          ("Pooled Hedges' g",  lambda v, r: f"95% CI [{r.get('ci_lower')}, {r.get('ci_upper')}]  p = {r.get('p_value')}"),
        "i_squared":         ("I²",                lambda v, r: "Between-study heterogeneity"),
        "tau":               ("τ",                 lambda v, r: "Between-study SD"),
        "k":                 ("Studies (k)",       None),
        "bias_risk":         ("Bias Risk",         lambda v, r: f"Egger's p = {r.get('eggers_p')}  k₀ = {r.get('trim_fill_k0')}"
                                                                 + (f"  Begg's p = {r.get('rank_test_p')}" if r.get('rank_test_p') is not None else "")
                                                                 + (f"  PET-PEESE = {r.get('pet_peese_estimate')}" if r.get('pet_peese_estimate') is not None else "")),
        "eggers_p":          ("Egger's p",         None),
        "trim_fill_k0":      ("k₀ (trim-fill)",    None),
    }
    stat_cards = ""
    for key in info["stats_keys"]:
        if key in results:
            val = results[key]
            label, sub_fn = stat_map.get(key, (key, None))
            sub = sub_fn(val, results) if sub_fn else ""
            if key == "pooled_g":
                # measure_label/native_pooling_used come from the pipeline's
                # own effect-measure resolution -- never hardcode "Hedges' g"
                # here, this group may have been pooled on RR/OR/MD instead.
                if results.get("measure_label"):
                    label = f"Pooled {results['measure_label']}"
                if results.get("native_pooling_used") is False:
                    warn = "Note: effect measure not confirmed, standardized fallback shown"
                    sub = f"{sub} — {warn}" if sub else warn
            if key == "bias_risk":
                val = str(val).upper()
            stat_cards += f"""<div class="scard">
              <div class="slabel">{label}</div>
              <div class="sval">{val}</div>
              {'<div class="ssub">' + sub + '</div>' if sub else ''}
            </div>"""

    # ── Log lines
    log_html = ""
    if logs:
        for entry in logs:
            lvl   = entry["level"]
            cls   = {"WARNING": "log-W", "ERROR": "log-E", "INFO": "log-I"}.get(lvl, "log-I")
            is_stage = entry["msg"].startswith("===") and entry["msg"].endswith("===")
            if is_stage:
                cls = "log-S"
            log_html += (
                f'<div class="ll">'
                f'<span class="lt">{entry["time"]}</span>'
                f'<span class="{cls}">{entry["msg"]}</span>'
                f'</div>'
            )
    else:
        log_html = '<div class="ll"><span class="log-I">No log lines captured for this stage yet.</span></div>'

    color = info["color"]
    title = info["title"]
    num   = info["num"]
    emoji = info["emoji"]
    role  = info["role"]
    desc  = info["description"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} — AutoSynthesis</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#d9dfe6;--panel:#edf0f4;--border:#aeb8c4;--text:#16202b;--muted:#46535f;--radius:3px}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}}
header{{background:#1b2a3a;border-bottom:3px solid #2b7348;padding:12px 32px;display:flex;align-items:center;gap:14px}}
.back{{color:#dbe4ee;text-decoration:none;font-size:.85rem;opacity:.9;border:1px solid #4a5b6d;padding:5px 12px;border-radius:6px;transition:opacity .2s}}
.back:hover{{opacity:1}}
h1{{font-size:1.2rem;font-weight:600;margin-left:8px;color:#fff}}
.badge{{background:{color};color:#fff;border-radius:6px;padding:3px 10px;font-size:.75rem;font-weight:700}}
.content{{max-width:1000px;margin:0 auto;padding:32px 24px;display:flex;flex-direction:column;gap:24px}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:22px 24px}}
.card h2{{font-size:.95rem;font-weight:700;margin-bottom:12px;color:var(--text);display:flex;align-items:center;gap:8px}}
.card h2 .dot{{width:8px;height:8px;border-radius:50%;background:{color}}}
.role{{font-size:.9rem;color:#334155;line-height:1.6;margin-bottom:12px}}
.desc{{font-size:.85rem;color:var(--muted);line-height:1.8}}
.desc code{{background:#c9d1da;border-radius:4px;padding:1px 5px;font-family:monospace;font-size:.82rem;color:#0369a1}}
.stat-row{{display:flex;flex-wrap:wrap;gap:12px}}
.scard{{background:#e4e8ed;border:1px solid var(--border);border-radius:3px;padding:14px 18px;min-width:140px}}
.slabel{{font-size:.68rem;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:4px}}
.sval{{font-size:1.3rem;font-weight:700;color:{color}}}
.ssub{{font-size:.7rem;color:var(--muted);margin-top:3px}}
/* log */
.logbox{{background:#e4e8ed;border-radius:3px;padding:14px 16px;font-family:'Consolas','Monaco',monospace;font-size:.78rem;line-height:1.7;max-height:420px;overflow-y:auto}}
.ll{{display:flex;gap:10px}}
.lt{{color:#8a97a8;flex-shrink:0;min-width:60px}}
.log-I{{color:#475569}}.log-W{{color:#f59e0b}}.log-E{{color:#ef4444;font-weight:700}}.log-S{{color:#3b82f6;font-weight:700}}
.logbox::-webkit-scrollbar{{width:4px}}
.logbox::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
/* files */
.frow{{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border)}}
.frow:last-child{{border-bottom:none}}
.fmissing{{opacity:.45}}
.ficon{{font-size:1.4rem;flex-shrink:0}}
.fmeta{{flex:1}}
.fname{{font-size:.85rem;font-weight:500}}
.fsize{{font-size:.72rem;color:var(--muted);margin-top:1px}}
.dbtn{{background:#24496e;color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:.78rem;cursor:pointer;text-decoration:none;white-space:nowrap}}
.dbtn:hover{{background:#2563eb}}
/* glass theme (matches the main page) */
:root{{--bg:#435064;--panel:rgba(255,255,255,.14);--border:rgba(255,255,255,.24);--text:#fff;--muted:rgba(240,244,248,.78);--radius:20px}}
body{{background:radial-gradient(1100px 650px at 12% -8%,rgba(255,196,140,.34),transparent 60%),radial-gradient(900px 600px at 98% 6%,rgba(150,190,255,.30),transparent 60%),radial-gradient(1100px 800px at 55% 115%,rgba(120,190,170,.30),transparent 60%),linear-gradient(160deg,#56657a 0%,#435064 50%,#36414f 100%);background-attachment:fixed;font-family:"Inter","SF Pro Display","Segoe UI",system-ui,sans-serif}}
header{{background:rgba(255,255,255,.12);backdrop-filter:blur(22px) saturate(140%);-webkit-backdrop-filter:blur(22px) saturate(140%);border-bottom:1px solid var(--border)}}
.back{{border-radius:999px;background:rgba(255,255,255,.06);border:1px solid var(--border);color:#eef2f7}}
.card{{background:var(--panel);backdrop-filter:blur(22px) saturate(140%);-webkit-backdrop-filter:blur(22px) saturate(140%);border:1px solid var(--border);border-radius:var(--radius);box-shadow:0 12px 32px rgba(0,0,0,.22)}}
.role{{color:#e3e9f0}}
.desc code{{background:rgba(255,255,255,.08);color:#a9c8ff}}
.scard{{background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:14px}}
.sval{{font-weight:300;font-size:1.7rem}}
.logbox{{background:rgba(30,38,50,.30);border-radius:14px}}
.lt{{color:rgba(226,232,240,.32)}} .log-I{{color:rgba(226,232,240,.78)}}
.dbtn{{background:rgba(255,255,255,.08);border:1px solid var(--border);border-radius:999px}}
.dbtn:hover{{background:rgba(255,255,255,.16)}}
</style>
</head>
<body>
<header>
  <a class="back" href="javascript:window.close()">← Close</a>
  <span class="badge">{num}</span>
  <h1>{emoji} {title}</h1>
</header>
<div class="content">

  <div class="card">
    <h2><span class="dot"></span>What this agent does</h2>
    <div class="role">{role}</div>
    <div class="desc">{desc}</div>
  </div>

  {'<div class="card"><h2><span class="dot"></span>Key Results</h2><div class="stat-row">' + stat_cards + '</div></div>' if stat_cards else ''}

  <div class="card">
    <h2><span class="dot"></span>Pipeline Activity ({len(logs)} log lines)</h2>
    <div class="logbox">{log_html}</div>
  </div>

  <div class="card">
    <h2><span class="dot"></span>Output Files</h2>
    {files_section}
  </div>

</div>
</body>
</html>"""


@app.get("/agent/{stage_id}", response_class=HTMLResponse)
def agent_page(stage_id: str, request: Request):
    return _render_agent_page(stage_id, request)


# ── Main HTML ──────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AutoSynthesis</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:      #d9dfe6;
    --sidebar: #cbd3dc;
    --panel:   #edf0f4;
    --border:  #aeb8c4;
    --text:    #16202b;
    --muted:   #46535f;
    --blue:    #24496e;
    --green:   #2b7348;
    --orange:  #a85a05;
    --red:     #a92a22;
    --purple:  #5a4a86;
    --radius:  3px;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', system-ui, sans-serif;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  /* ── Header ── */
  header {
    background: #1b2a3a;
    border-bottom: 3px solid #2b7348;
    padding: 10px 32px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: sticky; top: 0; z-index: 10;
  }
  header h1 { font-size: 1.4rem; font-weight: 600; color: #ffffff; letter-spacing: .2px; }
  header span { font-size: 0.82rem; color: #b6c2cf; margin-top: 2px; }
  .header-left { display: flex; flex-direction: column; }
  .header-right { margin-left: auto; display: flex; align-items: center; gap: 18px; }
  .header-link { font-size: 0.85rem; font-weight: 600; color: #dbe4ee; text-decoration: none; }
  .header-link:hover { text-decoration: underline; }
  .header-logo { height: 42px; width: auto; display: block; background: #fff; padding: 3px 6px; border-radius: 2px; }

  /* ── Layout ── */
  .layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    flex: 1;
  }

  /* ── Sidebar ── */
  aside {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
    padding: 20px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    position: sticky;
    top: 73px;
    height: calc(100vh - 73px);
    overflow-y: auto;
  }
  aside h2 {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 8px;
    padding-left: 8px;
  }

  /* ── Stage item ── */
  .stage {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 10px;
    border-radius: var(--radius);
    border: 1px solid transparent;
    transition: background 0.25s, border-color 0.25s;
    cursor: default;
    position: relative;
  }
  .stage.active {
    background: rgba(36,73,110,0.12);
    border-color: rgba(36,73,110,0.4);
  }
  .stage.done-s {
    background: rgba(43,115,72,0.06);
    cursor: pointer;
  }
  .stage.done-s:hover {
    background: rgba(43,115,72,0.14);
    border-color: rgba(43,115,72,0.35);
  }
  .stage.error-s { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.3); }

  /* ── Pulsing icon ── */
  @keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0   rgba(36,73,110,0.6); }
    60%  { box-shadow: 0 0 0 6px rgba(36,73,110,0);   }
    100% { box-shadow: 0 0 0 0   rgba(36,73,110,0);   }
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .stage-icon {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700;
    flex-shrink: 0;
    background: var(--border);
    color: var(--muted);
    transition: background 0.3s, color 0.3s;
  }
  .stage.active  .stage-icon {
    background: var(--blue); color: #fff;
    animation: pulse-ring 1.4s ease-out infinite;
  }
  .stage.done-s  .stage-icon { background: var(--green);  color: #fff; }
  .stage.error-s .stage-icon { background: var(--red);    color: #fff; }

  /* Live spinner inside active icon */
  .stage.active .stage-icon::after {
    content: "";
    position: absolute;
    width: 10px; height: 10px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    pointer-events: none;
  }

  .stage-info { flex: 1; min-width: 0; }
  .stage-label {
    font-size: 0.8rem; font-weight: 600;
    color: var(--muted);
    transition: color 0.2s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .stage.active  .stage-label { color: var(--blue); }
  .stage.done-s  .stage-label { color: var(--green); }
  .stage.error-s .stage-label { color: var(--red); }

  .stage-sub {
    font-size: 0.68rem; color: var(--muted);
    opacity: 0.6; margin-top: 1px;
  }

  /* click hint on done stages */
  .stage.done-s .stage-label::after {
    content: "";
  }

  /* ── Main ── */
  main {
    display: flex; flex-direction: column;
    padding: 24px; gap: 20px;    min-width: 0;   /* let wide tables scroll inside their own box instead of widening the page */
  }

  /* ── Input card ── */
  .input-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
  }
  .input-card label {
    display: block; font-size: 0.78rem;
    color: var(--muted); margin-bottom: 8px;
    text-transform: uppercase; letter-spacing: 0.5px;
  }
  .input-row { display: flex; gap: 10px; }
  .paper-card {
    background: var(--panel);
    border: 1px solid var(--border); border-left: 4px solid var(--blue);
    border-radius: var(--radius); padding: 18px 24px;
  }
  .paper-kicker { font-size: 0.72rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--blue); }
  .paper-title { font-family: Georgia, "Times New Roman", serif; font-size: 1.3rem; font-weight: 700; margin: 4px 0 6px; color: var(--text); }
  .paper-sub { font-size: 0.88rem; color: var(--muted); line-height: 1.55; max-width: 760px; margin-bottom: 12px; }
  .paper-btn { display: inline-block; text-decoration: none; padding: 8px 18px; }
  .paper-soon { font-size: 0.82rem; color: var(--muted); }
  .demo-banner { display: none; background: #ecdcc3; border: 1px solid #c9a96b; color: #5c3b0a;
    border-radius: 3px; padding: 9px 14px; font-size: 0.84rem; }
  footer.site-footer { text-align: center; padding: 18px; font-size: 0.8rem; color: var(--muted);
    border-top: 1px solid var(--border); background: var(--sidebar); }
  footer.site-footer a { color: var(--blue); text-decoration: none; margin: 0 8px; }
  #prompt {
    flex: 1;
    background: #f7f9fb;
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--text);
    padding: 11px 14px;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
  }
  #prompt:focus { border-color: var(--blue); }
  #prompt::placeholder { color: var(--muted); }
  #reviewId {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--text);
    padding: 7px 10px;
    font-size: 0.85rem;
    outline: none;
    width: 100%;
    transition: border-color 0.2s;
  }
  #reviewId:focus { border-color: var(--blue); }
  #reviewId::placeholder { color: var(--muted); }

  .btn {
    padding: 11px 22px; border-radius: 3px;
    font-size: 0.9rem; font-weight: 600;
    cursor: pointer; border: none;
    transition: opacity 0.2s, transform 0.1s;
  }
  .btn:active { transform: scale(0.97); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .btn-primary   { background: var(--blue);  color: #fff; }
  .btn-secondary { background: var(--card); color: var(--text); border: 1px solid var(--border); }
  .btn-secondary:hover { border-color: var(--accent); }
  .btn-danger    { background: var(--red);   color: #fff; }

  .mode-btn {
    padding: 5px 14px; border-radius: 3px;
    font-size: 0.78rem; font-weight: 600; cursor: pointer;
    border: 1px solid var(--border);
    background: transparent; color: var(--muted);
    transition: all 0.15s;
  }
  .mode-btn:hover { border-color: var(--blue); color: var(--blue); }
  .mode-btn.mode-active {
    background: rgba(36,73,110,0.15);
    border-color: rgba(36,73,110,0.5);
    color: var(--blue);
  }

  /* ── Status bar ── */
  #status-bar { display: none; align-items: center; gap: 10px; margin-top: 12px; font-size: 0.82rem; color: var(--muted); }
  #status-bar.visible { display: flex; }
  .spinner { width: 14px; height: 14px; border: 2px solid var(--border); border-top-color: var(--blue); border-radius: 50%; animation: spin 0.8s linear infinite; }
  #status-text { flex: 1; }
  #elapsed { color: var(--muted); font-family: monospace; }

  /* ── Log console ── */
  .console-card {
    background: #e4e8ed; border: 1px solid var(--border);
    border-radius: var(--radius);
    display: flex; flex-direction: column;
    min-height: 320px; max-height: 430px; overflow: hidden;
  }
  .console-header {
    padding: 10px 16px; background: #c5ced8;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 8px;
    font-size: 0.78rem; color: var(--muted);
  }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-r { background: #ef4444; } .dot-y { background: #f59e0b; } .dot-g { background: #22c55e; }
  #log {
    flex: 1; overflow-y: auto;
    padding: 12px 16px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.78rem; line-height: 1.7;
  }
  .log-line { display: flex; gap: 10px; }
  .log-time    { color: #8a97a8; flex-shrink: 0; min-width: 60px; }
  .log-INFO    { color: #475569; }
  .log-WARNING { color: var(--orange); }
  .log-ERROR   { color: var(--red); font-weight: 700; }
  .log-SUCCESS { color: var(--green); font-weight: 700; }
  .log-stage   { color: var(--blue); font-weight: 700; }
  #log::-webkit-scrollbar { width: 4px; }
  #log::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  /* ── Results ── */
  #results-panel { display: none; flex-direction: column; gap: 18px; }
  #results-panel.visible { display: flex; }

  .section-title {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.8px;
    color: var(--muted); margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
  }
  .section-title::after {
    content: ""; flex: 1; height: 1px; background: var(--border);
  }

  .results-header {
    font-size: 1.1rem; font-weight: 700;
    color: var(--green); display: flex; align-items: center; gap: 8px;
  }

  /* Statistics-engine confirmation badge -- verifiable proof (not just a
     trust-me label) that this run's numbers came from R's metafor package,
     via the R/metafor version string captured at the moment metafor
     actually computed the pooled estimate. */
  .engine-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(43,115,72,0.1); border: 1px solid rgba(43,115,72,0.35);
    color: var(--green); border-radius: 3px;
    padding: 6px 14px; font-size: 0.78rem; font-weight: 600;
  }
  .engine-badge .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green); flex-shrink: 0;
  }

  /* PRISMA */
  .prisma {
    display: flex; align-items: center; flex-wrap: wrap;
    background: var(--panel); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 14px 20px; gap: 4px;
  }
  .prisma { flex-direction: column; align-items: stretch; gap: 8px; padding: 16px 20px; }
  .pf-head, .pf-row { display: grid; grid-template-columns: minmax(150px, 240px) minmax(120px, 1fr) minmax(180px, 320px); gap: 14px; }
  .pf-head { font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.6px; color: var(--muted);
             padding-bottom: 6px; border-bottom: 1px solid var(--border); }
  .pf-row { align-items: start; padding: 6px 0; border-bottom: 1px solid rgba(148,163,184,0.12); }
  .pf-row:last-of-type { border-bottom: none; }
  .pf-lbl { font-size: 0.8rem; color: var(--text); line-height: 1.35; }
  .pf-note { display: block; color: var(--green); font-size: 0.74rem; margin-top: 2px; }
  .pf-track { height: 24px; background: rgba(148,163,184,0.14); border-radius: 6px; overflow: hidden; }
  .pf-fill { height: 100%; min-width: 38px; background: var(--blue); border-radius: 6px;
             display: flex; align-items: center; justify-content: flex-end; padding-right: 8px;
             color: #fff; font-size: 0.8rem; font-weight: 700; box-sizing: border-box; }
  .pf-effects .pf-fill { background: var(--green); }
  .pf-side { font-size: 0.74rem; color: var(--muted); }
  .pf-side-h { font-weight: 600; }
  .pf-out .pf-side-h { color: var(--orange); }
  .pf-in .pf-side-h { color: var(--green); }
  .pf-row ul { list-style: none; margin: 4px 0 0; padding: 0; }
  .pf-row li { display: flex; justify-content: space-between; gap: 10px; font-size: 0.72rem; color: var(--muted); padding: 1px 0; }
  .pf-row li b { color: var(--text); font-weight: 600; }
  .pf-row li.pf-all { display: block; }
  .pf-row details summary { cursor: pointer; color: var(--blue); font-size: 0.72rem; }
  .pf-row details ul { margin-top: 2px; }
  .pf-more { margin-top: 6px; }
  @media (max-width: 640px) {
    .pf-head { display: none; }
    .pf-row { grid-template-columns: 1fr; gap: 4px; }
    .pf-side:empty { display: none; }
  }

  /* Copy-ready results table */
  .results-table-wrap { overflow-x: auto; }
  .results-table { border-collapse: collapse; width: 100%; font-size: 0.85rem; background: var(--panel); }
  .results-table th, .results-table td {
    border: 1px solid var(--border); padding: 8px 12px; text-align: left; white-space: nowrap;
  }
  .results-table th { color: var(--muted); font-weight: 600; background: rgba(148,163,184,0.08); }
  .results-table-bar { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
  .results-table-hint { font-size: 0.72rem; color: var(--muted); }

  /* Stat cards */
  .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
  .stat-card {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 14px 16px;
  }
  .stat-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 4px; }
  .stat-value { font-size: 1.3rem; font-weight: 700; color: var(--text); line-height: 1; }
  .stat-sub   { font-size: 0.7rem; color: var(--muted); margin-top: 3px; }
  .stat-card.highlight { border-color: var(--blue); }
  .stat-card.highlight .stat-value { color: var(--blue); }
  .stat-card.risk-low      { border-color: var(--green); }
  .stat-card.risk-low      .stat-value { color: var(--green); }
  .stat-card.risk-moderate { border-color: var(--orange); }
  .stat-card.risk-moderate .stat-value { color: var(--orange); }
  .stat-card.risk-high     { border-color: var(--red); }
  .stat-card.risk-high     .stat-value { color: var(--red); }

  #group-select {
    background: var(--panel); color: var(--text); border: 1px solid var(--border);
    border-radius: 3px; padding: 6px 10px; font-size: 13px; font-family: inherit;
  }

  /* Plots */
  .plots-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
  .plot-card  { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
  .plot-card img { width: 100%; display: block; background: #fff; }
  .plot-card img { cursor: zoom-in; }
  .plot-foot { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 8px 12px; border-top: 1px solid var(--border); }
  .plot-title { font-size: 0.78rem; color: var(--muted); flex: 1; }
  .plot-actions { display: flex; gap: 6px; }
  .pbtn { background: rgba(255,255,255,0.08); color: var(--text); border: 1px solid var(--border); border-radius: 999px;
          padding: 3px 10px; font-size: 0.72rem; cursor: pointer; text-decoration: none; font-family: inherit; }
  .pbtn:hover { background: rgba(255,255,255,0.18); }
  .plot-tabs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 6px; }
  .plot-tab { background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: 999px;
              padding: 6px 14px; font-size: 0.8rem; cursor: pointer; font-family: inherit; }
  .plot-tab:hover { color: var(--text); }
  .plot-tab.active { background: var(--blue); border-color: var(--blue); color: #fff; }
  .plot-tab-desc { font-size: 0.78rem; color: var(--muted); margin: 0 0 10px; }
  .privacy-note { font-size: 0.74rem; color: var(--muted); margin: 8px 0 0; line-height: 1.45; }
  .privacy-note a { color: var(--blue); }
  .reports-intro { font-size: 0.8rem; color: var(--muted); margin: 0 0 10px; }
  .reports-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
  .report-card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius);
                 padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; }
  .report-card .dbtn { align-self: flex-start; margin-top: auto; }
  .report-name { font-weight: 600; font-size: 0.86rem; color: var(--text); }
  .report-desc { font-size: 0.76rem; color: var(--muted); line-height: 1.4; }
  .report-file { font-size: 0.72rem; color: var(--muted); font-family: ui-monospace, monospace; word-break: break-all; margin-top: auto; }
  .report-card .report-file + .dbtn { margin-top: 4px; }
  #lightbox.zoomed { overflow: auto; align-items: flex-start; justify-content: flex-start; }
  #lightbox.zoomed img { max-width: none; max-height: none; cursor: zoom-out; }

  /* ── Output Files card (collapsible) ── */
  .files-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
  }
  .files-card-header {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 18px;
    background: #c9d1da;
    cursor: pointer;
    user-select: none;
    font-size: 0.82rem; font-weight: 600; color: var(--text);
    transition: background 0.15s;
  }
  .files-card-header:hover { background: #bfc9d4; }
  .files-card-header .fch-title { flex: 1; display: flex; align-items: center; gap: 8px; }
  .chevron {
    font-size: 0.7rem; color: var(--muted);
    transition: transform 0.25s;
    display: inline-block;
  }
  .files-card.open .chevron { transform: rotate(90deg); }
  .files-card-header .fch-right { display: flex; align-items: center; gap: 8px; }
  .refresh-btn {
    background: rgba(36,73,110,0.12);
    border: 1px solid rgba(36,73,110,0.3);
    color: var(--blue);
    border-radius: 3px; padding: 4px 10px;
    font-size: 0.72rem; font-weight: 600;
    cursor: pointer; transition: background 0.15s;
  }
  .refresh-btn:hover { background: rgba(36,73,110,0.25); }
  .files-body {
    display: none;
    border-top: 1px solid var(--border);
  }
  .files-card.open .files-body { display: block; }
  .files-grid { display: flex; flex-direction: column; gap: 0; padding: 6px 10px; min-height: 54px; }
  .files-empty { color: var(--muted); font-size: 0.82rem; padding: 14px 8px; }
  .file-row {
    display: flex; align-items: center; gap: 12px;
    padding: 9px 10px; border-radius: 7px;
    transition: background 0.15s;
  }
  .file-row:hover { background: rgba(15,23,42,0.04); }
  .file-icon { font-size: 1.2rem; flex-shrink: 0; width: 26px; text-align: center; }
  .file-info { flex: 1; min-width: 0; }
  .file-name { font-size: 0.83rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .file-meta { font-size: 0.7rem; color: var(--muted); margin-top: 1px; }
  .file-actions { display: flex; gap: 6px; flex-shrink: 0; }
  .dbtn {
    background: rgba(36,73,110,0.15); color: var(--blue);
    border: 1px solid rgba(36,73,110,0.3);
    border-radius: 5px; padding: 4px 10px;
    font-size: 0.72rem; font-weight: 600;
    text-decoration: none; cursor: pointer;
    transition: background 0.15s;
  }
  .dbtn:hover { background: rgba(36,73,110,0.28); }
  .vbtn {
    background: rgba(43,115,72,0.12); color: var(--green);
    border: 1px solid rgba(43,115,72,0.3);
    border-radius: 5px; padding: 4px 10px;
    font-size: 0.72rem; font-weight: 600;
    cursor: pointer; transition: background 0.15s;
  }
  .vbtn:hover { background: rgba(43,115,72,0.25); }
  .file-type-badge {
    font-size: 0.6rem; font-weight: 700;
    padding: 2px 6px; border-radius: 4px;
    text-transform: uppercase; letter-spacing: 0.5px;
    flex-shrink: 0;
  }
  .ft-json { background: rgba(245,158,11,0.15); color: #b45309; border: 1px solid rgba(245,158,11,0.3); }
  .ft-md   { background: rgba(168,85,247,0.15); color: #7e22ce; border: 1px solid rgba(168,85,247,0.3); }
  .ft-csv  { background: rgba(43,115,72,0.12);  color: #15803d; border: 1px solid rgba(43,115,72,0.3); }
  .ft-png  { background: rgba(36,73,110,0.12); color: #1d4ed8; border: 1px solid rgba(36,73,110,0.3); }

  /* ── Image lightbox ── */
  #lightbox {
    display: none;
    position: fixed; inset: 0; z-index: 999;
    background: rgba(0,0,0,0.85);
    align-items: center; justify-content: center;
    flex-direction: column; gap: 14px;
    cursor: zoom-out;
  }
  #lightbox.open { display: flex; }
  #lightbox img {
    max-width: 92vw; max-height: 88vh;
    border-radius: 3px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.7);
    cursor: default;
  }
  #lightbox-caption {
    color: rgba(255,255,255,0.65); font-size: 0.82rem;
  }
  #lightbox-close {
    position: fixed; top: 18px; right: 24px;
    color: #fff; font-size: 1.6rem; cursor: pointer;
    opacity: 0.7; line-height: 1;
  }
  #lightbox-close:hover { opacity: 1; }
  .ft-pdf  { background: rgba(239,68,68,0.12);  color: #b91c1c; border: 1px solid rgba(239,68,68,0.3); }

  /* ── Paper review modal ── */
  #review-modal {
    display: none;
    position: fixed; inset: 0; z-index: 998;
    background: rgba(15,23,42,0.45);
    align-items: center; justify-content: center;
    padding: 24px;
  }
  #review-modal.open { display: flex; }
  .review-dialog {
    width: min(1120px, 96vw);
    max-height: 90vh;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: 0 24px 80px rgba(0,0,0,0.55);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .review-head {
    padding: 16px 18px;
    border-bottom: 1px solid var(--border);
    background: #c9d1da;
    display: flex; align-items: center; gap: 12px;
  }
  .review-head h2 { font-size: 1rem; flex: 1; }
  .review-count { font-size: 0.78rem; color: var(--muted); }
  .review-body { padding: 14px 18px; overflow: auto; }
  .review-note { color: var(--muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 12px; }
  .review-table-wrap {
    max-height: 54vh; overflow: auto;
    border: 1px solid var(--border); border-radius: 3px;
    background: #f4f6f8;
  }
  .review-table { width: 100%; border-collapse: collapse; font-size: 0.76rem; }
  .review-table th {
    position: sticky; top: 0; z-index: 1;
    background: #c9d1da; color: var(--text);
    text-align: left; padding: 8px 10px;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }
  .review-table td {
    padding: 8px 10px; border-bottom: 1px solid var(--border);
    color: #334155; vertical-align: top;
    max-width: 320px;
  }
  .review-table tr:last-child td { border-bottom: none; }
  .review-table td:first-child { min-width: 260px; color: var(--text); }
  .review-actions {
    padding: 14px 18px;
    border-top: 1px solid var(--border);
    display: flex; justify-content: flex-end; gap: 10px;
    background: #c9d1da;
  }

  /* ── Missing full-text upload modal (reuses .review-* styles above) ── */
  #fulltext-modal {
    display: none;
    position: fixed; inset: 0; z-index: 998;
    background: rgba(15,23,42,0.45);
    align-items: center; justify-content: center;
    padding: 24px;
  }
  #fulltext-modal.open { display: flex; }
  .fulltext-actions {
    padding: 14px 18px;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    background: #c9d1da;
  }

  /* ── Paper-selection modal (after the search agent; reuses .review-* styles) ── */
  #selection-modal {
    display: none;
    position: fixed; inset: 0; z-index: 998;
    background: rgba(15,23,42,0.45);
    align-items: center; justify-content: center;
    padding: 24px;
  }
  #selection-modal.open { display: flex; }
  .selection-tools {
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    margin-bottom: 10px; font-size: 0.78rem; color: var(--muted);
  }
  .selection-table td.sel-cell, .selection-table th.sel-cell { width: 34px; min-width: 34px; text-align: center; }
  .selection-table tr.declined td { opacity: 0.45; text-decoration: line-through; }
  .selection-table tr.declined td.sel-cell { opacity: 1; text-decoration: none; }
  .selection-table a { color: #2563eb; text-decoration: none; }
  .selection-table a:hover { text-decoration: underline; }
  .selection-add {
    margin-top: 12px; padding: 10px 12px;
    border: 1px dashed var(--border); border-radius: 3px;
    font-size: 0.8rem; color: var(--muted);
  }
  .selection-add-head { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
  .selection-file-list { list-style: none; margin: 6px 0 0; padding: 0; font-size: 0.78rem; color: #475569; }
  .selection-file-list li { display: flex; align-items: center; gap: 8px; padding: 2px 0; }
  .selection-file-list button {
    background: none; border: none; color: var(--red); cursor: pointer; font-size: 0.9rem;
  }

  /* ── Error panel ── */
  #error-panel {
    display: none; background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: var(--radius); padding: 16px 20px;
    color: var(--red); font-size: 0.85rem;
  }
  #error-panel.visible { display: block; }

  /* ══ Glass theme ═══════════════════════════════════════════════════════════
     Frosted translucent panels over a softly lit dark backdrop. Overrides the
     base rules above by order only; no element ids/classes changed. */
  :root {
    --bg: #10151c; --sidebar: transparent;
    --panel: rgba(255,255,255,0.14); --card: rgba(255,255,255,0.16);
    --border: rgba(255,255,255,0.24); --text: #ffffff; --muted: rgba(240,244,248,0.78);
    --blue: #a9c8ff; --green: #86d9a8; --orange: #f5c27a; --red: #ff8f85; --purple: #c8b5ff;
    --radius: 20px; --glass: blur(22px) saturate(140%);
  }
  body {
    background:
      radial-gradient(1100px 650px at 12% -8%, rgba(255,196,140,0.34), transparent 60%),
      radial-gradient(900px 600px at 98% 6%, rgba(150,190,255,0.30), transparent 60%),
      radial-gradient(1100px 800px at 55% 115%, rgba(120,190,170,0.30), transparent 60%),
      linear-gradient(160deg, #56657a 0%, #435064 50%, #36414f 100%);
    background-attachment: fixed;
    font-family: "Inter", "SF Pro Display", "Segoe UI", system-ui, sans-serif;
  }
  header {
    background: rgba(255,255,255,0.12); backdrop-filter: var(--glass); -webkit-backdrop-filter: var(--glass);
    border-bottom: 1px solid var(--border); box-shadow: none; padding: 12px 28px;
  }
  header h1 { color: #fff; font-weight: 600; letter-spacing: -0.2px; }
  header span { color: var(--muted); }
  header svg rect { fill: rgba(255,255,255,0.14); }
  .header-link { color: #eef2f7; padding: 7px 16px; border: 1px solid var(--border); border-radius: 999px;
    background: rgba(255,255,255,0.06); transition: background .2s; }
  .header-link:hover { background: rgba(255,255,255,0.14); text-decoration: none; }
  .header-logo { border-radius: 12px; height: 40px; padding: 4px 9px; }

  .layout { grid-template-columns: 260px 1fr; gap: 20px; padding: 20px; }
  aside {
    background: var(--panel); backdrop-filter: var(--glass); -webkit-backdrop-filter: var(--glass);
    border: 1px solid var(--border); border-radius: var(--radius);
    top: 88px; height: calc(100vh - 108px); padding: 18px 12px;
  }
  aside h2 { color: var(--muted); letter-spacing: 1.4px; }
  .stage { border-radius: 14px; padding: 9px 10px; }
  .stage:hover { background: rgba(255,255,255,0.05); }
  .stage-icon { background: rgba(255,255,255,0.09); color: var(--muted); border: 1px solid var(--border); }
  .stage-label { color: #e8edf3; }
  .stage-sub { color: var(--muted); opacity: 1; }
  .stage.active { background: rgba(255,255,255,0.13); border-color: rgba(255,255,255,0.28); }
  .stage.active .stage-icon { background: #fff; color: #11161d; border-color: #fff; }
  .stage.active .stage-label { color: #fff; }
  .stage.done-s { background: rgba(134,217,168,0.07); }
  .stage.done-s:hover { background: rgba(134,217,168,0.15); border-color: rgba(134,217,168,0.35); }
  .stage.done-s .stage-icon { background: rgba(134,217,168,0.92); color: #0e1a13; border-color: transparent; }
  .stage.done-s .stage-label { color: #d8f5e4; }

  main { padding: 0; gap: 20px; }
  .paper-card, .input-card, .console-card, .files-card, .prisma, .stat-card, .plot-card, .results-table-wrap {
    background: var(--panel); backdrop-filter: var(--glass); -webkit-backdrop-filter: var(--glass);
    border: 1px solid var(--border); border-radius: var(--radius);
    box-shadow: 0 10px 30px rgba(20,28,40,0.18);
  }
  .paper-card { padding: 28px 32px; border-left: 1px solid var(--border);
    background: linear-gradient(135deg, rgba(255,255,255,0.22), rgba(255,255,255,0.08)); }
  .paper-kicker { color: var(--orange); letter-spacing: 1.6px; }
  .paper-title { font-family: inherit; font-size: 1.65rem; font-weight: 600; color: #fff; letter-spacing: -0.3px; margin: 6px 0 8px; }
  .paper-sub { color: var(--muted); font-size: 0.92rem; }
  .paper-soon { color: var(--muted); }
  .input-card { padding: 22px 24px; }
  .input-card label { color: var(--muted); letter-spacing: 1.2px; }
  #prompt { background: rgba(255,255,255,0.12); border: 1px solid var(--border); border-radius: 14px;
    color: #fff; padding: 13px 16px; }
  #prompt::placeholder { color: rgba(226,232,240,0.42); }
  #prompt:focus { border-color: rgba(255,255,255,0.45); background: rgba(255,255,255,0.09); }
  #model-select { background: rgba(255,255,255,0.12) !important; border: 1px solid var(--border) !important;
    border-radius: 14px !important; color: #fff !important; padding: 0 14px !important; }
  #model-select option, #group-select option { color: #11161d; }
  .btn { border-radius: 999px; padding: 12px 24px; font-weight: 600; }
  .btn-primary { background: #f4f4f1; color: #11161d; }
  .btn-primary:hover { background: #ffffff; }
  .btn-secondary { background: rgba(255,255,255,0.08); color: #fff; border: 1px solid var(--border); }
  .btn-secondary:hover { background: rgba(255,255,255,0.15); border-color: rgba(255,255,255,0.32); }
  .mode-btn { border-radius: 999px; padding: 6px 16px; background: rgba(255,255,255,0.04);
    border: 1px solid var(--border); color: var(--muted); }
  .mode-btn:hover { color: #fff; border-color: rgba(255,255,255,0.35); }
  .mode-btn.mode-active { background: #f4f4f1; color: #11161d; border-color: #f4f4f1; }
  #status-bar { color: var(--muted); }
  .spinner { border-color: rgba(255,255,255,0.18); border-top-color: #fff; }

  .console-card { background: rgba(30,38,50,0.30); }
  .console-header { background: transparent; border-bottom: 1px solid var(--border); color: var(--muted); }
  .log-time { color: rgba(240,244,248,0.5); }
  .log-INFO { color: rgba(245,248,251,0.9); }
  .files-card-header { background: transparent; }
  .files-card-header:hover { background: rgba(255,255,255,0.04); }
  .file-row:hover { background: rgba(255,255,255,0.05); }
  .dbtn, .vbtn, .refresh-btn { border-radius: 999px; }
  .dbtn { background: rgba(255,255,255,0.08); color: #fff; border: 1px solid var(--border); }
  .dbtn:hover { background: rgba(255,255,255,0.16); }
  .vbtn { background: rgba(134,217,168,0.12); color: var(--green); border: 1px solid rgba(134,217,168,0.3); }
  .refresh-btn { background: rgba(255,255,255,0.08); color: #fff; border: 1px solid var(--border); }
  .refresh-btn:hover { background: rgba(255,255,255,0.16); }
  .file-type-badge { border-radius: 999px; }
  .ft-json { color: #f5c27a; } .ft-md { color: #c8b5ff; } .ft-csv { color: #86d9a8; }
  .ft-png  { color: #a9c8ff; } .ft-pdf { color: #ff8f85; }

  .section-title { color: var(--muted); letter-spacing: 1.4px; }
  .results-header { color: #fff; font-weight: 600; }
  .engine-badge { background: rgba(134,217,168,0.10); border: 1px solid rgba(134,217,168,0.3);
    color: var(--green); border-radius: 999px; }
  .prisma { padding: 20px 24px; }
  .prisma-n { font-size: 2rem; font-weight: 300; color: #fff; letter-spacing: -0.5px; }
  .prisma-lbl { color: var(--muted); }
  .prisma-arr { color: rgba(255,255,255,0.25); }
  .stat-grid { gap: 14px; }
  .stat-card { padding: 18px 20px; }
  .stat-label { color: var(--muted); letter-spacing: 1px; }
  .stat-value { font-size: clamp(1.25rem, 1.6vw, 2rem); font-weight: 300; color: #fff; letter-spacing: -0.5px;
    line-height: 1.15; overflow-wrap: anywhere; }
  .stat-sub { color: var(--muted); }
  .stat-card.highlight { border-color: rgba(169,200,255,0.45); }
  .stat-card.highlight .stat-value { color: #fff; }
  .stat-card.risk-low { border-color: rgba(134,217,168,0.45); }
  .stat-card.risk-moderate { border-color: rgba(245,194,122,0.5); }
  .stat-card.risk-high { border-color: rgba(255,143,133,0.5); }
  .results-table { background: transparent; color: var(--text); }
  .results-table th, .results-table td { border: 1px solid var(--border); }
  .results-table th { background: rgba(255,255,255,0.05); color: var(--muted); }
  .plot-card { overflow: hidden; padding: 10px; }
  .plot-card img { border-radius: 12px; }
  .plot-title { color: var(--muted); border-top: none; padding: 10px 6px 2px; }
  #group-select { background: rgba(255,255,255,0.12) !important; color: #fff !important;
    border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 8px 12px !important; }
  .demo-banner { background: rgba(245,194,122,0.12); border: 1px solid rgba(245,194,122,0.35);
    color: #f8dfbb; border-radius: 14px; padding: 11px 16px; }
  footer.site-footer { background: transparent; border-top: 1px solid var(--border); color: var(--muted); }

  #review-modal, #selection-modal, #fulltext-modal { background: rgba(5,8,12,0.55) !important;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
  .review-dialog { background: rgba(60,72,90,0.88); backdrop-filter: var(--glass); -webkit-backdrop-filter: var(--glass);
    border: 1px solid var(--border); border-radius: 22px; }
  .review-head { background: transparent; }
  .review-table-wrap { background: rgba(255,255,255,0.03); border-radius: 14px; }
  .review-table th { background: rgba(62,74,92,0.98); color: #fff; }
  .review-table td { color: rgba(226,232,240,0.86); }
  .selection-table a { color: var(--blue); }
  .selection-file-list { color: var(--muted); }

  /* First-visit welcome window */
  .welcome-overlay {
    position: fixed; inset: 0; z-index: 80; display: flex; align-items: center; justify-content: center;
    padding: 20px; background: rgba(20,28,40,0.45);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    opacity: 0; transition: opacity .3s ease;
  }
  .welcome-overlay.show { opacity: 1; }
  .welcome-card {
    width: min(620px, 100%); padding: 40px 44px 36px; border-radius: 28px;
    background: rgba(255,255,255,0.96); color: #16202b;
    box-shadow: 0 30px 80px rgba(10,16,24,0.35);
    transform: translateY(14px) scale(.98); transition: transform .35s ease;
  }
  .welcome-overlay.show .welcome-card { transform: none; }
  .welcome-kicker { font-size: 0.78rem; font-weight: 700; letter-spacing: 1.8px; text-transform: uppercase; color: #b7791f; }
  .welcome-card h2 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin: 6px 0 12px; }
  .welcome-card p { font-size: 1.02rem; line-height: 1.6; color: #3d4957; margin: 0 0 22px; }
  .welcome-points { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .welcome-card { position: relative; }
  .welcome-points > * { text-align: left; border-radius: 16px; padding: 18px 20px; }
  .welcome-points b, .welcome-points span, .welcome-points em, .welcome-points i { display: block; }
  .welcome-go {
    font: inherit; cursor: pointer; color: #fff; background: #16202b; border: 1px solid #16202b;
    box-shadow: 0 10px 26px rgba(10,16,24,0.25);
    transition: transform .15s, box-shadow .15s, background .15s;
    animation: welcomeShake 0.9s ease-in-out infinite, welcomeGlow 1.8s ease-in-out infinite;
  }
  .welcome-go:hover { background: #24313f; transform: translateY(-2px); box-shadow: 0 14px 32px rgba(10,16,24,0.32);
    animation: none; }
  .welcome-go:focus-visible { outline: 3px solid #f5c27a; outline-offset: 3px; }
  .welcome-points .welcome-go span { color: rgba(255,255,255,0.78); }
  .welcome-go em { font-style: normal; font-size: 0.7rem; font-weight: 700; letter-spacing: 1.4px;
    text-transform: uppercase; color: #f5c27a; margin-bottom: 4px; }
  .welcome-go i { font-style: normal; font-weight: 700; margin-top: 12px; }
  .btn-cancel { font: inherit; cursor: pointer; padding: 10px 18px; border-radius: 999px;
    background: transparent; color: #ffb4ab; border: 1px solid rgba(255,143,133,0.55); font-weight: 600;
    transition: background .15s, border-color .15s; }
  .btn-cancel:hover:not(:disabled) { background: rgba(255,143,133,0.14); border-color: #ff8f85; }
  .btn-cancel:disabled { opacity: .6; cursor: default; }
  .review-dialog .btn-cancel { color: #ffb4ab; }
  .demo-pick-list { display: grid; gap: 10px; }
  .demo-pick { font: inherit; cursor: pointer; text-align: left; position: relative;
    display: block; width: 100%; padding: 16px 48px 16px 20px; border-radius: 16px;
    background: #f3f5f8; border: 1px solid #dfe4ea; color: #16202b;
    transition: background .15s, border-color .15s, transform .15s, box-shadow .15s; }
  .demo-pick b { display: block; font-size: 1.05rem; }
  .demo-pick span { display: block; color: #5b6776; font-size: 0.9rem; margin-top: 2px; }
  .demo-pick i { position: absolute; right: 20px; top: 50%; transform: translateY(-50%);
    font-style: normal; font-weight: 700; color: #b7791f; font-size: 1.2rem; }
  .demo-pick:hover, .demo-pick:focus-visible { background: #16202b; border-color: #16202b; color: #fff;
    transform: translateY(-1px); box-shadow: 0 10px 24px rgba(10,16,24,0.22); outline: none; }
  .demo-pick:hover span, .demo-pick:focus-visible span { color: rgba(255,255,255,0.75); }
  .demo-pick:hover i, .demo-pick:focus-visible i { color: #f5c27a; }
  /* Only one dark item: while the mouse is over the list, the hovered item
     wins and a keyboard-focused item that is not hovered looks normal. */
  .demo-pick-list:hover .demo-pick:focus-visible:not(:hover) { background: #f3f5f8; border-color: #dfe4ea;
    color: #16202b; transform: none; box-shadow: none; }
  .demo-pick-list:hover .demo-pick:focus-visible:not(:hover) span { color: #5b6776; }
  .demo-pick-list:hover .demo-pick:focus-visible:not(:hover) i { color: #b7791f; }
  .welcome-info { background: #f1f4f7; border: 1px solid #e1e6ec; }
  .welcome-info b { color: #4b5866; }
  /* constant wiggle, no pause */
  @keyframes welcomeShake {
    0%, 100% { transform: translateX(0) rotate(0) scale(1.02); }
    25%      { transform: translateX(-6px) rotate(-2deg) scale(1.03); }
    50%      { transform: translateX(0) rotate(0) scale(1.02); }
    75%      { transform: translateX(6px) rotate(2deg) scale(1.03); }
  }
  @keyframes welcomeGlow {
    0%, 100% { box-shadow: 0 10px 26px rgba(10,16,24,0.25), 0 0 0 0 rgba(245,194,122,0.0); }
    50%      { box-shadow: 0 10px 26px rgba(10,16,24,0.25), 0 0 0 10px rgba(245,194,122,0.45); }
  }
  @media (prefers-reduced-motion: reduce) { .welcome-go { animation: welcomeGlow 1.8s ease-in-out infinite; } }
  .welcome-x {
    position: absolute; top: 16px; right: 18px; width: 36px; height: 36px; border-radius: 50%;
    border: none; background: transparent; color: #6b7785; font-size: 1.6rem; line-height: 1; cursor: pointer;
  }
  .welcome-x:hover { background: #eef1f4; color: #16202b; }
  .welcome-points b { display: block; font-size: 1.05rem; margin-bottom: 4px; }
  .welcome-points span { font-size: 0.92rem; color: #4b5866; line-height: 1.5; }
  .welcome-actions { display: flex; gap: 12px; flex-wrap: wrap; }
  .welcome-actions .btn { font-size: 1rem; padding: 14px 28px; }
  .welcome-actions .btn-primary { background: #16202b; color: #fff; }
  .welcome-actions .btn-primary:hover { background: #24313f; }
  .welcome-actions .btn-secondary { background: #fff; color: #16202b; border: 1px solid #cfd6de; }
  .welcome-actions .btn-secondary:hover { background: #f1f4f7; border-color: #b8c1cc; }
  @media (max-width: 560px) {
    .welcome-card { padding: 28px 22px 24px; }
    .welcome-card h2 { font-size: 1.55rem; }
    .welcome-points { grid-template-columns: 1fr; }
  }
  @keyframes demoPulse {
    0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.65); }
    70%  { box-shadow: 0 0 0 14px rgba(255,255,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
  }
  .demo-pulse { animation: demoPulse 1.8s ease-out infinite;
    background: rgba(255,255,255,0.26) !important; border-color: rgba(255,255,255,0.7) !important; }

</style>
</head>
<body>

<header>
  <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
    <rect width="36" height="36" rx="3" fill="#2b7348"/>
    <path d="M8 26 L12 14 L18 22 L22 10 L28 26" stroke="white" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle cx="28" cy="26" r="2.5" fill="white"/>
  </svg>
  <div class="header-left">
    <h1>AutoSynthesis</h1>
    <span>Automated Meta-Analysis System · Multi-Agent Pipeline</span>
  </div>
  <div class="header-right">
    <a class="header-link" id="hdr-paper" href="#" target="_blank" rel="noopener" style="display:none">Paper</a>
    <a class="header-link" href="/imprint">Imprint</a>
    <a class="header-link" href="/privacy">Privacy</a>
    <img class="header-logo" src="/assets/berd-nfdi-logo.png" alt="BERD@NFDI" onerror="this.style.display='none'">
  </div>
</header>

<div class="layout">

  <!-- ── Sidebar ── -->
  <aside>
    <h2>Pipeline Agents</h2>

    <div class="stage" id="s0" title="Planning Agent">
      <div class="stage-icon">0</div>
      <div class="stage-info">
        <div class="stage-label">Planning</div>
        <div class="stage-sub">Build analysis plan</div>
      </div>
    </div>
    <div class="stage" id="s1" title="Search Agent">
      <div class="stage-icon">1</div>
      <div class="stage-info">
        <div class="stage-label">Search</div>
        <div class="stage-sub">6 databases</div>
      </div>
    </div>
    <div class="stage" id="s2" title="Screening Agent">
      <div class="stage-icon">2</div>
      <div class="stage-info">
        <div class="stage-label">Screening</div>
        <div class="stage-sub">Title / abstract</div>
      </div>
    </div>
    <div class="stage" id="s3b" title="Full-Text Fetcher">
      <div class="stage-icon">↓</div>
      <div class="stage-info">
        <div class="stage-label">Full-Text Fetch</div>
        <div class="stage-sub">PDF + PMC download</div>
      </div>
    </div>
    <div class="stage" id="s3" title="Eligibility Agent">
      <div class="stage-icon">3</div>
      <div class="stage-info">
        <div class="stage-label">Eligibility</div>
        <div class="stage-sub">Strict inclusion</div>
      </div>
    </div>
    <div class="stage" id="s4" title="Data Extraction Agent">
      <div class="stage-icon">4</div>
      <div class="stage-info">
        <div class="stage-label">Data Extraction</div>
        <div class="stage-sub">Means, SDs, t/F</div>
      </div>
    </div>
    <div class="stage" id="s5" title="Effect Size Agent">
      <div class="stage-icon">5</div>
      <div class="stage-info">
        <div class="stage-label">Effect Sizes</div>
        <div class="stage-sub">Hedges' g</div>
      </div>
    </div>
    <div class="stage" id="s6" title="Meta-Analysis Agent">
      <div class="stage-icon">6</div>
      <div class="stage-info">
        <div class="stage-label">Meta-Analysis</div>
        <div class="stage-sub">metafor model</div>
      </div>
    </div>
    <div class="stage" id="s7" title="Moderator Agent">
      <div class="stage-icon">7</div>
      <div class="stage-info">
        <div class="stage-label">Moderators</div>
        <div class="stage-sub">Subgroup / regression</div>
      </div>
    </div>
    <div class="stage" id="s8" title="Bias Agent">
      <div class="stage-icon">8</div>
      <div class="stage-info">
        <div class="stage-label">Bias Assessment</div>
        <div class="stage-sub">Egger's + trim-fill</div>
      </div>
    </div>
    <div class="stage" id="s8b" title="Risk of Bias Agent">
      <div class="stage-icon">8b</div>
      <div class="stage-info">
        <div class="stage-label">Risk of Bias</div>
        <div class="stage-sub">RoB 2 / ROBINS-I</div>
      </div>
    </div>
    <div class="stage" id="s9" title="Report Agent">
      <div class="stage-icon">9</div>
      <div class="stage-info">
        <div class="stage-label">Report</div>
        <div class="stage-sub">Markdown + CSV</div>
      </div>
    </div>

    <div style="margin-top:auto;padding-top:16px;border-top:1px solid var(--border);font-size:0.65rem;color:var(--muted);padding-left:8px;line-height:1.6">
      After completion,<br>click any agent to<br>see its detail page.
    </div>
  </aside>

  <!-- ── Main ── -->
  <main>

    <div class="paper-card" id="paper-card">
      <div class="paper-kicker">Paper</div>
      <div class="paper-title" id="paper-title">AutoSynthesis: An agentic system for automated meta-analysis</div>
      <div class="paper-sub">A multi-agent system that automates the full meta-analysis workflow &mdash; literature search, screening,
        data extraction, statistics in R (metafor) and reporting.</div>
      <a class="btn btn-primary paper-btn" id="paper-btn" href="#" target="_blank" rel="noopener" style="display:none">Read the preprint on arXiv</a>
      <span class="paper-soon" id="paper-soon">Preprint link coming soon.</span>
    </div>

    <div class="input-card">
      <label>Research Question</label>
      <div class="input-row">
        <input id="prompt" type="text"
          placeholder="e.g. In adult smokers, what is the effect of an Internet-based cessation program, compared with no active control, on abstinence at 6 months or longer?"
          autocomplete="off" onkeydown="if(event.key==='Enter')startRun()"/>
        <select id="model-select" title="Model used by all agents" style="padding:0 10px;border-radius:3px;border:1px solid var(--border,#ccc);background:inherit;color:inherit;font:inherit"></select>
        <button id="demo-btn" class="btn btn-secondary" onclick="loadDemo()" style="display:none"
                title="Load a pre-computed example. No LLM is used, results appear instantly.">Demo</button>
        <button id="run-btn" class="btn btn-primary" onclick="startRun()">Run full pipeline</button>
        <button id="cancel-btn" class="btn btn-cancel" onclick="cancelRun()" style="display:none"
                title="Stop this run. It cannot be resumed afterwards.">Cancel run</button>
      </div>
      <p class="privacy-note">When you run an analysis, your question, any PDFs you upload and the results are
        stored for research and processed by external AI models. Please do not enter personal or confidential
        information. <a href="/privacy" target="_blank" rel="noopener">Privacy policy</a></p>

      <!-- Mode toggle -->
      <div style="display:flex;align-items:center;gap:10px;margin-top:14px;flex-wrap:wrap">
        <span style="font-size:0.78rem;color:var(--muted)">Paper source:</span>
        <button id="mode-auto" class="mode-btn mode-active">
          Automatic search
        </button>
        <button id="mode-pdf" class="mode-btn">
          Manual upload
        </button>
      </div>

      <!-- Pooling model (metafor) -->
      <div style="display:flex;align-items:center;gap:10px;margin-top:10px;flex-wrap:wrap">
        <label for="pooling-select" style="font-size:0.78rem;color:var(--muted);margin:0;text-transform:none;letter-spacing:0">Pooling model:</label>
        <select id="pooling-select" title="Meta-analytic model used to pool the studies (computed with R metafor)"
                style="padding:4px 10px;border-radius:3px;border:1px solid var(--border,#ccc);background:inherit;color:inherit;font:inherit;font-size:0.8rem">
          <option value="">Automatic (as asked in the question, else random effects REML)</option>
        </select>
      </div>

      <!-- PDF upload section (hidden unless manual mode) -->
      <div id="pdf-section" style="display:none;margin-top:12px">
        <label style="margin-bottom:8px">Upload PDF Files <span style="font-weight:400;text-transform:none;letter-spacing:0">(one or more .pdf files)</span></label>
        <div id="pdf-drop-zone"
          style="border:2px dashed var(--border);border-radius:10px;padding:24px 16px;text-align:center;cursor:pointer;transition:border-color .2s"
          onclick="document.getElementById('pdf-input').click()"
          ondragover="event.preventDefault();this.style.borderColor='var(--accent)'"
          ondragleave="this.style.borderColor='var(--border)'"
          ondrop="event.preventDefault();this.style.borderColor='var(--border)';handlePdfDrop(event.dataTransfer.files)">
          <input type="file" id="pdf-input" multiple accept=".pdf" style="display:none">
          
          <div style="font-size:0.85rem;color:var(--text)">Click to choose PDFs or drag &amp; drop here</div>
          <div style="font-size:0.72rem;color:var(--muted);margin-top:4px">.pdf files only</div>
        </div>
        <div id="pdf-file-list" style="margin-top:10px"></div>
        <div style="font-size:0.7rem;color:var(--muted);margin-top:6px">
          Stages 1–3 are skipped — text is extracted directly from your PDFs.
        </div>
      </div>

      <div id="status-bar">
        <div class="spinner"></div>
        <span id="status-text">Initialising...</span>
        <span id="elapsed">0s</span>
      </div>
    </div>

    <div id="error-panel"></div>

    <div id="review-modal">
      <div class="review-dialog">
        <div class="review-head">
          <h2>Review Eligible Papers</h2>
          <div id="review-count" class="review-count"></div>
        </div>
        <div class="review-body">
          <div class="review-note">
            The pipeline paused after eligibility. Review <code>paper_tracking.csv</code>;
            if the included papers look correct, continue to extraction and meta-analysis.
          </div>
          <div class="review-table-wrap">
            <table class="review-table">
              <thead id="review-table-head"></thead>
              <tbody id="review-table-body"></tbody>
            </table>
          </div>
        </div>
        <div class="review-actions">
          <a class="dbtn" id="review-download-link" href="/outputs/paper_tracking.csv" download>Download CSV</a>
          <button class="btn btn-cancel" onclick="cancelRun()">Cancel run</button>
          <button class="btn btn-primary" id="continue-btn" onclick="continueAfterReview()">Continue Pipeline</button>
        </div>
      </div>
    </div>

    <div id="selection-modal">
      <div class="review-dialog">
        <div class="review-head">
          <h2>Review Found Papers</h2>
          <div id="selection-count" class="review-count"></div>
        </div>
        <div class="review-body">
          <div class="review-note">
            The search agent found these papers. Untick any paper you do not want to enter the
            pipeline, and add your own PDFs alongside the found ones. Papers you add are read
            like any other paper; a PDF that matches a found paper is attached to it instead of
            being added twice.
          </div>
          <div class="selection-tools">
            <button class="dbtn" type="button" onclick="setAllPapers(true)">Select all</button>
            <button class="dbtn" type="button" onclick="setAllPapers(false)">Select none</button>
            <span id="selection-summary"></span>
          </div>
          <div class="review-table-wrap">
            <table class="review-table selection-table">
              <thead id="selection-table-head"></thead>
              <tbody id="selection-table-body"></tbody>
            </table>
          </div>
          <div class="selection-add">
            <div class="selection-add-head">
              <button class="dbtn" type="button" onclick="document.getElementById('selection-file-input').click()">Add PDF(s)</button>
              <span>Add further papers manually (PDF files).</span>
              <input type="file" id="selection-file-input" accept=".pdf" multiple
                     style="display:none" onchange="addSelectionFiles(this.files); this.value=''">
            </div>
            <ul class="selection-file-list" id="selection-file-list"></ul>
          </div>
        </div>
        <div class="fulltext-actions">
          <span id="selection-error" style="color:var(--red);font-size:0.78rem"></span>
          <button class="btn btn-cancel" onclick="cancelRun()">Cancel run</button>
          <button class="btn btn-primary" id="selection-continue-btn" onclick="submitPaperSelection()">Continue Pipeline</button>
        </div>
      </div>
    </div>

    <div id="fulltext-modal">
      <div class="review-dialog">
        <div class="review-head">
          <h2>Some Papers Could Not Be Retrieved</h2>
          <div id="fulltext-count" class="review-count"></div>
        </div>
        <div class="review-body">
          <div class="review-note">
            These papers looked relevant, but the pipeline could not access their full text
            automatically (paywalled, API limits, or no PDF found). You can upload the PDF(s)
            yourself and they will continue through eligibility and analysis exactly like any
            other paper, or continue without them.
          </div>
          <div class="review-table-wrap">
            <table class="review-table">
              <thead id="fulltext-table-head"></thead>
              <tbody id="fulltext-table-body"></tbody>
            </table>
          </div>
        </div>
        <div class="fulltext-actions">
          <button class="btn btn-cancel" onclick="cancelRun()">Cancel run</button>
          <button class="dbtn" id="fulltext-skip-btn" onclick="submitMissingFulltext([])">Continue Without Uploading</button>
          <button class="btn btn-primary" id="fulltext-upload-btn" onclick="triggerFulltextUpload()">Upload PDF(s)</button>
          <input type="file" id="fulltext-file-input" accept=".pdf" multiple
                 style="display:none" onchange="submitMissingFulltext(this.files)">
        </div>
      </div>
    </div>

    <!-- Lightbox for PNG preview -->
    <div id="lightbox" onclick="closeLightbox()">
      <span id="lightbox-close" onclick="closeLightbox()">✕</span>
      <img id="lightbox-img" src="" alt=""/>
      <div id="lightbox-caption"></div>
    </div>

    <!-- Results — shown after pipeline completes -->
    <div class="demo-banner" id="demo-banner"></div>
    <div id="results-panel">
      <div class="results-header">Analysis complete</div>

      <div>
        <div class="section-title">Study selection</div>
        <div class="prisma" id="prisma-flow"></div>
      </div>

      <div id="group-select-wrap" style="display:none; margin-bottom:10px;">
        <label for="group-select" style="font-size:13px; color:var(--muted); margin-right:8px;">Outcome:</label>
        <select id="group-select" onchange="selectGroup(this.value)"></select>
      </div>

      <div>
        <div class="section-title">Key Statistics</div>
        <div class="stat-grid" id="stat-grid"></div>
      </div>

      <div id="results-table-section" style="display:none">
        <div class="section-title">Results Table</div>
        <div class="results-table-wrap">
          <table class="results-table" id="results-table"></table>
        </div>
        <div class="results-table-bar">
          <button class="dbtn" type="button" onclick="copyResultsTable()">Copy for Excel</button>
          <span class="results-table-hint" id="results-table-hint">Copies the values only (no header row), tab-separated.</span>
        </div>
      </div>

      <div>
        <div class="section-title">Plots</div>
        <div class="plot-tabs" id="plot-tabs" role="tablist"></div>
        <p class="plot-tab-desc" id="plot-tab-desc"></p>
        <div class="plots-grid" id="plots-grid"></div>
      </div>

      <div id="reports-section" style="display:none">
        <div class="section-title">Detailed reports</div>
        <p class="reports-intro">The audit files behind the results above. They record how every paper was
          handled, so each number can be checked. CSV files open in Excel; JSON files in any text editor.</p>
        <div class="reports-grid" id="audit-csv-bar"></div>
      </div>
    </div>

    <!-- Log console -->
    <div class="console-card" id="console-card">
      <div class="console-header">
        <span style="margin-left:6px">Pipeline Log</span>
        <span id="log-count" style="margin-left:auto;opacity:0.5"></span>
      </div>
      <div id="log">
        <div class="log-line">
          <span class="log-INFO">Enter a research question above and click Run Analysis.</span>
        </div>
      </div>
    </div>

    <!-- Output Files — collapsible -->
    <div class="files-card" id="files-card">
      <div class="files-card-header" onclick="toggleFiles()">
        <div class="fch-title">
          <span class="chevron">▶</span>
          <span>Output files</span>
          <span id="files-count" style="color:var(--muted);font-size:0.72rem;font-weight:400"></span>
        </div>
        <div class="fch-right" onclick="event.stopPropagation()">
          <button class="refresh-btn" onclick="renderFiles()">Refresh</button>
        </div>
      </div>
      <div class="files-body">
        <div class="files-grid" id="files-grid">
          <span class="files-empty">No output files yet — run an analysis to generate results.</span>
        </div>
      </div>
    </div>


  </main>
</div>

<footer class="site-footer">
  <span>AutoSynthesis</span>
  <a href="/imprint">Imprint</a>
  <a href="/privacy">Privacy</a>
</footer>

<script>
// ── Stage map ─────────────────────────────────────────────────────────────────
const STAGE_MAP = {
  "STAGE 3b": "s3b",
  "STAGE 3A": "s4",
  "STAGE 4B": "s4",
  "STAGE 4C": "s4",
  "STAGE 0":  "s0",
  "STAGE 1":  "s1",
  "STAGE 2":  "s2",
  "STAGE 3":  "s3",
  "STAGE 4":  "s4",
  "STAGE 5":  "s5",
  "STAGE 6":  "s6",
  "STAGE 7":  "s7",
  "STAGE 8B": "s8b",
  "STAGE 8":  "s8",
  "STAGE 9":  "s9",
};
const STAGE_ORDER = ["s0","s1","s2","s3b","s3","s4","s5","s6","s7","s8","s8b","s9"];
let currentStageIdx = -1;
let es = null;
let startTime = null;
let timerInterval = null;
let logLineCount = 0;
let pipelineDone = false;

// ── Stage management ──────────────────────────────────────────────────────────

function resetStages() {
  STAGE_ORDER.forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove("active", "done-s", "error-s");
    el.querySelector(".stage-icon").textContent = id === "s3b" ? "↓" :
      id.replace("s","").replace("3b","↓");
    el.onclick = null;
    el.style.cursor = "default";
  });
  // fix icon numbers
  const icons = {"s0":"0","s1":"1","s2":"2","s3b":"↓","s3":"3","s4":"4","s5":"5","s6":"6","s7":"7","s8":"8","s8b":"8b","s9":"9"};
  STAGE_ORDER.forEach(id => {
    document.getElementById(id).querySelector(".stage-icon").textContent = icons[id];
  });
  currentStageIdx = -1;
  pipelineDone = false;
}

function activateStage(stageId) {
  const idx = STAGE_ORDER.indexOf(stageId);
  if (idx <= currentStageIdx) return;
  for (let i = Math.max(0, currentStageIdx); i < idx; i++) {
    finishStage(STAGE_ORDER[i]);
  }
  currentStageIdx = idx;
  const el = document.getElementById(stageId);
  el.classList.add("active");
  el.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function finishStage(stageId) {
  const el = document.getElementById(stageId);
  el.classList.remove("active");
  el.classList.add("done-s");
  el.querySelector(".stage-icon").textContent = "✓";
  el.style.cursor = "pointer";
  el.title = "Click to view agent details";
  el.onclick = () => window.open(`/agent/${stageId}`, "_blank");
}

function makeStagesClickable() {
  pipelineDone = true;
  // Finish any stage that was still active when the pipeline ended
  STAGE_ORDER.forEach(id => {
    const el = document.getElementById(id);
    if (el.classList.contains("active")) {
      finishStage(id);
    }
  });
}

function detectStage(msg) {
  // Longer/more-specific patterns first to avoid prefix collisions
  const orderedKeys = ["STAGE 3b","STAGE 3A","STAGE 4B","STAGE 4C",
                        "STAGE 0","STAGE 1","STAGE 2","STAGE 3",
                        "STAGE 4","STAGE 5","STAGE 6","STAGE 7","STAGE 8B","STAGE 8","STAGE 9"];
  for (const pattern of orderedKeys) {
    if (msg.includes(pattern)) {
      activateStage(STAGE_MAP[pattern]);
      return;
    }
  }
}

// ── Log ───────────────────────────────────────────────────────────────────────

function appendLog(time, msg, level) {
  const log = document.getElementById("log");
  const line = document.createElement("div");
  line.className = "log-line";
  const isStage = msg.startsWith("===") && msg.endsWith("===");
  const cls = isStage ? "log-stage" : `log-${level}`;
  line.innerHTML = time
    ? `<span class="log-time">${time}</span><span class="${cls}">${esc(msg)}</span>`
    : `<span class="${cls}">${esc(msg)}</span>`;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
  logLineCount++;
  document.getElementById("log-count").textContent = `${logLineCount} lines`;
}

function esc(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

// ── Timer ─────────────────────────────────────────────────────────────────────

function startTimer() {
  startTime = Date.now();
  timerInterval = setInterval(() => {
    const sec = Math.floor((Date.now() - startTime) / 1000);
    const m = Math.floor(sec/60), s = sec%60;
    document.getElementById("elapsed").textContent = m>0 ? `${m}m ${s}s` : `${s}s`;
  }, 1000);
}
function stopTimer() { if (timerInterval) { clearInterval(timerInterval); timerInterval = null; } }

// ── Mode toggle ───────────────────────────────────────────────────────────────

let currentMode = "auto";
let uploadedFiles = []; // [{name, path}] — server-confirmed uploads

function setMode(mode) {
  currentMode = mode;
  document.getElementById("mode-auto").classList.toggle("mode-active", mode === "auto");
  document.getElementById("mode-pdf").classList.toggle("mode-active", mode === "manual");
  document.getElementById("pdf-section").style.display = mode === "manual" ? "block" : "none";
  updateStage1Label(mode);
}

// Manual uploads skip the Search Agent (pipeline_graph.py routes
// manual_ingest_node -> study_detection_node, no database query happens) but
// its log lines still start with "STAGE 1", so they light up the same
// sidebar slot the Search Agent uses. Relabel that slot per mode so it never
// implies a database search ran during a manual-PDF run.
function updateStage1Label(mode) {
  const el = document.getElementById("s1");
  const label = el.querySelector(".stage-label");
  const sub = el.querySelector(".stage-sub");
  if (mode === "manual") {
    el.title = "Manual Ingest";
    label.textContent = "Manual Ingest";
    sub.textContent = "Extract from your PDFs";
  } else {
    el.title = "Search Agent";
    label.textContent = "Search";
    sub.textContent = "6 databases";
  }
}

// ── PDF upload helpers ─────────────────────────────────────────────────────────

async function handlePdfFiles(files) {
  if (!files || !files.length) return;
  const formData = new FormData();
  let added = 0;
  for (const f of files) {
    if (f.name.toLowerCase().endsWith(".pdf")) { formData.append("files", f); added++; }
  }
  if (!added) { alert("Please select .pdf files only."); return; }
  const resp = await fetch("/upload", {method: "POST", body: formData});
  const data = await resp.json();
  if (data.ok) {
    uploadedFiles = uploadedFiles.concat(data.files);
    renderPdfList();
  }
}

function handlePdfDrop(files) { handlePdfFiles(files); }

function renderPdfList() {
  const el = document.getElementById("pdf-file-list");
  if (!uploadedFiles.length) { el.innerHTML = ""; return; }
  el.innerHTML = uploadedFiles.map((f, i) =>
    `<div style="display:flex;align-items:center;gap:8px;padding:5px 8px;background:var(--bg);border:1px solid var(--border);border-radius:6px;margin-bottom:4px;font-size:0.8rem">
      <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${f.name}</span>
      <button onclick="removePdf(${i})" style="background:none;border:none;color:var(--muted);cursor:pointer;font-size:0.85rem;padding:0 2px" title="Remove">✕</button>
    </div>`
  ).join("");
}

function removePdf(i) {
  uploadedFiles.splice(i, 1);
  renderPdfList();
}

// ── Run ───────────────────────────────────────────────────────────────────────

async function loadModels() {
  try {
    const d = await (await fetch("/models")).json();
    const sel = document.getElementById("model-select");
    sel.innerHTML = d.models.map(m =>
      `<option value="${m.id}"${m.id === d.current ? " selected" : ""}>${m.label}</option>`).join("");
    if (d.models.length === 1) {            // deployment locked to one model: show it, nothing to choose
      sel.disabled = true;
      sel.title = "This server runs one model (the most cost-efficient one)";
    }
  } catch (e) {}
}
loadModels();

async function loadPoolingModels() {
  try {
    const d = await (await fetch("/models")).json();
    const sel = document.getElementById("pooling-select");
    if (!sel || !d.pooling_models) return;
    sel.innerHTML += d.pooling_models.map(m => `<option value="${m.id}">${m.label}</option>`).join("");
  } catch (e) {}
}
loadPoolingModels();

// ── Welcome window pointing at the Demo button (shown on every visit) ──
function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
function pulseDemo() {
  const btn = document.getElementById("demo-btn");
  if (!btn || btn.style.display === "none") return;
  btn.classList.remove("demo-pulse"); void btn.offsetWidth; btn.classList.add("demo-pulse");
  setTimeout(() => btn.classList.remove("demo-pulse"), 5600);
}
function showDemoHint() {
  // Shown on every visit to the start page (not only the first one).
  const btn = document.getElementById("demo-btn");
  if (!btn || btn.style.display === "none" || document.getElementById("demo-hint")) return;
  const ov = document.createElement("div");
  ov.id = "demo-hint"; ov.className = "welcome-overlay";
  ov.innerHTML = '<div class="welcome-card" role="dialog" aria-modal="true" aria-labelledby="welcome-title">'
    + '<button type="button" class="welcome-x" id="welcome-own" aria-label="Close">&times;</button>'
    + '<div class="welcome-kicker">Welcome</div>'
    + '<h2 id="welcome-title">AutoSynthesis</h2>'
    + '<p>AutoSynthesis runs a complete meta-analysis: literature search, screening, data extraction, '
    + 'statistics in R and a written report.</p>'
    + '<div class="welcome-points">'
    + '<button type="button" class="welcome-go" id="welcome-demo"><em>Recommended</em><b>Demo</b>'
    + '<span>Finished, real analyses. Open instantly, free.</span><i>Open the Demo &rarr;</i></button>'
    + '<div class="welcome-info"><b>Full run</b><span>About an hour per question and uses paid API credits.</span></div>'
    + '</div></div>';
  document.body.appendChild(ov);
  const close = (thenDemo) => {
    ov.classList.remove("show");
    setTimeout(() => ov.remove(), 300);
    document.removeEventListener("keydown", onKey);
    if (thenDemo) loadDemo(); else pulseDemo();
  };
  const onKey = (e) => { if (e.key === "Escape") close(false); };
  document.addEventListener("keydown", onKey);
  ov.querySelector("#welcome-demo").addEventListener("click", () => close(true));
  ov.querySelector("#welcome-own").addEventListener("click", () => close(false));
  requestAnimationFrame(() => ov.classList.add("show"));
  setTimeout(() => ov.querySelector("#welcome-demo").focus(), 350);
}

// ── "Server busy" window: only one analysis runs on the server at a time ──
async function serverBusy() {
  try { return (await (await fetch("/server_busy")).json()).busy === true; } catch (e) { return false; }
}
function showBusyPopup(msg) {
  if (document.getElementById("busy-popup")) return;
  const demoOk = (document.getElementById("demo-btn") || {}).style?.display !== "none";
  const ov = document.createElement("div");
  ov.id = "busy-popup"; ov.className = "welcome-overlay";
  ov.innerHTML = '<div class="welcome-card" role="dialog" aria-modal="true" aria-labelledby="busy-title">'
    + '<button type="button" class="welcome-x" id="busy-x" aria-label="Close">&times;</button>'
    + '<div class="welcome-kicker">Please wait</div>'
    + '<h2 id="busy-title">Another analysis is running</h2>'
    + '<p>' + (msg || "The server runs one analysis at a time. Please try again once it has finished.")
    + ' A full run takes about an hour.</p>'
    + (demoOk ? '<div class="welcome-points" style="grid-template-columns:1fr">'
      + '<button type="button" class="welcome-go" id="busy-demo"><em>Meanwhile</em><b>Open the Demo</b>'
      + '<span>See a finished, real analysis right away.</span><i>Open the Demo &rarr;</i></button></div>' : '')
    + '</div>';
  document.body.appendChild(ov);
  const close = (thenDemo) => {
    ov.classList.remove("show"); setTimeout(() => ov.remove(), 300);
    document.removeEventListener("keydown", onKey);
    if (thenDemo) loadDemo();
  };
  const onKey = (e) => { if (e.key === "Escape") close(false); };
  document.addEventListener("keydown", onKey);
  ov.querySelector("#busy-x").addEventListener("click", () => close(false));
  const d = ov.querySelector("#busy-demo"); if (d) d.addEventListener("click", () => close(true));
  requestAnimationFrame(() => ov.classList.add("show"));
}

async function loadSiteInfo() {
  try {
    const d = await (await fetch("/site_info")).json();
    document.getElementById("paper-title").textContent = d.paper_title;
    if (d.paper_url) {
      for (const id of ["paper-btn", "hdr-paper"]) {
        const a = document.getElementById(id);
        a.href = d.paper_url; a.style.display = "";
      }
      document.getElementById("paper-soon").style.display = "none";
    }
    if (d.demo_available) {
      DEMOS = d.demos || [];
      document.getElementById("demo-btn").style.display = "";
      setTimeout(showDemoHint, 700);
    }
  } catch (e) {}
}
loadSiteInfo();

// Demo: load a pre-computed real run (no LLM / search / R is used) and show it in the normal results view.
let DEMOS = [];
function escHtml(t) { const e = document.createElement("div"); e.textContent = t == null ? "" : String(t); return e.innerHTML; }
// Several examples installed: let the visitor pick one.
function showDemoPicker() {
  if (document.getElementById("demo-picker")) return;
  const ov = document.createElement("div");
  ov.id = "demo-picker"; ov.className = "welcome-overlay";
  ov.innerHTML = '<div class="welcome-card" role="dialog" aria-modal="true" aria-labelledby="picker-title">'
    + '<button type="button" class="welcome-x" id="picker-x" aria-label="Close">&times;</button>'
    + '<div class="welcome-kicker">Demo</div>'
    + '<h2 id="picker-title">Choose an example</h2>'
    + '<p>Finished, real analyses produced by AutoSynthesis. They open instantly and are free.</p>'
    + '<div class="demo-pick-list">'
    + DEMOS.map(d => '<button type="button" class="demo-pick" data-id="' + escHtml(d.id) + '"><b>'
        + escHtml(d.title) + '</b><span>' + escHtml(d.subtitle) + '</span><i>&rarr;</i></button>').join("")
    + '</div></div>';
  document.body.appendChild(ov);
  const close = () => {
    ov.classList.remove("show"); setTimeout(() => ov.remove(), 300);
    document.removeEventListener("keydown", onKey);
  };
  const onKey = (e) => { if (e.key === "Escape") close(); };
  document.addEventListener("keydown", onKey);
  ov.querySelector("#picker-x").addEventListener("click", close);
  ov.querySelectorAll(".demo-pick").forEach(b => b.addEventListener("click", () => { close(); loadDemo(b.dataset.id); }));
  requestAnimationFrame(() => ov.classList.add("show"));
  setTimeout(() => { const f = ov.querySelector(".demo-pick"); if (f) f.focus(); }, 350);
}

async function loadDemo(id) {
  if (!id && DEMOS.length > 1) { showDemoPicker(); return; }
  const btn = document.getElementById("demo-btn");
  btn.disabled = true;
  try {
    const data = await (await fetch("/demo/load", {method: "POST", headers: {"Content-Type": "application/json"},
                                                   body: JSON.stringify({id: id || ""})})).json();
    if (!data.ok) { showError(data.error); return; }
    document.getElementById("prompt").value = data.prompt || "";
    document.getElementById("error-panel").classList.remove("visible");
    document.getElementById("log").innerHTML = "";
    resetStages();
    STAGE_ORDER.forEach(id => { const el = document.getElementById(id); if (el) el.classList.add("done-s"); });
    makeStagesClickable();
    const banner = document.getElementById("demo-banner");
    banner.textContent = "Demo" + (data.title ? " – " + data.title : "") + ": "
      + (data.note || "pre-computed example, no LLM was used.");
    banner.style.display = "block";
    document.getElementById("console-card").style.display = "none";   // a demo has no pipeline log
    const res = await fetch("/results").then(r => r.json());
    renderResults(res);
    renderFiles();
    document.getElementById("status-text").textContent = "Demo loaded (pre-computed)";
    document.getElementById("results-panel").classList.add("visible");
    document.getElementById("results-panel").scrollIntoView({behavior: "smooth"});
  } finally {
    btn.disabled = false;
  }
}

async function startRun() {
  const prompt = document.getElementById("prompt").value.trim();
  if (!prompt) { document.getElementById("prompt").focus(); return; }
  if (await serverBusy()) { showBusyPopup(); return; }
  // Asked once per browser: a real run is slow and spends API credits -- point visitors to the Demo.
  if (!lsGet("as_run_confirmed")) {
    const ok = confirm("A full run searches the literature and analyses the papers. It takes about an hour "
      + "and uses paid API credits.\\n\\nTo see what AutoSynthesis produces, use the Demo button instead.\\n\\n"
      + "Start a full run anyway?");
    if (!ok) { pulseDemo(); return; }
    lsSet("as_run_confirmed", "1");
  }

  let paperFiles  = [];
  if (currentMode === "manual") {
    if (!uploadedFiles.length) {
      document.getElementById("pdf-input").click();
      return;
    }
    paperFiles = uploadedFiles.map(f => f.path);
  }

  document.getElementById("log").innerHTML = "";
  document.getElementById("demo-banner").style.display = "none";
  document.getElementById("results-panel").classList.remove("visible");
  document.getElementById("error-panel").classList.remove("visible");
  logLineCount = 0;
  document.getElementById("log-count").textContent = "";
  resetStages();

  lockUI();
  document.getElementById("status-text").textContent = "Starting pipeline...";
  startTimer();

  if (es) { es.close(); es = null; }

  const resp = await fetch("/run", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({prompt, paper_files: paperFiles, 
                           model: document.getElementById("model-select").value,
                           pooling_model: document.getElementById("pooling-select").value}),
  });
  const data = await resp.json();
  if (!data.ok && data.busy) { stopTimer(); unlockUI(); document.getElementById("status-text").textContent = "Ready"; showBusyPopup(data.error); return; }
  if (!data.ok) { showError(data.error); unlockUI(); return; }

  openPipelineStream();
}

function openPipelineStream() {
  if (es) { es.close(); es = null; }
  es = new EventSource("/stream");
  es.onmessage = evt => {
    const rec = JSON.parse(evt.data);
    if (rec.level === "PING") return;
    if (rec.level === "DONE") { es.close(); onDone(); return; }
    detectStage(rec.msg);
    appendLog(rec.time, rec.msg, rec.level);
    document.getElementById("status-text").textContent = rec.msg.substring(0, 90);
  };
  es.onerror = () => { appendLog("","Connection lost.","ERROR"); es.close(); unlockUI(); };
}

// ── Pipeline done ─────────────────────────────────────────────────────────────

// ── Cancel a run (running: stops at its next step; paused at a review step: discarded at once) ──
function showCancel(on) {
  const b = document.getElementById("cancel-btn");
  if (!b) return;
  b.style.display = on ? "" : "none";
  b.disabled = false;
  b.textContent = "Cancel run";
}
function finishCancelled() {
  stopTimer();
  ["review-modal", "selection-modal", "fulltext-modal"].forEach(id => {
    const m = document.getElementById(id); if (m) m.classList.remove("open");
  });
  STAGE_ORDER.forEach(id => { const el = document.getElementById(id); if (el) el.classList.remove("active"); });
  unlockUI();
  showCancel(false);
  document.querySelector(".spinner").style.display = "none";
  document.getElementById("status-text").textContent = "Run cancelled. You can start a new run or open the Demo.";
}
async function cancelRun() {
  if (!confirm("Cancel this run?\\n\\nIt stops at its next step and cannot be resumed. Results produced so far are not shown.")) return;
  document.querySelectorAll(".btn-cancel").forEach(b => { b.disabled = true; b.textContent = "Cancelling…"; });
  let d;
  try { d = await (await fetch("/cancel", {method: "POST"})).json(); } catch (e) { d = {ok: false, error: "Could not reach the server."}; }
  if (!d.ok) {
    document.querySelectorAll(".btn-cancel").forEach(b => { b.disabled = false; b.textContent = "Cancel run"; });
    showError(d.error); return;
  }
  if (d.state === "cancelling") {
    document.getElementById("status-text").textContent = "Cancelling… the run stops at its next step.";
    return;                       // the log stream ends with DONE -> onDone() -> finishCancelled()
  }
  appendLog(new Date().toTimeString().slice(0, 8), "Run cancelled by user.", "WARNING");
  finishCancelled();              // a paused run is discarded immediately
}

async function onDone() {
  stopTimer();
  const st = await fetch("/status").then(r => r.json());
  if (st.cancelled) { finishCancelled(); return; }
  if (st.error) {
    showCancel(false);
    showError(st.error);
    STAGE_ORDER.forEach(id => {
      const el = document.getElementById(id);
      if (el.classList.contains("active")) el.classList.add("error-s");
    });
    unlockUI();
    return;
  }
  if (st.awaiting_paper_selection) {
    await showSelectionModal();
    unlockUI();
    document.getElementById("run-btn").disabled = true;
    document.getElementById("prompt").disabled = true;
    document.getElementById("status-text").textContent = "Review the found papers, then continue.";
    return;
  }
  if (st.awaiting_fulltext_upload) {
    await showFulltextModal();
    unlockUI();
    document.getElementById("run-btn").disabled = true;
    document.getElementById("prompt").disabled = true;
    document.getElementById("status-text").textContent = "Some papers could not be retrieved — upload PDFs or continue.";
    return;
  }
  if (st.awaiting_review) {
    await showReviewModal();
    unlockUI();
    document.getElementById("run-btn").disabled = true;
    document.getElementById("prompt").disabled = true;
    document.getElementById("status-text").textContent = "Review paper_tracking.csv, then continue.";
    renderFiles();
    return;
  }
  showCancel(false);
  makeStagesClickable();
  const res = await fetch("/results").then(r => r.json());
  renderResults(res);
  renderFiles();   // refresh file list (panel stays closed until clicked)
  unlockUI();
  document.getElementById("status-text").textContent = "Pipeline complete";
  document.getElementById("results-panel").classList.add("visible");
  document.getElementById("results-panel").scrollIntoView({behavior:"smooth"});
}

// ── Paper review gate ────────────────────────────────────────────────────────

async function showReviewModal() {
  const data = await fetch("/review_tracking").then(r => r.json());
  if (!data.ok) {
    showError(data.error || "Could not load paper_tracking.csv");
    return;
  }

  const headers = data.headers || [];
  const rows = data.rows || [];
  document.getElementById("review-download-link").href =
    `/outputs/${encodeURIComponent(data.filename || "paper_tracking.csv")}`;
  document.getElementById("review-count").textContent =
    `${data.total_rows || rows.length} row${(data.total_rows || rows.length) !== 1 ? "s" : ""}`;

  document.getElementById("review-table-head").innerHTML =
    `<tr>${headers.map(h => `<th>${esc(h)}</th>`).join("")}</tr>`;
  document.getElementById("review-table-body").innerHTML = rows.map(row =>
    `<tr>${headers.map(h => `<td>${esc(String(row[h] ?? ""))}</td>`).join("")}</tr>`
  ).join("");

  document.getElementById("review-modal").classList.add("open");
}

async function continueAfterReview() {
  const btn = document.getElementById("continue-btn");
  btn.disabled = true;
  btn.textContent = "Continuing...";
  document.getElementById("review-modal").classList.remove("open");
  lockUI();
  document.getElementById("status-text").textContent = "Continuing pipeline...";
  startTimer();

  const resp = await fetch("/continue_pipeline", { method: "POST" });
  const data = await resp.json();
  if (!data.ok) {
    btn.disabled = false;
    btn.textContent = "Continue Pipeline";
    showError(data.error);
    unlockUI();
    return;
  }
  btn.disabled = false;
  btn.textContent = "Continue Pipeline";
  openPipelineStream();
}

// ── Paper-selection gate (right after the search agent) ──────────────────────

let selectionRows = [];
let selectionExtraFiles = [];

async function showSelectionModal() {
  const data = await fetch("/found_papers").then(r => r.json());
  if (!data.ok) {
    showError(data.error || "Could not load the found papers");
    return;
  }
  selectionRows = data.rows || [];
  selectionExtraFiles = [];
  document.getElementById("selection-error").textContent = "";
  document.getElementById("selection-table-head").innerHTML =
    `<tr><th class="sel-cell"></th><th>Title</th><th>Authors</th><th>Year</th><th>Source</th><th>DOI</th></tr>`;
  document.getElementById("selection-table-body").innerHTML = selectionRows.map((row, i) => {
    const title = row.url
      ? `<a href="${esc(row.url)}" target="_blank" rel="noopener">${esc(row.title)}</a>`
      : esc(row.title);
    return `<tr id="sel-row-${i}">
      <td class="sel-cell"><input type="checkbox" id="sel-cb-${i}" checked onchange="updateSelectionSummary()"></td>
      <td>${title}</td><td>${esc(String(row.authors))}</td><td>${esc(String(row.year))}</td>
      <td>${esc(String(row.source))}</td><td>${esc(String(row.doi))}</td></tr>`;
  }).join("");
  renderSelectionFiles();
  updateSelectionSummary();
  document.getElementById("selection-modal").classList.add("open");
}

function setAllPapers(checked) {
  selectionRows.forEach((_, i) => { document.getElementById(`sel-cb-${i}`).checked = checked; });
  updateSelectionSummary();
}

function updateSelectionSummary() {
  let kept = 0;
  selectionRows.forEach((_, i) => {
    const on = document.getElementById(`sel-cb-${i}`).checked;
    document.getElementById(`sel-row-${i}`).classList.toggle("declined", !on);
    if (on) kept++;
  });
  const total = selectionRows.length;
  document.getElementById("selection-count").textContent = `${total} paper${total !== 1 ? "s" : ""} found`;
  const extra = selectionExtraFiles.length;
  document.getElementById("selection-summary").textContent =
    `${kept} of ${total} selected` + (extra ? ` · ${extra} PDF${extra !== 1 ? "s" : ""} to add` : "");
}

function addSelectionFiles(files) {
  for (const f of files) {
    if (!f.name.toLowerCase().endsWith(".pdf")) continue;
    if (!selectionExtraFiles.some(x => x.name === f.name && x.size === f.size)) selectionExtraFiles.push(f);
  }
  renderSelectionFiles();
  updateSelectionSummary();
}

function removeSelectionFile(i) {
  selectionExtraFiles.splice(i, 1);
  renderSelectionFiles();
  updateSelectionSummary();
}

function renderSelectionFiles() {
  document.getElementById("selection-file-list").innerHTML = selectionExtraFiles.map((f, i) =>
    `<li><span>${esc(f.name)}</span><button type="button" title="Remove" onclick="removeSelectionFile(${i})">✕</button></li>`
  ).join("");
}

async function submitPaperSelection() {
  const excluded = [];
  selectionRows.forEach((row, i) => {
    if (!document.getElementById(`sel-cb-${i}`).checked) excluded.push(row.id);
  });
  if (excluded.length === selectionRows.length && !selectionExtraFiles.length) {
    document.getElementById("selection-error").textContent =
      "Keep at least one paper or add a PDF to continue.";
    return;
  }
  document.getElementById("selection-modal").classList.remove("open");
  lockUI();
  document.getElementById("status-text").textContent = "Applying your paper selection...";
  startTimer();

  const formData = new FormData();
  formData.append("excluded_ids", JSON.stringify(excluded));
  for (const f of selectionExtraFiles) formData.append("files", f);

  const resp = await fetch("/submit_paper_selection", { method: "POST", body: formData });
  const data = await resp.json();
  if (!data.ok) {
    showError(data.error);
    unlockUI();
    return;
  }
  openPipelineStream();
}

// ── Missing full-text upload gate ───────────────────────────────────────────

async function showFulltextModal() {
  const data = await fetch("/missing_fulltext").then(r => r.json());
  if (!data.ok) {
    showError(data.error || "Could not load missing full-text papers");
    return;
  }

  const rows = data.rows || [];
  const headers = ["title", "authors", "year", "source", "doi", "reason"];
  const labels = {
    title: "Title", authors: "Authors", year: "Year",
    source: "Source", doi: "DOI", reason: "Why full text is missing",
  };

  document.getElementById("fulltext-count").textContent =
    `${data.total_rows || rows.length} paper${(data.total_rows || rows.length) !== 1 ? "s" : ""}`;
  document.getElementById("fulltext-table-head").innerHTML =
    `<tr>${headers.map(h => `<th>${esc(labels[h])}</th>`).join("")}</tr>`;
  document.getElementById("fulltext-table-body").innerHTML = rows.map(row =>
    `<tr>${headers.map(h => `<td>${esc(String(row[h] ?? ""))}</td>`).join("")}</tr>`
  ).join("");

  document.getElementById("fulltext-modal").classList.add("open");
}

function triggerFulltextUpload() {
  document.getElementById("fulltext-file-input").click();
}

async function submitMissingFulltext(files) {
  document.getElementById("fulltext-modal").classList.remove("open");
  lockUI();
  document.getElementById("status-text").textContent =
    (files && files.length) ? "Uploading PDFs..." : "Continuing without uploads...";
  startTimer();

  const formData = new FormData();
  for (const f of (files || [])) formData.append("files", f);

  const resp = await fetch("/upload_missing_fulltext", { method: "POST", body: formData });
  const data = await resp.json();
  if (!data.ok) {
    showError(data.error);
    unlockUI();
    return;
  }
  openPipelineStream();
}

// ── Render results ────────────────────────────────────────────────────────────

function renderResults(res) {
  if (!res || !Object.keys(res).length) return;

  renderPrismaFlow(res);

  // ── Outcome-group selector ──────────────────────────────────────────────────
  // A run with more than one distinct outcome family/timepoint produces
  // several independently pooled results (see agents/meta_analysis_agent.py)
  // -- Key Statistics/Plots below always show ONE of them, defaulting to the
  // "primary" one the backend picked, but every other group is available via
  // this dropdown instead of being invisible.
  window.__lastResults = res;
  const selectWrap = document.getElementById("group-select-wrap");
  const select = document.getElementById("group-select");
  const groups = res.meta_groups || [];
  if (groups.length > 1) {
    select.innerHTML = groups.map(g => {
      const n = g.insufficient_data ? " (insufficient data)" : ` (k=${g.k})`;
      return `<option value="${esc(g.key)}">${esc(g.label)}${n}</option>`;
    }).join("");
    const primary = groups.find(g => g.is_primary) || groups[0];
    select.value = primary.key;
    selectWrap.style.display = "block";
    renderGroupResult(res, primary);
  } else {
    selectWrap.style.display = "none";
    renderGroupResult(res, null); // fall back to the top-level alias fields
  }

  // ── Detailed reports (audit files) ──────────────────────────────────────────
  const csvBar = document.getElementById("audit-csv-bar");
  const reports = [
    [res.audit_tracking_csv, "Paper tracking", "Every retrieved paper, the stage at which it left the pipeline and why."],
    [res.audit_screening_csv, "Screening decisions", "Each paper's screening and eligibility decision, with the exclusion stage and reason."],
    [res.audit_summary_csv, "Run summary", "Your question and how many papers were retrieved, screened, eligible and included."],
    [res.rob_assessments_json, "Risk-of-bias assessments", "RoB 2 / ROBINS-I judgement for every study and domain, with the rationale."],
  ].filter(r => r[0]);
  csvBar.innerHTML = reports.map(([f, title, desc]) => {
    const name = String(f).split("/").pop();
    return `<div class="report-card">
      <div class="report-name">${esc(title)}</div>
      <div class="report-desc">${esc(desc)}</div>
      <div class="report-file">${esc(name)}</div>
      <a class="dbtn" href="/outputs/${f}" download>Download</a>
    </div>`;
  }).join("");
  document.getElementById("reports-section").style.display = reports.length ? "block" : "none";
}

// Study-selection panel. Uses the PRISMA chart's own numbers
// (prisma_flowchart.json, as res.prisma_flow) so it shows every count and
// reason the full chart shows; older runs without it fall back to the
// stage counters.
function renderPrismaFlow(res) {
  const flow = document.getElementById("prisma-flow");
  let steps = (res.prisma_flow && res.prisma_flow.steps) || null;
  if (!steps || !steps.length) {
    steps = [
      {label: "Records retrieved", n: res.n_retrieved},
      {label: "Passed title/abstract screening", n: res.n_screened},
      {label: "Passed full-text eligibility", n: res.n_eligible},
      {label: "Studies with extracted data", n: res.n_studies},
      {label: "Studies included in synthesis", n: res.n_studies,
       note: res.n_effects !== undefined ? `${res.n_effects} effect sizes` : "", final: true},
    ];
  }
  const num = v => (v === undefined || v === null || !Number.isFinite(Number(v))) ? null : Number(v);
  const maxN = Math.max(1, ...steps.map(s => num(s.n) || 0));
  const list = items => {
    const li = (items || []).filter(it => it[1] === null || it[1] > 0).map(it =>
      `<li><span>${esc(it[0])}</span>${it[1] === null ? "" : `<b>${it[1]}</b>`}</li>`);
    if (li.length <= 5) return li.join("");
    return li.slice(0, 4).join("") +
      `<li class="pf-all"><details><summary>Show all ${li.length} reasons</summary><ul>${li.slice(4).join("")}</ul></details></li>`;
  };
  flow.innerHTML = `<div class="pf-head"><span>Stage</span><span>Studies / records</span><span>Removed or added</span></div>` +
    steps.map(s => {
      const n = num(s.n);
      const w = n === null ? 0 : Math.max(3, n / maxN * 100);
      const own = list(s.items);
      let side = "";
      if (s.side && (num(s.side.n) || 0) > 0) {
        const sign = s.side.kind === "in" ? "+" : "&minus;";
        const sub = list(s.side.items);
        side = `<div class="pf-side pf-${s.side.kind === "in" ? "in" : "out"}">
          <div class="pf-side-h">${sign}${s.side.n} ${esc(s.side.label)}</div>
          ${sub ? `<ul>${sub}</ul>` : ""}</div>`;
      }
      return `<div class="pf-row${s.final ? " pf-effects" : ""}">
        <div class="pf-lbl">${esc(s.label)}${s.note ? `<span class="pf-note">${esc(s.note)}</span>` : ""}
          ${own ? `<ul>${own}</ul>` : ""}</div>
        <div class="pf-track"><div class="pf-fill" style="width:${w}%"><span>${n === null ? "—" : n}</span></div></div>
        ${side || '<div class="pf-side"></div>'}
      </div>`;
    }).join("") + ((res.plots && res.plots.prisma)
      ? `<div class="pf-more"><button class="dbtn" type="button" onclick="showPlotTab('selection', true)">View the full PRISMA 2020 chart</button></div>`
      : "");
}

// Called by the outcome dropdown's onchange. `res` (the full /results
// payload) is cached on window.__lastResults by renderResults() above so
// switching groups never needs another round-trip to the server -- every
// group's stats and (already-generated, suffixed) plot filenames were sent
// down in the initial payload.
function selectGroup(key) {
  const res = window.__lastResults;
  if (!res) return;
  const g = (res.meta_groups || []).find(x => x.key === key);
  if (g) renderGroupResult(res, g);
}

// Renders the Key Statistics + Plots sections for ONE outcome group. `group`
// is an entry from res.meta_groups, or null to fall back to the top-level
// alias fields (res.pooled_g/plots/...) -- the pre-multi-group behavior,
// still used for legacy/single-outcome runs where res.meta_groups has 0 or 1
// entries and the selector is hidden.
function renderGroupResult(res, group) {
  const grid = document.getElementById("stat-grid");
  grid.innerHTML = "";

  const g = group || res; // same field names either way -- see dashboard.py's
                           // _results_from_pipeline_state()/meta_groups builder
  if (g.insufficient_data) {
    grid.innerHTML += scard("Insufficient data", "—",
      `Only ${g.k} contributing effect size${g.k!==1?"s":""} -- at least 2 are needed to pool`, "risk-moderate");
  } else if (g.pooled_g !== undefined) {
    // measure_label/native_pooling_used come from the pipeline's own
    // effect-measure resolution (utils/effect_measures.py) -- never
    // hardcode "Hedges' g" here, a group may be pooled on RR/OR/MD instead.
    const measureLabel = g.measure_label ? `Pooled ${g.measure_label}` : "Pooled Hedges' g";
    const measureWarn = g.native_pooling_used === false
      ? " &nbsp; Note: effect measure not confirmed — standardized fallback shown"
      : "";
    const modelNote = res.pooling_model_label ? `<br>${res.pooling_model_label}` : "";
    grid.innerHTML += scard(measureLabel, g.pooled_g,
      `95% CI [${g.ci_lower}, ${g.ci_upper}] &nbsp; p = ${g.p_value}${measureWarn}${modelNote}`, "highlight");
    grid.innerHTML += scard("I²", g.i_squared+"%",
      `τ = ${g.tau}`);
    grid.innerHTML += scard("Studies (k)", g.k,
      group ? `${g.n_total||''} total N` : `${res.n_effects} effect size${res.n_effects!==1?"s":""}`);
  }
  // Publication bias / Risk of Bias are computed once for the whole run, not
  // per outcome group (see agents/bias_agent.py, agents/rob_agent.py) -- so
  // these two cards always come from the top-level res, regardless of which
  // group is selected.
  if (res.bias_risk) {
    grid.innerHTML += scard("Publication Bias", res.bias_risk.toUpperCase(),
      `Egger's p = ${res.eggers_p} &nbsp; k₀ = ${res.trim_fill_k0}`
        + (res.rank_test_p !== undefined ? ` &nbsp; Begg's p = ${res.rank_test_p}` : "")
        + (res.pet_peese_estimate !== undefined && res.pet_peese_estimate !== null
            ? `<br>PET-PEESE (${res.pet_peese_selected}) = ${res.pet_peese_estimate}` : ""),
      `risk-${res.bias_risk}`);
  }
  if (res.rob_n_assessed) {
    const robClass = res.rob_n_high > 0 ? "risk-high" : (res.rob_n_elevated > 0 ? "risk-moderate" : "risk-low");
    grid.innerHTML += scard("Risk of Bias", `${res.rob_n_elevated}/${res.rob_n_assessed} elevated`,
      `RoB 2: ${res.rob_n_rob2} &nbsp; ROBINS-I: ${res.rob_n_robinsi} &nbsp; High/Serious: ${res.rob_n_high}`,
      robClass);
  }

  renderResultsTable(res, group);

  const labels = {
    forest:"Forest Plot", cumulative:"Cumulative Meta-Analysis",
    distribution:"Effect Size Distribution",
    bubble:"Effect Size vs. Sample Size", funnel:"Funnel Plot",
    heterogeneity:"Heterogeneity Summary",
    rob_rob2:"Risk of Bias (RoB 2)", rob_robins_i:"Risk of Bias (ROBINS-I)",
    prisma:"PRISMA 2020 Flowchart",
  };
  const ts = Date.now();
  const groupPlots = group ? (group.plots || {}) : (res.plots || {});
  // rob_rob2/rob_robins_i/prisma are run-level-only (never per-group) --
  // always show them alongside whichever group's own plots are selected.
  const all = {...groupPlots};
  for (const key of ["rob_rob2", "rob_robins_i", "prisma"]) {
    if (res.plots && res.plots[key]) all[key] = res.plots[key];
  }
  const card = (key, fname) => {
    const title = labels[key] || key;
    const png = `/outputs/${fname}`;
    const pdf = png.replace(/\.png$/i, ".pdf");
    return `<div class="plot-card">
      <img src="${png}?t=${ts}" alt="${esc(title)}" loading="lazy" onclick="zoomPlot(this)" title="Click to enlarge"/>
      <div class="plot-foot">
        <span class="plot-title">${esc(title)}</span>
        <span class="plot-actions">
          <button class="pbtn" type="button" onclick="zoomPlot(this)">Zoom</button>
          ${pdf !== png ? `<a class="pbtn pdf-link" data-file="${esc(pdf.split("/").pop())}" href="${pdf}" download>PDF</a>` : ""}
          <a class="pbtn" href="${png}" download>PNG</a>
        </span>
      </div>
    </div>`;
  };
  const panels = PLOT_TABS.map(t => ({...t, html: ""}));
  const byKey = {};
  panels.forEach(t => t.keys.forEach(k => { byKey[k] = t; }));
  const effectsTab = panels.find(t => t.id === "effects");
  for (const [key, fname] of Object.entries(all)) {
    (byKey[key] || effectsTab).html += card(key, fname);
  }
  window.__plotPanels = panels.filter(t => t.html);
  const tabs = document.getElementById("plot-tabs");
  tabs.innerHTML = window.__plotPanels.map(t =>
    `<button class="plot-tab" type="button" role="tab" data-tab="${t.id}" onclick="showPlotTab('${t.id}')">${t.title}</button>`
  ).join("");
  const keep = window.__plotPanels.find(t => t.id === window.__plotTab);
  showPlotTab(keep ? keep.id : (window.__plotPanels.find(t => t.id === "effects") || window.__plotPanels[0] || {}).id);
}

// Plot sub-panels: which plot keys go in which tab. Keys not listed here
// (new plot types) fall into "Effect sizes".
const PLOT_TABS = [
  {id: "selection", title: "Search & selection", keys: ["prisma"],
   desc: "How the papers were found and filtered, following the PRISMA 2020 statement."},
  {id: "effects", title: "Effect sizes", keys: ["forest", "distribution", "bubble"],
   desc: "Each study's effect with its confidence interval, and the pooled estimate."},
  {id: "robust", title: "Robustness & heterogeneity", keys: ["cumulative", "heterogeneity"],
   desc: "How stable the pooled estimate is as studies are added, and how much the studies disagree."},
  {id: "bias", title: "Bias", keys: ["funnel", "rob_rob2", "rob_robins_i"],
   desc: "Signs of publication bias (funnel plot) and each study's risk-of-bias judgement."},
];

function showPlotTab(id, scroll) {
  const t = (window.__plotPanels || []).find(p => p.id === id);
  if (!t) return;
  window.__plotTab = id;
  document.getElementById("plots-grid").innerHTML = t.html;
  document.getElementById("plot-tab-desc").textContent = t.desc;
  document.querySelectorAll("#plot-tabs .plot-tab").forEach(b => {
    const on = b.dataset.tab === id;
    b.classList.toggle("active", on);
    b.setAttribute("aria-selected", on ? "true" : "false");
  });
  hideMissingPdfs();
  if (scroll) document.getElementById("plot-tabs").scrollIntoView({behavior: "smooth", block: "start"});
}

// Older runs saved some plots as PNG only: hide a PDF button whose file is
// not among this session's output files.
async function hideMissingPdfs() {
  if (!window.__outFiles) {
    try { window.__outFiles = new Set((await (await fetch("/files")).json()).map(f => f.name)); }
    catch (e) { return; }
    setTimeout(() => { window.__outFiles = null; }, 5000);
  }
  document.querySelectorAll("#plots-grid .pdf-link").forEach(a => {
    if (!window.__outFiles.has(a.dataset.file)) a.remove();
  });
}

function zoomPlot(el) {
  const img = el.closest(".plot-card").querySelector("img");
  openLightbox(img.src, img.alt);
}

// Copy-ready summary table: one header row + one result row, matching the
// layout a reader expects to paste into Excel. Plain ASCII hyphen-minus is
// used on purpose (Excel does not parse a Unicode minus sign as a number).
// `group` is an entry from res.meta_groups, or null for the legacy
// single-outcome alias fields on res itself. Egger's p is run-level only
// (agents/bias_agent.py computes it once for the whole run).
const RESULTS_TABLE_HEADERS = ["Effect measure", "Effect", "k", "N", "CI", "p-value", "I²", "Egger's p", "Direction"];
window.__resultsTableRow = null;

function _fmtNum(v, d) {
  return (v === undefined || v === null || v === "" || Number.isNaN(Number(v))) ? "" : Number(v).toFixed(d);
}

function renderResultsTable(res, group) {
  const section = document.getElementById("results-table-section");
  const table = document.getElementById("results-table");
  const g = group || res;
  if (!section || !table) return;
  if (g.insufficient_data || g.pooled_g === undefined) {
    window.__resultsTableRow = null;
    section.style.display = "none";
    return;
  }
  const p = Number(g.p_value);
  const pText = Number.isNaN(p) ? "" : (p < 0.0001 ? "<0.0001" : p.toFixed(4));
  const favors = g.favors || "";
  const direction = !favors ? "" : (favors.startsWith("Neither") ? favors : "Favors " + favors);
  const row = [
    g.measure_label || "Hedges' g",
    _fmtNum(g.pooled_g, 3),
    g.k === undefined ? "" : String(g.k),
    (g.n_total === undefined || g.n_total === null) ? "" : String(g.n_total),
    `[${_fmtNum(g.ci_lower, 3)}, ${_fmtNum(g.ci_upper, 3)}]`,
    pText,
    Number.isNaN(Number(g.i_squared)) ? "" : `${Math.round(Number(g.i_squared))}%`,
    _fmtNum(res.eggers_p, 4),
    direction,
  ];
  window.__resultsTableRow = row;
  table.innerHTML =
    "<thead><tr>" + RESULTS_TABLE_HEADERS.map(h => `<th>${esc(h)}</th>`).join("") + "</tr></thead>" +
    "<tbody><tr>" + row.map(c => `<td>${esc(c)}</td>`).join("") + "</tr></tbody>";
  section.style.display = "block";
}

function copyResultsTable() {
  const row = window.__resultsTableRow;
  if (!row) return;
  // Values only (no header row): the Excel sheet already has the column names.
  const text = row.join("\\t");
  const hint = document.getElementById("results-table-hint");
  const done = ok => {
    if (hint) hint.textContent = ok ? "Copied. Paste into Excel." : "Copy failed: select the table and copy it manually.";
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => done(true), () => done(false));
  } else {
    const ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    let ok = false;
    try { ok = document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    done(ok);
  }
}

function scard(label, value, sub, extra="") {
  return `<div class="stat-card ${extra}">
    <div class="stat-label">${label}</div>
    <div class="stat-value">${value}</div>
    ${sub?`<div class="stat-sub">${sub}</div>`:""}
  </div>`;
}

// ── Files panel toggle ────────────────────────────────────────────────────────

function toggleFiles() {
  const card = document.getElementById("files-card");
  const isOpen = card.classList.toggle("open");
  if (isOpen) renderFiles();
}

function openFiles() {
  const card = document.getElementById("files-card");
  if (!card.classList.contains("open")) {
    card.classList.add("open");
    renderFiles();
  }
}

// ── Render output files ───────────────────────────────────────────────────────

async function renderFiles() {
  const files = await fetch("/files").then(r => r.json());
  const grid  = document.getElementById("files-grid");
  const count = document.getElementById("files-count");

  if (!files.length) {
    grid.innerHTML = '<span class="files-empty">No output files yet — run an analysis to generate results.</span>';
    count.textContent = "";
    return;
  }

  count.textContent = `${files.length} file${files.length!==1?"s":""}`;

  const icons = {json:"", md:"", csv:"", png:"", pdf:""};
  const fmt = n => n<1024?`${n} B`:n<1024**2?`${(n/1024).toFixed(1)} KB`:`${(n/1024**2).toFixed(1)} MB`;

  grid.innerHTML = files.map(f => {
    const isPng = f.type === "png";
    const viewBtn = isPng
      ? `<button class="vbtn" onclick="openLightbox('/outputs/${f.name}','${f.name}')">View</button>`
      : "";
    return `
    <div class="file-row">
      <span class="file-icon">${icons[f.type]||""}</span>
      <div class="file-info">
        <div class="file-name">${f.name}</div>
        <div class="file-meta">${fmt(f.size)} · ${f.modified}</div>
      </div>
      <div class="file-actions">
        <span class="file-type-badge ft-${f.type}">${f.type}</span>
        ${viewBtn}
        <a class="dbtn" href="/outputs/${f.name}" download>Download</a>
      </div>
    </div>`;
  }).join("");
}

// ── Lightbox ──────────────────────────────────────────────────────────────────

function openLightbox(src, caption) {
  document.getElementById("lightbox-img").src = src;
  document.getElementById("lightbox-caption").textContent = caption;
  document.getElementById("lightbox").classList.add("open");
  document.addEventListener("keydown", onLightboxKey);
}

function closeLightbox() {
  document.getElementById("lightbox").classList.remove("open", "zoomed");
  document.getElementById("lightbox-img").src = "";
  document.removeEventListener("keydown", onLightboxKey);
}

function onLightboxKey(e) { if (e.key === "Escape") closeLightbox(); }

// Stop click on the image itself from closing the lightbox
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("lightbox-img").addEventListener("click", e => {
    e.stopPropagation();
    document.getElementById("lightbox").classList.toggle("zoomed");
  });
  document.getElementById("mode-auto").addEventListener("click", () => setMode("auto"));
  document.getElementById("mode-pdf").addEventListener("click", () => setMode("manual"));
  document.getElementById("pdf-input").addEventListener("change", e => handlePdfFiles(e.target.files));
  renderFiles();
});

// ── Helpers ───────────────────────────────────────────────────────────────────

function showError(msg) {
  const el = document.getElementById("error-panel");
  el.textContent = "Error: " + msg;
  el.classList.add("visible");
}
function lockUI() {
  showCancel(true);
  document.getElementById("console-card").style.display = "";   // real runs show the log again
  document.getElementById("run-btn").disabled          = true;
  document.getElementById("prompt").disabled           = true;
  document.getElementById("model-select").disabled     = true;
  document.getElementById("pooling-select").disabled   = true;
  document.querySelector(".spinner").style.display = "";
  document.getElementById("status-bar").classList.add("visible");
}
function unlockUI() {
  document.getElementById("run-btn").disabled          = false;
  document.getElementById("prompt").disabled           = false;
  document.getElementById("model-select").disabled     = false;
  document.getElementById("pooling-select").disabled   = false;
  document.querySelector(".spinner").style.display = "none";
}

async function startDownstream() {
  const prompt = document.getElementById("prompt").value.trim();
  if (!prompt) { document.getElementById("prompt").focus(); return; }

  document.getElementById("log").innerHTML = "";
  document.getElementById("results-panel").classList.remove("visible");
  document.getElementById("error-panel").classList.remove("visible");
  logLineCount = 0;
  document.getElementById("log-count").textContent = "";
  resetStages();
  lockUI();
  document.getElementById("status-text").textContent = "Running analysis stages (5–9)...";
  startTimer();

  if (es) { es.close(); es = null; }

  const resp = await fetch("/run_analysis", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({prompt}),
  });
  const data = await resp.json();
  if (!data.ok && data.busy) { stopTimer(); unlockUI(); document.getElementById("status-text").textContent = "Ready"; showBusyPopup(data.error); return; }
  if (!data.ok) { showError(data.error); unlockUI(); return; }

  openPipelineStream();
}
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  AutoSynthesis Dashboard")
    print("  http://localhost:8000")
    print("=" * 55 + "\n")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
