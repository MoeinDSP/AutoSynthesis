"""
Meta-Analysis node — Stage 6.

Pattern 4: pools with the model chosen for the run (plan.pooling_model: fixed
effect, any metafor random-effects estimator, or UWLS; REML random effects by
default -- see statistics/metafor_engine.py), then calls llm.invoke() directly
for interpretation.

Groups effect sizes by outcome_group_key before pooling (see
utils/outcome_grouping.py) instead of pooling every included row from every
paper into one undifferentiated model. Root cause this fixes: earlier stages
(relevance_filter_agent, cross_paper_outcome_mapper_agent) already classify
each row into a distinct construct, but that classification used to be
computed and then discarded before reaching EffectSizeRecord -- see
models.py::EffectSizeRecord and agents/effect_size_agent.py.

Backward compatibility: when every effect size shares the same
outcome_group_key (either because outcome_family was never populated --
legacy runs, or because the review/paper set genuinely reports one outcome),
there is exactly ONE group and this node behaves exactly as before: the same
top-level state keys (meta_result, meta_plots, meta_interpretation), the same
unsuffixed plot filenames, the same meta_analysis_result.json content. Those
keys are always an alias for the "primary" group -- the largest group with
enough studies to pool -- so single-outcome callers need no changes. The new
per-group detail is additionally available under meta_results /
meta_group_plots / meta_group_interpretation.
"""

import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from agents.llm import llm
from models import EffectMeasure, EffectSizeRecord, MetaAnalysisGroupResult, MetaAnalysisResult, ValidationFlag
from statistics.heterogeneity import compute_all as compute_heterogeneity
from statistics import metafor_engine
from statistics.plots import (
    forest_plot, cumulative_forest_plot,
    effect_distribution_plot, bubble_chart,
    heterogeneity_summary_plot,
)
from utils.outcome_grouping import DEFAULT_GROUP_KEY, MIN_K_FOR_POOLING, group_label, safe_filename_fragment
from utils.effect_measures import (
    RATIO_MEASURES, compute_native_row_effect, group_needs_scale_harmonization, measure_label, pool_group_native, resolve_group_effect_measure,
    dichotomous_tie_break, determine_favors_treatment,
)
from utils.effect_measure_text import normalize_effect_measure_text
from core_utils import save_json

logger = logging.getLogger(__name__)


def _pooling_method(plan) -> str:
    """The pooling model for this run: plan.pooling_model (chosen by the user in the
    dashboard or requested in the prompt), else the default, REML random effects."""
    return metafor_engine.normalize_pooling_model(getattr(plan, "pooling_model", None) if plan else None)


def _run_model(values: List[float], variances: List[float], n_total: int, computation_scale: EffectMeasure,
               method: str = "REML") -> dict:
    """Run the chosen pooling model (`method`, see metafor_engine.POOLING_MODELS) on `values`/`variances` (already on
    computation_scale -- log scale for OR/RR/PETO_OR, linear otherwise) and
    return the full stats dict. `pooled_g`/`ci_lower`/`ci_upper` in the
    result are always on the human-interpretable scale (back-transformed
    for ratio measures via pool_group_native); heterogeneity is computed on
    the same scale metafor itself uses internally (log scale for ratios)."""
    k = len(values)
    re = pool_group_native(computation_scale, values, variances, method=method)
    hetero = compute_heterogeneity(values, variances, re["pooled_g"], re["tau_squared"], method=method)
    return {**re, **hetero, "k": k, "n_total": n_total}


def _plot_paths(output_dir: str, suffix: str) -> Dict[str, str]:
    """Legacy (suffix="") filenames stay unsuffixed so any code/tests that
    hardcode e.g. output_dir/forest_plot.png keep working unchanged."""
    tag = f"__{suffix}" if suffix else ""
    return {
        "forest":               os.path.join(output_dir, f"forest_plot{tag}.png"),
        "cumulative":           os.path.join(output_dir, f"cumulative_plot{tag}.png"),
        "distribution":         os.path.join(output_dir, f"effect_distribution{tag}.png"),
        "bubble":               os.path.join(output_dir, f"bubble_chart{tag}.png"),
        "heterogeneity_summary": os.path.join(output_dir, f"heterogeneity_summary{tag}.png"),
    }


