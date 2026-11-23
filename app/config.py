"""Configuration for the meta-analysis pipeline -- API settings only."""

import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenRouter ────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-5.6-sol")
# Experimental, OFF by default: when "1", a between-arm difference with its SE
# (e.g. an estimated treatment difference + 95% CI from ANCOVA/MMRM) is used
# for effect sizes and MD pooling whenever no other statistic works. Kept
# behind a switch so the published benchmark runs stay reproducible.
DIFF_FALLBACK = os.getenv("AUTOSYN_DIFF_FALLBACK", "").strip() == "1"
# Models a user can pick per run in the dashboard (the three used for the
# Cochrane benchmark). The first is the default.
_ALL_MODELS = [
    {"id": "openai/gpt-5.6-sol",        "label": "GPT-5.6 Sol"},
    {"id": "google/gemini-3.8-flash",   "label": "Gemini 3.8 Flash"},
    {"id": "anthropic/claude-opus-5",   "label": "Claude Opus 5"},
]
CHEAPEST_MODEL = "google/gemini-3.8-flash"   # lowest measured cost per study ($0.36 vs $2.27 / $2.91)

# ENABLED_MODELS locks a deployment to specific models, e.g. the public web app
# sets ENABLED_MODELS=google/gemini-3.8-flash so nobody can start a run with a
# more expensive model. Unset or "all" = every model (benchmark / local use).
_enabled_env = os.getenv("ENABLED_MODELS", "all").strip()
if _enabled_env.lower() in ("", "all"):
    ENABLED_MODELS = [m["id"] for m in _ALL_MODELS]
else:
    ENABLED_MODELS = [x.strip() for x in _enabled_env.split(",") if x.strip()]
AVAILABLE_MODELS = [m for m in _ALL_MODELS if m["id"] in ENABLED_MODELS]
if not AVAILABLE_MODELS:
    raise RuntimeError(f"ENABLED_MODELS={_enabled_env!r} matches none of {[m['id'] for m in _ALL_MODELS]}")
# Any configured chat model that is not enabled falls back to the first enabled one,
# so a leftover MODEL_NAME / query-variant setting in .env cannot bypass the lock.
if MODEL_NAME not in ENABLED_MODELS:
    MODEL_NAME = AVAILABLE_MODELS[0]["id"]


def set_active_model(model_id: str) -> None:
    """Switch the model every agent uses (read per request by agents/llm.py)."""
    global MODEL_NAME
    if model_id not in ENABLED_MODELS:
        raise ValueError(f"Model not enabled: {model_id}")
    MODEL_NAME = model_id


VISION_MODEL_NAME = os.getenv("VISION_MODEL_NAME", "anthropic/claude-opus-5")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MISTRAL_API_KEY = os.getenv("Mistral_api", "")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "")
MINERU_API_KEY = os.getenv("MinerU_API_KEY") or os.getenv("MINERU_API_KEY") or ""
# https://keenable.ai -- general web-search + landing-page-to-markdown API.
# Used as an additional (not sole) full-text discovery source and for
# /v1/fetch-based landing-page extraction in
# agents/paper_reading_agent.py::fetch_fulltext_node. Empty key => fully
# disabled, same convention as every other optional API key above.
KEENABLE_API_KEY = os.getenv("KEENABLE_API_KEY", "")

