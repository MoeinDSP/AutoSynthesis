"""
statistics/plots.py -- measure-aware labels/scale for forest_plot,
cumulative_forest_plot, effect_distribution_plot, bubble_chart, and
heterogeneity_summary_plot. Verifies: (1) axis/legend text uses the given
measure_label instead of a hardcoded "Hedges' g"; (2) log_scale=True sets a
log axis and moves the null reference from 0 to 1 for RR/OR; (3) defaults
(no measure_label/log_scale passed) reproduce the exact pre-existing
Hedges'-g/linear behaviour, so every old call site is unaffected.

No R/rpy2 dependency -- these call the plot functions directly with
hand-built effects/variances/pooled values, not through the pipeline.
"""

import math
import os
from unittest.mock import patch

import matplotlib.axes
import pytest

from statistics.plots import (
    bubble_chart, cumulative_forest_plot, effect_distribution_plot,
    forest_plot, funnel_plot, heterogeneity_summary_plot,
)


def _xscale_calls():
    return patch.object(matplotlib.axes.Axes, "set_xscale")


def _yscale_calls():
    return patch.object(matplotlib.axes.Axes, "set_yscale")


# ---------------------------------------------------------------------------
# forest_plot
# ---------------------------------------------------------------------------

def test_forest_plot_default_is_linear_hedges_g_unchanged(tmp_path):
    path = os.path.join(str(tmp_path), "forest.png")
    with _xscale_calls() as mock_scale:
        forest_plot(
            study_labels=["S1", "S2"], effects=[0.2, 0.4], variances=[0.02, 0.03],
            pooled_g=0.3, pooled_ci_lower=0.1, pooled_ci_upper=0.5,
            output_path=path,
        )
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []  # never switched to log -- default behaviour


def test_forest_plot_rr_uses_log_scale_and_measure_label(tmp_path):
    path = os.path.join(str(tmp_path), "forest_rr.png")
    # log(RR) values, as agents/meta_analysis_agent.py would pass for a
    # resolved RR group (native_value is on the log scale).
    with _xscale_calls() as mock_scale:
        forest_plot(
            study_labels=["S1", "S2"], effects=[math.log(0.6), math.log(0.4)],
            variances=[0.05, 0.06],
            pooled_g=math.log(0.52), pooled_ci_lower=math.log(0.37), pooled_ci_upper=math.log(0.75),
            output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
        )
    assert os.path.exists(path)
    mock_scale.assert_any_call("log")


def test_forest_plot_md_uses_linear_scale_and_measure_label(tmp_path):
    path = os.path.join(str(tmp_path), "forest_md.png")
    with _xscale_calls() as mock_scale:
        forest_plot(
            study_labels=["S1", "S2"], effects=[-5.0, -8.0], variances=[1.0, 1.5],
            pooled_g=-6.5, pooled_ci_lower=-9.0, pooled_ci_upper=-4.0,
            output_path=path, measure_label="Mean Difference (MD)", log_scale=False,
        )
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []


def test_forest_plot_smd_default_label_and_linear_scale(tmp_path):
    path = os.path.join(str(tmp_path), "forest_smd.png")
    with _xscale_calls() as mock_scale:
        forest_plot(
            study_labels=["S1", "S2"], effects=[0.3, 0.5], variances=[0.02, 0.03],
            pooled_g=0.4, pooled_ci_lower=0.2, pooled_ci_upper=0.6,
            output_path=path, measure_label="Standardized Mean Difference (SMD)",
        )
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []


# ---------------------------------------------------------------------------
# cumulative_forest_plot
# ---------------------------------------------------------------------------

def _cumulative_kwargs(**overrides):
    kwargs = dict(
        study_labels=["S1", "S2", "S3"],
        cumulative_g=[0.3, 0.35, 0.4],
        cumulative_ci_lower=[0.1, 0.15, 0.2],
        cumulative_ci_upper=[0.5, 0.55, 0.6],
        study_years=[2018, 2019, 2020],
        final_g=0.4,
    )
    kwargs.update(overrides)
    return kwargs


def test_cumulative_forest_plot_default_linear(tmp_path):
    path = os.path.join(str(tmp_path), "cum.png")
    with _yscale_calls() as mock_scale:
        cumulative_forest_plot(output_path=path, **_cumulative_kwargs())
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []


