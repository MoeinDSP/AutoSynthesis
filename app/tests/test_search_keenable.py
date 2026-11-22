"""database_search.search_keenable / keenable_fetch_markdown -- Keenable
(https://keenable.ai) general web-search + landing-page-markdown API, added
as an additional (not sole) full-text discovery source. No key => no-op,
same convention as every other optional connector in database_search.py.
"""

import database_search


class TestSearchKeenableDisabled:
    def test_no_key_returns_empty_list(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "")
        assert database_search.search_keenable("anything") == []

    def test_no_key_fetch_returns_none(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "")
        assert database_search.keenable_fetch_markdown("https://example.test/x") is None


class TestSearchKeenableEnabled:
    def test_posts_correct_request_and_parses_hits(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")
        captured = {}

        class FakeResponse:
            status_code = 200
            def raise_for_status(self): return None
            def json(self):
                return {"results": [
                    {"title": "A Randomized Trial", "url": "https://pub.test/a.pdf",
                     "description": "An RCT.", "published_at": "2022-05-01"},
                    {"title": "", "url": "https://pub.test/no-title"},  # dropped: no title
                    {"title": "No URL"},  # dropped: no url
                ]}

        def fake_post(url, json, headers, timeout):
            captured["url"] = url
            captured["json"] = json
            captured["headers"] = headers
            captured["timeout"] = timeout
            return FakeResponse()

        monkeypatch.setattr(database_search.requests, "post", fake_post)

        hits = database_search.search_keenable("depression CBT trial", max_results=5, start_year=2021)

        assert captured["url"] == "https://api.keenable.ai/v1/search"
        assert captured["json"]["query"] == "depression CBT trial"
        assert captured["json"]["max_results"] == 5
        assert captured["json"]["published_after"] == "2021-01-01"
        assert captured["headers"]["X-API-Key"] == "keen_test123"

        assert len(hits) == 1
        hit = hits[0]
        assert hit["title"] == "A Randomized Trial"
        assert hit["url"] == "https://pub.test/a.pdf"
        assert hit["source"] == "keenable"
        assert hit["year"] == 2022
        assert hit["abstract"] == "An RCT."
        # URL looks like a direct PDF -- open_access_pdf populated.
        assert hit["open_access_pdf"] == "https://pub.test/a.pdf"

    def test_non_pdf_url_leaves_open_access_pdf_unset(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")

        class FakeResponse:
            status_code = 200
            def raise_for_status(self): return None
            def json(self):
                return {"results": [
                    {"title": "Landing Page Result", "url": "https://pub.test/article/123"},
                ]}

        monkeypatch.setattr(database_search.requests, "post",
                             lambda *a, **k: FakeResponse())
        hits = database_search.search_keenable("query")
        assert hits[0]["open_access_pdf"] is None
        assert hits[0]["url"] == "https://pub.test/article/123"

    def test_retries_on_429_then_succeeds(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")
        monkeypatch.setattr(database_search.time, "sleep", lambda _s: None)
        attempts = []

        class RateLimited:
            status_code = 429
            def raise_for_status(self): return None
            def json(self): return {}

        class Ok:
            status_code = 200
            def raise_for_status(self): return None
            def json(self): return {"results": [{"title": "T", "url": "https://x.test/y"}]}

        def fake_post(*a, **k):
            attempts.append(1)
            return RateLimited() if len(attempts) < 2 else Ok()

        monkeypatch.setattr(database_search.requests, "post", fake_post)
        hits = database_search.search_keenable("query")
        assert len(attempts) == 2
        assert hits[0]["title"] == "T"

    def test_request_exception_returns_empty_list_not_raise(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")

        def raising_post(*a, **k):
            raise ConnectionError("boom")

        monkeypatch.setattr(database_search.requests, "post", raising_post)
        assert database_search.search_keenable("query") == []


class TestKeenableFetchMarkdown:
    def test_fetch_returns_content(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")
        captured = {}

        class FakeResponse:
            def raise_for_status(self): return None
            def json(self): return {"content": "# Title\n\nSome extracted markdown."}

        def fake_get(url, params, headers, timeout):
            captured["url"] = url
            captured["params"] = params
            captured["headers"] = headers
            return FakeResponse()

        monkeypatch.setattr(database_search.requests, "get", fake_get)
        content = database_search.keenable_fetch_markdown("https://pub.test/landing")

        assert captured["url"] == "https://api.keenable.ai/v1/fetch"
        assert captured["params"]["url"] == "https://pub.test/landing"
        assert captured["params"]["live"] == "true"
        assert captured["headers"]["X-API-Key"] == "keen_test123"
        assert content == "# Title\n\nSome extracted markdown."

    def test_empty_content_returns_none(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")

        class FakeResponse:
            def raise_for_status(self): return None
            def json(self): return {"content": "   "}

        monkeypatch.setattr(database_search.requests, "get", lambda *a, **k: FakeResponse())
        assert database_search.keenable_fetch_markdown("https://pub.test/x") is None

    def test_request_exception_returns_none_not_raise(self, monkeypatch):
        monkeypatch.setattr(database_search, "KEENABLE_API_KEY", "keen_test123")

        def raising_get(*a, **k):
            raise TimeoutError("slow")

        monkeypatch.setattr(database_search.requests, "get", raising_get)
        assert database_search.keenable_fetch_markdown("https://pub.test/x") is None
