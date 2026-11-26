"""
LangGraph pipeline — replaces orchestrator.py's hand-rolled stage loop.

Each pipeline stage is a node function: (GraphState) -> dict
The dict contains only the keys that this node updates.
Nodes are wired into a StateGraph in the build_graph() function at the bottom.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared graph state
# ---------------------------------------------------------------------------

class GraphState(TypedDict):
    # --- Inputs ---
    user_prompt:    str
    mode:           str          # "manual" | "search"
    paper_files:    List[str]
    output_dir:     str
    pooling_model:  Optional[str]   # dashboard's pooling-model choice; copied onto plan by plan_node

    # --- Stage outputs ---
    plan:             Optional[Any]   # MetaAnalysisPlan
    papers_eligible:  List[Any]       # List[PaperRecord]
    study_maps:       Dict[str, Any]  # paper_id -> study map dict
    rq_maps:          Dict[str, Any]  # paper_id -> {research_questions, content_sections}
    paper_results:    List[Dict]      # raw statistical result rows
    mapped_results:   List[Dict]      # after CrossPaperOutcomeMapper
    coded_csv_path:   str             # path to meta_ready_results.csv

    # --- Analysis ---
    effect_sizes:         List[Any]       # List[EffectSizeRecord]
    meta_result:          Optional[Any]   # MetaAnalysisResult -- alias for the "primary" (largest) outcome group; see meta_results
    meta_plots:           Dict[str, str]  # name -> file path -- primary group's plots only
    meta_interpretation:  Dict[str, str]  # primary group's LLM interpretation only
    meta_results:          List[Any]       # List[MetaAnalysisGroupResult] -- one per outcome_group_key, see agents/meta_analysis_agent.py
    meta_group_plots:      Dict[str, Dict[str, str]]  # outcome_group_key -> {plot_name: path}
    meta_group_interpretation: Dict[str, str]          # outcome_group_key -> interpretation text
    stats_engine_info:    Optional[Dict[str, str]]  # {"r_version", "metafor_version"} -- proof metafor actually ran
    moderator_results:    List[Any]       # List[ModeratorResult]
    combined_model:       Dict[str, Any]
    bias_result:          Optional[Any]   # BiasResult
    bias_funnel_path:     str
    bias_interpretation:  Dict[str, str]
    rob_assessments:      List[Any]       # List[RiskOfBiasAssessment]
    rob_plot_paths:       Dict[str, str]  # tool_name ("RoB2"|"ROBINS-I") -> file path

    # --- Per-paper tracking (populated by screen/eligibility nodes) ---
    all_retrieved_papers:   List[Any]       # snapshot of all papers before screening (search mode)
    screening_decisions:    Dict[str, Any]  # paper_id -> {decision, reason, title}
    eligibility_decisions:  Dict[str, Any]  # paper_id -> {decision, reason, exclusion_criterion, title}
    search_rejected_papers: List[Dict]      # papers found by DB but rejected by relevance filter
    papers_no_fulltext:     List[str]       # paper_ids dropped because no full text could be found
    papers_no_fulltext_reasons: Dict[str, str]  # paper_id -> retrieval failure/budget reason

    # --- PRISMA counts (populated by search/screen/eligibility nodes) ---
    n_search_retrieved:    int   # papers kept by search_node (after dedup)
    n_duplicates_removed:  int   # candidate records merged as duplicates by _CandidateIndex (search mode)
    n_screened_excluded:   int   # papers excluded at title/abstract screening (-1 if skipped)
    n_eligibility_excluded: int  # papers excluded at full-text eligibility (-1 if skipped)

    # --- Final ---
    report_path:           str
    prisma_flowchart_path: str
    audit_csv_path:        str
    review_tracking_csv_path: str
    errors:                List[str]

    # --- Validation/audit trail (see models.ValidationFlag) ---
    validation_flags:      List[Any]   # List[ValidationFlag] -- structured, never-silent record of
                                        # missing/incompatible/ambiguous/misclassified data at every stage
    document_type_excluded: List[Dict]  # manual mode only -- papers agents/document_type_agent.py
                                        # dropped from papers_eligible, {paper_id, title, document_type,
                                        # rationale} each -- surfaced as real rows in paper_tracking.csv


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _extract_tool_args(messages: list, tool_name: str) -> dict:
    """Return args of the last call to `tool_name` in message history, or {}."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == tool_name:
                    return dict(tc["args"])
    return {}


