"""
Bias node — Stage 8.

Pattern 4: runs Egger's test and trim-and-fill, generates funnel plot,
then uses llm.invoke() for interpretation.
"""

import logging
import math
import os
from typing import Any, Dict, List

from agents.llm import llm
from models import EffectMeasure, EffectSizeRecord, BiasResult
from statistics.publication_bias import eggers_test, trim_and_fill
from statistics.plots import funnel_plot
from utils.effect_measures import RATIO_MEASURES, measure_label
from core_utils import save_json

logger = logging.getLogger(__name__)


def bias_node(state: dict) -> dict:
    """Assess publication bias via Egger's test, trim-and-fill, and funnel plot."""
    logger.info("=== STAGE 8: Bias Assessment ===")
    effect_sizes: List[EffectSizeRecord] = state.get("effect_sizes", [])
    meta_result = state.get("meta_result")
    output_dir: str = state["output_dir"]

    if len(effect_sizes) < 3:
        logger.info("[Bias] Fewer than 3 effect sizes — skipping.")
        # Still write a fresh (empty) bias_result.json, and remove any stale
        # funnel plot files. output_dir is reused across runs within the
        # same dashboard session (run_service.py keys it off session_id, not
        # run id) -- skipping this write on a genuinely too-small run leaves
        # whatever bias_result.json/funnel_plot.png a PREVIOUS, unrelated run
        # left behind completely untouched, so this run's output silently
        # shows that other run's Egger's test/trim-and-fill numbers as if
        # they were its own. Same root cause and fix pattern as the
        # zero-poolable-effect-sizes carryover already fixed in
        # agents/effect_size_agent.py/agents/meta_analysis_agent.py -- this
        # is the analogous gap in bias_node's own "too few for Egger's test"
        # early return, confirmed live on a real CD010592 k=2 run that still
        # showed a prior k=4 run's eggers_p_value/trim_fill_g.
        save_json({}, os.path.join(output_dir, "bias_result.json"))
        for ext in ("png", "pdf"):
            stale_path = os.path.join(output_dir, f"funnel_plot.{ext}")
            if os.path.exists(stale_path):
                os.remove(stale_path)
        return {"bias_result": None, "bias_funnel_path": "", "bias_interpretation": {}}

    # Egger's test / trim-and-fill keep pooling on Hedges' g (pre-existing
    # behaviour, unchanged here -- out of scope for this fix, which is about
    # the funnel PLOT's display scale only; see effects_list/variances_list
    # below for the separate, measure-aware values the plot itself uses).
    effects_list = [es.hedges_g for es in effect_sizes]
    variances_list = [es.variance for es in effect_sizes]
    pooled_g = meta_result.pooled_g if meta_result else 0.0

    try:
        eggers = eggers_test(effects_list, variances_list)
        tf = trim_and_fill(effects_list, variances_list, side="right")
    except Exception as exc:
        logger.error(f"[Bias] Statistical tests failed: {exc}")
        return {
            "bias_result": None, "bias_funnel_path": "", "bias_interpretation": {},
            "errors": state.get("errors", []) + [str(exc)],
        }

    # --- Restrict to the PRIMARY outcome group's OWN studies before building
    # the funnel plot. state["effect_sizes"] is the FULL, unfiltered list Stage
    # 5 (effect_size_agent.py) produced across EVERY outcome group in this run
    # -- meta_analysis_node never overwrites it (see its own module docstring:
    # "primary" is just an alias for the largest group, meta_result is that
    # one group's .result, not the whole run's). Root cause this closes: a
    # review whose rows split into several outcome groups by effect measure
    # (e.g. CD008986's mortality outcome auto-splitting into separate RR/HR/
    # single-OR pools -- see utils/effect_measures.py's split_reason) would
    # otherwise plot studies from ALL those groups together on one funnel
    # plot -- e.g. 11 RR-scale points mixed with 5 HR-scale and 1 OR-scale
    # point, every one mislabeled as if it were RR -- exactly the "mixed
    # incompatible effect measures" failure this must prevent. state
    # ["meta_results"] (plural) carries every group's own
    # MetaAnalysisGroupResult, study_ids included; match the one whose
    # .result is meta_result to recover which studies actually belong to it. ---
    meta_results = state.get("meta_results") or []
    primary_group = next(
        (g for g in meta_results if meta_result is not None and getattr(g, "result", None) == meta_result),
        None,
    )
    if primary_group is not None and primary_group.study_ids:
        primary_ids = set(primary_group.study_ids)
        funnel_effect_sizes = [es for es in effect_sizes if es.study_id in primary_ids]
    else:
        # No group-membership info available (legacy state, or a run that
        # never populated meta_results) -- degrade to the full list, the
        # pre-existing behaviour for single-outcome-group runs (where "full
        # list" and "primary group's studies" are the same set anyway).
        funnel_effect_sizes = effect_sizes

    # --- Measure-aware inputs for the FUNNEL PLOT itself (distinct from
    # effects_list/pooled_g above) -- root-cause fix for the funnel plot
    # always rendering as if every group were Hedges' g. Each EffectSizeRecord
    # already carries native_value/native_variance (see models.py) on
    # computation_scale's own units -- log scale for RR/OR/PETO_OR/HR,
    # linear for MD/SMD/HEDGES_G/RD -- populated by meta_analysis_agent.py's
    # grouping/pooling step (falls back to hedges_g/variance itself when
    # resolution never ran, e.g. a group pooled before this field existed,
    # so this is additive/backward-compatible, never a behavior change for
    # existing Hedges' g-only data). MetaAnalysisResult has no separate
    # "pooled_log" (that's a transient local var inside
    # agents/meta_analysis_agent.py, never persisted) -- but for a ratio
    # measure, meta_result.pooled_g IS exp(pooled_log) by construction
    # (pool_group_native back-transforms), so math.log() recovers it exactly. ---
    native_effects = [
        es.native_value if es.native_value is not None else es.hedges_g
        for es in funnel_effect_sizes
    ]
    native_variances = [
        es.native_variance if es.native_variance is not None else es.variance
        for es in funnel_effect_sizes
    ]
    computation_scale = meta_result.computation_scale if meta_result else EffectMeasure.HEDGES_G
    effect_measure = meta_result.effect_measure if meta_result else EffectMeasure.UNKNOWN
    is_ratio = computation_scale in RATIO_MEASURES
    # UNKNOWN/GENERIC: no concrete, named native measure was ever resolved --
    # don't fabricate an axis/scale for numbers with no shared unit (per
    # utils/effect_measures.py's own resolution contract, UNKNOWN/GENERIC
    # are expected, non-error outcomes, not bugs to work around here).
    funnel_unavailable = effect_measure in (EffectMeasure.UNKNOWN, EffectMeasure.GENERIC)
    funnel_pooled_value = pooled_g
    if is_ratio:
        if pooled_g > 0:
            funnel_pooled_value = math.log(pooled_g)
        else:
            # A non-positive "ratio" pooled value can't be a real RR/OR/HR --
            # treat as unavailable rather than crash on log() or silently
            # mislabel a broken number as if it were valid.
            funnel_unavailable = True

    funnel_path = ""
    try:
        funnel_path = funnel_plot(
            effects=native_effects if not funnel_unavailable else [],
            variances=native_variances if not funnel_unavailable else [],
            pooled_g=funnel_pooled_value,
            title="Funnel Plot",
            output_path=os.path.join(output_dir, "funnel_plot.png"),
            measure_label=measure_label(computation_scale),
            log_scale=is_ratio,
            unavailable=funnel_unavailable,
        )
    except Exception as exc:
        logger.warning(f"[Bias] Funnel plot failed: {exc}")

    eggers_p = eggers.get("p_value", 1.0)
    tf_k0 = tf.get("k0", 0)
    if eggers_p < 0.05 or tf_k0 > 2:
        bias_risk = "high"
    elif eggers_p < 0.10 or tf_k0 > 0:
        bias_risk = "moderate"
    else:
        bias_risk = "low"

    bias_result = BiasResult(
        eggers_intercept=eggers.get("intercept", 0.0),
        eggers_se=eggers.get("se", 0.0),
        eggers_t_value=eggers.get("t_value", 0.0),
        eggers_p_value=eggers_p,
        trim_fill_k0=tf_k0,
        trim_fill_side=tf.get("side", "right"),
        trim_fill_g=tf.get("adjusted_g", 0.0),
        trim_fill_ci_lower=tf.get("adjusted_ci_lower", 0.0),
        trim_fill_ci_upper=tf.get("adjusted_ci_upper", 0.0),
        bias_risk=bias_risk,
    )

    interpretation: Dict[str, str] = {}
    try:
        resp = llm.invoke(
            f"Interpret this publication bias assessment in 2-3 sentences:\n"
            f"Egger's test p={eggers_p:.4f}, trim-and-fill k0={tf_k0}, risk={bias_risk}."
        )
        interpretation["overall"] = resp.content
    except Exception as exc:
        logger.warning(f"[Bias] LLM interpretation failed: {exc}")

    save_json(
        bias_result.model_dump() if hasattr(bias_result, "model_dump") else {},
        os.path.join(output_dir, "bias_result.json"),
    )

    logger.info(f"[Bias] Risk={bias_risk} Egger's p={eggers_p:.4f} k0={tf_k0}")
    return {
        "bias_result":         bias_result,
        "bias_funnel_path":    funnel_path,
        "bias_interpretation": interpretation,
    }
