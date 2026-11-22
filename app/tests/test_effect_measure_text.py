"""utils/effect_measure_text.py -- free-text -> EffectMeasure normalization,
focused on the hazard-ratio and rate-ratio additions (CD008986 root-cause fix:
"hazard ratio" previously normalized to UNKNOWN, making an HR-reporting row
invisible to resolve_group_effect_measure()'s tier-2 evidence collection)."""

from models import EffectMeasure
from utils.effect_measure_text import normalize_effect_measure_text


def test_hazard_ratio_variants_normalize_to_hr():
    for text in [
        "hazard ratio", "Hazard Ratio", "HAZARD RATIO", "HR", "hr",
        "adjusted hazard ratio", "adjusted HR", "cox hazard ratio",
    ]:
        assert normalize_effect_measure_text(text) == EffectMeasure.HR


def test_rate_ratio_variants_normalize_to_rr():
    # Rate ratios have no distinct pooling scale in this pipeline -- folded
    # into RR as the closest supported approximation rather than left
    # unrecognized (see utils/effect_measure_text.py's comment).
    for text in ["rate ratio", "Rate Ratio", "incidence rate ratio", "IRR", "irr"]:
        assert normalize_effect_measure_text(text) == EffectMeasure.RR


def test_existing_measures_still_normalize_correctly():
    assert normalize_effect_measure_text("risk ratio") == EffectMeasure.RR
    assert normalize_effect_measure_text("odds ratio") == EffectMeasure.OR
    assert normalize_effect_measure_text("mean difference") == EffectMeasure.MD
    assert normalize_effect_measure_text("standardized mean difference") == EffectMeasure.SMD
    assert normalize_effect_measure_text("hedges' g") == EffectMeasure.HEDGES_G


def test_unrecognized_text_returns_unknown_never_raises():
    assert normalize_effect_measure_text("some made-up measure") == EffectMeasure.UNKNOWN
    assert normalize_effect_measure_text("") == EffectMeasure.UNKNOWN
    assert normalize_effect_measure_text(None) == EffectMeasure.UNKNOWN


def test_hr_and_or_are_distinct_never_conflated():
    assert normalize_effect_measure_text("hazard ratio") != normalize_effect_measure_text("odds ratio")
    assert normalize_effect_measure_text("hazard ratio") != normalize_effect_measure_text("risk ratio")
