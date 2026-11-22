"""
Bridge to R's `metafor` package via rpy2.

This is the actual computational engine behind every meta-analysis statistic
in this pipeline: random-effects pooling, heterogeneity (Q/I²/H²/τ²,
prediction interval), subgroup analysis, meta-regression, Egger's test, and
trim-and-fill. `statistics/random_effects.py`, `statistics/heterogeneity.py`,
`statistics/moderator_analysis.py`, and `statistics/publication_bias.py`
delegate their computation here; their public function signatures and
return-dict shapes are unchanged, so nothing downstream (agents, plots,
dashboard) needed to change.

Requires R (>= 4.0) with the `metafor` CRAN package installed, plus the
`rpy2` Python package -- see requirements.txt / Dockerfile.
"""

from __future__ import annotations

import logging
import math
from typing import Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

_metafor = None
_ro = None
_engine_info: Optional[Dict[str, str]] = None


def _r():
    """Lazily import rpy2 and the metafor R package -- avoids a hard rpy2/R
    startup cost for any code path that never actually runs a meta-analysis.
    Logs once, on first real use, so it's directly visible in the pipeline
    log / dashboard that a given run's statistics came from R's metafor
    rather than a from-scratch Python formula.

    rpy2's default conversion rule lives in a contextvars.ContextVar, which
    is set once at module-import time -- but a fresh contextvars.Context
    (which a new threading.Thread gets, and which this pipeline creates
    routinely: one per dashboard run, plus whatever thread LangGraph's own
    executor dispatches each node on) does NOT inherit that. A module-level
    cache of `_metafor`/`_ro` alone is therefore not enough: the first
    thread to call this gets working conversions, every other thread reuses
    the cached objects but not the per-thread context, and fails with
    "Conversion rules for rpy2.robjects appear to be missing" (confirmed by
    reproducing it: works fine called twice in the same thread, breaks on
    the second call from a new thread). Re-activating the default converter
    on every call fixes it -- contextvars.ContextVar.set() is cheap, so
    doing it unconditionally (not just on first import) is the safe choice
    over trying to detect "is this a new thread."
    """
    global _metafor, _ro, _engine_info
    import rpy2.robjects as ro
    from rpy2.robjects import default_converter
    ro.conversion.set_conversion(default_converter)
    _ro = ro
    if _metafor is None:
        from rpy2.robjects.packages import importr
        _metafor = importr("metafor")
        try:
            r_version = ro.r("R.version.string")[0]
            metafor_version = ro.r('as.character(packageVersion("metafor"))')[0]
            _engine_info = {"r_version": r_version, "metafor_version": metafor_version}
            logger.info(
                f"[MetaforEngine] Statistics engine active: {r_version}, "
                f"metafor {metafor_version} (via rpy2) -- pooling, heterogeneity, "
                f"moderator analysis, publication bias, and effect-size conversion "
                f"are computed by R's metafor package, not from-scratch Python."
            )
        except Exception:
            pass
    return _ro, _metafor


def engine_info() -> Optional[Dict[str, str]]:
    """{"r_version": ..., "metafor_version": ...} for the R/metafor session
    actually used by this process -- surfaced in the dashboard UI as
    verifiable proof a given run's statistics came from metafor, not a
    from-scratch Python formula. None if metafor has never actually been
    invoked yet in this process (or its version info couldn't be read)."""
    _r()
    return _engine_info


def _fvec(values):
    ro, _ = _r()
    return ro.FloatVector([float(v) for v in values])


def _is_null(x) -> bool:
    ro, _ = _r()
    return x is ro.NULL or x is None or len(x) == 0


def _scalar(x, default: float = 0.0) -> float:
    """Pull a scalar out of an R vector, tolerating NULL/NA."""
    if _is_null(x):
        return default
    try:
        v = float(x[0])
    except (TypeError, ValueError, IndexError):
        return default
    return default if math.isnan(v) else v


def _r_matrix(design_matrix) -> "object":
    ro, _ = _r()
    X = np.asarray(design_matrix, dtype=float)
    return ro.r.matrix(ro.FloatVector(X.flatten(order="F")), nrow=X.shape[0], ncol=X.shape[1])


def _fit_rma(effects, variances, method: str = "REML", mods=None, intercept: bool = True):
    """Fit metafor::rma.uni() and return the raw R result object."""
    ro, metafor = _r()
    kwargs = {"yi": _fvec(effects), "vi": _fvec(variances), "method": method}
    if mods is not None:
        kwargs["mods"] = _r_matrix(mods)
        kwargs["intercept"] = intercept
    return metafor.rma_uni(**kwargs)


