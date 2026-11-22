"""Landing-page extras: model lock, demo loading (no LLM), imprint, paper/site info."""
import importlib
import os

import pytest
from fastapi.testclient import TestClient

import config
import dashboard


def test_enabled_models_locks_everything_to_the_cheapest(monkeypatch):
    monkeypatch.setenv("ENABLED_MODELS", "google/gemini-3.8-flash")
    monkeypatch.setenv("MODEL_NAME", "openai/gpt-5.6-sol")
    monkeypatch.setenv("SEARCH_QUERY_VARIANT_MODEL", "openai/gpt-5.6-sol")
    try:
        cfg = importlib.reload(config)
        assert cfg.MODEL_NAME == "google/gemini-3.8-flash"
        assert cfg.SEARCH_QUERY_VARIANT_MODEL == "google/gemini-3.8-flash"
        assert [m["id"] for m in cfg.AVAILABLE_MODELS] == ["google/gemini-3.8-flash"]
        with pytest.raises(ValueError):
            cfg.set_active_model("anthropic/claude-opus-5")
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_run_rejects_a_model_that_is_not_enabled(monkeypatch):
    monkeypatch.setattr(dashboard._config, "AVAILABLE_MODELS", [{"id": "google/gemini-3.8-flash", "label": "G"}])
    client = TestClient(dashboard.app)
    r = client.post("/run", json={"prompt": "x", "model": "openai/gpt-5.6-sol"}).json()
    assert r["ok"] is False and "Unknown model" in r["error"]


def test_site_info_and_imprint_and_logo():
    client = TestClient(dashboard.app)
    info = client.get("/site_info").json()
    assert info["paper_title"] and info["demo_available"] is True
    page = client.get("/imprint")
    assert page.status_code == 200 and "Imprint" in page.text and "Feuerriegel" in page.text
    assert client.get("/assets/berd-nfdi-logo.png").status_code == 200
    assert client.get("/assets/..%2Fconfig.py").status_code == 404
    assert client.get("/assets/nope.png").status_code == 404
    home = client.get("/").text
    assert 'id="demo-btn"' in home and "/imprint" in home and "berd-nfdi-logo.png" in home
    assert "showDemoHint" in home and "as_run_confirmed" in home


def test_demo_loads_without_any_llm_and_serves_results_and_plots():
    client = TestClient(dashboard.app)
    r = client.post("/demo/load").json()
    assert r["ok"] and r["prompt"]
    st = client.get("/status").json()
    assert st["done"] is True and st["running"] is False
    res = client.get("/results").json()
    assert res["demo"] is True and res["n_studies"] > 0
    assert client.get("/outputs/forest_plot.png").status_code == 200
    names = {f["name"] for f in client.get("/files").json()}
    assert "meta_analysis_report.md" in names and "forest_plot.png" in names


def test_second_run_blocked_while_another_session_runs(monkeypatch):
    import dashboard
    from fastapi.testclient import TestClient
    monkeypatch.setattr(dashboard, "MAX_CONCURRENT_RUNS", 1)
    other = dashboard._get_pipeline("someone-else")
    other["running"] = True
    try:
        c = TestClient(dashboard.app)
        assert c.get("/server_busy").json() == {"busy": True}
        r = c.post("/run", json={"prompt": "Does X improve Y?"}).json()
        assert r["ok"] is False and r.get("busy") is True
    finally:
        other["running"] = False
    assert TestClient(dashboard.app).get("/server_busy").json() == {"busy": False}


def test_busy_popup_wired_into_page():
    import dashboard
    from fastapi.testclient import TestClient
    html = TestClient(dashboard.app).get("/").text
    assert "function showBusyPopup" in html and "/server_busy" in html


def test_demo_examples_listed_and_switching_never_mixes_files():
    client = TestClient(dashboard.app)
    demos = client.get("/site_info").json()["demos"]
    ids = [d["id"] for d in demos]
    assert ids == ["cochrane-cd015092", "cochrane-cd016018", "cochrane-cd015610"]   # the paper's three reviews
    assert all(d["title"] and d["subtitle"] for d in demos)

    expected = {"cochrane-cd015092": 11, "cochrane-cd016018": 9, "cochrane-cd015610": 14}
    for demo_id, k in expected.items():
        r = client.post("/demo/load", json={"id": demo_id}).json()
        assert r["ok"] and r["id"] == demo_id and r["prompt"]
        res = client.get("/results").json()
        assert res["demo"] is True and res["k"] == k and res["effect_measure"] == "MD"
        names = {f["name"] for f in client.get("/files").json()}
        assert not any(n.startswith(".") for n in names)
        assert not any(n.startswith("fulltext_") for n in names)      # no paper full texts are shipped
        for plot in res["plots"].values():                            # every figure the results view shows exists
            assert client.get(f"/outputs/{plot}").status_code == 200
        assert {"prisma", "funnel", "forest", "rob_rob2"} <= set(res["plots"])

    assert client.post("/demo/load", json={"id": "../config"}).json()["ok"] is False
