"""Shared fixtures for infrastructure-requiring tests (Postgres/Redis/
RabbitMQ). Every fixture here is skipped when its corresponding
TEST_*_URL env var isn't set, so a bare `pytest -q` on a checkout with no
infrastructure running stays green -- this file's mere existence must never
make any existing test require a database."""

import os

import pytest

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "")
TEST_REDIS_URL = os.environ.get("TEST_REDIS_URL", "")
TEST_BROKER_URL = os.environ.get("TEST_BROKER_URL", "")

requires_db = pytest.mark.skipif(not TEST_DATABASE_URL, reason="TEST_DATABASE_URL not set")
requires_redis = pytest.mark.skipif(not TEST_REDIS_URL, reason="TEST_REDIS_URL not set")
requires_broker = pytest.mark.skipif(not TEST_BROKER_URL, reason="TEST_BROKER_URL not set")


@pytest.fixture
def pg_db(monkeypatch):
    """Points config.DATABASE_URL at TEST_DATABASE_URL for the duration of
    one test, applies migrations, truncates every table before AND after
    (so tests don't see leftovers from a previous run and don't leave any
    for the next), and disposes the engine on teardown so the next test
    (which may point at a different URL) gets a fresh connection pool."""
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL not set")

    import config
    monkeypatch.setattr(config, "DATABASE_URL", TEST_DATABASE_URL)

    from persistence import db
    db.dispose()  # drop any pool created under a different DATABASE_URL
    from persistence.migrate import run_migrations
    run_migrations()

    from persistence.schema import METADATA, schema_migrations
    # NEVER truncate schema_migrations itself here -- it's migration-tracking
    # metadata, not per-test row data; wiping it would make run_migrations()
    # think nothing has been applied and re-run DDL every test, which is
    # exactly the idempotency behavior test_persistence_schema.py checks.
    data_tables = [t for t in METADATA.sorted_tables if t is not schema_migrations]

    with db.connection() as conn:
        for table in reversed(data_tables):
            conn.execute(table.delete())

    yield TEST_DATABASE_URL

    with db.connection() as conn:
        for table in reversed(data_tables):
            conn.execute(table.delete())
    db.dispose()


@pytest.fixture
def redis_cache(monkeypatch):
    """Points config.REDIS_URL at TEST_REDIS_URL for one test, flushes the
    two DBs this repo uses (cache + events) before AND after."""
    if not TEST_REDIS_URL:
        pytest.skip("TEST_REDIS_URL not set")

    import config
    monkeypatch.setattr(config, "REDIS_URL", TEST_REDIS_URL)

    from caching import client
    client.dispose()
    client.get_client(config.REDIS_CACHE_DB).flushdb()
    client.get_client(config.REDIS_EVENTS_DB).flushdb()

    yield TEST_REDIS_URL

    client.get_client(config.REDIS_CACHE_DB).flushdb()
    client.get_client(config.REDIS_EVENTS_DB).flushdb()
    client.dispose()


@pytest.fixture(autouse=True)
def _paper_selection_gate_off(monkeypatch):
    """The paper-selection pause after the search agent (config.PAPER_SELECTION_GATE,
    on by default for the UI) would stall every older test that drives a search-mode
    run straight to the full-text / paper-tracking gates. Those tests keep their
    original flow; tests/test_paper_selection_gate.py switches the gate back on."""
    import config
    monkeypatch.setattr(config, "PAPER_SELECTION_GATE", False)
