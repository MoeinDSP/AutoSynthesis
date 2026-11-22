"""persistence/graph_state_codec.py -- JSON-safe GraphState round-trip.

Correctness-critical subset (per the infra-migration plan): at the two
pause boundaries this pipeline actually persists mid-run
(run_pause_states), only `plan`/`papers_eligible`/`all_retrieved_papers`
are populated -- nothing downstream of eligibility_node has run yet. Those
round-tripping to deep-equality is what matters most for correctness; the
rest (effect_sizes, meta_results, etc.) only matter for the terminal
snapshot, where a codec bug can't corrupt an in-flight run, but are still
tested here for full coverage.

No database needed -- these are pure functions of a dict.
"""

import pytest

from models import (
    MetaAnalysisPlan, PaperRecord, EffectSizeRecord, MetaAnalysisResult,
    MetaAnalysisGroupResult, ModeratorResult, BiasResult, RiskOfBiasAssessment,
    ValidationFlag, EffectMeasure,
)
from persistence.graph_state_codec import dump_graph_state, load_graph_state


def _plan(**kwargs):
    defaults = dict(
        research_question="q", treatment_label="t", control_label="c",
        outcome_description="o", positive_direction="p", search_queries=["a"],
        inclusion_criteria=["i"], exclusion_criteria=["e"], moderators_to_extract=["m"],
    )
    defaults.update(kwargs)
    return MetaAnalysisPlan(**defaults)


def _paper(**kwargs):
    defaults = dict(id="p1", title="T", abstract="A", authors=["X", "Y"],
                     year=2020, source="pubmed", full_text="full text")
    defaults.update(kwargs)
    return PaperRecord(**defaults)


def _es(**kwargs):
    defaults = dict(
        study_id="s1", report_id="r1", cohens_d=0.3, hedges_g=0.3,
        variance=0.02, se=0.14, ci_lower=0.02, ci_upper=0.58, n_total=50,
        computation_method="means_sds",
    )
    defaults.update(kwargs)
    return EffectSizeRecord(**defaults)


def _meta_result(**kwargs):
    defaults = dict(
        pooled_g=0.4, pooled_se=0.1, ci_lower=0.2, ci_upper=0.6,
        z_value=4.0, p_value=0.001, tau_squared=0.01, tau=0.1,
        i_squared=20.0, h_squared=1.2, q_statistic=5.0, q_df=4,
        q_p_value=0.3, k=5, n_total=250,
    )
    defaults.update(kwargs)
    return MetaAnalysisResult(**defaults)


class TestSingleModelKeys:
    def test_plan_round_trips_to_deep_equality(self):
        plan = _plan()
        state = {"plan": plan}
        loaded = load_graph_state(dump_graph_state(state))
        assert isinstance(loaded["plan"], MetaAnalysisPlan)
        assert loaded["plan"] == plan

    def test_meta_result_round_trips(self):
        result = _meta_result()
        state = {"meta_result": result}
        loaded = load_graph_state(dump_graph_state(state))
        assert loaded["meta_result"] == result

    def test_bias_result_round_trips(self):
        bias = BiasResult(
            eggers_intercept=0.1, eggers_se=0.05, eggers_t_value=2.0, eggers_p_value=0.04,
            trim_fill_k0=0, trim_fill_side="none", trim_fill_g=0.4,
            trim_fill_ci_lower=0.2, trim_fill_ci_upper=0.6, bias_risk="low",
        )
        loaded = load_graph_state(dump_graph_state({"bias_result": bias}))
        assert loaded["bias_result"] == bias

    def test_none_stays_none(self):
        loaded = load_graph_state(dump_graph_state({"plan": None, "meta_result": None}))
        assert loaded["plan"] is None
        assert loaded["meta_result"] is None


