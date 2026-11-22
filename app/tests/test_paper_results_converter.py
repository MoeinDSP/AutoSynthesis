import pytest


def test_regression_row_can_use_m_diff_and_se_diff():
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1",
        "study_label": "Study 1",
        "paper_title": "Example paper",
        "outcome_name": "Primary outcome",
        "result_role": "primary_outcome",
        "statistic_type": "regression",
        "M_diff": 2.0,
        "SE_diff": 1.0,
        "n_total": 100,
    }

    converted = _convert_row(row)

    assert converted["Include/Exclude"] == "Include"
    assert converted["cohens_d"] != ""
    assert converted["hedges_g"] != ""
    assert converted["M_diff"] == 2.0
    assert converted["SE_diff"] == 1.0


def _numerically_complete_row(**overrides):
    row = dict(
        paper_id="paper-1", study_label="Study 1", paper_title="Example paper",
        outcome_name="Overall memory functioning, baseline-to-long-term follow-up change",
        result_role="primary_outcome", statistic_type="regression",
        M_diff=2.0, SE_diff=1.0, n_total=100,
    )
    row.update(overrides)
    return row


def test_meta_analysis_candidate_false_excludes_even_a_computable_row():
    from utils.paper_results_converter import _convert_row
    row = _numerically_complete_row(meta_analysis_candidate=False)
    converted = _convert_row(row)
    assert converted["Include/Exclude"] == "Exclude"
    assert "meta_analysis_candidate" in converted["Comment"]


def test_meta_analysis_candidate_true_still_includes_a_computable_row():
    from utils.paper_results_converter import _convert_row
    row = _numerically_complete_row(meta_analysis_candidate=True)
    assert _convert_row(row)["Include/Exclude"] == "Include"
    row_no_field = _numerically_complete_row()
    assert _convert_row(row_no_field)["Include/Exclude"] == "Include"


def test_meta_analysis_candidate_false_does_not_overwrite_a_real_exclusion_reason():
    from utils.paper_results_converter import _convert_row
    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Some outcome", "result_role": "primary_outcome",
        "statistic_type": "unclear", "meta_analysis_candidate": False,
    }
    converted = _convert_row(row)
    assert converted["Include/Exclude"] == "Exclude"


def _lab_unit_row(**overrides):
    row = dict(
        paper_id="paper-1", study_label="Study 1", paper_title="Example paper",
        outcome_name="Triglycerides at 6 months", result_role="secondary_outcome",
        statistic_type="descriptive",
        group_1_label="Control", group_1_n=45, group_1_mean=-12.7, group_1_sd=52.7,
        group_2_label="Treatment", group_2_n=52, group_2_mean=2.5, group_2_sd=63.8,
        outcome_units="mg/dl",
    )
    row.update(overrides)
    return row


def test_unit_conversion_factor_and_canonical_rescale_means_sds_and_units():
    from utils.paper_results_converter import _convert_row

    row = _lab_unit_row(
        outcome_unit_conversion_factor=0.0113,
        outcome_units_canonical="mmol/L",
    )
    converted = _convert_row(row)

    assert converted["outcome_units"] == "mmol/L"
    assert converted["M_control"] == pytest.approx(-12.7 * 0.0113)
    assert converted["SD_control"] == pytest.approx(52.7 * 0.0113)
    assert converted["M_treatment"] == pytest.approx(2.5 * 0.0113)
    assert converted["SD_treatment"] == pytest.approx(63.8 * 0.0113)
    # Audit trail: original unit and factor are preserved for review.
    assert converted["outcome_units_original"] == "mg/dl"
    assert converted["outcome_unit_conversion_factor"] == 0.0113


