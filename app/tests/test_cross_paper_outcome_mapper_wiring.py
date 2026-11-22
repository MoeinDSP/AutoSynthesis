"""
agents/cross_paper_outcome_mapper_agent.py -- the two-pass, closed-vocabulary
outcome classification, and the mapped_results -> paper_results wiring fix.

Root causes this covers:
  1. mapping_node computed outcome_family (and follow_up_timepoint) per row
     and saved them to mapped_results.json, but used to return ONLY
     {"mapped_results": merged} -- export_table_node (the very next pipeline
     stage) reads state["paper_results"], which mapping_node never updated,
     so the classification was silently discarded before it could reach
     EffectSizeRecord/pooling. mapping_node must now also return
     "paper_results" so the enriched rows actually propagate downstream.
  2. The original single-pass design merged the LLM's output back onto rows
     via an EXACT STRING match on source_outcome_name -- any row the LLM
     paraphrased, or never called the tool for, silently got
     outcome_family="" and fell into the undifferentiated "default" pooling
     bucket. The fix merges by row_index instead, which survives arbitrary
     paraphrasing of source_outcome_name, and rows the LLM genuinely never
     classifies are now explicitly flagged (ValidationFlag), not silent.
"""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

# Must be imported before agents.cross_paper_outcome_mapper_agent (which
# itself imports from pipeline_graph) -- otherwise build_graph() tries to
# import agents.cross_paper_outcome_mapper_agent while it's still mid-import,
# a circular-import hazard documented in agents/planning_agent.py.
import pipeline_graph  # noqa: F401


def _fake_messages(tool_name: str, calls: list) -> list:
    """Build a fake react-agent message history with one call to `tool_name`
    per dict in `calls`."""
    messages = [HumanMessage(content="...")]
    for i, args in enumerate(calls):
        messages.append(AIMessage(content="", tool_calls=[{
            "name": tool_name, "args": args, "id": f"{tool_name}_{i}",
        }]))
        messages.append(ToolMessage(content="ok", tool_call_id=f"{tool_name}_{i}"))
    messages.append(AIMessage(content="Done."))
    return messages


def _run_mapping_node(paper_results, mapped_calls, tmp_path, taxonomy_families=None, taxonomy_timepoints=None, plan=None):
    """Patch create_react_agent so the Phase 1 (taxonomy) call and Phase 2
    (classify) call each get their own fake agent, distinguished by which
    tool was bound to them -- mapping_node calls create_react_agent twice,
    once per phase."""
    from agents.cross_paper_outcome_mapper_agent import mapping_node

    taxonomy_families = taxonomy_families if taxonomy_families is not None else [
        {"name": "subjective_cognitive_function", "description": "d", "synonyms": []},
        {"name": "some_family", "description": "d", "synonyms": []},
    ]
    taxonomy_timepoints = taxonomy_timepoints if taxonomy_timepoints is not None else []

    taxonomy_agent = MagicMock()
    taxonomy_agent.invoke.return_value = {
        "messages": _fake_messages(
            "record_outcome_taxonomy",
            [{"families": taxonomy_families, "timepoints": taxonomy_timepoints}],
        )
    }
    classify_agent = MagicMock()
    classify_agent.invoke.return_value = {
        "messages": _fake_messages("record_mapped_result", mapped_calls)
    }

    def _create_react_agent_side_effect(model, tools, prompt=None):
        tool_name = tools[0].name
        return taxonomy_agent if tool_name == "record_outcome_taxonomy" else classify_agent

    with patch(
        "agents.cross_paper_outcome_mapper_agent.create_react_agent",
        side_effect=_create_react_agent_side_effect,
    ):
        state = {
            "paper_results": paper_results,
            "user_prompt": "does X improve subjective memory?",
            "output_dir": str(tmp_path),
            "plan": plan,
        }
        return mapping_node(state)


