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
    method: str = "REML",
) -> dict:
    """Compute all heterogeneity statistics via metafor::rma.uni(), which
    fits its own pooled estimate and τ² internally -- `pooled`/`tau2` are
    accepted for call-site backward-compatibility but ignored; metafor's
    own consistent fit is what's actually used.

    `method` is the pooling model. For a random-effects estimator, tau^2, I^2 and
    the prediction interval use that same estimator. For FE and UWLS, which do not
    estimate tau^2, they are reported from a REML fit so that they still describe
    the between-study variation (Q and its p-value do not depend on the model)."""
    method = metafor_engine.normalize_pooling_model(method)
    het_method = "REML" if method in ("FE", "UWLS") else method
    return metafor_engine.heterogeneity(effects, variances, method=het_method)