def tau_squared(effects: List[float], variances: List[float], method: str = "REML") -> float:
    """τ² via metafor::rma.uni(method=...) -- replaces the from-scratch
    reml_tau_squared()/dersimonian_laird() iterative estimators."""
    if len(effects) < 2:
        return 0.0
    fit = _fit_rma(effects, variances, method=method)
    return _scalar(fit.rx2("tau2"))


def pool(effects: List[float], variances: List[float], method: str = "REML") -> dict:
    """Random-effects pooling via metafor::rma.uni().

    Same return contract as the old statistics.random_effects.random_effects_model().
    """
    ro, _ = _r()
    fit = _fit_rma(effects, variances, method=method)

    tau2 = _scalar(fit.rx2("tau2"))
    weights_r = ro.r["weights"](fit)
    weights = [float(x) for x in weights_r]

    return {
        "pooled_g": _scalar(fit.rx2("b")),
        "pooled_se": _scalar(fit.rx2("se")),
        "ci_lower": _scalar(fit.rx2("ci.lb")),
        "ci_upper": _scalar(fit.rx2("ci.ub")),
        "z_value": _scalar(fit.rx2("zval")),
        "p_value": _scalar(fit.rx2("pval"), default=1.0),
        "tau_squared": tau2,
        "tau": math.sqrt(max(0.0, tau2)),
        "weights": weights,
        "method": method,
    }


def heterogeneity(effects: List[float], variances: List[float], method: str = "REML") -> dict:
    """Q, I², H², τ², and a proper prediction interval (via metafor's own
    predict(), not an approximation) -- all from the same rma.uni() fit
    metafor uses for pooling.

    Same return contract as the old statistics.heterogeneity.compute_all().
    """
    ro, metafor = _r()
    fit = _fit_rma(effects, variances, method=method)
    k = int(_scalar(fit.rx2("k"), default=len(effects)))

    pi_lower, pi_upper = float("-inf"), float("inf")
    if k >= 3:
        try:
            from rpy2.robjects.packages import importr
            stats_r = importr("stats")
            pred = stats_r.predict(fit)
            pi_lower = _scalar(pred.rx2("pi.lb"), default=float("-inf"))
            pi_upper = _scalar(pred.rx2("pi.ub"), default=float("inf"))
        except Exception:
            pass

    tau2 = _scalar(fit.rx2("tau2"))
    return {
        "q_statistic": round(_scalar(fit.rx2("QE")), 3),
        "q_df": max(0, k - 1),
        "q_p_value": round(_scalar(fit.rx2("QEp"), default=1.0), 4),
        "i_squared": round(_scalar(fit.rx2("I2")), 2),
        "h_squared": round(_scalar(fit.rx2("H2"), default=1.0), 3),
        "tau_squared": round(tau2, 6),
        "tau": round(math.sqrt(max(0.0, tau2)), 4),
        "prediction_interval_lower": round(pi_lower, 4),
        "prediction_interval_upper": round(pi_upper, 4),
        "k": k,
    }


def subgroup(effects: List[float], variances: List[float], group_labels: List[str]) -> Dict[str, dict]:
    """Stratified random-effects analysis per group, via metafor per subgroup.

    Same return contract as the old statistics.moderator_analysis.subgroup_analysis().
    A single-study subgroup (k=1) isn't a meta-analysis -- handled directly
    with a plain normal-CI, not routed through R.
    """
    g = np.asarray(effects, dtype=float)
    v = np.asarray(variances, dtype=float)
    labels = np.asarray(group_labels)

    results: Dict[str, dict] = {}
    for grp in sorted(set(group_labels)):
        mask = labels == grp
        g_sub, v_sub = g[mask], v[mask]
        k_sub = int(np.sum(mask))
        if k_sub == 0:
            continue
        if k_sub == 1:
            pooled_g = float(g_sub[0])
            se = float(np.sqrt(v_sub[0]))
            results[grp] = {
                "k": 1, "pooled_g": pooled_g, "se": se,
                "ci_lower": pooled_g - 1.96 * se, "ci_upper": pooled_g + 1.96 * se,
                "tau_squared": 0.0, "i_squared": 0.0,
            }
            continue

        re = pool(g_sub.tolist(), v_sub.tolist())
        het = heterogeneity(g_sub.tolist(), v_sub.tolist())
        results[grp] = {
            "k": k_sub,
            "pooled_g": round(re["pooled_g"], 4),
            "se": round(re["pooled_se"], 4),
            "ci_lower": round(re["ci_lower"], 4),
            "ci_upper": round(re["ci_upper"], 4),
            "tau_squared": round(re["tau_squared"], 6),
            "i_squared": round(het["i_squared"], 2),
        }
    return results