def _generate_plots(
    effect_sizes: List[EffectSizeRecord],
    values: List[float],
    variances: List[float],
    computation_scale: EffectMeasure,
    result: MetaAnalysisResult,
    stats: dict,
    output_dir: str,
    plan,
    suffix: str,
    title_prefix: str = "",
) -> Dict[str, str]:
    """Generate the 5 standard plots for one group's pooled result.
    Wraps each in try/except so one failure doesn't abort the others (same
    behaviour as the original single-group implementation). `values`/
    `variances` are on computation_scale (same convention as _run_model) --
    for SMD/HEDGES_G/GENERIC groups these are identical to
    es.hedges_g/es.variance (backward compatible); for MD/OR/RR groups they
    are the native-scale numbers, so plots reflect what was actually pooled."""
    plots: Dict[str, str] = {}
    paths = _plot_paths(output_dir, suffix)
    labels = [f"{es.study_id}_{es.report_id}" for es in effect_sizes]
    effects_list = values
    variances_list = variances
    weights = stats.get("weights", [1.0] * stats["k"])
    title_prefix = f"{title_prefix} — " if title_prefix else ""

    # --- Measure-aware labeling/scale for every plot below -- see
    # utils/effect_measures.py. `label` names the axis/legend text (e.g.
    # "Risk Ratio (RR)"); `log_scale` is True for OR/RR/PETO_OR groups.
    # `values`/`variances` (== effects_list/variances_list) are already on
    # computation_scale (LOG scale for ratio measures, matching what
    # metafor/escalc computed) -- forest_plot/effect_distribution_plot/
    # bubble_chart expect their `pooled_g`/CI inputs in those SAME units so
    # their own display-time exp() transform is consistent, which is why
    # those three read stats["pooled_log"/"ci_lower_log"/"ci_upper_log"]
    # (present only for ratio measures, via pool_group_native) rather than
    # result.pooled_g/ci_lower/ci_upper (already back-transformed to the
    # ratio scale -- correct for cumulative_forest_plot/
    # heterogeneity_summary_plot below, which receive pre-pooled numbers
    # directly and do their own axis-only log transform, not a
    # per-coordinate one). ---
    label = measure_label(computation_scale)
    is_ratio = computation_scale in RATIO_MEASURES
    plot_pooled_g = stats.get("pooled_log", result.pooled_g)
    plot_ci_lower = stats.get("ci_lower_log", result.ci_lower)
    plot_ci_upper = stats.get("ci_upper_log", result.ci_upper)

    # Axis labels must match the RAW (never-flipped) sign plotted above: for a
    # difference-type scale (SMD/HEDGES_G/MD/GENERIC) where plan.higher_score_is_worse is
    # True (e.g. a symptom-severity outcome), a NEGATIVE value is the favourable one, so
    # "Favours {treatment}" belongs on the left, not the right. Ratio measures (is_ratio)
    # are left at the default -- see determine_favors_treatment()'s docstring for why
    # higher_score_is_worse doesn't apply to them.
    treatment_favoured_on_left = (
        not is_ratio and plan and getattr(plan, "higher_score_is_worse", False)
    )
    control_name = plan.control_label if plan else "control"
    treatment_name = plan.treatment_label if plan else "treatment"
    left_label = f"← Favours {treatment_name if treatment_favoured_on_left else control_name}"
    right_label = f"Favours {control_name if treatment_favoured_on_left else treatment_name} →"

    try:
        plots["forest"] = forest_plot(
            study_labels=labels,
            effects=effects_list,
            variances=variances_list,
            pooled_g=plot_pooled_g,
            pooled_ci_lower=plot_ci_lower,
            pooled_ci_upper=plot_ci_upper,
            weights=weights,
            title=f"{title_prefix}Forest Plot",
            left_label=left_label,
            right_label=right_label,
            output_path=paths["forest"],
            measure_label=label,
            log_scale=is_ratio,
        )
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] Forest plot failed ({suffix or 'primary'}): {exc}")

    try:
        cum_g, cum_lo, cum_hi, cum_labels, cum_years = [], [], [], [], []
        for i in range(1, len(effect_sizes) + 1):
            subset_n = sum(es.n_total for es in effect_sizes[:i])
            cum_stats = _run_model(values[:i], variances[:i], subset_n, computation_scale,
                                   method=result.method)
            cum_g.append(cum_stats["pooled_g"])
            cum_lo.append(cum_stats["ci_lower"])
            cum_hi.append(cum_stats["ci_upper"])
            es_i = effect_sizes[i - 1]
            cum_labels.append(f"{es_i.study_id}_{es_i.report_id}")
            cum_years.append(2020)
        plots["cumulative"] = cumulative_forest_plot(
            study_labels=cum_labels,
            cumulative_g=cum_g,
            cumulative_ci_lower=cum_lo,
            cumulative_ci_upper=cum_hi,
            study_years=cum_years,
            final_g=result.pooled_g,
            title=f"{title_prefix}Cumulative Meta-Analysis",
            output_path=paths["cumulative"],
            measure_label=label,
            log_scale=is_ratio,
        )
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] Cumulative plot failed ({suffix or 'primary'}): {exc}")

    try:
        plots["distribution"] = effect_distribution_plot(
            effects=effects_list,
            variances=variances_list,
            pooled_g=plot_pooled_g,
            pooled_ci_lower=plot_ci_lower,
            pooled_ci_upper=plot_ci_upper,
            title=f"{title_prefix}Effect Size Distribution",
            output_path=paths["distribution"],
            measure_label=label,
            log_scale=is_ratio,
        )
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] Distribution plot failed ({suffix or 'primary'}): {exc}")

    try:
        sample_sizes = [es.n_total for es in effect_sizes]
        plots["bubble"] = bubble_chart(
            study_labels=labels,
            effects=effects_list,
            variances=variances_list,
            sample_sizes=sample_sizes,
            pooled_g=plot_pooled_g,
            title=f"{title_prefix}Effect Size vs. Sample Size",
            output_path=paths["bubble"],
            measure_label=label,
            log_scale=is_ratio,
        )
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] Bubble chart failed ({suffix or 'primary'}): {exc}")

    try:
        plots["heterogeneity_summary"] = heterogeneity_summary_plot(
            pooled_g=result.pooled_g,
            pooled_ci_lower=result.ci_lower,
            pooled_ci_upper=result.ci_upper,
            p_value=result.p_value,
            k=result.k,
            n_total=result.n_total,
            q_statistic=result.q_statistic,
            q_df=result.q_df,
            q_p_value=result.q_p_value,
            i_squared=result.i_squared,
            tau_squared=result.tau_squared,
            tau=result.tau,
            h_squared=result.h_squared,
            title=f"{title_prefix}Heterogeneity Summary",
            output_path=paths["heterogeneity_summary"],
            measure_label=label,
        )
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] Heterogeneity summary plot failed ({suffix or 'primary'}): {exc}")

    return plots


