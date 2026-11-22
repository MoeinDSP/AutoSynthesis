"""Regression test for the MinerU cloud/local extractor's "asyncio.run()
cannot be called from a running event loop" failure.

In production this happened because paper_reading_agent's per-paper fetch
worker thread sometimes uses Playwright's *sync* API (the browser-fallback
strategy) earlier in the same fetch cascade, which leaves that thread's
asyncio state such that a later plain `asyncio.run()` call in
mineru_mcp_extractor.py raises RuntimeError -- failing MinerU extraction on
every paper that reached the browser fallback first. The simplest faithful
repro of "this thread already has a running event loop" is to call the
extractor from inside a coroutine that is itself being driven by
`asyncio.run()` on the same thread -- exactly the condition the error
message names, regardless of what caused it in production.
"""

import asyncio

from utils.mineru_mcp_extractor import _run_coro_isolated


async def _trivial_coro():
    return "ok"


def test_run_coro_isolated_works_even_inside_a_running_event_loop():
    async def _caller():
        # We are now executing inside asyncio.run()'s own event loop on
        # this thread -- a bare `asyncio.run(_trivial_coro())` right here
        # would raise "asyncio.run() cannot be called from a running event
        # loop", which is exactly what mineru_mcp_extractor's cloud/local
        # extractors used to do directly and would fail with in this
        # situation.
        return _run_coro_isolated(_trivial_coro)

    result = asyncio.run(_caller())
    assert result == "ok"


def test_run_coro_isolated_propagates_exceptions():
    async def _boom():
        raise ValueError("boom")

    try:
        _run_coro_isolated(_boom)
        assert False, "expected ValueError to propagate"
    except ValueError as exc:
        assert str(exc) == "boom"
