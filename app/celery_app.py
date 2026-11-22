"""Celery application object -- Phase 4 of the infrastructure migration.

Deliberately imports NOTHING from `agents/`, `orchestrator.py`, or
`run_service.py` at module level (those pull in rpy2/Playwright/LangGraph,
which must stay out of the prefork parent process -- `tasks.py` does its
real imports inside each task body instead, matching the exact pattern
`run_service.py`'s execute_* functions already use for `orchestrator`).

Config is tuned for a handful of 20-40 minute, LLM-bound jobs -- Celery's
own defaults (short tasks, many of them, disposable results) are wrong for
this workload; every deviation below is explained inline. See the plan's
Phase 4 section for the full rationale.
"""

from __future__ import annotations

from celery import Celery

import config as _config

app = Celery("autosynthesis", broker=_config.CELERY_BROKER_URL or None)

app.conf.update(
    # ── Queue / routing ──────────────────────────────────────────────────
    task_default_queue=_config.CELERY_TASK_QUEUE,
    task_default_exchange=_config.CELERY_TASK_QUEUE,
    task_default_routing_key=_config.CELERY_TASK_QUEUE,

    # ── Reliability vs. duplicate-execution trade-off ───────────────────
    # acks_late=True (Celery's usual recommendation) redelivers a task if
    # the worker dies mid-execution -- for a 20-40 minute LLM-driven run
    # that means silently re-running (and re-billing) a large chunk of
    # work. We take the opposite trade: acks_late=False means a crashed
    # worker loses only the in-flight MESSAGE, never the run itself -- the
    # `runs` row already has status/stage-events/partial data (persisted
    # incrementally by run_service.py throughout execution), and recovery
    # is an explicit POST /api/runs/{id}/retry, not automatic redelivery.
    task_acks_late=False,
    task_reject_on_worker_lost=False,
    # Never let a task auto-retry into a second LLM bill -- retries are a
    # human decision (the /retry endpoint), not an automatic one.
    task_annotations={"*": {"max_retries": 0}},

    # ── Prefetch / concurrency ───────────────────────────────────────────
    # One task at a time per worker process -- these are long, expensive,
    # memory-heavy (rpy2 + Chromium) jobs, not a queue of quick ones; the
    # ceiling on throughput is LLM rate limits/cost, not CPU (matches
    # cochrane_benchmark/runner.py's own COCHRANE_MAX_PARALLEL_REVIEWS
    # reasoning). Scale OUT (more worker processes/containers) rather than
    # up (more prefetch) -- see docker-compose.yml's celery-worker service.
    worker_prefetch_multiplier=1,
    worker_concurrency=_config.CELERY_WORKER_CONCURRENCY,
    # Recycle the child process after every task -- rpy2's R runtime and
    # Playwright/Chromium accumulate memory across runs that a normal
    # Python GC won't reclaim; a fresh child per task is the simplest fix.
    worker_max_tasks_per_child=_config.CELERY_MAX_TASKS_PER_CHILD,
    # rpy2/pypdf/Playwright are blocking C-extension calls -- never
    # gevent/eventlet (they'd silently serialize everything anyway).
    worker_pool="prefork",

    # ── Time limits ───────────────────────────────────────────────────────
    task_time_limit=_config.CELERY_TASK_TIME_LIMIT,          # hard kill
    task_soft_time_limit=_config.CELERY_TASK_SOFT_TIME_LIMIT,  # SoftTimeLimitExceeded first

    # ── Results ───────────────────────────────────────────────────────────
    # Nothing reads a Celery AsyncResult -- run_store (Postgres) is the
    # single source of truth for status/results, so don't pay to store a
    # duplicate copy in the broker/backend.
    task_ignore_result=True,
    result_backend=_config.CELERY_RESULT_BACKEND or None,

    # ── Broker connection ────────────────────────────────────────────────
    broker_connection_retry_on_startup=True,
    broker_heartbeat=_config.CELERY_BROKER_HEARTBEAT,

    # ── Serialization ────────────────────────────────────────────────────
    # Task payloads are just a run_id string (+ small args) -- see
    # tasks.py's module docstring for why the multi-MB GraphState never
    # enters RabbitMQ. json is sufficient and avoids pickle's RCE surface.
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    worker_send_task_events=_config.CELERY_WORKER_EVENTS,
)

# tasks.py registers its @app.task-decorated functions on import; imported
# here (not above, to keep this module's own import graph light) so
# `celery -A celery_app.app worker` (entrypoint.sh's APP_ROLE=worker case)
# finds them.
import tasks  # noqa: E402,F401
