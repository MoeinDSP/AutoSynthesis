"""Planning agent — Stage 0. Converts user prompt → MetaAnalysisPlan."""

import logging
import os
from typing import List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from core_utils import save_json
from models import EffectMeasure, MetaAnalysisPlan
from pipeline_graph import _extract_tool_args, GraphState

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an expert meta-analyst and systematic review methodologist. "
    "A user has given you a research question. Your job is to design a "
    "complete meta-analysis plan for that question following PRISMA 2020 guidelines.\n\n"
    "You must call `create_plan` with ALL fields filled in. Be specific:\n"
    "  - treatment_label / control_label: the two conditions being compared "
    "(e.g. 'LLM-generated persuasive text' vs 'human-written persuasive text').\n"
    "  - search_queries: 2-3 short keyword strings optimised for academic database "
    "search (not Boolean syntax -- just keyword phrases). Each query should include "
    "the intervention/topic plus empirical intent words when natural, such as "
    "'experiment', 'trial', 'controlled', 'comparison', 'quantitative', 'outcome', "
    "or 'effect'. Avoid queries that mainly retrieve reviews or meta-analyses.\n"
    "  - inclusion_criteria: 2-3 BROAD, permissive criteria. Keep them general — "
    "err heavily on the side of inclusion. A paper only needs to be broadly related "
    "to the topic and report some quantitative outcome. Do NOT add strict design, "
    "sample-size, or journal-quality requirements.\n"
    "  - exclusion_criteria: 3-4 exclusion reasons that MUST include: "
    "(1) not an original empirical study (systematic reviews, meta-analyses, "
    "editorials, opinion pieces, and theoretical papers are excluded); "
    "(2) no comparison between a treatment and a control condition; "
    "(3) no quantitative outcome data that can produce an effect size "
    "(means+SDs, t/F-values, proportions, or odds ratios required); "
    "(4) completely unrelated to the research topic.\n"
    "  - moderators_to_extract: 3-6 study-level variables that could explain "
    "heterogeneity (e.g. 'study design', 'topic domain', 'sample size category').\n"
    "  - positive_direction: what a POSITIVE Hedges g means in plain language.\n"
    "  - higher_score_is_worse: True when a HIGHER raw score on the outcome measure means a "
    "WORSE result (e.g. a symptom-severity, problem-count, or pain scale -- more = worse). "
    "False when a HIGHER raw score means a BETTER result (e.g. a function, quality-of-life, "
    "or skill scale -- more = better). This must be consistent with positive_direction: it is "
    "used to correctly sign the computed effect size so a positive value always means the "
    "outcome favors the treatment, matching what positive_direction says.\n"
    "  - search_start_year: sensible earliest year (e.g. 2015 for LLM topics, "
    "1990 for clinical trials).\n"
    "  - target_effect_measure: ONLY fill this when the user's OWN prompt explicitly requests "
    "a specific pooling measure (e.g. \"pool this as an odds ratio\", \"report results as a risk "
    "ratio\", \"pool using risk difference\"). One of RR, OR, PETO_OR, RD, HR, MD, SMD, HEDGES_G, "
    "GENERIC — RD (Risk Difference) when the user says \"risk difference\"/\"RD\", HR (Hazard "
    "Ratio) when the user says \"hazard ratio\"/\"HR\". Leave it unset (null) in every other case "
    "— do NOT infer a measure from the topic or outcome type, and never substitute GENERIC just "
    "because the user's exact wording isn't RR/OR/MD/SMD. Most requests will leave this null, and "
    "that is the expected, normal outcome.\n"
    "  - pooling_model: ONLY fill this when the user's OWN prompt explicitly asks for a specific "
    "meta-analytic model. One of FE (fixed effect / common effect), REML, DL (DerSimonian-Laird), "
    "ML, HE, HS (Hunter-Schmidt), SJ (Sidik-Jonkman), PM (Paule-Mandel), EB, UWLS (unrestricted "
    "weighted least squares). A request for \"a random-effects model\" without naming an estimator "
    "is REML. Leave it null in every other case -- do NOT choose a model yourself from the topic.\n"
    "  - split_by_timepoint: default False. Set True ONLY when the user's OWN prompt explicitly "
    "asks for separate results at different follow-up times (e.g. \"report results separately at "
    "3 months and 12 months\", \"analyze short-term and long-term effects as distinct outcomes\"). "
    "The default (False) means each outcome is pooled as ONE number across all its studies "
    "regardless of each study's individual follow-up length — the standard systematic-review "
    "convention. Do NOT set this True just because studies report different follow-up times; only "
    "set it when the user explicitly wants that split as the analysis structure.\n"
    "  - single_outcome_target: leave null in the normal case (the user's question spans several "
    "outcomes, or a broad clinical/functional battery, or doesn't name one specific construct). "
    "Set it ONLY when the user's OWN question explicitly asks about ONE specific, singular "
    "outcome/construct and nothing else (e.g. \"effect on mortality\", \"effect on positive "
    "symptoms of psychosis\", \"effect on depression scores\") — a short, canonical name for that "
    "one construct, e.g. \"positive symptoms of psychosis\". When set, every result across all "
    "papers that measures this construct gets pooled into ONE group regardless of which specific "
    "instrument/scale a study used to measure it (e.g. PANSS vs BPRS vs SAPS positive-symptom "
    "subscales all count as the same target construct) — do NOT set this for a broad question "
    "like \"effect on symptoms and functioning and quality of life\", only for a genuinely "
    "single-outcome question.\n"
)


