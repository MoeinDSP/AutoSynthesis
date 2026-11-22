"""Title/abstract screening agent — Stage 2b (search mode).

Runs after the search (and after the optional paper-selection gate) and BEFORE
full-text retrieval, as in a standard PRISMA workflow: each found record is
judged from its title and abstract against the plan's research question and
eligibility criteria, and only records that may be eligible go on to the
(slow, expensive) full-text fetch. Full-text eligibility_node still makes the
final include/exclude decision afterwards.

The screen is deliberately permissive: a record is excluded only when the
title/abstract make it clear that it cannot answer the research question.
Missing or sparse abstracts, uncertain terminology, or a failed LLM call all
default to INCLUDE, so the screen can only remove clearly irrelevant records.

Excluded records are written to screening_decisions (stage "Screening" in
paper_tracking.csv and the PRISMA "records excluded" box) with the LLM's
short reason.
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from langchain_core.tools import tool

import config
from agents.llm import llm
from models import MetaAnalysisPlan, PaperRecord

logger = logging.getLogger(__name__)

# Abstracts are long enough for a screen; cap them so one odd record (e.g. a
# whole body of text in the abstract field) cannot blow up a request.
_MAX_ABSTRACT_CHARS = 6000


@tool
def screening_decision(decision: str, reason: str) -> str:
    """Record the title/abstract screening verdict for this record.
    decision: 'include' (may be eligible -> retrieve full text) or 'exclude'
    (clearly cannot answer the research question).
    reason: concise phrase (<= 8 words), e.g. 'different population',
    'different intervention', 'no relevant comparator', 'systematic review',
    'protocol only', 'animal study', 'outcome not measured', 'may meet criteria'."""
    return "screening_recorded"


def _system_prompt(plan: MetaAnalysisPlan) -> str:
    inc = "\n".join(f"  {i + 1}. {c}" for i, c in enumerate(plan.inclusion_criteria))
    exc = "\n".join(f"  - {c}" for c in plan.exclusion_criteria)
    return (
        "You are a systematic reviewer doing TITLE/ABSTRACT screening for a "
        "quantitative meta-analysis. Records you include will have their full "
        "text retrieved and assessed in detail later; records you exclude are "
        "dropped for good.\n\n"
        f"Research question: {plan.research_question}\n\n"
        f"Inclusion criteria:\n{inc}\n\n"
        f"Exclusion criteria:\n{exc}\n\n"
        "EXCLUDE only when the title/abstract make it CLEAR that the record cannot "
        "contribute data to this research question, for example: a different "
        "population, a different intervention or exposure, no eligible comparator, "
        "a study design the criteria rule out, a review / meta-analysis / protocol / "
        "editorial / commentary, an animal or in-vitro study, or a topic unrelated "
        "to the question.\n"
        "INCLUDE when the record may be eligible, or when you are unsure, or when "
        "the abstract is missing or too short to judge. The outcome of interest is "
        "often not mentioned in an abstract; do not exclude only because the "
        "abstract does not name it.\n\n"
        "Call `screening_decision` exactly once with your decision and a short reason."
    )


def _screen_one(bound, system_prompt: str, paper: PaperRecord) -> Dict:
    abstract = (paper.abstract or "").strip()[:_MAX_ABSTRACT_CHARS]
    user_msg = (
        f"Title: {paper.title}\n"
        f"Year: {paper.year or 'unknown'}\n\n"
        f"Abstract:\n{abstract or '[no abstract available]'}"
    )
    for attempt in range(2):
        try:
            msg = bound.invoke([("system", system_prompt), ("user", user_msg)])
            for call in getattr(msg, "tool_calls", None) or []:
                if call.get("name") == "screening_decision":
                    args = call.get("args") or {}
                    decision = str(args.get("decision", "")).strip().lower()
                    if decision in ("include", "exclude"):
                        return {"decision": decision, "reason": str(args.get("reason", "")).strip()}
        except Exception as exc:  # network / provider error: retry once, then fail open
            logger.warning(f"[Screening] {paper.id}: attempt {attempt + 1} failed: {exc}")
    return {"decision": "include", "reason": "screening call failed; kept for full-text review"}


def title_abstract_screen_node(state: dict) -> dict:
    """Stage 2b (search mode): LLM title/abstract screening before full-text fetch."""
    papers: List[PaperRecord] = list(state.get("papers_eligible", []))
    if not config.TITLE_ABSTRACT_SCREENING or not papers:
        return {}
    logger.info(f"=== STAGE 2b: Title/Abstract Screening ({len(papers)} records) ===")
    plan: MetaAnalysisPlan = state["plan"]
    system_prompt = _system_prompt(plan)
    bound = llm.bind_tools([screening_decision], tool_choice="screening_decision")

    # Records that already carry full text (PDFs the user added or attached at
    # the paper-selection gate) were chosen by the user -- never screen them out.
    to_screen = [p for p in papers if not p.full_text]
    with ThreadPoolExecutor(max_workers=max(1, config.SCREENING_WORKERS)) as pool:
        verdicts = list(pool.map(lambda p: _screen_one(bound, system_prompt, p), to_screen))
    verdict_by_id = {p.id: v for p, v in zip(to_screen, verdicts)}

    screening = dict(state.get("screening_decisions", {}))
    kept: List[PaperRecord] = []
    n_excluded = 0
    for p in papers:
        v = verdict_by_id.get(p.id)
        if v is None or v["decision"] == "include":
            kept.append(p)
            continue
        n_excluded += 1
        prev = screening.get(p.id, {})
        screening[p.id] = {
            **prev,
            "decision": "exclude",
            "reason": f"title/abstract screening: {v['reason'] or 'not eligible'}",
            "title": p.title,
            "source": prev.get("source", p.source),
        }
        logger.info(f"[Screening] excluded {p.id} — {p.title[:70]} ({v['reason']})")

    n_prev = state.get("n_screened_excluded", 0)
    n_prev = n_prev if isinstance(n_prev, int) and n_prev >= 0 else 0
    logger.info(f"[Screening] {len(kept)} records kept for full-text retrieval, {n_excluded} excluded.")
    return {
        "papers_eligible": kept,
        "screening_decisions": screening,
        "n_screened_excluded": n_prev + n_excluded,
    }