def meta_regression(
    effects: List[float],
    variances: List[float],
    design_matrix,
    column_names: List[str],
) -> dict:
    """Meta-regression via metafor::rma.uni(mods=<design matrix>, intercept=FALSE)
    -- design_matrix already carries its own intercept column (see
    statistics.moderator_analysis.build_design_matrix()), so metafor is told
    not to add a second one. τ² is estimated jointly with the moderator model
    (the textbook-correct approach), not pre-computed and passed in.

    Same return contract as the old statistics.moderator_analysis.meta_regression(),
    minus the tau2 parameter (metafor estimates its own; accepted for
    backward-compat call sites but ignored).
    """
    fit = _fit_rma(effects, variances, mods=design_matrix, intercept=False, method="REML")

    b = [float(x) for x in fit.rx2("b")]
    se = [float(x) for x in fit.rx2("se")]
    pval = [float(x) for x in fit.rx2("pval")]
    ci_lb = [float(x) for x in fit.rx2("ci.lb")]
    ci_ub = [float(x) for x in fit.rx2("ci.ub")]

    coefficients = []
    for i, name in enumerate(column_names):
        coefficients.append({
            "term": name,
            "estimate": round(b[i], 4),
            "se": round(se[i], 4),
            "ci_lower": round(ci_lb[i], 4),
            "ci_upper": round(ci_ub[i], 4),
            "p_value": round(pval[i], 4),
        })

    qm_df_r = fit.rx2("QMdf")
    qm_df = int(_scalar(qm_df_r)) if not _is_null(qm_df_r) else len(column_names) - 1

    return {
        "coefficients": coefficients,
        "QM": round(_scalar(fit.rx2("QM")), 3),
        "QM_df": qm_df,
        "QM_p": round(_scalar(fit.rx2("QMp"), default=1.0), 4),
        "R2": round(_scalar(fit.rx2("R2")), 2),
        "tau2_residual": round(_scalar(fit.rx2("tau2")), 6),
        "I2_residual": round(_scalar(fit.rx2("I2")), 2),
        "k": int(_scalar(fit.rx2("k"), default=len(effects))),
        "p": len(column_names),
    }


def eggers_test(effects: List[float], variances: List[float]) -> dict:
    """Egger's regression test for funnel plot asymmetry, via
    metafor::regtest(model="rma", predictor="sei") -- the standard,
    citable implementation (Egger et al. 1997 as implemented/extended in
    metafor; see ?regtest). `zval`/`pval` are the actual asymmetry test;
    `est`/`ci.lb`/`ci.ub` are the "limit estimate" (effect at infinite
    precision), reported here as the funnel-plot intercept.

    Same return contract as the old statistics.publication_bias.eggers_test().
    """
    k = len(effects)
    if k < 3:
        return {
            "intercept": 0.0, "se": float("inf"),
            "t_value": 0.0, "p_value": 1.0,
            "slope": 0.0, "note": "Too few studies for Egger's test",
        }

    _, metafor = _r()
    fit = _fit_rma(effects, variances, method="REML")
    reg = metafor.regtest(fit, model="rma", predictor="sei")

    zval = _scalar(reg.rx2("zval"))
    pval = _scalar(reg.rx2("pval"), default=1.0)
    est = _scalar(reg.rx2("est"))
    ci_lb_r, ci_ub_r = reg.rx2("ci.lb"), reg.rx2("ci.ub")
    if not _is_null(ci_lb_r) and not _is_null(ci_ub_r):
        se = (_scalar(ci_ub_r) - _scalar(ci_lb_r)) / (2 * 1.96)
    else:
        se = float("inf")

    slope = 0.0
    try:
        slope = float(reg.rx2("fit").rx2("b")[1])  # 2nd coefficient = "sei" slope
    except Exception:
        pass

    return {
        "intercept": round(est, 4),
        "se": round(se, 4),
        "t_value": round(zval, 3),
        "p_value": round(pval, 4),
        "slope": round(slope, 4),
    }


