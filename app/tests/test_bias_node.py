"""
Regression test for agents/bias_agent.py's stale-carryover bug: output_dir
is reused across runs within one dashboard session, and bias_node's own
"fewer than 3 effect sizes" early return used to skip writing bias_result.json
entirely -- leaving a PREVIOUS, unrelated run's Egger's-test/trim-and-fill
numbers sitting there and later presented as if they were this run's own
result. Same root cause/fix pattern already applied to
agents/effect_size_agent.py and agents/meta_analysis_agent.py (see
tests/test_effect_size_node.py, tests/test_meta_analysis_node_grouping.py)
-- this is the analogous gap in bias_node specifically.

Confirmed live: a real CD010592 k=2 run still showed eggers_p_value=0.0263
and trim_fill_g=0.5064 -- both exactly matching a PRIOR, unrelated k=4 run's
own bias_result.json, byte-for-byte.
"""

import json
import math
from unittest.mock import patch

import pytest

from models import EffectMeasure, EffectSizeRecord, MetaAnalysisGroupResult, MetaAnalysisResult


def _es(study_id: str, g: float, variance: float = 0.02,
        native_value=None, native_variance=None) -> EffectSizeRecord:
    return EffectSizeRecord(
        study_id=study_id, report_id="R1", cohens_d=g, hedges_g=g,
        variance=variance, se=variance ** 0.5, ci_lower=g - 0.3, ci_upper=g + 0.3,
        n_total=50, computation_method="means_sds",
        native_value=native_value, native_variance=native_variance,
    )


def _meta_result(pooled_g: float, computation_scale: EffectMeasure,
                  effect_measure: EffectMeasure = None) -> MetaAnalysisResult:
    return MetaAnalysisResult(
        pooled_g=pooled_g, pooled_se=0.1, ci_lower=pooled_g - 0.2, ci_upper=pooled_g + 0.2,
        z_value=1.0, p_value=0.3, tau_squared=0.0, tau=0.0, i_squared=0.0, h_squared=1.0,
        q_statistic=1.0, q_df=2, q_p_value=0.5, k=3, n_total=150,
        effect_measure=effect_measure if effect_measure is not None else computation_scale,
        computation_scale=computation_scale,
    )


def test_fewer_than_3_effect_sizes_overwrites_a_stale_bias_result_json(tmp_path):
    from agents.bias_agent import bias_node

    # Seed a stale bias_result.json, exactly as a prior, unrelated (k=4)
    # run's real output would look.
    stale = {
        "eggers_intercept": 0.1617, "eggers_se": 0.13, "eggers_t_value": 2.221,
        "eggers_p_value": 0.0263, "trim_fill_k0": 0, "trim_fill_side": "right",
        "trim_fill_g": 0.5064, "trim_fill_ci_lower": 0.2752, "trim_fill_ci_upper": 0.7375,
        "bias_risk": "high",
    }
    (tmp_path / "bias_result.json").write_text(json.dumps(stale))
    (tmp_path / "funnel_plot.png").write_bytes(b"stale png bytes")

    state = {
        "effect_sizes": [_es("study_1", 0.05), _es("study_2", 0.07)],  # only k=2
        "meta_result": None,
        "output_dir": str(tmp_path),
    }
    result = bias_node(state)

    assert result["bias_result"] is None
    on_disk = json.loads((tmp_path / "bias_result.json").read_text())
    assert on_disk == {}
    # The stale funnel plot must not survive either.
    assert not (tmp_path / "funnel_plot.png").exists()


def test_zero_effect_sizes_overwrites_a_stale_bias_result_json(tmp_path):
    from agents.bias_agent import bias_node

    (tmp_path / "bias_result.json").write_text(json.dumps({"eggers_p_value": 0.01}))
    state = {"effect_sizes": [], "meta_result": None, "output_dir": str(tmp_path)}
    result = bias_node(state)

    assert result["bias_result"] is None
    on_disk = json.loads((tmp_path / "bias_result.json").read_text())
    assert on_disk == {}


