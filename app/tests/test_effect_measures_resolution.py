"""
utils/effect_measures.py -- native effect-measure resolution hierarchy.

Regression-anchors the two corrections the user explicitly required over
the first proposed design:
  1. Event counts alone (no explicit OR/RR reported anywhere) must NOT
     resolve to Risk Ratio -- must stay UNKNOWN.
  2. Matching outcome_measurement TEXT alone must NOT resolve to Mean
     Difference -- requires matching, non-empty outcome_units too.
"""

import pytest

from models import EffectMeasure, EffectSizeRecord, MetaAnalysisPlan


def _es(**kwargs):
    defaults = dict(
        study_id="S1", report_id="R1", cohens_d=0.3, hedges_g=0.3,
        variance=0.02, se=0.14, ci_lower=0.02, ci_upper=0.58, n_total=50,
        computation_method="means_sds",
    )
    defaults.update(kwargs)
    return EffectSizeRecord(**defaults)


def _plan(**kwargs):
    return MetaAnalysisPlan(
        research_question="x", treatment_label="t", control_label="c",
        outcome_description="o", positive_direction="d", search_queries=[],
        inclusion_criteria=[], exclusion_criteria=[], moderators_to_extract=[],
        **kwargs,
    )


# ---------------------------------------------------------------------------
# The two explicitly-rejected heuristics must NOT resolve anything
# ---------------------------------------------------------------------------

def test_event_counts_alone_do_not_resolve_to_risk_ratio():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(raw_measure_inputs={"events_treatment": 12, "n_treatment": 50, "events_control": 20, "n_control": 50}),
        _es(raw_measure_inputs={"events_treatment": 8, "n_treatment": 40, "events_control": 15, "n_control": 40}),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN
    assert resolution.computation_scale == EffectMeasure.HEDGES_G
    assert resolution.source == "unresolved_fallback"


def test_same_measurement_text_alone_does_not_resolve_to_mean_difference():
    """outcome_units intentionally left unset on both rows -- only the
    (irrelevant to this function) outcome_measurement free-text would match
    upstream; that alone must not be sufficient."""
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(outcome_units=None), _es(outcome_units=None)]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN
    assert resolution.computation_scale == EffectMeasure.HEDGES_G


def test_matching_units_alone_does_resolve_to_md_deterministic_evidence():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(outcome_units="mmHg"), _es(outcome_units="mmHg")]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.source == "deterministic_evidence"
    assert resolution.conflict is None


def test_mismatched_units_do_not_resolve_to_md():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(outcome_units="mmHg"), _es(outcome_units="points on HAM-D")]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN


# ---------------------------------------------------------------------------
# Scale harmonization: different-range instruments measuring the same
# construct (e.g. a 0-10 NRS and a 100mm VAS) pool as MD on a common
# rescaled footing, mirroring Cochrane's own stated convention (confirmed
# verbatim in CD014428's Methods: "we expressed these on a common 0 to 100
# scale as a mean difference"). Built directly from that real investigation:
# CD014428 pooled on Hedges' g (I^2=80.73%) where Cochrane pooled on a
# harmonized MD (I^2=0%) because different pain instruments' raw units were
# never reconciled onto one scale.
# ---------------------------------------------------------------------------

def test_rows_have_harmonizable_scale_range_true_when_all_rows_state_a_range():
    from utils.effect_measures import rows_have_harmonizable_scale_range

    rows = [
        _es(raw_measure_inputs={"scale_min": 0, "scale_max": 10}),
        _es(raw_measure_inputs={"scale_min": 0, "scale_max": 100}),
    ]
    assert rows_have_harmonizable_scale_range(rows) is True


def test_rows_have_harmonizable_scale_range_false_if_any_row_missing_it():
    from utils.effect_measures import rows_have_harmonizable_scale_range

    rows = [
        _es(raw_measure_inputs={"scale_min": 0, "scale_max": 10}),
        _es(raw_measure_inputs={}),  # no range stated for this row
    ]
    assert rows_have_harmonizable_scale_range(rows) is False


def test_rows_have_harmonizable_scale_range_false_when_degenerate():
    from utils.effect_measures import rows_have_harmonizable_scale_range

    rows = [_es(raw_measure_inputs={"scale_min": 10, "scale_max": 10})]  # min == max
    assert rows_have_harmonizable_scale_range(rows) is False


