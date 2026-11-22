"""Study Detector agent — Stage 3A. Pattern 1: record-output tool per paper."""

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

SYSTEM_PROMPT = (
    "You are a scientific-paper structure analyst specialised in identifying "
    "independent studies within a single paper.\n\n"
    "A paper may report one study or several (Study 1 / Study 2, "
    "Experiment 1 / Experiment 2, Wave 1 / Wave 2, etc.). Your job is to "
    "detect every independent study and record its sample size, design, "
    "treatment/control groups, primary outcome variables, and where its "
    "results appear in the paper.\n\n"
    "Rules:\n"
    "- A 'study' is an independent data-collection episode with its own sample. "
    "Separate conditions within ONE dataset are NOT separate studies.\n"
    "- Do not invent studies. If the paper has one study, record only one.\n"
    "- Every study record must cite where in the paper its results appear.\n"
    "- Call `record_study` once per study."
)


@tool
def record_study(
    paper_id: str,
    study_label: str,
    study_number: int,
    design: str,
    primary_outcomes: List[str],
    evidence_quote: str,
    page_or_section: str,
    n_total: Optional[float] = None,
    n_treatment: Optional[float] = None,
    n_control: Optional[float] = None,
    treatment_group_label: Optional[str] = None,
    control_group_label: Optional[str] = None,
    secondary_outcomes: Optional[List[str]] = None,
    results_location: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Record one independent study found within the paper.
    design: between_subjects | within_subjects | mixed | correlational | quasi_experimental | other"""
    return "study_recorded"


_MAX_CHARS = 70_000

_agent = create_react_agent(llm, [record_study], prompt=SYSTEM_PROMPT)


def study_detection_node(state: GraphState) -> dict:
    """Stage 3A: detect independent studies within each eligible paper."""
    logger.info("=== STAGE 3A: Study Detection ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    output_dir: str = state["output_dir"]
    all_study_maps: Dict[str, Any] = {}

    for paper in papers:
        try:
            text = (paper.full_text or paper.abstract or "")[:_MAX_CHARS]
            user_msg = (
                f"Detect all independent studies in this paper.\n\n"
                f"Paper ID : {paper.id}\n"
                f"Title    : {paper.title}\n\n"
                f"Abstract:\n{paper.abstract}\n\n"
                f"Full text:\n{text}\n\n"
                "Instructions:\n"
                "1. Scan the full text for markers that indicate an independent study:\n"
                "   • Explicit labels: 'Study 1', 'Study 2', 'Experiment 1', "
                "'Experiment 2', 'Wave 1', 'Phase 1', pilot study, replication study.\n"
                "   • Separate Methods / Participants / Results subsections per study.\n"
                "   • Different sample sizes reported for different experiments.\n"
                "2. If there is only ONE study, record it with study_label='Study 1', "
                "study_number=1.\n"
                "3. For each study record:\n"
                "   • n_total, n_treatment, n_control from the Participants section.\n"
                "   • treatment_group_label and control_group_label.\n"
                "   • primary_outcomes: outcome variable names measured in this study.\n"
                "   • results_location: table number or section where statistics appear.\n"
                "   • A 1–2 sentence description of what the study tested.\n"
                "4. Call `record_study` once per independent study.\n"
                "5. Do NOT create separate records for sub-conditions within one study."
            )
            result = _agent.invoke({"messages": [("user", user_msg)]})

            studies = _all_tool_args(result["messages"], "record_study")
            if not studies:
                logger.warning(f"[StudyDetector] {paper.id}: no studies detected — inserting default.")
                studies = [{
                    "paper_id": paper.id, "study_label": "Study 1", "study_number": 1,
                    "design": "unclear", "primary_outcomes": [],
                    "evidence_quote": "(default — detection failed)", "page_or_section": "unknown",
                }]
            study_labels = [s.get("study_label", f"Study {i+1}") for i, s in enumerate(studies)]
            all_study_maps[paper.id] = {
                "studies":       studies,
                "total_studies": len(studies),
                "study_labels":  study_labels,
            }
            logger.info(f"[StudyDetector] {paper.id}: {len(studies)} studies detected — {study_labels}")
        except Exception as exc:
            logger.error(f"[StudyDetector] {paper.id}: skipped due to error — {exc}")
            all_study_maps[paper.id] = {"studies": [], "total_studies": 0, "study_labels": []}

    save_json(all_study_maps, os.path.join(output_dir, "study_maps.json"))
    return {"study_maps": all_study_maps}