def _all_tool_args(messages: list, tool_name: str) -> list:
    """Return args dicts for every call to `tool_name` in message history."""
    results = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == tool_name:
                    results.append(dict(tc["args"]))
    return results


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------

def _route_mode(state: GraphState) -> str:
    if state.get("paper_files"):
        return "manual_ingest_node"
    return "search_node"


def _route_after_effects(state: GraphState) -> str:
    if not state.get("effect_sizes"):
        return "risk_of_bias_node"
    return "meta_analysis_node"


# ---------------------------------------------------------------------------
# Graph assembly  (nodes imported lazily to avoid circular imports)
# ---------------------------------------------------------------------------

def _add_downstream_nodes(g: StateGraph) -> None:
    from agents.study_detector_agent               import study_detection_node
    from agents.research_question_detector_agent   import rq_detection_node
    from agents.statistical_result_extractor_agent import extraction_node
    from agents.statistical_result_checker_agent   import validation_node
    from agents.relevance_filter_agent     import relevance_filter_node
    from agents.cross_paper_outcome_mapper_agent   import mapping_node
    from agents.effect_size_agent          import effect_size_node, export_table_node
    from agents.meta_analysis_agent        import meta_analysis_node
    from agents.moderator_agent            import moderator_node
    from agents.bias_agent                 import bias_node
    from agents.risk_of_bias_agent         import risk_of_bias_node
    from agents.report_agent               import report_node
    from agents.prisma_flowchart_agent     import prisma_node
    from agents.pipeline_audit_agent      import pipeline_audit_node

    g.add_node("study_detection_node",   study_detection_node)
    g.add_node("rq_detection_node",      rq_detection_node)
    g.add_node("extraction_node",        extraction_node)
    g.add_node("validation_node",       validation_node)
    g.add_node("relevance_filter_node", relevance_filter_node)
    g.add_node("mapping_node",          mapping_node)
    g.add_node("export_table_node",     export_table_node)
    g.add_node("effect_size_node",      effect_size_node)
    g.add_node("meta_analysis_node",    meta_analysis_node)
    g.add_node("moderator_node",        moderator_node)
    g.add_node("bias_node",             bias_node)
    g.add_node("risk_of_bias_node",     risk_of_bias_node)
    g.add_node("report_node",           report_node)
    g.add_node("prisma_node",           prisma_node)
    g.add_node("pipeline_audit_node",   pipeline_audit_node)

    g.add_edge("study_detection_node",  "rq_detection_node")
    g.add_edge("rq_detection_node",     "extraction_node")
    g.add_edge("extraction_node",       "validation_node")
    g.add_edge("validation_node",       "relevance_filter_node")
    g.add_edge("relevance_filter_node", "mapping_node")
    g.add_edge("mapping_node",          "export_table_node")
    g.add_edge("export_table_node",     "effect_size_node")

    g.add_conditional_edges("effect_size_node", _route_after_effects, {
        "risk_of_bias_node":  "risk_of_bias_node",
        "meta_analysis_node": "meta_analysis_node",
    })
    g.add_edge("meta_analysis_node", "moderator_node")
    g.add_edge("moderator_node",     "bias_node")
    g.add_edge("bias_node",          "risk_of_bias_node")
    g.add_edge("risk_of_bias_node",  "report_node")
    g.add_edge("report_node",        "prisma_node")
    g.add_edge("prisma_node",        "pipeline_audit_node")
    g.add_edge("pipeline_audit_node", END)


def build_post_eligibility_graph():
    """Build the resume graph that starts after user paper-tracking approval."""
    g = StateGraph(GraphState)
    _add_downstream_nodes(g)
    g.set_entry_point("study_detection_node")
    return g.compile()


