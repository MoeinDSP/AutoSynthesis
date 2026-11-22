"""Subgroup analyses and meta-regression for moderator effects -- computed
by R's metafor package (via statistics/metafor_engine.py), not from-scratch
Python WLS. build_design_matrix() is pure data-shaping (dummy-coding), not a
statistical estimate, so it stays plain Python."""

import numpy as np
from typing import Dict, List, Optional

from statistics import metafor_engine


def subgroup_analysis(
    effects: List[float],
    variances: List[float],
    group_labels: List[str],
) -> Dict[str, dict]:
    """
    Stratified random-effects analysis per group, via metafor per subgroup.

    Returns per-group pooled estimates and heterogeneity stats.
    """
    return metafor_engine.subgroup(effects, variances, group_labels)


def meta_regression(
    effects: List[float],
    variances: List[float],
    design_matrix: np.ndarray,
    column_names: List[str],
    tau2: Optional[float] = None,
) -> dict:
    """
    Meta-regression via metafor::rma.uni(mods=<design matrix>).

    design_matrix : (k × p) array including intercept column
    column_names  : names for each column (including 'intercept')
    tau2          : accepted for call-site backward-compatibility, but
                     ignored -- metafor estimates τ² jointly with the
                     moderator model rather than using a pre-computed value.

    Returns: coefficients, QM test for model significance, R², residual I².
    """
    return metafor_engine.meta_regression(effects, variances, design_matrix, column_names)


def build_design_matrix(
    group_labels: List[str],
    reference: str,
) -> tuple:
    """
    Build a dummy-coded design matrix for a categorical moderator.

    Returns: (X, column_names) — first column is intercept.
    """
    categories = sorted(set(group_labels))
    non_ref = [c for c in categories if c != reference]
    col_names = ["intercept"] + non_ref

    X = np.zeros((len(group_labels), len(col_names)))
    X[:, 0] = 1.0  # intercept
    for j, cat in enumerate(non_ref, start=1):
        for i, label in enumerate(group_labels):
            if label == cat:
                X[i, j] = 1.0

    return X, col_names
