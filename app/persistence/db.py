"""Lazy SQLAlchemy engine + connection helper for the persistence layer.

`DATABASE_URL` empty => `enabled()` is False and every persistence call is a
safe no-op (see `@safe` below) -- this is what makes the whole migration
additive: a checkout with no Postgres configured behaves exactly as before
this package existed.
"""

from __future__ import annotations

import functools
import logging
import threading
from contextlib import contextmanager
from typing import Any, Callable, Optional, TypeVar

import config

logger = logging.getLogger(__name__)

_engine = None
_engine_lock = threading.Lock()

F = TypeVar("F", bound=Callable[..., Any])


def enabled() -> bool:
    """True iff DATABASE_URL is configured. Every run_store function checks
    this (via @safe) before doing anything -- never assume a caller checked
    first."""
    return bool(config.DATABASE_URL)


def get_engine():
    """Lazily create (once, thread-safe) and return the SQLAlchemy engine.
    Returns None if persistence is disabled -- callers must handle that,
    which @safe does for them automatically."""
    global _engine
    if not enabled():
        return None
    if _engine is None:
        with _engine_lock:
            if _engine is None:  # re-check inside the lock
                from sqlalchemy import create_engine, event

                engine = create_engine(
                    config.DATABASE_URL,
                    pool_size=config.DB_POOL_SIZE,
                    max_overflow=config.DB_MAX_OVERFLOW,
                    pool_recycle=config.DB_POOL_RECYCLE_SECONDS,
                    pool_pre_ping=True,
                    echo=config.DB_ECHO,
                )

                if config.DB_STATEMENT_TIMEOUT_MS > 0:
                    @event.listens_for(engine, "connect")
                    def _set_statement_timeout(dbapi_conn, _record):
                        cursor = dbapi_conn.cursor()
                        cursor.execute(f"SET statement_timeout = {config.DB_STATEMENT_TIMEOUT_MS}")
                        cursor.close()

                _engine = engine
                logger.info("[DB] Engine created for %s", _safe_url(config.DATABASE_URL))
    return _engine


def _safe_url(url: str) -> str:
    """Redacts the password out of a DB URL for logging."""
    if "@" not in url:
        return url
    scheme_and_creds, rest = url.rsplit("@", 1)
    if "://" not in scheme_and_creds:
        return url
    scheme, _creds = scheme_and_creds.split("://", 1)
    return f"{scheme}://***@{rest}"


@contextmanager
def connection():
    """Yields a live SQLAlchemy Connection in a transaction (commits on
    clean exit, rolls back on exception). Raises RuntimeError if persistence
    is disabled -- callers should check `enabled()` or use `@safe` instead
    of calling this directly for anything that must degrade gracefully."""
    engine = get_engine()
    if engine is None:
        raise RuntimeError("persistence.db.connection() called but DATABASE_URL is not set")
    with engine.begin() as conn:
        yield conn


def safe(default: Any = None) -> Callable[[F], F]:
    """Decorator: if persistence is disabled, OR the wrapped function raises
    any exception talking to the database, log a warning and return
    `default` instead of propagating -- a DB outage or misconfiguration must
    never break a pipeline run. Every public run_store function is wrapped
    with this."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not enabled():
                return default
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 -- deliberately broad, see docstring
                logger.warning(
                    "[DB] %s failed, continuing without persistence: %s",
                    func.__name__, exc,
                )
                return default
        return wrapper  # type: ignore[return-value]

    return decorator


def verify_schema() -> bool:
    """Startup check: confirms every table this package expects actually
    exists (i.e. migrations have been applied). Returns True if disabled
    (nothing to verify) or if all tables are present; False otherwise --
    never raises."""
    if not enabled():
        return True
    try:
        from sqlalchemy import inspect
        from persistence.schema import METADATA

        engine = get_engine()
        inspector = inspect(engine)
        existing = set(inspector.get_table_names())
        expected = set(METADATA.tables.keys())
        missing = expected - existing
        if missing:
            logger.warning("[DB] verify_schema: missing tables %s -- run `python -m persistence.migrate`", sorted(missing))
            return False
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("[DB] verify_schema failed: %s", exc)
        return False


def dispose() -> None:
    """Closes the engine's connection pool. Mainly useful for tests that
    create/drop a database per test session."""
    global _engine
    with _engine_lock:
        if _engine is not None:
            _engine.dispose()
            _engine = None