def build_post_fulltext_graph(stop_after_eligibility: bool = False):
    """Build the resume graph that starts after the full-text human-in-the-loop
    upload pause (Stage 3b). fetch_fulltext_node already ran once before the
    pause; this graph starts at eligibility_node so any manually-uploaded
    papers go through the same eligibility assessment as automatically
    retrieved ones. Mirrors build_graph()'s stop_after_eligibility branch so
    the existing paper-tracking review gate still runs afterward.
    """
    from agents.eligibility_agent    import eligibility_node
    from agents.pipeline_audit_agent import paper_tracking_review_node

    g = StateGraph(GraphState)
    g.add_node("eligibility_node",           eligibility_node)
    g.add_node("paper_tracking_review_node", paper_tracking_review_node)
    _add_downstream_nodes(g)

    g.set_entry_point("eligibility_node")
    if stop_after_eligibility:
        g.add_edge("eligibility_node", "paper_tracking_review_node")
        g.add_edge("paper_tracking_review_node", END)
    else:
        g.add_edge("eligibility_node", "study_detection_node")
    return g.compile()


def build_post_search_graph():
    """Build the resume graph that starts after the paper-selection pause
    (right after the search agent): runs full-text fetch for the papers the
    user kept (papers that already carry full_text, e.g. manually added PDFs,
    are skipped by fetch_fulltext_node) and stops there, so the caller can
    apply the existing full-text upload pause logic."""
    from agents.paper_reading_agent import fetch_fulltext_node
    from agents.screening_agent import title_abstract_screen_node

    g = StateGraph(GraphState)
    g.add_node("screen_node", title_abstract_screen_node)
    g.add_node("fetch_fulltext_node", fetch_fulltext_node)
    g.set_entry_point("screen_node")
    g.add_edge("screen_node", "fetch_fulltext_node")
    g.add_edge("fetch_fulltext_node", END)
    return g.compile()


def build_graph(stop_after_eligibility: bool = False, stop_after_fulltext: bool = False,
                stop_after_search: bool = False):
    from agents.planning_agent              import plan_node
    from agents.search_agent               import search_node
    from agents.paper_reading_agent        import (manual_ingest_node,
                                                    fetch_fulltext_node)
    from agents.document_type_agent        import document_type_node
    from agents.eligibility_agent          import eligibility_node
    from agents.pipeline_audit_agent       import paper_tracking_review_node
    from agents.screening_agent            import title_abstract_screen_node

    g = StateGraph(GraphState)

    g.add_node("plan_node",             plan_node)
    g.add_node("manual_ingest_node",    manual_ingest_node)
    g.add_node("document_type_node",    document_type_node)
    g.add_node("search_node",           search_node)
    g.add_node("screen_node",           title_abstract_screen_node)
    g.add_node("fetch_fulltext_node",   fetch_fulltext_node)
    g.add_node("eligibility_node",      eligibility_node)
    g.add_node("paper_tracking_review_node", paper_tracking_review_node)
    _add_downstream_nodes(g)

    g.set_entry_point("plan_node")
    g.add_conditional_edges("plan_node", _route_mode, {
        "manual_ingest_node": "manual_ingest_node",
        "search_node":        "search_node",
    })

    # search path: relevance filter → title/abstract screen → full-text fetch → [optional pause for
    # missing-PDF upload] → eligibility → [optional pause for paper-tracking
    # review] → extraction
    if stop_after_search:
        # The resume graph (build_post_search_graph) runs full-text fetch
        # after the paper-selection pause.
        g.add_edge("search_node", END)
    elif stop_after_fulltext:
        g.add_edge("search_node", "screen_node")
        g.add_edge("screen_node", "fetch_fulltext_node")
        g.add_edge("fetch_fulltext_node", END)
    else:
        g.add_edge("search_node", "screen_node")
        g.add_edge("screen_node", "fetch_fulltext_node")
        g.add_edge("fetch_fulltext_node", "eligibility_node")
        if stop_after_eligibility:
            g.add_edge("eligibility_node", "paper_tracking_review_node")
            g.add_edge("paper_tracking_review_node", END)
        else:
            g.add_edge("eligibility_node", "study_detection_node")

    # manual path: document-type gate (drops review/protocol/duplicate PDFs
    # accidentally included among the uploaded "primary study" files -- see
    # agents/document_type_agent.py) then merges at study detection, exactly
    # like the search path's eligibility_node does for its own papers.
    g.add_edge("manual_ingest_node", "document_type_node")
    g.add_edge("document_type_node", "study_detection_node")

    return g.compile()


compiled_graph = build_graph()
