"""Paper-selection gate right after the search agent: the user can decline
found papers and add further PDFs before full-text retrieval.

Covers the pure selection logic (agents.paper_reading_agent.apply_paper_selection),
the graph wiring, and the full dashboard flow with MetaAnalysisOrchestrator
stubbed (same convention as test_search_mode_workflow.py)."""

import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph
import dashboard
from models import PaperRecord


def _paper(pid="p1", **kwargs):
    defaults = dict(id=pid, title=f"Title {pid}", abstract="A", authors=["X"],
                     year=2020, source="pubmed")
    defaults.update(kwargs)
    return PaperRecord(**defaults)


def _wait_until(client, predicate, timeout=10.0):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get("/status").json()
        if predicate(last):
            return last
        time.sleep(0.05)
    raise AssertionError(f"condition not met within {timeout}s -- last /status: {last}")


class TestGraphWiring:
    def test_graphs_compile(self):
        pipeline_graph.build_graph(stop_after_search=True)
        pipeline_graph.build_post_search_graph()
        pipeline_graph.build_graph()  # default wiring unchanged


class TestApplyPaperSelection:
    def _state(self):
        papers = [_paper("p1"), _paper("p2"), _paper("p3")]
        return {
            "papers_eligible": list(papers),
            "all_retrieved_papers": list(papers),
            "screening_decisions": {},
            "n_screened_excluded": 4,
        }

    def test_declined_papers_leave_the_pipeline_and_are_tracked(self, tmp_path):
        from agents.paper_reading_agent import apply_paper_selection, USER_DECLINED_REASON

        state, summary = apply_paper_selection(self._state(), ["p2"], [], str(tmp_path))
        assert [p.id for p in state["papers_eligible"]] == ["p1", "p3"]
        assert state["screening_decisions"]["p2"]["decision"] == "exclude"
        assert state["screening_decisions"]["p2"]["reason"] == USER_DECLINED_REASON
        assert state["n_screened_excluded"] == 5
        # still in the retrieved snapshot, so paper_tracking.csv lists it
        assert "p2" in [p.id for p in state["all_retrieved_papers"]]
        assert summary == {"declined": 1, "added": 0, "attached": 0, "unreadable": 0}

    def test_new_pdf_is_added_as_manual_paper_with_full_text(self, tmp_path, monkeypatch):
        import agents.paper_reading_agent as pra

        pdf = tmp_path / "ab12cd34_My Extra Trial.pdf"
        pdf.write_bytes(b"%PDF-1.4")
        monkeypatch.setattr(pra, "_extract_text_from_path", lambda path: "Completely different text about trial Z.")
        state, summary = pra.apply_paper_selection(self._state(), [], [str(pdf)], str(tmp_path))

        manual = [p for p in state["papers_eligible"] if p.source == "manual"]
        assert len(manual) == 1
        assert manual[0].title == "My Extra Trial"
        assert manual[0].full_text and manual[0].id.startswith("manual:")
        assert manual[0].id in [p.id for p in state["all_retrieved_papers"]]
        assert state["screening_decisions"][manual[0].id]["decision"] == "include"
        assert len(state["papers_eligible"]) == 4
        assert summary["added"] == 1

    def test_pdf_matching_a_found_paper_is_attached_not_duplicated(self, tmp_path, monkeypatch):
        import agents.paper_reading_agent as pra

        pdf = tmp_path / "x.pdf"
        pdf.write_bytes(b"%PDF-1.4")
        monkeypatch.setattr(pra, "_extract_text_from_path",
                            lambda path: "Title p1\n\nAbstract. Doi 10.1000/abc ...")
        state, summary = pra.apply_paper_selection(self._state(), [], [str(pdf)], str(tmp_path))
        assert len(state["papers_eligible"]) == 3
        by_id = {p.id: p for p in state["papers_eligible"]}
        assert by_id["p1"].full_text
        assert summary["attached"] == 1 and summary["added"] == 0

    def test_unreadable_pdf_is_skipped(self, tmp_path, monkeypatch):
        import agents.paper_reading_agent as pra

        pdf = tmp_path / "scan.pdf"
        pdf.write_bytes(b"%PDF-1.4")
        monkeypatch.setattr(pra, "_extract_text_from_path", lambda path: "   ")
        state, summary = pra.apply_paper_selection(self._state(), [], [str(pdf)], str(tmp_path))
        assert len(state["papers_eligible"]) == 3
        assert summary["unreadable"] == 1