@tool
def create_plan(
    research_question: str,
    treatment_label: str,
    control_label: str,
    outcome_description: str,
    positive_direction: str,
    higher_score_is_worse: bool,
    search_queries: List[str],
    inclusion_criteria: List[str],
    exclusion_criteria: List[str],
    moderators_to_extract: List[str],
    search_start_year: int,
    effect_size_note: Optional[str] = None,
    target_effect_measure: Optional[str] = None,
    split_by_timepoint: Optional[bool] = None,
    single_outcome_target: Optional[str] = None,
    pooling_model: Optional[str] = None,
) -> str:
    """Submit the complete meta-analysis plan. Call this once with all fields filled in.
    higher_score_is_worse: True for a symptom/problem/severity scale where a higher raw score
    is a worse result (e.g. ECBI, PHQ-9, pain VAS); False for a function/quality-of-life/skill
    scale where a higher raw score is a better result. Must agree with positive_direction.
    target_effect_measure: only set when the USER explicitly requested a specific pooling
    measure -- leave null otherwise (the normal case).
    split_by_timepoint: only set True when the USER explicitly asked for separate
    short-term/long-term (or similarly timepoint-based) results -- leave null/False otherwise
    (the normal case; each outcome is pooled as one number across all its studies by default).
    single_outcome_target: only set when the USER's question names ONE specific, singular
    outcome/construct and nothing else -- leave null otherwise (the normal, multi-outcome case).
    pooling_model: only set when the USER explicitly asked for a specific meta-analytic model
    (FE, REML, DL, ML, HE, HS, SJ, PM, EB or UWLS) -- leave null otherwise."""
    return "plan_created"


_agent = create_react_agent(llm, [create_plan], prompt=SYSTEM_PROMPT)


# Required MetaAnalysisPlan fields (no default) that create_plan must supply --
# checked before construction so a model that omits one gets a targeted
# retry asking specifically for what it left out, instead of a raw Pydantic
# ValidationError crashing the whole run. We never fabricate a value for
# any of these ourselves -- they're semantic judgments only the LLM can make.
_REQUIRED_PLAN_FIELDS = [
    "research_question", "treatment_label", "control_label",
    "outcome_description", "positive_direction", "higher_score_is_worse", "search_queries",
    "inclusion_criteria", "exclusion_criteria", "moderators_to_extract",
]


def _missing_plan_fields(args: dict) -> list[str]:
    missing = []
    for field in _REQUIRED_PLAN_FIELDS:
        value = args.get(field)
        if value is None or (isinstance(value, (str, list)) and not value):
            missing.append(field)
    return missing


