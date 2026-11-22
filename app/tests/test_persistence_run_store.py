"""persistence/run_store.py -- against a REAL Postgres. Skipped unless
TEST_DATABASE_URL is set (see conftest.py). Also covers graceful
degradation (DATABASE_URL empty -> every function is a safe no-op), which
needs NO database and always runs."""

from tests.conftest import requires_db


# ── Graceful degradation -- always runs, no DB needed ───────────────────────

class TestDisabledIsANoOp:
    def test_every_function_is_a_safe_noop_when_database_url_is_empty(self, monkeypatch):
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "")
        from persistence import db
        db.dispose()
        from persistence import run_store

        assert db.enabled() is False
        # None of these may raise, regardless of arguments.
        assert run_store.create_run("r1", "prompt", "outputs/r1") is None
        assert run_store.claim_run("r1") is False
        assert run_store.set_status("r1", "running") is None
        assert run_store.heartbeat("r1") is None
        assert run_store.record_stage_event("r1", "s0", "start") is None
        assert run_store.save_pause_state("r1", "after_fulltext", {}) is None
        assert run_store.load_pause_state("r1", "after_fulltext") is None
        assert run_store.persist_snapshot("r1", {}) is None
        assert run_store.finish_run("r1") is None
        assert run_store.fail_run("r1", "boom") is None
        assert run_store.get_run("r1") is None
        assert run_store.list_runs() == []
        assert run_store.metrics() == {}
        assert run_store.record_pdf_extraction_event("sha", "key", True) is None
        assert run_store.sweep_stale_runs(stale_seconds=1, queue_timeout_seconds=1) == \
            {"failed_running": 0, "failed_queued": 0}

    def test_db_error_degrades_instead_of_raising(self, monkeypatch):
        """A configured-but-unreachable database must also degrade
        gracefully -- @safe catches the exception, not just the
        enabled()==False branch."""
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "postgresql://nobody:nobody@127.0.0.1:1/nonexistent")
        from persistence import db
        db.dispose()
        from persistence import run_store

        assert db.enabled() is True  # configured...
        # ...but every call still degrades to a safe default, never raises.
        assert run_store.create_run("r1", "prompt", "outputs/r1") is None
        assert run_store.get_run("r1") is None
        assert run_store.list_runs() == []
        db.dispose()


# ── Real Postgres behavior ───────────────────────────────────────────────────