# ── Search ────────────────────────────────────────────────────────────────────
# How many papers to retain per query per enabled source.
MAX_PAPERS_PER_QUERY = int(os.getenv("MAX_PAPERS_PER_QUERY", "10"))
# Comma-separated sources the paper-discovery stage should query.
# Available names: deep_research, arxiv, semantic_scholar, crossref, osf,
# pubmed, elsevier (Scopus; requires ELSEVIER_API_KEY), wos (Web of Science;
# requires WOS_API_KEY), clinicaltrials_gov (free, no key). See
# database_search.py::SOURCE_REGISTRY for the authoritative list, including
# sources that are recognised but not yet usable (central, embase, cinahl,
# ictrp -- no confirmed API access; use manual import instead, see
# MANUAL_IMPORT_PATHS below). Matching is case/underscore/hyphen-insensitive
# (database_search.py::_normalize_db_name) so e.g. "SemanticScholar" and
# "semantic_scholar" both resolve to the same source. By default, paper
# discovery starts with OpenRouter
# o4-mini Deep Research. Academic databases are then used downstream to locate
# metadata, open-access PDFs, PMC full text, and DOI/Unpaywall content.
ENABLED_SEARCH_DATABASES = tuple(
    db.strip().lower()
    for db in os.getenv(
        "ENABLED_SEARCH_DATABASES",
        "deep_research",
    ).split(",")
    if db.strip()
)
# Comma-separated paths to manually-exported search-result files (.ris/.csv/
# .bib) -- see utils/manual_import.py. Used for sources with no live API
# connector (CENTRAL, Embase, CINAHL, Web of Science if desired) where a
# human ran the search through the database's own web interface and
# exported the results. Every record loaded this way goes through the SAME
# dedup/screening/full-text/eligibility/extraction pipeline as an
# API-retrieved paper -- no special treatment. Empty by default.
MANUAL_IMPORT_PATHS = tuple(
    p.strip() for p in os.getenv("MANUAL_IMPORT_PATHS", "").split(",") if p.strip()
)
# Maximum number of search-mode papers to attempt full-text retrieval for after
# title/abstract screening. Existing full-text records do not count toward it.
# LLM title/abstract screening between search and full-text retrieval
# (agents/screening_agent.py). On by default; set to 0 to skip it.
TITLE_ABSTRACT_SCREENING = os.getenv("TITLE_ABSTRACT_SCREENING", "1").strip().lower() in ("1", "true", "yes", "on")
SCREENING_WORKERS = int(os.getenv("SCREENING_WORKERS", "8"))
FULL_TEXT_FETCH_BUDGET = int(os.getenv("FULL_TEXT_FETCH_BUDGET", "40"))
# Hard wall-clock cap (seconds) on how long fetch_fulltext_node's retrieval
# cascade may spend on a single paper. Each paper's cascade runs in its own
# background thread; if it doesn't finish within this many seconds, that
# paper is abandoned (recorded as no-fulltext) and the run moves on to the
# next paper instead of hanging forever -- the concrete failure mode this
# guards against is a wedged Playwright/asyncio state in
# _browser_download_and_extract (see its docstring), which can otherwise
# stall the entire run indefinitely with no error and no timeout of its own.
FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS = int(os.getenv("FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS", "600"))
# Allow database-style full-text fallbacks such as arXiv, Semantic Scholar,
# CrossRef, OSF, PubMed/PMC, and DOI/Unpaywall.
# Returned paper URLs are tried later as direct/open-access retrieval fallbacks.
FULL_TEXT_USE_DATABASE_FALLBACKS = (
    os.getenv("FULL_TEXT_USE_DATABASE_FALLBACKS", "true").strip().lower()
    in {"1", "true", "yes", "on"}
)
# If database/index retrieval cannot find full text, use Deep Research web
# search as a last-resort open/direct PDF or landing-page finder. This does not
# bypass publisher paywalls or access controls.
FULL_TEXT_USE_WEB_SEARCH_FALLBACKS = (
    os.getenv("FULL_TEXT_USE_WEB_SEARCH_FALLBACKS", "true").strip().lower()
    in {"1", "true", "yes", "on"}
)
# Browser fallback for open publisher pages whose PDF links are created by
# JavaScript. This uses Playwright/Chromium as a last resort and does not bypass
# paywalls, logins, CAPTCHAs, or access controls.
FULL_TEXT_USE_BROWSER_FALLBACKS = (
    os.getenv("FULL_TEXT_USE_BROWSER_FALLBACKS", "true").strip().lower()
    in {"1", "true", "yes", "on"}
)
# Maximum number of intent-focused query variants to send to each database.
SEARCH_QUERY_VARIANTS = int(os.getenv("SEARCH_QUERY_VARIANTS", "5"))
# Use the main LLM to rewrite/expand search queries from the planned research
# question before falling back to deterministic keyword templates.
USE_LLM_SEARCH_QUERY_VARIANTS = (
    os.getenv("USE_LLM_SEARCH_QUERY_VARIANTS", "true").strip().lower()
    in {"1", "true", "yes", "on"}
)
SEARCH_QUERY_VARIANT_MODEL = os.getenv("SEARCH_QUERY_VARIANT_MODEL", "openai/gpt-5.6-sol")
if SEARCH_QUERY_VARIANT_MODEL not in ENABLED_MODELS:
    SEARCH_QUERY_VARIANT_MODEL = AVAILABLE_MODELS[0]["id"]   # see ENABLED_MODELS above