def plan_node(state: GraphState) -> dict:
    """Stage 0: generate MetaAnalysisPlan from user_prompt."""
    logger.info("=== STAGE 0: Planning ===")
    logger.info("[PlanningAgent] Generating meta-analysis plan...")
    messages = [(
        "user",
        f"Design a complete meta-analysis plan for:\n\n{state['user_prompt']}\n\n"
        "Call `create_plan` with all fields filled in.",
    )]
    args: dict = {}
    missing: list[str] = _REQUIRED_PLAN_FIELDS
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        result = _agent.invoke({"messages": messages})
        args = _extract_tool_args(result["messages"], "create_plan")
        if not args:
            logger.warning(f"[PlanningAgent] Attempt {attempt}/{max_attempts}: no create_plan call at all.")
            missing = _REQUIRED_PLAN_FIELDS
        else:
            missing = _missing_plan_fields(args)
        if not missing:
            break
        logger.warning(
            f"[PlanningAgent] Attempt {attempt}/{max_attempts}: create_plan call is missing "
            f"required field(s) {missing} -- retrying with a corrective follow-up."
        )
        messages = list(result["messages"]) + [(
            "user",
            f"Your create_plan call was missing required field(s): {', '.join(missing)}. "
            "Call `create_plan` again with EVERY field filled in, including these.",
        )]
    if missing:
        raise RuntimeError(
            f"[PlanningAgent] Failed to generate a complete plan after {max_attempts} attempts -- "
            f"still missing required field(s) {missing}. Check API key and model settings."
        )
    # target_effect_measure: only accept a value that maps onto a real
    # EffectMeasure -- an unrecognised/malformed string from the LLM must
    # not crash plan creation or be silently coerced into a guess.
    raw_measure = args.get("target_effect_measure")
    if raw_measure:
        try:
            args["target_effect_measure"] = EffectMeasure(str(raw_measure).strip().upper())
        except ValueError:
            logger.warning(
                f"[PlanningAgent] Ignoring unrecognised target_effect_measure={raw_measure!r} "
                "from the LLM -- leaving it unset rather than guessing."
            )
            args["target_effect_measure"] = None
    # split_by_timepoint: coerce to a plain bool, defaulting False -- an
    # unset/None/malformed value from the LLM must never accidentally enable
    # timepoint fragmentation (see models.MetaAnalysisPlan.split_by_timepoint).
    args["split_by_timepoint"] = bool(args.get("split_by_timepoint") or False)
    # higher_score_is_worse: coerce to a plain bool, defaulting False -- an unset/None/malformed
    # value from the LLM must never accidentally flip a sign it wasn't explicitly asked to
    # (see models.MetaAnalysisPlan.higher_score_is_worse).
    args["higher_score_is_worse"] = bool(args.get("higher_score_is_worse") or False)
    # single_outcome_target: coerce a blank/whitespace-only string to None --
    # an empty-but-truthy-looking value must not accidentally activate the
    # single-outcome pooling override (see models.MetaAnalysisPlan and
    # agents/cross_paper_outcome_mapper_agent.py's mapping_node()).
    raw_target = args.get("single_outcome_target")
    args["single_outcome_target"] = raw_target.strip() if raw_target and raw_target.strip() else None
    # pooling_model: the dashboard's explicit choice (state["pooling_model"]) wins over a
    # model the LLM read from the prompt; anything unrecognised is dropped (default REML).
    from statistics.metafor_engine import POOLING_MODELS
    chosen = state.get("pooling_model") or args.get("pooling_model")
    chosen = str(chosen).strip().upper() if chosen else None
    if chosen in ("EE", "CE", "FIXED", "COMMON"):
        chosen = "FE"
    if chosen and chosen not in POOLING_MODELS:
        logger.warning(f"[PlanningAgent] Ignoring unrecognised pooling_model={chosen!r} -- using the default (REML).")
        chosen = None
    args["pooling_model"] = chosen
    plan = MetaAnalysisPlan(**args)
    if plan.pooling_model:
        logger.info(f"[PlanningAgent] Pooling model: {POOLING_MODELS[plan.pooling_model]}")
    if plan.target_effect_measure:
        logger.info(f"[PlanningAgent] User explicitly requested target_effect_measure={plan.target_effect_measure.value}")
    if plan.single_outcome_target:
        logger.info(f"[PlanningAgent] Single-outcome mode: single_outcome_target={plan.single_outcome_target!r}")
    output_dir = state.get("output_dir")
    if output_dir:
        save_json(plan.model_dump(), os.path.join(output_dir, "plan.json"))
    logger.info(f"[PlanningAgent] Plan: RQ={plan.research_question!r}")
    return {"plan": plan}
