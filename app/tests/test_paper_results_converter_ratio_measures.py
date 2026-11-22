"""utils/paper_results_converter.py::_convert_row -- RR/HR/median-IQR
conversion paths, and the guard against silently deriving a substitute
measure when a paper names one but provides no numeric value. Built directly
from the CD008986 root-cause investigation (see cochrane_benchmark/README.md
and the manual-download run's meta_analysis_results_by_group.json)."""

from utils.paper_results_converter import _convert_row


def _base(**overrides):
    row = dict(
        paper_id="p1", paper_title="t", outcome_name="mortality",
        statistic_type="other", result_role="primary_outcome",
        comparison_type="between_subjects",
        group_1_n=100, group_2_n=100,
    )
    row.update(overrides)
    return row


def test_rr_only_row_now_converts_regression_for_silent_exclusion_bug():
    # Previously: RR was extracted but had NO conversion branch in
    # _convert_row's main chain -- fell straight to the catch-all
    # "unsupported or insufficient statistic type" exclusion.
    row = _base(risk_ratio=0.75, ci_lower_rr=0.6, ci_upper_rr=0.9,
                reported_effect_measure="risk ratio")
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["hedges_g"] != ""
    assert out["risk_ratio"] == 0.75
    assert out["conversion_method"] == "reported_rr"


def test_hr_row_with_numeric_value_converts_with_approximation_tag():
    row = _base(hazard_ratio=1.3, ci_lower_hr=1.0, ci_upper_hr=1.6,
                reported_effect_measure="hazard ratio")
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["hedges_g"] != ""
    assert out["hazard_ratio"] == 1.3
    assert out["conversion_method"] == "hr_to_d_approx"


def test_hr_named_but_no_value_is_explicitly_excluded_not_reverse_engineered():
    # Regression test for the exact CD008986 bug: a row whose paper reports
    # a hazard ratio, but only raw arm proportions were also extracted, used
    # to get silently routed through the "two proportions -> OR -> d"
    # fallback -- producing a Hedges' g with nothing to do with the actual
    # adjusted/time-to-event hazard ratio, and no warning at all.
    row = _base(reported_effect_measure="hazard ratio",
                group_1_mean=0.69, group_2_mean=0.67)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Exclude"
    assert out["hedges_g"] == ""
    assert "HR" in out["Comment"]
    assert "no numeric value" in out["Comment"]


def test_or_named_but_no_value_also_guarded():
    row = _base(reported_effect_measure="odds ratio",
                group_1_mean=0.60, group_2_mean=0.40)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Exclude"
    assert "OR" in out["Comment"]


def test_plain_proportions_still_convert_when_no_ratio_measure_named():
    # The guard must not break the existing, legitimate proportions->OR->d
    # fallback for rows that never named a measure at all.
    row = _base(group_1_mean=0.60, group_2_mean=0.40)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["conversion_method"] == "proportions_OR"


def test_median_iqr_row_converts_via_wan_2014_and_is_tagged_approximate():
    row = _base(
        group_1_median=10, group_1_iqr_lower=8, group_1_iqr_upper=13,
        group_2_median=7, group_2_iqr_lower=5, group_2_iqr_upper=9,
    )
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["hedges_g"] != ""
    assert out["conversion_method"] == "median_iqr_wan2014_approx"
    assert "APPROXIMATION" in out["Comment"]
    # The directly-reported-mean/SD GT columns must stay blank -- an
    # ESTIMATED mean/SD must never impersonate a directly-reported one.
    assert out["M_treatment"] == ""
    assert out["SD_treatment"] == ""


def test_median_range_row_also_converts():
    row = _base(
        group_1_median=10, group_1_range_lower=4, group_1_range_upper=20,
        group_2_median=7, group_2_range_lower=2, group_2_range_upper=15,
    )
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["conversion_method"] == "median_range_wan2014_approx"


def test_means_sds_row_unaffected_conversion_method_populated():
    row = _base(group_1_mean=5.0, group_1_sd=1.2, group_2_mean=6.0, group_2_sd=1.3)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["conversion_method"] == "means_sds"


def test_odds_ratio_still_converts_exactly_as_before():
    row = _base(odds_ratio=1.5, ci_lower_or=1.1, ci_upper_or=2.0,
                reported_effect_measure="odds ratio")
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["conversion_method"] == "reported_or"


def test_raw_2x2_counts_convert_via_exact_escalc_or():
    # Regression test for the biggest single yield gap found in the
    # CD008986 re-run: 13+ rows had complete, valid 2x2 event counts (a
    # Fisher's exact test, a chi-square test, or just "n events / N" with no
    # pre-computed OR/RR/HR) but the main conversion chain had NO branch for
    # them at all -- they fell straight through to the catch-all exclusion
    # even though the counts alone are everything metafor needs.
    row = _base(group_1_events=172, group_1_total=391, group_2_events=141, group_2_total=371)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["hedges_g"] != ""
    assert out["conversion_method"] == "counts_to_or_via_escalc"


