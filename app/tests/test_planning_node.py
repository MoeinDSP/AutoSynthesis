# tests/test_planning_node.py
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import pipeline_graph  # noqa: F401  (loads agents.planning_agent so patch() can resolve it)


def _fake_messages(tool_name: str, args: dict) -> list:
    return [
        HumanMessage(content="Design a plan..."),
        AIMessage(content="", tool_calls=[{
            "name": tool_name, "args": args, "id": "call_1",
        }]),
        ToolMessage(content="plan_created", tool_call_id="call_1"),
        AIMessage(content="Plan recorded."),
    ]


def test_plan_node_returns_meta_analysis_plan():
    args = {
        "research_question": "Does X affect Y?",
        "treatment_label": "X group",
        "control_label": "Control",
        "outcome_description": "Y score",
        "positive_direction": "Higher is better",
        "higher_score_is_worse": False,
        "search_queries": ["X Y effect"],
        "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"],
        "moderators_to_extract": ["year"],
        "search_start_year": 2015,
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Does X affect Y?",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].research_question == "Does X affect Y?"
    assert result["plan"].treatment_label == "X group"
    assert result["plan"].search_start_year == 2015
    # split_by_timepoint defaults to False when the LLM doesn't set it --
    # never accidentally enables timepoint fragmentation.
    assert result["plan"].split_by_timepoint is False


def test_plan_node_respects_explicit_split_by_timepoint_request():
    args = {
        "research_question": "Does X affect Y?",
        "treatment_label": "X group",
        "control_label": "Control",
        "outcome_description": "Y score",
        "positive_direction": "Higher is better",
        "higher_score_is_worse": False,
        "search_queries": ["X Y effect"],
        "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"],
        "moderators_to_extract": ["year"],
        "search_start_year": 2015,
        "split_by_timepoint": True,
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Does X affect Y, reported separately at 3 and 12 months?",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].split_by_timepoint is True


def test_plan_node_respects_explicit_risk_difference_request():
    """Real CD010592 bug: the planning LLM was never told RD/HR are valid
    target_effect_measure choices (only RR/OR/PETO_OR/MD/SMD/HEDGES_G/
    GENERIC were listed), so a user explicitly asking to "pool using risk
    difference" fell back to GENERIC and the native RD support added in
    utils/effect_measures.py never even got invoked. This guards the fix at
    the layer that actually broke: the LLM's own args, not the coercion
    logic (already correct) below it."""
    from models import EffectMeasure

    args = {
        "research_question": "Does X affect epistaxis risk?",
        "treatment_label": "INCS", "control_label": "Placebo",
        "outcome_description": "Epistaxis", "positive_direction": "Lower is better", "higher_score_is_worse": True,
        "search_queries": ["INCS epistaxis"], "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"], "moderators_to_extract": ["dose"],
        "search_start_year": 1990,
        "target_effect_measure": "RD",
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Pool using risk difference (RD).",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].target_effect_measure == EffectMeasure.RD


def test_plan_node_respects_explicit_hazard_ratio_request():
    """HR was likewise missing from the allowed-values list despite already
    being fully implemented in utils/effect_measures.py."""
    from models import EffectMeasure

    args = {
        "research_question": "Does X affect survival?",
        "treatment_label": "X group", "control_label": "Control",
        "outcome_description": "Overall survival", "positive_direction": "Lower is better", "higher_score_is_worse": True,
        "search_queries": ["X survival"], "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"], "moderators_to_extract": ["year"],
        "search_start_year": 2000,
        "target_effect_measure": "HR",
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Pool using hazard ratio (HR).",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].target_effect_measure == EffectMeasure.HR


def test_plan_node_respects_explicit_single_outcome_target():
    args = {
        "research_question": "Does X affect positive symptoms of psychosis?",
        "treatment_label": "X group",
        "control_label": "Control",
        "outcome_description": "Positive symptoms",
        "positive_direction": "Higher is better",
        "higher_score_is_worse": False,
        "search_queries": ["X positive symptoms"],
        "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"],
        "moderators_to_extract": ["year"],
        "search_start_year": 2015,
        "single_outcome_target": "positive symptoms of psychosis",
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Does X affect positive symptoms of psychosis?",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].single_outcome_target == "positive symptoms of psychosis"


def test_plan_node_single_outcome_target_defaults_to_none():
    args = {
        "research_question": "Does X affect Y?",
        "treatment_label": "X group",
        "control_label": "Control",
        "outcome_description": "Y score",
        "positive_direction": "Higher is better",
        "higher_score_is_worse": False,
        "search_queries": ["X Y effect"],
        "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"],
        "moderators_to_extract": ["year"],
        "search_start_year": 2015,
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Does X affect Y?",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    # Never accidentally activated -- the normal, multi-outcome case.
    assert result["plan"].single_outcome_target is None


def test_plan_node_blank_single_outcome_target_coerced_to_none():
    args = {
        "research_question": "Does X affect Y?",
        "treatment_label": "X group",
        "control_label": "Control",
        "outcome_description": "Y score",
        "positive_direction": "Higher is better",
        "higher_score_is_worse": False,
        "search_queries": ["X Y effect"],
        "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"],
        "moderators_to_extract": ["year"],
        "search_start_year": 2015,
        "single_outcome_target": "   ",  # whitespace-only from the LLM
    }
    mock_result = {"messages": _fake_messages("create_plan", args)}

    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        result = plan_node({
            "user_prompt": "Does X affect Y?",
            "output_dir": "/tmp", "mode": "search",
            "paper_files": [],
        })

    assert result["plan"].single_outcome_target is None


def test_plan_node_raises_on_no_tool_call():
    mock_result = {"messages": [
        HumanMessage(content="Design a plan"),
        AIMessage(content="I cannot help."),
    ]}
    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = mock_result
        from agents.planning_agent import plan_node
        import pytest
        with pytest.raises(RuntimeError, match="Failed to generate"):
            plan_node({"user_prompt": "test", "output_dir": "/tmp",
                       "mode": "search", "paper_files": []})


def _base_args(**extra):
    args = {
        "research_question": "Does X affect Y?", "treatment_label": "X group", "control_label": "Control",
        "outcome_description": "Y score", "positive_direction": "Higher is better",
        "higher_score_is_worse": False, "search_queries": ["X Y effect"], "inclusion_criteria": ["RCT"],
        "exclusion_criteria": ["reviews"], "moderators_to_extract": ["year"], "search_start_year": 2015,
    }
    args.update(extra)
    return args


def _run_plan(args, **state_extra):
    with patch("agents.planning_agent._agent") as mock_agent:
        mock_agent.invoke.return_value = {"messages": _fake_messages("create_plan", args)}
        from agents.planning_agent import plan_node
        state = {"user_prompt": "Does X affect Y?", "output_dir": "/tmp", "mode": "search", "paper_files": []}
        state.update(state_extra)
        return plan_node(state)["plan"]


def test_pooling_model_defaults_to_none():
    assert _run_plan(_base_args()).pooling_model is None


def test_pooling_model_from_prompt_is_kept_and_normalized():
    assert _run_plan(_base_args(pooling_model="fixed")).pooling_model == "FE"
    assert _run_plan(_base_args(pooling_model="uwls")).pooling_model == "UWLS"


def test_dashboard_pooling_model_overrides_prompt():
    assert _run_plan(_base_args(pooling_model="DL"), pooling_model="PM").pooling_model == "PM"


def test_unknown_pooling_model_is_dropped():
    assert _run_plan(_base_args(pooling_model="bayesian-magic")).pooling_model is None
