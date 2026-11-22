"""Report agent — Stage 9. Pattern 1: finalise_report tool writes the markdown file."""

import logging
import os
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from models import EffectMeasure
from pipeline_graph import _extract_tool_args, GraphState
from utils.effect_measures import measure_label as _measure_label, native_pooling_used as _native_pooling_used

logger = logging.getLogger(__name__)


def _measure_fields(effect_measure: EffectMeasure, computation_scale: EffectMeasure, source: str, conflict: Optional[str]) -> dict:
    """The measure-aware fields added to every group's context dict AND used
    to build the deterministic summary section -- one function, one source
    of truth for both."""
    native = _native_pooling_used(effect_measure, computation_scale)
    return {
        "effect_measure": effect_measure.value,
        "computation_scale": computation_scale.value,
        "measure_label": _measure_label(computation_scale),
        "effect_measure_source": source,
        "effect_measure_conflict": conflict,
        "native_pooling_used": native,
    }


def _build_effect_measure_summary(meta_results: List) -> str:
    """Deterministic (NOT LLM-authored) markdown section, appended to every
    report after the LLM's own text -- this is the guarantee behind "do not
    label native RR/OR/MD results as Hedges' g": the LLM is instructed not
    to mislabel (see the system prompts above), but this section states the
    resolved measure exactly as computed regardless of what the LLM wrote,
    for every outcome group meta_analysis_node produced (including
    insufficient_data ones, which still carry a resolved
    effect_measure/computation_scale even with no pooled result)."""
    if not meta_results:
        return ""
    lines = [
        "\n\n## Effect Measure Summary",
        "",
        "_This section is generated deterministically from the pipeline's own "
        "resolution output (see utils/effect_measures.py), not by the LLM writer above — "
        "it is the authoritative statement of which effect measure each outcome group was "
        "pooled on, and whether that was the group's own native scale or a Hedges' g/SMD "
        "fallback._",
        "",
        "| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |",
        "|---|---|---|---|---|",
    ]
    for g in meta_results:
        native = _native_pooling_used(g.effect_measure, g.computation_scale)
        measure_text = _measure_label(g.computation_scale)
        if not native:
            if g.effect_measure == EffectMeasure.UNKNOWN:
                reason = "effect measure not confirmed with sufficient evidence"
            else:
                reason = f"{_measure_label(g.effect_measure)} intended, but not computable natively for enough studies"
            measure_text = f"{measure_text} (fallback — {reason})"
        if g.result:
            estimate = f"{g.result.pooled_effect:.4f} [{g.result.ci_lower:.4f}, {g.result.ci_upper:.4f}]"
        elif g.single_effect_g is not None:
            estimate = f"{g.single_effect_g:.4f} (single study, not pooled)"
        else:
            estimate = "insufficient data"
        row = f"| {g.label} | {g.k} | {measure_text} | {'Yes' if native else 'No'} | {estimate} |"
        lines.append(row)
        if g.effect_measure_conflict:
            lines.append(f"| | | ⚠ {g.effect_measure_conflict} | | |")
    return "\n".join(lines) + "\n"

