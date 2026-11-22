import sys
import types


def test_search_top_per_db_queries_only_enabled_pipeline_databases(monkeypatch):
    import database_search

    calls = []

    def fake_search(name):
        def _inner(query, max_results, start_year):
            calls.append((name, query, max_results, start_year))
            return [{"title": f"{name} paper", "source": name}]
        return _inner

    # Dispatch now goes through SOURCE_REGISTRY[key].searcher (a reference
    # captured once, not a dynamic module-attribute lookup per call) -- see
    # database_search.py::SourceSpec. Patch the registry entries themselves,
    # not the bare module-level function names, to match that.
    for name in ("arxiv", "semantic_scholar", "crossref", "osf", "pubmed"):
        monkeypatch.setitem(
            database_search.SOURCE_REGISTRY, name,
            database_search.SourceSpec(name, fake_search(name), "api", []),
        )
    monkeypatch.setattr(database_search, "ENABLED_SEARCH_DATABASES", ("arxiv",))

    results = database_search.search_top_per_db("test query", start_year=2020, top_n=7)

    assert set(results) == {"arxiv"}
    assert [name for name, *_ in calls] == ["arxiv"]
    assert calls[0][2] == 7


def test_search_top_per_db_can_enable_deep_research(monkeypatch):
    import database_search

    calls = []

    def fake_search(name):
        def _inner(query, max_results, start_year):
            calls.append(name)
            return [{"title": f"{name} paper", "source": name}]
        return _inner

    for name in ("arxiv", "deep_research", "semantic_scholar", "crossref", "osf", "pubmed"):
        monkeypatch.setitem(
            database_search.SOURCE_REGISTRY, name,
            database_search.SourceSpec(name, fake_search(name), "api", []),
        )
    monkeypatch.setattr(database_search, "ENABLED_SEARCH_DATABASES", ("arxiv", "deep_research"))

    results = database_search.search_top_per_db("test query", start_year=2020, top_n=7)

    assert set(results) == {"arxiv", "deep_research"}
    assert set(calls) == {"deep_research", "arxiv"}


def test_parse_deep_research_papers_from_fenced_json():
    from database_search import _parse_deep_research_papers

    text = """```json
{
  "papers": [
    {
      "title": "A quantitative LLM persuasion experiment",
      "authors": ["A. Researcher"],
      "year": 2024,
      "url": "https://arxiv.org/abs/2401.00001",
      "pdf_url": "https://arxiv.org/pdf/2401.00001",
      "doi": "",
      "abstract": "Reports an experiment with quantitative outcomes."
    }
  ]
}
```"""

    papers = _parse_deep_research_papers(text, max_results=50)

    assert papers == [{
        "id": papers[0]["id"],
        "title": "A quantitative LLM persuasion experiment",
        "abstract": "Reports an experiment with quantitative outcomes.",
        "authors": ["A. Researcher"],
        "year": 2024,
        "url": "https://arxiv.org/abs/2401.00001",
        "source": "deep_research",
        "open_access_pdf": "https://arxiv.org/pdf/2401.00001",
        "doi": None,
    }]


def test_search_deep_research_uses_openrouter_responses_endpoint(monkeypatch):
    import database_search

    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured["create"] = kwargs
            return types.SimpleNamespace(output_text="""{
              "papers": [
                {
                  "title": "OpenRouter Deep Research Paper",
                  "authors": ["A. Author"],
                  "year": 2025,
                  "url": "https://example.test/paper",
                  "pdf_url": "",
                  "doi": "",
                  "abstract": "A quantitative paper."
                }
              ]
            }""")

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured["init"] = kwargs
            self.responses = FakeResponses()

    fake_openai = types.SimpleNamespace(OpenAI=FakeOpenAI)

    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    monkeypatch.setattr(database_search, "OPENROUTER_API_KEY", "or-test")
    monkeypatch.setattr(database_search, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setattr(database_search, "DEEP_RESEARCH_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setattr(database_search, "DEEP_RESEARCH_MAX_TOOL_CALLS", 3)
    monkeypatch.setattr(database_search, "DEEP_RESEARCH_TIMEOUT_SECONDS", 99)

    papers = database_search.search_deep_research("mindfulness anxiety", max_results=50)

    assert captured["init"] == {
        "api_key": "or-test",
        "base_url": "https://openrouter.ai/api/v1",
        "timeout": 99,
    }
    assert captured["create"]["model"] == "openai/gpt-4o-mini"
    assert "Return the top" not in captured["create"]["input"]
    assert captured["create"]["tools"] == [{"type": "openrouter:web_search"}]
    assert captured["create"]["max_tool_calls"] == 3
    assert papers[0]["title"] == "OpenRouter Deep Research Paper"
