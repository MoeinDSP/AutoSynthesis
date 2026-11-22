"""Publication bias assessment: Egger's regression test and trim-and-fill --
computed by R's metafor package (via statistics/metafor_engine.py), not
from-scratch Python implementations."""

from typing import List

from statistics import metafor_engine


def eggers_test(effects: List[float], variances: List[float]) -> dict:
    """
    Egger's regression test for funnel plot asymmetry, via
    metafor::regtest(model="rma", predictor="sei").

    Returns: intercept (limit estimate), SE, test statistic, p-value, and slope.
    """
    return metafor_engine.eggers_test(effects, variances)


def trim_and_fill(
    effects: List[float],
    variances: List[float],
    side: str = "right",
) -> dict:
    """
    Trim-and-fill method via metafor::trimfill() (L₀ estimator by default,
    Duval & Tweedie 2000).

    Returns: k0, adjusted_g, ci_lower, ci_upper, original_g.
    """
    return metafor_engine.trim_and_fill(effects, variances, side=side)
