"""
Wan et al. (2014) median/IQR/range -> mean/SD estimation.

Reference: Wan X, Wang W, Liu J, Tong T. "Estimating the sample mean and
standard deviation from the sample size, median, range and/or interquartile
range." BMC Med Res Methodol. 2014;14:135.

Cochrane reviews routinely include trials that report medians instead of
means (common for skewed clinical outcomes -- length of stay, cost, time to
event). Without this, any such row is unusable for a mean-difference-based
meta-analysis no matter how well-reported the paper is. This module converts
a reported median + IQR (or median + range) into an ESTIMATED mean/SD, so
that data can flow through the existing means/SDs -> escalc(SMD/MD) path
unchanged.

This is explicitly an APPROXIMATION, not a substitute for a directly reported
mean/SD -- every caller MUST tag the resulting row's conversion_method as
"median_iqr_wan2014_approx" (or the range variant) so it is never silently
indistinguishable from an exact value downstream (see
utils/paper_results_converter.py, models.EffectSizeRecord.conversion_method).
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

from scipy.stats import norm


def estimate_mean_sd_from_median_iqr(
    median: float, q1: float, q3: float, n: int
) -> Optional[Tuple[float, float]]:
    """Scenario S2 (Wan et al. 2014, eq. 14/15): sample size, median, and
    interquartile range (Q1, Q3) -- e.g. "median 12 days (IQR 8-19)".

    mean ~= (Q1 + 2*median + Q3) / 4   (weights the median twice, more
                                         accurate than the naive (Q1+m+Q3)/3
                                         average for skewed distributions)
    SD   ~= (Q3 - Q1) / (2 * Phi^-1((0.75n - 0.125) / (n + 0.25)))
                                        (size-adjusted normal-quantile
                                         denominator -- converges to the
                                         familiar IQR/1.35 only as n -> inf;
                                         matters for the small trial sizes
                                         typical of Cochrane-included studies)

    Returns None if inputs are invalid (n<2, q3<=q1, or any missing).
    """
    if median is None or q1 is None or q3 is None or n is None:
        return None
    try:
        n = int(n)
    except (TypeError, ValueError):
        return None
    if n < 2 or q3 <= q1:
        return None

    mean_est = (q1 + 2.0 * median + q3) / 4.0
    z = norm.ppf((0.75 * n - 0.125) / (n + 0.25))
    if z <= 0:
        return None
    sd_est = (q3 - q1) / (2.0 * z)
    if sd_est <= 0 or not math.isfinite(sd_est) or not math.isfinite(mean_est):
        return None
    return mean_est, sd_est


def estimate_mean_sd_from_median_range(
    median: float, lo: float, hi: float, n: int
) -> Optional[Tuple[float, float]]:
    """Scenario S1 (Wan et al. 2014, eq. 9/10; refines Hozo et al. 2005):
    sample size, median, and range (min, max) -- e.g. "median 12 days
    (range 5-30)". Used only when IQR is not reported -- range gives a
    coarser SD estimate than IQR, so estimate_mean_sd_from_median_iqr()
    is preferred whenever both are available.

    mean ~= (min + 2*median + max) / 4
    SD   ~= (max - min) / (2 * Phi^-1((n - 0.375) / (n + 0.25)))

    Returns None if inputs are invalid (n<2, hi<=lo, or any missing).
    """
    if median is None or lo is None or hi is None or n is None:
        return None
    try:
        n = int(n)
    except (TypeError, ValueError):
        return None
    if n < 2 or hi <= lo:
        return None

    mean_est = (lo + 2.0 * median + hi) / 4.0
    z = norm.ppf((n - 0.375) / (n + 0.25))
    if z <= 0:
        return None
    sd_est = (hi - lo) / (2.0 * z)
    if sd_est <= 0 or not math.isfinite(sd_est) or not math.isfinite(mean_est):
        return None
    return mean_est, sd_est
