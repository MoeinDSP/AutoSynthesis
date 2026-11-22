"""persistence/snapshot.py -- pure GraphState -> row-list mapping.
No database access, no DATABASE_URL needed -- these are plain functions of
a dict/list of Pydantic instances."""

from models import (
    MetaAnalysisPlan, PaperRecord, StudyData, EffectSizeRecord,
    MetaAnalysisGroupResult, MetaAnalysisResult, ModeratorResult, BiasResult,
    RiskOfBiasAssessment, ValidationFlag,
)
from persistence import snapshot as snap


def _paper(**kwargs):
    defaults = dict(id="p1", title="T", abstract="A", authors=["X"], year=2020, source="pubmed")
    defaults.update(kwargs)
    return PaperRecord(**defaults)


def _meta_result(**kwargs):
    defaults = dict(
        pooled_g=0.4, pooled_se=0.1, ci_lower=0.2, ci_upper=0.6,
        z_value=4.0, p_value=0.001, tau_squared=0.01, tau=0.1,
        i_squared=20.0, h_squared=1.2, q_statistic=5.0, q_df=4,
        q_p_value=0.3, k=5, n_total=250,
    )
    defaults.update(kwargs)
    return MetaAnalysisResult(**defaults)


def test_derive_run_summary_pulls_from_raw_graph_state_not_pipeline_state():
    plan = MetaAnalysisPlan(
        research_question="q", treatment_label="t", control_label="c",
        outcome_description="o", positive_direction="p", search_queries=[],
        inclusion_criteria=[], exclusion_criteria=[], moderators_to_extract=[],
    )
    state = {
        "plan": plan,
        "papers_eligible": [_paper(id="p1"), _paper(id="p2")],
        "effect_sizes": [],
        "n_search_retrieved": 23,
        "n_screened_excluded": 5,
        "n_eligibility_excluded": 2,
    }
    summary = snap.derive_run_summary(state)
    # The whole point: these three counts are dead in PipelineState post-
    # conversion (orchestrator.py::_to_pipeline_state), but derive_run_summary
    # reads them straight off the raw GraphState, so the DB is richer.
    assert summary["n_search_retrieved"] == 23
    assert summary["n_screened_excluded"] == 5
    assert summary["n_eligibility_excluded"] == 2
    assert summary["n_papers_eligible"] == 2
    assert summary["plan_json"]["research_question"] == "q"


def test_build_paper_rows_joins_screening_and_eligibility_by_paper_id():
    papers = [_paper(id="p1"), _paper(id="p2")]
    state = {
        "papers_eligible": papers,
        "screening_decisions": {
            "p1": {"paper_id": "p1", "decision": "include", "reason": "relevant"},
            "p2": {"paper_id": "p2", "decision": "include", "reason": "relevant"},
        },
        "eligibility_decisions": {
            "p1": {"paper_id": "p1", "decision": "include", "reason": "meets criteria",
                   "exclusion_criterion": None},
        },
    }
    rows = snap.build_paper_rows(state)
    by_id = {r["paper_id"]: r for r in rows}
    assert by_id["p1"]["screening_decision"] == "include"
    assert by_id["p1"]["eligibility_decision"] == "include"
    # p2 has a screening decision but no eligibility decision recorded yet.
    assert by_id["p2"]["eligibility_decision"] is None


def test_build_paper_rows_papers_eligible_wins_over_all_retrieved_on_conflict():
    # Same paper_id in both lists, different title -- papers_eligible (the
    # later-stage, more-authoritative list) must win.
    early = _paper(id="p1", title="Early title")
    later = _paper(id="p1", title="Later title")
    state = {"all_retrieved_papers": [early], "papers_eligible": [later]}
    rows = snap.build_paper_rows(state)
    assert len(rows) == 1
    assert rows[0]["title"] == "Later title"


def test_build_paper_rows_marks_manual_uploads():
    state = {"papers_eligible": [_paper(id="p1", source="manual")]}
    rows = snap.build_paper_rows(state)
    assert rows[0]["is_uploaded"] is True


def test_build_study_rows_from_explicit_list_not_graph_state_key():
    studies = [StudyData(study_id="s1", report_id="r1", paper_id="p1",
                          treatment_label="t", control_label="c", n_treatment=20, n_control=20)]
    rows = snap.build_study_rows(studies)
    assert rows[0]["study_id"] == "s1"
    assert rows[0]["n_participants"] == 40  # derived by StudyData's own validator


def test_build_study_rows_none_or_empty_returns_empty():
    assert snap.build_study_rows(None) == []
    assert snap.build_study_rows([]) == []


