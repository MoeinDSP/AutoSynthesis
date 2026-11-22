"""Relevance Filter Agent — Stage 4C.

Four-stage pipeline applied to ALL results from a paper at once:
  1. Outcome classification  — categorise each row (primary, secondary, manipulation_check, …)
  2. Construct grouping      — assign a normalised construct_family label
  3. Priority ranking        — rank within each (study × construct_family) group
  4. Redundancy reduction    — keep ONE winner per group; discard the rest

Only rows marked is_winner=True are passed downstream.
"""

import logging
from typing import Annotated, Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import Field

from agents.llm import llm
from pipeline_graph import _all_tool_args, GraphState

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a meta-analysis outcome classifier. "
    "Your ONLY job is to classify each row — you do NOT decide which rows to keep. "
    "A separate algorithm will select winners based on your classifications.\n\n"

    "For EVERY row call classify_and_select with accurate values for:\n\n"

    "1. OUTCOME CLASS\n"
    "   primary | secondary | manipulation_check | process_variable | "
    "exploratory | robustness_check | descriptive\n\n"

    "2. CONSTRUCT FAMILY\n"
    "   A normalised label for the underlying construct being measured.\n"
    "   CRITICAL — PARENTHETICAL QUALIFIER RULE:\n"
    "   Outcome names that share the same base name but differ only by a parenthetical\n"
    "   qualifier are sub-conditions of the SAME construct. Strip the qualifier.\n"
    "   Examples:\n"
    "     'Compliance rate (overall)', 'Compliance rate (truthful)', "
    "'Compliance rate (deceptive)'\n"
    "     → all three: construct_family = 'compliance_rate'\n"
    "     'Accuracy (truthful persuasion)', 'Accuracy (deceptive persuasion)'\n"
    "     → both: construct_family = 'accuracy'\n"
    "     'Attitude change (immediate)', 'Attitude change (delayed)'\n"
    "     → both: construct_family = 'attitude_change'\n"
    "   The qualifier NEVER creates a new construct_family.\n\n"

    "3. GRANULARITY LEVEL\n"
    "   Within the construct_family group, is this row:\n"
    "   • 'aggregate'    — covers all conditions/full sample "
    "(keyword: 'overall', 'total', 'combined', or no qualifier)\n"
    "   • 'sub_condition' — splits by condition, content type, time point, sub-scale\n"
    "     (keywords: 'truthful', 'deceptive', 'immediate', 'delayed', etc.)\n"
    "   • 'standalone'   — neither (single unique measure)\n\n"

    "4. COMPARISON ARM\n"
    "   From group_1_label / group_2_label, classify the comparison arm:\n"
    "   • 'target_arm'     — treatment is the LLM / AI intervention of interest\n"
    "   • 'non_target_arm' — treatment is a human or other non-AI comparator\n"
    "   • 'primary'        — only one arm exists\n\n"

    "5. IS SYNTHESIS RELEVANT\n"
    "   True if the construct directly answers the synthesis objective. "
    "False for manipulation checks, process variables unrelated to the main outcome, etc.\n\n"

    "6. PRIORITY RANK (1 = highest)\n"
    "   1=behavior, 2=compliance/persuasion, 3=attitude, 4=intention, "
    "5=resistance, 6=experiential, 7=mechanism, 8=descriptive\n\n"

    "Call classify_and_select once for EVERY row. Do not skip any.\n"
    "Set is_winner=True for all rows — the selection algorithm overrides this."
)


@tool
def classify_and_select(
    row_index: Annotated[int, Field(description="1-based index matching the input row list.")],
    paper_id: Annotated[str, Field(description="paper_id of this row.")],
    study_label: Annotated[str, Field(description="study_label of this row.")],
    outcome_name: Annotated[str, Field(description="outcome_name of this row.")],
    outcome_class: Annotated[str, Field(description=(
        "Classification: primary | secondary | manipulation_check | "
        "process_variable | exploratory | robustness_check | descriptive"
    ))],
    construct_family: Annotated[str, Field(description=(
        "Normalised construct label shared by all rows measuring the same underlying "
        "construct, e.g. 'persuasion', 'attitude_change', 'behavioral_intention'."
    ))],
    granularity_level: Annotated[str, Field(description=(
        "Granularity of this outcome within its construct_family: "
        "'aggregate' — covers the full sample/all conditions (e.g. overall rate); "
        "'sub_condition' — a breakdown of the aggregate by content type, sub-scale, "
        "condition, time point, etc.; "
        "'standalone' — neither aggregate nor sub-condition (single measure)."
    ))],
    comparison_arm: Annotated[str, Field(description=(
        "Which comparison arm this row represents, derived from group labels. "
        "E.g. 'intervention_vs_control', 'active_control_vs_control', 'pre_vs_post'. "
        "Use 'primary' if only one arm exists. "
        "Use 'non_target_arm' if this arm does not represent the target intervention."
    ))],
    priority_rank: Annotated[int, Field(description=(
        "Priority within the (paper × study × construct_family) group. "
        "1 = highest priority (actual behavior). Use the 8-level hierarchy from instructions."
    ))],
    is_synthesis_relevant: Annotated[bool, Field(description=(
        "True if this outcome's construct_family directly answers the synthesis objective."
    ))],
    is_winner: Annotated[bool, Field(description=(
        "True = keep this row in the meta-analysis dataset. "
        "False = sub_condition of an existing aggregate, non-target comparison arm, "
        "manipulation_check, robustness_check, descriptive, or irrelevant construct."
    ))],
    reason: Annotated[str, Field(description="One sentence explaining the winner/non-winner decision.")],
    redundant_with: Annotated[Optional[int], Field(description=(
        "row_index of the winner this row is redundant with. Null if is_winner=True."
    ))] = None,
) -> str:
    """Classify, group, rank, and select one result row.
    Called once per row. Winners (is_winner=True) pass through to the dataset."""
    return "classified"


