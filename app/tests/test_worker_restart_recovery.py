"""Phase 4's worker-crash-recovery mechanics: sweep_stale_runs() (built
ahead of need in Phase 1, wired to real routes in Phase 4) reclaiming a
run whose worker died mid-execution, and POST /api/runs/{id}/retry
re-dispatching it with attempt=2. Requires real Postgres -- these are
conditional-UPDATE race/timing semantics that a mock can't meaningfully
stand in for.
"""

import datetime as dt
import uuid
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401 -- import ordering, see other test files
import dashboard
from tests.conftest import requires_db


def _run_id():
    return "recovery_test_" + uuid.uuid4().hex[:12]


@requires_db
class TestStaleRunSweep:
    def test_running_row_with_dead_heartbeat_is_marked_failed(self, pg_db):
        from persistence import run_store, schema as sc, db

        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s1")
        run_store.claim_run(run_id)
        # Simulate a worker that died a long time ago: backdate heartbeat_at
        # directly (run_store has no "set heartbeat to the past" helper by
        # design -- only sweep_stale_runs and the real heartbeat loop touch
        # this column in production).
        stale_at = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)
        with db.connection() as conn:
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id)
                         .values(heartbeat_at=stale_at))

        result = run_store.sweep_stale_runs(stale_seconds=60, queue_timeout_seconds=3600)
        assert result["failed_running"] >= 1

        row = run_store.get_run(run_id)
        assert row["status"] == "failed"
        assert row["error_message"] == "worker lost (no heartbeat)"

    def test_running_row_with_fresh_heartbeat_is_left_alone(self, pg_db):
        from persistence import run_store

        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s2")
        run_store.claim_run(run_id)
        run_store.heartbeat(run_id)

        run_store.sweep_stale_runs(stale_seconds=1800, queue_timeout_seconds=3600)
        row = run_store.get_run(run_id)
        assert row["status"] == "running"

    def test_completed_runs_are_never_swept(self, pg_db):
        from persistence import run_store, schema as sc, db

        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s3")
        run_store.claim_run(run_id)
        run_store.finish_run(run_id, results_json={"pooled_g": 0.1})
        stale_at = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)
        with db.connection() as conn:
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id)
                         .values(heartbeat_at=stale_at))

        run_store.sweep_stale_runs(stale_seconds=60, queue_timeout_seconds=3600)
        row = run_store.get_run(run_id)
        assert row["status"] == "completed"  # untouched -- only `running`/`queued` are swept

    def test_queued_row_past_timeout_is_marked_failed(self, pg_db):
        from persistence import run_store, schema as sc, db

        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s4")
        old_created = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)
        with db.connection() as conn:
            conn.execute(sc.runs.update().where(sc.runs.c.run_id == run_id)
                         .values(created_at=old_created))

        result = run_store.sweep_stale_runs(stale_seconds=1800, queue_timeout_seconds=60)
        assert result["failed_queued"] >= 1
        row = run_store.get_run(run_id)
        assert row["status"] == "failed"
        assert "timed out" in row["error_message"]


@requires_db
class TestRetryEndpoint:
    def test_retry_requires_failed_status(self, pg_db):
        from persistence import run_store
        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual", source="dashboard")
        client = TestClient(dashboard.app)
        resp = client.post(f"/api/runs/{run_id}/retry")
        assert resp.json()["ok"] is False

    def test_retry_missing_run(self):
        client = TestClient(dashboard.app)
        resp = client.post(f"/api/runs/{uuid.uuid4().hex}/retry")
        assert resp.json()["ok"] is False

    def test_retry_requeues_and_second_execution_gets_attempt_two(self, pg_db, monkeypatch, tmp_path):
        from persistence import run_store
        import orchestrator as orchestrator_module
        from models import PipelineState

        mock_orch = MagicMock()
        mock_orch.run.return_value = PipelineState()
        mock_orch.last_graph_state = {"effect_sizes": []}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        run_id = _run_id()
        run_store.create_run(run_id, "q", str(tmp_path), mode="manual", source="dashboard",
                              session_id="s5", paper_files=["a.pdf"])
        run_store.claim_run(run_id)
        run_store.fail_run(run_id, "first attempt crashed")
        assert run_store.get_run(run_id)["attempt"] == 1

        client = TestClient(dashboard.app)
        resp = client.post(f"/api/runs/{run_id}/retry")
        assert resp.json()["ok"] is True

        # The retry dispatches a real threading.Thread (RUN_EXECUTION_BACKEND
        # defaults to "thread" in tests) -- give it a moment to complete
        # against the mocked (instant) orchestrator.
        import time
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            row = run_store.get_run(run_id)
            if row["status"] == "completed":
                break
            time.sleep(0.05)

        row = run_store.get_run(run_id)
        assert row["status"] == "completed"
        assert row["attempt"] == 2
        assert mock_orch.run.call_count == 1

    def test_retry_race_only_one_caller_wins(self, pg_db):
        """Two concurrent /retry calls on the same failed run: only one may
        successfully transition it (the other must report failure, not
        silently double-dispatch)."""
        from persistence import run_store
        run_id = _run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual", source="dashboard")
        run_store.claim_run(run_id)
        run_store.fail_run(run_id, "boom")

        first = run_store.retry_run(run_id)
        second = run_store.retry_run(run_id)
        assert first is True
        assert second is False
