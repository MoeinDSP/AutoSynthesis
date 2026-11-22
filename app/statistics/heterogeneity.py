"""Heterogeneity statistics: Cochran's Q, I², τ², H², prediction interval --
computed by R's metafor package (via statistics/metafor_engine.py), not
from-scratch Python formulas."""

from typing import List

from statistics import metafor_engine


def compute_all(
    effects: List[float],
    variances: List[float],
    pooled: float = 0.0,
    tau2: float = 0.0,
) -> dict:
    """Compute all heterogeneity statistics via metafor::rma.uni(), which
    fits its own pooled estimate and τ² internally -- `pooled`/`tau2` are
    accepted for call-site backward-compatibility but ignored; metafor's
    own consistent fit is what's actually used."""
    return metafor_engine.heterogeneity(effects, variances)
