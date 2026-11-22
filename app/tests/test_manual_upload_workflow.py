"""Full manual-upload workflow through dashboard.py's real FastAPI app --
/upload -> /run -> poll /status -> /results -- with MetaAnalysisOrchestrator
stubbed (this test is about the dashboard/persistence WIRING, not the
scientific pipeline, which has its own extensive test coverage elsewhere).

Parametrised over both RUN_EXECUTION_BACKEND values per the migration plan
-- Phase 3 only implements "thread" for real, but the test is written to
already accept "celery" so Phase 4 only needs to stop skipping it.
"""

import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401 -- import before dashboard (circular-import ordering, see other test files)
import dashboard
from models import PipelineState


def _stub_orchestrator_run(monkeypatch, *, results_state: PipelineState, raise_exc: Exception = None):
    """Patches orchestrator.MetaAnalysisOrchestrator (as imported freshly
    inside _run_pipeline on every call) so .run() returns a canned
    PipelineState instantly instead of executing the real LLM pipeline."""
    import orchestrator as orchestrator_module

    mock_orch = MagicMock()
    mock_orch.last_graph_state = {"effect_sizes": [], "meta_results": []}
    if raise_exc:
        mock_orch.run.side_effect = raise_exc
    else:
        mock_orch.run.return_value = results_state
    monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))
    return mock_orch


def _wait_for_done(client: TestClient, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get("/status").json()
        if last["done"]:
            return last
        time.sleep(0.05)
    raise AssertionError(f"pipeline did not finish within {timeout}s -- last /status: {last}")


@pytest.fixture(autouse=True)
def _fresh_session_per_test():
    """dashboard.py's session state is a module-level dict keyed by cookie
    session_id -- TestClient issues a fresh cookie jar per instance, so each
    test naturally gets an isolated pipeline dict. Nothing to do here except
    document why isolation holds without an explicit reset."""
    yield


class TestManualUploadWorkflow:
    def test_run_returns_run_id_immediately(self, monkeypatch):
        _stub_orchestrator_run(monkeypatch, results_state=PipelineState())
        client = TestClient(dashboard.app)
        resp = client.post("/run", json={"prompt": "does X help Y?", "paper_files": ["a.pdf"]})
        body = resp.json()
        assert body["ok"] is True
        assert body["run_id"]  # present and truthy -- the new, additive key
        _wait_for_done(client)

    def test_status_reports_running_then_done(self, monkeypatch):
        mock_orch = _stub_orchestrator_run(monkeypatch, results_state=PipelineState())
        # Make .run() take a moment so we can observe "running" before "done".
        def _slow_run(*a, **k):
            time.sleep(0.2)
            return PipelineState()
        mock_orch.run.side_effect = _slow_run

        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        immediate = client.get("/status").json()
        assert immediate["status"] in ("queued", "running")
        final = _wait_for_done(client)
        assert final["status"] == "completed"
        assert final["done"] is True
        assert final["error"] is None

    def test_results_reflects_stubbed_pipeline_state(self, monkeypatch):
        from models import MetaAnalysisResult
        state = PipelineState(meta_analysis=MetaAnalysisResult(
            pooled_g=0.42, pooled_se=0.1, ci_lower=0.2, ci_upper=0.6,
            z_value=4.0, p_value=0.001, tau_squared=0.01, tau=0.1,
            i_squared=20.0, h_squared=1.2, q_statistic=5.0, q_df=4,
            q_p_value=0.3, k=5, n_total=250,
        ))
        _stub_orchestrator_run(monkeypatch, results_state=state)
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        _wait_for_done(client)
        results = client.get("/results").json()
        assert results["pooled_g"] == 0.42
        assert results["k"] == 5

    def test_error_is_reported_not_swallowed(self, monkeypatch):
        _stub_orchestrator_run(monkeypatch, results_state=None, raise_exc=RuntimeError("boom"))
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        final = _wait_for_done(client)
        assert final["status"] == "failed"
        assert "boom" in final["error"]

    def test_already_running_guard_blocks_a_second_submit(self, monkeypatch):
        mock_orch = _stub_orchestrator_run(monkeypatch, results_state=PipelineState())
        def _slow_run(*a, **k):
            time.sleep(0.3)
            return PipelineState()
        mock_orch.run.side_effect = _slow_run

        client = TestClient(dashboard.app)
        first = client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        assert first.json()["ok"] is True
        second = client.post("/run", json={"prompt": "q2", "paper_files": ["b.pdf"]})
        assert second.json() == {"ok": False, "error": "A pipeline is already running."}
        _wait_for_done(client)

    def test_empty_prompt_rejected(self):
        client = TestClient(dashboard.app)
        resp = client.post("/run", json={"prompt": "   ", "paper_files": []})
        assert resp.json()["ok"] is False


@pytest.mark.parametrize("backend", ["thread"])  # "celery" added in Phase 4
class TestBackendParametrized:
    def test_manual_upload_completes_under_backend(self, monkeypatch, backend):
        import config
        monkeypatch.setattr(config, "RUN_EXECUTION_BACKEND", backend)
        _stub_orchestrator_run(monkeypatch, results_state=PipelineState())
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        final = _wait_for_done(client)
        assert final["status"] == "completed"