def test_different_bounded_scales_resolve_to_md_via_harmonization():
    """Different outcome_units text (so the existing identical-units path
    does NOT fire), but every row states its own instrument's range --
    this alone must be sufficient to resolve to MD."""
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(outcome_units="cm on a 10 cm VAS", raw_measure_inputs={"scale_min": 0, "scale_max": 10}),
        _es(outcome_units="mm on a 100 mm VAS", raw_measure_inputs={"scale_min": 0, "scale_max": 100}),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.source == "deterministic_evidence"


def test_one_row_missing_scale_range_does_not_force_harmonized_md():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(outcome_units="cm on a 10 cm VAS", raw_measure_inputs={"scale_min": 0, "scale_max": 10}),
        _es(outcome_units="a validated pain scale", raw_measure_inputs={}),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN
    assert resolution.computation_scale == EffectMeasure.HEDGES_G


def test_compute_native_row_effect_rescales_onto_the_common_range():
    """A 0-10 NRS row (2 vs 4, SD 1) rescaled to 0-100 becomes 20 vs 40,
    SD 10 -- MD should land at -20, not the raw-scale -2."""
    from utils.effect_measures import compute_native_row_effect

    inp = {
        "mean_treatment": 2.0, "sd_treatment": 1.0, "n_treatment": 20.0,
        "mean_control": 4.0, "sd_control": 1.0, "n_control": 20.0,
        "scale_min": 0.0, "scale_max": 10.0,
    }
    value, variance = compute_native_row_effect(EffectMeasure.MD, inp, None, None)
    assert value == pytest.approx(-20.0, abs=0.01)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_md_unaffected_when_no_scale_range_given():
    """Regression guard: a row with no scale_min/scale_max (e.g. an
    existing kg-based body-weight group) must compute the exact same MD as
    before this feature existed -- raw units, no rescale applied."""
    from utils.effect_measures import compute_native_row_effect

    inp = {
        "mean_treatment": -1.79, "sd_treatment": 3.78, "n_treatment": 318.0,
        "mean_control": -1.03, "sd_control": 3.58, "n_control": 332.0,
    }
    value, variance = compute_native_row_effect(EffectMeasure.MD, inp, None, None)
    assert value == pytest.approx(-1.79 - (-1.03), abs=0.01)


def _vas_row(m1, m2, rng=None):
    inp = {
        "mean_treatment": m1, "sd_treatment": 1.0, "n_treatment": 30.0,
        "mean_control": m2, "sd_control": 1.0, "n_control": 30.0,
    }
    if rng:
        inp["scale_min"], inp["scale_max"] = rng
    return _es(raw_measure_inputs=inp)


def test_group_needs_scale_harmonization_only_when_all_rows_have_differing_ranges():
    from utils.effect_measures import group_needs_scale_harmonization

    assert group_needs_scale_harmonization([_vas_row(2, 4, (0, 10)), _vas_row(20, 40, (0, 100))]) is True
    # identical range everywhere: already on one scale, keep native units
    assert group_needs_scale_harmonization([_vas_row(2, 4, (1, 10)), _vas_row(3, 5, (1, 10))]) is False
    # one row without a range: all-or-nothing, so nothing is rescaled
    assert group_needs_scale_harmonization([_vas_row(2, 4, (1, 10)), _vas_row(3, 5)]) is False


def test_compute_native_row_effect_skips_rescale_when_group_says_no():
    from utils.effect_measures import compute_native_row_effect

    row = _vas_row(2.0, 4.0, (1, 10))
    on, _ = compute_native_row_effect(EffectMeasure.MD, row.raw_measure_inputs, None, None)
    off, _ = compute_native_row_effect(EffectMeasure.MD, row.raw_measure_inputs, None, None, harmonize_scale=False)
    assert on == pytest.approx(-22.22, abs=0.01)
    assert off == pytest.approx(-2.0, abs=0.01)


