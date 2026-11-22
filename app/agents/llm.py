"""Shared LangChain LLM client for all agents."""
from langchain_openai import ChatOpenAI

import config
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME


class _ActiveModelChat(ChatOpenAI):
    """ChatOpenAI whose model follows config.MODEL_NAME on every request, so the
    user's per-run model choice applies to the shared `llm` that the agents
    imported at start-up (including structured-output / bound variants)."""

    def _get_request_payload(self, input_, *, stop=None, **kwargs):
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        payload["model"] = config.MODEL_NAME
        return payload


llm = _ActiveModelChat(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    timeout=180,          # 3-minute hard timeout per API call — prevents silent hangs
    max_retries=2,        # retry transient errors instead of hanging
)