def test_mapping_node_writes_outcome_family_back_into_paper_results(tmp_path):
    paper_results = [
        {"paper_id": "p1", "outcome_name": "PROMIS Cognitive Abilities", "n_total": 50},
    ]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "PROMIS Cognitive Abilities",
        "research_question_id": "RQ1",
        "research_question_text": "does X improve subjective memory?",
        "target_construct": "subjective memory",
        "outcome_family": "subjective_cognitive_function",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)

    # The critical wiring fix: "paper_results" must reflect the mapping,
    # not just "mapped_results".
    assert "paper_results" in result
    assert result["paper_results"][0]["outcome_family"] == "subjective_cognitive_function"
    assert result["paper_results"] == result["mapped_results"]
    # Original fields are preserved (union, not replacement).
    assert result["paper_results"][0]["paper_id"] == "p1"
    assert result["paper_results"][0]["n_total"] == 50


def test_mapping_node_merges_by_row_index_even_if_llm_paraphrases_name(tmp_path):
    # Regression test for the exact-string-merge bug: the LLM's echoed
    # source_outcome_name doesn't need to match byte-for-byte -- row_index
    # is what actually drives the merge.
    paper_results = [
        {"paper_id": "p1", "outcome_name": "PROMIS Cognitive Abilities (self-report)", "n_total": 50},
    ]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "PROMIS cognitive abilities",  # paraphrased, not exact
        "research_question_id": "RQ1",
        "research_question_text": "x",
        "target_construct": "subjective memory",
        "outcome_family": "subjective_cognitive_function",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)
    assert result["paper_results"][0]["outcome_family"] == "subjective_cognitive_function"


def test_mapping_node_flags_row_the_llm_never_classified(tmp_path):
    paper_results = [
        {"paper_id": "p1", "outcome_name": "Outcome A", "n_total": 50},
        {"paper_id": "p2", "outcome_name": "Outcome B", "n_total": 40},
    ]
    tool_calls = [{
        "row_index": 0,  # only row 0 classified -- row 1 silently skipped by the LLM
        "source_outcome_name": "Outcome A",
        "research_question_id": "RQ1",
        "research_question_text": "x",
        "target_construct": "a",
        "outcome_family": "some_family",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)

    assert result["paper_results"][0]["outcome_family"] == "some_family"
    assert result["paper_results"][1]["outcome_family"] == ""  # not silently defaulted to a guess

    flags = result["validation_flags"]
    assert any(
        f.stage == "outcome_classification" and f.severity == "warning" and "p2" == f.subject_id
        for f in flags
    )


def test_mapping_node_unclassified_sentinel_leaves_row_unclassified_not_forced(tmp_path):
    paper_results = [{"paper_id": "p1", "outcome_name": "Some odd outcome", "n_total": 40}]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Some odd outcome",
        "research_question_id": "RQ1",
        "research_question_text": "x",
        "target_construct": "x",
        "outcome_family": "UNCLASSIFIED",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)
    assert result["paper_results"][0]["outcome_family"] == ""
    flags = result["validation_flags"]
    assert any(f.stage == "outcome_classification" and f.severity == "info" for f in flags)


def test_mapping_node_captures_follow_up_timepoint(tmp_path):
    paper_results = [
        {"paper_id": "p1", "outcome_name": "Subjective memory (3-month follow-up)", "n_total": 40},
    ]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Subjective memory (3-month follow-up)",
        "research_question_id": "RQ1",
        "research_question_text": "does X improve subjective memory?",
        "target_construct": "subjective memory",
        "outcome_family": "subjective_cognitive_function",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
        "follow_up_timepoint": "intermediate (1-6 months)",
    }]
    result = _run_mapping_node(
        paper_results, tool_calls, tmp_path,
        taxonomy_timepoints=[{"name": "intermediate (1-6 months)", "description": "d"}],
    )
    assert result["paper_results"][0]["follow_up_timepoint"] == "intermediate (1-6 months)"


