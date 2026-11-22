"""
End-to-end: agents/meta_analysis_agent.py's real resolution + real R/metafor
pooling + real plot generation, verifying the plotting layer actually
receives the resolved effect_measure/computation_scale (not just that
statistics/plots.py's own functions behave correctly in isolation -- see
tests/test_plots_measure_aware.py for that). One scenario each for RR, MD,
SMD (explicit), and the UNKNOWN->Hedges' g fallback.
"""

import math
from unittest.mock import MagicMock, patch

import matplotlib.axes
import pytest

from models import EffectMeasure, EffectSizeRecord
from utils.outcome_grouping import build_outcome_group_key


def _es(study_id, g=0.3, var=0.02, n_t=50, n_c=50, **kw):
    n_total = n_t + n_c
    return EffectSizeRecord(
        study_id=study_id, report_id=study_id, cohens_d=g, hedges_g=g, variance=var,
        se=var ** 0.5, ci_lower=g - 1.96 * var ** 0.5, ci_upper=g + 1.96 * var ** 0.5,
        n_total=n_total, computation_method="means_sds",
        outcome_name="Outcome", outcome_family="family", follow_up_timepoint=None,
        outcome_group_key=build_outcome_group_key("family", None),
        **kw,
    )


@pytest.fixture(autouse=True)
def _mock_llm_interpretation():
    mock_resp = MagicMock()
    mock_resp.content = "Mocked interpretation."
    with patch("agents.meta_analysis_agent.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_resp
        yield mock_llm


def _run(effect_sizes, tmp_path, plan=None):
    from agents.meta_analysis_agent import meta_analysis_node
    state = {"effect_sizes": effect_sizes, "output_dir": str(tmp_path), "plan": plan}
    return meta_analysis_node(state)


def _xscale_and_yscale_patches():
    return (
        patch.object(matplotlib.axes.Axes, "set_xscale"),
        patch.object(matplotlib.axes.Axes, "set_yscale"),
    )


def test_rr_group_resolves_and_plots_on_log_scale(tmp_path):
    rows = [
        _es("p1", reported_effect_measure="risk ratio",
            raw_measure_inputs={"events_treatment": 12, "n_treatment": 60, "events_control": 24, "n_control": 60}),
        _es("p2", reported_effect_measure="Risk Ratio",
            raw_measure_inputs={"events_treatment": 8, "n_treatment": 50, "events_control": 18, "n_control": 50}),
        _es("p3", reported_effect_measure="risk ratio",
            raw_measure_inputs={"events_treatment": 15, "n_treatment": 70, "events_control": 25, "n_control": 70}),
    ]
    xp, yp = _xscale_and_yscale_patches()
    with xp as mock_x, yp as mock_y:
        result = _run(rows, tmp_path)

    group = result["meta_results"][0]
    assert group.effect_measure == EffectMeasure.RR
    assert group.computation_scale == EffectMeasure.RR
    assert not group.insufficient_data

    # forest_plot uses set_xscale("log"); cumulative/distribution/bubble use set_yscale.
    mock_x.assert_any_call("log")
    mock_y.assert_any_call("log")
    assert result["meta_plots"]["forest"].endswith("forest_plot.png")


def test_md_group_resolves_and_plots_stay_linear(tmp_path):
    rows = [
        _es("p1", outcome_units="mmHg",
            raw_measure_inputs={"mean_treatment": 128.0, "sd_treatment": 9.0, "n_treatment": 40,
                                  "mean_control": 134.0, "sd_control": 10.0, "n_control": 40}),
        _es("p2", outcome_units="mmHg",
            raw_measure_inputs={"mean_treatment": 122.0, "sd_treatment": 8.5, "n_treatment": 35,
                                  "mean_control": 129.0, "sd_control": 9.5, "n_control": 35}),
    ]
    xp, yp = _xscale_and_yscale_patches()
    with xp as mock_x, yp as mock_y:
        result = _run(rows, tmp_path)

    group = result["meta_results"][0]
    assert group.effect_measure == EffectMeasure.MD
    assert group.computation_scale == EffectMeasure.MD
    assert not group.insufficient_data

    assert "log" not in [c.args[0] for c in mock_x.call_args_list if c.args]
    assert "log" not in [c.args[0] for c in mock_y.call_args_list if c.args]


def test_smd_group_explicit_resolution_still_linear(tmp_path):
    rows = [
        _es("p1", g=0.42, var=0.03, reported_effect_measure="standardized mean difference"),
        _es("p2", g=0.31, var=0.025, reported_effect_measure="standardized mean difference"),
    ]
    xp, yp = _xscale_and_yscale_patches()
    with xp as mock_x, yp as mock_y:
        result = _run(rows, tmp_path)

    group = result["meta_results"][0]
    assert group.effect_measure == EffectMeasure.SMD
    assert group.computation_scale == EffectMeasure.SMD
    assert group.effect_measure_source == "explicit_paper_reported"

    assert "log" not in [c.args[0] for c in mock_x.call_args_list if c.args]
    assert "log" not in [c.args[0] for c in mock_y.call_args_list if c.args]


def test_unknown_group_falls_back_to_hedges_g_and_linear_plots(tmp_path):
    """No reported_effect_measure, no outcome_units, no raw counts -- nothing
    resolves the measure, and the group must still be pooled+plotted (via
    the Hedges' g fallback), never crash or silently claim a native measure."""
    rows = [_es("p1", g=0.3, var=0.02), _es("p2", g=0.4, var=0.02)]
    xp, yp = _xscale_and_yscale_patches()
    with xp as mock_x, yp as mock_y:
        result = _run(rows, tmp_path)

    group = result["meta_results"][0]
    assert group.effect_measure == EffectMeasure.UNKNOWN
    assert group.computation_scale == EffectMeasure.HEDGES_G
    assert group.effect_measure_source == "unresolved_fallback"
    assert not group.insufficient_data  # still pooled -- fallback, not a failure

    assert "log" not in [c.args[0] for c in mock_x.call_args_list if c.args]
    assert "log" not in [c.args[0] for c in mock_y.call_args_list if c.args]
    assert result["meta_plots"]["forest"].endswith("forest_plot.png")
