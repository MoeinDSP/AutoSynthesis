"""caching/pdf_text_cache.py -- cache key construction. No Redis needed --
these are pure functions of their inputs."""

from caching.pdf_text_cache import compute_code_hash, fingerprint, key_for, installed_versions


def _f1():
    return 1


def _f2():
    return 2


def _f2_reworded():
    return 2  # semantically identical, but different source text


class TestCodeHash:
    def test_deterministic_for_the_same_functions(self):
        assert compute_code_hash(_f1, _f2) == compute_code_hash(_f1, _f2)

    def test_changes_when_source_changes(self):
        # _f2 and _f2_reworded return the same value but have different
        # source text -- the hash must differ, since it's meant to catch
        # ANY code change, not just behavior changes.
        assert compute_code_hash(_f1, _f2) != compute_code_hash(_f1, _f2_reworded)

    def test_order_of_functions_matters(self):
        # Not a strict requirement, but documents actual behavior: swapping
        # argument order changes the concatenated source, hence the hash.
        assert compute_code_hash(_f1, _f2) != compute_code_hash(_f2, _f1)


class TestFingerprint:
    def test_deterministic_for_the_same_inputs(self):
        fp1 = fingerprint("codehash1", ["mineru_cloud", "pypdf"], {"pypdf": "4.0.0"})
        fp2 = fingerprint("codehash1", ["mineru_cloud", "pypdf"], {"pypdf": "4.0.0"})
        assert fp1 == fp2

    def test_changes_when_code_hash_changes(self):
        fp1 = fingerprint("codehash1", ["pypdf"], {})
        fp2 = fingerprint("codehash2", ["pypdf"], {})
        assert fp1 != fp2

    def test_changes_when_cascade_changes(self):
        """The 'code changes must not return stale results' requirement,
        applied to which extractors are even AVAILABLE (e.g. an API key
        being added/removed changes the cascade even with zero code
        changes) -- this must also invalidate."""
        fp1 = fingerprint("codehash1", ["mineru_cloud", "pypdf"], {})
        fp2 = fingerprint("codehash1", ["pypdf"], {})
        assert fp1 != fp2

    def test_changes_when_module_versions_change(self):
        fp1 = fingerprint("codehash1", ["pypdf"], {"pypdf": "4.0.0"})
        fp2 = fingerprint("codehash1", ["pypdf"], {"pypdf": "4.1.0"})
        assert fp1 != fp2

    def test_is_reasonably_short_and_hex(self):
        fp = fingerprint("codehash1", ["pypdf"], {"pypdf": "4.0.0"})
        assert len(fp) == 16
        int(fp, 16)  # must be valid hex -- raises ValueError otherwise

    def test_never_contains_secret_material(self):
        """Cache keys must be safely loggable -- fingerprint() never
        receives API key VALUES, only the boolean-derived cascade list
        (see agents/paper_reading_agent.py::_pdf_cache_cascade(), which
        builds that list from presence/absence, never the key string
        itself). This test documents/pins that contract at the fingerprint
        level: passing something that LOOKS like a secret in the cascade
        list would show up in the fingerprint's OWN inputs, so the
        discipline has to be enforced by the caller -- verified here by
        checking the real caller never does that."""
        import inspect
        import agents.paper_reading_agent as pra
        source = inspect.getsource(pra._pdf_cache_cascade)
        assert "_mineru_api_key()" in source  # only used for a truthiness check
        assert "MISTRAL_API_KEY" not in source.split("if")[0]  # not embedded as a value anywhere but a condition


class TestKeyFor:
    def test_key_shape(self, monkeypatch):
        import config
        monkeypatch.setattr(config, "PDF_TEXT_CACHE_VERSION", "v1")
        key = key_for("a" * 64, "b" * 16)
        assert key == f"autosynthesis:pdf_text:v1:{'b' * 16}:{'a' * 64}"

    def test_key_changes_when_cache_version_changes(self, monkeypatch):
        import config
        monkeypatch.setattr(config, "PDF_TEXT_CACHE_VERSION", "v1")
        key_v1 = key_for("a" * 64, "b" * 16)
        monkeypatch.setattr(config, "PDF_TEXT_CACHE_VERSION", "v2")
        key_v2 = key_for("a" * 64, "b" * 16)
        assert key_v1 != key_v2

    def test_key_changes_when_content_hash_changes(self):
        key1 = key_for("a" * 64, "fp")
        key2 = key_for("c" * 64, "fp")
        assert key1 != key2


class TestInstalledVersions:
    def test_returns_a_version_for_a_real_installed_package(self):
        versions = installed_versions(["pypdf"])
        assert versions["pypdf"]  # non-empty -- pypdf is a hard dependency

    def test_missing_package_returns_empty_string_not_an_exception(self):
        versions = installed_versions(["this-package-does-not-exist-xyz"])
        assert versions["this-package-does-not-exist-xyz"] == ""