def test_mapping_node_drops_timepoint_not_in_closed_vocabulary(tmp_path):
    # If the batch defined no (or a different) timepoint vocabulary in
    # Phase 1, a stray/non-canonical label must be dropped to null rather
    # than fragmenting the pooling key with a one-off string -- the direct
    # fix for the 21-distinct-raw-timepoint-strings bug.
    paper_results = [{"paper_id": "p1", "outcome_name": "Some outcome", "n_total": 40}]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Some outcome",
        "research_question_id": "RQ1",
        "research_question_text": "x",
        "target_construct": "x",
        "outcome_family": "some_family",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
        "follow_up_timepoint": "some ad hoc label the model made up",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path, taxonomy_timepoints=[])
    assert result["paper_results"][0]["follow_up_timepoint"] is None


def test_mapping_node_nulls_a_self_contradicting_long_term_misclassification(tmp_path):
    paper_results = [{
        "paper_id": "p1",
        "outcome_name": "Baseline-to-long-term-follow-up change in self-reported memory",
        "evidence_quote": "change score from baseline to the long-term follow-up assessment",
        "n_total": 28,
    }]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Baseline-to-long-term-follow-up change in self-reported memory",
        "research_question_id": "RQ1", "research_question_text": "x",
        "target_construct": "subjective memory", "outcome_family": "subjective_cognitive_function",
        "comparison_family": "intervention_vs_control", "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True, "conversion_priority": "direct",
        "follow_up_timepoint": "intermediate follow-up (1-6 months)",
    }]
    result = _run_mapping_node(
        paper_results, tool_calls, tmp_path,
        taxonomy_timepoints=[
            {"name": "intermediate follow-up (1-6 months)", "description": "d"},
            {"name": "long-term follow-up (>6 months)", "description": "d"},
        ],
    )
    assert result["paper_results"][0]["follow_up_timepoint"] is None
    flags = result["validation_flags"]
    assert any(
        f.stage == "outcome_classification" and f.severity == "warning"
        and f.subject_id == "p1" and "long-term" in f.message
        for f in flags
    )


def test_mapping_node_does_not_null_a_genuinely_correct_long_term_classification(tmp_path):
    paper_results = [{"paper_id": "p1", "outcome_name": "Long-term follow-up memory score", "n_total": 40}]
    tool_calls = [{
        "row_index": 0, "source_outcome_name": "Long-term follow-up memory score",
        "research_question_id": "RQ1", "research_question_text": "x",
        "target_construct": "subjective memory", "outcome_family": "subjective_cognitive_function",
        "comparison_family": "intervention_vs_control", "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True, "conversion_priority": "direct",
        "follow_up_timepoint": "long-term follow-up (>6 months)",
    }]
    result = _run_mapping_node(
        paper_results, tool_calls, tmp_path,
        taxonomy_timepoints=[{"name": "long-term follow-up (>6 months)", "description": "d"}],
    )
    assert result["paper_results"][0]["follow_up_timepoint"] == "long-term follow-up (>6 months)"
    assert not any(f.subject_id == "p1" for f in result["validation_flags"])


def test_mapping_node_leaves_timepoint_null_when_not_stated(tmp_path):
    paper_results = [{"paper_id": "p1", "outcome_name": "Some outcome", "n_total": 40}]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Some outcome",
        "research_question_id": "RQ1",
        "research_question_text": "x",
        "target_construct": "x",
        "outcome_family": "some_family",
        "comparison_family": "intervention_vs_control",
        "effect_direction": "higher_is_better",
        "meta_analysis_candidate": True,
        "conversion_priority": "direct",
        # follow_up_timepoint omitted -- must not be guessed/invented.
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)
    assert result["paper_results"][0]["follow_up_timepoint"] is None


def test_mapping_node_no_results_returns_empty_without_calling_agent(tmp_path):
    from agents.cross_paper_outcome_mapper_agent import mapping_node

    with patch("agents.cross_paper_outcome_mapper_agent.create_react_agent") as mock_create:
        result = mapping_node({"paper_results": [], "user_prompt": "x", "output_dir": str(tmp_path)})
    mock_create.assert_not_called()
    assert result == {"mapped_results": []}


