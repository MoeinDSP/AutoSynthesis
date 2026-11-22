"""Full search-mode workflow through dashboard.py's real FastAPI app,
covering BOTH pause branches: the fulltext-upload pause (some papers'
full text couldn't be auto-retrieved) and the no-missing-fulltext branch
(skips straight through to the paper-tracking review pause) -- with
MetaAnalysisOrchestrator stubbed, same convention as
test_manual_upload_workflow.py.
"""

import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401
import dashboard
from models import PaperRecord


def _paper(pid="p1", **kwargs):
    defaults = dict(id=pid, title=f"Title {pid}", abstract="A", authors=["X"],
                     year=2020, source="pubmed")
    defaults.update(kwargs)
    return PaperRecord(**defaults)


def _wait_until(client: TestClient, predicate, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get("/status").json()
        if predicate(last):
            return last
        time.sleep(0.05)
    raise AssertionError(f"condition not met within {timeout}s -- last /status: {last}")


class TestNoMissingFulltextBranch:
    """papers_no_fulltext is empty -- the pipeline must skip the fulltext
    pause entirely and go straight to the paper-tracking-review pause, with
    no dialog shown to the user (today's exact behavior, unchanged)."""

    def test_skips_straight_to_awaiting_review(self, monkeypatch):
        import orchestrator as orchestrator_module

        mock_orch = MagicMock()
        mock_orch.run_until_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 10,
            "papers_eligible": [_paper("p1"), _paper("p2")],
        }
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 10,
            "papers_eligible": [_paper("p1"), _paper("p2")],
        }
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        client = TestClient(dashboard.app)
        resp = client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})
        assert resp.json()["ok"] is True

        final = _wait_until(client, lambda s: s["awaiting_review"] or s["done"])
        assert final["awaiting_review"] is True
        assert final["status"] == "awaiting_review"
        assert final["awaiting_fulltext_upload"] is False
        mock_orch.continue_after_fulltext_review.assert_called_once()


class TestMissingFulltextBranch:
    """papers_no_fulltext is non-empty -- must pause for the fulltext-upload
    dialog, then (via /upload_missing_fulltext) continue to the
    paper-tracking-review pause."""

    def test_pauses_for_fulltext_upload_then_review(self, monkeypatch):
        import orchestrator as orchestrator_module

        mock_orch = MagicMock()
        mock_orch.run_until_fulltext_review.return_value = {
            "papers_no_fulltext": ["p1"],
            "papers_no_fulltext_reasons": {"p1": "no open-access copy found"},
            "all_retrieved_papers": [_paper("p1")],
            "n_search_retrieved": 10,
        }
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 10,
            "papers_eligible": [_paper("p1")],
        }
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))
        monkeypatch.setattr("agents.paper_reading_agent.ingest_uploaded_fulltext_pdfs",
                             lambda *a, **k: ([], []))

        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})

        paused = _wait_until(client, lambda s: s["awaiting_fulltext_upload"] or s["done"])
        assert paused["awaiting_fulltext_upload"] is True
        assert paused["status"] == "awaiting_fulltext_upload"

        missing = client.get("/missing_fulltext").json()
        assert missing["ok"] is True
        assert missing["total_rows"] == 1
        assert missing["rows"][0]["reason"] == "no open-access copy found"

        # "Continue Without Uploading" -- empty files list.
        resp = client.post("/upload_missing_fulltext")
        assert resp.json()["ok"] is True

        final = _wait_until(client, lambda s: s["awaiting_review"] or s["done"])
        assert final["awaiting_review"] is True
        assert final["status"] == "awaiting_review"
        mock_orch.continue_after_fulltext_review.assert_called_once()


class TestPaperTrackingReviewApproval:
    def test_continue_pipeline_completes_the_run(self, monkeypatch, tmp_path):
        import orchestrator as orchestrator_module
        from models import PipelineState

        mock_orch = MagicMock()
        mock_orch.run_until_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 5,
            "papers_eligible": [_paper("p1")],
        }
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 5,
            "papers_eligible": [_paper("p1")],
        }
        mock_orch.continue_after_review.return_value = PipelineState()
        mock_orch.last_graph_state = {"effect_sizes": []}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})
        _wait_until(client, lambda s: s["awaiting_review"] or s["done"])

        resp = client.post("/continue_pipeline")
        assert resp.json()["ok"] is True
        final = _wait_until(client, lambda s: s["done"])
        assert final["status"] == "completed"
        mock_orch.continue_after_review.assert_called_once()

    def test_continue_pipeline_without_a_pending_review_is_rejected(self):
        client = TestClient(dashboard.app)
        resp = client.post("/continue_pipeline")
        assert resp.json()["ok"] is False
