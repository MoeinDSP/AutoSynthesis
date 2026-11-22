"""agents/paper_reading_agent.py's cached _extract_text_from_path/_bytes
wrappers -- against a REAL Redis (see tests/conftest.py's redis_cache
fixture). Skipped unless TEST_REDIS_URL is set. The counting-mock tests
(TestIdenticalPdfExtractedOnce) are the direct regression test for the
literal requirement: "identical PDFs should not be parsed repeatedly."
"""

import pipeline_graph  # noqa: F401 -- import before agents.* (see other test files' notes on this)
import agents.paper_reading_agent as pra

from tests.conftest import requires_redis


def _make_counting_stub(return_text="extracted text"):
    calls = []

    def _stub(*args, **kwargs):
        calls.append(args)
        return return_text

    _stub.calls = calls
    return _stub


@requires_redis
class TestIdenticalPdfExtractedOnce:
    def test_identical_bytes_at_different_paths_extracted_only_once(self, redis_cache, tmp_path, monkeypatch):
        stub = _make_counting_stub("some extracted text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)

        path_a = tmp_path / "a.pdf"
        path_b = tmp_path / "b.pdf"  # different filename, IDENTICAL bytes
        path_a.write_bytes(b"%PDF-1.4 identical content for both files")
        path_b.write_bytes(b"%PDF-1.4 identical content for both files")

        text_a = pra._extract_text_from_path(str(path_a))
        text_b = pra._extract_text_from_path(str(path_b))

        assert len(stub.calls) == 1  # the actual requirement, verified directly
        assert text_a == text_b == "some extracted text"

    def test_one_differing_byte_extracted_twice(self, redis_cache, tmp_path, monkeypatch):
        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)

        path_a = tmp_path / "a.pdf"
        path_b = tmp_path / "b.pdf"
        path_a.write_bytes(b"%PDF-1.4 content X")
        path_b.write_bytes(b"%PDF-1.4 content Y")  # one differing byte

        pra._extract_text_from_path(str(path_a))
        pra._extract_text_from_path(str(path_b))

        assert len(stub.calls) == 2

    def test_same_path_called_twice_only_extracts_once(self, redis_cache, tmp_path, monkeypatch):
        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 same file")

        pra._extract_text_from_path(str(path))
        pra._extract_text_from_path(str(path))
        assert len(stub.calls) == 1

    def test_bytes_variant_also_dedupes(self, redis_cache, monkeypatch):
        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_bytes_uncached", stub)

        raw = b"%PDF-1.4 identical bytes payload"
        pra._extract_text_from_bytes(raw)
        pra._extract_text_from_bytes(bytes(raw))  # a fresh bytes object, same content
        assert len(stub.calls) == 1


@requires_redis
class TestCacheDisabledConfig:
    def test_pdf_text_cache_enabled_false_always_calls_uncached(self, redis_cache, tmp_path, monkeypatch):
        import config
        monkeypatch.setattr(config, "PDF_TEXT_CACHE_ENABLED", False)
        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 x")

        pra._extract_text_from_path(str(path))
        pra._extract_text_from_path(str(path))
        assert len(stub.calls) == 2  # cache never consulted

    def test_oversized_file_skips_cache(self, redis_cache, tmp_path, monkeypatch):
        import config
        monkeypatch.setattr(config, "PDF_TEXT_CACHE_MAX_BYTES", 10)  # tiny cap
        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 " + b"x" * 100)  # well over the 10-byte cap

        pra._extract_text_from_path(str(path))
        pra._extract_text_from_path(str(path))
        assert len(stub.calls) == 2  # never cached -- too big


class TestUnreachableRedisDegradesGracefully:
    """Deliberately does NOT use the redis_cache fixture -- this class tests
    behavior when Redis is CONFIGURED but UNREACHABLE, so it needs no real
    Redis at all and always runs (no TEST_REDIS_URL requirement). Manually
    verified once against the real stack with a real dead port during this
    phase's implementation, in addition to this automated version."""

    def test_falls_through_to_uncached_not_a_crash(self, tmp_path, monkeypatch):
        import config
        from caching import client as cache_client

        monkeypatch.setattr(config, "REDIS_URL", "redis://127.0.0.1:1")  # nothing listens here
        cache_client.dispose()  # drop any client already pointing at a working URL

        stub = _make_counting_stub("text despite redis outage")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 x")

        text = pra._extract_text_from_path(str(path))
        assert text == "text despite redis outage"
        assert len(stub.calls) == 1  # degraded to uncached, didn't crash

        cache_client.dispose()  # drop the bad-URL client before monkeypatch restores REDIS_URL


@requires_redis
class TestFailureModes:
    def test_empty_extraction_result_is_not_cached(self, redis_cache, tmp_path, monkeypatch):
        """An extraction failure (empty string) must not poison the cache
        with a permanent empty result for that PDF."""
        stub = _make_counting_stub("")  # simulates every extractor failing
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 unparseable")

        pra._extract_text_from_path(str(path))
        pra._extract_text_from_path(str(path))
        assert len(stub.calls) == 2  # not cached, retried both times


@requires_redis
class TestRecordEvent:
    def test_hit_and_miss_increment_redis_counters(self, redis_cache, tmp_path, monkeypatch):
        import config
        from caching.client import get_client
        from caching.pdf_text_cache import _STATS_HITS_KEY, _STATS_MISSES_KEY

        stub = _make_counting_stub("text")
        monkeypatch.setattr(pra, "_extract_text_from_path_uncached", stub)
        path = tmp_path / "a.pdf"
        path.write_bytes(b"%PDF-1.4 x")

        pra._extract_text_from_path(str(path))  # miss
        pra._extract_text_from_path(str(path))  # hit

        events_client = get_client(config.REDIS_EVENTS_DB)
        assert int(events_client.get(_STATS_MISSES_KEY) or 0) == 1
        assert int(events_client.get(_STATS_HITS_KEY) or 0) == 1

    def test_record_event_never_raises_even_if_persistence_import_fails(self, redis_cache, monkeypatch):
        from caching import pdf_text_cache
        import builtins

        real_import = builtins.__import__

        def _blocked_import(name, *a, **k):
            if name == "persistence" or name.startswith("persistence."):
                raise ImportError("simulated")
            return real_import(name, *a, **k)

        monkeypatch.setattr(builtins, "__import__", _blocked_import)
        # Must not raise, even with persistence unimportable.
        pdf_text_cache.record_event(
            run_id=None, content_sha256="a" * 64, cache_key="k", cache_hit=False,
        )