def relevance_filter_node(state: GraphState) -> dict:
    """Stage 4C: LLM classifies rows; Python enforces exactly-one-winner per group."""
    logger.info("=== STAGE 4B: Relevance Filter ===")
    results: List[dict] = state.get("paper_results", [])
    user_query: str = state.get("user_prompt", "")
    logger.info(f"[RelevanceFilter] Classifying {len(results)} result rows.")

    if not results:
        return {"paper_results": []}

    # ── Build LLM input ────────────────────────────────────────────────────────
    result_lines = []
    for i, r in enumerate(results, start=1):
        result_lines.append(
            f"[Row {i}] paper_id={r.get('paper_id')!r} "
            f"study_label={r.get('study_label')!r} "
            f"outcome_name={r.get('outcome_name')!r} "
            f"outcome_type={r.get('outcome_type')!r} "
            f"result_role={r.get('result_role')!r} "
            f"task_or_measure={r.get('task_or_measure')!r} "
            f"comparison_type={r.get('comparison_type')!r} "
            f"group_1_label={r.get('group_1_label')!r} "
            f"group_2_label={r.get('group_2_label')!r} "
            f"true_research_question={r.get('true_research_question')!r}"
        )

    user_msg = (
        f"SYNTHESIS OBJECTIVE: \"{user_query}\"\n\n"
        "Classify every row below. Call classify_and_select once per row.\n\n"
        + "\n".join(result_lines)
        + "\n\nCall classify_and_select for ALL rows. Do not skip any."
    )

    agent = create_react_agent(llm, [classify_and_select], prompt=SYSTEM_PROMPT)
    result = agent.invoke({"messages": [("user", user_msg)]})

    verdicts: Dict[int, dict] = {}
    for v in _all_tool_args(result["messages"], "classify_and_select"):
        row_index = v.get("row_index")
        if row_index is None:
            logger.warning(
                f"[RelevanceFilter] classify_and_select call missing row_index, "
                f"dropping it: {v!r}"
            )
            continue
        verdicts[row_index] = v

    # ── Annotate rows with LLM classifications ─────────────────────────────────
    annotated: List[tuple] = []
    for i, row in enumerate(results, start=1):
        v = verdicts.get(i)
        if v is None:
            logger.warning(
                f"[RelevanceFilter] No verdict for row {i} "
                f"({row.get('study_label')!r}/{row.get('outcome_name')!r}) — "
                "keeping with defaults."
            )
            v = {}
        row["_outcome_class"]         = v.get("outcome_class", "unknown")
        row["_construct_family"]      = v.get("construct_family") or f"construct_{i}"
        row["_granularity_level"]     = v.get("granularity_level", "standalone")
        row["_comparison_arm"]        = v.get("comparison_arm", "primary")
        row["_priority_rank"]         = v.get("priority_rank", 99)
        row["_is_synthesis_relevant"] = v.get("is_synthesis_relevant", True)
        row["_filter_reason"]         = v.get("reason", "")
        annotated.append((i, row))

    # ── Deterministic winner selection (Python, not LLM) ───────────────────────
    # Classes that are NEVER relevant to a meta-analysis dataset
    _EXCLUDE_CLASSES = {"manipulation_check", "robustness_check", "descriptive"}

    # Granularity preference: aggregate wins over standalone wins over sub_condition
    _GRAN_RANK = {"aggregate": 0, "standalone": 1, "sub_condition": 2}

    # Step 1: split into ineligible (always drop) and eligible (compete per group)
    from collections import defaultdict
    eligible: Dict[tuple, list] = defaultdict(list)
    dropped: List[dict] = []

    for i, row in annotated:
        oc  = row["_outcome_class"]
        rel = row["_is_synthesis_relevant"]
        arm = row["_comparison_arm"]

        if oc in _EXCLUDE_CLASSES:
            row["_filter_reason"] = f"excluded class: {oc}"
            dropped.append(row)
        elif not rel:
            row["_filter_reason"] = "not relevant to synthesis objective"
            dropped.append(row)
        elif arm == "non_target_arm":
            row["_filter_reason"] = "non-target comparison arm"
            dropped.append(row)
        else:
            key = (
                row.get("paper_id", ""),
                row.get("study_label", ""),
                row["_construct_family"],
            )
            eligible[key].append((i, row))

    # Step 2: within each group keep exactly ONE winner
    kept: List[dict] = []
    for group_key, group_items in eligible.items():
        # Sort: aggregate first → then by priority_rank (lower = better)
        group_items.sort(key=lambda x: (
            _GRAN_RANK.get(x[1]["_granularity_level"], 1),
            x[1]["_priority_rank"],
        ))

        winner_i, winner_row = group_items[0]
        kept.append(winner_row)

        for _, loser_row in group_items[1:]:
            loser_row["_filter_reason"] = (
                f"redundant with row {winner_i} "
                f"({winner_row.get('outcome_name', '')} / "
                f"granularity={winner_row['_granularity_level']})"
            )
            dropped.append(loser_row)
            logger.debug(
                f"[RelevanceFilter] Dropped {loser_row.get('outcome_name')!r}: "
                f"{loser_row['_filter_reason']}"
            )

    logger.info(
        f"[RelevanceFilter] {len(kept)} kept / {len(dropped)} dropped "
        f"from {len(results)} rows."
    )
    return {"paper_results": kept}