def _interpret_group(result: MetaAnalysisResult, label: str, plan=None) -> Optional[str]:
    # The raw pooled_g sign alone is NOT a reliable direction signal for a higher-is-worse
    # outcome (e.g. a symptom-severity scale) -- result.favors_treatment already resolved
    # that correctly (see determine_favors_treatment()), so state it explicitly rather than
    # letting the LLM infer direction from the sign itself, which would be backwards for
    # such outcomes.
    treatment_name = plan.treatment_label if plan else "the treatment"
    control_name = plan.control_label if plan else "control"
    if result.favors_treatment is True:
        direction_note = f"This result favors {treatment_name} over {control_name}."
    elif result.favors_treatment is False:
        direction_note = f"This result favors {control_name} over {treatment_name}."
    else:
        direction_note = (
            "This result is essentially a tie, or direction could not be determined "
            "(e.g. a ratio measure, where favourability depends on which event was counted)."
        )
    try:
        prompt = (
            f"You are a meta-analysis expert. Summarise these results in 3-4 sentences "
            f"suitable for a systematic review paper. This pooled estimate covers the "
            f"outcome group \"{label}\", pooled with the model: "
            f"{metafor_engine.POOLING_MODELS.get(result.method, result.method)}.\n"
            f"  Pooled Hedges' g = {result.pooled_g:.3f}, "
            f"95% CI [{result.ci_lower:.3f}, {result.ci_upper:.3f}], "
            f"p = {result.p_value:.4f}, I² = {result.i_squared:.1f}%, "
            f"τ = {result.tau:.4f}, k = {result.k} studies.\n"
            f"  {direction_note} State direction using this fact, not by inferring it "
            f"yourself from the raw sign of pooled Hedges' g above -- this outcome may be "
            f"scored so that a lower raw value is actually the better outcome.\n"
            f"Focus on effect magnitude, direction, and heterogeneity."
        )
        resp = llm.invoke(prompt)
        return resp.content
    except Exception as exc:
        logger.warning(f"[MetaAnalysis] LLM interpretation failed ({label}): {exc}")
        return None


