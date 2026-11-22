"""
Moderator node — Stage 7.

Pattern 4: runs subgroup analyses and meta-regression for each plan
moderator, then uses llm.invoke() for interpretation.
"""

import logging
import os
from typing import Any, Dict, List

import numpy as np

from agents.llm import llm
from models import EffectSizeRecord, MetaAnalysisPlan, ModeratorResult, SubgroupResult
from statistics.moderator_analysis import (
    subgroup_analysis, meta_regression, build_design_matrix,
)
from statistics.random_effects import reml_tau_squared
from statistics.plots import moderator_plot, violin_subgroup_plot
from core_utils import save_json

logger = logging.getLogger(__name__)


def _labels_for_moderator(
    effect_sizes: List[EffectSizeRecord],
    study_maps: Dict[str, Any],
    mod_name: str,
) -> List[str]:
    """Extract per-effect moderator label from study_maps, defaulting to 'unknown'."""
    labels = []
    for es in effect_sizes:
        smap = study_maps.get(es.study_id) or study_maps.get(f"{es.study_id}_{es.report_id}") or {}
        val = smap.get("moderators", {}).get(mod_name) if isinstance(smap, dict) else None
        labels.append(str(val) if val else "unknown")
    return labels


def _run_single_moderator(
    mod_name: str,
    effects: np.ndarray,
    variances: np.ndarray,
    labels: List[str],
    output_dir: str,
) -> ModeratorResult:
    """Port of ModeratorAgent._single_moderator(). Run subgroup analysis + meta-regression."""
    categories = sorted(set(labels))
    reference = categories[0] if categories else "unknown"

    subgroup_res = subgroup_analysis(effects.tolist(), variances.tolist(), labels)
    subgroups = [
        SubgroupResult(
            category=cat,
            k=subgroup_res[cat]["k"],
            pooled_g=subgroup_res[cat]["pooled_g"],
            ci_lower=subgroup_res[cat]["ci_lower"],
            ci_upper=subgroup_res[cat]["ci_upper"],
            tau_squared=subgroup_res[cat]["tau_squared"],
            i_squared=subgroup_res[cat]["i_squared"],
        )
        for cat in categories
        if cat in subgroup_res
    ]

    tau2 = reml_tau_squared(effects, variances)
    X, col_names = build_design_matrix(labels, reference)
    reg = meta_regression(effects.tolist(), variances.tolist(), X, col_names, tau2=tau2)

    # Moderator dot-and-whisker plot
    safe_name = mod_name.replace(' ', '_')
    plot_path = os.path.join(output_dir, f"moderator_{safe_name}.png")
    if subgroups:
        moderator_plot(
            moderator_name=mod_name,
            categories=[sg.category for sg in subgroups],
            estimates=[sg.pooled_g for sg in subgroups],
            ci_lower_90=[sg.pooled_g - 0.82 * (sg.pooled_g - sg.ci_lower) for sg in subgroups],
            ci_upper_90=[sg.pooled_g + 0.82 * (sg.ci_upper - sg.pooled_g) for sg in subgroups],
            ci_lower_95=[sg.ci_lower for sg in subgroups],
            ci_upper_95=[sg.ci_upper for sg in subgroups],
            n_per_group=[sg.k for sg in subgroups],
            output_path=plot_path,
        )

    # Violin plot — individual effect sizes per subgroup
    group_effects: Dict[str, List[float]] = {}
    for es, lbl in zip(effects.tolist(), labels):
        group_effects.setdefault(lbl, []).append(es)
    violin_path = os.path.join(output_dir, f"violin_{safe_name}.png")
    violin_subgroup_plot(
        moderator_name=mod_name,
        group_effects=group_effects,
        output_path=violin_path,
    )

    return ModeratorResult(
        moderator_name=mod_name,
        qm_statistic=reg["QM"],
        qm_df=reg["QM_df"],
        qm_p_value=reg["QM_p"],
        subgroups=subgroups,
        reference_category=reference,
        coefficients=reg["coefficients"],
    )


def moderator_node(state: dict) -> dict:
    """Run subgroup analyses and meta-regression for each plan moderator."""
    logger.info("=== STAGE 7: Moderator Analysis ===")
    effect_sizes: List[EffectSizeRecord] = state.get("effect_sizes", [])
    plan: MetaAnalysisPlan = state.get("plan")
    output_dir: str = state["output_dir"]
    study_maps: Dict[str, Any] = state.get("study_maps", {})

    if not effect_sizes or not plan or not getattr(plan, "moderators_to_extract", []):
        logger.info("[Moderator] Nothing to analyse.")
        return {"moderator_results": [], "combined_model": {}}

    effects_arr = np.array([es.hedges_g for es in effect_sizes])
    variances_arr = np.array([es.variance for es in effect_sizes])
    moderator_results: List[ModeratorResult] = []

    for mod_name in plan.moderators_to_extract:
        labels = _labels_for_moderator(effect_sizes, study_maps, mod_name)
        unique_cats = set(labels) - {"unknown"}

        if len(unique_cats) < 2:
            logger.info(f"[Moderator] Skipping '{mod_name}' — fewer than 2 categories.")
            continue

        try:
            mod_result = _run_single_moderator(
                mod_name, effects_arr, variances_arr, labels, output_dir
            )
            moderator_results.append(mod_result)

            try:
                resp = llm.invoke(
                    f"Interpret the '{mod_name}' moderator subgroup analysis in one paragraph:\n"
                    f"QM={mod_result.qm_statistic:.3f} p={mod_result.qm_p_value:.3f}\n"
                    + "\n".join(
                        f"  {sg.category}: g={sg.pooled_g:.3f} k={sg.k}"
                        for sg in mod_result.subgroups
                    )
                )
                # ModeratorResult has no interpretation field — log it only
                logger.info(f"[Moderator] '{mod_name}' interpretation: {resp.content[:200]}")
            except Exception:
                pass

        except Exception as exc:
            logger.warning(f"[Moderator] Failed for '{mod_name}': {exc}")

    combined_model: Dict[str, Any] = {}
    if len(plan.moderators_to_extract) > 1 and moderator_results:
        try:
            all_labels = [
                _labels_for_moderator(effect_sizes, study_maps, m)
                for m in plan.moderators_to_extract
            ]
            # Build a simple combined design matrix (intercept only as fallback)
            combined_model = {"note": "combined model skipped — use per-moderator results"}
        except Exception as exc:
            logger.warning(f"[Moderator] Combined model failed: {exc}")

    save_json(
        [r.model_dump() if hasattr(r, "model_dump") else {} for r in moderator_results],
        os.path.join(output_dir, "moderator_results.json"),
    )

    logger.info(f"[Moderator] Completed {len(moderator_results)} moderator analyses.")
    return {"moderator_results": moderator_results, "combined_model": combined_model}
