"""Cancelling a run from the UI: a running run stops at its next step (even
inside an agent's broad `except Exception`), a paused run is discarded at once,
and both end with status "cancelled" -- never "failed"."""
import sys
import threading
import time
import types

from fastapi.testclient import TestClient

import dashboard
import run_service


class _StubbornOrchestrator:
    """Stands in for the real pipeline: busy Python work that swallows every
    ordinary exception, like many agents' retry loops do."""
    def __init__(self, output_dir):
        pass

    def run_until_search_review(self, prompt, paper_files=None):
        for _ in range(400):                      # ~20 s if never cancelled
            try:
                time.sleep(0.05)
                sum(range(1000))
            except Exception:                    # noqa: BLE001 -- must not swallow a cancel
                pass
        return {"papers_eligible": []}

    run_until_fulltext_review = run_until_search_review


def test_running_run_is_cancelled_even_inside_broad_except(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "orchestrator",
                        types.SimpleNamespace(MetaAnalysisOrchestrator=_StubbornOrchestrator))
    sid = "cancel-test-running"
    t = threading.Thread(target=run_service.execute_run, args=("q", str(tmp_path), sid, None, None), daemon=True)
    t0 = time.time()
    t.start()
    pipeline = run_service._get_pipeline(sid)
    for _ in range(100):
        if pipeline.get("running"):
            break
        time.sleep(0.02)
    assert pipeline["running"]
    assert run_service.request_cancel(sid) == "cancelling"
    t.join(timeout=5)
    assert not t.is_alive(), "run thread did not stop"
    assert time.time() - t0 < 5
    assert pipeline["cancelled"] is True and pipeline["running"] is False and pipeline["error"] is None
    assert dashboard._derive_run_status(pipeline) == "cancelled"


def test_nothing_to_cancel_for_a_fresh_visitor():
    client = TestClient(dashboard.app)
    r = client.post("/cancel").json()
    assert r["ok"] is False and "no run" in r["error"].lower()


def test_paused_run_cancel_via_endpoint(monkeypatch):
    client = TestClient(dashboard.app)
    monkeypatch.setattr(dashboard, "_get_session_id", lambda request: "cancel-test-paused")
    p = run_service._get_pipeline("cancel-test-paused")
    p.update({"running": False, "awaiting_paper_selection": True, "pending_graph_state": {"x": 1}, "run_id": None})
    r = client.post("/cancel").json()
    assert r == {"ok": True, "state": "cancelled"}
    st = client.get("/status").json()
    assert st["cancelled"] is True and st["status"] == "cancelled" and st["awaiting_paper_selection"] is False
    assert p["pending_graph_state"] is None


def test_cancel_ui_is_on_the_page():
    html = TestClient(dashboard.app).get("/").text
    assert 'id="cancel-btn"' in html and "function cancelRun" in html and html.count('onclick="cancelRun()"') == 4


def test_page_javascript_is_valid():
    """The page's JS lives inside a Python string; a stray escape breaks the whole UI."""
    import re, shutil, subprocess, tempfile
    import pytest
    if not shutil.which("node"):
        pytest.skip("node not installed")
    html = TestClient(dashboard.app).get("/").text
    js = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:500]
