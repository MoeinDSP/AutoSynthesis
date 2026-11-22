"""Research Question Detector — Stage 3B. Pattern 1: per-paper record-output tools.

Takes the full text produced by PaperReadingAgent and outputs two artefacts per paper:
  1. research_questions — list of RQs / hypotheses actually tested, each with
       its comparison, target construct, outcomes, and pointer to the result section.
  2. content_sections  — the paper sliced into labelled sections so the extractor
       works on the right slice instead of the whole document.

The combined output is stored in state["rq_maps"] and passed to the extractor
so it knows (a) what to look for and (b) exactly where in the document to find it.
"""

import logging
import os
from typing import Annotated, Any, Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import Field

from agents.llm import llm
from models import PaperRecord
from pipeline_graph import _all_tool_args, GraphState
from core_utils import save_json

logger = logging.getLogger(__name__)

_MAX_CHARS = 80_000

SYSTEM_PROMPT = (
    "You are a scientific meta-analysis extraction specialist.\n\n"
    "Your task is NOT to extract every statistical analysis or every hypothesis in the paper.\n\n"
    "Your task is to extract ONLY the experimentally tested effects that are directly "
    "relevant to the synthesis objective provided by the user.\n\n"
    "The synthesis objective defines:\n"
    "  * which constructs are relevant,\n"
    "  * which outcomes are primary,\n"
    "  * and which analyses should be ignored.\n\n"
    "--------------------------------------\n"
    "GENERAL EXTRACTION RULES\n"
    "--------------------------------------\n\n"
    "Extract:\n"
    "  * primary experimentally tested effects\n"
    "  * preregistered or central outcomes\n"
    "  * statistically evaluated comparisons directly relevant to the synthesis objective\n\n"
    "Do NOT extract:\n"
    "  * manipulation checks\n"
    "  * robustness checks\n"
    "  * mediation analyses\n"
    "  * moderation analyses unless central\n"
    "  * exploratory analyses\n"
    "  * manipulation validation\n"
    "  * linguistic/process variables\n"
    "  * descriptive-only statistics\n"
    "  * supplementary analyses\n"
    "  * subgroup analyses unless central to the paper's main claim\n\n"
    "--------------------------------------\n"
    "UNIT OF EXTRACTION\n"
    "--------------------------------------\n\n"
    "The unit of extraction is:\n"
    "ONE DISTINCT EFFECT RELEVANT TO THE SYNTHESIS OBJECTIVE\n\n"
    "NOT:\n"
    "  * every table row\n"
    "  * every regression\n"
    "  * every statistical test\n\n"
    "If multiple analyses test the same construct:\n"
    "extract only the primary/preferred/main analysis.\n\n"
    "--------------------------------------\n"
    "PRIORITIZATION\n"
    "--------------------------------------\n\n"
    "Prioritize:\n"
    "  1. Primary outcomes\n"
    "  2. Preregistered outcomes\n"
    "  3. Main experimental contrasts\n"
    "  4. Central claims in abstract/results/discussion\n\n"
    "If uncertain whether an effect is central:\n"
    "prefer inclusion — it is better to over-extract than to miss a relevant effect.\n\n"
    "--------------------------------------\n"
    "OUTPUT PHILOSOPHY\n"
    "--------------------------------------\n\n"
    "You are building a CLEAN SYNTHESIS DATASET,\n"
    "not a complete theory map.\n\n"
    "Fewer highly relevant effects are preferred over many weakly related analyses."
)

_agent = None


def _get_agent():
    global _agent
    if _agent is None:
        _agent = create_react_agent(
            llm,
            [record_relevant_effect, record_content_section],
            prompt=SYSTEM_PROMPT,
        )
    return _agent