def test_partial_scale_ranges_never_mix_rescaled_and_raw_rows():
    """CD013445 regression: 5 rows with a stated 1-10 range plus 2 without
    one used to put 5 rows on 0-100 and 2 on raw 1-10 (pooled MD 7.33 for
    pain differences that all lie within -1.5..2.65)."""
    from agents.meta_analysis_agent import _resolve_and_populate_native

    rows = [_vas_row(4.8, 3.8, (1, 10)), _vas_row(4.1, 3.2, (1, 10)), _vas_row(5.3, 2.7, (1, 10)),
            _vas_row(4.7, 2.3), _vas_row(4.7, 3.3)]
    for i, r in enumerate(rows):
        r.study_id = f"S{i}"
    plan = _plan(target_effect_measure=EffectMeasure.MD)
    measure, scale, source, conflict, usable = _resolve_and_populate_native("g", rows, plan)
    assert scale == EffectMeasure.MD
    values = [r.native_value for r in usable]
    assert all(abs(v) < 5 for v in values), values  # raw 1-10 units, not 0-100
    assert conflict and "no 0-100 rescaling" in conflict


# ---------------------------------------------------------------------------
# Tier 2: explicit paper-reported measure
# ---------------------------------------------------------------------------

def test_paper_reported_measure_resolves_the_group():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(reported_effect_measure="risk ratio"), _es(reported_effect_measure="Risk Ratio")]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.RR
    assert resolution.source == "explicit_paper_reported"
    assert resolution.conflict is None


def test_paper_reported_measure_disagreement_is_recorded_not_silently_resolved_wrong():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="risk ratio"),
        _es(reported_effect_measure="risk ratio"),
        _es(reported_effect_measure="odds ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.RR  # majority
    assert resolution.conflict is not None
    assert "inconsistent" in resolution.conflict


# ---------------------------------------------------------------------------
# MD is scale-dependent (unlike RR/OR/HR): a single row's free-text "mean
# difference" label must not force the WHOLE group onto raw MD unless every
# row actually shares the same outcome_units (the real CD015331 bug -- one
# PANSS-total row saying "mean difference" pooled alongside BPRS-total and
# CGI-S rows on raw MD, producing a nonsensical g=1.0, CI [-1.59, 3.60]).
# ---------------------------------------------------------------------------

def test_single_row_mean_difference_report_does_not_force_md_across_mismatched_scales():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="mean difference", outcome_units="PANSS total"),
        _es(reported_effect_measure=None, outcome_units="BPRS total"),
        _es(reported_effect_measure=None, outcome_units="CGI-S"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN
    assert resolution.computation_scale == EffectMeasure.HEDGES_G
    assert resolution.conflict is not None
    assert "scale-dependent" in resolution.conflict


def test_paper_reported_mean_difference_still_resolves_when_units_actually_match():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="mean difference", outcome_units="mmHg"),
        _es(reported_effect_measure=None, outcome_units="mmHg"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.source == "explicit_paper_reported"


def test_paper_reported_ratio_measure_unaffected_by_the_md_units_guard():
    """RR/OR/HR are dimensionless -- the new units check must apply only to
    MD, never gate a ratio measure on outcome_units at all."""
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="risk ratio", outcome_units=None),
        _es(reported_effect_measure=None, outcome_units="mg/dL"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.RR
    assert resolution.conflict is None


# ---------------------------------------------------------------------------
# Tier 1: explicit user request -- wins, but disagreement is still recorded
# ---------------------------------------------------------------------------

def test_explicit_user_request_wins_over_paper_reported_but_conflict_is_recorded():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(reported_effect_measure="odds ratio")]
    plan = _plan(target_effect_measure=EffectMeasure.RR)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.RR
    assert resolution.source == "explicit_user_request"
    assert resolution.conflict is not None
    assert "user requested" in resolution.conflict


def test_explicit_user_request_alone_no_conflict_when_paper_silent():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es()]
    plan = _plan(target_effect_measure=EffectMeasure.MD)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.conflict is None


# ---------------------------------------------------------------------------
# Tier 3: methodology hint (Cochrane methodology text) -- supporting only,
# never used when tier 1/2 already resolved something.
# ---------------------------------------------------------------------------

def test_methodology_hint_used_only_when_no_explicit_signal():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es()]
    plan = _plan(methodology_effect_measure_hint=EffectMeasure.RR)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.RR
    assert resolution.source == "methodology_prior"