# ---------------------------------------------------------------------------
# models.MetaAnalysisPlan.single_outcome_target -- when the plan declares one
# explicit target outcome, Phase 1's freely-invented per-instrument
# sub-families (e.g. "PANSS positive symptoms" vs "BPRS positive symptoms")
# must collapse into that ONE family instead of fragmenting the pool. Root
# cause: a real test run (single-outcome-scoped prompt over 25 papers,
# CD015331) confirmed this fragmentation happened even with a single
# declared target outcome, purely because of which rating scale each study
# used -- see models.py and agents/cross_paper_outcome_mapper_agent.py.
# ---------------------------------------------------------------------------

def _plan(**kwargs):
    from models import MetaAnalysisPlan
    defaults = dict(
        research_question="q", treatment_label="t", control_label="c",
        outcome_description="o", positive_direction="p", search_queries=[],
        inclusion_criteria=[], exclusion_criteria=[], moderators_to_extract=[],
    )
    defaults.update(kwargs)
    return MetaAnalysisPlan(**defaults)


def test_single_outcome_target_collapses_multiple_taxonomy_families(tmp_path):
    paper_results = [
        {"paper_id": "p1", "outcome_name": "PANSS positive symptoms", "n_total": 40},
        {"paper_id": "p2", "outcome_name": "BPRS positive symptoms", "n_total": 40},
        {"paper_id": "p3", "outcome_name": "positive symptoms of psychosis", "n_total": 40},
    ]
    # Phase 1 (taxonomy) proposes TWO instrument-specific families, exactly
    # the fragmentation bug this override exists to prevent.
    taxonomy_families = [
        {"name": "PANSS positive symptoms", "description": "d", "synonyms": []},
        {"name": "BPRS positive symptoms", "description": "d", "synonyms": []},
    ]
    tool_calls = [
        {
            "row_index": 0, "source_outcome_name": "PANSS positive symptoms",
            "research_question_id": "RQ1", "research_question_text": "x",
            "target_construct": "positive symptoms", "outcome_family": "positive symptoms of psychosis",
            "comparison_family": None, "effect_direction": "favor intervention",
            "meta_analysis_candidate": True, "conversion_priority": "direct",
        },
        {
            "row_index": 1, "source_outcome_name": "BPRS positive symptoms",
            "research_question_id": "RQ1", "research_question_text": "x",
            "target_construct": "positive symptoms", "outcome_family": "positive symptoms of psychosis",
            "comparison_family": None, "effect_direction": "favor intervention",
            "meta_analysis_candidate": True, "conversion_priority": "direct",
        },
        {
            "row_index": 2, "source_outcome_name": "positive symptoms of psychosis",
            "research_question_id": "RQ1", "research_question_text": "x",
            "target_construct": "positive symptoms", "outcome_family": "positive symptoms of psychosis",
            "comparison_family": None, "effect_direction": "favor intervention",
            "meta_analysis_candidate": True, "conversion_priority": "direct",
        },
    ]
    plan = _plan(single_outcome_target="positive symptoms of psychosis")
    result = _run_mapping_node(
        paper_results, tool_calls, tmp_path,
        taxonomy_families=taxonomy_families, plan=plan,
    )
    families_used = {r["outcome_family"] for r in result["paper_results"]}
    # All three rows collapse into ONE family regardless of instrument --
    # never split into "PANSS positive symptoms" / "BPRS positive symptoms".
    assert families_used == {"positive symptoms of psychosis"}


def test_single_outcome_target_tool_rejects_other_family_names(tmp_path):
    # Direct tool-level check (not just the mock-agent merge path): once the
    # override is active, record_mapped_result's OWN validation must refuse
    # an outcome_family that isn't the one collapsed target -- not just rely
    # on the classify prompt asking nicely.
    from agents.cross_paper_outcome_mapper_agent import _make_record_mapped_result

    valid_names = {"positive symptoms of psychosis": "positive symptoms of psychosis"}
    tool = _make_record_mapped_result(valid_names, {})
    result = tool.func(
        row_index=0, source_outcome_name="x", research_question_id="RQ1",
        research_question_text="x", target_construct="x",
        outcome_family="PANSS positive symptoms",  # an instrument-specific name, not the target
        effect_direction="favor intervention", meta_analysis_candidate=True,
        conversion_priority="direct", conversion_reason="x",
    )
    assert result.startswith("ERROR")
    assert "positive symptoms of psychosis" in result


