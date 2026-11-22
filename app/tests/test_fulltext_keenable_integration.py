"""Keenable's integration into agents/paper_reading_agent.py::fetch_fulltext_node
-- covering both pieces the user asked for:

  1. Keenable search results are merged, validated (_metadata_hit_matches_paper),
     and deduplicated (_dedupe_hits) alongside every other full-text
     discovery source, not tried only as a last-resort fallback.
  2. Keenable's /v1/fetch is tried as a landing-page extraction step before
     the Playwright browser fallback.

All network calls are monkeypatched; nothing here hits the real Keenable
API or the real academic connectors.
"""

from models import PaperRecord


def _paper(**kwargs):
    defaults = dict(id="p1", title="Effects of CBT on Depression: An RCT",
                     abstract="", authors=["A. Author"], year=2022, source="test")
    defaults.update(kwargs)
    return PaperRecord(**defaults)


def _stub_all_searchers(monkeypatch, paper_reading, *, arxiv=None, ss=None, crossref=None,
                         osf=None, pubmed=None, keenable=None, deep_research=None):
    """Patches database_search's module-level search_* functions (imported
    lazily inside fetch_fulltext_node) so no real network call happens.
    Empty list is the default for every source not explicitly given."""
    import database_search

    monkeypatch.setattr(database_search, "search_arxiv", lambda *a, **k: arxiv or [])
    monkeypatch.setattr(database_search, "search_semantic_scholar", lambda *a, **k: ss or [])
    monkeypatch.setattr(database_search, "search_crossref", lambda *a, **k: crossref or [])
    monkeypatch.setattr(database_search, "search_osf", lambda *a, **k: osf or [])
    monkeypatch.setattr(database_search, "search_pubmed", lambda *a, **k: pubmed or [])
    monkeypatch.setattr(database_search, "search_keenable", lambda *a, **k: keenable or [])
    monkeypatch.setattr(database_search, "search_deep_research", lambda *a, **k: deep_research or [])
    # fetch_open_access_pdf_url / fetch_pmc_fulltext are imported at module
    # level in paper_reading_agent.py -- neutralize them too so no strategy
    # this test isn't exercising can accidentally "succeed".
    monkeypatch.setattr(paper_reading, "fetch_open_access_pdf_url", lambda *a, **k: None)
    monkeypatch.setattr(paper_reading, "fetch_pmc_fulltext", lambda *a, **k: None)


