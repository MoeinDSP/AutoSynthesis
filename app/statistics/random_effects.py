"""Random-effects meta-analysis pooling -- computed by R's metafor package
(via statistics/metafor_engine.py), not a from-scratch Python estimator."""

from typing import List

from statistics import metafor_engine


def dersimonian_laird(effects: List[float], variances: List[float]) -> float:
    """DerSimonian-Laird estimate of between-study variance τ², via metafor::rma.uni(method="DL")."""
    return metafor_engine.tau_squared(effects, variances, method="DL")


def reml_tau_squared(effects: List[float], variances: List[float]) -> float:
    """Restricted Maximum Likelihood (REML) estimate of τ², via metafor::rma.uni(method="REML")."""
    return metafor_engine.tau_squared(effects, variances, method="REML")


def random_effects_model(
    effects: List[float],
    variances: List[float],
    method: str = "REML",
) -> dict:
    """
    Fit a random-effects meta-analysis model via metafor::rma.uni().

    Parameters
    ----------
    effects   : list of Hedges' g values
    variances : list of corresponding sampling variances
    method    : 'REML' (default) or 'DL'

    Returns
    -------
    dict with: pooled_g, pooled_se, ci_lower, ci_upper, z_value, p_value,
               tau_squared, tau, weights, method
    """
    return metafor_engine.pool(effects, variances, method=method)