# ---------------------------------------------------------------------------
# Funnel-plot scale-mismatch fix: bias_node must call statistics.plots.
# funnel_plot with inputs on the group's ACTUAL native scale (RR/OR/HR log
# scale, MD/SMD/Hedges' g linear scale) instead of unconditionally passing
# es.hedges_g/meta_result.pooled_g as if every group were Hedges' g. The
# CD008986 case: pooled RR = 0.851 used to render as "Pooled Hedges' g =
# 0.851". See statistics/plots.py's own tests (test_plots_measure_aware.py)
# for funnel_plot's internal rendering; these test bias_node's WIRING --
# what it passes to funnel_plot for each computation_scale.
#
# hedges_g/variance below (fed to the real eggers_test/trim_and_fill calls,
# unaffected by this fix -- see agents/bias_agent.py's own comment) are
# deliberately given slightly different values per study; identical
# hedges_g/variance across all rows can make the underlying R meta-
# regression's design matrix exactly singular ("Model matrix no longer of
# full rank"), which is a test-data artifact, not something this fix touches.
# ---------------------------------------------------------------------------

def _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result):
    from agents.bias_agent import bias_node

    state = {"effect_sizes": effect_sizes, "meta_result": meta_result, "output_dir": str(tmp_path)}
    with patch("agents.bias_agent.funnel_plot", return_value="funnel.png") as mock_funnel:
        bias_node(state)
    assert mock_funnel.called, "funnel_plot was never called"
    return mock_funnel.call_args.kwargs