_SYSTEM_PROMPT_BASE = (
    "You are an academic writer specialising in systematic reviews and meta-analyses. "
    "Write a comprehensive, publication-quality meta-analysis report based on the "
    "provided pipeline results. Follow PRISMA 2020 reporting guidelines.\n\n"
    "Structure your report with these sections:\n"
    "  1. Abstract (structured)\n"
    "  2. Search and Screening Results\n"
    "  3. Included Studies Overview\n"
    "  4. Effect Sizes\n"
    "  5. Main Meta-Analytic Result(s)\n"
    "  6. Heterogeneity Analysis\n"
    "  7. Moderator Analyses\n"
    "  8. Publication Bias\n"
    "  9. Discussion\n"
    " 10. Limitations\n"
    " 11. Conclusion\n\n"
    "If context data includes 'meta_analysis_groups' with more than one entry, "
    "the included studies measured more than one distinct outcome (and/or the same "
    "outcome at different follow-up timepoints) — report each group's own k, pooled "
    "effect, CI, and heterogeneity separately in section 5. Do not merge them into one "
    "overall number. Groups marked insufficient_data have too few studies to pool "
    "(state that plainly; do not invent a pooled estimate for them).\n\n"
    "EFFECT MEASURE LABELING — every meta_analysis / meta_analysis_groups entry carries "
    "'measure_label' (the correct name for the number you're reporting) and "
    "'native_pooling_used' (true/false). Always use 'measure_label' as the name of the "
    "statistic in your prose — e.g. write 'pooled risk ratio' or 'pooled mean difference' "
    "when measure_label says so. NEVER call a result \"Hedges' g\" unless measure_label "
    "itself says \"Hedges' g\". When native_pooling_used is false, say plainly that the "
    "effect measure could not be confidently determined and the number shown is a "
    "standardized fallback estimate, not a confirmed native-scale result — use "
    "'pooled_effect' (not the legacy 'pooled_g' name) when phrasing this. A deterministic "
    "Effect Measure Summary table is appended after your text — do not duplicate it, but do "
    "not contradict it either.\n\n"
    "DIRECTION — every meta_analysis / meta_analysis_groups entry also carries a 'favors' "
    "field. Always state which arm the result favors using THIS field, never by inferring it "
    "yourself from the sign of pooled_effect/pooled_g — those numbers keep the raw statistical "
    "sign convention (treatment minus control), and for some outcomes a LOWER raw value is "
    "actually the better one, so the sign alone can be misleading.\n\n"
    "Call `finalise_report` with the complete Markdown text."
)


@tool
def finalise_report(title: str, abstract: str, body: str) -> str:
    """Write the completed PRISMA-compliant meta-analysis report to disk.
    body: full Markdown body (Introduction through References)."""
    return "report_finalised"