def test_raw_2x2_counts_use_rr_when_paper_names_it():
    row = _base(group_1_events=172, group_1_total=391, group_2_events=141, group_2_total=371,
                reported_effect_measure="risk ratio")
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["conversion_method"] == "counts_to_rr_via_escalc"


def test_raw_2x2_counts_preferred_over_proportions_approximation():
    # When BOTH raw counts and means-as-proportions happen to be present,
    # the exact counts-based conversion must win over the coarser
    # proportions-reconstruction approximation (Priority 5).
    row = _base(group_1_events=172, group_1_total=391, group_2_events=141, group_2_total=371,
                group_1_mean=0.44, group_2_mean=0.38)
    out = _convert_row(row)
    assert out["conversion_method"] == "counts_to_or_via_escalc"


def test_invalid_counts_do_not_crash_fall_through_to_exclusion():
    # events >= total is nonsensical -- must not attempt escalc on it.
    row = _base(group_1_events=400, group_1_total=391, group_2_events=141, group_2_total=371)
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Exclude"


def test_mean_plus_95_ci_derives_sd_and_converts():
    # Regression test for a real yield gap found investigating CD008986's
    # ED-contacts pool: "mean with 95% CI, no SD" is a completely standard
    # reporting format (Cochrane Handbook 6.5.2.3 gives the exact SD
    # derivation) but previously had no conversion path -- a paper reporting
    # its outcome this way was silently excluded even though a directly-
    # reported mean and an exact, non-approximate SD derivation were both
    # available.
    row = _base(
        group_1_mean=5.2, group_1_ci_lower=4.5, group_1_ci_upper=5.9,
        group_2_mean=4.1, group_2_ci_lower=3.6, group_2_ci_upper=4.6,
    )
    out = _convert_row(row)
    assert out["Include/Exclude"] == "Include"
    assert out["hedges_g"] != ""
    assert out["conversion_method"] == "means_ci_derived_sd"
    assert out["SD_treatment"] != "" and out["SD_control"] != ""
    assert "derived from its reported mean CI" in out["Comment"]


def test_mean_plus_ci_respects_explicit_confidence_level():
    row_95 = _base(group_1_mean=5.2, group_1_ci_lower=4.5, group_1_ci_upper=5.9,
                    group_2_mean=4.1, group_2_ci_lower=3.6, group_2_ci_upper=4.6)
    row_90 = dict(row_95, ci_level=90)
    out_95 = _convert_row(row_95)
    out_90 = _convert_row(row_90)
    # A narrower confidence level (90% vs 95%) implies a SMALLER SD for the
    # SAME reported interval width -- different z, different derived SD.
    assert out_90["SD_treatment"] != out_95["SD_treatment"]


def test_explicit_sd_always_wins_over_ci_derivation():
    row = _base(group_1_mean=5.2, group_1_sd=1.1, group_1_ci_lower=4.5, group_1_ci_upper=5.9,
                group_2_mean=4.1, group_2_sd=1.0)
    out = _convert_row(row)
    assert out["conversion_method"] == "means_sds"  # not means_ci_derived_sd
    assert out["SD_control"] == 1.1  # the explicit SD, not a CI-derived one


def test_degenerate_ci_does_not_crash_or_derive_nonsense():
    # ci_upper < ci_lower (bad extraction) must not produce a fake SD.
    row = _base(group_1_mean=5.2, group_1_ci_lower=5.9, group_1_ci_upper=4.5,
                group_2_mean=4.1, group_2_ci_lower=3.6, group_2_ci_upper=4.6)
    out = _convert_row(row)
    assert out["conversion_method"] != "means_ci_derived_sd"


def test_swapped_arm_labels_corrected_and_sign_flips():
    # Regression test built directly from a real, confirmed bug: a paper's
    # own table listed the intervention arm first, so the extractor filled
    # group_1_* (this pipeline's CONTROL slot) with the intervention's
    # numbers and group_2_* (TREATMENT slot) with control's -- silently
    # inverting the computed direction. Here: true intervention=0/51 events,
    # true control=4/53 -- intervention arm has FEWER events (favors
    # intervention), but with labels swapped as extracted, must be detected
    # and corrected to negative Hedges' g (favors intervention), not positive.
    row = _base(
        group_1_label="intervention group", group_1_events=0, group_1_total=51, group_1_n=51,
        group_2_label="control group", group_2_events=4, group_2_total=53, group_2_n=53,
    )
    out = _convert_row(row)
    assert out["hedges_g"] < 0  # favors intervention, not > 0
    assert "swapped" in out["Comment"]
    assert "intervention" in out["Comment"] and "control" in out["Comment"]