def _resolve_and_populate_native(
    group_key: str, effect_sizes: List[EffectSizeRecord], plan
) -> Tuple[EffectMeasure, EffectMeasure, str, Optional[str], List[EffectSizeRecord]]:
    """Resolve this group's effect measure (utils/effect_measures.py) and
    populate native_value/native_variance on every row. Returns
    (effect_measure, computation_scale, source, conflict, usable_rows) --
    `usable_rows` is the subset that actually has a valid native_value; for
    SMD/HEDGES_G/GENERIC groups this is always all rows (backward
    compatible). For MD/OR/RR groups, when too few rows carry the raw
    inputs needed to compute the native scale, the WHOLE group falls back
    to HEDGES_G pooling rather than silently mixing scales across rows --
    recorded in the conflict note, never silent."""
    resolution = resolve_group_effect_measure(effect_sizes, plan)
    conflict_notes = [resolution.conflict] if resolution.conflict else []

    harmonize_scale = group_needs_scale_harmonization(effect_sizes)
    if resolution.computation_scale == EffectMeasure.MD and not harmonize_scale:
        with_range = [es.study_id for es in effect_sizes if (es.raw_measure_inputs or {}).get("scale_min") is not None]
        if with_range and len(with_range) < len(effect_sizes):
            conflict_notes.append(
                f"instrument range stated for only {len(with_range)}/{len(effect_sizes)} row(s) -- "
                "no 0-100 rescaling applied (MD pooled in the papers' raw units)"
            )

    for es in effect_sizes:
        value, variance = compute_native_row_effect(
            resolution.computation_scale, es.raw_measure_inputs, es.hedges_g, es.variance,
            harmonize_scale=harmonize_scale,
        )
        es.effect_measure = resolution.effect_measure
        es.computation_scale = resolution.computation_scale
        es.native_value = value
        es.native_variance = variance

    usable = [es for es in effect_sizes if es.native_value is not None and es.native_variance not in (None, 0)]
    usable_ids = {id(es) for es in usable}
    computation_scale = resolution.computation_scale
    source = resolution.source

    if computation_scale not in (EffectMeasure.SMD, EffectMeasure.HEDGES_G, EffectMeasure.GENERIC):
        if len(usable) < MIN_K_FOR_POOLING <= len(effect_sizes):
            excluded = [es.study_id for es in effect_sizes if id(es) not in usable_ids]
            conflict_notes.append(
                f"only {len(usable)}/{len(effect_sizes)} row(s) had raw inputs for {computation_scale.value} "
                f"(missing: {excluded}) -- falling back to Hedges' g pooling for the whole group"
            )
            computation_scale = EffectMeasure.HEDGES_G
            # effect_measure is DELIBERATELY left as resolution.effect_measure
            # (e.g. "HR") rather than reset to UNKNOWN here -- this is what
            # lets agents/report_agent.py's deterministic Effect Measure
            # Summary table distinguish "never resolved to anything" (UNKNOWN
            # from the start) from "we knew HR was intended but too few rows
            # had raw inputs to compute it natively" (this branch), producing
            # the more informative "<measure> intended, but not computable
            # natively for enough studies" message instead of a generic
            # "not confirmed" one. See _build_effect_measure_summary()'s
            # g.effect_measure == UNKNOWN branch -- effect_measure and
            # computation_scale intentionally diverging here is not a bug.
            for es in effect_sizes:
                es.computation_scale = computation_scale
                es.native_value = es.hedges_g
                es.native_variance = es.variance
            usable = list(effect_sizes)
            source = "unresolved_fallback"
        elif len(usable) < len(effect_sizes):
            excluded = [es.study_id for es in effect_sizes if id(es) not in usable_ids]
            conflict_notes.append(
                f"{len(effect_sizes) - len(usable)} row(s) excluded from native {computation_scale.value} "
                f"pooling for lacking raw inputs: {excluded}"
            )

    return resolution.effect_measure, computation_scale, source, ("; ".join(conflict_notes) or None), usable