DEEP_RESEARCH_MODEL = os.getenv("DEEP_RESEARCH_MODEL", "openai/gpt-5.6-sol")
DEEP_RESEARCH_MAX_TOOL_CALLS = int(os.getenv("DEEP_RESEARCH_MAX_TOOL_CALLS", "10"))
DEEP_RESEARCH_TIMEOUT_SECONDS = int(os.getenv("DEEP_RESEARCH_TIMEOUT_SECONDS", "240"))

# ── Statistical analysis ──────────────────────────────────────────────────────
ALPHA = 0.05
REML_MAX_ITER = 1000
REML_TOL = 1e-8

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
DOWNLOADED_PDF_DIR = os.getenv("DOWNLOADED_PDF_DIR", "downloaded_pdfs")

# ── Infrastructure (Postgres / Redis / Celery / RabbitMQ) ──────────────────────
# Every one of these subsystems is OPTIONAL and OFF by default: an empty
# *_URL means "not configured", and persistence.py/caching/run_service.py all
# no-op cleanly in that case (see their own module docstrings) -- a bare
# checkout with no infra services running behaves exactly as before this
# block was added. See docker-compose.yml for the corresponding services and
# .env.example for the full set of values a real deployment needs.

# Postgres -- durable run/result storage (persistence/db.py). Empty = disabled.
DATABASE_URL = os.getenv("DATABASE_URL", "")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "5"))
DB_POOL_RECYCLE_SECONDS = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800"))
DB_STATEMENT_TIMEOUT_MS = int(os.getenv("DB_STATEMENT_TIMEOUT_MS", "30000"))
DB_ECHO = os.getenv("DB_ECHO", "false").strip().lower() in {"1", "true", "yes", "on"}