@pytest.fixture
def gate_on(monkeypatch):
    import config
    monkeypatch.setattr(config, "PAPER_SELECTION_GATE", True)


class TestDashboardFlow:
    def _orch(self, monkeypatch):
        import orchestrator as orchestrator_module

        mock_orch = MagicMock()
        mock_orch.run_until_search_review.return_value = {
            "papers_eligible": [_paper("p1"), _paper("p2")], "n_search_retrieved": 2,
        }
        mock_orch.continue_after_search_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 2, "papers_eligible": [_paper("p1")],
        }
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 2, "papers_eligible": [_paper("p1")],
        }
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))
        return mock_orch

    def test_pauses_after_search_then_continues_with_selection(self, gate_on, monkeypatch):
        mock_orch = self._orch(monkeypatch)
        client = TestClient(dashboard.app)
        assert client.post("/run", json={"prompt": "does X help Y?", "paper_files": []}).json()["ok"]

        paused = _wait_until(client, lambda s: s["awaiting_paper_selection"] or s["done"])
        assert paused["awaiting_paper_selection"] is True
        assert paused["status"] == "awaiting_paper_selection"
        mock_orch.run_until_fulltext_review.assert_not_called()

        found = client.get("/found_papers").json()
        assert found["ok"] and found["total_rows"] == 2
        assert {r["id"] for r in found["rows"]} == {"p1", "p2"}

        resp = client.post("/submit_paper_selection", data={"excluded_ids": '["p2"]'})
        assert resp.json()["ok"] is True
        final = _wait_until(client, lambda s: s["awaiting_review"] or s["done"])
        assert final["awaiting_review"] is True
        assert final["awaiting_paper_selection"] is False
        kwargs = mock_orch.continue_after_search_review.call_args.kwargs
        assert kwargs["excluded_ids"] == ["p2"]
        assert kwargs["pdf_paths"] == []

    def test_uploaded_pdfs_are_passed_through(self, gate_on, monkeypatch):
        mock_orch = self._orch(monkeypatch)
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})
        _wait_until(client, lambda s: s["awaiting_paper_selection"] or s["done"])

        resp = client.post("/submit_paper_selection", data={"excluded_ids": "[]"},
                           files=[("files", ("extra.pdf", b"%PDF-1.4", "application/pdf")),
                                  ("files", ("notes.txt", b"ignored", "text/plain"))])
        assert resp.json()["ok"] is True
        _wait_until(client, lambda s: s["awaiting_review"] or s["done"])
        pdf_paths = mock_orch.continue_after_search_review.call_args.kwargs["pdf_paths"]
        assert len(pdf_paths) == 1 and pdf_paths[0].endswith("extra.pdf")

    def test_declining_everything_without_adding_a_pdf_is_rejected(self, gate_on, monkeypatch):
        mock_orch = self._orch(monkeypatch)
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})
        _wait_until(client, lambda s: s["awaiting_paper_selection"] or s["done"])

        resp = client.post("/submit_paper_selection", data={"excluded_ids": '["p1", "p2"]'}).json()
        assert resp["ok"] is False
        assert "at least one" in resp["error"]
        mock_orch.continue_after_search_review.assert_not_called()
        # still paused
        assert client.get("/status").json()["awaiting_paper_selection"] is True

    def test_submit_without_pending_selection_is_rejected(self):
        client = TestClient(dashboard.app)
        resp = client.post("/submit_paper_selection", data={"excluded_ids": "[]"}).json()
        assert resp["ok"] is False

    def test_gate_off_keeps_the_original_flow(self, monkeypatch):
        import orchestrator as orchestrator_module
        mock_orch = MagicMock()
        mock_orch.run_until_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 1, "papers_eligible": [_paper("p1")]}
        mock_orch.continue_after_fulltext_review.return_value = {
            "papers_no_fulltext": [], "n_search_retrieved": 1, "papers_eligible": [_paper("p1")]}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))
        client = TestClient(dashboard.app)
        client.post("/run", json={"prompt": "does X help Y?", "paper_files": []})
        final = _wait_until(client, lambda s: s["awaiting_review"] or s["done"])
        assert final["awaiting_review"] is True
        mock_orch.run_until_search_review.assert_not_called()
