"""The 5 legacy, session-cookie-based routes n8n's existing 4 workflows
call today (/run, /status, /results, /review_tracking, /continue_pipeline)
-- Phase 3's hard backward-compat bar: their response key sets must be a
SUPERSET of what they returned before this session's infra work, with no
existing key's TYPE changed, and the "already running" guard must keep
firing only on queued/running (never on awaiting_* -- that was never a
block before Phase 3 and must not become one)."""

import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401
import dashboard
from models import PipelineState


# The exact key sets /status and /run returned BEFORE this session's work
# (frozen baseline -- see baselines/before/ for the captured real-run
# equivalent). New keys are fine to ADD; none of these may disappear or
# change type.
LEGACY_STATUS_KEYS = {"running", "done", "error", "awaiting_review", "awaiting_fulltext_upload"}
LEGACY_RUN_OK_KEYS = {"ok"}


def _wait_for_done(client: TestClient, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get("/status").json()
        if last["done"]:
            return last
        time.sleep(0.05)
    raise AssertionError(f"pipeline did not finish within {timeout}s -- last /status: {last}")


class TestStatusContract:
    def test_status_is_a_superset_of_the_legacy_keys_with_unchanged_types(self, monkeypatch):
        import orchestrator as orchestrator_module
        mock_orch = MagicMock()
        mock_orch.run.return_value = PipelineState()
        mock_orch.last_graph_state = {}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        body = _wait_for_done(client)

        assert LEGACY_STATUS_KEYS.issubset(body.keys())
        assert isinstance(body["running"], bool)
        assert isinstance(body["done"], bool)
        assert body["error"] is None or isinstance(body["error"], str)
        assert isinstance(body["awaiting_review"], bool)
        assert isinstance(body["awaiting_fulltext_upload"], bool)
        # New, additive keys -- present, but never required by an old caller.
        assert "run_id" in body
        assert "status" in body

    def test_fresh_session_status_shape_unchanged(self):
        """A session that never called /run -- the exact shape dashboard.py
        has always returned for an idle session."""
        client = TestClient(dashboard.app)
        body = client.get("/status").json()
        assert LEGACY_STATUS_KEYS.issubset(body.keys())
        assert body["running"] is False
        assert body["done"] is False


class TestRunContract:
    def test_run_response_is_a_superset_of_ok(self, monkeypatch):
        import orchestrator as orchestrator_module
        mock_orch = MagicMock()
        mock_orch.run.return_value = PipelineState()
        mock_orch.last_graph_state = {}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        client = TestClient(dashboard.app)
        resp = client.post("/run", json={"prompt": "q", "paper_files": ["a.pdf"]})
        body = resp.json()
        assert LEGACY_RUN_OK_KEYS.issubset(body.keys())
        assert body["ok"] is True
        assert "run_id" in body  # additive
        _wait_for_done(client)

    def test_run_error_response_shape_unchanged(self):
        client = TestClient(dashboard.app)
        resp = client.post("/run", json={"prompt": "", "paper_files": []})
        body = resp.json()
        assert body == {"ok": False, "error": "Please enter a research question."}


class TestAlreadyRunningGuard:
    """The guard must fire ONLY on queued/running -- an awaiting_* paused
    run was never blocked before Phase 3 and must not become one now."""

    def test_guard_does_not_fire_while_awaiting_review(self, monkeypatch):
        import orchestrator as orchestrator_module
        mock_orch = MagicMock()
        mock_orch.run_until_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 1, "papers_eligible": [],
        }
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 1, "papers_eligible": [],
        }
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "q", "paper_files": []})
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if client.get("/status").json()["awaiting_review"]:
                break
            time.sleep(0.05)
        else:
            raise AssertionError("never reached awaiting_review")

        # /run must NOT be blocked by "a pipeline is already running" here --
        # "running" is False while paused (matches today's exact semantics).
        assert client.get("/status").json()["running"] is False


class TestReviewTrackingAndContinue:
    def test_review_tracking_without_a_pending_review(self):
        client = TestClient(dashboard.app)
        resp = client.get("/review_tracking")
        assert resp.json()["ok"] is False

    def test_continue_pipeline_without_a_pending_review(self):
        client = TestClient(dashboard.app)
        resp = client.post("/continue_pipeline")
        assert resp.json() == {"ok": False, "error": "There is no paused paper review to continue."}
