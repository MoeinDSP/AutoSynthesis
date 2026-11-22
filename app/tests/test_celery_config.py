"""Pins celery_app.py's config contract -- the specific deviations from
Celery's defaults that make this workload (a handful of 20-40 minute,
LLM-bound jobs) work correctly. See celery_app.py's inline comments for the
rationale behind each one; this test exists so a future "helpful" tuning
change doesn't silently reintroduce Celery's defaults (which are wrong
here) without a human noticing."""

import celery_app


class TestCeleryConfigContract:
    def test_acks_late_is_off(self):
        # Deliberate: a worker crash must lose only the in-flight message,
        # never trigger automatic redelivery of an expensive LLM-driven run.
        assert celery_app.app.conf.task_acks_late is False

    def test_no_automatic_retries(self):
        assert celery_app.app.conf.task_annotations["*"]["max_retries"] == 0

    def test_prefetch_is_one(self):
        assert celery_app.app.conf.worker_prefetch_multiplier == 1

    def test_max_tasks_per_child_is_one(self):
        # Recycles the rpy2/Playwright-laden child process after every run.
        assert celery_app.app.conf.worker_max_tasks_per_child == 1

    def test_pool_is_prefork_not_gevent_or_eventlet(self):
        # rpy2/pypdf/Playwright are blocking C-extension calls.
        assert celery_app.app.conf.worker_pool == "prefork"

    def test_time_limits_are_generous_not_celerys_short_defaults(self):
        assert celery_app.app.conf.task_time_limit >= 3600
        assert celery_app.app.conf.task_soft_time_limit >= 3600
        assert celery_app.app.conf.task_soft_time_limit < celery_app.app.conf.task_time_limit

    def test_results_are_not_stored(self):
        # Nothing reads a Celery AsyncResult -- Postgres (run_store) is the
        # single source of truth for status/results.
        assert celery_app.app.conf.task_ignore_result is True

    def test_task_serializer_is_json_not_pickle(self):
        assert celery_app.app.conf.task_serializer == "json"

    def test_broker_reconnects_on_startup(self):
        assert celery_app.app.conf.broker_connection_retry_on_startup is True

    def test_default_queue_matches_config(self):
        import config
        assert celery_app.app.conf.task_default_queue == config.CELERY_TASK_QUEUE

    def test_all_four_tasks_registered(self):
        names = set(celery_app.app.tasks.keys())
        for expected in [
            "autosynthesis.run_pipeline",
            "autosynthesis.continue_after_fulltext",
            "autosynthesis.continue_after_review",
            "autosynthesis.run_downstream",
        ]:
            assert expected in names