@requires_db
class TestRunLifecycle:
    def test_create_then_get_round_trips(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "does X help Y?", "outputs/r1", mode="manual", source="api")
        row = run_store.get_run("r1")
        assert row["run_id"] == "r1"
        assert row["status"] == "queued"
        assert row["prompt"] == "does X help Y?"
        assert row["mode"] == "manual"

    def test_claim_run_succeeds_once_and_only_once(self, pg_db):
        """The core anti-duplicate-execution guard -- see run_store.claim_run's
        docstring and the plan's Celery acks_late=False design."""
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        assert run_store.claim_run("r1") is True
        assert run_store.get_run("r1")["status"] == "running"
        assert run_store.get_run("r1")["attempt"] == 1

        # A duplicate delivery / accidental double-submit must NOT re-claim.
        assert run_store.claim_run("r1") is False
        assert run_store.get_run("r1")["attempt"] == 1

    def test_claim_run_can_reclaim_a_retried_run(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        run_store.fail_run("r1", "worker lost")
        run_store.set_status("r1", "queued")  # simulate an explicit /retry
        assert run_store.claim_run("r1") is True
        assert run_store.get_run("r1")["attempt"] == 2

    def test_finish_run_stores_results_json(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        run_store.finish_run("r1", results_json={"pooled_g": 0.5, "k": 3})
        row = run_store.get_run("r1")
        assert row["status"] == "completed"
        assert row["finished_at"] is not None
        assert row["results_json"] == {"pooled_g": 0.5, "k": 3}

    def test_fail_run_records_stage_and_traceback(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        run_store.fail_run("r1", "boom", error_traceback="Traceback...", failure_stage="s4")
        row = run_store.get_run("r1")
        assert row["status"] == "failed"
        assert row["error_message"] == "boom"
        assert row["failure_stage"] == "s4"


@requires_db
class TestPauseResume:
    def test_save_and_load_pause_state_round_trips(self, pg_db):
        from models import MetaAnalysisPlan
        from persistence import run_store

        run_store.create_run("r1", "p", "outputs/r1", mode="search")
        plan = MetaAnalysisPlan(
            research_question="q", treatment_label="t", control_label="c",
            outcome_description="o", positive_direction="p", search_queries=[],
            inclusion_criteria=[], exclusion_criteria=[], moderators_to_extract=[],
        )
        run_store.save_pause_state("r1", "after_fulltext", {"plan": plan, "n_search_retrieved": 10})
        loaded = run_store.load_pause_state("r1", "after_fulltext")
        assert loaded["plan"] == plan
        assert loaded["n_search_retrieved"] == 10

    def test_save_pause_state_upserts_not_duplicates(self, pg_db):
        from persistence import run_store, db
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.save_pause_state("r1", "after_fulltext", {"user_prompt": "v1"})
        run_store.save_pause_state("r1", "after_fulltext", {"user_prompt": "v2"})
        loaded = run_store.load_pause_state("r1", "after_fulltext")
        assert loaded["user_prompt"] == "v2"

        from persistence.schema import run_pause_states
        with db.connection() as conn:
            count = conn.execute(
                run_pause_states.select().where(run_pause_states.c.run_id == "r1")
            ).mappings().all()
        assert len(count) == 1  # upsert, not a second row

    def test_load_pause_state_missing_returns_none(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        assert run_store.load_pause_state("r1", "after_fulltext") is None


@requires_db
class TestSnapshot:
    def test_persist_snapshot_is_idempotent(self, pg_db):
        """Calling it twice with the same graph_state must produce the same
        rows, not duplicates -- see run_store.persist_snapshot's docstring."""
        from models import PaperRecord
        from persistence import run_store, db
        from persistence.schema import run_papers

        run_store.create_run("r1", "p", "outputs/r1")
        paper = PaperRecord(id="p1", title="T", abstract="A", authors=[], year=2020, source="pubmed")
        state = {"papers_eligible": [paper], "effect_sizes": [], "meta_results": [],
                 "moderator_results": [], "rob_assessments": [], "validation_flags": []}

        run_store.persist_snapshot("r1", state)
        run_store.persist_snapshot("r1", state)  # same state again

        with db.connection() as conn:
            rows = conn.execute(run_papers.select().where(run_papers.c.run_id == "r1")).mappings().all()
        assert len(rows) == 1  # not 2

    def test_persist_snapshot_updates_run_summary_counts(self, pg_db):
        from models import PaperRecord
        from persistence import run_store

        run_store.create_run("r1", "p", "outputs/r1")
        papers = [PaperRecord(id=f"p{i}", title="T", abstract="A", authors=[], year=2020, source="pubmed")
                  for i in range(3)]
        run_store.persist_snapshot("r1", {"papers_eligible": papers})
        row = run_store.get_run("r1")
        assert row["n_papers_eligible"] == 3


@requires_db
class TestReads:
    def test_list_runs_filters_by_status(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.create_run("r2", "p", "outputs/r2")
        run_store.claim_run("r2")
        queued = run_store.list_runs(status="queued")
        running = run_store.list_runs(status="running")
        assert {r["run_id"] for r in queued} == {"r1"}
        assert {r["run_id"] for r in running} == {"r2"}

    def test_list_runs_filters_by_external_ref(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1", external_ref="CD008986")
        run_store.create_run("r2", "p", "outputs/r2", external_ref="CD015331")
        rows = run_store.list_runs(external_ref="CD008986")
        assert {r["run_id"] for r in rows} == {"r1"}

    def test_latest_run_for_session(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1", session_id="sess-1")
        run_store.create_run("r2", "p", "outputs/r2", session_id="sess-1")
        latest = run_store.latest_run_for_session("sess-1")
        assert latest["run_id"] == "r2"  # created later

    def test_metrics_aggregates_status_and_pdf_cache(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        run_store.finish_run("r1")
        run_store.record_pdf_extraction_event("sha1", "key1", True, run_id="r1")
        run_store.record_pdf_extraction_event("sha2", "key2", False, run_id="r1")

        m = run_store.metrics()
        assert m["runs"]["total"] == 1
        assert m["runs"]["by_status"]["completed"] == 1
        assert m["pdf_cache"]["hits"] == 1
        assert m["pdf_cache"]["misses"] == 1
        assert m["pdf_cache"]["hit_rate"] == 0.5


@requires_db
class TestStaleSweep:
    def test_sweep_marks_stale_running_as_failed(self, pg_db):
        import datetime as dt
        from persistence import run_store, db
        from persistence.schema import runs

        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        # Force a stale heartbeat directly (simulating a worker that died
        # without ever updating it again).
        stale = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=9999)
        with db.connection() as conn:
            conn.execute(runs.update().where(runs.c.run_id == "r1").values(
                heartbeat_at=stale, current_stage="s4"))

        result = run_store.sweep_stale_runs(stale_seconds=60, queue_timeout_seconds=99999)
        assert result["failed_running"] == 1
        row = run_store.get_run("r1")
        assert row["status"] == "failed"
        assert row["failure_stage"] == "s4"

    def test_sweep_does_not_touch_completed_runs(self, pg_db):
        from persistence import run_store
        run_store.create_run("r1", "p", "outputs/r1")
        run_store.claim_run("r1")
        run_store.finish_run("r1")
        run_store.sweep_stale_runs(stale_seconds=0, queue_timeout_seconds=0)
        assert run_store.get_run("r1")["status"] == "completed"

    def test_sweep_marks_stale_queued_as_failed(self, pg_db):
        import datetime as dt
        from persistence import run_store, db
        from persistence.schema import runs

        run_store.create_run("r1", "p", "outputs/r1")
        stale = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=9999)
        with db.connection() as conn:
            conn.execute(runs.update().where(runs.c.run_id == "r1").values(created_at=stale))

        result = run_store.sweep_stale_runs(stale_seconds=99999, queue_timeout_seconds=60)
        assert result["failed_queued"] == 1
        assert run_store.get_run("r1")["status"] == "failed"


@requires_db
class TestArtifacts:
    def test_record_artifact_upserts_on_relative_path(self, pg_db):
        from persistence import run_store, db
        from persistence.schema import run_artifacts

        run_store.create_run("r1", "p", "outputs/r1")
        run_store.record_artifact("r1", "plan.json", "plan.json", kind="json", size_bytes=100)
        run_store.record_artifact("r1", "plan.json", "plan.json", kind="json", size_bytes=200)

        with db.connection() as conn:
            rows = conn.execute(
                run_artifacts.select().where(run_artifacts.c.run_id == "r1")
            ).mappings().all()
        assert len(rows) == 1
        assert rows[0]["size_bytes"] == 200