class TestListModelKeys:
    def test_papers_eligible_round_trips(self):
        papers = [_paper(id="p1"), _paper(id="p2", trial_cluster_id="cluster-1")]
        loaded = load_graph_state(dump_graph_state({"papers_eligible": papers}))
        assert loaded["papers_eligible"] == papers

    def test_all_retrieved_papers_round_trips(self):
        papers = [_paper(id="p1"), _paper(id="p2")]
        loaded = load_graph_state(dump_graph_state({"all_retrieved_papers": papers}))
        assert loaded["all_retrieved_papers"] == papers

    def test_effect_sizes_round_trip_including_enum_fields(self):
        rows = [_es(study_id="s1", effect_measure=EffectMeasure.HR),
                _es(study_id="s2", effect_measure=EffectMeasure.RR)]
        loaded = load_graph_state(dump_graph_state({"effect_sizes": rows}))
        assert loaded["effect_sizes"] == rows
        assert loaded["effect_sizes"][0].effect_measure == EffectMeasure.HR

    def test_meta_results_group_list_round_trips(self):
        groups = [MetaAnalysisGroupResult(
            outcome_group_key="mortality", label="mortality", k=3, n_total=150,
            study_ids=["s1", "s2", "s3"], insufficient_data=False,
            result=_meta_result(),
        )]
        loaded = load_graph_state(dump_graph_state({"meta_results": groups}))
        assert loaded["meta_results"] == groups

    def test_moderator_results_round_trip(self):
        mods = [ModeratorResult(moderator_name="design", qm_statistic=1.0, qm_df=1, qm_p_value=0.3,
                                 subgroups=[], reference_category="RCT", coefficients=[])]
        loaded = load_graph_state(dump_graph_state({"moderator_results": mods}))
        assert loaded["moderator_results"] == mods

    def test_rob_assessments_round_trip(self):
        robs = [RiskOfBiasAssessment(
            paper_id="p1", paper_title="T", design_classification="randomized",
            design_rationale="r", tool_used="RoB2", overall_risk="low",
            overall_summary="s", domain_judgments=[],
        )]
        loaded = load_graph_state(dump_graph_state({"rob_assessments": robs}))
        assert loaded["rob_assessments"] == robs

    def test_validation_flags_round_trip(self):
        flags = [ValidationFlag(stage="extraction", severity="warning",
                                 subject_id="p1", message="m", auto_action="none")]
        loaded = load_graph_state(dump_graph_state({"validation_flags": flags}))
        assert loaded["validation_flags"] == flags

    def test_empty_list_stays_empty_list(self):
        loaded = load_graph_state(dump_graph_state({"effect_sizes": []}))
        assert loaded["effect_sizes"] == []


class TestPassthroughAndFullState:
    def test_json_native_keys_pass_through_unchanged(self):
        state = {"user_prompt": "does X help Y?", "mode": "manual",
                 "n_search_retrieved": 23, "errors": ["e1"]}
        assert load_graph_state(dump_graph_state(state)) == state

    def test_full_realistic_graph_state_round_trips(self):
        """The actual shape saved at the 'after_fulltext' pause boundary --
        the correctness-critical case."""
        plan = _plan()
        papers = [_paper(id="p1"), _paper(id="p2", full_text=None)]
        state = {
            "user_prompt": "does X help Y?",
            "mode": "search",
            "paper_files": [],
            "output_dir": "outputs/abc123",
            "plan": plan,
            "papers_eligible": papers,
            "all_retrieved_papers": papers,
            "n_search_retrieved": 23,
            "papers_no_fulltext": [],
            "errors": [],
        }
        loaded = load_graph_state(dump_graph_state(state))
        assert loaded["plan"] == plan
        assert loaded["papers_eligible"] == papers
        assert loaded["all_retrieved_papers"] == papers
        assert loaded["user_prompt"] == state["user_prompt"]
        assert loaded["n_search_retrieved"] == 23

    def test_dump_is_actually_json_serializable(self):
        """Guards the safety-net check in dump_graph_state itself -- the
        output must be plain-JSON-safe, not just 'close enough'."""
        import json
        state = {"plan": _plan(), "effect_sizes": [_es()], "papers_eligible": [_paper()]}
        dumped = dump_graph_state(state)
        json.dumps(dumped)  # must not raise


class TestUnknownTypeSafetyNet:
    def test_unhandled_pydantic_instance_raises_loudly(self):
        """If GraphState ever gains a new key holding a Pydantic model this
        codec doesn't know about, dump_graph_state must raise clearly,
        never silently store something load_graph_state can't reconstruct."""
        class _NotInTheCodec:
            def model_dump(self, mode="json"):
                raise AssertionError("should never be called")

        # Use a real, genuinely-unmapped Pydantic-like object: reuse
        # StudyData, which is deliberately NOT in _SINGLE_MODEL_KEYS/
        # _LIST_MODEL_KEYS (see snapshot.py's build_study_rows comment).
        from models import StudyData
        rogue = StudyData(study_id="s1", report_id="r1")
        with pytest.raises(TypeError):
            dump_graph_state({"included_studies": rogue})
