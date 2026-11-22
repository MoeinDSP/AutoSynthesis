"""dashboard.py::_results_from_pipeline_state -- the "meta_groups" breakdown.

Root-cause context: the pipeline (agents/meta_analysis_agent.py) has always
been able to produce SEVERAL independently pooled MetaAnalysisGroupResults
(state.meta_analysis_groups) -- one per distinct outcome family/timepoint --
but the dashboard only ever surfaced ONE of them (state.meta_analysis, the
"primary" alias) to the UI. A real multi-outcome run (39 groups) confirmed
the UI showed exactly one Key Statistics card no matter how many outcomes
existed. This tests the fix: the JSON payload sent to the frontend must
include every group, correctly flagging which one is primary."""

import pytest

from models import MetaAnalysisGroupResult, MetaAnalysisResult, PipelineState


def _result(g=0.3, k=5) -> MetaAnalysisResult:
    return MetaAnalysisResult(
        pooled_g=g, pooled_se=0.1, ci_lower=g - 0.2, ci_upper=g + 0.2,
        z_value=1.0, p_value=0.05, tau_squared=0.01, tau=0.1, i_squared=50.0,
        h_squared=2.0, q_statistic=8.0, q_df=k - 1, q_p_value=0.05, k=k, n_total=k * 40,
    )


def _group(key, label, k=5, insufficient=False, result=None) -> MetaAnalysisGroupResult:
    return MetaAnalysisGroupResult(
        outcome_group_key=key, outcome_family=key.split("::")[0], label=label,
        k=k, n_total=k * 40, insufficient_data=insufficient,
        result=result if not insufficient else None,
    )


def test_meta_groups_included_for_multi_outcome_run(tmp_path):
    from dashboard import _results_from_pipeline_state

    primary_result = _result(g=0.05, k=13)
    secondary_result = _result(g=0.35, k=10)
    state = PipelineState(
        meta_analysis=primary_result,
        meta_analysis_groups=[
            _group("verbal_memory::immediate", "verbal memory (immediate)", k=13, result=primary_result),
            _group("quality_of_life::immediate", "quality of life (immediate)", k=10, result=secondary_result),
            _group("fatigue::immediate", "fatigue (immediate)", k=1, insufficient=True),
        ],
    )

    results = _results_from_pipeline_state(state, str(tmp_path))
    groups = results["meta_groups"]

    assert len(groups) == 3
    by_key = {g["key"]: g for g in groups}

    assert by_key["verbal_memory::immediate"]["is_primary"] is True
    assert by_key["quality_of_life::immediate"]["is_primary"] is False
    assert by_key["fatigue::immediate"]["is_primary"] is False

    assert by_key["verbal_memory::immediate"]["pooled_g"] == 0.05
    assert by_key["quality_of_life::immediate"]["pooled_g"] == 0.35
    assert "pooled_g" not in by_key["fatigue::immediate"]  # insufficient_data -> no result
    assert by_key["fatigue::immediate"]["insufficient_data"] is True

    # Sorted primary-first, then by descending k, insufficient-data last.
    assert [g["key"] for g in groups] == [
        "verbal_memory::immediate", "quality_of_life::immediate", "fatigue::immediate",
    ]


def test_meta_groups_empty_for_legacy_single_group_run(tmp_path):
    # A run with exactly one group (the pre-multi-group / "default" case)
    # still populates meta_groups with that one entry -- the frontend hides
    # the selector itself when len <= 1, this just needs to not crash or
    # silently omit the field.
    from dashboard import _results_from_pipeline_state

    result = _result(g=0.2, k=3)
    state = PipelineState(
        meta_analysis=result,
        meta_analysis_groups=[_group("default", "All outcomes (undifferentiated)", k=3, result=result)],
    )
    results = _results_from_pipeline_state(state, str(tmp_path))
    assert len(results["meta_groups"]) == 1
    assert results["meta_groups"][0]["is_primary"] is True


def test_meta_groups_absent_when_no_meta_analysis_ran(tmp_path):
    from dashboard import _results_from_pipeline_state

    state = PipelineState()
    results = _results_from_pipeline_state(state, str(tmp_path))
    assert results["meta_groups"] == []
