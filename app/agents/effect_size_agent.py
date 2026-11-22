"""
Effect Size node — Stage 5 of the pipeline.

Pattern 4: reads pre-computed effect sizes from meta_ready_results.json
and assembles EffectSizeRecord objects. No LLM call needed.

Also exports the meta-ready coding table via export_table_node.
"""

import logging
import os

from models import EffectSizeRecord
from utils.paper_results_converter import convert_paper_results
from utils.outcome_grouping import build_outcome_group_key
from utils.effect_measures import determine_favors_treatment
from core_utils import load_json, save_json

logger = logging.getLogger(__name__)


def export_table_node(state: dict) -> dict:
    """Convert paper_results → meta_ready_results.json/csv using final in-memory state."""
    logger.info("=== STAGE 4C: Export Table ===")
    output_dir = state["output_dir"]
    paper_results_path = os.path.join(output_dir, "paper_results.json")

    # Use the final in-memory paper_results (after validation + relevance filtering).
    # If present, overwrite the file so it reflects all pipeline stages, not just
    # the raw extraction output that extraction_node wrote earlier.
    in_memory = state.get("paper_results")
    if in_memory:
        save_json(in_memory, paper_results_path)
        logger.info(f"[ExportTable] Using {len(in_memory)} in-memory results (post-validation).")
    elif not os.path.exists(paper_results_path):
        logger.warning("[ExportTable] paper_results.json not found — skipping export.")
        return {"coded_csv_path": ""}
    else:
        logger.warning(
            "[ExportTable] In-memory paper_results is empty (validation/filter removed all) — "
            "falling back to raw extraction file on disk."
        )

    try:
        converted = convert_paper_results(
            input_path=paper_results_path,
            output_dir=output_dir,
        )
        coded_csv = os.path.join(output_dir, "meta_ready_results.csv")
        n_include = sum(1 for r in converted if r.get("Include/Exclude") == "Include")
        logger.info(f"[ExportTable] {n_include}/{len(converted)} rows marked Include.")
        if n_include == 0 and converted:
            reasons = {}
            for r in converted:
                reason = (r.get("Comment") or "no comment")[:80]
                reasons[reason] = reasons.get(reason, 0) + 1
            for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
                logger.warning(f"[ExportTable] Excluded ({count}x): {reason}")
        return {"coded_csv_path": coded_csv}
    except Exception as exc:
        logger.error(f"[ExportTable] Failed: {exc}")
        return {"coded_csv_path": "", "errors": state.get("errors", []) + [str(exc)]}


