# tests/test_graph_utils.py
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def test_extract_tool_args_finds_named_tool():
    from pipeline_graph import _extract_tool_args

    messages = [
        HumanMessage(content="Do the thing"),
        AIMessage(content="", tool_calls=[{
            "name": "create_plan",
            "args": {"research_question": "Does X affect Y?", "treatment_label": "X"},
            "id": "call_abc",
        }]),
        ToolMessage(content="plan_created", tool_call_id="call_abc"),
        AIMessage(content="Done."),
    ]
    args = _extract_tool_args(messages, "create_plan")
    assert args["research_question"] == "Does X affect Y?"
    assert args["treatment_label"] == "X"


def test_extract_tool_args_returns_empty_when_not_found():
    from pipeline_graph import _extract_tool_args

    messages = [HumanMessage(content="hello"), AIMessage(content="world")]
    args = _extract_tool_args(messages, "nonexistent_tool")
    assert args == {}


def test_extract_tool_args_returns_last_call_when_multiple():
    from pipeline_graph import _extract_tool_args

    messages = [
        AIMessage(content="", tool_calls=[{
            "name": "record_plan", "args": {"step": "first"}, "id": "c1",
        }]),
        ToolMessage(content="ok", tool_call_id="c1"),
        AIMessage(content="", tool_calls=[{
            "name": "record_plan", "args": {"step": "second"}, "id": "c2",
        }]),
    ]
    args = _extract_tool_args(messages, "record_plan")
    assert args["step"] == "second"
