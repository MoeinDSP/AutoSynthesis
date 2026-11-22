"""
Statistical Result Extractor — Stage 4. Pattern 3: phase-ordered tools in closure.

Phase 1: record_paper_map (must complete before Phase 2)
Phase 2: record_statistical_result (repeatable, requires Phase 1)
"""

import logging
import os
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from models import PaperRecord
from pipeline_graph import _all_tool_args, GraphState
from core_utils import save_json

logger = logging.getLogger(__name__)


def _DIFF_FALLBACK_RULE() -> str:
    """Extra extraction rule, only when config.DIFF_FALLBACK is on (off by
    default, so the benchmark's original extraction prompt is unchanged)."""
    import config as _cfg
    if not getattr(_cfg, "DIFF_FALLBACK", False):
        return ""
    return (
        "14b. Between-arm differences from ANY analysis model (ANCOVA, MMRM, mixed model,\n"
        "    regression, or an unnamed 'estimated treatment difference'):\n"
        "    • If the paper reports the difference between the intervention and control arms\n"
        "      with a 95% CI (or SE), store it in M_diff as intervention minus control, and\n"
        "      store SE_diff = SE, or (CI_upper - CI_lower) / 3.92 from the 95% CI; note the\n"
        "      derivation in extraction_warning. Do this even when arm-level SDs, an exact\n"
        "      p-value or an F/t statistic are not reported.\n"
        "    • Sample sizes: if the analysed N per arm is not stated but the analysis includes\n"
        "      all randomised participants (intention-to-treat, full analysis set or\n"
        "      treatment-policy estimand with imputation), use the randomised N per arm.\n"
    )

SYSTEM_PROMPT = (
    "You are a precise research-paper analyst and statistical extractor. "
    "You work in two mandatory phases:\n\n"
    "PHASE 1 — Paper Understanding (ALWAYS FIRST)\n"
    "  Call `record_paper_map` ONCE before anything else.\n"
    "  Build a complete structural map: paper type, study design, comparison type, "
    "studies, outcome variables, hypotheses (H1/H2/RQ1/…), and the sections where "
    "statistics appear.\n"
    "  For each hypothesis record: hypothesis_id, hypothesis_text, linked_outcome "
    "(the outcome variable it tests), study_label, and predicted direction.\n\n"
    "PHASE 2 — Statistical Extraction\n"
    "  Use the paper map from Phase 1 as your mental model.\n"
    "  When a user query is provided, use the hypotheses list to identify ALL "
    "hypotheses whose linked_outcome directly or closely measures the construct "
    "in the user query — then extract the statistical result for EACH relevant "
    "hypothesis in EACH independent study.\n"
    "  Extract ONLY from this paper's own Results sections — never from "
    "Introduction, Related Work, Background, or Discussion sections "
    "that describe OTHER papers' statistics.\n\n"
    "Phase 1 must always complete before Phase 2 begins. "
    "Never skip the paper map. Never invent experiments or statistics."
)

_MAX_CHARS = 100_000