def test_unit_conversion_requires_both_factor_and_canonical():
    from utils.paper_results_converter import _convert_row

    # Factor alone, no canonical unit name -> no conversion applied.
    row = _lab_unit_row(outcome_unit_conversion_factor=0.0113)
    converted = _convert_row(row)
    assert converted["outcome_units"] == "mg/dl"
    assert converted["M_control"] == -12.7
    assert converted["outcome_units_original"] == ""

    # Canonical unit alone, no factor -> no conversion applied.
    row2 = _lab_unit_row(outcome_units_canonical="mmol/L")
    converted2 = _convert_row(row2)
    assert converted2["outcome_units"] == "mg/dl"
    assert converted2["M_control"] == -12.7


def test_no_unit_conversion_fields_leaves_values_and_units_unchanged():
    from utils.paper_results_converter import _convert_row

    row = _lab_unit_row()
    converted = _convert_row(row)
    assert converted["outcome_units"] == "mg/dl"
    assert converted["M_control"] == -12.7
    assert converted["SD_control"] == 52.7
    assert converted["M_treatment"] == 2.5
    assert converted["SD_treatment"] == 63.8
    assert converted["outcome_units_original"] == ""
    assert converted["outcome_unit_conversion_factor"] == ""


def test_dichotomous_row_derives_n_treatment_n_control_from_group_totals_when_group_n_absent():
    """Regression guard for the real CD007674 bug: a dichotomous row that only
    fills group_1_events/group_1_total/group_2_events/group_2_total (never the
    continuous-style group_1_n/group_2_n) must still get n_treatment/n_control/
    n_total populated from those totals -- otherwise it silently vanishes later
    in agents/effect_size_agent.py, which has no group_*_total fallback of its
    own, despite having perfectly complete, poolable event/total counts."""
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Trial dropout at 6 months", "result_role": "secondary_outcome",
        "statistic_type": "proportion",
        "group_1_label": "Control", "group_1_events": 9.0, "group_1_total": 26.0,
        "group_2_label": "Treatment", "group_2_events": 8.0, "group_2_total": 26.0,
        # Deliberately no group_1_n/group_2_n/n_treatment/n_control/n_total --
        # this is exactly what the real Wetherell 2003 extraction looked like.
    }
    converted = _convert_row(row)

    assert converted["n_treatment"] == 26
    assert converted["n_control"] == 26
    assert converted["n_total"] == 52
    # A usable effect size must actually be computed from the counts.
    assert converted["cohens_d"] != ""
    assert converted["hedges_g"] != ""
    assert converted["Include/Exclude"] == "Include"


def test_group_n_still_wins_over_group_total_when_both_present():
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Some outcome", "result_role": "secondary_outcome",
        "statistic_type": "descriptive",
        "group_1_n": 40, "group_1_mean": 5.0, "group_1_sd": 1.0,
        "group_2_n": 42, "group_2_mean": 6.0, "group_2_sd": 1.0,
        # group_*_total absent entirely here -- unaffected by the fallback.
    }
    converted = _convert_row(row)
    assert converted["n_treatment"] == 42
    assert converted["n_control"] == 40


def test_double_zero_event_row_excluded_not_continuity_corrected():
    """Cochrane/RevMan convention: a study with zero events in BOTH arms is
    marked 'Not estimable' and excluded from a ratio-measure pool, rather than
    given a manufactured near-null value via continuity correction. Purely
    data-driven (both event counts are exactly zero) -- generic across any
    review/study, matching the real Hui 2017 (0/32 vs 0/31) case in CD007674."""
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Trial dropout at 6 months", "result_role": "secondary_outcome",
        "statistic_type": "proportion",
        "group_1_label": "Control", "group_1_events": 0.0, "group_1_total": 31.0,
        "group_2_label": "Treatment", "group_2_events": 0.0, "group_2_total": 32.0,
    }
    converted = _convert_row(row)

    assert converted["Include/Exclude"] == "Exclude"
    assert "not estimable" in converted["Comment"].lower()
    assert converted["cohens_d"] == ""


