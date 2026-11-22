# tests/test_llm_client.py
def test_llm_client_is_chat_openai():
    from agents.llm import llm
    from langchain_openai import ChatOpenAI
    assert isinstance(llm, ChatOpenAI)

def test_llm_client_uses_openrouter_base_url():
    from agents.llm import llm
    from config import OPENROUTER_BASE_URL
    assert llm.openai_api_base == OPENROUTER_BASE_URL or \
           str(llm.base_url) == OPENROUTER_BASE_URL