def extraction_node(state: GraphState) -> dict:
    """Stage 4: two-phase statistical extraction per paper."""
    logger.info("=== STAGE 4: Data Extraction ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    study_maps: Dict[str, Any] = state.get("study_maps", {})
    rq_maps: Dict[str, Any] = state.get("rq_maps", {})
    output_dir: str = state["output_dir"]
    user_query: Optional[str] = state.get("user_prompt", "")
    plan = state.get("plan")

    if plan:
        synthesis_plan_text = (
            f"User prompt: {user_query}\n"
            f"Planned research question: {plan.research_question}\n"
            f"Treatment/intervention to extract: {plan.treatment_label}\n"
            f"Control/comparator to extract: {plan.control_label}\n"
            f"Outcome to extract: {plan.outcome_description}\n"
            f"Positive direction: {plan.positive_direction}\n"
            f"Effect-size note: {plan.effect_size_note or 'standard Hedges g'}\n"
        )
    else:
        synthesis_plan_text = f"User prompt: {user_query}\n"

    all_results: List[dict] = []
    all_paper_maps: Dict[str, dict] = {}

    for paper in papers:
        paper_results: List[dict] = []
        paper_map: dict = {}
        phase_done = {"map": False}

        @tool
        def record_paper_map(
            paper_id: str,
            true_research_question: str,
            paper_type: str,
            study_design: str,
            comparison_type: str,
            main_groups: List[str],
            studies: List[dict],
            outcomes: List[dict],
            hypotheses: Optional[List[dict]] = None,
            results_sections: Optional[List[str]] = None,
            warnings: Optional[List[str]] = None,
        ) -> str:
            """Phase 1: record the paper's structural map. Call this FIRST."""
            nonlocal paper_map
            phase_done["map"] = True
            paper_map = {
                "paper_id": paper_id,
                "true_research_question": true_research_question,
                "paper_type": paper_type,
                "study_design": study_design,
                "comparison_type": comparison_type,
                "main_groups": main_groups,
                "studies": studies,
                "outcomes": outcomes,
                "hypotheses": hypotheses or [],
                "results_sections": results_sections or [],
                "warnings": warnings or [],
            }
            return "paper_map_recorded"

        @tool
        def record_statistical_result(
            paper_id: str,
            paper_title: str,
            true_research_question: str,
            study_label: str,
            task_or_measure: str,
            outcome_name: str,
            result_role: str,
            comparison_type: str,
            statistic_type: str,
            evidence_quote: str,
            page_or_section: str,
            # paper-level metadata
            author: Optional[str] = None,
            publication_year: Optional[float] = None,
            publication_status: Optional[str] = None,
            design_type: Optional[str] = None,
            domain: Optional[str] = None,
            study_environment: Optional[str] = None,
            country: Optional[str] = None,
            study_year: Optional[float] = None,
            llm_model: Optional[str] = None,
            medium: Optional[str] = None,
            content_length: Optional[str] = None,
            topic_of_content: Optional[str] = None,
            interaction_type: Optional[str] = None,
            participant_type: Optional[str] = None,
            recruitment_source: Optional[str] = None,
            # study structure
            outcome_selection_reason: Optional[str] = None,
            is_independent_study: Optional[bool] = None,
            outcome_type: Optional[str] = None,
            outcome_measurement: Optional[str] = None,
            # This tool's convention is group_1=control, group_2=treatment --
            # but a paper's own table order is whatever the paper itself
            # used, and this field is the ONLY reliable way downstream code
            # can tell whether you followed the convention or reported the
            # arms in the paper's own (possibly reversed) order. Fill it
            # from your own reading of THIS row's group_1_label against
            # "Treatment/intervention to extract" and "Control/comparator to
            # extract" above -- never from label wording alone, since a
            # control arm is very often an ACTIVE comparator (e.g.
            # "supportive therapy", "treatment as usual", another
            # psychosocial intervention) whose label doesn't contain any
            # obvious "control" word. True = group_1 really is this study's
            # control/comparator arm (the normal case). False = group_1 is
            # actually the intervention/treatment arm (the paper's table
            # listed it first) -- downstream code will swap group_1/group_2
            # so the intervention always ends up correctly identified
            # regardless of the paper's own ordering. See rule 21.
            group_1_is_control: Optional[bool] = None,
            group_1_label: Optional[str] = None,
            group_1_n: Optional[float] = None,
            group_1_mean: Optional[float] = None,
            group_1_sd: Optional[float] = None,
            # Standard ERROR, not SD -- fill this INSTEAD of group_1_sd when the paper reports
            # SE (e.g. least-squares/adjusted means from an ANCOVA or mixed model). Never put an
            # SE value into group_1_sd or vice versa -- see rule 24.
            group_1_se: Optional[float] = None,
            group_1_mean_emm: Optional[float] = None,
            group_1_mean_perc: Optional[float] = None,
            group_1_ci_lower: Optional[float] = None,
            group_1_ci_upper: Optional[float] = None,
            # group 2 (treatment)
            group_2_label: Optional[str] = None,
            group_2_n: Optional[float] = None,
            group_2_mean: Optional[float] = None,
            group_2_sd: Optional[float] = None,
            # See group_1_se above -- same SE-not-SD rule, same rule 24.
            group_2_se: Optional[float] = None,
            group_2_mean_emm: Optional[float] = None,
            group_2_mean_perc: Optional[float] = None,
            group_2_ci_lower: Optional[float] = None,
            group_2_ci_upper: Optional[float] = None,
            # A trial with MORE than 2 arms: after choosing which 2 arms go into group_1/group_2
            # (per plan.treatment_label/plan.control_label -- see rule 15), record every OTHER
            # reported arm here as free text, e.g. "Brief PCIT (usual-care comparator, not this
            # review's target adaptation): n=39, M=11.9, SE=1.35" -- one entry per excluded arm,
            # semicolon-separated. This is an audit trail only (never pooled) so an excluded arm
            # is always traceable instead of silently vanishing. See rule 15.
            additional_group_ns: Optional[str] = None,
            n_total: Optional[float] = None,
            ci_level: Optional[float] = None,
            # test statistics
            df1: Optional[float] = None,
            df2: Optional[float] = None,
            test_statistic: Optional[float] = None,
            p_value: Optional[float] = None,
            effect_size_name: Optional[str] = None,
            effect_size_value: Optional[float] = None,
            # odds ratio
            odds_ratio: Optional[float] = None,
            ci_lower_or: Optional[float] = None,
            ci_upper_or: Optional[float] = None,
            # risk ratio (symmetric to odds_ratio above -- separate field
            # because OR and RR are NOT interchangeable and must never be
            # conflated; only filled when the paper reports an RR directly)
            risk_ratio: Optional[float] = None,
            ci_lower_rr: Optional[float] = None,
            ci_upper_rr: Optional[float] = None,
            # hazard ratio (symmetric to risk_ratio/odds_ratio above -- a
            # hazard ratio is NEVER interchangeable with OR/RR and must never
            # be silently substituted for one; there is also no valid 2x2-
            # counts reconstruction for HR, so this is the ONLY way an HR row
            # can ever be pooled on its native scale -- see
            # utils/paper_results_converter.py and utils/effect_measures.py)
            hazard_ratio: Optional[float] = None,
            ci_lower_hr: Optional[float] = None,
            ci_upper_hr: Optional[float] = None,
            # dichotomous event counts (needed to recompute a native OR/RR
            # via metafor::escalc when the paper reports raw counts rather
            # than a pre-computed ratio)
            group_1_events: Optional[float] = None,
            group_1_total: Optional[float] = None,
            group_2_events: Optional[float] = None,
            group_2_total: Optional[float] = None,
            # median/IQR or median/range (continuous outcomes reported as
            # medians instead of means -- common in skewed clinical data).
            # Only usable when BOTH arms report the SAME shape (median+IQR
            # for both, or median+range for both); see utils/wan2014.py for
            # the mean/SD estimation this feeds, always tagged as an
            # approximation, never treated as an exact reported mean/SD.
            group_1_median: Optional[float] = None,
            group_1_iqr_lower: Optional[float] = None,
            group_1_iqr_upper: Optional[float] = None,
            group_1_range_lower: Optional[float] = None,
            group_1_range_upper: Optional[float] = None,
            group_2_median: Optional[float] = None,
            group_2_iqr_lower: Optional[float] = None,
            group_2_iqr_upper: Optional[float] = None,
            group_2_range_lower: Optional[float] = None,
            group_2_range_upper: Optional[float] = None,
            # mean difference
            M_diff: Optional[float] = None,
            SE_diff: Optional[float] = None,
            # native effect-measure resolution evidence (see
            # utils/effect_measures.py::resolve_group_effect_measure())
            reported_effect_measure: Optional[str] = None,
            outcome_units: Optional[str] = None,
            outcome_scale_min: Optional[float] = None,
            outcome_scale_max: Optional[float] = None,
            # Lab/clinical-unit conversion (e.g. mg/dL -> mmol/L for a named
            # analyte). See rule 23 below and outcome_units_canonical's own
            # docstring for exactly when to fill these.
            outcome_unit_conversion_factor: Optional[float] = None,
            outcome_units_canonical: Optional[str] = None,
            extraction_warning: Optional[str] = None,
        ) -> str:
            """Phase 2: record one statistical result row. Requires record_paper_map first.
            result_role: primary_outcome|secondary_outcome|manipulation_check|demographic|covariate|unclear
            comparison_type: between_subjects|within_subjects|matched|mixed|correlational|regression|descriptive_only|unclear
            statistic_type: descriptive|t_test|anova|chi_square|correlation|regression|proportion|other|unclear
            reported_effect_measure: ONLY fill this when the paper's OWN results text explicitly
              names its effect measure (e.g. "risk ratio", "odds ratio", "hazard ratio",
              "mean difference", "standardized mean difference") -- never infer it from which
              numeric fields happen to be filled. Leave empty if the paper does not name its
              own measure.
              IMPORTANT -- a paper does not have to use one of those exact phrases: some papers
              report an already-computed group-comparison ratio under a DIFFERENT label (e.g.
              calling it a "quotient", "estimate", "adjusted ratio", "relative reduction", or
              simply giving the number with a 95% CI right after two group rates/proportions with
              no name at all). If you can tell from the surrounding text that a number IS a
              ratio-type comparison between the two groups (its own reported CI straddling 1 for a
              null effect is a strong signal), extract it into risk_ratio/ci_lower_rr/ci_upper_rr
              (the general-purpose ratio bucket) even when the paper's own label for it is
              unusual -- do not require an exact phrase match before recording a number that is
              clearly already a computed relative comparison. Only skip it if you cannot tell
              whether the number is a ratio at all (e.g. it could equally be a raw rate).
            outcome_units: ONLY fill this when the paper explicitly states the outcome's natural
              unit (e.g. "mmHg", "days", "points on the HAM-D scale") -- leave empty otherwise.
            outcome_scale_min/outcome_scale_max: ONLY fill BOTH when the paper explicitly states
              the instrument's fixed numeric range (e.g. "100 mm visual analogue scale" ->
              min=0, max=100; "Numerical Rating Scale, 0-10" -> min=0, max=10; "score range
              0-100" -> min=0, max=100). This is the theoretical range of the INSTRUMENT itself,
              not the observed min/max of the data. Leave BOTH empty if the paper does not state
              an explicit range, or if the outcome has no natural fixed range (e.g. reaction
              time in ms, a raw count) -- never guess a scale's range from convention or from
              what "looks like" a percentage. These two fields exist so that downstream pooling
              can rescale different-range instruments measuring the same construct (e.g. a 0-10
              NRS and a 100 mm VAS) onto one common scale before pooling as a mean difference,
              instead of always falling back to a standardized effect size -- but only when the
              range is explicitly stated, never inferred.
            outcome_unit_conversion_factor/outcome_units_canonical: fill BOTH only when the
              paper's own outcome_units is a lab/clinical unit that has a UNIVERSALLY FIXED,
              textbook conversion factor to a different, more standard unit for that exact
              analyte (e.g. triglycerides reported in mg/dL -> mmol/L uses the fixed constant
              0.0113; total/LDL/HDL cholesterol mg/dL -> mmol/L uses 0.0259; glucose mg/dL ->
              mmol/L uses 0.0555). outcome_unit_conversion_factor is the multiplier applied to
              this row's own means/SDs to convert them from the paper's stated outcome_units into
              outcome_units_canonical. Only use a factor you are certain is a fixed constant for
              the named analyte -- never estimate or approximate one. Leave BOTH empty when
              outcome_units is already the standard unit (no conversion needed), when no
              universal constant exists for this quantity, or when you are not fully certain of
              the exact factor -- a missed conversion is far safer than a wrong one. This exists
              so that different papers reporting the same construct in different lab units can
              still be pooled as a mean difference on one common unit, instead of one paper's
              row silently blocking the whole group from pooling on its native scale.
            hazard_ratio/ci_lower_hr/ci_upper_hr: ONLY fill when the paper reports a hazard ratio
              directly (e.g. from a Cox model). Do NOT approximate an HR from event counts or
              proportions -- there is no valid way to reconstruct a time-to-event hazard ratio
              from a simple 2x2 table; leave empty if only counts/proportions are available.
            group_1_median/group_2_median (+ _iqr_lower/_iqr_upper or _range_lower/_range_upper):
              ONLY fill when the paper reports medians instead of means for a continuous outcome.
              Fill IQR or range, whichever the paper actually reports -- never both, never invent
              one from the other. Both arms must use the SAME shape (median+IQR for both, or
              median+range for both) to be usable."""
            if not phase_done["map"]:
                return "ERROR: call record_paper_map (Phase 1) first."
            paper_results.append({
                "paper_id": paper_id,
                "paper_title": paper_title,
                "true_research_question": true_research_question,
                "author": author,
                "publication_year": publication_year,
                "publication_status": publication_status,
                "design_type": design_type,
                "domain": domain,
                "study_environment": study_environment,
                "country": country,
                "study_year": study_year,
                "llm_model": llm_model,
                "medium": medium,
                "content_length": content_length,
                "topic_of_content": topic_of_content,
                "interaction_type": interaction_type,
                "participant_type": participant_type,
                "recruitment_source": recruitment_source,
                "study_label": study_label,
                "outcome_selection_reason": outcome_selection_reason,
                "is_independent_study": is_independent_study,
                "task_or_measure": task_or_measure,
                "outcome_name": outcome_name,
                "outcome_type": outcome_type,
                "outcome_measurement": outcome_measurement,
                "result_role": result_role,
                "comparison_type": comparison_type,
                "group_1_label": group_1_label,
                "group_1_n": group_1_n,
                "group_1_mean": group_1_mean,
                "group_1_sd": group_1_sd,
                "group_1_se": group_1_se,
                "group_1_mean_emm": group_1_mean_emm,
                "group_1_mean_perc": group_1_mean_perc,
                "group_1_ci_lower": group_1_ci_lower,
                "group_1_ci_upper": group_1_ci_upper,
                "group_1_is_control": group_1_is_control,
                "group_2_label": group_2_label,
                "group_2_n": group_2_n,
                "group_2_mean": group_2_mean,
                "group_2_sd": group_2_sd,
                "group_2_se": group_2_se,
                "group_2_mean_emm": group_2_mean_emm,
                "group_2_mean_perc": group_2_mean_perc,
                "group_2_ci_lower": group_2_ci_lower,
                "group_2_ci_upper": group_2_ci_upper,
                "additional_group_ns": additional_group_ns,
                "n_total": n_total,
                "ci_level": ci_level,
                "statistic_type": statistic_type,
                "df1": df1,
                "df2": df2,
                "test_statistic": test_statistic,
                "p_value": p_value,
                "effect_size_name": effect_size_name,
                "effect_size_value": effect_size_value,
                "odds_ratio": odds_ratio,
                "ci_lower_or": ci_lower_or,
                "ci_upper_or": ci_upper_or,
                "risk_ratio": risk_ratio,
                "ci_lower_rr": ci_lower_rr,
                "ci_upper_rr": ci_upper_rr,
                "hazard_ratio": hazard_ratio,
                "ci_lower_hr": ci_lower_hr,
                "ci_upper_hr": ci_upper_hr,
                "group_1_events": group_1_events,
                "group_1_total": group_1_total,
                "group_2_events": group_2_events,
                "group_2_total": group_2_total,
                "group_1_median": group_1_median,
                "group_1_iqr_lower": group_1_iqr_lower,
                "group_1_iqr_upper": group_1_iqr_upper,
                "group_1_range_lower": group_1_range_lower,
                "group_1_range_upper": group_1_range_upper,
                "group_2_median": group_2_median,
                "group_2_iqr_lower": group_2_iqr_lower,
                "group_2_iqr_upper": group_2_iqr_upper,
                "group_2_range_lower": group_2_range_lower,
                "group_2_range_upper": group_2_range_upper,
                "M_diff": M_diff,
                "SE_diff": SE_diff,
                "reported_effect_measure": reported_effect_measure,
                "outcome_units": outcome_units,
                "outcome_scale_min": outcome_scale_min,
                "outcome_scale_max": outcome_scale_max,
                "outcome_unit_conversion_factor": outcome_unit_conversion_factor,
                "outcome_units_canonical": outcome_units_canonical,
                "evidence_quote": evidence_quote,
                "page_or_section": page_or_section,
                "extraction_warning": extraction_warning,
            })
            return "result_recorded"

        study_map = study_maps.get(paper.id, {})
        rq_map    = rq_maps.get(paper.id, {})
        text = (paper.full_text or paper.abstract or "")[:_MAX_CHARS]

        # Build study-map context block exactly as the original agent did
        study_context = ""
        if study_map and study_map.get("studies"):
            lines = [
                f"\nStudy map ({study_map['total_studies']} study/studies "
                "from StudyDetectorAgent — use these study_label values exactly):"
            ]
            for s in study_map["studies"]:
                outcomes = ", ".join(s.get("primary_outcomes", [])) or "—"
                n_info = f"  N={s['n_total']}" if s.get("n_total") else ""
                lines.append(
                    f"  [{s['study_label']}]{n_info}\n"
                    f"    Design: {s.get('design', '—')}\n"
                    f"    Treatment: {s.get('treatment_group_label', '—')} "
                    f"vs Control: {s.get('control_group_label', '—')}\n"
                    f"    Primary outcomes: {outcomes}\n"
                    f"    Results at: {s.get('results_location', '—')}"
                )
            study_context = "\n".join(lines)

        # Build effect context block from ResearchQuestionDetectorAgent output
        rq_context = ""
        rq_list = rq_map.get("research_questions", [])
        if rq_list:
            lines = [
                f"\nPre-identified effects to extract ({len(rq_list)} total — ONE per distinct study × outcome × comparison):"
            ]
            for rq in rq_list:
                lines.append(
                    f"  [{rq.get('effect_id', '?')}] "
                    f"{'(PRIMARY) ' if rq.get('is_primary_outcome') else ''}"
                    f"Construct: {rq.get('target_construct', '—')}\n"
                    f"    Outcome variable: {rq.get('primary_outcome', '—')}\n"
                    f"    Treatment: {rq.get('treatment_description', '—')}\n"
                    f"    Control:   {rq.get('control_description', '—')}\n"
                    f"    Direction: {rq.get('effect_direction', '—')}\n"
                    f"    Results at: {rq.get('result_section_hint', '—')}"
                )
            # Results sections that contain statistics
            stat_sections = [
                s for s in rq_map.get("content_sections", [])
                if s.get("contains_statistics")
            ]
            if stat_sections:
                lines.append("\nSections that contain statistics:")
                for s in stat_sections:
                    linked = ", ".join(s.get("linked_rq_ids") or []) or "—"
                    lines.append(
                        f"  {s.get('section_title', s.get('section_id', '?'))} "
                        f"(pages {s.get('page_range', '?')}) — effects: {linked}"
                    )
            rq_context = "\n".join(lines)

        user_msg = (
            f"Analyse this paper in two mandatory phases.\n\n"
            "CRITICAL — ANTI-HALLUCINATION: Only record numbers found VERBATIM in the "
            "text. Leave any field empty (null) if the value is not explicitly stated. "
            "A missing field is always better than an invented number.\n\n"
            f"Paper ID : {paper.id}\n"
            f"Title    : {paper.title}\n"
            f"Abstract :\n{paper.abstract}\n"
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "SYNTHESIS PLAN — THIS IS THE EXTRACTION CONTRACT\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{synthesis_plan_text}\n"
            "Only extract rows that can contribute to this planned treatment-vs-control "
            "and outcome synthesis. If a paper has many hypotheses, ignore hypotheses "
            "whose constructs, groups, or outcomes do not match this contract. "
            "When a paper reports multiple analyses for the same construct, prefer "
            "the primary/preregistered outcome and the direct treatment-vs-control "
            "comparison.\n"
            "MATCH BY MEANING, NOT EXACT WORDING: a paper very often reports one of the "
            "plan's outcomes under different terminology than the plan itself uses -- e.g. "
            "'overall survival' or 'time to death' is the same construct as 'mortality'; "
            "'rehospitalization' or 'hospital utilization' is the same as 'hospital "
            "readmission'; 'ED visit' or 'emergency room contact' is the same as 'emergency "
            "department contact'. Before deciding a paper doesn't report one of the plan's "
            "outcomes, actively check whether it appears under a clinical synonym anywhere in "
            "the abstract, results, or a results table -- do not require the plan's exact "
            "words to appear in the paper. This applies symmetrically to every outcome in the "
            "plan, whatever they are for this particular review -- never assume any one "
            "construct is more likely to be paraphrased than another.\n"
            f"{study_context}\n"
            f"{rq_context}\n\n"
            f"Full text:\n{text}\n\n"
            "CRITICAL — VALUE VALIDITY RULES (applies to ALL numeric fields, "
            "especially SD_control, SD_treatment, cohens_d, hedges_g, M_diff, SE_diff):\n"
            "  1. Direct extraction: if a value is explicitly reported → extract it.\n"
            "  2. Valid computation: compute ONLY if ALL required inputs are explicitly "
            "available and compatible:\n"
            "       • cohens_d / hedges_g requires: group means + SDs + group sizes\n"
            "       • SE_diff requires: SDs + sample sizes for both groups\n"
            "       • M_diff: compute as group_2_mean − group_1_mean ONLY if (a) both "
            "means are explicitly reported, (b) the design is a simple two-group "
            "comparison (single factor, between-subjects), and (c) both means represent "
            "that exact comparison — not marginal means from a factorial ANOVA.\n"
            "  3. Do NOT compute if:\n"
            "       • any required input is missing\n"
            "       • inputs come from subgroups, moderators, or different analyses\n"
            "       • the study uses complex designs (multi-level ANOVA, interaction "
            "effects) without clear group-level statistics\n"
            "       • M_diff — ADDITIONAL PROHIBITIONS:\n"
            "           – NEVER compute M_diff from marginal means in a 2×2, 2×3, or "
            "any multi-factor ANOVA. Marginal means represent factor-level averages, "
            "NOT a simple treatment vs. control comparison.\n"
            "           – NEVER compute M_diff by averaging differences across multiple "
            "studies or conditions.\n"
            "           – NEVER compute M_diff when group_1_mean and group_2_mean come "
            "from different factors, different conditions, or different tables.\n"
            "           – If unsure whether the means represent a simple two-group "
            "comparison, leave M_diff empty.\n"
            "  4. NEVER: assign 0 as a default, approximate, guess, mix values from "
            "different tables or conditions, or compute from F-values / p-values alone.\n"
            "  5. Consistency check: if a computed value seems inconsistent with the "
            "reported statistics → discard it and leave the field empty.\n"
            "  6. Final rule: if a value is NOT explicitly reported AND cannot be "
            "correctly computed from explicitly reported inputs → LEAVE THE FIELD EMPTY.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "PHASE 1 — UNDERSTAND  (call record_paper_map EXACTLY ONCE, RIGHT NOW)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Before extracting any numbers, build a structural map of the paper:\n"
            "  • paper_type and study_design (what kind of study is this?)\n"
            "  • comparison_type (between-subjects, within-subjects, mixed, …)\n"
            "  • main_groups: what are the treatment and control group labels?\n"
            "  • studies: list every independent study / experiment with its sample size\n"
            "    and where its results appear (table number, section, page).\n"
            "  • outcomes: list every outcome variable with its role "
            "(primary / secondary / manipulation check / …)\n"
            "    and the statistics reported for it.\n"
            "  • hypotheses: list every hypothesis or research question explicitly stated\n"
            "    in the paper (H1, H2, RQ1, …). For each hypothesis record:\n"
            "      - hypothesis_id (e.g. 'H1')\n"
            "      - hypothesis_text (verbatim or close paraphrase)\n"
            "      - linked_outcome: the outcome variable name that directly tests this\n"
            "        hypothesis (must match a name in your outcomes list)\n"
            "      - study_label: which study tests this hypothesis\n"
            "      - direction: the predicted direction (if stated)\n"
            "    If the paper has no explicit hypothesis labels, create one entry per\n"
            "    primary research question inferred from the Introduction/Methods.\n"
            "  • results_sections: name the sections / pages that contain THIS paper's\n"
            "    own statistics — you will extract only from these locations in Phase 2.\n\n"
            "Call record_paper_map now. Do not call record_statistical_result yet.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "PHASE 2 — EXTRACT  (call record_statistical_result per result row)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            + (
                f"SYNTHESIS PLAN:\n{synthesis_plan_text}\n"
                + (
                    "STUDY AND OUTCOME SELECTION RULE — apply this before recording anything:\n\n"
                    "  The pre-identified effects listed above are your primary guide.\n"
                    "  Each effect = ONE distinct (study × outcome × comparison) triplet.\n"
                    "  Your goal: extract ONE statistical result row per pre-identified effect.\n\n"
                    "  STEP 1 — EFFECT RELEVANCE CHECK\n"
                    "  For each pre-identified effect, verify that its treatment, control,\n"
                    "  and outcome match the synthesis plan above. An effect is RELEVANT\n"
                    "  only if it measures the planned outcome or a direct proxy for it.\n"
                    "  SKIP effects whose construct, comparison, or population is clearly different.\n\n"
                    "  STEP 2 — EXTRACTION (one row per relevant effect)\n"
                    "  For each relevant effect, go to the result_section_hint location,\n"
                    "  find the statistics for that outcome variable, and call\n"
                    "  record_statistical_result ONCE for that effect.\n\n"
                    "  DEDUPLICATION: If two effect IDs test the same outcome in the same\n"
                    "  study via the same comparison, extract only ONE row (use the primary).\n\n"
                    "  SKIP: manipulation checks, demographic outcomes, covariate measures,\n"
                    "  and any effect that measures a clearly different construct.\n"
                    if rq_list else
                    "No effects were pre-identified for this paper. "
                    "Extract ALL primary outcomes from the results sections "
                    "that directly match the synthesis plan above. "
                    "Focus especially on comparisons between the treatment and control groups. "
                    "Do not skip any result that is plausibly related to the query — "
                    "it is better to over-extract than to miss a relevant result.\n\n"
                )
                if user_query else
                "Use the paper map you just built as your guide. Work through every\n"
                "results section identified in Phase 1.\n\n"
            )
            + "Extraction rules:\n\n"
            "1.  Extract one row per outcome-level statistical result.\n"
            "2.  Only extract statistics from this paper's own Results sections.\n"
            "    NEVER extract from Introduction, Related Work, or Discussion.\n"
            "3.  STUDY LABEL — this is the most common error, so read carefully:\n"
            "    Every result row MUST carry the study_label of the SPECIFIC independent\n"
            "    study it comes from.  Use the study map above — it lists every study\n"
            "    with its label, design, and results_location.  Match each result to the\n"
            "    correct study by table number, section heading, or page.  If the paper\n"
            "    has Study 1, Study 2, and Study 3, results from Study 2 MUST carry\n"
            "    study_label='Study 2' — never 'Study 1'.  Check every row before\n"
            "    recording it.\n"
            "4.  Always identify task_or_measure and outcome_name before recording numbers.\n"
            "5.  Do not attach a statistic to an outcome unless the paper links them.\n"
            "6.  Every number must have an evidence_quote and page_or_section.\n"
            "7.  Leave group means/SDs empty when not stated — NEVER fill with 0.\n"
            "8.  For t(df)=value: df1=df, df2=null. Never use df2=0.\n"
            "9.  For F(df1,df2)=value: extract df1, df2, test_statistic correctly.\n"
            "10. Sample sizes — always use FINAL ANALYSED N, not enrolled N.\n"
            "    Per-group Ns in table headers/footnotes take priority; fallback to Methods.\n"
            "    DF inference: independent t-test df = n1+n2-2; one-way ANOVA df_within = N-k.\n"
            "11. Two groups matched one-to-one → comparison_type='matched'.\n"
            "12. b=… coefficients → store in the coefficient field, not test_statistic.\n"
            "13. 2×2 ANOVA → THREE separate rows (main effect A, main effect B, interaction).\n"
            "14. M_diff / SE_diff for regression and mixed models:\n"
            "    • If the paper reports an unstandardized coefficient b (and no per-group means),\n"
            "      store b in M_diff.\n"
            "    • SE_diff: store SE(b) if directly reported.\n"
            "      If SE(b) is NOT reported but a 95% CI for the coefficient IS reported,\n"
            "      compute SE = (CI_upper − CI_lower) / 3.92 and store it in SE_diff;\n"
            "      note this derivation in extraction_warning.\n"
            "    • For non-regression designs: compute M_diff = group_2_mean − group_1_mean\n"
            "      ONLY when both means are explicit and the design is simple two-group\n"
            "      between-subjects. NEVER compute from marginal means in factorial ANOVA.\n"
            + _DIFF_FALLBACK_RULE() +
            "15. Trial/study with 3+ arms/conditions reporting the SAME outcome: first check "
            "whether exactly TWO of the reported arms match this paper's own "
            "\"Treatment/intervention to extract\" and \"Control/comparator to extract\" "
            "definitions above (e.g. a 3-arm trial of control vs. brief-dose vs. extended-dose "
            "PCIT, where the review's own plan defines the adapted/extended arm as the "
            "intervention and only ONE other arm as its comparator). When they do, extract "
            "those TWO arms' own raw means/SDs/Ns into group_1_*/group_2_* exactly as you would "
            "for a normal two-arm trial -- do NOT fall back to an omnibus statistic just because "
            "a 3rd arm exists. Record every OTHER reported arm (the one(s) not chosen) in "
            "additional_group_ns per its own docstring above, so the exclusion is auditable, "
            "never silent. Only fall back to extracting eta_squared/partial_eta_squared into "
            "effect_size_name + effect_size_value for the genuine omnibus case: when NO clean "
            "1-to-1 mapping exists between the reported arms and this review's treatment/control "
            "definitions (e.g. a true dose-response curve across several dose levels with no arm "
            "matching \"control\", or a factorial interaction effect).\n"
            "16. Regression / mixed models: extract t-value for the treatment coefficient;\n"
            "    if not given, compute t = b / SE(b) and store in test_statistic;\n"
            "    note the derivation in extraction_warning.\n"
            "17. Paper metadata (author, year, country, design_type, domain, llm_model,\n"
            "    medium, participant_type) is the SAME for every row — fill consistently.\n"
            + (
                "18. Extract ONE row per pre-identified effect — use effect_id as your\n"
                "    checklist. Do not add extra rows beyond the pre-identified effects\n"
                "    unless an effect was clearly missed by the detector.\n"
                if (user_query and rq_list) else
                "18. Extract ALL outcome variables — do not stop after the first.\n"
            )
            + "19. reported_effect_measure: fill ONLY when the paper's own results text names its "
              "effect measure explicitly (e.g. states \"reported as a risk ratio\"). Do NOT fill it "
              "just because you extracted an odds_ratio/M_diff/other numeric field — those are "
              "separate, purely numeric fields. Do NOT guess a measure from event counts alone: "
              "dichotomous counts alone never tell you whether the paper intended risk ratio or "
              "odds ratio. outcome_units: fill ONLY when the paper explicitly states the outcome's "
              "natural unit or instrument scale — leave empty if unsure, never guess from a "
              "matching label across studies.\n"
              "20. For dichotomous (event/non-event) outcomes, always extract group_1_events/"
              "group_1_total and group_2_events/group_2_total directly from the paper's own 2x2 "
              "counts when reported — this preserves the ability to pool on the native scale "
              "instead of always converting to a standardized effect size. Dichotomous counts "
              "(dropout/attrition, mortality, relapse, adverse events, and similar event-type "
              "outcomes) are very often reported as NARRATIVE PROSE in the Results/Attrition/"
              "Sample-Selection text rather than as a labeled table — e.g. \"5.9% [4/70] vs. "
              "21.9% [14/64]\" or \"15 (33%) of the 46 participants... 7 from the SP condition "
              "and 8 from CBT\" embedded in a paragraph. Read these sections as carefully as any "
              "table for the outcome you are extracting — do not conclude a paper has no usable "
              "quantitative data for it just because the numbers are not in a table; a fraction "
              "or percentage-of-N stated in running text is exactly as usable as a table cell.\n"
              "21. group_1_is_control: ALWAYS fill this (True or False) whenever you fill "
              "group_1_label/group_2_label. Decide it from your own understanding of the paper "
              "and the \"Treatment/intervention to extract\" / \"Control/comparator to extract\" "
              "definitions above — NEVER from label wording heuristics (a control arm is often "
              "an ACTIVE comparator such as \"supportive therapy\", \"treatment as usual\", or a "
              "different psychosocial intervention, not something that literally says "
              "\"control\"). If the paper's own table lists the intervention arm first, put it "
              "in group_1 exactly as the paper does, and set group_1_is_control=False — do not "
              "reorder the numbers to force group_1 into being the control arm; the boolean is "
              "what tells downstream code the true arm identity, not the field position.\n"
              "22. outcome_scale_min/outcome_scale_max: fill BOTH only when the paper explicitly "
              "states the instrument's fixed numeric range (e.g. \"100 mm visual analogue scale\" "
              "-> min=0, max=100; \"Numerical Rating Scale, 0-10\" -> min=0, max=10). Leave BOTH "
              "empty otherwise — never guess a range from convention, from the observed data's "
              "own min/max, or from what a scale \"usually\" spans.\n"
              "23. outcome_unit_conversion_factor/outcome_units_canonical: when outcome_units is "
              "a lab/clinical unit with a fixed, textbook conversion to a different standard "
              "unit FOR THE EXACT ANALYTE NAMED (e.g. triglycerides mg/dL -> mmol/L, factor "
              "0.0113; cholesterol mg/dL -> mmol/L, factor 0.0259; glucose mg/dL -> mmol/L, "
              "factor 0.0555), fill both so this row's means/SDs can be put on the same unit as "
              "other studies of the same outcome. Do this consistently — do not convert one "
              "study's units while leaving another study of the SAME outcome unconverted; if you "
              "are not certain of the exact constant, leave both empty rather than guessing.\n"
              "24. Standard error vs. standard deviation — these are NOT interchangeable and must "
              "never be conflated. If the paper explicitly reports a standard DEVIATION for a "
              "group's mean, fill group_1_sd/group_2_sd as usual. If it instead reports a "
              "standard ERROR (common for least-squares/adjusted/estimated marginal means from "
              "an ANCOVA, mixed model, or repeated-measures analysis — often labeled \"SE\", "
              "\"SEM\", or shown as a small value next to an adjusted mean in a results table), "
              "fill group_1_se/group_2_se INSTEAD — never put an SE value into the _sd field, "
              "and never invent an SD by guessing a conversion yourself. Downstream code converts "
              "a reported SE to SD automatically (SD = SE x sqrt(n)) once you tag it correctly as "
              "SE; your only job is to report the paper's own number under its own correct label.\n"
        )

        try:
            agent = create_react_agent(
                llm,
                [record_paper_map, record_statistical_result],
                prompt=SYSTEM_PROMPT,
            )
            agent.invoke({"messages": [("user", user_msg)]})
            logger.info(
                f"[Extraction] {paper.id}: {len(paper_results)} results extracted."
            )
            # Warn when a multi-study paper has all results on one study label
            n_detected = study_map.get("total_studies", 0)
            if n_detected > 1 and paper_results:
                used_labels = {r.get("study_label") for r in paper_results}
                if len(used_labels) == 1:
                    logger.warning(
                        f"[Extraction] {paper.id}: {n_detected} studies detected "
                        f"but all {len(paper_results)} results carry label "
                        f"'{next(iter(used_labels))}'. "
                        "Study labels may be wrong — check study_maps.json."
                    )
        except Exception as exc:
            logger.error(f"[Extraction] {paper.id}: skipped due to error — {exc}")

        all_results.extend(paper_results)
        all_paper_maps[paper.id] = paper_map

    save_json(all_paper_maps, os.path.join(output_dir, "paper_maps.json"))
    save_json(all_results,    os.path.join(output_dir, "paper_results.json"))

    logger.info(f"[Extraction] Total: {len(all_results)} result rows across {len(papers)} papers.")
    return {"paper_results": all_results}