def test_single_zero_event_arm_still_pools_normally():
    """Regression guard: only the double-zero (BOTH arms zero) case is
    excluded -- a single zero-event arm (a real, informative comparison) must
    still be computed normally via the existing continuity-corrected escalc
    path, unchanged from before this fix."""
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Some dichotomous outcome", "result_role": "secondary_outcome",
        "statistic_type": "proportion",
        "group_1_label": "Control", "group_1_events": 0.0, "group_1_total": 20.0,
        "group_2_label": "Treatment", "group_2_events": 3.0, "group_2_total": 22.0,
    }
    converted = _convert_row(row)

    assert converted["Include/Exclude"] == "Include"
    assert converted["cohens_d"] != ""


def test_cohens_d_always_uses_raw_sign_regardless_of_outcome_scale_direction():
    """cohens_d/hedges_g must ALWAYS keep the raw (treatment - control)/SD sign, matching
    Cochrane/RevMan's own convention -- _convert_row() takes no scale-direction input at all
    any more. plan.higher_score_is_worse is consulted ONLY downstream, to compute the
    separate favors_treatment field (see utils.effect_measures.determine_favors_treatment and
    agents/effect_size_agent.py) -- it must never change the numeric value itself. Regression
    guard for reverting the CD012746-era sign-flip: a treatment arm scoring LOWER than control
    must still produce a NEGATIVE raw value here, even though that would be a benefit on a
    lower-is-better scale like ECBI."""
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "ECBI Problem subscale", "result_role": "primary_outcome",
        "statistic_type": "descriptive",
        # Treatment (group_2) scored LOWER than control (group_1) -- on a lower-is-better
        # scale this is a BENEFIT for treatment, but the raw statistical sign is still negative.
        "group_1_n": 15, "group_1_mean": 12.47, "group_1_sd": 10.15,
        "group_2_n": 13, "group_2_mean": 2.15, "group_2_sd": 3.36,
    }

    converted = _convert_row(row)

    assert converted["cohens_d"] < 0
    assert converted["hedges_g"] < 0

    # _convert_row() no longer accepts any scale-direction parameter at all.
    with pytest.raises(TypeError):
        _convert_row(dict(row), reverse_scale=True)


def test_sd_derived_from_reported_se_when_no_sd_or_ci_given():
    """A paper reporting standard error (not SD) for least-squares/adjusted means -- e.g.
    Mersky et al. 2016's 3-arm ANCOVA table -- previously fell through to "insufficient
    numeric information" because nothing ever converted group_1_se/group_2_se into
    SD_control/SD_treatment. SD = SE * sqrt(n) is an exact identity, not an approximation."""
    import math
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Some outcome", "result_role": "primary_outcome",
        "statistic_type": "descriptive",
        "group_1_n": 39, "group_1_mean": 11.9, "group_1_se": 1.35,
        "group_2_n": 19, "group_2_mean": 10.8, "group_2_se": 1.97,
    }

    converted = _convert_row(row)

    assert converted["Include/Exclude"] == "Include"
    assert converted["SD_control"] == pytest.approx(1.35 * math.sqrt(39))
    assert converted["SD_treatment"] == pytest.approx(1.97 * math.sqrt(19))


def test_directly_reported_sd_wins_over_se():
    """A directly-reported SD must never be overwritten by an SE-derived value, even when
    both fields happen to be filled on the same row."""
    from utils.paper_results_converter import _convert_row

    row = {
        "paper_id": "paper-1", "study_label": "Study 1", "paper_title": "Example paper",
        "outcome_name": "Some outcome", "result_role": "primary_outcome",
        "statistic_type": "descriptive",
        "group_1_n": 39, "group_1_mean": 11.9, "group_1_sd": 8.43, "group_1_se": 1.35,
        "group_2_n": 19, "group_2_mean": 10.8, "group_2_sd": 8.59, "group_2_se": 1.97,
    }

    converted = _convert_row(row)

    assert converted["SD_control"] == 8.43
    assert converted["SD_treatment"] == 8.59