@tool
def record_relevant_effect(
    paper_id: str,
    effect_id: Annotated[str, Field(description=(
        "Short stable identifier for this effect, e.g. 'E1', 'E2'. "
        "One effect = one distinct (study × outcome × comparison) triplet. "
        "If H1 and H2 both measure the same outcome in the same study via the same comparison, "
        "they are ONE effect — record once."
    ))],
    study_label: Annotated[str, Field(description=(
        "Which independent study or experiment this effect comes from. "
        "If a study map is provided in the prompt, you MUST reuse one of its study_label "
        "values exactly — do not invent a new label or renumber. Otherwise, use 'Study 1', "
        "'Study 2', 'Experiment 1', etc., or 'Study 1' if the paper has only one study."
    ))],
    target_construct: Annotated[str, Field(description=(
        "The single construct this effect measures, stated in plain terms, "
        "e.g. 'persuasion', 'attitude change', 'credibility', 'cognitive load'. "
        "Must directly relate to the synthesis objective."
    ))],
    primary_outcome: Annotated[str, Field(description=(
        "The specific outcome variable name as used in the paper, "
        "e.g. 'attitude_change_index', 'compliance_rate', 'persuasion_score'."
    ))],
    treatment_description: Annotated[str, Field(description="What the treatment / intervention group received.")],
    control_description: Annotated[str, Field(description="What the control / comparison group received.")],
    is_primary_outcome: Annotated[bool, Field(description=(
        "True if this is the paper's primary/preregistered outcome. "
        "False for secondary, exploratory, or supplementary outcomes."
    ))],
    result_section_hint: Annotated[str, Field(description=(
        "Exact location of the statistics for this effect: table number, "
        "section heading, or page number. E.g. 'Table 2', 'Section 3.1 p.7'."
    ))],
    evidence_quote: Annotated[str, Field(description="Verbatim sentence from the paper that reports or introduces this effect.")],
    effect_direction: Annotated[Optional[str], Field(description="Reported or predicted direction, e.g. 'treatment > control', 'no significant difference', 'negative'.")] = None,
    expected_statistic_type: Annotated[Optional[str], Field(description="Statistical test used: t_test | anova | regression | chi_square | correlation | other.")] = None,
    exclusion_note: Annotated[Optional[str], Field(description="If this effect was considered but excluded from synthesis, briefly state why.")] = None,
) -> str:
    """Record ONE distinct effect relevant to the synthesis objective.

    The unit is (study × outcome × comparison) — NOT one per hypothesis.

    DEDUPLICATION RULE: If the paper tests the same construct on the same outcome
    in the same study via the same comparison under multiple hypothesis labels
    (H1, H1a, H1b, RQ1…), record it ONCE using the primary label.

    Call this tool only for effects that are:
      - directly relevant to the synthesis objective
      - primary or preregistered outcomes (prefer over secondary)
      - supported by inferential statistics (not descriptive-only)
    """
    return "effect_recorded"


@tool
def record_content_section(
    paper_id: str,
    section_id: Annotated[str, Field(description="Normalised identifier: 'abstract', 'introduction', 'related_work', 'methods', 'results', 'discussion', 'conclusion', 'appendix', 'other'.")],
    section_title: Annotated[str, Field(description="Exact heading as it appears in the markdown, e.g. '## 3. Results'.")],
    section_role: Annotated[str, Field(description="Functional role: background | methods | results | discussion | supplementary | other.")],
    contains_statistics: Annotated[bool, Field(description="True if this section contains reported statistical values (F, t, p, means, SDs, ORs).")],
    contains_hypotheses: Annotated[bool, Field(description="True if this section states hypotheses or research questions.")],
    page_range: Annotated[Optional[str], Field(description="Page span from <!-- page N --> markers, e.g. '4–7'.")] = None,
    linked_rq_ids: Annotated[Optional[List[str]], Field(description="rq_id values whose results appear in this section.")] = None,
    key_content_summary: Annotated[Optional[str], Field(description="1–3 sentence summary. For results sections, name the outcomes and main findings.")] = None,
) -> str:
    """Record one major section of the paper.
    Call for every distinct section: abstract, introduction, related work, methods,
    results, discussion, conclusion, appendix."""
    return "section_recorded"


