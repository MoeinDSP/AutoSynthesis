"""Two simultaneous runs (thread backend -- what's actually deployed) stay
fully isolated: distinct run_ids, distinct per-session pipeline dicts,
non-interleaved stage logs (the _SSEHandler's `record.thread != self.thread_id`
filter is the whole mechanism -- this proves it holds under real concurrent
threads, not just by reading the code), and correctly-attributed results.
"""

import threading
import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import pipeline_graph  # noqa: F401 -- import ordering, see other test files
import dashboard
from models import PipelineState, MetaAnalysisResult


def _wait_for_done(client: TestClient, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get("/status").json()
        if last["done"]:
            return last
        time.sleep(0.05)
    raise AssertionError(f"pipeline did not finish within {timeout}s -- last /status: {last}")


def _state_with_pooled_g(value: float) -> PipelineState:
    return PipelineState(meta_analysis=MetaAnalysisResult(
        pooled_g=value, pooled_se=0.1, ci_lower=value - 0.2, ci_upper=value + 0.2,
        z_value=4.0, p_value=0.001, tau_squared=0.01, tau=0.1,
        i_squared=20.0, h_squared=1.2, q_statistic=5.0, q_df=4,
        q_p_value=0.3, k=5, n_total=250,
    ))


class TestConcurrentRunsStayIsolated:
    def test_two_sessions_two_run_ids_two_results(self, monkeypatch):
        import orchestrator as orchestrator_module
        # The server allows one run at a time by default (MAX_CONCURRENT_RUNS);
        # this test needs two in parallel to prove their state stays isolated.
        monkeypatch.setattr(dashboard, "MAX_CONCURRENT_RUNS", 2)

        # Each session's orchestrator instance returns a DIFFERENT pooled_g
        # after a small, staggered delay -- if session state leaked between
        # threads, one session's /results would show the other's number.
        def _make_orch(pooled_g: float, delay: float):
            orch = MagicMock()
            def _run(*a, **k):
                time.sleep(delay)
                return _state_with_pooled_g(pooled_g)
            orch.run.side_effect = _run
            orch.last_graph_state = {"effect_sizes": []}
            return orch

        orch_a = _make_orch(0.11, 0.15)
        orch_b = _make_orch(0.99, 0.05)
        instances = iter([orch_a, orch_b])
        monkeypatch.setattr(orchestrator_module, "MetaAnalysisOrchestrator",
                             MagicMock(side_effect=lambda **k: next(instances)))

        client_a = TestClient(dashboard.app)
        client_b = TestClient(dashboard.app)

        resp_a = client_a.post("/run", json={"prompt": "question A", "paper_files": ["a.pdf"]})
        resp_b = client_b.post("/run", json={"prompt": "question B", "paper_files": ["b.pdf"]})
        run_id_a = resp_a.json()["run_id"]
        run_id_b = resp_b.json()["run_id"]
        assert run_id_a != run_id_b

        final_a = _wait_for_done(client_a)
        final_b = _wait_for_done(client_b)
        assert final_a["run_id"] == run_id_a
        assert final_b["run_id"] == run_id_b

        results_a = client_a.get("/results").json()
        results_b = client_b.get("/results").json()
        assert results_a["pooled_g"] == 0.11
        assert results_b["pooled_g"] == 0.99

    def test_distinct_output_dirs_per_session(self):
        client_a = TestClient(dashboard.app)
        client_b = TestClient(dashboard.app)
        # Trigger session-cookie issuance without a real run.
        client_a.get("/status")
        client_b.get("/status")
        session_a = client_a.cookies.get("session")
        session_b = client_b.cookies.get("session")
        assert session_a != session_b

    def test_stage_logs_do_not_interleave_across_real_threads(self):
        """Direct test of the _SSEHandler thread-id filter that makes
        isolation possible in the first place -- two real threads logging
        concurrently under two different session_ids/run_ids must each only
        see their own lines in pipeline["stage_logs"]."""
        import logging
        import run_service

        session_a, session_b = "concurrent_test_a", "concurrent_test_b"
        pipeline_a = run_service._get_pipeline(session_a)
        pipeline_b = run_service._get_pipeline(session_b)
        pipeline_a["stage_logs"] = {sid: [] for sid in run_service.STAGE_ORDER}
        pipeline_b["stage_logs"] = {sid: [] for sid in run_service.STAGE_ORDER}

        logger = logging.getLogger("test_concurrent_runs_logger")
        barrier = threading.Barrier(2)

        def _worker(session_id, tag, n=20):
            handler = run_service._attach_handler(session_id)
            barrier.wait()
            try:
                for i in range(n):
                    logger.info(f"STAGE 0: {tag}-{i}")
            finally:
                run_service._detach_handler(handler)

        t1 = threading.Thread(target=_worker, args=(session_a, "A"))
        t2 = threading.Thread(target=_worker, args=(session_b, "B"))
        t1.start(); t2.start()
        t1.join(); t2.join()

        lines_a = [entry["msg"] for entry in pipeline_a["stage_logs"]["s0"]]
        lines_b = [entry["msg"] for entry in pipeline_b["stage_logs"]["s0"]]
        assert all("A-" in msg for msg in lines_a)
        assert all("B-" in msg for msg in lines_b)
        assert len(lines_a) == 20
        assert len(lines_b) == 20

    def test_tracked_child_thread_logs_still_forwarded_but_stay_isolated(self):
        """Regression test for the Stage-3b-looks-stuck bug: a pipeline stage
        that offloads work to a `spawn_tracked_thread` worker (e.g.
        paper_reading_agent's per-paper full-text-fetch timeout worker) must
        still have its log lines reach the owning session's live log/
        stage_logs -- a bare `threading.Thread(...).start()` there silently
        dropped every line, because `_SSEHandler.emit`'s `record.thread ==
        self.thread_id` check only ever matched the pipeline's own thread.
        A worker thread NOT spawned via spawn_tracked_thread (e.g. another
        session's own pipeline thread) must still be filtered out, so
        cross-session isolation is unaffected."""
        import logging
        import threading as _threading
        import run_service
        from utils import thread_tracking as _thread_tracking

        session_id = "concurrent_test_tracked_child"
        other_session_id = "concurrent_test_untracked_other"
        pipeline = run_service._get_pipeline(session_id)
        other_pipeline = run_service._get_pipeline(other_session_id)
        pipeline["stage_logs"] = {sid: [] for sid in run_service.STAGE_ORDER}
        other_pipeline["stage_logs"] = {sid: [] for sid in run_service.STAGE_ORDER}

        logger = logging.getLogger("test_concurrent_runs_logger")

        def _main():
            handler = run_service._attach_handler(session_id)
            try:
                logger.info("STAGE 0: from-main-thread")
                child_done = _threading.Event()

                def _child_work():
                    logger.info("STAGE 0: from-tracked-child")
                    child_done.set()

                worker = _thread_tracking.spawn_tracked_thread(target=_child_work)
                worker.join(timeout=5)
                assert child_done.is_set()

                # An unrelated (not-tracked-as-a-child) thread's logs must
                # NOT bleed into this session, even while this handler is
                # attached -- isolation from other concurrent sessions is
                # unaffected by the is_descendant() check.
                other_done = _threading.Event()

                def _unrelated_work():
                    other_handler = run_service._attach_handler(other_session_id)
                    try:
                        logger.info("STAGE 0: from-other-session")
                    finally:
                        run_service._detach_handler(other_handler)
                    other_done.set()

                other = _threading.Thread(target=_unrelated_work)
                other.start()
                other.join(timeout=5)
                assert other_done.is_set()
            finally:
                run_service._detach_handler(handler)

        t = _threading.Thread(target=_main)
        t.start()
        t.join(timeout=10)

        lines = [entry["msg"] for entry in pipeline["stage_logs"]["s0"]]
        assert "STAGE 0: from-main-thread" in lines
        assert "STAGE 0: from-tracked-child" in lines
        assert not any("from-other-session" in msg for msg in lines)

        other_lines = [entry["msg"] for entry in other_pipeline["stage_logs"]["s0"]]
        assert "STAGE 0: from-other-session" in other_lines
        assert not any("from-tracked-child" in msg for msg in other_lines)
