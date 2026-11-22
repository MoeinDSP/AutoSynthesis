"""
Convert general statistical extraction output into meta-analysis-ready records.

Core 53 columns match GT.xlsx exactly; one additional column is prepended:
  study_label — which independent study within the paper (Study 1, Study 2, …)
Total: 54 columns.
"""

import csv
import json
import math
import os
from typing import Any, Dict, List, Tuple

from statistics import metafor_engine
from models import EffectMeasure
from utils.effect_measure_text import normalize_effect_measure_text
from utils.wan2014 import estimate_mean_sd_from_median_iqr, estimate_mean_sd_from_median_range

# Ratio measures a paper can explicitly report as its own effect measure --
# used to (a) recognize a directly-reported RR/HR the same way an odds_ratio
# is already recognized below, and (b) guard against silently deriving a
# DIFFERENT measure (e.g. from raw proportions) for a row that names one of
# these but provides no numeric value -- see the exclusion guard in
# _convert_row() below.
_NAMED_RATIO_MEASURES = {EffectMeasure.OR, EffectMeasure.RR, EffectMeasure.HR, EffectMeasure.PETO_OR}

# 53 GT.xlsx columns + 1 study-structure column = 54 total
GT_COLUMNS = [
    "Study_ID",
    "study_label",   # which independent study within the paper
    "Report_ID",
    "Title",
    "Author",
    "Publication Year",
    "Comment",
    "Design Type",
    "Include/Exclude",
    "Publication Status",
    "domain",
    "Study Environment",
    "Country",
    "Study Year",
    "llm_model",
    "Medium",
    "Content length",
    "Topic of Content",
    "interaction_type",
    "Comparison type",
    "Participant type",
    "Recruitment source",
    "Outcome type",
    "Outcome measurement",
    "Outcome variable",
    "n_total",
    "n_treatment",
    "M_treatment",
    "M_treatment_emm",
    "M_treatment_perc",
    "CI_Level",
    "CI_lower_treatment",
    "CI_upper_treatment",
    "SE_treatment",
    "SD_treatment",
    "n_control",
    "M_control",
    "M_control_emm",
    "M_control_perc",
    "CI_lower_control",
    "CI_upper_control",
    "t_value",
    "df",
    "SE_control",
    "SD_control",
    "F_value",
    "odds_ratio",
    "CI_lower_or",
    "CI_upper_or",
    "P_value",
    "cohens_d",
    "hedges_g",
    "M_diff",
    "SE_diff",
    "statistic_type",
    "additional_group_ns",  # multi-group (k>2): all per-condition Ns as "Label=n, ..."
]