# Redis -- PDF-text cache (caching/) + run-log transport (runlog.py). Empty = disabled.
REDIS_URL = os.getenv("REDIS_URL", "")
REDIS_CACHE_DB = int(os.getenv("REDIS_CACHE_DB", "0"))
REDIS_EVENTS_DB = int(os.getenv("REDIS_EVENTS_DB", "1"))
REDIS_SOCKET_TIMEOUT_SECONDS = float(os.getenv("REDIS_SOCKET_TIMEOUT_SECONDS", "3"))
PDF_TEXT_CACHE_ENABLED = (
    os.getenv("PDF_TEXT_CACHE_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
)
# Manual half of cache invalidation -- bump this whenever utils/mineru_*.py,
# utils/llamaparse_extractor.py, or utils/mistral_ocr_extractor.py change in
# a way that alters extracted text (the automatic half is a source-code hash
# of the dispatch functions themselves -- see caching/pdf_text_cache.py).
PDF_TEXT_CACHE_VERSION = os.getenv("PDF_TEXT_CACHE_VERSION", "v1")
PDF_TEXT_CACHE_TTL_SECONDS = int(os.getenv("PDF_TEXT_CACHE_TTL_SECONDS", "0"))  # 0 = no expiry
PDF_TEXT_CACHE_MAX_BYTES = int(os.getenv("PDF_TEXT_CACHE_MAX_BYTES", str(8 * 1024 * 1024)))
RUN_LOG_TTL_SECONDS = int(os.getenv("RUN_LOG_TTL_SECONDS", "86400"))
RUN_LOG_MAX_LINES = int(os.getenv("RUN_LOG_MAX_LINES", "2000"))

# Human-in-the-loop pause right after the search agent (search mode only): the
# user can untick papers that should not enter the pipeline and upload extra
# PDFs to add alongside the found ones. Set to "false" for unattended runs.
# Paper shown on the dashboard landing page (override with PAPER_URL in .env).
PAPER_TITLE = os.getenv("PAPER_TITLE", "AutoSynthesis: An agentic system for automated meta-analysis")
PAPER_URL = os.getenv("PAPER_URL", "https://arxiv.org/abs/2607.15247").strip()
PAPER_SELECTION_GATE = os.getenv("PAPER_SELECTION_GATE", "true").strip().lower() in ("1", "true", "yes", "on")

# Execution backend -- "thread" (default, today's behaviour) or "celery".
RUN_EXECUTION_BACKEND = os.getenv("RUN_EXECUTION_BACKEND", "thread").strip().lower()
RUN_HEARTBEAT_SECONDS = int(os.getenv("RUN_HEARTBEAT_SECONDS", "30"))
RUN_STALE_SECONDS = int(os.getenv("RUN_STALE_SECONDS", "1800"))
RUN_QUEUE_TIMEOUT_SECONDS = int(os.getenv("RUN_QUEUE_TIMEOUT_SECONDS", "3600"))

# Celery / RabbitMQ -- background task execution (celery_app.py, tasks.py).
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "")  # deliberately unset by default
CELERY_TASK_QUEUE = os.getenv("CELERY_TASK_QUEUE", "autosynthesis.pipeline")
CELERY_WORKER_CONCURRENCY = int(os.getenv("CELERY_WORKER_CONCURRENCY", "2"))
# 20-40 minute LLM-bound jobs -- generous hard/soft limits, not the short-task
# defaults Celery assumes. See run_service.py/celery_app.py for why every
# other Celery default is also overridden for this workload.
CELERY_TASK_TIME_LIMIT = int(os.getenv("CELERY_TASK_TIME_LIMIT", "14400"))       # 4h hard
CELERY_TASK_SOFT_TIME_LIMIT = int(os.getenv("CELERY_TASK_SOFT_TIME_LIMIT", "10800"))  # 3h soft
CELERY_MAX_TASKS_PER_CHILD = int(os.getenv("CELERY_MAX_TASKS_PER_CHILD", "1"))
CELERY_BROKER_HEARTBEAT = int(os.getenv("CELERY_BROKER_HEARTBEAT", "120"))
CELERY_WORKER_EVENTS = (
    os.getenv("CELERY_WORKER_EVENTS", "false").strip().lower() in {"1", "true", "yes", "on"}
)

# ── Server identity ──────────────────────────────────────────────────────────
# SESSION_SECRET: dashboard.py's SessionMiddleware previously defaulted to a
# FRESH RANDOM value every process restart (secrets.token_hex(32)), silently
# invalidating every session cookie -- harmless when restarts are rare, but
# once Celery/Docker make restarts routine this breaks any client (including
# n8n's HTTP-node cookie jars) mid-session. Pin a real value in .env for any
# deployment that restarts more than once in a session's lifetime; the
# random fallback remains for zero-config local/dev use (dashboard.py logs a
# WARNING when it's used).
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
APP_ROLE = os.getenv("APP_ROLE", "api").strip().lower()  # "api" | "worker" | "migrate"
APP_VERSION = os.getenv("APP_VERSION", "")