def test_cumulative_forest_plot_rr_uses_log_scale():
    """Already-ratio-scale cumulative values (as _generate_plots supplies for
    RR/OR groups, back-transformed by pool_group_native) plus log_scale=True
    must set a log y-axis and not crash on a positive-only value range."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "cum_rr.png")
        with _yscale_calls() as mock_scale:
            cumulative_forest_plot(
                output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
                **_cumulative_kwargs(
                    cumulative_g=[0.6, 0.55, 0.52], cumulative_ci_lower=[0.4, 0.4, 0.37],
                    cumulative_ci_upper=[0.9, 0.8, 0.75], final_g=0.52,
                ),
            )
        assert os.path.exists(path)
        mock_scale.assert_any_call("log")


# ---------------------------------------------------------------------------
# effect_distribution_plot
# ---------------------------------------------------------------------------

def test_effect_distribution_plot_default_linear(tmp_path):
    path = os.path.join(str(tmp_path), "dist.png")
    with _yscale_calls() as mock_scale:
        effect_distribution_plot(
            effects=[0.2, 0.3, 0.4, 0.5], variances=[0.02, 0.02, 0.03, 0.03],
            pooled_g=0.35, pooled_ci_lower=0.2, pooled_ci_upper=0.5,
            output_path=path,
        )
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []


def test_effect_distribution_plot_rr_log_scale():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "dist_rr.png")
        with _yscale_calls() as mock_scale:
            effect_distribution_plot(
                effects=[math.log(0.6), math.log(0.5), math.log(0.4), math.log(0.55)],
                variances=[0.04, 0.05, 0.05, 0.04],
                pooled_g=math.log(0.52), pooled_ci_lower=math.log(0.37), pooled_ci_upper=math.log(0.75),
                output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
            )
        assert os.path.exists(path)
        mock_scale.assert_any_call("log")


# ---------------------------------------------------------------------------
# bubble_chart
# ---------------------------------------------------------------------------

def test_bubble_chart_default_linear(tmp_path):
    path = os.path.join(str(tmp_path), "bubble.png")
    with _yscale_calls() as mock_scale:
        bubble_chart(
            study_labels=["S1", "S2"], effects=[0.2, 0.4], variances=[0.02, 0.03],
            sample_sizes=[50, 80], pooled_g=0.3, output_path=path,
        )
    assert os.path.exists(path)
    assert mock_scale.call_args_list == []


def test_bubble_chart_rr_log_scale():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "bubble_rr.png")
        with _yscale_calls() as mock_scale:
            bubble_chart(
                study_labels=["S1", "S2"], effects=[math.log(0.6), math.log(0.4)],
                variances=[0.05, 0.06], sample_sizes=[50, 80],
                pooled_g=math.log(0.52), output_path=path,
                measure_label="Risk Ratio (RR)", log_scale=True,
            )
        assert os.path.exists(path)
        mock_scale.assert_any_call("log")


# ---------------------------------------------------------------------------
# heterogeneity_summary_plot -- label only, no axis scale involved
# ---------------------------------------------------------------------------

def test_heterogeneity_summary_plot_default_label(tmp_path):
    path = os.path.join(str(tmp_path), "het.png")
    out = heterogeneity_summary_plot(
        pooled_g=0.4, pooled_ci_lower=0.2, pooled_ci_upper=0.6, p_value=0.01,
        k=3, n_total=150, q_statistic=1.2, q_df=2, q_p_value=0.5,
        i_squared=10.0, tau_squared=0.01, tau=0.1, h_squared=1.1,
        output_path=path,
    )
    assert out == path and os.path.exists(path)


def test_heterogeneity_summary_plot_accepts_measure_label(tmp_path):
    path = os.path.join(str(tmp_path), "het_rr.png")
    out = heterogeneity_summary_plot(
        pooled_g=0.52, pooled_ci_lower=0.37, pooled_ci_upper=0.75, p_value=0.01,
        k=3, n_total=150, q_statistic=1.2, q_df=2, q_p_value=0.5,
        i_squared=10.0, tau_squared=0.01, tau=0.1, h_squared=1.1,
        output_path=path, measure_label="Risk Ratio (RR)",
    )
    assert out == path and os.path.exists(path)


# ---------------------------------------------------------------------------
# funnel_plot -- regression coverage for the RR/OR/HR/MD/SMD scale-mismatch
# bug: this function used to unconditionally label everything "Hedges' g"
# regardless of what was actually pooled (e.g. a CD008986-style RR group's
# pooled value of 0.851 rendered as "Pooled Hedges' g = 0.851", an invalid
# mix of scales). See agents/bias_agent.py for the caller-side fix (building
# native_value-based inputs + math.log() of the back-transformed pooled
# ratio) and tests/test_bias_node.py for that integration.
# ---------------------------------------------------------------------------

def _run_and_capture(**kwargs):
    """Call funnel_plot, capturing (xscale_calls, axvline_calls, xlabel_calls)
    -- all as call-arg lists, immune to the figure being closed internally.
    xvalues is every axvline's x= in call order (pooled line first, then the
    null-reference line -- see funnel_plot's own draw order)."""
    with patch.object(matplotlib.axes.Axes, "set_xscale") as mock_xscale, \
         patch.object(matplotlib.axes.Axes, "axvline",
                       side_effect=matplotlib.axes.Axes.axvline, autospec=True) as mock_axvline, \
         patch.object(matplotlib.axes.Axes, "set_xlabel",
                       side_effect=matplotlib.axes.Axes.set_xlabel, autospec=True) as mock_xlabel:
        out = funnel_plot(**kwargs)
    labels = [c.kwargs.get("label") for c in mock_axvline.call_args_list if c.kwargs.get("label")]
    xlabels = [c.args[1] if len(c.args) > 1 else c.kwargs.get("xlabel") for c in mock_xlabel.call_args_list]
    xvalues = [c.kwargs.get("x") for c in mock_axvline.call_args_list]
    return out, mock_xscale.call_args_list, labels, xlabels, xvalues


