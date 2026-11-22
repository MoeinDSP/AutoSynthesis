"""
database_search.py's SOURCE_REGISTRY / search_top_per_db() -- explicit
per-source status reporting (fixes the confirmed-live bug where a source
could sit in ENABLED_SEARCH_DATABASES while silently contributing zero
results, with no way to tell without grepping logs), plus the naming-
normalization fix for the specific Semantic Scholar dispatch mismatch that
caused it.
"""

from unittest.mock import patch

import database_search as ds


def test_normalize_db_name_collapses_separators_and_case():
    assert ds._normalize_db_name("SemanticScholar") == ds._normalize_db_name("semantic_scholar")
    assert ds._normalize_db_name("Web-Of-Science") == ds._normalize_db_name("web of science".replace(" ", "_"))
    assert ds._normalize_db_name("PubMed") == "pubmed"


def test_semantic_scholar_naming_variants_all_resolve_to_registry_key():
    """The exact bug confirmed live: '.env' spelled it "SemanticScholar" (no
    separator), the OLD hardcoded dispatch key was "semantic_scholar" (with
    one) -- they never matched. Every plausible spelling must now resolve."""
    for variant in ("SemanticScholar", "semantic_scholar", "semantic-scholar", "SEMANTICSCHOLAR"):
        key = ds._REGISTRY_BY_NORMALIZED_NAME.get(ds._normalize_db_name(variant))
        assert key == "semantic_scholar", f"{variant!r} did not resolve"


def test_source_status_report_distinguishes_wired_unimplemented_and_not_requested():
    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("PubMed", "wos", "central", "not_a_real_source")):
        report = ds.source_status_report()
    assert report["pubmed"]["status"] == "requested_and_wired"
    assert report["central"]["status"] == "requested_but_no_credentials"
    assert "not_requested" in {v["status"] for k, v in report.items() if k not in
                                {"pubmed", "wos", "central", "not_a_real_source"}}
    assert report["not_a_real_source"]["status"] == "requested_but_unknown_source"


def test_source_status_report_flags_ictrp_as_unimplemented_not_no_credentials():
    """ICTRP has no connector at all (searcher=None) -- distinct status from
    central/embase/cinahl, which have a stub connector but no usable
    credentials ("requested_but_no_credentials")."""
    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("ictrp",)):
        report = ds.source_status_report()
    assert report["ictrp"]["status"] == "requested_but_unimplemented"


def test_search_top_per_db_reports_unimplemented_source_without_crashing():
    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("central", "embase", "cinahl")):
        results = ds.search_top_per_db("test query", start_year=2015, top_n=5)
    # None of these have real access -- must return cleanly with no results,
    # never raise, never silently pretend to have queried something.
    assert results == {}


def test_search_top_per_db_skips_unknown_source_gracefully():
    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("not_a_real_source",)):
        results = ds.search_top_per_db("test query", start_year=2015, top_n=5)
    assert results == {}


def test_search_top_per_db_calls_only_the_registered_searcher_for_each_enabled_source():
    called = {}

    def fake_pubmed(query, max_results, start_year):
        called["pubmed"] = True
        return [{"title": "Fake Paper", "source": "pubmed", "year": 2021}]

    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("pubmed",)):
        with patch.dict(ds.SOURCE_REGISTRY, {
            "pubmed": ds.SourceSpec("pubmed", fake_pubmed, "api", []),
        }):
            results = ds.search_top_per_db("query", start_year=2015, top_n=5)

    assert called.get("pubmed") is True
    assert results["pubmed"][0]["title"] == "Fake Paper"


def test_registry_has_clean_placeholders_for_central_embase_cinahl():
    for key in ("central", "embase", "cinahl"):
        spec = ds.SOURCE_REGISTRY[key]
        assert spec.access_mode == "unavailable"
        assert spec.searcher is not None  # a real function exists...
        assert spec.searcher(  # ...but it never pretends to hit a real API
            "query", max_results=5, start_year=2015
        ) == []


def test_registry_ictrp_has_no_connector_at_all():
    assert ds.SOURCE_REGISTRY["ictrp"].searcher is None


def test_search_top_per_db_runs_enabled_sources_concurrently_not_sequentially():
    """search_top_per_db now runs each enabled database's searcher in a
    thread pool (see its docstring for why that's safe here specifically).
    Prove it actually overlaps in wall-clock time, not just that it still
    returns the right shape -- 4 fake sources each sleeping 0.3s must
    finish in well under their sum (1.2s) if they're truly concurrent."""
    import time

    def make_slow_searcher(tag):
        def _searcher(query, max_results, start_year):
            time.sleep(0.3)
            return [{"title": tag, "source": tag, "year": 2021}]
        return _searcher

    # Reuse existing registry keys (only swapping out their searcher
    # functions) -- _REGISTRY_BY_NORMALIZED_NAME is a reverse-lookup dict
    # precomputed once at import time from the ORIGINAL SOURCE_REGISTRY, so
    # a brand-new key introduced only via patch.dict here would never
    # resolve and get classified as "unknown_source" instead.
    fake_sources = ["pubmed", "arxiv", "semantic_scholar", "wos"]
    with patch.object(ds, "ENABLED_SEARCH_DATABASES", tuple(fake_sources)):
        with patch.dict(ds.SOURCE_REGISTRY, {
            name: ds.SourceSpec(name, make_slow_searcher(name), "api", [])
            for name in fake_sources
        }):
            start = time.monotonic()
            results = ds.search_top_per_db("query", start_year=2015, top_n=5)
            elapsed = time.monotonic() - start

    assert elapsed < 0.8, f"took {elapsed:.2f}s -- looks sequential (expected ~0.3s if concurrent)"
    for name in fake_sources:
        assert results[name][0]["title"] == name


def test_search_top_per_db_one_slow_failure_does_not_block_or_lose_the_others():
    """Exception isolation must survive the move to a thread pool: one
    source raising (or hanging past the others) must not prevent the
    other sources' results from coming back, and must not raise out of
    search_top_per_db itself."""
    import time

    def fake_ok(query, max_results, start_year):
        return [{"title": "ok", "source": "fake_ok", "year": 2021}]

    def fake_slow_then_raises(query, max_results, start_year):
        time.sleep(0.2)
        raise RuntimeError("simulated upstream failure")

    with patch.object(ds, "ENABLED_SEARCH_DATABASES", ("pubmed", "arxiv")):
        with patch.dict(ds.SOURCE_REGISTRY, {
            "pubmed": ds.SourceSpec("pubmed", fake_ok, "api", []),
            "arxiv": ds.SourceSpec("arxiv", fake_slow_then_raises, "api", []),
        }):
            results = ds.search_top_per_db("query", start_year=2015, top_n=5)

    assert results["pubmed"][0]["title"] == "ok"
    assert "arxiv" not in results