def report_node(state: GraphState) -> dict:
    """Stage 9: generate PRISMA-compliant markdown report."""
    logger.info("=== STAGE 9: Report Generation ===")
    output_dir: str = state["output_dir"]
    plan        = state.get("plan")
    meta_result = state.get("meta_result")
    mod_results = state.get("moderator_results", [])
    bias_result = state.get("bias_result")
    effect_sizes= state.get("effect_sizes", [])

    # Build the rich context dict the original ReportAgent passed as context=
    meta_plots = state.get("meta_plots", {})
    meta_interpretation = state.get("meta_interpretation", {})
    combined_model = state.get("combined_model", {})
    bias_interpretation = state.get("bias_interpretation", {})
    papers_eligible = state.get("papers_eligible", [])

    context: Dict[str, Any] = {
        "research_question": plan.research_question if plan else "Not specified",
        "treatment_label":   plan.treatment_label   if plan else "treatment",
        "control_label":     plan.control_label     if plan else "control",
        "pipeline_summary": {
            "n_studies":      len(papers_eligible),
            "n_effect_sizes": len(effect_sizes),
        },
        "effect_sizes": [
            {
                "label":    f"{es.study_id}_{es.report_id}" if hasattr(es, "study_id") else str(es),
                "hedges_g": getattr(es, "hedges_g", None),
                "ci":       f"[{getattr(es,'ci_lower',0):.3f}, {getattr(es,'ci_upper',0):.3f}]",
                "n":        getattr(es, "n_total", None),
            }
            for es in effect_sizes
        ],
    }
    if meta_result:
        context["meta_analysis"] = {
            "pooled_effect": meta_result.pooled_effect,   # measure-neutral -- use this name in prose
            "pooled_g":   meta_result.pooled_g,            # backward-compat alias, same value
            # pooled_effect/pooled_g ALWAYS use the raw (treatment - control)/SD sign
            # (Cochrane/RevMan's own convention) -- do NOT infer direction from that sign;
            # this field is the separate, already-resolved answer (see
            # EffectSizeRecord.favors_treatment's docstring in models.py for why: some
            # outcomes are scored so a LOWER raw value is the better one).
            "favors": (
                (plan.treatment_label if plan else "treatment") if meta_result.favors_treatment is True
                else (plan.control_label if plan else "control") if meta_result.favors_treatment is False
                else "neither (essentially a tie, or a ratio measure where favourability "
                     "depends on which event was counted)"
            ),
            "p_value":    meta_result.p_value,
            "ci_95":      f"[{meta_result.ci_lower:.3f}, {meta_result.ci_upper:.3f}]",
            "i_squared":  meta_result.i_squared,
            "tau_squared":meta_result.tau_squared,
            "q_statistic":meta_result.q_statistic,
            "q_p_value":  meta_result.q_p_value,
            "k":          meta_result.k,
            "n_total":    meta_result.n_total,
            "method":     meta_result.method,
            **_measure_fields(
                meta_result.effect_measure, meta_result.computation_scale,
                meta_result.effect_measure_source, meta_result.effect_measure_conflict,
            ),
        }

    # meta_results: every distinct outcome group meta_analysis_node pooled
    # separately (construct x follow-up timepoint), not just the single
    # "primary" one meta_result/context["meta_analysis"] aliases above. When
    # there's only one group this duplicates meta_analysis and the LLM can
    # ignore it; when there are several, this is what lets the report
    # describe each pooled outcome on its own instead of implying the whole
    # review boiled down to one number.
    meta_results = state.get("meta_results", []) or []
    if len(meta_results) > 1:
        context["meta_analysis_groups"] = [
            {
                "outcome_group_key": g.outcome_group_key,
                "label":             g.label,
                "k":                 g.k,
                "n_total":           g.n_total,
                "insufficient_data": g.insufficient_data,
                # measure fields come from the WRAPPER (MetaAnalysisGroupResult),
                # not g.result -- available even when insufficient_data means
                # g.result is None, since resolution runs before pooling.
                **_measure_fields(g.effect_measure, g.computation_scale, g.effect_measure_source, g.effect_measure_conflict),
                **(
                    {
                        "pooled_effect": g.result.pooled_effect,
                        "pooled_g":  g.result.pooled_g,
                        "ci_95":     f"[{g.result.ci_lower:.3f}, {g.result.ci_upper:.3f}]",
                        "p_value":   g.result.p_value,
                        "i_squared": g.result.i_squared,
                        # See context["meta_analysis"]["favors"] above -- same reasoning.
                        "favors": (
                            (plan.treatment_label if plan else "treatment") if g.result.favors_treatment is True
                            else (plan.control_label if plan else "control") if g.result.favors_treatment is False
                            else "neither (tie or undetermined)"
                        ),
                    }
                    if g.result else
                    {"single_effect_g": g.single_effect_g} if g.single_effect_g is not None else {}
                ),
            }
            for g in meta_results
        ]
    if mod_results:
        context["moderators"] = [
            {
                "name":    m.moderator_name,
                "QM":      m.qm_statistic,
                "QM_p":    m.qm_p_value,
                "subgroups": [
                    {"category": sg.category, "k": sg.k, "g": sg.pooled_g, "i2": sg.i_squared}
                    for sg in m.subgroups
                ],
                "coefficients": m.coefficients,
            }
            for m in mod_results
        ]
    if combined_model:
        context["combined_model"] = combined_model
    if bias_result:
        context["publication_bias"] = {
            "eggers_intercept": bias_result.eggers_intercept,
            "eggers_p":         bias_result.eggers_p_value,
            "trim_fill_k0":     bias_result.trim_fill_k0,
            "trim_fill_g":      bias_result.trim_fill_g,
            "risk":             bias_result.bias_risk,
        }
    if meta_plots:
        context["figures"] = meta_plots
    if meta_interpretation or bias_interpretation:
        context["interpretations"] = {**meta_interpretation, **bias_interpretation}

    # validation_flags: every models.ValidationFlag appended anywhere in the
    # pipeline (outcome-classification misses, document-type exclusions,
    # measure-incompatibility splits, trial-dedup exclusions, ...) -- see
    # agents/pipeline_audit_agent.py::write_validation_report() for the full
    # persisted record. Only "warning"/"error" severity surfaces in the
    # report itself (routine "info" notes, e.g. a successful trial-cluster
    # detection, are audit-trail detail, not reader-facing caveats).
    validation_flags = [f for f in (state.get("validation_flags") or []) if f.severity in ("warning", "error")]
    if validation_flags:
        context["validation_flags"] = [
            {"stage": f.stage, "severity": f.severity, "subject": f.subject_id, "message": f.message}
            for f in validation_flags
        ]

    if plan:
        system_prompt = (
            "You are an academic writer specialising in systematic reviews and meta-analyses. "
            f"Write a comprehensive, publication-quality meta-analysis report.\n\n"
            f"Research question: {plan.research_question}\n"
            f"Treatment: {plan.treatment_label}\n"
            f"Control: {plan.control_label}\n"
            f"Outcome: {plan.outcome_description}\n"
            f"Effect direction: {plan.positive_direction}\n\n"
            "Structure: Abstract -> Search/Screening -> Included Studies -> "
            "Effect Sizes -> Meta-Analytic Result(s) -> Heterogeneity -> "
            "Moderators -> Publication Bias -> Discussion -> Limitations -> Conclusion.\n"
            "If context data includes 'meta_analysis_groups' with more than one entry, "
            "the included studies span more than one distinct outcome/timepoint — report "
            "each group's own k, pooled effect, CI, and heterogeneity separately rather "
            "than merging them into one overall number. Groups marked insufficient_data "
            "have too few studies to pool; state that plainly instead of inventing a value.\n"
            "EFFECT MEASURE LABELING — every meta_analysis / meta_analysis_groups entry "
            "carries 'measure_label' and 'native_pooling_used'. Always name the statistic "
            "using 'measure_label' (e.g. 'pooled risk ratio', 'pooled mean difference'). "
            "NEVER call a result \"Hedges' g\" unless measure_label itself says so. When "
            "native_pooling_used is false, state plainly that the effect measure was not "
            "confirmed and the value is a standardized fallback, not a confirmed native-scale "
            "result. A deterministic Effect Measure Summary table is appended after your text "
            "— do not duplicate it, but do not contradict it either.\n"
            "DIRECTION — every meta_analysis / meta_analysis_groups entry also carries a "
            "'favors' field. Always state which arm the result favors using THIS field, never "
            "by inferring it yourself from the sign of pooled_effect/pooled_g — those numbers "
            "keep the raw statistical sign convention (treatment minus control), and for some "
            "outcomes a LOWER raw value is actually the better one.\n"
            "If context data includes 'validation_flags', add a short 'Data Quality & Validation "
            "Notes' section near the end (before Limitations) summarizing them in plain language — "
            "e.g. documents excluded as reviews/duplicates, outcomes that couldn't be classified, "
            "effect measures that had to be pooled separately, or trial reports excluded to avoid "
            "double-counting. State plainly, do not soften or omit these.\n"
            "Call `finalise_report` with the complete Markdown text."
        )
    else:
        system_prompt = _SYSTEM_PROMPT_BASE

    agent = create_react_agent(llm, [finalise_report], prompt=system_prompt)
    import json as _json
    result = agent.invoke({"messages": [(
        "user",
        "Write a comprehensive meta-analysis report based on the provided results. "
        "Be precise with statistics (report exact values). Include references to "
        "figure paths where plots were generated. Call `finalise_report` at the end.\n\n"
        f"Context data:\n{_json.dumps(context, indent=2, default=str)}",
    )]})

    args = _extract_tool_args(result["messages"], "finalise_report")
    if not args:
        logger.error("[ReportAgent] No report generated.")
        return {"report_path": ""}

    full_report = f"# {args.get('title', 'Meta-Analysis Report')}\n\n"
    full_report += f"## Abstract\n\n{args.get('abstract', '')}\n\n"
    full_report += args.get("body", "")
    full_report += _build_effect_measure_summary(meta_results)

    report_path = os.path.join(output_dir, "meta_analysis_report.md")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(full_report)

    logger.info(f"[ReportAgent] Report saved: {report_path} ({len(full_report):,} chars)")
    return {"report_path": report_path}
