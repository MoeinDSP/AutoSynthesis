"""
agents/report_agent.py's effect-measure labeling helpers -- the
"do not label native RR/OR/MD results as Hedges' g" guarantee, enforced
deterministically (not just via LLM prompt instructions). Also covers
models.py::MetaAnalysisResult's pooled_effect/effect_measure/computation_scale
additions (the "consumers reading meta_result directly" requirement).
"""

import pipeline_graph  # noqa: F401 -- import first, see report_agent.py's own circular-import note

from agents.report_agent import _build_effect_measure_summary, _measure_fields, _measure_label, _native_pooling_used
from models import EffectMeasure, MetaAnalysisGroupResult, MetaAnalysisResult


def _group(effect_measure, computation_scale, source, conflict=None, pooled=0.5, k=2, single_g=None):
    result = None
    if pooled is not None:
        result = MetaAnalysisResult(
            pooled_g=pooled, pooled_se=0.1, ci_lower=pooled - 0.2, ci_upper=pooled + 0.2,
            z_value=2.0, p_value=0.01, tau_squared=0.01, tau=0.1, i_squared=10.0, h_squared=1.1,
            q_statistic=1.0, q_df=k - 1, q_p_value=0.5, k=k, n_total=k * 50, method="REML",
            effect_measure=effect_measure, computation_scale=computation_scale,
            effect_measure_source=source, effect_measure_conflict=conflict,
        )
    return MetaAnalysisGroupResult(
        outcome_group_key="g", label="Group", k=k, n_total=k * 50, study_ids=["S1", "S2"][:k],
        insufficient_data=result is None, result=result, single_effect_g=single_g,
        effect_measure=effect_measure, computation_scale=computation_scale,
        effect_measure_source=source, effect_measure_conflict=conflict,
    )


# ---------------------------------------------------------------------------
# MetaAnalysisResult: pooled_effect auto-fill + measure fields readable
# without the wrapper (the explicit ask: "consumers reading meta_result
# directly can determine its measure/scale")
# ---------------------------------------------------------------------------

def test_pooled_effect_auto_fills_from_pooled_g_for_legacy_callers():
    r = MetaAnalysisResult(
        pooled_g=0.42, pooled_se=0.1, ci_lower=0.2, ci_upper=0.6, z_value=2.0, p_value=0.01,
        tau_squared=0.0, tau=0.0, i_squared=0.0, h_squared=1.0, q_statistic=0.0, q_df=1,
        q_p_value=1.0, k=2, n_total=100,
    )
    assert r.pooled_effect == 0.42
    # backward-compat defaults preserve old (Hedges' g-only) behaviour:
    assert r.effect_measure == EffectMeasure.HEDGES_G
    assert r.computation_scale == EffectMeasure.HEDGES_G


def test_meta_analysis_result_carries_its_own_measure_without_the_wrapper():
    r = MetaAnalysisResult(
        pooled_g=0.72, pooled_effect=0.72, pooled_se=0.1, ci_lower=0.5, ci_upper=0.95,
        z_value=2.0, p_value=0.01, tau_squared=0.0, tau=0.0, i_squared=0.0, h_squared=1.0,
        q_statistic=0.0, q_df=1, q_p_value=1.0, k=3, n_total=200, method="REML",
        effect_measure=EffectMeasure.RR, computation_scale=EffectMeasure.RR,
        effect_measure_source="explicit_paper_reported",
    )
    # No MetaAnalysisGroupResult involved at all -- direct field access:
    assert r.effect_measure == EffectMeasure.RR
    assert r.computation_scale == EffectMeasure.RR
    assert _measure_label(r.computation_scale) == "Risk Ratio (RR)"


# ---------------------------------------------------------------------------
# _measure_fields / _native_pooling_used
# ---------------------------------------------------------------------------

def test_native_pooling_true_when_measure_equals_scale():
    assert _native_pooling_used(EffectMeasure.RR, EffectMeasure.RR) is True
    assert _native_pooling_used(EffectMeasure.MD, EffectMeasure.MD) is True


def test_native_pooling_false_for_unknown_fallback():
    assert _native_pooling_used(EffectMeasure.UNKNOWN, EffectMeasure.HEDGES_G) is False


def test_measure_fields_never_call_rr_hedges_g():
    fields = _measure_fields(EffectMeasure.RR, EffectMeasure.RR, "explicit_paper_reported", None)
    assert fields["measure_label"] == "Risk Ratio (RR)"
    assert "Hedges" not in fields["measure_label"]
    assert fields["native_pooling_used"] is True


def test_measure_fields_never_call_md_hedges_g():
    fields = _measure_fields(EffectMeasure.MD, EffectMeasure.MD, "deterministic_evidence", None)
    assert fields["measure_label"] == "Mean Difference (MD)"
    assert "Hedges" not in fields["measure_label"]


# ---------------------------------------------------------------------------
# _build_effect_measure_summary -- one row per RR / MD / SMD / UNKNOWN case
# ---------------------------------------------------------------------------

def _row_line(md: str) -> str:
    """The single data row (not the caption, which always mentions the
    Hedges' g/SMD fallback boilerplate) -- the line starting with '| Group'."""
    return next(line for line in md.splitlines() if line.startswith("| Group"))


def test_summary_table_rr():
    md = _build_effect_measure_summary([_group(EffectMeasure.RR, EffectMeasure.RR, "explicit_paper_reported", pooled=0.52)])
    assert "Risk Ratio (RR)" in md
    assert "| Yes |" in md
    assert "Hedges" not in _row_line(md)


def test_summary_table_md():
    md = _build_effect_measure_summary([_group(EffectMeasure.MD, EffectMeasure.MD, "deterministic_evidence", pooled=-6.5)])
    assert "Mean Difference (MD)" in md
    assert "| Yes |" in md
    assert "Hedges" not in _row_line(md)


def test_summary_table_smd_explicit():
    md = _build_effect_measure_summary([_group(EffectMeasure.SMD, EffectMeasure.SMD, "explicit_paper_reported", pooled=0.36)])
    assert "Standardized Mean Difference (SMD)" in md
    assert "| Yes |" in md


def test_summary_table_unknown_fallback_labeled_as_fallback_not_confirmed_smd():
    md = _build_effect_measure_summary([_group(EffectMeasure.UNKNOWN, EffectMeasure.HEDGES_G, "unresolved_fallback", pooled=0.36)])
    assert "Hedges' g (fallback" in md
    assert "not confirmed" in md
    assert "| No |" in md


def test_summary_table_insufficient_data_group_still_shows_resolved_measure():
    """A group with no result (too few studies) still has a resolved
    effect_measure/computation_scale from the wrapper -- must not be blank."""
    g = _group(EffectMeasure.MD, EffectMeasure.MD, "deterministic_evidence", pooled=None, k=1, single_g=0.3)
    md = _build_effect_measure_summary([g])
    assert "Mean Difference (MD)" in md
    assert "single study, not pooled" in md


def test_summary_table_empty_groups_returns_empty_string():
    assert _build_effect_measure_summary([]) == ""


def test_summary_table_conflict_note_surfaced():
    g = _group(EffectMeasure.RR, EffectMeasure.RR, "explicit_user_request",
               conflict="user requested RR, but the paper(s) explicitly report OR", pooled=0.5)
    md = _build_effect_measure_summary([g])
    assert "user requested RR" in md