def test_methodology_hint_never_overrides_paper_reported_measure():
    from utils.effect_measures import resolve_group_effect_measure

    # outcome_units set (and trivially matching, single-row) so the MD scale
    # guard (see test_single_row_mean_difference_report_does_not_force_md_
    # across_mismatched_scales below) doesn't itself null the paper-reported
    # signal before this test's actual target -- the methodology-hint
    # precedence rule -- is exercised. Side effect: with units set, this
    # row's deterministic evidence also resolves to MD, so the recorded
    # conflict text comes from that vs. the methodology hint disagreeing
    # with EACH OTHER (not from a "paper vs supporting signal" mismatch) --
    # either way, the outcome that actually matters here is unchanged:
    # tier 2 (paper-reported) still wins outright, never tier 3.
    rows = [_es(reported_effect_measure="mean difference", outcome_units="mmHg")]
    plan = _plan(methodology_effect_measure_hint=EffectMeasure.RR)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.source == "explicit_paper_reported"
    assert resolution.conflict is not None  # disagreement recorded, not silent


def test_methodology_hint_and_deterministic_evidence_agree():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(outcome_units="mmHg"), _es(outcome_units="mmHg")]
    plan = _plan(methodology_effect_measure_hint=EffectMeasure.MD)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.MD
    assert resolution.source == "methodology_and_deterministic_agree"


def test_methodology_hint_and_deterministic_evidence_disagree_stays_unknown():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [_es(outcome_units="mmHg"), _es(outcome_units="mmHg")]
    plan = _plan(methodology_effect_measure_hint=EffectMeasure.RR)
    resolution = resolve_group_effect_measure(rows, plan)
    assert resolution.effect_measure == EffectMeasure.UNKNOWN
    assert resolution.source == "unresolved_fallback"
    assert "disagreement" in resolution.conflict


# ---------------------------------------------------------------------------
# compute_native_row_effect -- per-row raw-input computation (rpy2 required)
# ---------------------------------------------------------------------------

pytest.importorskip("rpy2")


def test_compute_native_row_effect_md_from_means():
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.MD,
        {"mean_treatment": 120.0, "sd_treatment": 10.0, "n_treatment": 30,
         "mean_control": 130.0, "sd_control": 12.0, "n_control": 30},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value == pytest.approx(-10.0, abs=0.01)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_rd_from_counts():
    """Real CD010592 case: Risk Difference computed directly from raw 2x2
    counts, on the LINEAR (not log) scale -- Cochrane's own alternative to
    RR/OR for rare-event/zero-cell-heavy outcomes like epistaxis."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RD,
        {"events_treatment": 16, "n_treatment": 353, "events_control": 9, "n_control": 346},
        fallback_value=0.3, fallback_variance=0.02,
    )
    # p_treatment - p_control = 16/353 - 9/346 ≈ 0.0453 - 0.0260 ≈ 0.0193
    assert value == pytest.approx(16 / 353 - 9 / 346, abs=1e-4)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_rd_single_zero_arm_still_computed():
    """A single zero-event arm (real, informative comparison) must still
    compute normally on the RD scale -- unlike a log-ratio measure, RD's
    variance formula stays well-behaved with one zero cell. metafor's own
    escalc(measure="RD") default applies its standard 0.5-per-cell
    continuity correction whenever any cell in the 2x2 table is zero (the
    same built-in behavior OR/RR already get for a single zero cell) --
    real Malm 1981 case: 1/22 treatment vs 0/22 control."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RD,
        {"events_treatment": 1, "n_treatment": 22, "events_control": 0, "n_control": 22},
        fallback_value=0.3, fallback_variance=0.02,
    )
    # metafor's default correction: a,b,c,d each +0.5 -> 1.5/23 - 0.5/23
    assert value == pytest.approx(1.5 / 23 - 0.5 / 23, abs=1e-6)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_rd_double_zero_excluded():
    """Same Cochrane convention as OR/RR: zero events in BOTH arms gives a
    degenerate RD with no real information -- excluded, not assigned a
    manufactured zero-variance point estimate."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RD,
        {"events_treatment": 0, "n_treatment": 49, "events_control": 0, "n_control": 53},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is None and variance is None


def test_rd_is_not_a_ratio_measure_pooled_on_linear_scale():
    """RD must never be back-transformed with exp() the way RR/OR/HR are --
    it's already on a linear, directly-interpretable scale."""
    from utils.effect_measures import RATIO_MEASURES
    assert EffectMeasure.RD not in RATIO_MEASURES