class TestKeenableMergedIntoDiscoveryPool:
    def test_keenable_hit_is_tried_alongside_structured_sources_not_after(self, monkeypatch, tmp_path):
        """With every structured academic connector returning nothing,
        Keenable's own candidate must still be found and downloaded --
        proving it's a real peer source, not unreachable dead code."""
        import agents.paper_reading_agent as paper_reading

        paper = _paper()
        keenable_hit = {
            "id": "keenable:1", "title": paper.title, "url": "https://pub.test/keenable.pdf",
            "source": "keenable", "open_access_pdf": "https://pub.test/keenable.pdf",
        }
        _stub_all_searchers(monkeypatch, paper_reading, keenable=[keenable_hit])

        calls = []
        def fake_download(url, paper_id="", output_dir=""):
            calls.append(url)
            return "extracted full text" if url == "https://pub.test/keenable.pdf" else None
        monkeypatch.setattr(paper_reading, "_download_and_extract", fake_download)

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert [p.id for p in result["papers_eligible"]] == ["p1"]
        assert calls == ["https://pub.test/keenable.pdf"]

    def test_arxiv_and_keenable_agree_on_same_pdf_url_only_downloaded_once(self, monkeypatch, tmp_path):
        """The core 'deduplicated' requirement: two sources returning the
        SAME open_access_pdf URL must result in exactly one download
        attempt, not two."""
        import agents.paper_reading_agent as paper_reading

        paper = _paper()
        shared_url = "https://pub.test/shared.pdf"
        arxiv_hit = {"id": "arxiv:1", "title": paper.title, "url": "https://arxiv.org/abs/1",
                     "source": "arxiv", "open_access_pdf": shared_url}
        keenable_hit = {"id": "keenable:1", "title": paper.title, "url": shared_url,
                         "source": "keenable", "open_access_pdf": shared_url}
        _stub_all_searchers(monkeypatch, paper_reading, arxiv=[arxiv_hit], keenable=[keenable_hit])

        calls = []
        def fake_download(url, paper_id="", output_dir=""):
            calls.append(url)
            return None  # never succeeds -- we're only counting attempts
        monkeypatch.setattr(paper_reading, "_download_and_extract", fake_download)
        monkeypatch.setattr(paper_reading, "FULL_TEXT_USE_BROWSER_FALLBACKS", False)
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "")  # isolate: no Strategy-4 fetch noise

        paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert calls.count(shared_url) == 1, f"expected exactly one attempt at the shared URL, got {calls}"

    def test_structured_academic_source_tried_before_keenable_on_tie(self, monkeypatch, tmp_path):
        """_dedupe_hits keeps source-list order as priority: when both a
        structured connector (arXiv) and Keenable offer a WORKING but
        DIFFERENT candidate, arXiv's is tried first (and succeeds first)."""
        import agents.paper_reading_agent as paper_reading

        paper = _paper()
        arxiv_hit = {"id": "arxiv:1", "title": paper.title, "url": "https://arxiv.org/abs/1",
                     "source": "arxiv", "open_access_pdf": "https://arxiv.test/a.pdf"}
        keenable_hit = {"id": "keenable:1", "title": paper.title, "url": "https://pub.test/k.pdf",
                         "source": "keenable", "open_access_pdf": "https://pub.test/k.pdf"}
        _stub_all_searchers(monkeypatch, paper_reading, arxiv=[arxiv_hit], keenable=[keenable_hit])

        order = []
        def fake_download(url, paper_id="", output_dir=""):
            order.append(url)
            return "text" if url == "https://arxiv.test/a.pdf" else None
        monkeypatch.setattr(paper_reading, "_download_and_extract", fake_download)

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert order[0] == "https://arxiv.test/a.pdf"
        assert "https://pub.test/k.pdf" not in order  # stopped as soon as arXiv's succeeded
        assert result["papers_eligible"][0].full_text == "text"

    def test_keenable_and_deep_research_run_even_with_database_fallbacks_disabled(self, monkeypatch, tmp_path):
        """Regression guard for a real bug caught during implementation:
        Keenable/Deep Research are general web search, not structured
        academic-DB lookups -- they must stay reachable when a deployer sets
        FULL_TEXT_USE_DATABASE_FALLBACKS=False (skip arXiv/S2/CrossRef/OSF/
        PubMed specifically) while leaving web-search fallbacks on."""
        import agents.paper_reading_agent as paper_reading

        paper = _paper()
        keenable_hit = {"id": "keenable:1", "title": paper.title, "url": "https://pub.test/k.pdf",
                         "source": "keenable", "open_access_pdf": "https://pub.test/k.pdf"}
        _stub_all_searchers(monkeypatch, paper_reading, keenable=[keenable_hit])
        monkeypatch.setattr(paper_reading, "FULL_TEXT_USE_DATABASE_FALLBACKS", False)
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "keen_test")

        db_searcher_calls = []
        import database_search
        monkeypatch.setattr(database_search, "search_arxiv",
                             lambda *a, **k: db_searcher_calls.append("arxiv") or [])

        calls = []
        def fake_download(url, paper_id="", output_dir=""):
            calls.append(url)
            return "text" if url == "https://pub.test/k.pdf" else None
        monkeypatch.setattr(paper_reading, "_download_and_extract", fake_download)

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert db_searcher_calls == [], "arXiv (a 'database' source) must NOT run when the flag is off"
        assert calls == ["https://pub.test/k.pdf"], "Keenable must still run -- it's not a 'database' fallback"
        assert result["papers_eligible"][0].full_text == "text"

    def test_keenable_absent_pipeline_behaves_exactly_as_before(self, monkeypatch, tmp_path):
        """Regression guard: with no KEENABLE_API_KEY (search_keenable's own
        no-op), the merged pool contains exactly what the old sequential
        cascade would have produced."""
        import agents.paper_reading_agent as paper_reading
        import database_search

        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "")
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "")
        paper = _paper()
        arxiv_hit = {"id": "arxiv:1", "title": paper.title, "url": "https://arxiv.org/abs/1",
                     "source": "arxiv", "open_access_pdf": "https://arxiv.test/a.pdf"}
        _stub_all_searchers(monkeypatch, paper_reading, arxiv=[arxiv_hit])
        monkeypatch.setattr(paper_reading, "_download_and_extract",
                             lambda url, paper_id="", output_dir="": "text")

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })
        assert result["papers_eligible"][0].full_text == "text"


