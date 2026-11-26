"""
Native effect-measure resolution and per-row/per-group computation for the
production pipeline's outcome-group-based pooling
(agents/meta_analysis_agent.py).

This module is intentionally production-only: it imports nothing from
cochrane_benchmark, and resolve_group_effect_measure()'s signature has no
parameter that could accept a GroundTruth/GroundTruthOutcome object -- only
plain EffectSizeRecord rows and a MetaAnalysisPlan. Cochrane's actual
pooled-effect measure is evaluation-only and must never influence which
measure AutoSynthesis pools on; see
tests/test_cochrane_benchmark_leakage_prevention.py, which extends its
AST-based import-boundary scan to this file.

Resolution hierarchy (per outcome group), per explicit instruction:
  1. Explicit user request (plan.target_effect_measure) -- a deliberate,
     informed override. When it disagrees with what the paper(s) in the
     group report (tier 2), the user's request still wins, but the
     disagreement is recorded in effect_measure_conflict, never silently
     dropped.
  2. Explicit measure reported by the paper itself (each row's own
     reported_effect_measure text -- never inferred from event counts or
     from a shared outcome_measurement label alone).
  3. Supporting signals, used ONLY when neither 1 nor 2 resolved anything:
     the Cochrane review's own stated methodology (plan.
     methodology_effect_measure_hint -- methodology text, never
     GroundTruth) and strong deterministic evidence from the extracted
     statistics (currently: identical, non-empty outcome_units across every
     row in the group -- same measurement TEXT alone is not sufficient).
     If both fire and disagree with each other, the group is left UNKNOWN
     rather than guessing between them.
  4. UNKNOWN otherwise.

UNKNOWN is a normal, expected outcome, not a failure: every group still
gets pooled (computation_scale falls back to HEDGES_G, exactly the
pipeline's pre-existing behaviour), but effect_measure_source/
effect_measure_conflict record that the label is not confirmed, so
reporting can say so honestly instead of asserting a specific native
measure with false confidence.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from models import EffectMeasure, EffectSizeRecord, MetaAnalysisPlan
from statistics import metafor_engine
from utils.effect_measure_text import normalize_effect_measure_text

RATIO_MEASURES = {EffectMeasure.OR, EffectMeasure.RR, EffectMeasure.PETO_OR, EffectMeasure.HR}
LINEAR_FALLBACK_MEASURES = {EffectMeasure.SMD, EffectMeasure.HEDGES_G, EffectMeasure.GENERIC}

# Common target range every row's own stated instrument range (raw_measure_
# inputs["scale_min"]/["scale_max"], see rows_have_harmonizable_scale_range)
# gets linearly rescaled onto before native MD pooling -- 0-100 specifically
# because that is the Cochrane Handbook's own stated convention for
# harmonizing continuous outcomes measured on different bounded instruments
# (confirmed verbatim in CD014428's Methods: "we expressed these on a
# common 0 to 100 scale as a mean difference"), not a value picked for any
# one review or outcome -- a 0-10 NRS and a 100mm VAS are both linearly
# rescaled to this same range regardless of which construct they measure.
HARMONIZED_SCALE_MAX = 100.0

# Cochrane Handbook's own default preference for DICHOTOMOUS (binary-event)
# outcomes: RR is the conventional/most-interpretable default, OR the usual
# alternative, Peto OR reserved for rare-event/sparse-data special cases.
# HR is deliberately NOT in this list -- it isn't a "compatible alternative"
# to RR/OR for the SAME underlying data the way OR is; it requires genuinely
# different (time-to-event/survival) data (see compute_native_row_effect's
# comment: HR has no counts-reconstruction path at all). Choosing between
# "this outcome's data is fundamentally dichotomous vs. fundamentally
# time-to-event" is a DATA-DRIVEN decision (which family has more/better-
# supported evidence -- see _partition_by_row_measure in
# agents/meta_analysis_agent.py), never a stylistic preference between RR
# and HR. This list is ONLY a tie-breaker among measures that genuinely
# compete for the SAME dichotomous data -- see dichotomous_preference_rank().
DICHOTOMOUS_PREFERENCE_ORDER = [EffectMeasure.RR, EffectMeasure.OR, EffectMeasure.PETO_OR]


def dichotomous_preference_rank(measure: EffectMeasure) -> Optional[int]:
    """Lower = more preferred. Returns None for a measure OUTSIDE
    DICHOTOMOUS_PREFERENCE_ORDER (e.g. HR, MD, SMD) -- callers MUST apply
    this tie-break only when EVERY tied candidate has a non-None rank (see
    dichotomous_tie_break() below). Ranking an unranked measure as "always
    less preferred" would silently turn a genuine HR-vs-RR tie into an
    absolute RR-over-HR rule -- exactly what this mechanism must NOT do,
    since HR reflects a fundamentally different, not-a-real-alternative data
    type (time-to-event), not a stylistic choice."""
    try:
        return DICHOTOMOUS_PREFERENCE_ORDER.index(measure)
    except ValueError:
        return None


def dichotomous_tie_break(leaders: List[EffectMeasure]) -> List[EffectMeasure]:
    """Sort `leaders` (measures tied for the most support) by Cochrane's
    dichotomous preference IFF every one of them is a genuine dichotomous
    alternative (RR/OR/Peto OR) -- otherwise returns `leaders` unchanged
    (e.g. an HR-vs-RR tie is left as a real, unresolved tie; the preference
    only applies when ALL tied candidates actually compete for the same
    kind of data)."""
    if all(dichotomous_preference_rank(m) is not None for m in leaders):
        return sorted(leaders, key=dichotomous_preference_rank)
    return leaders


@dataclass
class EffectMeasureResolution:
    effect_measure: EffectMeasure
    computation_scale: EffectMeasure
    source: str
    conflict: Optional[str] = None


def _consensus_paper_reported_measure(rows: List[EffectSizeRecord]) -> Tuple[Optional[EffectMeasure], bool]:
    """Tier 2. Only rows with an explicit reported_effect_measure count --
    never inferred from odds_ratio/M_diff presence alone (a paper's own
    stated measure name is the deliberately higher bar). Returns
    (majority_measure_or_None, had_disagreement)."""
    found = []
    for r in rows:
        text = getattr(r, "reported_effect_measure", None)
        if not text:
            continue
        m = normalize_effect_measure_text(text)
        if m != EffectMeasure.UNKNOWN:
            found.append(m)
    if not found:
        return None, False
    counts = Counter(found)
    if len(counts) == 1:
        return found[0], False
    # A genuine tie in how many rows report each measure -- break it with
    # Cochrane's own dichotomous-measure preference (RR > OR > Peto OR)
    # when every tied measure is a real dichotomous alternative (see
    # dichotomous_tie_break()); a tie involving HR (or any other measure
    # outside that family) is left as an unresolved tie rather than forced
    # toward RR, since that comparison isn't a stylistic choice at all.
    # This is a TIE-BREAKER ONLY: whenever one measure has strictly more
    # support than another, that majority still wins regardless of
    # preference -- never an absolute override.
    max_count = max(counts.values())
    leaders = dichotomous_tie_break([m for m, c in counts.items() if c == max_count])
    return leaders[0], True


def rows_have_harmonizable_scale_range(rows: List[EffectSizeRecord]) -> bool:
    """True iff EVERY row in the group has an explicit, valid instrument
    range (raw_measure_inputs["scale_min"]/["scale_max"], filled only when
    the paper itself states the instrument's numeric bounds -- see
    agents/statistical_result_extractor_agent.py rule 22). This is
    DELIBERATELY not keyed on outcome name/family text (e.g. "pain",
    "VAS") -- any continuous outcome where every contributing paper stated
    its own instrument's fixed range qualifies, generalizing to whatever
    construct the review is pooling rather than a hardcoded vocabulary of
    "pain scale" names. A single row missing the range (or one row's range
    being degenerate, min>=max) is enough to return False -- exactly like
    _deterministic_evidence's existing outcome_units check, an incomplete
    signal must never partially upgrade a group."""
    for r in rows:
        inp = getattr(r, "raw_measure_inputs", None) or {}
        lo, hi = inp.get("scale_min"), inp.get("scale_max")
        if lo is None or hi is None or not (hi > lo):
            return False
    return True


def group_needs_scale_harmonization(rows: List[EffectSizeRecord]) -> bool:
    """True iff native MD pooling for this group should rescale each row onto
    the common 0-100 range. Group-level (all-or-nothing) on purpose: the
    rescale is a per-row linear transform, so applying it to only SOME rows
    puts part of the group on 0-100 and the rest on raw units, and the pooled
    MD is then meaningless (real case, CD013445: five 1-10 VAS rows rescaled,
    two rows without a stated range left raw -> MD 7.33 where every study's
    own difference lay between -1.5 and +2.65).

    Requires BOTH (a) every row states a valid instrument range, and (b) the
    stated ranges are not all identical. When every row shares one range
    there is nothing to reconcile -- the group is already on a common scale,
    and rescaling would only move the result off the papers' native units
    (and off a Cochrane analysis pooled on them)."""
    if not rows_have_harmonizable_scale_range(rows):
        return False
    ranges = {
        (r.raw_measure_inputs["scale_min"], r.raw_measure_inputs["scale_max"])
        for r in rows
    }
    return len(ranges) > 1


def _deterministic_evidence(rows: List[EffectSizeRecord]) -> Optional[EffectMeasure]:
    """Tier 3's deterministic component. Narrowed per explicit instruction:
    matching outcome_measurement TEXT alone is not evidence of a shared
    interpretable scale -- two papers can use the same label for different
    instruments. Requires either (a) every row in the group to carry the
    SAME non-empty outcome_units value (e.g. "mmHg", "days"), or (b) every
    row to have an explicit instrument range that can be rescaled onto a
    common footing (see rows_have_harmonizable_scale_range) -- before
    upgrading to MD; otherwise returns None (leave to SMD/UNKNOWN). Case
    (b) is what lets a 0-10 NRS and a 100mm VAS pool together as MD on a
    common rescaled range, mirroring Cochrane's own stated convention for
    pain/function outcomes (Cochrane Handbook; confirmed verbatim in
    CD014428's own Methods: "we expressed these on a common 0 to 100 scale
    as a mean difference") -- generalized here to any bounded instrument,
    not hardcoded to pain. No RR-vs-OR branch: both are computable from the
    same 2x2 counts, so counts alone can never reveal which the review
    intended -- see module docstring."""
    units = {getattr(r, "outcome_units", None) for r in rows}
    if len(units) == 1 and next(iter(units)):
        return EffectMeasure.MD
    if rows_have_harmonizable_scale_range(rows):
        return EffectMeasure.MD
    return None


def _supporting_signal(
    rows: List[EffectSizeRecord], methodology_hint: Optional[EffectMeasure]
) -> Tuple[Optional[EffectMeasure], Optional[str]]:
    """Tier 3. Returns (measure_or_None, conflict_note_or_None). When both
    the methodology hint and deterministic evidence fire and disagree,
    returns (None, note) -- the caller must not pick one over the other."""
    deterministic = _deterministic_evidence(rows)
    if methodology_hint is not None and deterministic is not None:
        if methodology_hint != deterministic:
            return None, (
                f"Cochrane methodology statement suggests {methodology_hint.value}; deterministic evidence "
                f"from extracted statistics suggests {deterministic.value} -- disagreement, left unresolved"
            )
        return deterministic, None
    return (methodology_hint or deterministic), None


def _finalize(measure: EffectMeasure, source: str, conflict_notes: List[str]) -> EffectMeasureResolution:
    computation_scale = measure if measure != EffectMeasure.UNKNOWN else EffectMeasure.HEDGES_G
    return EffectMeasureResolution(
        effect_measure=measure,
        computation_scale=computation_scale,
        source=source,
        conflict="; ".join(conflict_notes) if conflict_notes else None,
    )


def resolve_group_effect_measure(
    rows: List[EffectSizeRecord],
    plan: Optional[MetaAnalysisPlan] = None,
) -> EffectMeasureResolution:
    """Resolve ONE outcome group's effect measure. See module docstring for
    the full hierarchy. `rows` should be every EffectSizeRecord already
    grouped under one outcome_group_key (agents/meta_analysis_agent.py does
    the grouping); this function does not group anything itself."""
    target = plan.target_effect_measure if plan else None
    methodology_hint = plan.methodology_effect_measure_hint if plan else None

    paper_reported, paper_conflict = _consensus_paper_reported_measure(rows)
    conflict_notes: List[str] = []
    if paper_conflict:
        conflict_notes.append(
            f"rows in this group report inconsistent effect measures "
            f"(majority taken: {paper_reported.value if paper_reported else '?'})"
        )

    # MD is NOT scale-invariant the way RR/OR/HR/PETO_OR are: a ratio means
    # the same thing regardless of each study's particular instrument, but a
    # raw mean difference does not -- pooling "mean difference" across, say,
    # PANSS total (range ~30-210) and BPRS total (range ~18-126) is not a
    # different-population nuance, it's arithmetically meaningless. Tier 2
    # otherwise only requires ONE row in the group to carry the free-text
    # label "mean difference" (a paper describing its OWN within-study
    # result, saying nothing about the other rows' instruments) to force the
    # WHOLE group onto raw MD. Require the same same-outcome_units evidence
    # tier 3 already demands before trusting an MD signal here too, so a
    # single row's label can never drag scale-incompatible rows into a raw
    # MD pool. (The real CD015331 bug: one row saying "mean difference"
    # forced 9 other rows spanning 3 different instruments -- PANSS, BPRS,
    # CGI-S -- onto MD, producing a nonsensical g=1.0, CI [-1.59, 3.60].)
    if paper_reported == EffectMeasure.MD and _deterministic_evidence(rows) is None:
        conflict_notes.append(
            "paper(s) explicitly report mean difference, but rows in this group do not share a "
            "common outcome_units value -- MD is scale-dependent (unlike RR/OR/HR), so this "
            "signal is not trusted alone; falling through to standardized-effect pooling"
        )
        paper_reported = None

    if target is not None:
        if paper_reported is not None and paper_reported != target:
            conflict_notes.append(
                f"user requested {target.value}, but the paper(s) explicitly report {paper_reported.value} "
                "-- user request kept as authoritative"
            )
        return _finalize(target, "explicit_user_request", conflict_notes)

    if paper_reported is not None:
        supporting, supporting_conflict = _supporting_signal(rows, methodology_hint)
        if supporting_conflict:
            conflict_notes.append(supporting_conflict)
        elif supporting is not None and supporting != paper_reported:
            conflict_notes.append(
                f"paper reports {paper_reported.value}; supporting signal suggests {supporting.value} "
                "-- paper-reported measure kept authoritative"
            )
        return _finalize(paper_reported, "explicit_paper_reported", conflict_notes)

    supporting, supporting_conflict = _supporting_signal(rows, methodology_hint)
    if supporting_conflict:
        conflict_notes.append(supporting_conflict)
        return _finalize(EffectMeasure.UNKNOWN, "unresolved_fallback", conflict_notes)
    if supporting is not None:
        if methodology_hint is not None and _deterministic_evidence(rows) is not None:
            source = "methodology_and_deterministic_agree"
        elif methodology_hint is not None:
            source = "methodology_prior"
        else:
            source = "deterministic_evidence"
        return _finalize(supporting, source, conflict_notes)

    return _finalize(EffectMeasure.UNKNOWN, "unresolved_fallback", conflict_notes)


def compute_native_row_effect(
    computation_scale: EffectMeasure,
    raw_measure_inputs: Dict[str, Union[float, str]],
    fallback_value: Optional[float],
    fallback_variance: Optional[float],
    harmonize_scale: bool = True,
) -> Tuple[Optional[float], Optional[float]]:
    """Per-row point estimate + variance on computation_scale, reusing
    metafor_engine's escalc_*() functions. Falls back to the row's existing
    hedges_g/variance (already computed by utils/paper_results_converter.py)
    for SMD/HEDGES_G/GENERIC or whenever the measure-specific raw inputs
    aren't available for THIS row -- this is what keeps every existing
    single-measure run's numbers unchanged. Returns (None, None) when
    computation_scale is a ratio/MD measure but this row has no usable raw
    inputs for it -- callers must exclude such rows from that group's
    native pooling rather than silently mixing scales."""
    inp = raw_measure_inputs or {}

    if computation_scale in LINEAR_FALLBACK_MEASURES:
        return fallback_value, fallback_variance

    if computation_scale == EffectMeasure.MD:
        m1, sd1, n1 = inp.get("mean_treatment"), inp.get("sd_treatment"), inp.get("n_treatment")
        m2, sd2, n2 = inp.get("mean_control"), inp.get("sd_control"), inp.get("n_control")
        if None not in (m1, sd1, n1, m2, sd2, n2):
            # Rescale onto the common harmonized range when THIS row states
            # its own instrument's bounds -- a pure per-row linear
            # transform, independent of what any other row in the group
            # does. A row with no scale_min/scale_max is pooled exactly as
            # before (raw units unchanged): this only activates when the
            # extractor explicitly recorded a range, never inferred, so a
            # kg-based body-weight group (no natural fixed range) behaves
            # identically to before this feature existed.
            # harmonize_scale is the GROUP-level decision (see
            # group_needs_scale_harmonization): callers pass False when the
            # rest of the group can't be rescaled too, so no group ever mixes
            # rescaled and raw rows.
            scale_min, scale_max = inp.get("scale_min"), inp.get("scale_max")
            if harmonize_scale and scale_min is not None and scale_max is not None and scale_max > scale_min:
                span = scale_max - scale_min
                factor = HARMONIZED_SCALE_MAX / span
                m1 = (m1 - scale_min) * factor
                sd1 = sd1 * factor
                m2 = (m2 - scale_min) * factor
                sd2 = sd2 * factor
            result = metafor_engine.escalc_md_from_means(m1, sd1, n1, m2, sd2, n2)
            if result is not None:
                return result["md"], result["vi"]
        import config as _cfg
        if getattr(_cfg, "DIFF_FALLBACK", False):
            md, se = inp.get("mean_diff"), inp.get("se_diff")
            if md is not None and se is not None and se > 0 and inp.get("scale_min") is None:
                return float(md), float(se) ** 2
        return None, None

    if computation_scale == EffectMeasure.RD:
        # Risk Difference: LINEAR scale (p_treatment - p_control), computed
        # directly from the same raw 2x2 counts as OR/RR below -- never
        # log-transformed, since a difference of proportions can legitimately
        # be zero or negative. Cochrane's standard alternative to RR/OR for
        # rare-event/zero-cell-heavy outcomes (confirmed live in CD010592's
        # own "Risk Difference M-H, Fixed, 95% CI" epistaxis analysis) --
        # generic across any review, keyed purely on computation_scale.
        e1, n1 = inp.get("events_treatment"), inp.get("n_treatment")
        e2, n2 = inp.get("events_control"), inp.get("n_control")
        # Same double-zero exclusion as OR/RR below: zero events in BOTH
        # arms gives a degenerate (zero) RD variance, carrying no real
        # information about the relative treatment effect -- Cochrane
        # convention excludes it rather than assign it artificial weight.
        is_double_zero = e1 == 0 and e2 == 0
        if (
            not is_double_zero and None not in (e1, n1, e2, n2)
            and n1 is not None and n2 is not None and n1 > e1 >= 0 and n2 > e2 >= 0
        ):
            a, b, c, d = e1, n1 - e1, e2, n2 - e2
            result = metafor_engine.escalc_rd_from_counts(a, b, c, d)
            if result is not None:
                return result["rd"], result["vi"]
        return None, None

    if computation_scale in (EffectMeasure.OR, EffectMeasure.RR, EffectMeasure.HR):
        # HR has NO counts-reconstruction path -- a hazard ratio cannot be
        # recovered from a simple 2x2 event/total table (it needs the
        # underlying time-to-event data, or at minimum O-E/V logrank
        # statistics this extraction schema doesn't capture). Skip straight
        # to the already-reported-ratio fallback below for HR.
        if computation_scale != EffectMeasure.HR:
            e1, n1 = inp.get("events_treatment"), inp.get("n_treatment")
            e2, n2 = inp.get("events_control"), inp.get("n_control")
            # Double-zero-event rows (zero events in BOTH arms) are excluded
            # from native RR/OR pooling entirely -- same Cochrane-convention
            # rule as utils/paper_results_converter.py's Priority 0d, purely
            # data-driven (e1 == e2 == 0), never study/review-specific.
            is_double_zero = e1 == 0 and e2 == 0
            if (
                not is_double_zero and None not in (e1, n1, e2, n2)
                and n1 is not None and n2 is not None and n1 > e1 >= 0 and n2 > e2 >= 0
            ):
                a, b, c, d = e1, n1 - e1, e2, n2 - e2
                fn = metafor_engine.escalc_or_from_counts if computation_scale == EffectMeasure.OR else metafor_engine.escalc_rr_from_counts
                result = fn(a, b, c, d)
                if result is not None:
                    key = "log_or" if computation_scale == EffectMeasure.OR else "log_rr"
                    return result[key], result["vi"]
        # Fall back to an already-reported ratio + CI (generic inverse
        # variance on the log scale -- same convention metafor's escalc uses).
        # For HR, this is the ONLY path -- see comment above.
        # RR/OR/HR are never interchangeable (see agents/effect_size_agent.py's
        # reported_ratio_measure tagging) -- only accept this fallback when the
        # row's OWN reported ratio type actually matches the scale being
        # computed here. A row whose only reported ratio is an HR must not
        # silently satisfy a group resolved to RR (or vice versa) just because
        # both live on the same log scale -- that was the real CD011197 bug
        # (Elliott 2023's hazard ratio pooled as if it were a risk ratio).
        ratio = inp.get("reported_ratio")
        ratio_measure = inp.get("reported_ratio_measure")
        if ratio_measure is not None and ratio_measure != computation_scale.value:
            ratio = None
        lo, hi = inp.get("reported_ratio_ci_lower"), inp.get("reported_ratio_ci_upper")
        if ratio and ratio > 0 and lo and hi and lo > 0 and hi > 0:
            log_ratio = math.log(ratio)
            se = (math.log(hi) - math.log(lo)) / (2 * 1.96)
            if se > 0:
                return log_ratio, se ** 2
        return None, None

    # PETO_OR: no counts-based conversion is wired here -- Peto's method
    # needs (O-E, V) statistics this extraction schema doesn't capture.
    # No native value rather than silently approximating with plain OR.
    return None, None


def pool_group_native(computation_scale: EffectMeasure, values: List[float], variances: List[float],
                      method: str = "REML") -> dict:
    """Random-effects pooling on computation_scale, reusing metafor_engine
    directly: log-scale pooling + back-transform for ratio measures
    (matching how Cochrane/RevMan itself reports pooled ORs/RRs), plain
    linear pooling otherwise. `pooled_g`/`ci_lower`/`ci_upper` in the
    returned dict are always on the HUMAN-INTERPRETABLE scale (back-
    transformed for ratios); heterogeneity should still be computed from
    the log-scale `values`/`variances` passed in here, same as metafor
    itself does internally.

    For ratio measures, `pooled_log`/`ci_lower_log`/`ci_upper_log` are also
    included -- the pre-back-transform values metafor_engine.pool_log_measure()
    already computes internally (no new math, just not discarded). Consumed
    by statistics/plots.py's forest_plot/cumulative_forest_plot/etc, which
    receive per-study values on the SAME (log) scale as `values` above and
    need the pooled reference line in matching units before their own
    display-time exp() transform -- see agents/meta_analysis_agent.py's
    `_generate_plots()`."""
    if computation_scale in RATIO_MEASURES:
        raw = metafor_engine.pool_log_measure(values, variances, method=method)
        return {
            **raw,
            "pooled_g": raw["pooled_ratio"],
            "ci_lower": raw["ci_lower_ratio"],
            "ci_upper": raw["ci_upper_ratio"],
            "pooled_log": raw["pooled_g"],
            "ci_lower_log": raw["ci_lower"],
            "ci_upper_log": raw["ci_upper"],
        }
    return metafor_engine.pool(values, variances, method=method)


# ---------------------------------------------------------------------------
# Human-readable labeling -- ONE shared source of truth so
# agents/report_agent.py, dashboard.py, and agents/meta_analysis_agent.py's
# own plot calls never disagree about what to call a given measure/scale.
# ---------------------------------------------------------------------------

MEASURE_LABELS = {
    EffectMeasure.RR: "Risk Ratio (RR)",
    EffectMeasure.OR: "Odds Ratio (OR)",
    EffectMeasure.HR: "Hazard Ratio (HR)",
    EffectMeasure.PETO_OR: "Peto Odds Ratio",
    EffectMeasure.MD: "Mean Difference (MD)",
    EffectMeasure.RD: "Risk Difference (RD)",
    EffectMeasure.SMD: "Standardized Mean Difference (SMD)",
    EffectMeasure.HEDGES_G: "Hedges' g",
    EffectMeasure.GENERIC: "Generic estimate (already-computed)",
    EffectMeasure.UNKNOWN: "Not confirmed",
}


def measure_label(measure: EffectMeasure) -> str:
    return MEASURE_LABELS.get(measure, str(getattr(measure, "value", measure)))


def determine_favors_treatment(effect_value: Optional[float], higher_score_is_worse: bool) -> Optional[bool]:
    """Whether a (raw-sign, never flipped) effect value favors treatment or control.

    hedges_g/cohens_d/pooled_g always keep the raw (treatment - control)/SD sign -- the
    same convention Cochrane/RevMan itself uses, so a number here is directly comparable to
    a published forest plot cell. plan.higher_score_is_worse is consulted ONLY here, to
    answer "which side is favourable" as a separate field, never to alter the number itself:
      - higher_score_is_worse=False (default, higher=better): positive favors treatment.
      - higher_score_is_worse=True (e.g. a symptom-severity scale): negative favors
        treatment, since a LOWER raw score is the better outcome there.
    Returns None for a missing value or an exact tie (effect_value == 0) -- a tie favors
    neither side, and is not the same as "unknown"."""
    if effect_value is None:
        return None
    if effect_value == 0:
        return None
    return (effect_value < 0) if higher_score_is_worse else (effect_value > 0)


def native_pooling_used(effect_measure: EffectMeasure, computation_scale: EffectMeasure) -> bool:
    """True iff a group was pooled on its own resolved measure, not the
    Hedges' g/SMD fallback. For SMD/HEDGES_G/GENERIC groups this is True
    even though the numbers are computed identically to the fallback (by
    design, see compute_native_row_effect) -- the resolution was still
    genuinely confirmed, just on a scale that happens to coincide with it."""
    return effect_measure == computation_scale and effect_measure != EffectMeasure.UNKNOWN