def rq_detection_node(state: GraphState) -> dict:
    """Stage 3B: detect research questions and content sections per paper."""
    logger.info("=== STAGE 4: RQ Detection ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    output_dir: str = state["output_dir"]
    user_query: str = state.get("user_prompt", "")
    plan = state.get("plan")
    study_maps: Dict[str, Any] = state.get("study_maps", {})

    if plan:
        synthesis_context = (
            f"User prompt: {user_query}\n"
            f"Planned research question: {plan.research_question}\n"
            f"Planned treatment/intervention: {plan.treatment_label}\n"
            f"Planned control/comparator: {plan.control_label}\n"
            f"Planned outcome: {plan.outcome_description}\n"
            f"Positive effect direction: {plan.positive_direction}\n"
            f"Inclusion criteria: {'; '.join(plan.inclusion_criteria)}\n"
            f"Exclusion criteria: {'; '.join(plan.exclusion_criteria)}\n"
        )
    else:
        synthesis_context = f"User prompt: {user_query}\n"

    rq_maps: Dict[str, Any] = {}
    agent = _get_agent()

    for paper in papers:
        try:
            text = (paper.full_text or paper.abstract or "")[:_MAX_CHARS]

            # Reuse StudyDetectorAgent's canonical study_label values instead of
            # letting this agent re-derive its own study structure from scratch --
            # keeps study_label consistent with study_maps.json, which downstream
            # extraction (Stage 4) and the moderator agent both join against.
            study_map = study_maps.get(paper.id, {})
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
                        f"    Primary outcomes: {outcomes}"
                    )
                study_context = "\n".join(lines) + "\n"

            user_msg = (
                f"Paper ID  : {paper.id}\n"
                f"Title     : {paper.title}\n\n"
                f"Abstract:\n{paper.abstract}\n\n"
                f"Full markdown text:\n{text}\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "STUDY MAP\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{study_context or 'No study map available — determine study_label yourself.'}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "SYNTHESIS OBJECTIVE\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{synthesis_context}\n"
                "Use the planned treatment, control, and outcome above as the authority. "
                "A paper RQ, hypothesis, or effect is CRITICAL only if it can plausibly "
                "contribute to that planned contrast and outcome. Do not treat every "
                "paper hypothesis as critical just because it is important inside the "
                "paper.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "EXTRACTION TASK\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Extract ONLY the experimentally tested effects that are directly "
                "relevant to the synthesis objective.\n\n"
                "A relevant effect must satisfy ALL of these checks:\n"
                "  * Its treatment/intervention matches or is a close operationalization "
                "of the planned treatment.\n"
                "  * Its comparator matches or is a close operationalization of the planned control.\n"
                "  * Its measured outcome is the planned outcome or a direct proxy.\n"
                "  * It reports inferential or descriptive quantitative statistics that "
                "could support an effect size.\n\n"
                "Focus on:\n"
                "  * primary outcomes\n"
                "  * preregistered outcomes\n"
                "  * main experimental comparisons\n"
                "  * central claims reported in the abstract/results/discussion\n\n"
                "Do NOT extract:\n"
                "  * robustness checks\n"
                "  * manipulation checks\n"
                "  * mediation/moderation analyses unless central\n"
                "  * exploratory analyses\n"
                "  * linguistic/process variables\n"
                "  * descriptive-only analyses\n"
                "  * subgroup analyses unless central to the paper's primary claim\n\n"
                "If multiple analyses test the same construct:\n"
                "extract only the primary/preferred/main analysis.\n\n"
                "The goal is to build a concise, high-quality synthesis dataset,\n"
                "NOT a complete map of all analyses in the paper.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "INSTRUCTIONS\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "STEP 1 — Call record_content_section for every major section:\n"
                "  • Use ## / ### headings and <!-- page N --> markers for boundaries.\n"
                "  • Set contains_statistics=true only if the section reports statistical "
                "values (F, t, p, means, SDs, ORs).\n"
                "  • Set contains_hypotheses=true if the section states an H or RQ.\n"
                "  • Link results sections to the rq_ids they address.\n\n"
                "STEP 2 — Call record_relevant_effect for each relevant effect:\n"
                "  • Assign a stable effect_id (E1, E2, …).\n"
                "  • Set study_label to one of the STUDY MAP labels above exactly, if a "
                "study map was provided — do not invent or renumber study labels.\n"
                "  • Identify treatment_description, control_description, and target_construct.\n"
                "  • List the primary_outcome variable by the name used in the paper.\n"
                "  • State effect_direction if given.\n"
                "  • Point result_section_hint to the exact table/section/page.\n"
                "  • Quote the sentence that introduces this effect.\n\n"
                "Call record_content_section for ALL sections first, "
                "then call record_relevant_effect for each relevant effect."
            )

            result = agent.invoke({"messages": [("user", user_msg)]})

            questions = _all_tool_args(result["messages"], "record_relevant_effect")
            sections  = _all_tool_args(result["messages"], "record_content_section")

            if not questions:
                logger.warning(f"[RQDetector] {paper.id}: no RQs detected.")

            rq_maps[paper.id] = {
                "research_questions": questions,
                "content_sections":   sections,
            }
            logger.info(
                f"[RQDetector] {paper.id}: {len(questions)} RQs, "
                f"{len(sections)} sections detected."
            )

        except Exception as exc:
            logger.error(f"[RQDetector] {paper.id}: skipped — {exc}")
            rq_maps[paper.id] = {"research_questions": [], "content_sections": []}

    save_json(rq_maps, os.path.join(output_dir, "rq_maps.json"))
    return {"rq_maps": rq_maps}
