"""
Free-text -> EffectMeasure normalization for the PRODUCTION pipeline's own
EffectMeasure enum (models.py).

Deliberately NOT the same function as
cochrane_benchmark/sources/structured/_effect_measure_text.py, even though
the text->measure vocabulary is identical: that module normalizes into
cochrane_benchmark.models.EffectMeasure (an evaluation-only enum), and
production code must not import from the benchmark subpackage (see
utils/effect_measures.py's module docstring). The two enums are kept
independent by design; this is the small, accepted duplication that buys
that independence -- extend both vocabularies together if a new text
variant is confirmed.
"""

from __future__ import annotations

from models import EffectMeasure

EFFECT_MEASURE_TEXT = {
    "risk ratio": EffectMeasure.RR,
    "relative risk": EffectMeasure.RR,
    "rr": EffectMeasure.RR,
    # Rate ratios (incidence-rate ratios, person-time denominators) are
    # conceptually distinct from risk ratios (head-count denominators), but
    # this pipeline has no separate pooling scale for them -- folded into RR
    # as the closest supported approximation (both are ratio measures pooled
    # via generic inverse-variance on the log scale) rather than left
    # unrecognized, which previously caused rows reporting one to be
    # silently misclassified as "no measure stated" and pooled on a fake
    # Hedges' g fallback alongside unrelated outcomes.
    "rate ratio": EffectMeasure.RR,
    "incidence rate ratio": EffectMeasure.RR,
    "irr": EffectMeasure.RR,
    "odds ratio": EffectMeasure.OR,
    "or": EffectMeasure.OR,
    "peto odds ratio": EffectMeasure.PETO_OR,
    "peto or": EffectMeasure.PETO_OR,
    "hazard ratio": EffectMeasure.HR,
    "hazard ratios": EffectMeasure.HR,
    "hr": EffectMeasure.HR,
    "adjusted hazard ratio": EffectMeasure.HR,
    "adjusted hr": EffectMeasure.HR,
    "cox hazard ratio": EffectMeasure.HR,
    "mean difference": EffectMeasure.MD,
    "md": EffectMeasure.MD,
    "std. mean difference": EffectMeasure.SMD,
    "standardized mean difference": EffectMeasure.SMD,
    "standardised mean difference": EffectMeasure.SMD,
    "smd": EffectMeasure.SMD,
    "hedges' g": EffectMeasure.HEDGES_G,
    "hedges g": EffectMeasure.HEDGES_G,
    "risk difference": EffectMeasure.RD,
    "risk differences": EffectMeasure.RD,
    "absolute risk difference": EffectMeasure.RD,
    "rd": EffectMeasure.RD,
}


def normalize_effect_measure_text(text: str) -> EffectMeasure:
    """Exact/near-exact phrase match only -- deliberately conservative (no
    substring/fuzzy matching) since this feeds tier-2 ("explicit paper-
    reported measure") and tier-3 ("methodology prior") evidence in
    resolve_group_effect_measure(); a wrong guess here would silently
    misdirect pooling. Returns UNKNOWN, never raises, when nothing matches."""
    return EFFECT_MEASURE_TEXT.get((text or "").strip().lower(), EffectMeasure.UNKNOWN)