def escalc_smd_from_means(m1, sd1, n1, m2, sd2, n2) -> Optional[dict]:
    """Hedges' g (bias-corrected) + its sampling variance from group means/SDs,
    via metafor::escalc(measure="SMD"). escalc applies the same Hedges (1981)
    small-sample correction as the pipeline's own bias-correction formula
    (verified numerically identical), so this is a full replacement for the
    from-scratch means-based conversion in utils/paper_results_converter.py.
    Returns {"g": ..., "vi": ...} or None if metafor can't compute it."""
    _, metafor = _r()
    try:
        res = metafor.escalc(
            measure="SMD",
            m1i=_fvec([m1]), sd1i=_fvec([sd1]), n1i=_fvec([n1]),
            m2i=_fvec([m2]), sd2i=_fvec([sd2]), n2i=_fvec([n2]),
        )
    except Exception:
        return None
    g = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(g) or math.isnan(vi):
        return None
    return {"g": g, "vi": vi}


def escalc_smd_from_t(t_value, n1, n2) -> Optional[dict]:
    """Hedges' g + its sampling variance from an independent-samples
    t-statistic, via metafor::escalc(measure="SMD", ti=...). Full replacement
    for the from-scratch t-based conversion (verified numerically identical)."""
    _, metafor = _r()
    try:
        res = metafor.escalc(measure="SMD", ti=_fvec([t_value]), n1i=_fvec([n1]), n2i=_fvec([n2]))
    except Exception:
        return None
    g = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(g) or math.isnan(vi):
        return None
    return {"g": g, "vi": vi}


def escalc_pcor(t_value, n, num_predictors) -> Optional[dict]:
    """Partial correlation + its sampling variance from a regression
    coefficient's t-statistic, via metafor::escalc(measure="PCOR", ti=, ni=,
    mi=) -- the methodologically preferred way to convert a regression
    coefficient into an effect size (Aloe & Becker 2012), used in place of
    treating the coefficient's t-value as if it came from a plain t-test.
    `num_predictors` is the total number of predictors in the model
    (including the focal one) -- when not directly reported, the caller can
    derive it from the model's residual df: num_predictors = n - df - 1.
    Returns {"r": partial_r, "vi": ...} or None if unavailable/invalid
    (e.g. |r| >= 1, which shouldn't happen for valid inputs but is guarded
    against since a caller would otherwise silently divide by zero converting
    r to d downstream)."""
    _, metafor = _r()
    try:
        res = metafor.escalc(measure="PCOR", ti=_fvec([t_value]), ni=_fvec([n]), mi=_fvec([num_predictors]))
    except Exception:
        return None
    r = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(r) or math.isnan(vi) or abs(r) >= 1:
        return None
    return {"r": r, "vi": vi}


def escalc_or_from_counts(a: float, b: float, c: float, d: float) -> Optional[dict]:
    """Log odds ratio + its sampling variance from a 2x2 table, via
    metafor::escalc(measure="OR"). a/b = events/non-events in the treatment
    arm, c/d = events/non-events in the control arm (metafor's own ai/bi/ci/di
    convention). Added for cochrane_benchmark/effect_measures.py, which
    needs native OR/RR/MD pooling (not just the SMD-family conversions the
    main pipeline uses) to compare against Cochrane reviews that pool on
    those scales -- purely additive, no existing caller's behavior changes.
    Returns {"log_or": ..., "vi": ...} (natural-log scale, matching metafor's
    own yi) or None if escalc can't compute it (e.g. a zero cell metafor's
    default continuity correction can't rescue)."""
    _, metafor = _r()
    try:
        res = metafor.escalc(measure="OR", ai=_fvec([a]), bi=_fvec([b]), ci=_fvec([c]), di=_fvec([d]))
    except Exception:
        return None
    yi = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(yi) or math.isnan(vi):
        return None
    return {"log_or": yi, "vi": vi}


def escalc_rr_from_counts(a: float, b: float, c: float, d: float) -> Optional[dict]:
    """Log risk ratio + its sampling variance from a 2x2 table, via
    metafor::escalc(measure="RR"). Same ai/bi/ci/di convention as
    escalc_or_from_counts(). Returns {"log_rr": ..., "vi": ...} or None."""
    _, metafor = _r()
    try:
        res = metafor.escalc(measure="RR", ai=_fvec([a]), bi=_fvec([b]), ci=_fvec([c]), di=_fvec([d]))
    except Exception:
        return None
    yi = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(yi) or math.isnan(vi):
        return None
    return {"log_rr": yi, "vi": vi}


