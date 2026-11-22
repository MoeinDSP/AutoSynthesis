"""Lazy Redis client + graceful-degradation helpers.

`REDIS_URL` empty => `enabled()` is False and every safe_* helper is a
no-op / returns a miss-equivalent default -- a checkout with no Redis
configured behaves exactly as before this package existed. A Redis outage
(configured but unreachable) degrades the SAME way: caught, logged
(rate-limited so a hung Redis can't flood the run's log), never raised
into the caller.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Optional

import config

logger = logging.getLogger(__name__)

_clients: dict = {}
_client_lock = threading.Lock()

# Rate-limit warning logs per (operation) so a persistently-down Redis
# doesn't spam the run log for every single PDF -- one warning per op per
# 60s is plenty to notice the problem without drowning everything else out.
_last_warned: dict = {}
_WARN_INTERVAL_SECONDS = 60


def enabled() -> bool:
    return bool(config.REDIS_URL)


def _warn_once(op: str, exc: Exception) -> None:
    now = time.monotonic()
    last = _last_warned.get(op, 0)
    if now - last >= _WARN_INTERVAL_SECONDS:
        _last_warned[op] = now
        logger.warning("[Redis] %s failed, degrading gracefully: %s", op, exc)


def get_client(db: int = 0):
    """Lazily create (once per db index, thread-safe) and return a redis.Redis
    client. Returns None if Redis is disabled."""
    if not enabled():
        return None
    if db not in _clients:
        with _client_lock:
            if db not in _clients:
                import redis as _redis

                _clients[db] = _redis.Redis.from_url(
                    config.REDIS_URL,
                    db=db,
                    socket_timeout=config.REDIS_SOCKET_TIMEOUT_SECONDS,
                    socket_connect_timeout=config.REDIS_SOCKET_TIMEOUT_SECONDS,
                    health_check_interval=30,
                )
    return _clients[db]


def safe_get(key: str, *, db: int = 0) -> Optional[bytes]:
    if not enabled():
        return None
    try:
        return get_client(db).get(key)
    except Exception as exc:  # noqa: BLE001
        _warn_once("get", exc)
        return None


def safe_set(key: str, value: Any, *, db: int = 0, ex: Optional[int] = None) -> bool:
    if not enabled():
        return False
    try:
        get_client(db).set(key, value, ex=ex if ex else None)
        return True
    except Exception as exc:  # noqa: BLE001
        _warn_once("set", exc)
        return False


def safe_incr(key: str, *, db: int = 0, amount: int = 1) -> Optional[int]:
    if not enabled():
        return None
    try:
        return get_client(db).incrby(key, amount)
    except Exception as exc:  # noqa: BLE001
        _warn_once("incr", exc)
        return None


def safe_publish(channel: str, message: Any, *, db: int = 0) -> bool:
    if not enabled():
        return False
    try:
        get_client(db).publish(channel, message)
        return True
    except Exception as exc:  # noqa: BLE001
        _warn_once("publish", exc)
        return False


def dispose() -> None:
    """Closes all client connection pools. Mainly for tests."""
    global _clients
    with _client_lock:
        for client in _clients.values():
            try:
                client.close()
            except Exception:  # noqa: BLE001
                pass
        _clients = {}