def test_pool_group_native_rd_uses_plain_linear_pooling_not_log_backtransform():
    """RD values feed straight into metafor's plain (non-log) pooling --
    unlike RR/OR/HR, there is no pooled_log/exp() back-transform step."""
    from utils.effect_measures import pool_group_native

    result = pool_group_native(EffectMeasure.RD, [0.02, 0.04, 0.06], [0.0004, 0.0004, 0.0004])
    assert "pooled_log" not in result
    # A simple average of small positive differences should stay a small
    # positive difference, not blow up the way exp() of these would.
    assert 0.0 < result["pooled_g"] < 0.1


def test_risk_difference_reported_resolves_to_rd_not_unknown():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="risk difference"),
        _es(reported_effect_measure="risk difference"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.RD
    assert resolution.computation_scale == EffectMeasure.RD
    assert resolution.source == "explicit_paper_reported"


def test_compute_native_row_effect_or_from_counts():
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.OR,
        {"events_treatment": 10, "n_treatment": 50, "events_control": 20, "n_control": 50},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is not None and value < 0  # log OR < 1 => negative log
    assert variance is not None and variance > 0


def test_compute_native_row_effect_double_zero_excluded_not_corrected():
    """Cochrane/RevMan convention: zero events in BOTH arms is 'Not
    estimable' for a ratio measure -- excluded from native pooling rather
    than continuity-corrected into a manufactured near-null value. Purely
    data-driven (both counts are exactly zero), generic across any study."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.OR,
        {"events_treatment": 0, "n_treatment": 32, "events_control": 0, "n_control": 31},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is None and variance is None


def test_compute_native_row_effect_single_zero_arm_still_computed():
    """Only the double-zero case is excluded -- a single zero-event arm is a
    real, informative comparison and must still compute normally."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RR,
        {"events_treatment": 3, "n_treatment": 22, "events_control": 0, "n_control": 20},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is not None and variance is not None and variance > 0


def test_compute_native_row_effect_rr_falls_back_to_reported_ratio_ci():
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RR,
        {"reported_ratio": 0.8, "reported_ratio_ci_lower": 0.6, "reported_ratio_ci_upper": 1.05},
        fallback_value=0.3, fallback_variance=0.02,
    )
    import math
    assert value == pytest.approx(math.log(0.8), abs=1e-9)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_peto_or_returns_none_not_a_guess():
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(EffectMeasure.PETO_OR, {}, fallback_value=0.3, fallback_variance=0.02)
    assert value is None and variance is None


def test_compute_native_row_effect_linear_fallback_measures_reuse_hedges_g():
    from utils.effect_measures import compute_native_row_effect

    for measure in (EffectMeasure.SMD, EffectMeasure.HEDGES_G, EffectMeasure.GENERIC):
        value, variance = compute_native_row_effect(measure, {}, fallback_value=0.42, fallback_variance=0.05)
        assert value == 0.42
        assert variance == 0.05


def test_compute_native_row_effect_md_missing_inputs_returns_none():
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(EffectMeasure.MD, {}, fallback_value=0.3, fallback_variance=0.02)
    assert value is None and variance is None


# ---------------------------------------------------------------------------
# Hazard ratio (CD008986 root-cause fix): a row explicitly reporting a
# hazard ratio must be recognized as tier-2 evidence, resolved to HR (not
# silently discarded into UNKNOWN/HEDGES_G), pooled on the log scale like
# OR/RR, and NEVER reconstructed from a 2x2 counts table.
# ---------------------------------------------------------------------------

