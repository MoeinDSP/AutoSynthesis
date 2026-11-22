from models import MetaAnalysisPlan


def _plan() -> MetaAnalysisPlan:
    return MetaAnalysisPlan(
        research_question="Does mindfulness reduce anxiety symptoms?",
        treatment_label="mindfulness intervention",
        control_label="usual care control",
        outcome_description="anxiety symptoms",
        positive_direction="positive g means lower anxiety in mindfulness",
        search_queries=["mindfulness anxiety"],
        inclusion_criteria=["original empirical study", "quantitative anxiety outcome"],
        exclusion_criteria=["reviews", "no quantitative outcome"],
        moderators_to_extract=["study design"],
        search_start_year=2010,
    )


def test_intent_queries_add_empirical_terms(monkeypatch):
    import agents.search_agent as search_agent

    monkeypatch.setattr(search_agent, "USE_LLM_SEARCH_QUERY_VARIANTS", False)
    queries = search_agent._build_intent_queries(_plan())

    assert queries[0] == "mindfulness anxiety"
    assert any(
        any(term in query.lower() for term in ("quantitative", "experiment", "trial", "controlled"))
        for query in queries
    )


def test_intent_queries_can_use_llm(monkeypatch):
    import types
    import agents.search_agent as search_agent

    monkeypatch.setattr(search_agent, "USE_LLM_SEARCH_QUERY_VARIANTS", True)
    monkeypatch.setattr(search_agent, "SEARCH_QUERY_VARIANTS", 2)
    monkeypatch.setattr(
        search_agent,
        "query_variant_llm",
        types.SimpleNamespace(
            invoke=lambda _prompt: types.SimpleNamespace(
                content='{"queries": ["mindfulness anxiety randomized trial", "mindfulness anxiety quantitative outcome"]}'
            )
        ),
    )

    queries = search_agent._build_intent_queries(_plan())

    assert queries == [
        "mindfulness anxiety randomized trial",
        "mindfulness anxiety quantitative outcome",
    ]


def test_statistical_signal_detector_finds_reported_results():
    from agents.search_agent import _has_statistical_signal

    assert _has_statistical_signal("Participants improved, t(58) = 2.31, p = .03, SD = 1.2.")


def test_prefetch_screen_excludes_clear_review_without_stats():
    from agents.search_agent import _prefetch_screen_paper

    include, reason, details = _prefetch_screen_paper(
        {
            "title": "Mindfulness for anxiety: a systematic review and meta-analysis",
            "abstract": "This article reviews previous studies and summarizes the literature.",
        },
        _plan(),
    )

    assert include is False
    assert "review" in reason
    assert details["non_empirical_signal"] is True


def test_prefetch_screen_keeps_borderline_records():
    from agents.search_agent import _prefetch_screen_paper

    include, reason, _details = _prefetch_screen_paper(
        {
            "title": "Mindfulness training in university students",
            "abstract": "",
        },
        _plan(),
    )

    assert include is True
    assert "keep" in reason


def test_search_node_arxiv_only_caps_total_unique_papers(monkeypatch):
    import agents.search_agent as search_agent

    raw = [
        {
            "id": f"arxiv:{i}",
            "title": f"Mindfulness anxiety trial {i}",
            "abstract": "A quantitative experiment reported t(58) = 2.31, p = .03.",
            "authors": [],
            "year": 2024,
            "url": f"https://arxiv.org/abs/2401.{i:05d}",
            "source": "arxiv",
        }
        for i in range(10)
    ]

    calls = []

    def fake_search_top_per_db(query, start_year, top_n):
        calls.append((query, start_year, top_n))
        return {"arxiv": raw}

    monkeypatch.setattr(search_agent, "search_top_per_db", fake_search_top_per_db)
    monkeypatch.setattr(search_agent, "ENABLED_SEARCH_DATABASES", ("arxiv",))
    monkeypatch.setattr(search_agent, "MAX_PAPERS_PER_QUERY", 7)

    result = search_agent.search_node({
        "plan": _plan(),
    })

    assert len(result["all_retrieved_papers"]) == 7
    assert len(result["papers_eligible"]) == 7
    assert set(result["screening_decisions"]) == {f"arxiv:{i}" for i in range(7)}
    assert calls[0][2] == 7


def test_search_node_keeps_arxiv_cap_when_deep_research_enabled(monkeypatch):
    import agents.search_agent as search_agent

    arxiv_rows = [
        {
            "id": f"arxiv:{i}",
            "title": f"Mindfulness anxiety arxiv trial {i}",
            "abstract": "A quantitative experiment reported t(58) = 2.31, p = .03.",
            "authors": [],
            "year": 2024,
            "url": f"https://arxiv.org/abs/2402.{i:05d}",
            "source": "arxiv",
        }
        for i in range(10)
    ]
    deep_rows = [
        {
            "id": f"deep_research:{i}",
            "title": f"Mindfulness anxiety deep research paper {i}",
            "abstract": "A quantitative controlled comparison reported p = .04.",
            "authors": [],
            "year": 2024,
            "url": f"https://example.test/paper-{i}",
            "source": "deep_research",
        }
        for i in range(2)
    ]

    def fake_search_top_per_db(query, start_year, top_n):
        return {"arxiv": arxiv_rows, "deep_research": deep_rows}

    monkeypatch.setattr(search_agent, "search_top_per_db", fake_search_top_per_db)
    monkeypatch.setattr(search_agent, "ENABLED_SEARCH_DATABASES", ("arxiv", "deep_research"))
    monkeypatch.setattr(search_agent, "MAX_PAPERS_PER_QUERY", 7)

    result = search_agent.search_node({
        "plan": _plan(),
    })

    assert [p.source for p in result["all_retrieved_papers"]].count("arxiv") == 7
    assert [p.source for p in result["all_retrieved_papers"]].count("deep_research") == 2
