"""
Risk-of-bias agent — Stage 8B. Pattern 3: phase-ordered tools in a per-paper closure
(design classification must complete before any domain judgment; domain judgments
before the overall judgment), mirroring statistical_result_extractor_agent.py's
two-phase gating.

For each eligible paper, the LLM first classifies the study design (randomized vs.
non-randomized) from the methods section, then applies the corresponding standard
risk-of-bias tool:
  - Randomized:      RoB 2 (Sterne et al. 2019, BMJ) -- 5 domains, low/some_concerns/high
  - Non-randomized:   ROBINS-I (Sterne et al. 2016, BMJ) -- 7 domains,
                       low/moderate/serious/critical/no_information

Produces one RiskOfBiasAssessment per paper (models.py) and a Cochrane-style
traffic-light plot per tool actually used (a run with only randomized studies gets
one plot; a run with both gets two).
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from core_utils import save_json
from models import PaperRecord, RiskOfBiasAssessment
from pipeline_graph import GraphState
from statistics.plots import risk_of_bias_traffic_light_plot

logger = logging.getLogger(__name__)

_MAX_CHARS = 100_000

ROB2_DOMAINS = [
    "Randomization process",
    "Deviations from intended interventions",
    "Missing outcome data",
    "Measurement of the outcome",
    "Selection of the reported result",
]
ROB2_JUDGMENTS = {"low", "some_concerns", "high"}

ROBINS_I_DOMAINS = [
    "Bias due to confounding",
    "Bias due to selection of participants into the study",
    "Bias in classification of interventions",
    "Bias due to deviations from intended interventions",
    "Bias due to missing data",
    "Bias in measurement of outcomes",
    "Bias in selection of the reported result",
]
ROBINS_I_JUDGMENTS = {"low", "moderate", "serious", "critical", "no_information"}

SYSTEM_PROMPT = (
    "You are a systematic-review methodologist assessing risk of bias for ONE study "
    "at a time, following the two standard Cochrane tools.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STEP 1 — CLASSIFY THE STUDY DESIGN (call classify_study_design exactly once, first)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "Read the Methods/Participants section. Classify as:\n"
    "  'randomized'     — participants/units were randomly assigned to conditions "
    "(random number generator, randomization software, coin flip, etc. -- explicit "
    "random allocation, not just 'between-subjects').\n"
    "  'non_randomized' — any other assignment mechanism: self-selection, "
    "convenience/quota sampling into conditions, quasi-experimental, observational, "
    "or assignment method not clearly random.\n"
    "If the paper does not explicitly describe random allocation, classify as "
    "'non_randomized' -- do not assume randomization was used.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STEP 2 — DOMAIN JUDGMENTS (call record_domain_judgment once per domain, in order)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "If randomized, apply RoB 2 (5 domains, judgment in {low, some_concerns, high}):\n"
    "  D1 Randomization process — was allocation sequence random and concealed until "
    "assignment? Were baseline differences between groups consistent with chance?\n"
    "  D2 Deviations from intended interventions — did participants know their assigned "
    "condition (relevant for behavioral/persuasion studies); were there deviations from "
    "the intended intervention that affected the outcome; was an appropriate analysis "
    "used (e.g., intention-to-treat)?\n"
    "  D3 Missing outcome data — was outcome data available for nearly all "
    "participants; if not, is there evidence results weren't biased by missingness?\n"
    "  D4 Measurement of the outcome — was the outcome measure appropriate; was it "
    "assessed the same way across groups; could assessors have been influenced by "
    "knowledge of the intervention received?\n"
    "  D5 Selection of the reported result — was the reported result selected from "
    "multiple eligible outcome measurements or analyses (e.g., no pre-registration, "
    "multiple outcome operationalizations, flexible analysis)?\n\n"
    "If non_randomized, apply ROBINS-I (7 domains, judgment in "
    "{low, moderate, serious, critical, no_information}):\n"
    "  D1 Bias due to confounding — were groups comparable on factors that plausibly "
    "affect the outcome, beyond the intervention itself?\n"
    "  D2 Bias due to selection of participants into the study — did selection into "
    "the study or into a condition relate to both intervention and outcome?\n"
    "  D3 Bias in classification of interventions — was the intervention/condition "
    "clearly and consistently defined and classified?\n"
    "  D4 Bias due to deviations from intended interventions — as RoB 2 D2.\n"
    "  D5 Bias due to missing data — as RoB 2 D3.\n"
    "  D6 Bias in measurement of outcomes — as RoB 2 D4.\n"
    "  D7 Bias in selection of the reported result — as RoB 2 D5.\n\n"
    "For EVERY domain: if the paper does not report the information needed to judge "
    "a domain, that is itself evidence of risk -- do not default to 'low'. Use "
    "'some_concerns'/'moderate' for missing-but-plausibly-fine information, and "
    "'no_information' (ROBINS-I only) only when truly nothing can be inferred. "
    "Always give a one-sentence rationale and, where possible, a verbatim evidence "
    "quote from the text.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STEP 3 — OVERALL JUDGMENT (call record_overall_judgment exactly once, last)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "The overall judgment is at least as severe as the single worst domain judgment "
    "(standard convention for both tools) -- e.g. one 'high'/'serious' domain makes "
    "the overall judgment 'high'/'serious' even if all other domains are 'low'. "
    "Give a 1-2 sentence summary explaining what drove the overall judgment."
)


def risk_of_bias_node(state: GraphState) -> dict:
    """Stage 8B: per-paper risk-of-bias assessment (RoB 2 or ROBINS-I)."""
    logger.info("=== STAGE 8B: Risk of Bias Assessment ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    output_dir: str = state["output_dir"]

    if not papers:
        return {"rob_assessments": [], "rob_plot_paths": {}}

    assessments: List[RiskOfBiasAssessment] = []

    for paper in papers:
        text = (paper.full_text or paper.abstract or "")[:_MAX_CHARS]
        captured: Dict = {"design": None, "design_rationale": "", "tool_used": None,
                           "domains": [], "overall_risk": None, "overall_summary": ""}

        @tool
        def classify_study_design(paper_id: str, design: str, rationale: str) -> str:
            """Classify this study's design. Call FIRST, exactly once.
            design: 'randomized' or 'non_randomized'."""
            design_norm = design.strip().lower()
            captured["design"] = design_norm
            captured["design_rationale"] = rationale
            captured["tool_used"] = "RoB2" if design_norm == "randomized" else "ROBINS-I"
            return f"design_recorded: use {captured['tool_used']} for the domain judgments"

        @tool
        def record_domain_judgment(
            paper_id: str,
            domain_number: int,
            domain_name: str,
            judgment: str,
            rationale: str,
            evidence_quote: Optional[str] = None,
        ) -> str:
            """Record one risk-of-bias domain judgment. Requires classify_study_design
            to have been called first. Call once per domain, in order (5 domains for
            RoB 2, 7 for ROBINS-I)."""
            if captured["design"] is None:
                return "ERROR: call classify_study_design first."
            expected_n = len(ROB2_DOMAINS) if captured["tool_used"] == "RoB2" else len(ROBINS_I_DOMAINS)
            entry = {
                "domain_number": domain_number,
                "domain_name": domain_name,
                "judgment": judgment.strip().lower(),
                "rationale": rationale,
                "evidence_quote": evidence_quote,
            }
            for idx, existing in enumerate(captured["domains"]):
                if existing["domain_number"] == domain_number:
                    captured["domains"][idx] = entry  # re-judgment of the same domain: overwrite
                    return "domain_judgment_updated (domain already recorded — replaced prior judgment)"
            if len(captured["domains"]) >= expected_n:
                return (
                    f"ERROR: all {expected_n} domains for {captured['tool_used']} are already "
                    "recorded. Call record_overall_judgment next."
                )
            captured["domains"].append(entry)
            return "domain_judgment_recorded"

        @tool
        def record_overall_judgment(paper_id: str, overall_risk: str, summary: str) -> str:
            """Record the overall risk-of-bias judgment. Call LAST, exactly once,
            after all domain judgments."""
            if captured["design"] is None:
                return "ERROR: call classify_study_design first."
            captured["overall_risk"] = overall_risk.strip().lower()
            captured["overall_summary"] = summary
            return "overall_judgment_recorded"

        user_msg = (
            f"Paper ID : {paper.id}\n"
            f"Title    : {paper.title}\n\n"
            f"Full text (or abstract if full text unavailable):\n{text}\n\n"
            "Follow STEP 1 -> STEP 2 -> STEP 3 exactly as instructed."
        )

        try:
            agent = create_react_agent(
                llm,
                [classify_study_design, record_domain_judgment, record_overall_judgment],
                prompt=SYSTEM_PROMPT,
            )
            agent.invoke({"messages": [("user", user_msg)]})
        except Exception as exc:
            logger.error(f"[RiskOfBias] {paper.id}: LLM call failed — {exc}")

        if captured["design"] is None:
            logger.warning(f"[RiskOfBias] {paper.id}: model never classified design — skipping.")
            continue

        valid_judgments = ROB2_JUDGMENTS if captured["tool_used"] == "RoB2" else ROBINS_I_JUDGMENTS
        if captured["overall_risk"] not in valid_judgments:
            logger.warning(
                f"[RiskOfBias] {paper.id}: no/invalid overall judgment "
                f"({captured['overall_risk']!r}) — defaulting to worst domain judgment."
            )
            severity_order = ["low", "some_concerns", "moderate", "serious", "high", "critical"]
            domain_judgments = [d["judgment"] for d in captured["domains"] if d["judgment"] in severity_order]
            captured["overall_risk"] = (
                max(domain_judgments, key=severity_order.index) if domain_judgments else "no_information"
            )

        assessment = RiskOfBiasAssessment(
            paper_id=paper.id,
            paper_title=paper.title,
            design_classification=captured["design"] if captured["design"] in {"randomized", "non_randomized"} else "non_randomized",
            design_rationale=captured["design_rationale"],
            tool_used=captured["tool_used"],
            domain_judgments=captured["domains"],
            overall_risk=captured["overall_risk"],
            overall_summary=captured["overall_summary"],
        )
        assessments.append(assessment)
        logger.info(
            f"[RiskOfBias] {paper.id}: {assessment.tool_used}, "
            f"{len(assessment.domain_judgments)} domains, overall={assessment.overall_risk}"
        )

    save_json(
        [a.model_dump() for a in assessments],
        os.path.join(output_dir, "rob_assessments.json"),
    )

    # ── Traffic-light plot(s), one per tool actually used ───────────────────────
    plot_paths: Dict[str, str] = {}
    for tool_name, domains_const in [("RoB2", ROB2_DOMAINS), ("ROBINS-I", ROBINS_I_DOMAINS)]:
        group = [a for a in assessments if a.tool_used == tool_name]
        if not group:
            continue
        domain_names = [d.domain_name for d in group[0].domain_judgments] or domains_const
        judgments = [
            [d.judgment for d in a.domain_judgments] for a in group
        ]
        try:
            path = risk_of_bias_traffic_light_plot(
                study_labels=[a.paper_title[:45] for a in group],
                domain_names=domain_names,
                judgments=judgments,
                overall_judgments=[a.overall_risk for a in group],
                tool_name="RoB 2" if tool_name == "RoB2" else "ROBINS-I",
                output_path=os.path.join(output_dir, f"rob_traffic_light_{tool_name.lower().replace('-', '_')}.png"),
            )
            plot_paths[tool_name] = path
        except Exception as exc:
            logger.warning(f"[RiskOfBias] Traffic-light plot failed for {tool_name}: {exc}")

    logger.info(f"[RiskOfBias] {len(assessments)} papers assessed.")
    return {"rob_assessments": assessments, "rob_plot_paths": plot_paths}
