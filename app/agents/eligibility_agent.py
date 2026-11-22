"""Eligibility agent — Stage 3 (search mode). Pattern 1: per-paper record-output tool."""

import logging
from typing import Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from models import MetaAnalysisPlan, PaperRecord
from pipeline_graph import _all_tool_args, GraphState

logger = logging.getLogger(__name__)

@tool
def eligibility_decision(
    paper_id: str,
    decision: str,
    reason: str,
    exclusion_criterion: Optional[str] = None,
) -> str:
    """Record full-text eligibility verdict. decision: 'include' or 'exclude'.
    reason: concise phrase (≤8 words) for the decision, e.g.:
      exclude: 'no quantitative data', 'wrong population', 'missing outcome measure',
               'wrong study design', 'no control condition', 'irrelevant intervention'
      include: 'meets inclusion criteria', 'has quantitative outcome data'
    exclusion_criterion: 'insufficient_design' or 'missing_data' if excluding."""
    return "eligibility_recorded"


def eligibility_node(state: GraphState) -> dict:
    """Stage 3 (search mode): full-text eligibility assessment."""
    logger.info("=== STAGE 3: Eligibility ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    plan: MetaAnalysisPlan = state["plan"]

    if not papers:
        return {"papers_eligible": [], "eligibility_decisions": {},
                "n_eligibility_excluded": 0}

    criteria_text = "\n".join(
        f"  {i+1}. {c}" for i, c in enumerate(plan.inclusion_criteria)
    )
    exclusion_text = "\n".join(f"  - {c}" for c in plan.exclusion_criteria)

    system_prompt = (
        "You are a systematic review methodologist assessing papers for inclusion "
        "in a quantitative meta-analysis.\n\n"
        f"Research question: {plan.research_question}\n\n"
        f"Inclusion criteria:\n{criteria_text}\n\n"
        f"Exclusion criteria:\n{exclusion_text}\n\n"
        "Only EXCLUDE the paper when the evidence is clear. Do not infer exclusion "
        "from missing snippets, sparse abstracts, or uncertain terminology.\n\n"
        "EXCLUDE the paper if ANY of the following is clearly true:\n"
        "  A) It is NOT an original empirical study — it is a systematic review, "
        "meta-analysis, editorial, commentary, opinion piece, or purely theoretical paper.\n"
        "  B) It has NO comparison between at least two groups or conditions "
        "(no treatment vs. control, intervention vs. baseline, or equivalent contrast).\n"
        "  C) It clearly has NO quantitative outcome data — no means, SDs, t-values, "
        "F-values, proportions, or odds ratios that could support an effect size computation.\n"
        "  D) It is completely unrelated to the research question.\n\n"
        "INCLUDE if none of the above clearly apply. When in doubt about design, "
        "topic fit, or quantitative data availability, INCLUDE — the extractor "
        "and deterministic statistical checks will verify this downstream.\n\n"
        "Call `eligibility_decision` for every paper. Always provide a short reason "
        "(≤8 words), e.g. 'systematic review', 'no control condition', "
        "'no quantitative outcome data', 'meets all criteria'."
    )

    agent = create_react_agent(llm, [eligibility_decision], prompt=system_prompt)

    decisions: Dict[str, Dict] = {}
    for paper in papers:
        logger.info(f"[Eligibility] Assessing: {paper.id} — {paper.title[:60]}")
        full_text_section = (
            f"\n\nFull text excerpt:\n{paper.full_text}"
            if paper.full_text
            else "\n\n[Full text not available — assess from abstract only. When in doubt, INCLUDE.]"
        )
        user_msg = (
            f"Paper ID: {paper.id}\n"
            f"Title: {paper.title}\n"
            f"Year: {paper.year}\n\n"
            f"Abstract:\n{paper.abstract}"
            f"{full_text_section}\n\n"
            "Assess this paper against all inclusion criteria and call `eligibility_decision` "
            "with your decision and a short reason."
        )
        result = agent.invoke({"messages": [("user", user_msg)]})
        for d in _all_tool_args(result["messages"], "eligibility_decision"):
            d_paper_id = d.get("paper_id")
            if d_paper_id is None or d.get("decision") is None:
                logger.warning(
                    f"[Eligibility] {paper.id}: malformed eligibility_decision call, "
                    f"dropping it (defaults to include): {d!r}"
                )
                continue
            decisions[d_paper_id] = {
                "decision":           d["decision"],
                "reason":             d.get("reason", ""),
                "exclusion_criterion": d.get("exclusion_criterion"),
                "title":              paper.title,
            }

    included = [p for p in papers if decisions.get(p.id, {}).get("decision", "include") == "include"]
    n_excluded = len(papers) - len(included)
    logger.info(f"[Eligibility] {len(included)} included, {n_excluded} excluded.")

    return {
        "papers_eligible":       included,
        "n_eligibility_excluded": n_excluded,
        "eligibility_decisions": decisions,
    }