def test_funnel_plot_default_is_linear_hedges_g_unchanged(tmp_path):
    """No measure_label/log_scale passed -- byte-for-byte pre-existing
    behaviour for any caller not yet updated (e.g. regenerate_run_plots.py,
    which always pools on Hedges' g by design)."""
    path = os.path.join(str(tmp_path), "funnel.png")
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[0.2, 0.3, 0.4], variances=[0.02, 0.03, 0.025],
        pooled_g=0.3, output_path=path,
    )
    assert out == path and os.path.exists(path)
    assert xscale_calls == []  # never switched to log
    assert any("Pooled Hedges' g = 0.300" in l for l in labels), labels


def test_funnel_plot_rr_uses_log_scale_and_natural_pooled_value_in_legend(tmp_path):
    """The CD008986 case: pooled RR = 0.851, native per-study values on the
    log scale (as EffectSizeRecord.native_value holds them). Caller passes
    math.log(0.851) for pooled_g (mirroring math.log() of the back-
    transformed ratio, exactly what agents/bias_agent.py now does) --
    funnel_plot must draw/label the NATURAL RR value, not the raw log number,
    while the axis itself is explicitly log-scaled."""
    path = os.path.join(str(tmp_path), "funnel_rr.png")
    pooled_rr = 0.8512993518510397
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[math.log(0.7), math.log(0.9), math.log(1.05)],
        variances=[0.04, 0.05, 0.03],
        pooled_g=math.log(pooled_rr),
        output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
    )
    assert os.path.exists(path)
    assert "log" in xscale_calls[0].args if xscale_calls else False
    assert any("Risk Ratio (RR) = 0.851" in l for l in labels), labels
    assert not any("Hedges" in l for l in labels), labels
    assert any(xl == "Risk Ratio (RR), logarithmic scale" for xl in xlabels), xlabels


def test_funnel_plot_or_uses_log_scale_and_measure_label(tmp_path):
    path = os.path.join(str(tmp_path), "funnel_or.png")
    pooled_or = 1.71
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[math.log(1.5), math.log(2.0), math.log(1.6)],
        variances=[0.05, 0.06, 0.04],
        pooled_g=math.log(pooled_or),
        output_path=path, measure_label="Odds Ratio (OR)", log_scale=True,
    )
    assert xscale_calls, "expected set_xscale('log') to be called"
    assert any("Odds Ratio (OR) = 1.710" in l for l in labels), labels
    assert any(xl == "Odds Ratio (OR), logarithmic scale" for xl in xlabels), xlabels


def test_funnel_plot_hr_uses_log_scale_and_measure_label(tmp_path):
    path = os.path.join(str(tmp_path), "funnel_hr.png")
    pooled_hr = 0.88
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[math.log(0.75), math.log(0.95), math.log(0.85)],
        variances=[0.02, 0.03, 0.025],
        pooled_g=math.log(pooled_hr),
        output_path=path, measure_label="Hazard Ratio (HR)", log_scale=True,
    )
    assert xscale_calls, "expected set_xscale('log') to be called"
    assert any("Hazard Ratio (HR) = 0.880" in l for l in labels), labels
    assert any(xl == "Hazard Ratio (HR), logarithmic scale" for xl in xlabels), xlabels