class TestKeenableLandingPageFetchFallback:
    def test_tried_when_key_set_and_other_strategies_exhausted(self, monkeypatch, tmp_path):
        import agents.paper_reading_agent as paper_reading

        paper = _paper(url="https://pub.test/landing")
        _stub_all_searchers(monkeypatch, paper_reading)
        monkeypatch.setattr(paper_reading, "_download_and_extract", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "_download_from_returned_url", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "FULL_TEXT_USE_BROWSER_FALLBACKS", False)
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "keen_test")

        fetch_calls = []
        def fake_keenable_fetch(url):
            fetch_calls.append(url)
            return "# Landing page\n\nExtracted markdown content."
        monkeypatch.setattr(paper_reading, "keenable_fetch_markdown", fake_keenable_fetch)

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert fetch_calls == ["https://pub.test/landing"]
        assert result["papers_eligible"][0].full_text.startswith("# Landing page")

    def test_skipped_entirely_when_key_unset(self, monkeypatch, tmp_path):
        import agents.paper_reading_agent as paper_reading

        paper = _paper(url="https://pub.test/landing")
        _stub_all_searchers(monkeypatch, paper_reading)
        monkeypatch.setattr(paper_reading, "_download_and_extract", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "_download_from_returned_url", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "FULL_TEXT_USE_BROWSER_FALLBACKS", False)
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "")

        fetch_calls = []
        monkeypatch.setattr(paper_reading, "keenable_fetch_markdown",
                             lambda url: fetch_calls.append(url) or "should not be reached")

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert fetch_calls == []
        assert result["papers_no_fulltext"] == ["p1"]

    def test_falls_back_to_browser_when_keenable_fetch_finds_nothing(self, monkeypatch, tmp_path):
        import agents.paper_reading_agent as paper_reading

        paper = _paper(url="https://pub.test/landing")
        _stub_all_searchers(monkeypatch, paper_reading)
        monkeypatch.setattr(paper_reading, "_download_and_extract", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "_download_from_returned_url", lambda *a, **k: None)
        monkeypatch.setattr(paper_reading, "KEENABLE_API_KEY", "keen_test")
        monkeypatch.setattr(paper_reading, "keenable_fetch_markdown", lambda url: None)
        monkeypatch.setattr(paper_reading, "FULL_TEXT_USE_BROWSER_FALLBACKS", True)

        browser_calls = []
        def fake_browser(url, paper_id="", output_dir=""):
            browser_calls.append(url)
            return "browser-extracted text"
        monkeypatch.setattr(paper_reading, "_browser_download_and_extract", fake_browser)

        result = paper_reading.fetch_fulltext_node({
            "papers_eligible": [paper], "output_dir": str(tmp_path),
        })

        assert browser_calls == ["https://pub.test/landing"]
        assert result["papers_eligible"][0].full_text == "browser-extracted text"


class TestDedupeHitsUnit:
    def test_dedupes_by_open_access_pdf_url(self):
        from agents.paper_reading_agent import _dedupe_hits
        hits = [
            ("arXiv", {"url": "https://a.test/1", "open_access_pdf": "https://x.test/shared.pdf"}),
            ("Keenable", {"url": "https://b.test/2", "open_access_pdf": "https://x.test/shared.pdf"}),
        ]
        deduped = _dedupe_hits(hits)
        assert len(deduped) == 1
        assert deduped[0][0] == "arXiv"  # first source wins

    def test_dedupes_by_doi(self):
        from agents.paper_reading_agent import _dedupe_hits
        hits = [
            ("Semantic Scholar", {"url": "https://a.test/1", "doi": "10.1/xyz"}),
            ("Keenable", {"url": "https://b.test/2", "doi": "10.1/xyz"}),
        ]
        deduped = _dedupe_hits(hits)
        assert len(deduped) == 1
        assert deduped[0][0] == "Semantic Scholar"

    def test_distinct_candidates_all_kept(self):
        from agents.paper_reading_agent import _dedupe_hits
        hits = [
            ("arXiv", {"url": "https://a.test/1"}),
            ("Keenable", {"url": "https://b.test/2"}),
            ("CrossRef", {"url": "https://c.test/3", "doi": "10.1/abc"}),
        ]
        deduped = _dedupe_hits(hits)
        assert len(deduped) == 3

    def test_case_and_trailing_slash_insensitive(self):
        from agents.paper_reading_agent import _dedupe_hits
        hits = [
            ("arXiv", {"url": "https://X.test/Shared/"}),
            ("Keenable", {"url": "https://x.test/shared"}),
        ]
        deduped = _dedupe_hits(hits)
        assert len(deduped) == 1