def test_hazard_ratio_reported_resolves_to_hr_not_unknown():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="hazard ratio"),
        _es(reported_effect_measure="hazard ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.HR
    assert resolution.computation_scale == EffectMeasure.HR
    assert resolution.source == "explicit_paper_reported"


def test_hr_is_a_ratio_measure_pooled_on_log_scale():
    from utils.effect_measures import RATIO_MEASURES
    assert EffectMeasure.HR in RATIO_MEASURES


def test_compute_native_row_effect_hr_uses_reported_ratio_never_counts():
    from utils.effect_measures import compute_native_row_effect
    import math

    # Even when 2x2-style counts ARE present, HR must NOT be reconstructed
    # from them (no valid hazard-ratio-from-counts formula exists) -- only
    # the already-reported ratio+CI path applies.
    value, variance = compute_native_row_effect(
        EffectMeasure.HR,
        {
            "events_treatment": 12, "n_treatment": 50,
            "events_control": 20, "n_control": 50,
            "reported_ratio": 1.3, "reported_ratio_ci_lower": 1.0, "reported_ratio_ci_upper": 1.6,
        },
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value == pytest.approx(math.log(1.3), abs=1e-9)
    assert variance is not None and variance > 0


def test_compute_native_row_effect_hr_without_reported_ratio_returns_none():
    from utils.effect_measures import compute_native_row_effect

    # Counts alone (no reported HR+CI) must never silently produce a value.
    value, variance = compute_native_row_effect(
        EffectMeasure.HR,
        {"events_treatment": 12, "n_treatment": 50, "events_control": 20, "n_control": 50},
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is None and variance is None


def test_compute_native_row_effect_hr_tagged_ratio_does_not_satisfy_rr_target():
    """Real CD011197 bug: a row whose only reported ratio is a hazard ratio
    (e.g. Elliott 2023's AF-recurrence HR=0.50) must NOT be silently pooled
    as if it were a risk ratio just because a run explicitly requests RR
    pooling -- RR/OR/HR are never interchangeable even though all three live
    on the same log scale. Tagged data (reported_ratio_measure) must be
    checked; a row explicitly marked HR is excluded from an RR/OR pool."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.RR,
        {
            "reported_ratio": 0.5, "reported_ratio_ci_lower": 0.33, "reported_ratio_ci_upper": 0.78,
            "reported_ratio_measure": "HR",
        },
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is None and variance is None


def test_compute_native_row_effect_rr_tagged_ratio_does_not_satisfy_hr_target():
    """Symmetric case: a row's own reported RR must not impersonate an HR
    either, when a group resolves to native HR pooling."""
    from utils.effect_measures import compute_native_row_effect

    value, variance = compute_native_row_effect(
        EffectMeasure.HR,
        {
            "reported_ratio": 0.8, "reported_ratio_ci_lower": 0.6, "reported_ratio_ci_upper": 1.05,
            "reported_ratio_measure": "RR",
        },
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value is None and variance is None


def test_compute_native_row_effect_tagged_ratio_matching_target_still_works():
    """The tag doesn't break the normal, matching case -- an RR-tagged row
    still satisfies an RR-scale request."""
    from utils.effect_measures import compute_native_row_effect
    import math

    value, variance = compute_native_row_effect(
        EffectMeasure.RR,
        {
            "reported_ratio": 0.8, "reported_ratio_ci_lower": 0.6, "reported_ratio_ci_upper": 1.05,
            "reported_ratio_measure": "RR",
        },
        fallback_value=0.3, fallback_variance=0.02,
    )
    assert value == pytest.approx(math.log(0.8), abs=1e-9)
    assert variance is not None and variance > 0


def test_hr_and_or_reports_in_same_group_produce_a_conflict_note():
    # Majority vote picks one measure, but disagreement is always recorded,
    # never silently dropped (the per-row partition that actually SPLITS
    # these into separate pooling groups lives in
    # agents/meta_analysis_agent.py::_partition_by_row_measure -- this test
    # only covers resolve_group_effect_measure()'s own conflict recording).
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="hazard ratio"),
        _es(reported_effect_measure="hazard ratio"),
        _es(reported_effect_measure="odds ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.HR  # majority
    assert resolution.conflict is not None


# ---------------------------------------------------------------------------
# Preference hierarchy (TIE-BREAKER ONLY, never an absolute override) --
# Cochrane's own dichotomous-measure convention (RR > OR > Peto OR) decides
# ties, but a real majority always wins regardless of preference. Root cause:
# a CD008986 re-run raised the question "wouldn't it be a problem that
# AutoSynthesis pooled on HR while Cochrane used RR" -- the answer implemented
# here is that the CHOICE between fundamentally different data types (e.g.
# HR vs RR, which reflect different underlying data -- time-to-event vs
# dichotomous) must stay evidence-driven (majority), while a genuine tie
# between measures that DO compete for the same dichotomous data (RR vs OR)
# should follow Cochrane's own stated preference rather than arbitrary
# tie-breaking.
# ---------------------------------------------------------------------------

def test_rr_or_tie_breaks_toward_rr_by_cochrane_convention():
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="odds ratio"),
        _es(reported_effect_measure="risk ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.RR


def test_or_still_wins_with_a_real_majority_despite_rr_preference():
    # The preference is a TIE-BREAKER, never an absolute override -- 2 real
    # votes for OR must beat 1 vote for RR, even though RR is preferred on
    # a tie.
    from utils.effect_measures import resolve_group_effect_measure

    rows = [
        _es(reported_effect_measure="odds ratio"),
        _es(reported_effect_measure="odds ratio"),
        _es(reported_effect_measure="risk ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    assert resolution.effect_measure == EffectMeasure.OR


def test_hr_vs_rr_tie_is_not_forced_toward_rr():
    # HR isn't a "compatible alternative" to RR (different underlying data
    # type -- time-to-event vs dichotomous), so a genuine HR-vs-RR tie must
    # NOT be pushed toward RR just because RR is preferred among real
    # dichotomous alternatives. Regression test for a real bug caught before
    # shipping: ranking HR as "always less preferred than RR" would silently
    # turn this into an absolute RR-over-HR rule, which is exactly what this
    # mechanism must avoid (see resolve_group_effect_measure's module
    # docstring and utils.effect_measures.dichotomous_tie_break()).
    from utils.effect_measures import resolve_group_effect_measure, dichotomous_tie_break

    rows = [
        _es(reported_effect_measure="hazard ratio"),
        _es(reported_effect_measure="risk ratio"),
    ]
    resolution = resolve_group_effect_measure(rows, plan=None)
    # Must NOT unconditionally resolve to RR -- either measure winning the
    # tie is acceptable (it's genuinely unresolved), but it must be the
    # SAME choice most_common() would make without any preference logic --
    # i.e. driven by encounter order, not artificially forced toward RR.
    assert resolution.effect_measure == EffectMeasure.HR

    # Direct unit check on the tie-break helper itself: an HR-vs-RR tie is
    # returned UNCHANGED (not sorted/reordered), because HR has no rank in
    # the dichotomous preference family at all.
    assert dichotomous_tie_break([EffectMeasure.HR, EffectMeasure.RR]) == [EffectMeasure.HR, EffectMeasure.RR]
    assert dichotomous_tie_break([EffectMeasure.RR, EffectMeasure.HR]) == [EffectMeasure.RR, EffectMeasure.HR]


def test_dichotomous_tie_break_orders_rr_or_peto_when_all_three_present():
    from utils.effect_measures import dichotomous_tie_break

    assert dichotomous_tie_break([EffectMeasure.PETO_OR, EffectMeasure.OR, EffectMeasure.RR]) == [
        EffectMeasure.RR, EffectMeasure.OR, EffectMeasure.PETO_OR,
    ]


class TestDetermineFavorsTreatment:
    """determine_favors_treatment() is the ONLY place plan.higher_score_is_worse is allowed
    to affect anything -- it answers "which side does this favor" as a field separate from
    the effect value, which always keeps its raw (treatment - control)/SD sign (matching
    Cochrane/RevMan). See models.EffectSizeRecord.favors_treatment's docstring."""

    def test_higher_is_better_positive_favors_treatment(self):
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(0.5, higher_score_is_worse=False) is True

    def test_higher_is_better_negative_favors_control(self):
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(-0.5, higher_score_is_worse=False) is False

    def test_higher_is_worse_negative_favors_treatment(self):
        """The ECBI case: treatment scored lower (raw value negative), and lower is better."""
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(-0.5, higher_score_is_worse=True) is True

    def test_higher_is_worse_positive_favors_control(self):
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(0.5, higher_score_is_worse=True) is False

    def test_exact_tie_is_none_not_false(self):
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(0.0, higher_score_is_worse=False) is None
        assert determine_favors_treatment(0.0, higher_score_is_worse=True) is None

    def test_missing_value_is_none(self):
        from utils.effect_measures import determine_favors_treatment
        assert determine_favors_treatment(None, higher_score_is_worse=False) is None