def _partition_by_row_measure(
    rows: List[EffectSizeRecord],
) -> List[Tuple[str, List[EffectSizeRecord], Optional[str]]]:
    """Split rows sharing one outcome_group_key into sub-buckets when their
    OWN reported_effect_measure resolves (via normalize_effect_measure_text)
    to two-or-more DIFFERENT non-UNKNOWN EffectMeasure values.

    Without this, resolve_group_effect_measure()'s majority vote picks ONE
    measure for the whole group and pools every row on it regardless of what
    a minority of rows actually reported -- e.g. HR-reporting rows and OR-
    reporting rows silently pooled together on a Hedges' g fallback (see the
    CD008986 investigation this fixes). Rows with no explicit
    reported_effect_measure at all ("UNKNOWN") carry no conflicting evidence,
    so they join the largest explicit sub-bucket -- the same majority-vote
    convention resolve_group_effect_measure() already uses for ambiguous rows.

    Returns a list of (key_suffix, sub_rows, split_reason) tuples. When 0 or
    1 distinct explicit measure is present, returns a single tuple with
    key_suffix="" and split_reason=None -- identical to pre-partition
    behavior (the existing resolver already handles that case correctly)."""
    by_measure: Dict[EffectMeasure, List[EffectSizeRecord]] = defaultdict(list)
    unknown_rows: List[EffectSizeRecord] = []
    for es in rows:
        m = normalize_effect_measure_text(es.reported_effect_measure)
        (unknown_rows if m == EffectMeasure.UNKNOWN else by_measure[m]).append(es)

    if len(by_measure) < 2:
        return [("", rows, None)]

    # Which bucket the UNKNOWN (unlabeled) rows join: normally whichever
    # explicit measure has the most support, but on a genuine tie between
    # measures that are real dichotomous alternatives (RR/OR/Peto OR),
    # prefer Cochrane's own convention over arbitrary iteration order -- a
    # tie-breaker only, and only within that family (a tie involving HR is
    # left unresolved rather than forced toward RR -- see
    # utils.effect_measures.dichotomous_tie_break()).
    max_support = max(len(v) for v in by_measure.values())
    tied_leaders = dichotomous_tie_break([m for m in by_measure if len(by_measure[m]) == max_support])
    largest_measure = tied_leaders[0]

    # Second CD008986 regression this also fixes: an UNKNOWN row can NEVER
    # be pooled as HR -- hazard ratios have no counts-reconstruction path at
    # all (utils.effect_measures.compute_native_row_effect skips straight to
    # the already-reported-ratio fallback for HR, which these rows by
    # definition don't have). If the plurality winner above is HR but a
    # genuine dichotomous alternative (RR/OR/Peto OR) is ALSO present,
    # reroute individual unlabeled rows there IFF that specific row actually
    # has usable raw inputs for it (the same raw event-count table --
    # events/n for both arms -- that left it unclassified is exactly what
    # escalc_rr_from_counts/escalc_or_from_counts needs). This is a
    # feasibility check, not a stylistic RR-preference override: an
    # unlabeled row with no usable dichotomous inputs either (e.g. it only
    # ever had a pre-computed Hedges' g, no raw counts) is left exactly
    # where the majority-vote rule already put it, preserving the existing
    # "never force toward RR just because it's tie-preferred" guarantee
    # (see test_unlabeled_rows_do_not_force_rr_over_a_real_hr_majority) --
    # this only rescues rows that would otherwise be silent, avoidable dead
    # weight in a bucket that can structurally never use them.
    rerouted_unknown: List[EffectSizeRecord] = []
    reroute_target: Optional[EffectMeasure] = None
    if largest_measure == EffectMeasure.HR and unknown_rows:
        dichotomous_present = [m for m in by_measure if m in RATIO_MEASURES and m != EffectMeasure.HR]
        if dichotomous_present:
            reroute_target = dichotomous_tie_break(
                sorted(dichotomous_present, key=lambda m: -len(by_measure[m]))
            )[0]
            still_unknown: List[EffectSizeRecord] = []
            for es in unknown_rows:
                value, _ = compute_native_row_effect(
                    reroute_target, es.raw_measure_inputs, es.hedges_g, es.variance
                )
                (rerouted_unknown if value is not None else still_unknown).append(es)
            unknown_rows = still_unknown

    measure_names = sorted(m.value for m in by_measure)
    reason = (
        f"rows in this outcome group report incompatible effect measures ({', '.join(measure_names)}); "
        "auto-split and pooled separately rather than mixed on a common fallback scale"
    )
    buckets: List[Tuple[str, List[EffectSizeRecord], Optional[str]]] = []
    for m, m_rows in by_measure.items():
        sub_rows = list(m_rows)
        if m == largest_measure:
            sub_rows += unknown_rows
        if m == reroute_target:
            sub_rows += rerouted_unknown
        buckets.append((f"::measure={m.value}", sub_rows, reason))
    return buckets


def _dedupe_same_trial_rows(
    group_key: str, effect_sizes: List[EffectSizeRecord], validation_flags: List[ValidationFlag]
) -> List[EffectSizeRecord]:
    """When two-or-more rows in this group share a trial_cluster_id (see
    utils/trial_matching.py -- different PAPERS describing the SAME trial),
    keep only the one with the largest n_total and drop the rest from THIS
    group's pooling, so one trial's data is never counted twice within a
    single outcome. The dropped paper's OTHER, non-overlapping outcomes
    (different outcome_group_key) are entirely unaffected -- this only acts
    within one group. Always recorded via ValidationFlag, never silent."""
    by_cluster: Dict[str, List[EffectSizeRecord]] = defaultdict(list)
    unclustered: List[EffectSizeRecord] = []
    for es in effect_sizes:
        (by_cluster[es.trial_cluster_id] if es.trial_cluster_id else unclustered).append(es)

    kept = list(unclustered)
    for cluster_id, rows in by_cluster.items():
        if len(rows) < 2:
            kept.extend(rows)
            continue
        rows_sorted = sorted(rows, key=lambda es: es.n_total, reverse=True)
        primary, dropped = rows_sorted[0], rows_sorted[1:]
        kept.append(primary)
        dropped_ids = [es.study_id for es in dropped]
        logger.info(
            f"[MetaAnalysis] Group '{group_key}': trial cluster {cluster_id} -- keeping "
            f"{primary.study_id} (n_total={primary.n_total}), excluding {dropped_ids} from this group "
            "to avoid double-counting the same trial."
        )
        validation_flags.append(ValidationFlag(
            stage="trial_dedup", severity="warning", subject_id=group_key,
            message=f"Trial cluster {cluster_id}: kept {primary.study_id} (largest n_total) for this "
                    f"outcome group, excluded {dropped_ids} as duplicate reports of the same trial.",
            auto_action="excluded_row",
        ))
    return kept


