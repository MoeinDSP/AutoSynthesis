"""persistence/migrate.py + persistence/db.py -- migration idempotency and
schema verification against a REAL Postgres. Skipped unless TEST_DATABASE_URL
is set (see conftest.py) -- bare `pytest -q` needs no infrastructure."""

from tests.conftest import requires_db


@requires_db
def test_migration_is_idempotent(pg_db):
    from persistence.migrate import run_migrations

    # conftest's pg_db fixture already ran migrations once (to create the
    # tables it truncates) -- running again here must be a genuine no-op.
    applied = run_migrations()
    assert applied == []


@requires_db
def test_verify_schema_passes_after_migration(pg_db):
    from persistence.db import verify_schema
    assert verify_schema() is True


@requires_db
def test_verify_schema_reports_false_for_missing_table(pg_db):
    from sqlalchemy import text
    from persistence.db import connection, verify_schema
    from persistence.migrate import run_migrations

    with connection() as conn:
        conn.execute(text("DROP TABLE IF EXISTS run_validation_flags CASCADE"))
    try:
        assert verify_schema() is False
    finally:
        # Restore the DB for whatever test runs next: since migrations.sql
        # uses CREATE TABLE IF NOT EXISTS, forcing a full re-apply (by
        # un-recording 0001_initial) safely recreates just the dropped
        # table without disturbing anything else -- run_migrations() alone
        # would be a no-op here since schema_migrations still lists
        # 0001_initial as applied.
        with connection() as conn:
            conn.execute(text("DELETE FROM schema_migrations WHERE version = '0001_initial'"))
        run_migrations()
        assert verify_schema() is True


@requires_db
def test_all_expected_tables_exist(pg_db):
    from sqlalchemy import inspect
    from persistence.db import get_engine
    from persistence.schema import METADATA

    inspector = inspect(get_engine())
    existing = set(inspector.get_table_names())
    expected = set(METADATA.tables.keys())
    assert expected.issubset(existing)
