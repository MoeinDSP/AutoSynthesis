"""Celery tasks (tasks.py) in eager mode -- runs the task body inline
(no real broker needed) against real Postgres, so these prove: (a) the
claim guard is the actual duplicate-execution mechanism (not just present
in code but never exercised), and (b) tasks.py's thin wrappers correctly
delegate to run_service's backend-agnostic execute_* functions -- the same
functions the (mocked-orchestrator) thread-backend tests already exercise
in test_manual_upload_workflow.py/test_search_mode_workflow.py.

Orchestrator is monkeypatched exactly like those files (patched on the
`orchestrator` module object, since run_service's execute_* functions do a
fresh local `from orchestrator import MetaAnalysisOrchestrator` on every
call) so no real LLM pipeline runs.
"""

import uuid
from unittest.mock import MagicMock

import pytest

import pipeline_graph  # noqa: F401 -- import ordering, see other test files
import celery_app
from tests.conftest import requires_db


@pytest.fixture(autouse=True)
def _eager_mode():
    celery_app.app.conf.task_always_eager = True
    celery_app.app.conf.task_eager_propagates = True
    yield
    celery_app.app.conf.task_always_eager = False
    celery_app.app.conf.task_eager_propagates = False


def _run_id():
    return "celery_test_" + uuid.uuid4().hex[:12]


def _stub_orchestrator(monkeypatch, *, results_state=None, raise_exc: Exception = None):
    import orchestrator as orchestrator_module
    from models import PipelineState

    mock_orch = MagicMock()
    mock_orch.last_graph_state = {"effect_sizes": []}
    if raise_exc:
        mock_orch.run.side_effect = raise_exc
    else:
        mock_orch.run.return_value = results_state or PipelineState()
    monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))
    return mock_orch


@requires_db
class TestRunPipelineTaskClaimGuard:
    def test_happy_path_claims_and_completes(self, pg_db, monkeypatch, tmp_path):
        from persistence import run_store
        from tasks import run_pipeline_task

        mock_orch = _stub_orchestrator(monkeypatch)
        run_id = _run_id()
        run_store.create_run(run_id, "q", str(tmp_path), mode="manual",
                              source="dashboard", session_id="s1", execution_backend="celery")

        run_pipeline_task.apply(args=[
            "does X help Y?", str(tmp_path), "s1", ["a.pdf"], run_id,
        ])

        assert mock_orch.run.call_count == 1
        row = run_store.get_run(run_id)
        assert row["status"] == "completed"
        assert row["attempt"] == 1

    def test_duplicate_delivery_is_skipped_not_double_executed(self, pg_db, monkeypatch, tmp_path):
        """The core anti-duplicate-execution guarantee: if a run_id has
        already transitioned out of "queued" (another delivery claimed it,
        or it already finished), a second delivery of the SAME task must
        not call the orchestrator at all."""
        from persistence import run_store
        from tasks import run_pipeline_task

        mock_orch = _stub_orchestrator(monkeypatch)
        run_id = _run_id()
        run_store.create_run(run_id, "q", str(tmp_path), mode="manual",
                              source="dashboard", session_id="s2", execution_backend="celery")
        # Simulate "another delivery already claimed this run" by claiming
        # it directly, out from under the task about to run.
        claimed = run_store.claim_run(run_id)
        assert claimed is True

        run_pipeline_task.apply(args=[
            "does X help Y?", str(tmp_path), "s2", ["a.pdf"], run_id,
        ])

        assert mock_orch.run.call_count == 0

    def test_failure_is_recorded_with_traceback(self, pg_db, monkeypatch, tmp_path):
        from persistence import run_store
        from tasks import run_pipeline_task

        _stub_orchestrator(monkeypatch, raise_exc=RuntimeError("boom"))
        run_id = _run_id()
        run_store.create_run(run_id, "q", str(tmp_path), mode="manual",
                              source="dashboard", session_id="s3", execution_backend="celery")

        run_pipeline_task.apply(args=[
            "does X help Y?", str(tmp_path), "s3", ["a.pdf"], run_id,
        ])

        row = run_store.get_run(run_id)
        assert row["status"] == "failed"
        assert "boom" in row["error_message"]
        assert row["error_traceback"]


@requires_db
class TestPauseResumeAcrossProcessBoundary:
    """The scenario that's impossible under the thread backend's in-memory
    dict but is the entire point of celery's Postgres-only pause state:
    save the pause state as if a DIFFERENT worker process paused the run,
    then resume in THIS process with no in-memory pipeline dict populated."""

    def test_continue_after_review_loads_pause_state_from_postgres(self, pg_db, monkeypatch, tmp_path):
        from persistence import run_store
        from models import PaperRecord, PipelineState
        from tasks import continue_after_review_task
        import orchestrator as orchestrator_module

        run_id = _run_id()
        run_store.create_run(run_id, "q", str(tmp_path), mode="search",
                              source="dashboard", session_id="s4", execution_backend="celery")
        run_store.claim_run(run_id)
        graph_state = {
            "papers_no_fulltext": [], "n_search_retrieved": 3,
            "papers_eligible": [PaperRecord(id="p1", title="T", abstract="A",
                                             authors=["X"], year=2020, source="pubmed")],
        }
        run_store.save_pause_state(run_id, "after_eligibility", graph_state)
        run_store.set_status(run_id, "awaiting_review")

        mock_orch = MagicMock()
        mock_orch.continue_after_review.return_value = PipelineState()
        mock_orch.last_graph_state = {"effect_sizes": []}
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator", MagicMock(return_value=mock_orch))

        # Note: run_service's module-level `_pipelines` dict has NO entry
        # for session "s4" from this process's perspective -- this proves
        # the resume works purely from Postgres, not a lucky in-memory hit.
        continue_after_review_task.apply(args=[str(tmp_path), "s4", run_id])

        mock_orch.continue_after_review.assert_called_once()
        # The graph_state passed through was reconstructed from Postgres --
        # spot-check the one field that survived the round trip.
        called_state = mock_orch.continue_after_review.call_args[0][0]
        assert called_state["n_search_retrieved"] == 3
        assert len(called_state["papers_eligible"]) == 1

        row = run_store.get_run(run_id)
        assert row["status"] == "completed"


class TestClaimGuardFailsOpenWithoutDatabase:
    def test_no_database_url_proceeds_anyway(self, monkeypatch, tmp_path):
        """Celery backend without Postgres can't guard against duplicates
        (documented limitation -- see tasks.py's _claim_or_skip docstring),
        but must still execute rather than silently hang forever."""
        import config
        monkeypatch.setattr(config, "DATABASE_URL", "")
        from tasks import _claim_or_skip
        assert _claim_or_skip("some_run_id", "queued", "task-1") is True

    def test_no_run_id_proceeds(self):
        from tasks import _claim_or_skip
        assert _claim_or_skip(None, "queued", "task-1") is True