def _safe_float(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def _safe_int(x):
    if x is None or x == "":
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


def _v(x):
    """Return x if not None/empty, else empty string."""
    if x is None:
        return ""
    return x


def _sd_from_ci(ci_lower, ci_upper, n, ci_level=None):
    """Derive a group's SD from its reported mean's confidence interval and
    sample size -- Cochrane Handbook 6.5.2.3 ("Obtaining standard deviations
    from standard errors, confidence intervals... for group means"):
        SE = (upper - lower) / (2*z)     SD = SE * sqrt(n)
    z is the normal quantile for whatever confidence level was actually
    reported (95% is by far the most common in practice, but this respects
    an explicit ci_level field when the paper states a different one, e.g.
    90% or 99%) -- not a statistical approximation the way Wan 2014's
    median/IQR estimate is; this is an exact algebraic inverse of the
    standard mean +/- z*SE construction a normal-theory CI already is.
    Returns None on any invalid/degenerate input rather than guessing."""
    if ci_lower is None or ci_upper is None or n is None or n < 2:
        return None
    width = ci_upper - ci_lower
    if width <= 0:
        return None
    from scipy.stats import norm
    level = (ci_level or 95.0) / 100.0
    if not (0 < level < 1):
        return None
    z = norm.ppf(0.5 + level / 2.0)
    if z <= 0:
        return None
    se = width / (2.0 * z)
    sd = se * math.sqrt(n)
    return sd if sd > 0 and math.isfinite(sd) else None


def _cohens_d_from_means(m_t, sd_t, n_t, m_c, sd_c, n_c):
    m_t = _safe_float(m_t)
    sd_t = _safe_float(sd_t)
    n_t = _safe_float(n_t)
    m_c = _safe_float(m_c)
    sd_c = _safe_float(sd_c)
    n_c = _safe_float(n_c)

    if None in [m_t, sd_t, n_t, m_c, sd_c, n_c]:
        return None

    if sd_t <= 0 or sd_c <= 0 or n_t <= 1 or n_c <= 1:
        return None

    pooled_sd = math.sqrt(
        ((n_t - 1) * sd_t**2 + (n_c - 1) * sd_c**2) / (n_t + n_c - 2)
    )

    if pooled_sd == 0:
        return None

    return (m_t - m_c) / pooled_sd


def _cohens_d_from_t(t_value, n_t, n_c):
    t_value = _safe_float(t_value)
    n_t = _safe_float(n_t)
    n_c = _safe_float(n_c)

    if None in [t_value, n_t, n_c]:
        return None

    if n_t <= 0 or n_c <= 0:
        return None

    return t_value * math.sqrt((n_t + n_c) / (n_t * n_c))


def _hedges_g(d, n_t, n_c):
    d = _safe_float(d)
    n_t = _safe_float(n_t)
    n_c = _safe_float(n_c)

    if None in [d, n_t, n_c]:
        return None

    df = n_t + n_c - 2

    if df <= 1:
        return None

    correction = 1 - (3 / (4 * df - 1))
    return correction * d


def _hedges_correction_factor(n_t, n_c):
    """Hedges (1981) small-sample bias-correction factor J -- used to back out
    a raw Cohen's d from an escalc()-supplied bias-corrected Hedges' g
    (d = g / J), since the GT schema keeps cohens_d and hedges_g as separate
    columns. Same formula as _hedges_g() below, applied in reverse."""
    n_t = _safe_float(n_t)
    n_c = _safe_float(n_c)
    if n_t is None or n_c is None:
        return None
    df = n_t + n_c - 2
    if df <= 1:
        return None
    return 1 - (3 / (4 * df - 1))


def _safe_log(x):
    x = _safe_float(x)
    if x is None or x <= 0:
        return None
    return math.log(x)


def _cohens_d_from_odds_ratio(or_value):
    """Convert odds ratio to Cohen's d via the log-odds transformation (Borenstein 2009)."""
    return _cohens_d_from_log_ratio(or_value)


def _cohens_d_from_log_ratio(ratio_value):
    """Convert a ratio measure (OR, RR, or HR) to Cohen's d via the log-odds
    transformation (Borenstein 2009): d = ln(ratio) * sqrt(3) / pi.

    Exact for an odds ratio. For RR/HR this is a LINEAR APPROXIMATION (RR/HR
    are not mathematically identical to OR) -- used only as a last-resort
    fallback so a row's hedges_g column is never left empty when the paper
    reports a ratio measure with no means/SDs available; the row's NATIVE
    ratio value (log-scale, exact) is preserved separately (see risk_ratio/
    hazard_ratio in _convert_row()'s output and utils/effect_measures.py's
    native-scale pooling path, which is authoritative over this fallback).
    Callers MUST tag conversion_method (e.g. "reported_rr", "hr_to_d_approx")
    so downstream code can distinguish an exact OR conversion from an
    approximate RR/HR one."""
    ratio_value = _safe_float(ratio_value)
    if ratio_value is None or ratio_value <= 0:
        return None
    return math.log(ratio_value) * math.sqrt(3) / math.pi


def _cohens_d_from_eta_squared(eta_sq):
    """Convert eta-squared (or partial eta-squared) to Cohen's d.

    Path: η² → r = √η², then r → d = 2r / √(1 − r²).
    Valid for 2-group contrasts; for k > 2 groups gives the average pairwise d.
    Reference: Cohen (1988), Borenstein et al. (2009).
    """
    eta_sq = _safe_float(eta_sq)
    if eta_sq is None or eta_sq <= 0 or eta_sq >= 1:
        return None
    r = math.sqrt(eta_sq)
    return 2 * r / math.sqrt(1 - r ** 2)


def _cohens_d_from_r(r):
    """Convert Pearson / point-biserial r to Cohen's d."""
    r = _safe_float(r)
    if r is None or abs(r) >= 1:
        return None
    return 2 * r / math.sqrt(1 - r ** 2)


def _cohens_d_from_beta(beta):
    """Convert standardised regression β to Cohen's d.

    Approximation: treat β ≈ point-biserial r, then apply r → d.
    Accurate when the predictor is a 0/1 binary dummy and groups are roughly equal.
    Reference: Peterson & Brown (2005).
    """
    beta = _safe_float(beta)
    if beta is None or abs(beta) >= 1:
        return None
    return 2 * beta / math.sqrt(1 - beta ** 2)


def _sum_additional_group_ns(s: str):
    """Parse 'Label=n, Label=n, ...' and return the sum, or None if unparseable."""
    import re
    nums = re.findall(r"=\s*(\d+)", s)
    if not nums:
        return None
    return sum(int(n) for n in nums)


def _normalise_proportion(v: float) -> float:
    """Convert percentage (0–100) or proportion (0–1) to a proportion (0–1)."""
    return v / 100.0 if v > 1.0 else v


def _looks_like_proportions(m_t, m_c, row) -> bool:
    """
    Return True when both means represent proportions or percentages.

    Signals checked (in order):
      1. Extractor explicitly filled group_N_mean_perc fields.
      2. outcome_measurement contains 'proportion', 'binary', 'percent', 'rate', 'dichotom'.
      3. Both raw means are already in (0, 1) — proportion form.
      (Values 1–100 are treated as percentages ONLY when signal 1 or 2 is present,
       to avoid misidentifying Likert-scale means as percentages.)
    """
    if m_t is None or m_c is None:
        return False
    # Signal 1: extractor flagged as percentage
    if row.get("group_2_mean_perc") or row.get("group_1_mean_perc"):
        return True
    # Signal 2: outcome measurement label
    om = _norm_text(row.get("outcome_measurement") or "")
    if any(kw in om for kw in ("proportion", "binary", "percent", "rate", "dichotom")):
        return True
    # Signal 3: values already in (0, 1) — unambiguously proportional
    if 0 < m_t < 1 and 0 < m_c < 1:
        return True
    return False


def _norm_text(x):
    return str(x or "").strip().lower()


def _looks_like_group_row(row):
    has_group_label = any(
        row.get(k) not in [None, ""]
        for k in ["group_label", "model", "condition", "group", "GenAI_Model"]
    )

    has_single_mean = any(
        row.get(k) not in [None, ""]
        for k in ["mean", "M", "group_mean"]
    )

    has_single_sd = any(
        row.get(k) not in [None, ""]
        for k in ["sd", "SD", "group_sd"]
    )

    has_single_n = any(
        row.get(k) not in [None, ""]
        for k in ["n", "N", "group_n"]
    )

    already_pairwise = any(
        row.get(k) not in [None, ""]
        for k in ["group_1_mean", "group_2_mean", "mean_control", "mean_treatment"]
    )

    return has_group_label and has_single_mean and has_single_sd and has_single_n and not already_pairwise


def _get_group_label(row):
    return (
        row.get("group_label")
        or row.get("model")
        or row.get("condition")
        or row.get("group")
        or row.get("GenAI_Model")
    )


def _get_single_mean(row):
    return row.get("mean") or row.get("M") or row.get("group_mean")


def _get_single_sd(row):
    return row.get("sd") or row.get("SD") or row.get("group_sd")


def _get_single_n(row):
    return row.get("n") or row.get("N") or row.get("group_n")


# ── Intervention/control ARM ORIENTATION check ──────────────────────────────
# This pipeline's whole conversion chain assumes group_1_* fields = control
# arm, group_2_* fields = treatment arm (see m_t/m_c above) -- but nothing
# upstream enforces that; the extractor just fills group_1_label/group_2_label
# with whatever text the paper's own table order happened to be. When a
# paper's table lists its intervention arm FIRST, the extracted group_1_*
# fields hold the intervention's numbers under this pipeline's own "control"
# slot -- silently inverting every downstream sign/direction for that row
# (confirmed on real data: a paper stating "readmissions were higher in the
# CONTROL group" produced a positive/"harm" Hedges' g here purely because
# group_1_label='intervention group' had been extracted into the control
# slot). Detected and corrected here from GENERIC RCT-arm phrasing only
# (control/placebo/usual-care vs intervention/add-on-phrasing) -- never a
# study/drug/review-specific rule, and only acted on when the signal is
# unambiguous; ambiguous or absent labels are left exactly as extracted.
_ARM_CONTROL_KEYWORDS = [
    "control", "placebo", "usual care", "usual treatment", "standard care",
    "standard treatment", "routine care", "comparison group", "waitlist",
    "no treatment", "no intervention", "baseline care",
]
_ARM_INTERVENTION_KEYWORDS = ["intervention", "treatment group", "experimental group"]
_ARM_ADDON_PHRASES = [
    "plus", "supplemented by", "in addition to", "added to", "with added",
    "combined with", "and additional", "on top of",
]


def _arm_orientation_score(label) -> int:
    """+1 if the label reads as a control/reference arm, -1 if it reads as
    the intervention arm, 0 if neither generic signal is present."""
    text = _norm_text(label)
    if not text:
        return 0
    score = 0
    if any(kw in text for kw in _ARM_CONTROL_KEYWORDS):
        score += 1
    if any(kw in text for kw in _ARM_INTERVENTION_KEYWORDS):
        score -= 1
    if any(kw in text for kw in _ARM_ADDON_PHRASES):
        score -= 1  # "X supplemented by Y" / "X plus Y" reads as the add-on/intervention arm
    return score


def _group_arms_are_swapped(group_1_label, group_2_label) -> bool:
    """Keyword-based FALLBACK ONLY -- see _row_arms_are_swapped(), which
    prefers the extractor's own explicit group_1_is_control judgment and
    only reaches this heuristic for legacy rows that never had that field
    filled. True only when group_1_label unambiguously reads as the
    intervention arm AND group_2_label unambiguously reads as the control
    arm. No fixed keyword list can cover every real phrasing (a control arm
    is very often an ACTIVE comparator -- "supportive therapy", "treatment
    as usual", another psychosocial intervention -- whose label doesn't
    obviously say "control"), which is exactly why this is a fallback and
    not the primary mechanism. Never guesses: any ambiguous/neutral/absent
    label on either side returns False (no correction applied)."""
    if not group_1_label or not group_2_label:
        return False
    return _arm_orientation_score(group_1_label) < 0 and _arm_orientation_score(group_2_label) > 0


def _row_arms_are_swapped(row: Dict[str, Any]) -> Tuple[bool, str]:
    """Whether this row's group_1/group_2 fields need swapping, and why.

    Primary signal: group_1_is_control, filled by the extraction LLM itself
    (agents/statistical_result_extractor_agent.py rule 21) from its own
    full-text reading of the paper against this study's actual treatment/
    control definitions -- inherently more reliable than any keyword list,
    since it generalizes to any phrasing (or language) the paper happens to
    use, not just the ones a list anticipated. Only when that field was
    left empty (legacy rows extracted before this field existed) does this
    fall back to the label-keyword heuristic in _group_arms_are_swapped()."""
    explicit = row.get("group_1_is_control")
    if explicit is not None:
        return (not bool(explicit)), "extractor_stated"
    return _group_arms_are_swapped(row.get("group_1_label"), row.get("group_2_label")), "label_keyword_fallback"


# Every group_1_*/group_2_* field pair (plus the legacy *_treatment/*_control
# aliases) that must swap together when a reversal is detected -- keeping
# this as one explicit list rather than a naming-convention scan means a row
# with unrelated group_1-prefixed keys (there are none today, but the whole
# point of this being a bug found via real data is that "should never
# happen" isn't a safe assumption) can never be swapped by accident.
_SWAPPABLE_FIELD_PAIRS = [
    ("group_1_label", "group_2_label"),
    ("group_1_n", "group_2_n"),
    ("group_1_mean", "group_2_mean"),
    ("group_1_sd", "group_2_sd"),
    ("group_1_se", "group_2_se"),
    ("group_1_mean_emm", "group_2_mean_emm"),
    ("group_1_mean_perc", "group_2_mean_perc"),
    ("group_1_ci_lower", "group_2_ci_lower"),
    ("group_1_ci_upper", "group_2_ci_upper"),
    ("group_1_events", "group_2_events"),
    ("group_1_total", "group_2_total"),
    ("group_1_median", "group_2_median"),
    ("group_1_iqr_lower", "group_2_iqr_lower"),
    ("group_1_iqr_upper", "group_2_iqr_upper"),
    ("group_1_range_lower", "group_2_range_lower"),
    ("group_1_range_upper", "group_2_range_upper"),
    ("mean_control", "mean_treatment"),
    ("sd_control", "sd_treatment"),
    ("n_control", "n_treatment"),
]


def _correct_group_swap_if_detected(row: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a swapped copy of `row` if its arms need reversing (per
    _row_arms_are_swapped -- the extractor's own explicit judgment when
    present, else the label-keyword fallback), else returns `row` unchanged
    (same object, no copy -- a no-op for the overwhelming majority of rows
    that are already correctly oriented)."""
    swap_needed, reason = _row_arms_are_swapped(row)
    if not swap_needed:
        return row
    swapped = dict(row)
    for key_a, key_b in _SWAPPABLE_FIELD_PAIRS:
        swapped[key_a], swapped[key_b] = row.get(key_b), row.get(key_a)
    if reason == "extractor_stated":
        swapped["_arm_orientation_corrected"] = (
            f"group_1/group_2 fields swapped: the extractor itself stated group_1_label "
            f"({row.get('group_1_label')!r}) is the intervention arm (group_1_is_control=False)"
        )
    else:
        swapped["_arm_orientation_corrected"] = (
            f"group_1/group_2 fields swapped: group_1_label ({row.get('group_1_label')!r}) read as "
            f"the intervention arm, group_2_label ({row.get('group_2_label')!r}) read as the control "
            "arm -- reversed relative to this pipeline's group_1=control/group_2=treatment convention "
            "(label-keyword fallback; row predates the extractor's explicit group_1_is_control field)"
        )
    return swapped


def _select_reference_group(group_rows):
    priority_terms = [
        "control",
        "placebo",
        "baseline",
        "usual care",
        "standard care",
        "human",
        "no treatment",
        "low dose",
        "waitlist",
    ]

    for term in priority_terms:
        for row in group_rows:
            label = _norm_text(_get_group_label(row))
            if term in label:
                return row

    return group_rows[0]


def build_pairwise_comparisons(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert group-level descriptive rows into comparison-level rows."""
    group_rows = [r for r in rows if _looks_like_group_row(r)]
    other_rows = [r for r in rows if not _looks_like_group_row(r)]

    if not group_rows:
        return rows

    grouped = {}

    for row in group_rows:
        key = (
            row.get("paper_id"),
            row.get("study_label"),
            row.get("outcome_name"),
            row.get("result_role"),
        )
        grouped.setdefault(key, []).append(row)

    comparisons = []

    for key, rows_for_outcome in grouped.items():
        if len(rows_for_outcome) < 2:
            comparisons.extend(rows_for_outcome)
            continue

        control = _select_reference_group(rows_for_outcome)
        control_label = _get_group_label(control)

        for row in rows_for_outcome:
            if row is control:
                continue

            treatment_label = _get_group_label(row)
            comparison = dict(row)

            comparison["group_2_label"] = treatment_label
            comparison["group_1_label"] = control_label

            comparison["group_2_n"] = _get_single_n(row)
            comparison["group_2_mean"] = _get_single_mean(row)
            comparison["group_2_sd"] = _get_single_sd(row)

            comparison["group_1_n"] = _get_single_n(control)
            comparison["group_1_mean"] = _get_single_mean(control)
            comparison["group_1_sd"] = _get_single_sd(control)

            comparison["comparison_label"] = f"{treatment_label} vs {control_label}"
            comparison["statistic_type"] = "descriptive"
            comparison["comparison_type"] = "pairwise_from_group_table"

            comparisons.append(comparison)

    return other_rows + comparisons


def _propagate_sample_sizes(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Fill missing n_treatment / n_control from a known row in the same study."""
    study_ns: Dict[tuple, tuple] = {}

    for row in rows:
        key = (row.get("paper_id"), row.get("study_label"))
        n_t = _safe_int(row.get("group_2_n") or row.get("n_treatment"))
        n_c = _safe_int(row.get("group_1_n") or row.get("n_control"))
        if n_t and n_c and key not in study_ns:
            study_ns[key] = (n_t, n_c)

    for row in rows:
        key = (row.get("paper_id"), row.get("study_label"))
        n_t = _safe_int(row.get("group_2_n") or row.get("n_treatment"))
        n_c = _safe_int(row.get("group_1_n") or row.get("n_control"))
        if (not n_t or not n_c) and key in study_ns:
            filled_t, filled_c = study_ns[key]
            if not row.get("group_2_n") and not row.get("n_treatment"):
                row["group_2_n"] = filled_t
            if not row.get("group_1_n") and not row.get("n_control"):
                row["group_1_n"] = filled_c

    return rows


def _deduplicate_raw(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove redundant rows for the same outcome within the same study.
    Operates on raw extracted rows (before conversion to GT columns).
    """
    _STAT_RANK = {
        "t_test": 0, "anova": 1, "chi_square": 2,
        "proportion": 3, "descriptive": 4, "descriptive_only": 5,
    }

    def _rank(row):
        return _STAT_RANK.get(_norm_text(row.get("statistic_type") or ""), 99)

    def _means_match(a, b):
        ma = _safe_float(a.get("group_2_mean") or a.get("mean_treatment"))
        mb = _safe_float(b.get("group_2_mean") or b.get("mean_treatment"))
        ca = _safe_float(a.get("group_1_mean") or a.get("mean_control"))
        cb = _safe_float(b.get("group_1_mean") or b.get("mean_control"))
        if None in (ma, mb, ca, cb):
            return False
        return (
            abs(ma - mb) / (abs(mb) + 1e-9) < 0.01
            and abs(ca - cb) / (abs(cb) + 1e-9) < 0.01
        )

    def _test_stat_match(a, b):
        ta = _safe_float(a.get("test_statistic"))
        tb = _safe_float(b.get("test_statistic"))
        if ta is None or tb is None:
            return False
        return abs(ta - tb) / (abs(tb) + 1e-9) < 0.01

    from collections import defaultdict
    groups: Dict[tuple, list] = defaultdict(list)
    for row in rows:
        key = (
            row.get("paper_id"),
            row.get("study_label"),
            _norm_text(row.get("outcome_name") or ""),
        )
        groups[key].append(row)

    result = []
    for key, group_rows in groups.items():
        if len(group_rows) == 1:
            result.extend(group_rows)
            continue

        non_descriptive = [r for r in group_rows if _rank(r) < 4]
        descriptive = [r for r in group_rows if _rank(r) >= 4]

        seen = []
        for row in non_descriptive:
            is_dup = any(
                _norm_text(row.get("statistic_type") or "") ==
                _norm_text(s.get("statistic_type") or "")
                and _means_match(row, s)
                and _test_stat_match(row, s)
                for s in seen
            )
            if not is_dup:
                seen.append(row)
        non_descriptive = seen

        if not non_descriptive:
            result.extend(group_rows)
            continue

        to_drop = set()
        for desc in descriptive:
            for nd in non_descriptive:
                if _means_match(desc, nd):
                    to_drop.add(id(desc))
                    break

        result.extend(non_descriptive)
        result.extend(d for d in descriptive if id(d) not in to_drop)

    return result


def _normalize_study_labels(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Re-sequence study_label values per paper so they always start at 1.

    Unique labels are sorted by their embedded integer (Study 2 < Study 3)
    before mapping, so extraction order never determines the final numbering.
    """
    import re

    def _label_sort_key(lbl: str):
        m = re.search(r"\d+", lbl)
        return (int(m.group()), lbl) if m else (9999, lbl)

    # Collect unique labels per paper
    paper_unique: Dict[str, set] = {}
    for row in rows:
        pid = row.get("paper_id") or ""
        lbl = row.get("study_label") or ""
        if lbl:
            paper_unique.setdefault(pid, set()).add(lbl)

    # Build mapping: sort by embedded number, then assign Study 1, Study 2, …
    paper_label_map: Dict[str, Dict[str, str]] = {}
    for pid, labels in paper_unique.items():
        sorted_labels = sorted(labels, key=_label_sort_key)
        paper_label_map[pid] = {lbl: f"Study {i + 1}" for i, lbl in enumerate(sorted_labels)}

    for row in rows:
        pid = row.get("paper_id") or ""
        lbl = row.get("study_label") or ""
        if pid in paper_label_map and lbl in paper_label_map[pid]:
            row["study_label"] = paper_label_map[pid][lbl]

    return rows


def _detect_odds_ratio(row):
    text = " ".join(
        str(row.get(k, ""))
        for k in [
            "effect_size_name",
            "statistic_type",
            "outcome_name",
            "evidence_quote",
            "notes",
        ]
    ).lower()
    return "odds" in text or "or =" in text or "odds ratio" in text


def _get_odds_ratio(row):
    for key in ["odds_ratio", "or_value", "effect_value"]:
        value = _safe_float(row.get(key))
        if value is not None and value > 0:
            return value

    relative_change = _safe_float(row.get("relative_change"))
    if relative_change is not None:
        return 1 + relative_change

    import re
    evidence = str(row.get("evidence_quote", ""))
    match = re.search(
        r"([+-]?\d+(\.\d+)?)\s*%\s*(increase|decrease).*odds", evidence.lower()
    )
    if match:
        pct = float(match.group(1)) / 100.0
        return 1 - pct if "decrease" in match.group(3) else 1 + pct

    return None


def _get_ci_bounds(row):
    low = row.get("ci_low") or row.get("ci_lower") or row.get("confidence_interval_low")
    high = row.get("ci_high") or row.get("ci_upper") or row.get("confidence_interval_high")

    low = _safe_float(low)
    high = _safe_float(high)

    if low is not None and high is not None:
        if low < 1 and high > 1:
            return 1 + low, 1 + high
        return low, high

    import re
    evidence = str(row.get("evidence_quote", ""))
    match = re.search(
        r"ci\s*\[\s*([+-]?\d+(\.\d+)?)\s*%\s*,\s*([+-]?\d+(\.\d+)?)\s*%",
        evidence.lower(),
    )
    if match:
        return 1 + float(match.group(1)) / 100.0, 1 + float(match.group(3)) / 100.0

    return None, None


def _convert_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Convert one raw extracted row into a GT-column dict (53 columns)."""
    row = _correct_group_swap_if_detected(row)
    statistic_type = row.get("statistic_type")
    result_role = row.get("result_role")

    # ── Core numeric extractions ────────────────────────────────────────────
    # n_t/n_c: prefer the continuous-style group_2_n/group_1_n (or the
    # already-coalesced n_treatment/n_control), but fall back to the
    # dichotomous group_2_total/group_1_total when neither is filled -- a
    # row reporting only event/total counts (e.g. dropout, mortality) is
    # just as valid a sample size as one reporting mean/SD, and this is the
    # ONLY place in the whole conversion that derives the OUTPUT
    # n_treatment/n_control/n_total GT columns, so leaving it unfallback'd
    # here silently drops an otherwise fully poolable dichotomous row later
    # in agents/effect_size_agent.py (which has no group_*_total fallback of
    # its own) purely because the extractor happened not to also redundantly
    # fill group_2_n/group_1_n for THIS row while filling them for others in
    # the same outcome group -- the real root cause of a Wetherell 2003 row
    # vanishing from CD007674's dropout-rate pool despite complete 8/26 vs
    # 9/26 counts. Generic across every review/study: keyed purely on which
    # fields are present, never on any study/paper identity.
    n_t = _safe_int(row.get("group_2_n") or row.get("n_treatment") or row.get("group_2_total"))
    n_c = _safe_int(row.get("group_1_n") or row.get("n_control") or row.get("group_1_total"))
    m_t = _safe_float(row.get("group_2_mean") or row.get("mean_treatment"))
    m_c = _safe_float(row.get("group_1_mean") or row.get("mean_control"))
    sd_t = _safe_float(row.get("group_2_sd") or row.get("sd_treatment"))
    sd_c = _safe_float(row.get("group_1_sd") or row.get("sd_control"))

    # ── SD derived from a reported mean + CI, when no SD/SE was extracted ──
    # Common, fully standard reporting format (mean with 95% CI instead of
    # SD) that previously had no conversion path at all -- see
    # _sd_from_ci()'s docstring for the exact (non-approximate) formula.
    # Only fills the gap; a directly-reported SD always wins.
    sd_t_derivation = None
    sd_c_derivation = None
    ci_level = _safe_float(row.get("ci_level"))
    if sd_t is None:
        sd_t = _sd_from_ci(
            _safe_float(row.get("group_2_ci_lower")), _safe_float(row.get("group_2_ci_upper")),
            n_t, ci_level,
        )
        if sd_t is not None:
            sd_t_derivation = "treatment SD derived from its reported mean CI"
    if sd_c is None:
        sd_c = _sd_from_ci(
            _safe_float(row.get("group_1_ci_lower")), _safe_float(row.get("group_1_ci_upper")),
            n_c, ci_level,
        )
        if sd_c is not None:
            sd_c_derivation = "control SD derived from its reported mean CI"

    # ── SD derived from a reported standard ERROR, when no SD/CI was extracted ──
    # A paper reporting SE instead of SD (common for least-squares/adjusted means from
    # an ANCOVA or mixed model) previously had no conversion path at all -- the
    # extractor's group_1_se/group_2_se fields were collected but never consumed here,
    # so a row like this silently fell through to "insufficient numeric information"
    # even though SD = SE * sqrt(n) is an exact, standard identity, not an approximation.
    # Same priority as the CI-derivation above: only fills the gap, a directly-reported
    # or CI-derived SD always wins.
    if sd_t is None:
        se_t = _safe_float(row.get("group_2_se"))
        if se_t is not None and n_t:
            sd_t = se_t * math.sqrt(n_t)
            sd_t_derivation = "treatment SD derived from its reported SE (SD = SE * sqrt(n))"
    if sd_c is None:
        se_c = _safe_float(row.get("group_1_se"))
        if se_c is not None and n_c:
            sd_c = se_c * math.sqrt(n_c)
            sd_c_derivation = "control SD derived from its reported SE (SD = SE * sqrt(n))"

    test_stat = row.get("test_statistic")
    # For t_test: test_statistic IS the t-value.
    # For regression/mixed_model: the extractor puts the coefficient t-value in
    # test_statistic; fall back to an explicit t_value field if present.
    if statistic_type == "t_test":
        t_val = _safe_float(test_stat)
    else:
        t_val = _safe_float(row.get("t_value")) or _safe_float(test_stat)
    f_val = _safe_float(test_stat) if statistic_type == "anova" else _safe_float(row.get("f_value"))

    # ── Odds ratio ──────────────────────────────────────────────────────────
    odds_ratio = _safe_float(row.get("odds_ratio"))
    ci_lower_or = _safe_float(row.get("ci_lower_or"))
    ci_upper_or = _safe_float(row.get("ci_upper_or"))

    # Treat 0 as "not reported" — 0 is not a valid odds ratio
    if not odds_ratio:
        odds_ratio = None
    if not ci_lower_or:
        ci_lower_or = None
    if not ci_upper_or:
        ci_upper_or = None

    if odds_ratio is None and _detect_odds_ratio(row):
        odds_ratio = _get_odds_ratio(row)
        if ci_lower_or is None or ci_upper_or is None:
            lo, hi = _get_ci_bounds(row)
            ci_lower_or = ci_lower_or if ci_lower_or is not None else lo
            ci_upper_or = ci_upper_or if ci_upper_or is not None else hi

    # ── Risk ratio (native-measure evidence -- NOT derived from odds_ratio;
    # only a directly-reported RR counts as tier-2 "paper explicitly
    # reported this measure" evidence, see utils/effect_measures.py) ───────
    risk_ratio = _safe_float(row.get("risk_ratio")) or None
    ci_lower_rr = _safe_float(row.get("ci_lower_rr")) or None
    ci_upper_rr = _safe_float(row.get("ci_upper_rr")) or None

    # ── Hazard ratio (same native-measure convention as risk ratio above --
    # NEVER derived from counts/proportions; there is no valid 2x2-table
    # reconstruction of a time-to-event hazard ratio) ──────────────────────
    hazard_ratio = _safe_float(row.get("hazard_ratio")) or None
    ci_lower_hr = _safe_float(row.get("ci_lower_hr")) or None
    ci_upper_hr = _safe_float(row.get("ci_upper_hr")) or None

    # ── Dichotomous event counts (native OR/RR raw inputs) ─────────────────
    group_1_events = _safe_float(row.get("group_1_events"))
    group_1_total = _safe_float(row.get("group_1_total"))
    group_2_events = _safe_float(row.get("group_2_events"))
    group_2_total = _safe_float(row.get("group_2_total"))

    # ── Median/IQR or median/range (continuous outcomes reported without
    # means/SDs) -- see utils/wan2014.py. Both arms must report the SAME
    # shape to be usable (checked below, at the point of use). ─────────────
    g1_median = _safe_float(row.get("group_1_median"))
    g1_iqr_lo = _safe_float(row.get("group_1_iqr_lower"))
    g1_iqr_hi = _safe_float(row.get("group_1_iqr_upper"))
    g1_range_lo = _safe_float(row.get("group_1_range_lower"))
    g1_range_hi = _safe_float(row.get("group_1_range_upper"))
    g2_median = _safe_float(row.get("group_2_median"))
    g2_iqr_lo = _safe_float(row.get("group_2_iqr_lower"))
    g2_iqr_hi = _safe_float(row.get("group_2_iqr_upper"))
    g2_range_lo = _safe_float(row.get("group_2_range_lower"))
    g2_range_hi = _safe_float(row.get("group_2_range_upper"))

    # ── Native effect-measure resolution evidence (passthrough, never
    # inferred here -- only what the extractor explicitly recorded) ────────
    reported_effect_measure = row.get("reported_effect_measure") or None
    outcome_units = row.get("outcome_units") or None
    outcome_scale_min = _safe_float(row.get("outcome_scale_min"))
    outcome_scale_max = _safe_float(row.get("outcome_scale_max"))

    # ── Lab/clinical-unit conversion (e.g. mg/dL -> mmol/L for a named
    # analyte) -- applied here, before m_t/sd_t/m_c/sd_c are used for M_diff/
    # cohens_d below and written out as M_treatment/SD_treatment/etc., so
    # every downstream consumer (GT columns, effect_size_agent.py,
    # effect_measures.py's outcome_units equality check) sees an
    # already-canonicalized value with no separate unit-aware code path
    # needed anywhere else. Filled by the extractor ONLY when the paper's
    # stated unit has a universally fixed, textbook conversion factor for
    # the exact analyte named in outcome_name -- never inferred or guessed
    # here; see agents/statistical_result_extractor_agent.py rule 23. Both
    # fields must be present (never one alone), mirroring the
    # outcome_scale_min/outcome_scale_max convention above.
    outcome_unit_conversion_factor = _safe_float(row.get("outcome_unit_conversion_factor"))
    outcome_units_canonical = row.get("outcome_units_canonical") or None
    outcome_units_original = None
    if outcome_unit_conversion_factor and outcome_units_canonical:
        outcome_units_original = outcome_units
        if m_t is not None:
            m_t = m_t * outcome_unit_conversion_factor
        if sd_t is not None:
            sd_t = sd_t * outcome_unit_conversion_factor
        if m_c is not None:
            m_c = m_c * outcome_unit_conversion_factor
        if sd_c is not None:
            sd_c = sd_c * outcome_unit_conversion_factor
        outcome_units = outcome_units_canonical

    reported_measure_enum = normalize_effect_measure_text(reported_effect_measure)

    # ── n_total (needed by inference block below) ───────────────────────────
    n_total = _safe_int(row.get("n_total"))
    if n_total is None and n_t and n_c:
        n_total = n_t + n_c

    # ── df→n inference (t-test only) ────────────────────────────────────────
    # For independent-samples t-test: df = n1 + n2 − 2  ⟹  n_total = df + 2.
    # When both group Ns are missing but df is reported, recover them.
    _extra_notes = []
    _df1_raw = _safe_int(row.get("df1"))
    if (
        statistic_type == "t_test"
        and t_val is not None
        and _df1_raw is not None
        and not n_t
        and not n_c
    ):
        _n_total_inferred = _df1_raw + 2
        n_t = _n_total_inferred // 2
        n_c = _n_total_inferred - n_t
        if n_total is None:
            n_total = _n_total_inferred
        _extra_notes.append(
            f"n_treatment({n_t}) and n_control({n_c}) inferred from t-test df={_df1_raw}"
        )

    # ── equal-split inference from n_total ───────────────────────────────────
    # When per-group Ns are still missing but n_total is known and the design
    # is a 2-group comparison (t-test with df, or 2-group ANOVA with df1=1,
    # or descriptive with means+SDs), assume equal groups as a last resort.
    # This recovers effect sizes for papers that report only total N.
    _is_two_group_design = (
        statistic_type in {"t_test", "descriptive", "descriptive_only"}
        or (statistic_type == "anova" and (_df1_raw is None or _df1_raw == 1))
    )
    if not n_t and not n_c and n_total and _is_two_group_design:
        n_t = n_total // 2
        n_c = n_total - n_t
        _extra_notes.append(
            f"n_treatment({n_t}) and n_control({n_c}) assumed equal split from n_total={n_total}"
        )

    # ── M_diff and SE_diff ──────────────────────────────────────────────────
    # These are needed by the regression/mixed-model conversion path below.
    # Treat 0 as "not reported" — the LLM often fills unused numeric fields with 0.
    M_diff = _safe_float(row.get("M_diff")) or None
    if M_diff is None and m_t is not None and m_c is not None:
        # Only compute M_diff for simple t-test-style two-group comparisons.
        # For ANOVA and other designs, a single pairwise difference may not be meaningful.
        if statistic_type in {"t_test", None, ""}:
            M_diff = round(m_t - m_c, 6)

    # SE_diff: pass through only if directly reported or derived upstream with an
    # explicit extraction warning; never compute it here from SDs.
    SE_diff = _safe_float(row.get("SE_diff")) or None

    # ── Effect size computation ─────────────────────────────────────────────
    # Established conversions (means+SDs, t-value, and — for regression/mixed
    # models — the coefficient's partial correlation) are computed by R's
    # metafor::escalc() (statistics/metafor_engine.py), not from-scratch
    # Python formulas. Conversions with no established escalc() measure (η²,
    # standardised β, r, odds ratio, proportions) are unchanged. When escalc
    # supplies hedges_g_val directly, it also supplies effect_variance —
    # agents/effect_size_agent.py already prefers that field over its own
    # fallback variance formula, so no changes were needed there.
    cohens_d = None
    hedges_g_val = None
    effect_variance = None
    effect_size_ready = False
    exclusion_reason = None

    # Reported effect size name/value (used for eta², β, r conversions)
    es_name = _norm_text(row.get("effect_size_name") or "")
    es_val  = _safe_float(row.get("effect_size_value"))

    method = None
    conversion_method = None

    if odds_ratio is not None:
        # Convert OR → Cohen's d → Hedges' g (no established escalc() measure
        # for an already-reported OR with no raw 2x2 table to recompute from —
        # stays the from-scratch Borenstein 2009 log-odds conversion)
        or_d = _cohens_d_from_odds_ratio(odds_ratio)
        if or_d is not None:
            if n_t and n_c and n_t > 1 and n_c > 1:
                or_g = _hedges_g(or_d, n_t, n_c)
            else:
                or_g = or_d
            if or_g is not None:
                cohens_d = round(or_d, 6)
                hedges_g_val = round(or_g, 6)
        effect_size_ready = True
        conversion_method = "reported_or"

    # ── Priority 0b/0c: directly-reported RR or HR ──────────────────────────
    # Same convention as OR above: an already-reported ratio+CI is always
    # recognized ahead of everything else. The row's NATIVE value (risk_ratio/
    # hazard_ratio, log scale) is preserved unchanged in the output dict below
    # and is what utils/effect_measures.py actually pools on; the Hedges' g
    # computed here is only a same-scale-as-everything-else fallback display
    # value, explicitly tagged so it's never confused with an exact SMD.
    elif risk_ratio is not None:
        rr_d = _cohens_d_from_log_ratio(risk_ratio)
        if rr_d is not None:
            rr_g = _hedges_g(rr_d, n_t, n_c) if (n_t and n_c and n_t > 1 and n_c > 1) else rr_d
            if rr_g is not None:
                cohens_d = round(rr_d, 6)
                hedges_g_val = round(rr_g, 6)
        effect_size_ready = True
        conversion_method = "reported_rr"

    elif hazard_ratio is not None:
        hr_d = _cohens_d_from_log_ratio(hazard_ratio)
        if hr_d is not None:
            hr_g = _hedges_g(hr_d, n_t, n_c) if (n_t and n_c and n_t > 1 and n_c > 1) else hr_d
            if hr_g is not None:
                cohens_d = round(hr_d, 6)
                hedges_g_val = round(hr_g, 6)
        effect_size_ready = True
        conversion_method = "hr_to_d_approx"

    elif result_role not in {None, "", "primary_outcome", "secondary_outcome", "unclear"}:
        exclusion_reason = "not primary or secondary outcome"

    else:
        has_means_sds = all(
            v is not None for v in [m_t, m_c, sd_t, sd_c, n_t, n_c]
        )
        has_dichotomous_counts = (
            group_1_events is not None and group_1_total is not None
            and group_2_events is not None and group_2_total is not None
            and group_1_total > group_1_events >= 0 and group_2_total > group_2_events >= 0
        )

        # ── Priority 0d: raw 2x2 event counts -> exact log-OR/RR via
        # metafor::escalc(), then the SAME Borenstein log-ratio->d transform
        # already used for an already-reported ratio (Priorities 0/0b/0c).
        # This is an EXACT computation from the paper's own reported counts
        # -- strictly better than Priority 5's proportions-reconstruction
        # approximation below, so it's tried first whenever real counts are
        # available. Root-cause fix: raw counts were already being extracted
        # (group_1/2_events/total) and already used by utils/effect_measures.py's
        # native-scale side-channel, but the MAIN cohens_d/hedges_g/GT-column
        # chain had no branch for them at all -- a paper reporting a plain
        # 2x2 table (Fisher's exact test, chi-square, or just "n events / N")
        # with no pre-computed OR/RR/HR fell straight through every other
        # priority to the "unsupported" catch-all, even though the counts
        # alone are everything metafor needs to compute an exact effect size.
        if has_dichotomous_counts and group_1_events == 0 and group_2_events == 0:
            # Double-zero-event study: zero events in BOTH arms carries no
            # information about the relative treatment effect for a ratio
            # measure -- standard Cochrane Handbook / RevMan practice is to
            # mark such a study "Not estimable" and exclude it from the
            # pooled analysis entirely, rather than apply a continuity
            # correction that would manufacture a near-null point estimate
            # out of a genuinely uninformative comparison (observed directly
            # in multiple Cochrane forest plots this benchmark, e.g. zero-
            # event rows shown as "Not estimable"). Purely data-driven (both
            # event counts are exactly zero) -- no study/review identity
            # involved, so this applies uniformly to any dichotomous outcome.
            exclusion_reason = (
                "zero events in both arms -- not estimable for a ratio measure "
                "(Cochrane convention: excluded from pooling, not continuity-corrected)"
            )
        elif has_dichotomous_counts:
            a, b, c, d = group_2_events, group_2_total - group_2_events, group_1_events, group_1_total - group_1_events
            use_rr = reported_measure_enum == EffectMeasure.RR
            fn = metafor_engine.escalc_rr_from_counts if use_rr else metafor_engine.escalc_or_from_counts
            escalc_result = fn(a, b, c, d)
            if escalc_result is not None:
                log_ratio = escalc_result["log_rr" if use_rr else "log_or"]
                cohens_d = log_ratio * math.sqrt(3) / math.pi
                method = "counts_to_rr_via_escalc" if use_rr else "counts_to_or_via_escalc"
                conversion_method = method

        # ── Priority 1: means + SDs (works for any design) ─────────────────
        elif has_means_sds:
            smd = metafor_engine.escalc_smd_from_means(m_t, sd_t, n_t, m_c, sd_c, n_c)
            if smd is not None:
                hedges_g_val = smd["g"]
                effect_variance = smd["vi"]
                correction = _hedges_correction_factor(n_t, n_c)
                cohens_d = hedges_g_val / correction if correction else hedges_g_val
            else:
                cohens_d = _cohens_d_from_means(m_t, sd_t, n_t, m_c, sd_c, n_c)
            if sd_t_derivation or sd_c_derivation:
                method = "means_ci_derived_sd"
                for note in (sd_t_derivation, sd_c_derivation):
                    if note:
                        _extra_notes.append(note)
            else:
                method = "means_sds"
            conversion_method = method

        # ── Priority 1b: median/IQR or median/range (Wan et al. 2014) --
        # only when means/SDs are unavailable but BOTH arms report the same
        # median-based shape. Estimated means/SDs then flow through the same
        # escalc(SMD) call as Priority 1 -- always tagged as an approximation.
        elif (
            g1_median is not None and g2_median is not None and n_t and n_c
            and (
                (g1_iqr_lo is not None and g1_iqr_hi is not None
                 and g2_iqr_lo is not None and g2_iqr_hi is not None)
                or (g1_range_lo is not None and g1_range_hi is not None
                    and g2_range_lo is not None and g2_range_hi is not None)
            )
        ):
            if g1_iqr_lo is not None and g1_iqr_hi is not None and g2_iqr_lo is not None and g2_iqr_hi is not None:
                est_t = estimate_mean_sd_from_median_iqr(g2_median, g2_iqr_lo, g2_iqr_hi, n_t)
                est_c = estimate_mean_sd_from_median_iqr(g1_median, g1_iqr_lo, g1_iqr_hi, n_c)
                shape = "iqr"
            else:
                est_t = estimate_mean_sd_from_median_range(g2_median, g2_range_lo, g2_range_hi, n_t)
                est_c = estimate_mean_sd_from_median_range(g1_median, g1_range_lo, g1_range_hi, n_c)
                shape = "range"
            if est_t is not None and est_c is not None:
                m_t_est, sd_t_est = est_t
                m_c_est, sd_c_est = est_c
                smd = metafor_engine.escalc_smd_from_means(m_t_est, sd_t_est, n_t, m_c_est, sd_c_est, n_c)
                if smd is not None:
                    hedges_g_val = smd["g"]
                    effect_variance = smd["vi"]
                    correction = _hedges_correction_factor(n_t, n_c)
                    cohens_d = hedges_g_val / correction if correction else hedges_g_val
                else:
                    cohens_d = _cohens_d_from_means(m_t_est, sd_t_est, n_t, m_c_est, sd_c_est, n_c)
                # m_t/sd_t/m_c/sd_c (below, in the output dict's M_treatment/
                # SD_treatment/etc. columns) deliberately stay None/whatever
                # the paper actually reported -- an ESTIMATED mean/SD must
                # never impersonate a directly-reported one in those columns.
                # The estimate is only used for the escalc() call above and
                # surfaced in Comment (_extra_notes) + conversion_method.
                method = f"median_{shape}_wan2014_approx"
                conversion_method = "median_iqr_wan2014_approx" if shape == "iqr" else "median_range_wan2014_approx"
                _extra_notes.append(
                    f"mean/SD estimated from median/{shape.upper()} via Wan et al. (2014): "
                    f"treatment mean={m_t_est:.4f} SD={sd_t_est:.4f}, "
                    f"control mean={m_c_est:.4f} SD={sd_c_est:.4f} -- APPROXIMATION, not directly reported"
                )
            else:
                exclusion_reason = "median/IQR or median/range reported but Wan 2014 estimation failed (invalid inputs)"

        # ── Priority 2: t-test ──────────────────────────────────────────────
        elif statistic_type == "t_test" and t_val is not None and n_t and n_c:
            smd = metafor_engine.escalc_smd_from_t(t_val, n_t, n_c)
            if smd is not None:
                hedges_g_val = smd["g"]
                effect_variance = smd["vi"]
                correction = _hedges_correction_factor(n_t, n_c)
                cohens_d = hedges_g_val / correction if correction else hedges_g_val
            else:
                cohens_d = _cohens_d_from_t(t_val, n_t, n_c)
            method = "t_value"

        # ── Priority 3: ANOVA ───────────────────────────────────────────────
        elif statistic_type == "anova":
            ct = _norm_text(row.get("comparison_type") or "")
            if ct not in {"between_subjects", "matched", ""}:
                exclusion_reason = (
                    f"ANOVA excluded: comparison_type='{ct}' is not between-group"
                )
            else:
                f_v  = _safe_float(test_stat)
                df1  = _safe_int(row.get("df1"))
                if f_v is not None and f_v > 0 and n_t and n_c:
                    if df1 is None or df1 == 1:
                        # 2-group ANOVA: F → t (sign recovered from means; no
                        # F→SMD escalc measure exists) → SMD via escalc
                        t_equiv = math.sqrt(f_v)
                        if m_t is not None and m_c is not None and m_t < m_c:
                            t_equiv = -t_equiv
                        smd = metafor_engine.escalc_smd_from_t(t_equiv, n_t, n_c)
                        if smd is not None:
                            hedges_g_val = smd["g"]
                            effect_variance = smd["vi"]
                            correction = _hedges_correction_factor(n_t, n_c)
                            cohens_d = hedges_g_val / correction if correction else hedges_g_val
                        else:
                            cohens_d = _cohens_d_from_t(t_equiv, n_t, n_c)
                        method = "f_value"
                    else:
                        # Multi-group ANOVA (df1 > 1): require η² (no η²→SMD
                        # escalc measure exists — stays from-scratch)
                        if es_val is not None and es_name in {
                            "eta_squared", "partial_eta_squared",
                            "eta2", "partial_eta2", "eta_sq",
                        }:
                            cohens_d = _cohens_d_from_eta_squared(es_val)
                            method = f"eta_squared (df1={df1})"
                        else:
                            exclusion_reason = (
                                f"multi-group ANOVA (df1={df1}): "
                                "eta-squared or partial-eta-squared required — not found"
                            )
                else:
                    exclusion_reason = "ANOVA: missing F-value or group sizes"

        # ── Priority 4: regression / mixed model ────────────────────────────
        elif statistic_type in {"regression", "mixed_model"}:
            # Preferred: partial correlation via metafor::escalc(measure="PCOR")
            # (Aloe & Becker 2012) — the methodologically correct way to convert
            # a regression coefficient, rather than treating its t-value as if
            # it came from a plain t-test. Needs the coefficient's t-value, the
            # model's total N, and its number of predictors; the last of these
            # isn't extracted directly but is recoverable from the residual df
            # the extractor already captures (df1) via the standard OLS
            # identity: predictors = N − df1 − 1. Only used when that identity
            # yields a sane predictor count (>=1, and less than N-2) — otherwise
            # falls through to the existing approach below.
            pcor_used = False
            n_for_pcor = (n_t + n_c) if (n_t and n_c) else n_total
            if t_val is not None and _df1_raw is not None and n_for_pcor:
                num_predictors = n_for_pcor - _df1_raw - 1
                if 1 <= num_predictors <= n_for_pcor - 3:
                    pcor = metafor_engine.escalc_pcor(t_val, n_for_pcor, num_predictors)
                    if pcor is not None:
                        pcor_d = _cohens_d_from_r(pcor["r"])
                        if pcor_d is not None:
                            cohens_d = pcor_d
                            method = f"pcor_{statistic_type}"
                            pcor_used = True
                            # The later Hedges' g correction needs per-group Ns;
                            # a regression model has none, so approximate with
                            # an equal split of the model's total N (same
                            # convention already used by the *_approx paths
                            # below) purely for that correction step.
                            if not (n_t and n_c):
                                n_t = n_for_pcor // 2
                                n_c = n_for_pcor - n_t
                                _extra_notes.append(
                                    f"PCOR from t={t_val}, N={n_for_pcor}, "
                                    f"predictors={num_predictors} (from df1={_df1_raw}); "
                                    "n_treatment/n_control assumed equal split for the "
                                    "Hedges' g small-sample correction only"
                                )

            if pcor_used:
                pass
            elif t_val is not None and n_t and n_c:
                # t-value of the key coefficient, treated as if from a t-test —
                # fallback when PCOR's inputs (t + N + predictor count) aren't
                # all available or don't yield a sane predictor count.
                smd = metafor_engine.escalc_smd_from_t(t_val, n_t, n_c)
                if smd is not None:
                    hedges_g_val = smd["g"]
                    effect_variance = smd["vi"]
                    correction = _hedges_correction_factor(n_t, n_c)
                    cohens_d = hedges_g_val / correction if correction else hedges_g_val
                else:
                    cohens_d = _cohens_d_from_t(t_val, n_t, n_c)
                method = f"t_{statistic_type}"
            elif t_val is not None and (n_t or n_c):
                # Only total N available — assume equal split
                n_total_approx = (n_t or 0) + (n_c or 0)
                n_half = max(n_total_approx // 2, 1)
                n_rest = n_total_approx - n_half
                smd = metafor_engine.escalc_smd_from_t(t_val, n_half, n_rest)
                if smd is not None:
                    hedges_g_val = smd["g"]
                    effect_variance = smd["vi"]
                    correction = _hedges_correction_factor(n_half, n_rest)
                    cohens_d = hedges_g_val / correction if correction else hedges_g_val
                else:
                    cohens_d = _cohens_d_from_t(t_val, n_half, n_rest)
                method = f"t_{statistic_type}_approx"
            elif (
                M_diff is not None
                and SE_diff is not None
                and SE_diff > 0
                and (n_t or n_c or n_total)
            ):
                # Derive t from unstandardized coefficient b and its SE:  t = b / SE(b)
                # (plain arithmetic, not an escalc function); the resulting t
                # then goes through the same escalc SMD/ti path as above.
                t_from_b = M_diff / SE_diff
                if n_t and n_c:
                    smd = metafor_engine.escalc_smd_from_t(t_from_b, n_t, n_c)
                    if smd is not None:
                        hedges_g_val = smd["g"]
                        effect_variance = smd["vi"]
                        correction = _hedges_correction_factor(n_t, n_c)
                        cohens_d = hedges_g_val / correction if correction else hedges_g_val
                    else:
                        cohens_d = _cohens_d_from_t(t_from_b, n_t, n_c)
                    method = f"t_from_b_se_{statistic_type}"
                elif n_total and n_total > 1:
                    n_half = n_total // 2
                    n_rest = n_total - n_half
                    smd = metafor_engine.escalc_smd_from_t(t_from_b, n_half, n_rest)
                    if smd is not None:
                        hedges_g_val = smd["g"]
                        effect_variance = smd["vi"]
                        correction = _hedges_correction_factor(n_half, n_rest)
                        cohens_d = hedges_g_val / correction if correction else hedges_g_val
                    else:
                        cohens_d = _cohens_d_from_t(t_from_b, n_half, n_rest)
                    method = f"t_from_b_se_approx_{statistic_type}"
                    _extra_notes.append(
                        f"t={t_from_b:.4f} derived from b={M_diff}/SE={SE_diff}; "
                        "n assumed equal split from n_total"
                    )
            elif es_name in {
                "standardized_beta", "beta", "beta_standardized",
                "std_beta", "b_standardized",
            } and es_val is not None:
                # No escalc measure takes a standardised β directly — stays from-scratch.
                cohens_d = _cohens_d_from_beta(es_val)
                method = f"beta_{statistic_type}"
            elif es_name in {
                "r", "correlation", "pearson_r", "point_biserial_r",
            } and es_val is not None:
                # An already-reported r has no raw inputs for escalc's PCOR/COR
                # to recompute from — stays the from-scratch r→d conversion.
                cohens_d = _cohens_d_from_r(es_val)
                method = f"r_{statistic_type}"
            elif es_name in {
                "eta_squared", "partial_eta_squared", "eta2",
            } and es_val is not None:
                cohens_d = _cohens_d_from_eta_squared(es_val)
                method = f"eta_squared_{statistic_type}"
            else:
                exclusion_reason = (
                    f"{statistic_type}: no convertible statistic — "
                    "need t-value for coefficient, b+SE(b), standardised β, r, η², or means+SDs"
                )

        # ── Guard: paper names a ratio measure (OR/RR/HR/Peto OR) but no
        # numeric value/CI was extracted for it ─────────────────────────────
        # Without this, a row like "reported_effect_measure=hazard ratio,
        # hazard_ratio=None" would silently fall through to Priority 5 below
        # and get a Hedges' g reverse-engineered from raw arm proportions --
        # a value that has nothing to do with the paper's actual (adjusted,
        # censored, time-to-event) hazard ratio. Explicitly excluded instead;
        # never guess a different measure than the one the paper itself named.
        elif (
            reported_measure_enum in _NAMED_RATIO_MEASURES
            and odds_ratio is None and risk_ratio is None and hazard_ratio is None
        ):
            exclusion_reason = (
                f"paper reports {reported_measure_enum.value} as its effect measure but no "
                "numeric value/CI was extracted for it; not deriving a different measure "
                "(e.g. from raw proportions) as a substitute"
            )

        # ── Priority 5: two proportions + Ns → OR → d ───────────────────────
        # Universal last resort for any statistic_type when proportion means are
        # present but SDs are missing (binary / dichotomous outcomes).
        # Uses the Borenstein (2009) log-odds conversion: d = ln(OR)·√3/π.
        # Deliberately NOT routed through escalc(measure="OR") -- doing so
        # would require reconstructing integer 2x2 cell counts from continuous
        # proportions via rounding, which was checked empirically and found to
        # shift results by up to ~20% for some proportion/N combinations with
        # no compensating accuracy benefit (the paper reports rates, not raw
        # counts, so treating them as exact proportions is the more faithful
        # of the two options).
        elif _looks_like_proportions(m_t, m_c, row) and m_t is not None and m_c is not None and n_t and n_c:
            p_t = _normalise_proportion(m_t)
            p_c = _normalise_proportion(m_c)
            if 0 < p_t < 1 and 0 < p_c < 1 and p_t != p_c:
                or_from_props = (p_t * (1.0 - p_c)) / (p_c * (1.0 - p_t))
                cohens_d = _cohens_d_from_odds_ratio(or_from_props)
                method = "proportions_OR"
                _extra_notes.append(
                    f"d from proportions via OR (p_treatment={p_t:.4f}, p_control={p_c:.4f}, "
                    f"OR={or_from_props:.4f}); assumes binary outcome"
                )
            else:
                exclusion_reason = (
                    "proportions out of valid range or equal — cannot compute OR"
                )

        # ── Priority 6: descriptive only with no usable data ────────────────
        elif _norm_text(row.get("comparison_type") or "") == "descriptive_only":
            exclusion_reason = (
                "descriptive_only: no means+SDs, no proportions, or insufficient data"
            )

        else:
            exclusion_reason = "unsupported or insufficient statistic type"

        # conversion_method may already be set explicitly (means/SDs, median/
        # IQR); for the remaining branches (t-test, ANOVA, regression,
        # proportions) it's identical to the existing `method` label -- reuse
        # it rather than duplicating a conversion_method= assignment at every
        # one of those call sites.
        # ── Fallback (config.DIFF_FALLBACK, off by default): a reported
        # between-arm difference with its SE -- whatever statistic_type the
        # row was labelled (ANOVA/ANCOVA/t-test/other) -- is converted the
        # same way as the regression b/SE(b) path above, but only for rows
        # that would otherwise be excluded, so included rows never change.
        import config as _cfg
        if (getattr(_cfg, "DIFF_FALLBACK", False) and exclusion_reason
                and M_diff is not None and SE_diff is not None and SE_diff > 0
                and ((n_t and n_c) or (n_total and n_total > 1))):
            t_from_diff = M_diff / SE_diff
            _nt, _nc = (n_t, n_c) if (n_t and n_c) else (n_total // 2, n_total - n_total // 2)
            smd = metafor_engine.escalc_smd_from_t(t_from_diff, _nt, _nc)
            if smd is not None:
                hedges_g_val = smd["g"]
                effect_variance = smd["vi"]
                correction = _hedges_correction_factor(_nt, _nc)
                cohens_d = hedges_g_val / correction if correction else hedges_g_val
            else:
                cohens_d = _cohens_d_from_t(t_from_diff, _nt, _nc)
            _extra_notes.append(
                f"difference fallback: t={t_from_diff:.4f} from M_diff={M_diff}/SE_diff={SE_diff} "
                f"(row was excluded as: {exclusion_reason})"
            )
            method = "t_from_diff_se_fallback"
            conversion_method = None
            exclusion_reason = None

        if conversion_method is None:
            conversion_method = method

        # ── Finalise cohens_d → hedges_g ────────────────────────────────────
        # hedges_g_val (and effect_variance) may already be set directly from
        # an escalc() call above; only fall back to the from-scratch
        # correction formula when that didn't happen.
        if exclusion_reason is None:
            if cohens_d is not None:
                if hedges_g_val is None:
                    hedges_g_val = _hedges_g(cohens_d, n_t, n_c) if (n_t and n_c) else cohens_d
                if hedges_g_val is not None:
                    effect_size_ready = True
                    # cohens_d/hedges_g ALWAYS keep the raw (treatment - control)/SD sign --
                    # the same convention Cochrane/RevMan itself reports, so this number is
                    # directly comparable to a published forest plot cell. plan.higher_score_is_worse
                    # is NEVER applied here (previously it flipped the sign for a lower-is-better
                    # outcome like ECBI); it's used only downstream, in
                    # agents/effect_size_agent.py/meta_analysis_agent.py, to compute the separate
                    # favors_treatment field -- see utils/effect_measures.py::determine_favors_treatment().
                    cohens_d     = round(cohens_d, 6)
                    hedges_g_val = round(hedges_g_val, 6)
                else:
                    exclusion_reason = "could not compute Hedges' g"
            else:
                exclusion_reason = "insufficient numeric information"

    # ── Include/Exclude and Comment ─────────────────────────────────────────
    # A row the classifier explicitly marked meta_analysis_candidate=False
    # (agents/cross_paper_outcome_mapper_agent.py -- "this doesn't answer
    # the user's meta-analysis question", e.g. wrong outcome or wrong
    # follow-up timepoint) must never be pooled just because it happens to
    # be numerically computable. Root cause this fixes (the CD008754
    # Chiaravalloti 2005 investigation): meta_analysis_candidate was
    # computed and recorded by the mapper -- correctly, in that
    # investigation's case -- but nothing downstream ever consulted it, so
    # a row already flagged as ineligible could still be marked "Include"
    # here purely because effect_size_ready came out True. This override is
    # checked LAST and never touches the numeric-computation logic above.
    if row.get("meta_analysis_candidate", True) is False:
        include_exclude = "Exclude"
        if exclusion_reason is None:
            exclusion_reason = (
                "excluded by outcome classification: does not match the requested "
                "outcome/timepoint (meta_analysis_candidate=False)"
            )
    else:
        include_exclude = "Include" if effect_size_ready else "Exclude"

    comment = row.get("extraction_warning") or row.get("comment") or ""
    if row.get("_arm_orientation_corrected"):
        comment = f"{comment}; {row['_arm_orientation_corrected']}".lstrip("; ")
    if exclusion_reason and include_exclude == "Exclude":
        comment = f"{comment}; {exclusion_reason}".lstrip("; ")
    for note in _extra_notes:
        comment = f"{comment}; {note}".lstrip("; ")

    # ── N consistency checks (deterministic, catch LLM errors) ──────────────
    df1_val = _safe_int(row.get("df1"))
    df2_val = _safe_int(row.get("df2"))
    is_two_group = statistic_type == "t_test" or (
        statistic_type == "anova" and (df1_val is None or df1_val == 1)
    )
    is_multi_group = statistic_type == "anova" and df1_val is not None and df1_val > 1

    if is_two_group and n_t and n_c:
        # 2-group: n1 + n2 must equal n_total
        n_sum = n_t + n_c
        if n_total and abs(n_sum - n_total) > 2:
            comment = (
                f"{comment}; N-INCONSISTENCY: n_control({n_c}) + n_treatment({n_t}) = {n_sum} "
                f"≠ n_total({n_total}) — verify per-group Ns"
            ).lstrip("; ")
        # t-test: df = n1 + n2 - 2
        if statistic_type == "t_test" and df1_val is not None:
            expected_df = n_t + n_c - 2
            if abs(expected_df - df1_val) > 1:
                comment = (
                    f"{comment}; N-DF MISMATCH: n_control({n_c}) + n_treatment({n_t}) − 2 = {expected_df} "
                    f"but reported df={df1_val} — check which N is correct"
                ).lstrip("; ")

    if is_multi_group:
        # Multi-group ANOVA: different checks apply
        # 1. df-based total N: n_total = df1 + df2 + 1  (since df1=k-1, df2=N-k)
        if df2_val is not None and n_total:
            n_from_df = df1_val + df2_val + 1
            if abs(n_from_df - n_total) > 2:
                comment = (
                    f"{comment}; N-DF MISMATCH (ANOVA): df1({df1_val}) + df2({df2_val}) + 1 = {n_from_df} "
                    f"≠ n_total({n_total}) — verify total sample size"
                ).lstrip("; ")
        # 2. additional_group_ns sum must equal n_total
        add_ns_str = row.get("additional_group_ns") or ""
        if add_ns_str and n_total:
            parsed_sum = _sum_additional_group_ns(add_ns_str)
            if parsed_sum is not None and abs(parsed_sum - n_total) > 2:
                comment = (
                    f"{comment}; N-INCONSISTENCY (multi-group): sum of additional_group_ns = {parsed_sum} "
                    f"≠ n_total({n_total}) — verify all group Ns"
                ).lstrip("; ")
        # 3. Sanity: per-group Ns must not exceed n_total
        for grp_n, label in [(n_t, "n_treatment"), (n_c, "n_control")]:
            if grp_n and n_total and grp_n >= n_total:
                comment = (
                    f"{comment}; N-SANITY: {label}({grp_n}) ≥ n_total({n_total}) — "
                    "likely the total N was incorrectly placed in a per-group field"
                ).lstrip("; ")

    # ── Build the output dict ────────────────────────────────────────────────
    # All extracted stat columns are always written — even for excluded rows —
    # so the raw data is preserved for manual review and potential re-analysis.
    # Only cohens_d and hedges_g are blanked for excluded rows because those
    # are computed values that cannot be trusted when the row is excluded.
    def _ef(val):
        """Blank cohens_d / hedges_g for excluded rows; pass through otherwise."""
        if not effect_size_ready:
            return ""
        return val if val is not None else ""

    def _n(val):
        """Pass through numeric value as-is (empty string if None)."""
        return val if val is not None else ""

    return {
        # ── Metadata ────────────────────────────────────────────────────────
        "Study_ID": _v(row.get("paper_id")),
        "study_label": _v(row.get("study_label")),
        "Report_ID": _v(row.get("comparison_label") or row.get("outcome_name")),
        "Title": _v(row.get("paper_title")),
        "Author": _v(row.get("author")),
        "Publication Year": _v(row.get("publication_year")),
        "Comment": comment,
        "Design Type": _v(row.get("design_type")),
        "Include/Exclude": include_exclude,
        "Publication Status": _v(row.get("publication_status")),
        "domain": _v(row.get("domain")),
        "Study Environment": _v(row.get("study_environment")),
        "Country": _v(row.get("country")),
        "Study Year": _v(row.get("study_year")),
        "llm_model": _v(row.get("llm_model")),
        "Medium": _v(row.get("medium")),
        "Content length": _v(row.get("content_length")),
        "Topic of Content": _v(row.get("topic_of_content")),
        "interaction_type": _v(row.get("interaction_type")),
        "Comparison type": _v(row.get("comparison_type")),
        "Participant type": _v(row.get("participant_type")),
        "Recruitment source": _v(row.get("recruitment_source")),
        "Outcome type": _v(row.get("outcome_type")),
        "Outcome measurement": _v(row.get("outcome_measurement")),
        "Outcome variable": _v(row.get("outcome_name")),
        "statistic_type": _v(row.get("statistic_type")),
        # ── Raw extracted stats (always present, even for excluded rows) ─────
        "n_total": _n(n_total),
        "n_treatment": _n(n_t),
        "M_treatment": _n(m_t),
        "M_treatment_emm": _n(_safe_float(row.get("group_2_mean_emm"))),
        "M_treatment_perc": _n(_safe_float(row.get("group_2_mean_perc"))),
        "CI_Level": _n(_safe_float(row.get("ci_level"))),
        "CI_lower_treatment": _n(_safe_float(row.get("group_2_ci_lower"))),
        "CI_upper_treatment": _n(_safe_float(row.get("group_2_ci_upper"))),
        "SE_treatment": _n(_safe_float(row.get("group_2_se"))),
        "SD_treatment": _n(sd_t),
        "n_control": _n(n_c),
        "M_control": _n(m_c),
        "M_control_emm": _n(_safe_float(row.get("group_1_mean_emm"))),
        "M_control_perc": _n(_safe_float(row.get("group_1_mean_perc"))),
        "CI_lower_control": _n(_safe_float(row.get("group_1_ci_lower"))),
        "CI_upper_control": _n(_safe_float(row.get("group_1_ci_upper"))),
        "t_value": _n(t_val),
        "df": _n(_safe_float(row.get("df1"))),
        "SE_control": _n(_safe_float(row.get("group_1_se"))),
        "SD_control": _n(sd_c),
        "F_value": _n(f_val),
        "odds_ratio": _n(odds_ratio),
        "CI_lower_or": _n(ci_lower_or),
        "CI_upper_or": _n(ci_upper_or),
        "P_value": _n(_safe_float(row.get("p_value")) if row.get("p_value") is not None else None),
        # ── Computed effect sizes (blank for excluded rows) ──────────────────
        "cohens_d": _ef(cohens_d),
        "hedges_g": _ef(hedges_g_val),
        # Not one of the 54 GT columns (see convert_paper_results()'s CSV
        # writer, extrasaction="ignore") -- JSON-only, read directly by
        # agents/effect_size_agent.py in preference to its own fallback
        # variance formula, when escalc() supplied it above.
        "effect_variance": _ef(effect_variance),
        "M_diff": _n(M_diff),
        "SE_diff": _n(SE_diff),
        "additional_group_ns": _v(row.get("additional_group_ns")),
        # JSON-only, same convention as effect_variance above -- not part of
        # the fixed 54-column GT schema. Populated by
        # cross_paper_outcome_mapper_agent (mapping_node) when present;
        # read by agents/effect_size_agent.py to build outcome_group_key
        # (utils/outcome_grouping.py) so meta_analysis_node can pool each
        # distinct outcome construct/timepoint separately instead of
        # collapsing every included row into one undifferentiated model.
        "outcome_family": _v(row.get("outcome_family")),
        "follow_up_timepoint": _v(row.get("follow_up_timepoint")),
        # JSON-only, same convention as outcome_family/follow_up_timepoint
        # above -- populated by cross_paper_outcome_mapper_agent (mapping_node)
        # when present; read by agents/effect_size_agent.py onto
        # EffectSizeRecord.comparison_family/effect_direction/unit_of_analysis.
        # See utils/outcome_grouping.py (comparison_family splits pooling
        # groups) and agents/meta_analysis_agent.py (direction/unit-of-
        # analysis are validation-only, never used to auto-correct a row).
        "comparison_family": _v(row.get("comparison_family")),
        "effect_direction": _v(row.get("effect_direction")),
        "unit_of_analysis": _v(row.get("unit_of_analysis")),
        # ── Native effect-measure inputs/evidence -- JSON-only, same
        # convention as effect_variance/outcome_family above (not part of
        # the fixed 54-column GT schema). Read by
        # agents/effect_size_agent.py to populate EffectSizeRecord's
        # reported_effect_measure/outcome_units/raw_measure_inputs, which
        # utils/effect_measures.py then uses to resolve and (re)compute
        # each outcome group's pooled effect on its native scale instead of
        # always collapsing to Hedges' g. ──────────────────────────────────
        "reported_effect_measure": _v(reported_effect_measure),
        "outcome_units": _v(outcome_units),
        "outcome_scale_min": _n(outcome_scale_min),
        "outcome_scale_max": _n(outcome_scale_max),
        # JSON-only audit trail for the unit conversion applied above (if
        # any) -- outcome_units already reflects the canonical unit and
        # M_treatment/SD_treatment/M_control/SD_control already reflect the
        # converted values; these two fields exist only so a reviewer can
        # see what was converted from what, not for any further computation.
        "outcome_units_original": _v(outcome_units_original),
        "outcome_unit_conversion_factor": _n(outcome_unit_conversion_factor if outcome_units_original else None),
        "risk_ratio": _n(risk_ratio),
        "CI_lower_rr": _n(ci_lower_rr),
        "CI_upper_rr": _n(ci_upper_rr),
        "hazard_ratio": _n(hazard_ratio),
        "CI_lower_hr": _n(ci_lower_hr),
        "CI_upper_hr": _n(ci_upper_hr),
        "group_1_events": _n(group_1_events),
        "group_1_total": _n(group_1_total),
        "group_2_events": _n(group_2_events),
        "group_2_total": _n(group_2_total),
        # JSON-only, raw median/IQR/range as reported -- preserved for audit
        # even on excluded rows, same convention as group_1_events etc. above.
        "group_1_median": _n(g1_median),
        "group_1_iqr_lower": _n(g1_iqr_lo),
        "group_1_iqr_upper": _n(g1_iqr_hi),
        "group_1_range_lower": _n(g1_range_lo),
        "group_1_range_upper": _n(g1_range_hi),
        "group_2_median": _n(g2_median),
        "group_2_iqr_lower": _n(g2_iqr_lo),
        "group_2_iqr_upper": _n(g2_iqr_hi),
        "group_2_range_lower": _n(g2_range_lo),
        "group_2_range_upper": _n(g2_range_hi),
        # JSON-only -- how cohens_d/hedges_g above were derived, e.g.
        # "means_sds" | "reported_or" | "reported_rr" | "hr_to_d_approx" |
        # "median_iqr_wan2014_approx". Blanked for excluded rows (nothing was
        # computed); read by agents/effect_size_agent.py onto
        # EffectSizeRecord.conversion_method so an exact conversion is never
        # silently indistinguishable from a tagged approximation downstream.
        "conversion_method": _ef(conversion_method),
    }


def _renumber_studies_globally(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Replace per-paper 'Study N' labels with globally unique numbers.

    Within each paper, the per-paper sequence (Study 1, Study 2, …) is already
    correct after _normalize_study_labels.  This step maps each unique
    (paper_id, study_label) pair to a single global counter so that Study 1 of
    Paper A and Study 1 of Paper B become Study 1 and Study 2 in the output.
    Encounter order determines the global number.
    """
    seen: Dict[tuple, str] = {}
    counter = 0
    for row in rows:
        key = (row.get("paper_id", ""), row.get("study_label", ""))
        if key not in seen:
            counter += 1
            seen[key] = f"Study {counter}"
    for row in rows:
        key = (row.get("paper_id", ""), row.get("study_label", ""))
        if key in seen:
            row["study_label"] = seen[key]
    return rows


def convert_paper_results(
    input_path: str,
    output_dir: str,
) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        rows = json.load(f)

    rows = build_pairwise_comparisons(rows)
    rows = _propagate_sample_sizes(rows)
    rows = _normalize_study_labels(rows)
    rows = _renumber_studies_globally(rows)
    rows = _deduplicate_raw(rows)

    converted = [_convert_row(row) for row in rows]

    json_path = os.path.join(output_dir, "meta_ready_results.json")
    csv_path = os.path.join(output_dir, "meta_ready_results.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(converted, f, indent=2, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        # extrasaction="ignore": _convert_row() now also returns
        # "effect_variance" (JSON-only, see there) which isn't one of the
        # 54 GT columns -- drop it here rather than error.
        writer = csv.DictWriter(f, fieldnames=GT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(converted)

    return converted