def test_no_single_outcome_target_leaves_multi_family_taxonomy_untouched(tmp_path):
    # Backward compatibility: without single_outcome_target set (the normal,
    # multi-outcome case), Phase 1's own multi-family taxonomy must be used
    # as-is -- this override must never activate unless the plan explicitly
    # asks for it.
    paper_results = [
        {"paper_id": "p1", "outcome_name": "PANSS positive symptoms", "n_total": 40},
        {"paper_id": "p2", "outcome_name": "PANSS negative symptoms", "n_total": 40},
    ]
    taxonomy_families = [
        {"name": "PANSS positive symptoms", "description": "d", "synonyms": []},
        {"name": "PANSS negative symptoms", "description": "d", "synonyms": []},
    ]
    tool_calls = [
        {
            "row_index": 0, "source_outcome_name": "PANSS positive symptoms",
            "research_question_id": "RQ1", "research_question_text": "x",
            "target_construct": "x", "outcome_family": "PANSS positive symptoms",
            "comparison_family": None, "effect_direction": "favor intervention",
            "meta_analysis_candidate": True, "conversion_priority": "direct",
        },
        {
            "row_index": 1, "source_outcome_name": "PANSS negative symptoms",
            "research_question_id": "RQ1", "research_question_text": "x",
            "target_construct": "x", "outcome_family": "PANSS negative symptoms",
            "comparison_family": None, "effect_direction": "favor intervention",
            "meta_analysis_candidate": True, "conversion_priority": "direct",
        },
    ]
    plan = _plan(single_outcome_target=None)
    result = _run_mapping_node(
        paper_results, tool_calls, tmp_path,
        taxonomy_families=taxonomy_families, plan=plan,
    )
    families_used = {r["outcome_family"] for r in result["paper_results"]}
    assert families_used == {"PANSS positive symptoms", "PANSS negative symptoms"}


def test_mismatched_comparator_type_flows_through_via_comparison_family(tmp_path):
    # Wiring check for the real CD013591 bug: a trial comparing two versions
    # of the same smartphone app (no true no/minimal-intervention arm at
    # all) was pooled into an "app vs no/minimal intervention" analysis it
    # never belonged to. The fix is prompt-only (agents/
    # cross_paper_outcome_mapper_agent.py's comparison_family guidance) --
    # this test proves the WIRING half: once the classifier correctly
    # recognizes and labels a mismatched comparator via comparison_family,
    # that label survives into paper_results (which
    # utils/outcome_grouping.py's build_outcome_group_key downstream keys
    # pooling groups on -- see test_meta_analysis_node_grouping.py's
    # test_different_comparisons_on_same_outcome_are_pooled_separately for
    # proof that a distinct comparison_family value produces a distinct,
    # separately-pooled group). Whether the LLM classifier actually makes
    # this call on real papers is a live-run question, not a unit-testable
    # one -- this only confirms the field is honored once set.
    paper_results = [
        {"paper_id": "p1", "outcome_name": "Body weight change over 3 months", "n_total": 15},
    ]
    tool_calls = [{
        "row_index": 0,
        "source_outcome_name": "Body weight change over 3 months",
        "research_question_id": "RQ1", "research_question_text": "x",
        "target_construct": "body weight", "outcome_family": "anthropometric_measures",
        "comparison_family": "app_vs_app",
        "effect_direction": "lower_is_better",
        "meta_analysis_candidate": True, "conversion_priority": "direct",
    }]
    result = _run_mapping_node(paper_results, tool_calls, tmp_path)
    assert result["paper_results"][0]["comparison_family"] == "app_vs_app"