def escalc_rd_from_counts(a: float, b: float, c: float, d: float) -> Optional[dict]:
    """Risk difference (p_treatment - p_control) + its sampling variance from
    a 2x2 table, via metafor::escalc(measure="RD"). Same ai/bi/ci/di
    convention as escalc_or_from_counts() above. Unlike OR/RR/HR, RD is
    already on a LINEAR (not log) scale -- p1-p2 is directly interpretable
    and can be zero or negative, so callers must pool/report it exactly like
    MD (no exp() back-transform), never with pool_log_measure(). This is the
    standard Cochrane Handbook alternative to RR/OR for rare-event or
    zero-cell-heavy dichotomous outcomes, where RD's variance formula
    (p1(1-p1)/n1 + p2(1-p2)/n2) stays well-behaved without a continuity
    correction, unlike a log-ratio measure. Returns {"rd": ..., "vi": ...}
    or None if escalc can't compute it."""
    _, metafor = _r()
    try:
        res = metafor.escalc(measure="RD", ai=_fvec([a]), bi=_fvec([b]), ci=_fvec([c]), di=_fvec([d]))
    except Exception:
        return None
    yi = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(yi) or math.isnan(vi):
        return None
    return {"rd": yi, "vi": vi}


def escalc_md_from_means(m1, sd1, n1, m2, sd2, n2) -> Optional[dict]:
    """RAW (unstandardized) mean difference + its sampling variance, via
    metafor::escalc(measure="MD") -- distinct from escalc_smd_from_means()
    above: MD is on the outcome's own natural units (what Cochrane reviews
    pool when every included study used the same scale/instrument), SMD
    divides by pooled SD to make heterogeneous scales comparable. Returns
    {"md": ..., "vi": ...} or None."""
    _, metafor = _r()
    try:
        res = metafor.escalc(
            measure="MD",
            m1i=_fvec([m1]), sd1i=_fvec([sd1]), n1i=_fvec([n1]),
            m2i=_fvec([m2]), sd2i=_fvec([sd2]), n2i=_fvec([n2]),
        )
    except Exception:
        return None
    yi = _scalar(res.rx2("yi"), default=float("nan"))
    vi = _scalar(res.rx2("vi"), default=float("nan"))
    if math.isnan(yi) or math.isnan(vi):
        return None
    return {"md": yi, "vi": vi}


def pool_log_measure(log_effects: List[float], variances: List[float], method: str = "REML") -> dict:
    """Pool already-log-transformed effects (log OR / log RR) via the same
    rma.uni() pool() uses, then back-transform the pooled estimate + CI to
    the natural (ratio) scale with exp(). Point estimate, CI, and
    significance are all still computed on the log scale internally --
    that's the textbook-correct way to pool ratio measures -- only the
    returned numbers are back-transformed, matching how Cochrane/RevMan
    itself reports pooled ORs and RRs (as ratios, not log-ratios)."""
    raw = pool(log_effects, variances, method=method)
    return {
        **raw,
        "pooled_ratio": math.exp(raw["pooled_g"]),
        "ci_lower_ratio": math.exp(raw["ci_lower"]),
        "ci_upper_ratio": math.exp(raw["ci_upper"]),
    }


def trim_and_fill(effects: List[float], variances: List[float], side: str = "right") -> dict:
    """Trim-and-fill via metafor::trimfill() (Duval & Tweedie 2000, L0
    estimator by default -- the same estimator the old from-scratch
    implementation targeted).

    Same return contract as the old statistics.publication_bias.trim_and_fill().
    """
    _, metafor = _r()
    fit = _fit_rma(effects, variances, method="REML")
    tf = metafor.trimfill(fit, side=side)

    return {
        "k0": int(_scalar(tf.rx2("k0"))),
        "side": side,
        "adjusted_g": round(_scalar(tf.rx2("b")), 4),
        "adjusted_ci_lower": round(_scalar(tf.rx2("ci.lb")), 4),
        "adjusted_ci_upper": round(_scalar(tf.rx2("ci.ub")), 4),
        "original_g": round(_scalar(fit.rx2("b")), 4),
    }
