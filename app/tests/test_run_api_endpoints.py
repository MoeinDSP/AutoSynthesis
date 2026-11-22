"""Phase 3's new run_id-addressed read API (api_runs.py, mounted under
/api/*) plus /api/health's degradation reporting.

Split into two groups:
  - DB-independent shape tests (persistence disabled -- the default): every
    endpoint must degrade gracefully (empty list / not-found / "disabled"),
    never raise, matching the "app runs exactly as today with zero infra"
    guarantee documented in the migration plan.
  - requires_db-gated tests: real Postgres round-trip -- create_run/
    finish_run/record_stage_event via run_store, then read the same data
    back through the HTTP API.
"""

import uuid

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401 -- import ordering, see other test files
import dashboard
from tests.conftest import requires_db


@pytest.fixture
def client():
    return TestClient(dashboard.app)


class TestHealthDegradesGracefully:
    def test_health_ok_with_all_subsystems_disabled(self, client, monkeypatch):
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "")
        monkeypatch.setattr(config, "REDIS_URL", "")
        monkeypatch.setattr(config, "CELERY_BROKER_URL", "")
        # dashboard.py reads config via its own `_config` alias -- patch that
        # module object too so the route sees the same values.
        monkeypatch.setattr(dashboard._config, "DATABASE_URL", "")
        monkeypatch.setattr(dashboard._config, "REDIS_URL", "")
        monkeypatch.setattr(dashboard._config, "CELERY_BROKER_URL", "")

        resp = client.get("/api/health")
        body = resp.json()
        assert body["ok"] is True
        assert body["db"] == "disabled"
        assert body["redis"] == "disabled"
        assert body["broker"] == "disabled"
        assert body["backend"] in ("thread", "celery")

    def test_health_reports_db_error_not_crash_when_unreachable(self, client, monkeypatch):
        monkeypatch.setattr(dashboard._config, "DATABASE_URL",
                             "postgresql://nouser:nopass@127.0.0.1:1/nodb")
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["db"] == "error"


class TestRunsListDegradesGracefully:
    def test_list_runs_empty_not_error_when_db_disabled(self, client, monkeypatch):
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "")
        resp = client.get("/api/runs")
        body = resp.json()
        assert body["ok"] is True
        assert body["runs"] == []
        assert body["total"] == 0

    def test_get_missing_run_returns_ok_false_not_500(self, client):
        resp = client.get(f"/api/runs/{uuid.uuid4().hex}")
        assert resp.status_code == 200
        assert resp.json()["ok"] is False

    def test_missing_run_status_returns_ok_false(self, client):
        resp = client.get(f"/api/runs/{uuid.uuid4().hex}/status")
        assert resp.json()["ok"] is False

    def test_missing_run_results_returns_ok_false(self, client):
        resp = client.get(f"/api/runs/{uuid.uuid4().hex}/results")
        assert resp.json()["ok"] is False

    def test_missing_run_results_flat_mode_still_reports_not_found(self, client):
        # flat=True only changes the shape of a FOUND run's results (bare
        # dict instead of the {"ok",...} wrapper) -- a missing run_id still
        # gets the standard not-found envelope either way.
        resp = client.get(f"/api/runs/{uuid.uuid4().hex}/results?flat=true")
        assert resp.json()["ok"] is False

    def test_missing_run_events_returns_empty_list(self, client):
        resp = client.get(f"/api/runs/{uuid.uuid4().hex}/events")
        body = resp.json()
        assert body["ok"] is True
        assert body["events"] == []

    def test_metrics_never_raises_when_db_disabled(self, client, monkeypatch):
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "")
        resp = client.get("/api/metrics")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True


@requires_db
class TestRunsRoundTripAgainstRealPostgres(object):
    def _run_id(self):
        return "test_" + uuid.uuid4().hex[:12]

    def test_created_run_appears_in_list_and_get(self, pg_db):
        from persistence import run_store
        run_id = self._run_id()
        run_store.create_run(run_id, "does X help Y?", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s1")
        run_store.claim_run(run_id)
        run_store.record_stage_event(run_id, "s0", "start")
        run_store.record_stage_event(run_id, "s1", "start")
        run_store.finish_run(run_id, results_json={
            "pooled_g": 0.5, "ci_lower": 0.1, "ci_upper": 0.9, "p_value": 0.01,
            "i_squared": 10.0, "tau": 0.05, "k": 3, "measure_label": "SMD",
        })

        client = TestClient(dashboard.app)

        got = client.get(f"/api/runs/{run_id}").json()
        assert got["ok"] is True
        assert got["run"]["run_id"] == run_id
        assert got["run"]["status"] == "completed"

        status_resp = client.get(f"/api/runs/{run_id}/status").json()
        assert status_resp["status"] == "completed"
        assert status_resp["done"] is True
        assert status_resp["running"] is False

        results_resp = client.get(f"/api/runs/{run_id}/results").json()
        assert results_resp["results"]["pooled_g"] == 0.5

        flat = client.get(f"/api/runs/{run_id}/results?flat=true").json()
        assert flat["pooled_g"] == 0.5
        assert "ok" not in flat  # bare legacy dict, not the wrapped shape

        events = client.get(f"/api/runs/{run_id}/events").json()
        assert events["ok"] is True
        assert [e["stage_id"] for e in events["events"]] == ["s0", "s1"]

        listing = client.get("/api/runs", params={"mode": "manual", "limit": 500}).json()
        matching = [r for r in listing["runs"] if r["run_id"] == run_id]
        assert len(matching) == 1
        assert matching[0]["pooled_effect"] == 0.5
        assert matching[0]["k"] == 3

    def test_list_runs_filters_by_status(self, pg_db):
        from persistence import run_store
        run_id = self._run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s2")
        run_store.claim_run(run_id)
        run_store.fail_run(run_id, "boom", failure_stage="s4")

        client = TestClient(dashboard.app)
        failed = client.get("/api/runs", params={"status": "failed", "limit": 500}).json()
        assert any(r["run_id"] == run_id for r in failed["runs"])
        completed = client.get("/api/runs", params={"status": "completed", "limit": 500}).json()
        assert not any(r["run_id"] == run_id for r in completed["runs"])

    def test_health_reports_db_ok_against_real_postgres(self, pg_db):
        client = TestClient(dashboard.app)
        resp = client.get("/api/health")
        assert resp.json()["db"] == "ok"

    def test_metrics_reflects_real_data(self, pg_db):
        from persistence import run_store
        run_id = self._run_id()
        run_store.create_run(run_id, "q", "/tmp/out", mode="manual",
                              source="dashboard", session_id="s3")
        client = TestClient(dashboard.app)
        resp = client.get("/api/metrics")
        assert resp.json()["ok"] is True
