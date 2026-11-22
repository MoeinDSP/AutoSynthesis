"""Applies unapplied migrations/*.sql files, in filename order, recording
each in `schema_migrations`. Idempotent: running twice is a no-op the
second time. Deliberately NOT Alembic -- autogenerate needs a declarative
metadata + its own config framework (alembic.ini, env.py, a versions/
directory with its own conventions) that's disproportionate for ~15 tables
that change rarely; plain, reviewable, greppable .sql files plus this
~40-line runner is proportionate to the rest of this codebase's style
(core_utils.py's small-helpers convention).

CLI usage:
    python -m persistence.migrate
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import config
from persistence.db import get_engine, enabled

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _discover_migrations() -> list[Path]:
    return sorted(MIGRATIONS_DIR.glob("*.sql"))


def run_migrations() -> list[str]:
    """Applies every migration not yet recorded in schema_migrations, each
    inside its own transaction. Returns the list of version strings newly
    applied (empty if everything was already applied, or if persistence is
    disabled). Raises on a genuine SQL error -- unlike run_store's
    @safe-wrapped functions, a failed migration should NOT be silently
    swallowed; the caller (the `migrate` APP_ROLE, or a test) needs to know."""
    if not enabled():
        logger.info("[Migrate] DATABASE_URL not set -- nothing to do.")
        return []

    from sqlalchemy import text

    engine = get_engine()
    applied: list[str] = []

    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
        ))
        already = {row[0] for row in conn.execute(text("SELECT version FROM schema_migrations"))}

    for path in _discover_migrations():
        version = path.stem
        if version in already:
            logger.info("[Migrate] %s already applied, skipping.", version)
            continue
        sql = path.read_text()
        logger.info("[Migrate] Applying %s...", version)
        with engine.begin() as conn:
            conn.execute(text(sql))
            conn.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:v)"),
                {"v": version},
            )
        applied.append(version)
        logger.info("[Migrate] %s applied.", version)

    if not applied:
        logger.info("[Migrate] Nothing to apply -- schema already up to date.")
    return applied


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)s %(message)s")
    if not config.DATABASE_URL:
        logger.error("[Migrate] DATABASE_URL is not set -- refusing to run (nothing to migrate).")
        return 1
    try:
        applied = run_migrations()
    except Exception:
        logger.exception("[Migrate] Migration failed.")
        return 1
    logger.info("[Migrate] Done. Applied: %s", applied or "(none -- already up to date)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