def effect_size_node(state: dict) -> dict:
    """Load pre-computed effect sizes from meta_ready_results.json."""
    logger.info("=== STAGE 5: Effect Size ===")
    output_dir = state["output_dir"]
    meta_ready_path = os.path.join(output_dir, "meta_ready_results.json")

    if not os.path.exists(meta_ready_path):
        logger.warning("[EffectSize] meta_ready_results.json not found — no effect sizes.")
        return {"effect_sizes": []}

    meta_ready = load_json(meta_ready_path)
    effect_sizes = []
    plan = state.get("plan")
    higher_score_is_worse = bool(getattr(plan, "higher_score_is_worse", False)) if plan else False

    # paper_id -> trial_cluster_id, when agents/document_type_agent.py's
    # assign_trial_clusters() detected a companion publication of the same
    # trial (see models.PaperRecord.trial_cluster_id). Empty for any run
    # that never populated it (search mode, or no companion detected) --
    # every row's trial_cluster_id then stays None, unchanged behavior.
    cluster_map = {
        p.id: p.trial_cluster_id
        for p in state.get("papers_eligible", [])
        if getattr(p, "trial_cluster_id", None)
    }

    def _to_float(v):
        try:
            return float(v) if v not in (None, "") else None
        except (TypeError, ValueError):
            return None

    for i, row in enumerate(meta_ready, start=1):
        include_exclude = row.get("Include/Exclude") or row.get("include_exclude") or ""
        ready = row.get("effect_size_ready")
        if isinstance(ready, str):
            ready = ready.lower() == "true"

        inc = str(include_exclude).strip().lower()
        if inc == "exclude":
            # An EXPLICIT exclusion decision -- whether for insufficient
            # data, or because the row doesn't match the requested outcome/
            # timepoint (utils/paper_results_converter.py's
            # meta_analysis_candidate=False override) -- must never be
            # second-guessed just because a Hedges' g/Cohen's d already
            # happens to be computed for it. That computation runs BEFORE
            # the include/exclude decision, so without this check a
            # wrongly-scoped-but-numerically-computable row would silently
            # slip back in here regardless of why it was excluded (the real
            # CD008754 Chiaravalloti 2005 bug: correctly excluded upstream,
            # then re-included right here via this exact fallback).
            continue
        # Old-format files may lack Include/Exclude entirely (inc == "") --
        # treat a genuinely MISSING field (never an explicit "exclude",
        # handled above) as included if a pre-computed hedges_g or cohens_d
        # value is already present.
        if not ready and inc != "include":
            has_precomputed = (
                row.get("hedges_g") not in (None, "")
                or row.get("cohens_d") not in (None, "")
            )
            if not has_precomputed:
                continue

        hedges_g = _to_float(row.get("hedges_g"))
        cohens_d = _to_float(row.get("cohens_d"))
        log_effect = _to_float(row.get("log_effect"))

        effect_value = hedges_g if hedges_g is not None else (
            log_effect if log_effect is not None else cohens_d
        )

        if effect_value is None:
            logger.warning(
                f"[EffectSize] Skipping row {i}: "
                f"effect_value=None (hedges_g={row.get('hedges_g')!r}, "
                f"cohens_d={row.get('cohens_d')!r}, "
                f"Include/Exclude={row.get('Include/Exclude')!r})"
            )
            continue

        n_t = row.get("n_treatment")
        n_c = row.get("n_control")

        try:
            n_t = float(n_t)
            n_c = float(n_c)
            n_total = int(n_t + n_c)
        except Exception:
            n_t = None
            n_c = None
            n_total_raw = row.get("n_total")
            n_total = int(float(n_total_raw)) if n_total_raw not in (None, "") else 0
            logger.warning(
                f"[EffectSize] Row {i}: n_treatment/n_control not numeric "
                f"(n_treatment={row.get('n_treatment')!r}, "
                f"n_control={row.get('n_control')!r}), "
                f"n_total={n_total}"
            )

        variance = _to_float(row.get("effect_variance"))
        g_val = effect_value  # already a float from _to_float above

        if variance is None:
            if n_t and n_c:
                # Full Hedges' g variance formula
                variance = (n_t + n_c) / (n_t * n_c) + g_val**2 / (2 * (n_t + n_c))
            elif n_total and n_total > 0:
                # Approximate with equal group split
                n_half = n_total / 2.0
                variance = n_total / (n_half * n_half) + g_val**2 / (2 * n_total)
            else:
                logger.warning(
                    f"[EffectSize] Skipping row {i}: "
                    "no sample size available to compute variance."
                )
                continue

        if variance <= 0:
            logger.warning(
                f"[EffectSize] Skipping row {i}: variance={variance} <= 0."
            )
            continue

        se = variance ** 0.5
        ci_lower = g_val - 1.96 * se
        ci_upper = g_val + 1.96 * se

        outcome_family = row.get("outcome_family") or None
        follow_up_timepoint = row.get("follow_up_timepoint") or None

        # --- Native effect-measure raw inputs/evidence (see
        # utils/effect_measures.py). All optional; a row with none of this
        # populated (the vast majority of legacy runs/topics) behaves
        # exactly as before -- pooled on hedges_g only. ---
        raw_inputs = {}
        for key, converter_key in (
            ("mean_treatment", "M_treatment"), ("sd_treatment", "SD_treatment"),
            ("mean_control", "M_control"), ("sd_control", "SD_control"),
            ("events_treatment", "group_2_events"), ("events_control", "group_1_events"),
        ):
            v = _to_float(row.get(converter_key))
            if v is not None:
                raw_inputs[key] = v
        # n_treatment/n_control: prefer the explicit dichotomous total
        # (group_2_total/group_1_total) when present, else the already-
        # coalesced n_treatment/n_control column (covers the continuous case).
        n_treatment_raw = _to_float(row.get("group_2_total")) if row.get("group_2_total") not in (None, "") else n_t
        n_control_raw = _to_float(row.get("group_1_total")) if row.get("group_1_total") not in (None, "") else n_c
        if n_treatment_raw is not None:
            raw_inputs["n_treatment"] = n_treatment_raw
        import config as _cfg
        if getattr(_cfg, "DIFF_FALLBACK", False):
            m_diff, se_diff = _to_float(row.get("M_diff")), _to_float(row.get("SE_diff"))
            if m_diff is not None and se_diff and se_diff > 0:
                raw_inputs["mean_diff"] = m_diff
                raw_inputs["se_diff"] = se_diff
        if n_control_raw is not None:
            raw_inputs["n_control"] = n_control_raw
        # scale_min/scale_max: the instrument's own stated numeric range
        # (e.g. a 100mm VAS -> 0/100), filled by the extractor ONLY when the
        # paper explicitly states it -- see utils/effect_measures.py's
        # scale-harmonization logic, which rescales rows sharing this onto a
        # common footing before pooling as a mean difference. Both must be
        # present (never one alone) for a usable range.
        scale_min = _to_float(row.get("outcome_scale_min"))
        scale_max = _to_float(row.get("outcome_scale_max"))
        if scale_min is not None and scale_max is not None and scale_max > scale_min:
            raw_inputs["scale_min"] = scale_min
            raw_inputs["scale_max"] = scale_max
        # Track WHICH specific ratio field supplied reported_ratio -- RR, OR,
        # and HR are never interchangeable (an HR is a time-to-event measure,
        # not a simple proportion ratio; see the extractor's own docstring
        # for hazard_ratio), so utils/effect_measures.py's native-pooling
        # fallback must only accept this value when it actually matches the
        # group's target computation_scale, never silently substitute across
        # types just because all three happen to live on the same log scale.
        # Root cause this fixes: a row reporting only a hazard ratio (e.g.
        # Elliott 2023's AF-recurrence HR) was being pooled as if it were a
        # risk ratio whenever a run explicitly requested RR pooling.
        risk_ratio_val = _to_float(row.get("risk_ratio"))
        odds_ratio_val = _to_float(row.get("odds_ratio"))
        hazard_ratio_val = _to_float(row.get("hazard_ratio"))
        if risk_ratio_val:
            reported_ratio, reported_ratio_measure = risk_ratio_val, "RR"
            lo, hi = _to_float(row.get("CI_lower_rr")), _to_float(row.get("CI_upper_rr"))
        elif odds_ratio_val:
            reported_ratio, reported_ratio_measure = odds_ratio_val, "OR"
            lo, hi = _to_float(row.get("CI_lower_or")), _to_float(row.get("CI_upper_or"))
        elif hazard_ratio_val:
            reported_ratio, reported_ratio_measure = hazard_ratio_val, "HR"
            lo, hi = _to_float(row.get("CI_lower_hr")), _to_float(row.get("CI_upper_hr"))
        else:
            reported_ratio, reported_ratio_measure, lo, hi = None, None, None, None
        if reported_ratio:
            raw_inputs["reported_ratio"] = reported_ratio
            raw_inputs["reported_ratio_measure"] = reported_ratio_measure
            if lo is not None:
                raw_inputs["reported_ratio_ci_lower"] = lo
            if hi is not None:
                raw_inputs["reported_ratio_ci_upper"] = hi

        es = EffectSizeRecord(
            study_id=row.get("paper_id") or f"study_{i}",
            report_id=row.get("comparison_label") or f"R{i}",
            hedges_g=g_val,
            cohens_d=cohens_d if cohens_d is not None else g_val,
            se=float(se),
            ci_lower=float(ci_lower),
            ci_upper=float(ci_upper),
            variance=float(variance),
            n_total=int(n_total),
            computation_method=row.get("conversion_method") or "meta_ready",
            conversion_method=row.get("conversion_method") or None,
            # meta_ready_results rows key the paper id as "Study_ID" (the GT
            # column name, see utils/paper_results_converter.py::GT_COLUMNS)
            # -- "paper_id" (lowercase) is never actually populated here (same
            # gap noted for study_id's own paper_tracking.csv matching in
            # agents/pipeline_audit_agent.py); check both so this lookup
            # doesn't silently never match.
            trial_cluster_id=cluster_map.get(row.get("Study_ID") or row.get("paper_id")),
            outcome_name=row.get("Outcome variable") or row.get("outcome_name") or None,
            outcome_family=outcome_family,
            comparison_family=row.get("comparison_family") or None,
            effect_direction=row.get("effect_direction") or None,
            favors_treatment=determine_favors_treatment(g_val, higher_score_is_worse),
            unit_of_analysis=row.get("unit_of_analysis") or None,
            follow_up_timepoint=follow_up_timepoint,
            outcome_group_key=build_outcome_group_key(
                outcome_family, follow_up_timepoint,
                comparison_family=row.get("comparison_family") or None,
                split_by_timepoint=bool(state.get("plan") and getattr(state["plan"], "split_by_timepoint", False)),
            ),
            reported_effect_measure=row.get("reported_effect_measure") or None,
            outcome_units=row.get("outcome_units") or None,
            raw_measure_inputs=raw_inputs,
        )

        effect_sizes.append(es)

    logger.info(f"[EffectSize] Loaded {len(effect_sizes)} effect sizes from meta_ready_results.")

    # Always write effect_sizes.json, even when the list is empty. Every
    # output_dir is reused across runs within the same dashboard session
    # (run_service.py keys it off session_id, not run id) -- if a run
    # genuinely has zero poolable rows and this write is skipped, a STALE
    # effect_sizes.json from a PREVIOUS, unrelated run silently stays in
    # place and gets picked up by meta_analysis_node next, producing a
    # result for a completely different topic that looks like a real
    # answer for this run. A real CD014821 run hit exactly this: every
    # candidate row was excluded (percentage-only reporting, no raw event
    # counts), effect_sizes ended up [], and the run's output directory
    # kept an unrelated CD015331 run's schizophrenia-outcome result.
    save_json(
        [es.model_dump() if hasattr(es, "model_dump") else es for es in effect_sizes],
        os.path.join(output_dir, "effect_sizes.json"),
    )

    return {"effect_sizes": effect_sizes}