def test_correctly_oriented_labels_never_touched():
    row = _base(
        group_1_label="Control/usual clinical care", group_1_events=27, group_1_total=128, group_1_n=128,
        group_2_label="Intervention/CAS-based pharmacist-physician intervention",
        group_2_events=27, group_2_total=126, group_2_n=126,
    )
    out = _convert_row(row)
    assert out["Comment"] == ""


def test_ambiguous_labels_never_guessed():
    # No generic control/intervention/add-on signal in either label -- must
    # NOT be "corrected" (a wrong guess here would be worse than doing nothing).
    row = _base(
        group_1_label="Group A", group_1_events=5, group_1_total=50, group_1_n=50,
        group_2_label="Group B", group_2_events=10, group_2_total=50, group_2_n=50,
    )
    out = _convert_row(row)
    assert out["Comment"] == ""


def test_missing_labels_never_guessed():
    row = _base(group_1_events=5, group_1_total=50, group_1_n=50,
                group_2_events=10, group_2_total=50, group_2_n=50)
    out = _convert_row(row)
    assert out["Comment"] == ""


def test_swap_correction_generic_not_disease_specific():
    # Same mechanism, completely different domain/wording -- must fire on
    # ANY generic RCT arm-orientation phrasing, not a hardcoded vocabulary.
    row = _base(
        group_1_label="Experimental group", group_1_mean=2.1, group_1_sd=0.5, group_1_n=40,
        group_2_label="Placebo", group_2_mean=3.4, group_2_sd=0.6, group_2_n=42,
    )
    out = _convert_row(row)
    assert "swapped" in out["Comment"]


# ---------------------------------------------------------------------------
# group_1_is_control -- the extractor's own explicit judgment (rule 21 in
# agents/statistical_result_extractor_agent.py), which must be trusted over
# the label-keyword fallback above. Built from the real CD015331 bug: a
# control arm's own label ("Treatment as usual alone", "Supportive therapy +
# treatment as usual") never matched the fixed keyword list at all, so the
# fallback silently never fired for roughly half the pooled studies -- no
# keyword list can be complete, but the extractor reading full paper text
# against this study's own treatment/control definitions can be.
# ---------------------------------------------------------------------------

def test_explicit_group_1_is_control_false_swaps_even_with_unmatchable_labels():
    # Neither label contains anything in the keyword list -- the fallback
    # alone would never correct this (this IS the real CD015331 bug case).
    row = _base(
        group_1_label="CBT plus treatment as usual", group_1_mean=8.6, group_1_sd=2.7, group_1_n=28,
        group_2_label="Treatment as usual alone", group_2_mean=10.7, group_2_sd=5.0, group_2_n=28,
        group_1_is_control=False,
    )
    out = _convert_row(row)
    assert "swapped" in out["Comment"]
    assert "itself stated" in out["Comment"]
    # After swapping, group_1 (now control) = 10.7, group_2 (now treatment) = 8.6.
    # This module's raw convention is g = treatment_mean - control_mean (no
    # lower-is-better flip baked in here -- that's a separate, later step),
    # so a lower treatment mean gives a NEGATIVE g.
    assert out["hedges_g"] < 0


def test_explicit_group_1_is_control_true_is_trusted_even_if_keywords_would_disagree():
    # group_1_label happens to contain "experimental" (an intervention-ish
    # word) but the extractor explicitly says group_1 IS the control arm for
    # this study -- the explicit field must win, no swap applied.
    row = _base(
        group_1_label="Experimental standard-care-only arm", group_1_mean=3.4, group_1_sd=0.6, group_1_n=42,
        group_2_label="CBT arm", group_2_mean=2.1, group_2_sd=0.5, group_2_n=40,
        group_1_is_control=True,
    )
    out = _convert_row(row)
    assert out["Comment"] == ""
    # No swap: group_1=control=3.4, group_2=treatment=2.1 -- g = treatment - control < 0.
    assert out["hedges_g"] < 0


def test_missing_group_1_is_control_still_uses_label_keyword_fallback():
    # Legacy rows (extracted before this field existed) must keep working
    # exactly as before via the fallback -- same case as
    # test_swapped_arm_labels_corrected_and_sign_flips, just re-asserting
    # the fallback path specifically still fires when the field is absent.
    row = _base(
        group_1_label="intervention group", group_1_events=0, group_1_total=51, group_1_n=51,
        group_2_label="control group", group_2_events=4, group_2_total=53, group_2_n=53,
    )
    out = _convert_row(row)
    assert "swapped" in out["Comment"]
    assert "itself stated" not in out["Comment"]