def test_build_effect_size_rows_mirrors_effect_size_record():
    es = EffectSizeRecord(
        study_id="s1", report_id="r1", cohens_d=0.3, hedges_g=0.3,
        variance=0.02, se=0.14, ci_lower=0.02, ci_upper=0.58, n_total=50,
        computation_method="means_sds", outcome_group_key="mortality",
    )
    rows = snap.build_effect_size_rows({"effect_sizes": [es]})
    assert rows[0]["study_id"] == "s1"
    assert rows[0]["outcome_group_key"] == "mortality"
    assert rows[0]["hedges_g"] == 0.3
    # EffectSizeRecord has no paper_id field of its own -- deliberately NULL.
    assert rows[0]["paper_id"] is None


def test_build_outcome_group_and_pooled_rows_marks_primary_by_identity():
    primary_result = _meta_result(pooled_g=0.1)
    other_result = _meta_result(pooled_g=0.9)
    primary_group = MetaAnalysisGroupResult(
        outcome_group_key="mortality", label="mortality", k=5, n_total=250,
        study_ids=["s1"], insufficient_data=False, result=primary_result,
    )
    other_group = MetaAnalysisGroupResult(
        outcome_group_key="default", label="All outcomes (undifferentiated)", k=9, n_total=400,
        study_ids=["s2"], insufficient_data=False, result=other_result,
    )
    state = {"meta_results": [other_group, primary_group], "meta_result": primary_result}
    group_rows, pooled_rows = snap.build_outcome_group_and_pooled_rows(state)

    groups_by_key = {r["outcome_group_key"]: r for r in group_rows}
    assert groups_by_key["mortality"]["is_primary"] is True
    assert groups_by_key["default"]["is_primary"] is False

    pooled_by_key = {r["outcome_group_key"]: r for r in pooled_rows}
    assert pooled_by_key["mortality"]["is_primary"] is True
    assert pooled_by_key["mortality"]["pooled_g"] == 0.1
    assert pooled_by_key["default"]["is_primary"] is False
    assert pooled_by_key["default"]["pooled_g"] == 0.9


def test_build_outcome_group_rows_insufficient_data_group_has_no_pooled_row():
    group = MetaAnalysisGroupResult(
        outcome_group_key="rare", label="rare", k=1, n_total=20,
        study_ids=["s1"], insufficient_data=True, single_effect_g=0.5, result=None,
    )
    state = {"meta_results": [group], "meta_result": None}
    group_rows, pooled_rows = snap.build_outcome_group_and_pooled_rows(state)
    assert len(group_rows) == 1
    assert group_rows[0]["insufficient_data"] is True
    assert len(pooled_rows) == 0  # no MetaAnalysisResult to mirror


def test_build_moderator_rows():
    mods = [ModeratorResult(moderator_name="design", qm_statistic=1.0, qm_df=1, qm_p_value=0.3,
                             subgroups=[], reference_category="RCT", coefficients=[])]
    rows = snap.build_moderator_rows({"moderator_results": mods})
    assert rows[0]["moderator_name"] == "design"


def test_build_bias_rows_single_run_level_result():
    bias = BiasResult(
        eggers_intercept=0.1, eggers_se=0.05, eggers_t_value=2.0, eggers_p_value=0.04,
        trim_fill_k0=0, trim_fill_side="none", trim_fill_g=0.4,
        trim_fill_ci_lower=0.2, trim_fill_ci_upper=0.6, bias_risk="low",
    )
    rows = snap.build_bias_rows({"bias_result": bias})
    assert len(rows) == 1
    assert rows[0]["bias_risk"] == "low"


def test_build_bias_rows_none_returns_empty():
    assert snap.build_bias_rows({"bias_result": None}) == []
    assert snap.build_bias_rows({}) == []


def test_build_rob_rows():
    robs = [RiskOfBiasAssessment(
        paper_id="p1", paper_title="T", design_classification="randomized",
        design_rationale="r", tool_used="RoB2", overall_risk="low",
        overall_summary="s", domain_judgments=[],
    )]
    rows = snap.build_rob_rows({"rob_assessments": robs})
    assert rows[0]["paper_id"] == "p1"
    assert rows[0]["tool_used"] == "RoB2"


def test_build_validation_flag_rows():
    flags = [ValidationFlag(stage="extraction", severity="warning",
                             subject_id="p1", message="m", auto_action="none")]
    rows = snap.build_validation_flag_rows({"validation_flags": flags})
    assert rows[0]["stage"] == "extraction"
    assert rows[0]["severity"] == "warning"