def _build_group(
    group_key: str,
    effect_sizes: List[EffectSizeRecord],
    output_dir: str,
    plan,
    is_primary: bool,
    split_reason: Optional[str] = None,
    validation_flags: Optional[List[ValidationFlag]] = None,
) -> Tuple[MetaAnalysisGroupResult, Dict[str, str], Optional[str]]:
    """Build one group's pooled result (or an insufficient-data placeholder),
    its plots, and its LLM interpretation."""
    effect_sizes = _dedupe_same_trial_rows(group_key, effect_sizes, validation_flags if validation_flags is not None else [])
    family = effect_sizes[0].outcome_family
    comparison = effect_sizes[0].comparison_family
    timepoint = effect_sizes[0].follow_up_timepoint
    split_by_timepoint = bool(plan and getattr(plan, "split_by_timepoint", False))
    label = (
        group_label(family, timepoint, comparison_family=comparison, split_by_timepoint=split_by_timepoint)
        if group_key != "default" else "All outcomes (undifferentiated)"
    )
    k = len(effect_sizes)
    n_total = sum(es.n_total for es in effect_sizes)
    study_ids = [es.study_id for es in effect_sizes]

    effect_measure, computation_scale, measure_source, measure_conflict, usable = _resolve_and_populate_native(
        group_key, effect_sizes, plan
    )
    logger.info(
        f"[MetaAnalysis] Group '{group_key}' ({label}): effect_measure={effect_measure.value} "
        f"computation_scale={computation_scale.value} source={measure_source}"
        + (f" CONFLICT: {measure_conflict}" if measure_conflict else "")
    )

    if len(usable) < MIN_K_FOR_POOLING:
        logger.warning(
            f"[MetaAnalysis] Group '{group_key}' ({label}): only k={len(usable)} usable effect size(s) — "
            f"insufficient to estimate heterogeneity (need k>={MIN_K_FOR_POOLING}). "
            "Reporting as insufficient_data instead of silently merging into another group."
        )
        return (
            MetaAnalysisGroupResult(
                outcome_group_key=group_key,
                outcome_family=family,
                comparison_family=comparison,
                follow_up_timepoint=timepoint,
                label=label,
                k=k,
                n_total=n_total,
                study_ids=study_ids,
                insufficient_data=True,
                single_effect_g=effect_sizes[0].hedges_g if k == 1 else None,
                result=None,
                effect_measure=effect_measure,
                computation_scale=computation_scale,
                effect_measure_source=measure_source,
                effect_measure_conflict=measure_conflict,
                split_reason=split_reason,
            ),
            {},
            None,
        )

    values = [es.native_value for es in usable]
    variances = [es.native_variance for es in usable]

    try:
        stats = _run_model(values, variances, sum(es.n_total for es in usable), computation_scale,
                           method=_pooling_method(plan))
    except Exception as exc:
        logger.error(f"[MetaAnalysis] Statistical computation failed for group '{group_key}': {exc}")
        return (
            MetaAnalysisGroupResult(
                outcome_group_key=group_key,
                outcome_family=family,
                comparison_family=comparison,
                follow_up_timepoint=timepoint,
                label=label,
                k=k,
                n_total=n_total,
                study_ids=study_ids,
                insufficient_data=True,
                result=None,
                effect_measure=effect_measure,
                computation_scale=computation_scale,
                effect_measure_source=measure_source,
                effect_measure_conflict=measure_conflict,
                split_reason=split_reason,
            ),
            {},
            None,
        )

    # favors_treatment: only meaningful for a difference-type scale (SMD/HEDGES_G/MD/GENERIC),
    # where 0 = no effect and plan.higher_score_is_worse tells us which side of 0 is
    # favourable. A ratio measure (RR/OR/HR/PETO_OR) has "no effect" at 1, not 0, AND
    # whether a lower ratio is favourable depends on whether the counted event itself is
    # good or bad (e.g. RR of death vs RR of recovery) -- a separate question
    # higher_score_is_worse was never designed to answer, so left None (not guessed) here
    # rather than silently assuming every ratio outcome counts an undesirable event.
    higher_score_is_worse = bool(plan and getattr(plan, "higher_score_is_worse", False))
    pooled_favors_treatment = (
        None if computation_scale in RATIO_MEASURES
        else determine_favors_treatment(stats["pooled_g"], higher_score_is_worse)
    )

    result = MetaAnalysisResult(
        pooled_g=stats["pooled_g"],
        pooled_effect=stats["pooled_g"],
        pooled_se=stats["pooled_se"],
        ci_lower=stats["ci_lower"],
        ci_upper=stats["ci_upper"],
        z_value=stats["z_value"],
        p_value=stats["p_value"],
        tau_squared=stats["tau_squared"],
        tau=stats["tau"],
        i_squared=stats["i_squared"],
        h_squared=stats["h_squared"],
        q_statistic=stats["q_statistic"],
        q_df=stats["q_df"],
        q_p_value=stats["q_p_value"],
        k=stats["k"],
        n_total=stats["n_total"],
        method=stats.get("method", _pooling_method(plan)),
        favors_treatment=pooled_favors_treatment,
        effect_measure=effect_measure,
        computation_scale=computation_scale,
        effect_measure_source=measure_source,
        effect_measure_conflict=measure_conflict,
    )

    suffix = "" if is_primary else safe_filename_fragment(group_key)
    title_prefix = "" if is_primary else label
    if measure_conflict or effect_measure == EffectMeasure.UNKNOWN:
        title_prefix = f"{title_prefix} [effect measure unconfirmed]".strip()
    plots = _generate_plots(usable, values, variances, computation_scale, result, stats, output_dir, plan, suffix, title_prefix)
    interpretation = _interpret_group(result, label, plan)

    logger.info(
        f"[MetaAnalysis] Group '{group_key}' ({label}): "
        f"g={result.pooled_g:.3f} CI[{result.ci_lower:.3f},{result.ci_upper:.3f}] "
        f"I²={result.i_squared:.1f}% k={result.k}"
    )

    return (
        MetaAnalysisGroupResult(
            outcome_group_key=group_key,
            outcome_family=family,
            comparison_family=comparison,
            follow_up_timepoint=timepoint,
            label=label,
            k=k,
            n_total=n_total,
            study_ids=study_ids,
            insufficient_data=False,
            result=result,
            effect_measure=effect_measure,
            computation_scale=computation_scale,
            effect_measure_source=measure_source,
            effect_measure_conflict=measure_conflict,
            split_reason=split_reason,
        ),
        plots,
        interpretation,
    )