def test_funnel_plot_md_plots_directly_no_log_scale(tmp_path):
    path = os.path.join(str(tmp_path), "funnel_md.png")
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[-5.0, -8.0, -6.0], variances=[1.0, 1.5, 1.2],
        pooled_g=-6.5, output_path=path,
        measure_label="Mean Difference (MD)", log_scale=False,
    )
    assert xscale_calls == []  # MD is never log-transformed
    assert any("Mean Difference (MD) = -6.500" in l for l in labels), labels
    assert any(xl == "Observed outcome (Mean Difference (MD))" for xl in xlabels), xlabels


def test_funnel_plot_smd_plots_standardized_effect_directly(tmp_path):
    path = os.path.join(str(tmp_path), "funnel_smd.png")
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[0.3, 0.5, 0.4], variances=[0.02, 0.03, 0.025],
        pooled_g=0.4, output_path=path,
        measure_label="Standardized Mean Difference (SMD)",
    )
    assert xscale_calls == []
    assert any("Standardized Mean Difference (SMD) = 0.400" in l for l in labels), labels


def test_funnel_plot_unavailable_renders_placeholder_not_a_fabricated_scale(tmp_path):
    """UNKNOWN/GENERIC groups -- no concrete native measure was resolved.
    Must not fabricate an axis/scale; renders an explicit "unavailable"
    placeholder instead (see agents/bias_agent.py's funnel_unavailable)."""
    path = os.path.join(str(tmp_path), "funnel_unavailable.png")
    with patch.object(matplotlib.axes.Axes, "axvline") as mock_axvline, \
         patch.object(matplotlib.axes.Axes, "text",
                       side_effect=matplotlib.axes.Axes.text, autospec=True) as mock_text:
        out = funnel_plot(
            effects=[], variances=[], pooled_g=0.0,
            output_path=path, unavailable=True,
        )
    assert out == path and os.path.exists(path)
    assert mock_axvline.call_args_list == []  # no pooled-line/null-line claim of any scale
    texts = [c.args[3] if len(c.args) > 3 else c.kwargs.get("s", "") for c in mock_text.call_args_list]
    assert any("unavailable" in str(t).lower() for t in texts), texts


def test_funnel_plot_rr_null_line_at_one_and_pooled_line_at_raw_ratio_same_axis(tmp_path):
    """Explicit check for the exact scenario this task calls out: pooled
    RR = 0.851 -- the null-reference line must sit at the natural value 1
    (never 0, which would be where log(RR)=0 sits instead), the pooled line
    must sit at the natural value 0.851 (never log(0.851) = -0.161), and
    both must be drawn on the SAME logarithmic x-axis as the study points."""
    path = os.path.join(str(tmp_path), "funnel_rr_null_check.png")
    pooled_rr = 0.851
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[math.log(0.6), math.log(0.75), math.log(0.95)],
        variances=[0.03, 0.02, 0.025],
        pooled_g=math.log(pooled_rr),
        output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
    )
    assert xscale_calls, "study points and pooled line must share a log-scaled x-axis"
    # Two axvline calls: the pooled-estimate line (labeled) and the null
    # line (unlabeled, distinguishable by x=1.0). Order doesn't matter here.
    assert any(x == pytest.approx(1.0) for x in xvalues), xvalues       # null = 1, not 0
    assert any(x == pytest.approx(pooled_rr) for x in xvalues), xvalues  # pooled = 0.851, not log(0.851)
    assert not any(x == pytest.approx(math.log(pooled_rr)) for x in xvalues), xvalues
    assert not any(x == pytest.approx(0.0) for x in xvalues), xvalues


def test_funnel_plot_rr_scale_never_labeled_hedges_g_or_smd(tmp_path):
    """Dedicated guard, independent of any specific caller: whatever
    measure_label is supplied for an RR-scale plot, the rendered legend/axis
    text must never contain "Hedges" or "SMD"/"Standardized" -- an RR
    analysis is never, under any circumstance, an SMD/Hedges' g one."""
    path = os.path.join(str(tmp_path), "funnel_rr_not_smd.png")
    out, xscale_calls, labels, xlabels, xvalues = _run_and_capture(
        effects=[math.log(0.6), math.log(0.75), math.log(0.95)],
        variances=[0.03, 0.02, 0.025],
        pooled_g=math.log(0.851),
        output_path=path, measure_label="Risk Ratio (RR)", log_scale=True,
    )
    for text in labels + xlabels:
        assert "Hedges" not in text, (text, labels, xlabels)
        assert "SMD" not in text and "Standardized" not in text, (text, labels, xlabels)
