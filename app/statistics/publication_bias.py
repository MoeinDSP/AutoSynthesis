"""Publication bias / small-study effects: Egger's regression test, Begg's rank
test, trim-and-fill and PET-PEESE -- computed in R (metafor, and lm() for
PET-PEESE) via statistics/metafor_engine.py, not from-scratch Python."""

from typing import List, Optional

from statistics import metafor_engine


def eggers_test(effects: List[float], variances: List[float], method: str = "REML") -> dict:
    """Egger's regression test for funnel plot asymmetry, via
    metafor::regtest(model="rma", predictor="sei").

    Returns: intercept (limit estimate), SE, test statistic, p-value, and slope.
    """
    return metafor_engine.eggers_test(effects, variances, method=metafor_engine._rma_method(method))


def rank_test(effects: List[float], variances: List[float], method: str = "REML") -> dict:
    """Begg & Mazumdar's rank correlation test, via metafor::ranktest()."""
    return metafor_engine.rank_test(effects, variances, method=metafor_engine._rma_method(method))


def trim_and_fill(
    effects: List[float],
    variances: List[float],
    side: Optional[str] = "right",
    method: str = "REML",
) -> dict:
    """
    Trim-and-fill method via metafor::trimfill() (L0 estimator by default,
    Duval & Tweedie 2000). side=None lets metafor pick the side from Egger's test.

    Returns: k0, adjusted_g, ci_lower, ci_upper, original_g.
    """
    return metafor_engine.trim_and_fill(effects, variances, side=side,
                                        method=metafor_engine._rma_method(method))


def pet_peese(effects: List[float], variances: List[float], alpha: float = 0.05) -> dict:
    """PET-PEESE (Stanley & Doucouliagos 2014) as WLS meta-regressions on SE (PET)
    and on the variance (PEESE), with the conditional PET -> PEESE rule."""
    return metafor_engine.pet_peese(effects, variances, alpha=alpha)