def meta_analysis_node(state: dict) -> dict:
    logger.info("=== STAGE 6: Meta-Analysis ===")
    effect_sizes: List[EffectSizeRecord] = state.get("effect_sizes", [])
    output_dir: str = state["output_dir"]
    plan = state.get("plan")
    validation_flags: List[ValidationFlag] = list(state.get("validation_flags", []))

    if not effect_sizes:
        logger.warning("[MetaAnalysis] No effect sizes — skipping.")
        # Still write fresh (empty) result files. output_dir is reused across
        # runs within the same dashboard session (run_service.py keys it off
        # session_id, not run id) -- skipping these writes on a genuinely
        # empty run leaves whatever meta_analysis_result.json/
        # meta_analysis_results_by_group.json a PREVIOUS, unrelated run left
        # behind completely untouched, so this run's output would silently
        # show that other run's pooled result as if it were its own. A real
        # run hit exactly this: every candidate row got excluded upstream
        # (no raw event counts, only reported percentages), effect_sizes
        # arrived here empty, and the output directory kept an unrelated
        # prior run's result for a completely different review/outcome.
        save_json({}, os.path.join(output_dir, "meta_analysis_result.json"))
        save_json([], os.path.join(output_dir, "meta_analysis_results_by_group.json"))
        return {
            "meta_result": None, "meta_plots": {}, "meta_interpretation": {},
            "meta_results": [], "meta_group_plots": {}, "meta_group_interpretation": {},
        }

    # --- Group effect sizes by outcome_group_key (declarative, built at
    # extraction time from outcome_family/follow_up_timepoint/comparison_family
    # -- see utils/outcome_grouping.py). Rows with no classification all share
    # "default", so a legacy/single-outcome run produces exactly one group,
    # identical to the pre-grouping behaviour of this node. ---
    raw_groups: Dict[str, List[EffectSizeRecord]] = defaultdict(list)
    for es in effect_sizes:
        raw_groups[es.outcome_group_key].append(es)

    # --- Measure-compatibility partition pass: within each outcome_group_key,
    # split rows further when they report >=2 incompatible effect measures
    # (see _partition_by_row_measure()) -- prevents e.g. HR rows and OR rows
    # sharing one outcome_group_key from being silently pooled together on a
    # common Hedges' g fallback. Never applied silently: a split_reason is
    # attached to every resulting group when a split actually happened. ---
    groups: Dict[str, List[EffectSizeRecord]] = {}
    split_reasons: Dict[str, str] = {}
    for key, rows in raw_groups.items():
        for suffix, sub_rows, reason in _partition_by_row_measure(rows):
            new_key = f"{key}{suffix}"
            groups[new_key] = sub_rows
            if reason:
                split_reasons[new_key] = reason
                logger.info(f"[MetaAnalysis] Group '{key}' split into '{new_key}': {reason}")

    logger.info(
        f"[MetaAnalysis] {len(effect_sizes)} effect sizes across {len(groups)} "
        f"outcome group(s): {sorted(groups.keys())}"
    )

    # Deterministic ordering: largest group first (ties broken alphabetically
    # by key) -- the first group built is treated as "primary" and gets the
    # unsuffixed legacy plot filenames. Groups rooted in the uncategorized
    # "default" bucket (rows the outcome classifier explicitly could not fit
    # into any real family -- see cross_paper_outcome_mapper_agent.py) are
    # sorted to the END regardless of size: "default" is a leftover pile of
    # UNRELATED outcomes, not a real construct, so it must never be picked as
    # THE headline pooled result just because it happens to have more rows
    # than any single real outcome family. It only becomes primary if it is
    # the only group that exists at all (legacy single-outcome runs, where
    # every row is unclassified -- that must keep working exactly as before).
    def _is_default_rooted(key: str) -> bool:
        return key == DEFAULT_GROUP_KEY or key.startswith(f"{DEFAULT_GROUP_KEY}::")

    ordered_keys = sorted(
        groups.keys(),
        key=lambda k: (_is_default_rooted(k), -len(groups[k]), k),
    )

    all_group_results: List[MetaAnalysisGroupResult] = []
    group_plots: Dict[str, Dict[str, str]] = {}
    group_interpretation: Dict[str, str] = {}
    primary_key: Optional[str] = None

    for i, key in enumerate(ordered_keys):
        is_primary_candidate = (i == 0)
        group_result, plots, interpretation = _build_group(
            key, groups[key], output_dir, plan, is_primary_candidate,
            split_reason=split_reasons.get(key),
            validation_flags=validation_flags,
        )
        all_group_results.append(group_result)
        if plots:
            group_plots[key] = plots
        if interpretation:
            group_interpretation[key] = interpretation
        if is_primary_candidate and not group_result.insufficient_data:
            primary_key = key

    # If the largest (non-default) group didn't have enough data to pool,
    # fall back to the next-largest group that DID -- preferring any real
    # classified outcome over "default" -- never fabricate a "primary" from
    # an insufficient-data group.
    if primary_key is None:
        for gr in sorted(
            all_group_results,
            key=lambda g: (_is_default_rooted(g.outcome_group_key), -g.k),
        ):
            if not gr.insufficient_data:
                primary_key = gr.outcome_group_key
                break

    primary = next((g for g in all_group_results if g.outcome_group_key == primary_key), None)

    # --- Backward-compatible top-level aliases ---
    meta_result = primary.result if primary else None
    meta_plots = group_plots.get(primary_key, {}) if primary_key else {}
    meta_interpretation = (
        {"overall": group_interpretation[primary_key]}
        if primary_key in group_interpretation else {}
    )

    save_json(
        meta_result.model_dump() if meta_result else {},
        os.path.join(output_dir, "meta_analysis_result.json"),
    )
    save_json(
        [g.model_dump() for g in all_group_results],
        os.path.join(output_dir, "meta_analysis_results_by_group.json"),
    )

    n_insufficient = sum(1 for g in all_group_results if g.insufficient_data)
    if n_insufficient:
        logger.info(
            f"[MetaAnalysis] {n_insufficient}/{len(all_group_results)} group(s) had "
            f"insufficient data (k<{MIN_K_FOR_POOLING}) — reported, not pooled."
        )

    # Captured after at least one _run_model() call has already succeeded
    # above -- i.e. only once metafor has actually computed a real result,
    # not just because the R bridge is importable.
    engine_info = metafor_engine.engine_info() if meta_result else None
    if engine_info:
        save_json(engine_info, os.path.join(output_dir, "stats_engine_info.json"))

    return {
        "meta_result":         meta_result,
        "meta_plots":          meta_plots,
        "meta_interpretation": meta_interpretation,
        "meta_results":        all_group_results,
        "meta_group_plots":    group_plots,
        "meta_group_interpretation": group_interpretation,
        "stats_engine_info":   engine_info,
        "validation_flags":    validation_flags,
    }
