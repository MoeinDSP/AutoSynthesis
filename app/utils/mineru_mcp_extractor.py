"""MinerU PDF extractors via MCP (local pipeline or cloud API).

Two server backends share the same MCP client wiring:

  • LOCAL  — spawns `mcp-mineru` via uvx (Apple Silicon local pipeline, no API key)
  • CLOUD  — spawns `utils/mineru_cloud_mcp_server.py` (mineru.net REST API, requires MinerU_API_KEY)

Usage:
    # Cloud MCP (primary — requires MinerU_API_KEY in env)
    text = extract_text_mineru_cloud("/absolute/path/to/paper.pdf")

    # Local MCP (offline fallback — requires mcp-mineru installed via uvx)
    text = extract_text_mineru("/absolute/path/to/paper.pdf")

Install dependencies (one-time):
    pip install "mcp[cli]" requests
    uvx --from mcp-mineru python -m mcp_mineru.server --help  # for local backend
"""

import asyncio
import logging
import os
import pathlib
import shutil
import sys
import tempfile
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from utils.thread_tracking import spawn_tracked_thread

logger = logging.getLogger(__name__)


def _run_coro_isolated(coro_factory):
    """Run an asyncio coroutine to completion in a brand-new OS thread via
    asyncio.run(), instead of calling asyncio.run() directly on the calling
    thread.

    Why: this module's callers run inside paper_reading_agent's per-paper
    fetch worker thread (see FULL_TEXT_PER_PAPER_TIMEOUT_SECONDS), which
    earlier in the SAME fetch cascade may have used Playwright's *sync* API
    (the browser-fallback strategy) -- that leaves the thread's asyncio
    state such that a later plain `asyncio.run()` call on it raises
    "asyncio.run() cannot be called from a running event loop", failing
    MinerU cloud/local extraction on essentially every paper that reached
    the browser fallback first (observed in production logs). A brand-new
    thread has none of that leftover state. spawn_tracked_thread (not a
    bare threading.Thread) so this still shows up in the run's live log if
    the coroutine itself ever logs anything.
    """
    result_box: dict = {}

    def _runner():
        try:
            result_box["value"] = asyncio.run(coro_factory())
        except BaseException as exc:  # noqa: BLE001 -- re-raised on the caller's thread below
            result_box["error"] = exc

    worker = spawn_tracked_thread(target=_runner)
    worker.join()
    if "error" in result_box:
        raise result_box["error"]
    return result_box["value"]

# ── Local (uvx mcp-mineru) ────────────────────────────────────────────────────
def _find_uvx() -> Optional[str]:
    # 1. System PATH
    found = shutil.which("uvx")
    if found:
        return found
    # 2. Same bin/ as the running Python (works when venv not activated in shell)
    py_bin = os.path.dirname(sys.executable)
    candidate = os.path.join(py_bin, "uvx")
    if os.path.isfile(candidate):
        return candidate
    # 3. sys.prefix/bin (virtualenv / conda prefix)
    candidate = os.path.join(sys.prefix, "bin", "uvx")
    if os.path.isfile(candidate):
        return candidate
    return None

_UVX: Optional[str] = _find_uvx()
_DEFAULT_BACKEND = "pipeline"  # vlm-mlx-engine has MLX thread-safety issues

# ── Cloud MCP server script path ──────────────────────────────────────────────
_CLOUD_SERVER = str(pathlib.Path(__file__).parent / "mineru_cloud_mcp_server.py")


# ── Shared async MCP call ─────────────────────────────────────────────────────

async def _call_mcp_parse_pdf(
    server_params: StdioServerParameters,
    tool_args: dict,
) -> str:
    """Connect to an MCP server via stdio, call parse_pdf, return text."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("parse_pdf", tool_args)

    parts = [item.text for item in result.content if hasattr(item, "text") and item.text]
    text = "\n\n".join(parts)

    if text.startswith("❌") or text.lower().startswith("error"):
        raise RuntimeError(f"MinerU MCP error response: {text[:200]}")
    return text


# ── Cloud MCP ─────────────────────────────────────────────────────────────────

async def _async_extract_cloud(abs_path: str) -> str:
    """Call the cloud MCP server for one PDF path."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[_CLOUD_SERVER],
        env=os.environ.copy(),
    )
    return await _call_mcp_parse_pdf(
        server_params,
        {
            "file_path": abs_path,
            "enable_formula": True,
            "enable_table": True,
        },
    )


def extract_text_mineru_cloud(pdf_path: str) -> str:
    """Extract text via the MinerU cloud MCP server.

    Spawns `mineru_cloud_mcp_server.py` as a subprocess and calls its
    parse_pdf tool, which uploads to mineru.net and returns Markdown.

    Requires MinerU_API_KEY to be set in the environment.
    """
    abs_path = os.path.abspath(pdf_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    logger.info(f"[MinerU Cloud MCP] Parsing {os.path.basename(abs_path)}")
    text = _run_coro_isolated(lambda: _async_extract_cloud(abs_path))
    logger.info(f"[MinerU Cloud MCP] Extracted {len(text)} chars")
    return text


def extract_text_mineru_cloud_from_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes via the MinerU cloud MCP server."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        return extract_text_mineru_cloud(tmp_path)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# ── Local MCP (mcp-mineru via uvx) ───────────────────────────────────────────

async def _async_extract_local(
    abs_path: str,
    backend: str,
    start_page: Optional[int],
    end_page: Optional[int],
) -> str:
    if not _UVX:
        raise RuntimeError("uvx not found. Install uv: pip install uv")

    server_params = StdioServerParameters(
        command=_UVX,
        args=["--from", "mcp-mineru", "python", "-m", "mcp_mineru.server"],
        env={**os.environ, "PYTHONPATH": ""},  # isolate from project's statistics/ module
        cwd=tempfile.gettempdir(),
    )

    args: dict = {
        "file_path": abs_path,
        "backend": backend,
        "formula_enable": True,
        "table_enable": True,
    }
    if start_page is not None:
        args["start_page"] = start_page
    if end_page is not None:
        args["end_page"] = end_page

    return await _call_mcp_parse_pdf(server_params, args)


def extract_text_mineru(
    pdf_path: str,
    backend: str = _DEFAULT_BACKEND,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
) -> str:
    """Extract text via the local mcp-mineru MCP server (no API key required).

    Args:
        pdf_path:   Absolute path to the PDF file.
        backend:    "pipeline" (default) | "vlm-transformers"
        start_page: First page to parse (0-based, optional).
        end_page:   Last page to parse (0-based, inclusive, optional).
    """
    abs_path = os.path.abspath(pdf_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")

    logger.info(f"[MinerU Local MCP] Parsing {os.path.basename(abs_path)} backend={backend!r}")
    text = _run_coro_isolated(lambda: _async_extract_local(abs_path, backend, start_page, end_page))
    logger.info(f"[MinerU Local MCP] Extracted {len(text)} chars")
    return text


def extract_text_mineru_from_bytes(
    pdf_bytes: bytes,
    backend: str = _DEFAULT_BACKEND,
) -> str:
    """Extract text from PDF bytes via the local mcp-mineru MCP server."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        return extract_text_mineru(tmp_path, backend=backend)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