def test_funnel_plot_wiring_for_rr_group_uses_log_scale_and_native_values(tmp_path):
    """The CD008986 case, reproduced: pooled RR = 0.851, each row's
    native_value already on the log scale."""
    effect_sizes = [
        _es("s1", g=0.30, variance=0.018, native_value=math.log(0.7), native_variance=0.04),
        _es("s2", g=0.40, variance=0.024, native_value=math.log(0.9), native_variance=0.05),
        _es("s3", g=0.20, variance=0.021, native_value=math.log(1.05), native_variance=0.03),
    ]
    meta_result = _meta_result(pooled_g=0.8512993518510397, computation_scale=EffectMeasure.RR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is True
    assert kwargs["measure_label"] == "Risk Ratio (RR)"
    assert kwargs["unavailable"] is False
    assert kwargs["effects"] == [math.log(0.7), math.log(0.9), math.log(1.05)]
    assert kwargs["variances"] == [0.04, 0.05, 0.03]
    assert kwargs["pooled_g"] == pytest.approx(math.log(0.8512993518510397))


def test_funnel_plot_wiring_for_or_group(tmp_path):
    effect_sizes = [
        _es("s1", g=0.30, variance=0.018, native_value=math.log(1.5), native_variance=0.05),
        _es("s2", g=0.40, variance=0.024, native_value=math.log(2.0), native_variance=0.06),
        _es("s3", g=0.20, variance=0.021, native_value=math.log(1.6), native_variance=0.04),
    ]
    meta_result = _meta_result(pooled_g=1.71, computation_scale=EffectMeasure.OR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is True
    assert kwargs["measure_label"] == "Odds Ratio (OR)"
    assert kwargs["pooled_g"] == pytest.approx(math.log(1.71))


def test_funnel_plot_wiring_for_hr_group(tmp_path):
    effect_sizes = [
        _es("s1", g=0.10, variance=0.018, native_value=math.log(0.75), native_variance=0.02),
        _es("s2", g=0.20, variance=0.024, native_value=math.log(0.95), native_variance=0.03),
        _es("s3", g=0.00, variance=0.021, native_value=math.log(0.85), native_variance=0.025),
    ]
    meta_result = _meta_result(pooled_g=0.88, computation_scale=EffectMeasure.HR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is True
    assert kwargs["measure_label"] == "Hazard Ratio (HR)"
    assert kwargs["pooled_g"] == pytest.approx(math.log(0.88))


def test_funnel_plot_wiring_for_md_group_plots_directly(tmp_path):
    effect_sizes = [
        _es("s1", g=0.10, variance=0.018, native_value=-5.0, native_variance=1.0),
        _es("s2", g=0.20, variance=0.024, native_value=-8.0, native_variance=1.5),
        _es("s3", g=0.00, variance=0.021, native_value=-6.0, native_variance=1.2),
    ]
    meta_result = _meta_result(pooled_g=-6.5, computation_scale=EffectMeasure.MD)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is False
    assert kwargs["measure_label"] == "Mean Difference (MD)"
    assert kwargs["pooled_g"] == pytest.approx(-6.5)  # NOT log-transformed
    assert kwargs["effects"] == [-5.0, -8.0, -6.0]


def test_funnel_plot_wiring_for_smd_hedges_g_group_unchanged(tmp_path):
    """No meta_result.computation_scale override -- defaults to HEDGES_G,
    the pre-existing behaviour, byte-for-byte."""
    effect_sizes = [
        _es("s1", g=0.2, variance=0.018), _es("s2", g=0.3, variance=0.024), _es("s3", g=0.4, variance=0.021),
    ]
    meta_result = _meta_result(pooled_g=0.3, computation_scale=EffectMeasure.HEDGES_G)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is False
    assert kwargs["measure_label"] == "Hedges' g"
    assert kwargs["pooled_g"] == pytest.approx(0.3)
    # native_value was never set on these rows -- falls back to hedges_g/variance.
    assert kwargs["effects"] == [0.2, 0.3, 0.4]


def test_funnel_plot_wiring_falls_back_to_hedges_g_when_native_value_missing(tmp_path):
    """Explicit coverage for the case the task called out: the pooled
    estimate/scale IS RR, but these particular rows never had native
    resolution run on them (e.g. older data predating native_value/
    native_variance) -- so they only carry the Hedges' g-approximation
    fallback. bias_node must not crash; it falls back row-by-row to
    hedges_g/variance for the funnel plot's per-study points, while the
    scale/label/pooled-line still follow meta_result's own RR resolution
    (the same fallback-when-missing convention meta_analysis_agent.py
    itself uses when populating native_value in the first place)."""
    effect_sizes = [
        _es("s1", g=0.38172, variance=0.0069),   # no native_value/native_variance set
        _es("s2", g=0.257476, variance=0.0074),
        _es("s3", g=0.295398, variance=0.0070),
    ]
    meta_result = _meta_result(pooled_g=1.2975383198728472, computation_scale=EffectMeasure.RR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["log_scale"] is True
    assert kwargs["measure_label"] == "Risk Ratio (RR)"
    assert kwargs["effects"] == [0.38172, 0.257476, 0.295398]      # fell back to hedges_g
    assert kwargs["variances"] == [0.0069, 0.0074, 0.0070]         # fell back to .variance
    assert kwargs["pooled_g"] == pytest.approx(math.log(1.2975383198728472))


def test_funnel_plot_wiring_unknown_measure_marked_unavailable(tmp_path):
    effect_sizes = [
        _es("s1", g=0.2, variance=0.018), _es("s2", g=0.3, variance=0.024), _es("s3", g=0.4, variance=0.021),
    ]
    meta_result = _meta_result(pooled_g=0.3, computation_scale=EffectMeasure.UNKNOWN)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["unavailable"] is True
    assert kwargs["effects"] == []
    assert kwargs["variances"] == []


def test_funnel_plot_wiring_generic_measure_marked_unavailable(tmp_path):
    effect_sizes = [
        _es("s1", g=0.2, variance=0.018), _es("s2", g=0.3, variance=0.024), _es("s3", g=0.4, variance=0.021),
    ]
    meta_result = _meta_result(pooled_g=0.3, computation_scale=EffectMeasure.GENERIC)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["unavailable"] is True


def test_funnel_plot_wiring_nonpositive_ratio_pooled_value_marked_unavailable(tmp_path):
    """A non-positive "pooled RR" can't be a real ratio -- must not crash on
    math.log() or silently mislabel a broken number as valid."""
    effect_sizes = [
        _es("s1", g=0.30, variance=0.018, native_value=math.log(0.7), native_variance=0.04),
        _es("s2", g=0.40, variance=0.024, native_value=math.log(0.9), native_variance=0.05),
        _es("s3", g=0.20, variance=0.021, native_value=math.log(1.05), native_variance=0.03),
    ]
    meta_result = _meta_result(pooled_g=-0.5, computation_scale=EffectMeasure.RR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["unavailable"] is True


def test_funnel_plot_wiring_never_labels_rr_as_hedges_g_or_smd(tmp_path):
    """Dedicated, explicit guard: an RR-scale analysis must never render as
    if it were Hedges' g/SMD, whatever measure_label() happens to produce
    for RR (this test would fail if that mapping ever regressed)."""
    effect_sizes = [
        _es("s1", g=0.30, variance=0.018, native_value=math.log(0.7), native_variance=0.04),
        _es("s2", g=0.40, variance=0.024, native_value=math.log(0.9), native_variance=0.05),
        _es("s3", g=0.20, variance=0.021, native_value=math.log(1.05), native_variance=0.03),
    ]
    meta_result = _meta_result(pooled_g=0.8512993518510397, computation_scale=EffectMeasure.RR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["measure_label"] == "Risk Ratio (RR)"
    assert "Hedges" not in kwargs["measure_label"]
    assert "SMD" not in kwargs["measure_label"] and "Standardized" not in kwargs["measure_label"]


# ---------------------------------------------------------------------------
# Multi-group mixing regression: state["effect_sizes"] is the FULL,
# unfiltered list Stage 5 produces across EVERY outcome group in the run
# (meta_analysis_node never overwrites it -- meta_result is just one group's
# .result). Confirmed live on CD008986: a mortality outcome that
# auto-split into 3 separate pools (RR k=11, HR k=5, single-study OR k=1)
# by effect measure -- before this fix, bias_node's funnel plot silently
# mixed all 17 rows from all 3 groups into one plot, labeled as if every
# point were on the primary (RR) group's scale. This is the "mixed
# incompatible effect measures" failure mode: an HR-scale point's
# native_value (log(HR)) is NOT the same quantity as an RR-scale point's
# native_value (log(RR)), even though both look like plain floats.
# ---------------------------------------------------------------------------

def test_funnel_plot_wiring_filters_to_primary_group_studies_only(tmp_path):
    """The CD008986 shape, reproduced: 17 total effect_sizes across 3 groups,
    but only the primary (RR, k=11 here reduced to 3 for test brevity)
    group's own studies must feed the funnel plot -- not the HR-group's or
    the OR-group's rows, even though they're all sitting in the same
    state["effect_sizes"] list."""
    from agents.bias_agent import bias_node

    rr_rows = [
        _es("rr_1", g=0.30, variance=0.018, native_value=math.log(0.7), native_variance=0.04),
        _es("rr_2", g=0.40, variance=0.024, native_value=math.log(0.9), native_variance=0.05),
        _es("rr_3", g=0.20, variance=0.021, native_value=math.log(1.05), native_variance=0.03),
    ]
    hr_rows = [
        _es("hr_1", g=0.10, variance=0.02, native_value=math.log(0.75), native_variance=0.02),
        _es("hr_2", g=0.20, variance=0.03, native_value=math.log(0.95), native_variance=0.03),
        _es("hr_3", g=0.05, variance=0.025, native_value=math.log(0.85), native_variance=0.025),
    ]
    or_rows = [_es("or_1", g=-0.14, variance=0.05, native_value=math.log(1.71), native_variance=0.06)]
    all_effect_sizes = rr_rows + hr_rows + or_rows  # exactly state["effect_sizes"]'s real shape

    rr_result = _meta_result(pooled_g=0.8512993518510397, computation_scale=EffectMeasure.RR)
    rr_group = MetaAnalysisGroupResult(
        outcome_group_key="mortality::measure=RR", label="mortality", k=3, n_total=300,
        study_ids=["rr_1", "rr_2", "rr_3"], result=rr_result,
        effect_measure=EffectMeasure.RR, computation_scale=EffectMeasure.RR,
    )
    hr_group = MetaAnalysisGroupResult(
        outcome_group_key="mortality::measure=HR", label="mortality", k=3, n_total=300,
        study_ids=["hr_1", "hr_2", "hr_3"],
        result=_meta_result(pooled_g=0.88, computation_scale=EffectMeasure.HR),
        effect_measure=EffectMeasure.HR, computation_scale=EffectMeasure.HR,
    )
    or_group = MetaAnalysisGroupResult(
        outcome_group_key="mortality::measure=OR", label="mortality", k=1, n_total=100,
        study_ids=["or_1"], insufficient_data=True, single_effect_g=-0.14,
        effect_measure=EffectMeasure.OR, computation_scale=EffectMeasure.OR,
    )

    state = {
        "effect_sizes": all_effect_sizes,
        "meta_result": rr_result,
        "meta_results": [rr_group, hr_group, or_group],
        "output_dir": str(tmp_path),
    }
    with patch("agents.bias_agent.funnel_plot", return_value="funnel.png") as mock_funnel:
        bias_node(state)
    kwargs = mock_funnel.call_args.kwargs

    # Only the 3 RR-group native log(RR) values -- never the HR/OR rows'.
    assert sorted(kwargs["effects"]) == sorted(
        [math.log(0.7), math.log(0.9), math.log(1.05)]
    )
    assert len(kwargs["effects"]) == 3
    assert kwargs["measure_label"] == "Risk Ratio (RR)"
    assert kwargs["log_scale"] is True


def test_funnel_plot_wiring_falls_back_to_full_list_when_no_group_membership_info(tmp_path):
    """No meta_results in state (legacy state shape, or a single-group run
    where it was never populated) -- degrade to the pre-existing behaviour
    of using the full effect_sizes list, never crash."""
    effect_sizes = [
        _es("s1", g=0.2, variance=0.018), _es("s2", g=0.3, variance=0.024), _es("s3", g=0.4, variance=0.021),
    ]
    meta_result = _meta_result(pooled_g=0.3, computation_scale=EffectMeasure.HEDGES_G)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    assert kwargs["effects"] == [0.2, 0.3, 0.4]


# ---------------------------------------------------------------------------
# Explicit null-line/pooled-line-on-the-same-scale check, at the bias_node
# wiring level (statistics/plots.py's own test_plots_measure_aware.py covers
# the same thing at the rendering level).
# ---------------------------------------------------------------------------

def test_funnel_plot_wiring_pooled_rr_0_851_recovers_to_log_of_0_851(tmp_path):
    effect_sizes = [
        _es("s1", g=0.30, variance=0.018, native_value=math.log(0.7), native_variance=0.04),
        _es("s2", g=0.40, variance=0.024, native_value=math.log(0.9), native_variance=0.05),
        _es("s3", g=0.20, variance=0.021, native_value=math.log(1.05), native_variance=0.03),
    ]
    meta_result = _meta_result(pooled_g=0.851, computation_scale=EffectMeasure.RR)

    kwargs = _run_bias_node_and_capture_funnel_kwargs(tmp_path, effect_sizes, meta_result)

    # funnel_plot's own contract (see test_plots_measure_aware.py) is that,
    # for log_scale=True, exp(pooled_g given here) is what gets drawn/
    # labeled -- so passing math.log(0.851) is what puts both the null line
    # (fixed at the natural value 1.0 by funnel_plot itself) and the pooled
    # line (at the natural value 0.851) on the exact same log-transformed
    # x-axis as the study points above (also all math.log(...) values).
    assert kwargs["pooled_g"] == pytest.approx(math.log(0.851))
    assert kwargs["log_scale"] is True
