"""
Meta-Analysis Orchestrator — thin adapter over the LangGraph pipeline.

dashboard.py calls MetaAnalysisOrchestrator.run() and run_downstream().
These methods are preserved with their original signatures; internally
they now delegate to pipeline_graph.build_graph().invoke().
"""

import logging
import os
from typing import List, Optional

from config import OUTPUT_DIR
from core_utils import load_json, ensure_dir, setup_logging
from models import PipelineState, MetaAnalysisPlan, StudyData

logger = logging.getLogger(__name__)


def _initial_graph_state(
    user_prompt: str,
    output_dir: str,
    paper_files: Optional[List[str]] = None,
    pooling_model: Optional[str] = None,
) -> dict:
    if paper_files:
        mode = "manual"
    else:
        mode = "search"
    return {
        "user_prompt":   user_prompt,
        "mode":          mode,
        "paper_files":   paper_files or [],
        "output_dir":    output_dir,
        "pooling_model": pooling_model,   # dashboard drop-down; None = prompt/default (see plan_node)
        "plan":          None,
        "papers_eligible": [],
        "study_maps":    {},
        "rq_maps":       {},
        "paper_results": [],
        "mapped_results": [],
        "coded_csv_path": "",
        "effect_sizes":  [],
        "meta_result":   None,
        "meta_plots":    {},
        "meta_interpretation": {},
        "meta_results":  [],
        "meta_group_plots": {},
        "meta_group_interpretation": {},
        "stats_engine_info": None,
        "moderator_results": [],
        "combined_model": {},
        "bias_result":   None,
        "bias_funnel_path": "",
        "bias_interpretation": {},
        "rob_assessments": [],
        "rob_plot_paths": {},
        "all_retrieved_papers":    [],
        "screening_decisions":     {},
        "eligibility_decisions":   {},
        "search_rejected_papers":  [],
        "papers_no_fulltext":      [],
        "papers_no_fulltext_reasons": {},
        "report_path":             "",
        "prisma_flowchart_path":   "",
        "audit_csv_path":          "",
        "review_tracking_csv_path": "",
        "n_search_retrieved":      0,
        "n_duplicates_removed":    0,
        "n_screened_excluded":     -1,
        "n_eligibility_excluded":  -1,
        "errors":                  [],
        "validation_flags":        [],
        "document_type_excluded":  [],
    }


def _to_pipeline_state(graph_result: dict) -> PipelineState:
    """Convert GraphState dict → legacy PipelineState Pydantic model."""
    plan = graph_result.get("plan")
    state = PipelineState()

    if plan:
        state.plan = plan

    eligible = graph_result.get("papers_eligible", [])
    state.search_n_retrieved    = len(eligible)
    state.screening_n_included  = len(eligible)
    state.eligibility_n_included = len(eligible)

    # Count unique papers that had at least one result extracted
    paper_results = graph_result.get("paper_results", [])
    unique_extracted = set(
        r.get("paper_id", "") for r in paper_results if r.get("paper_id")
    )
    state.included_studies = [
        StudyData(study_id=pid, report_id=pid) for pid in unique_extracted
    ]

    state.effect_sizes   = graph_result.get("effect_sizes", [])
    state.meta_analysis  = graph_result.get("meta_result")
    state.meta_analysis_groups = graph_result.get("meta_results", [])
    state.bias_result    = graph_result.get("bias_result")
    state.report_path    = graph_result.get("report_path", "")
    state.moderator_results = graph_result.get("moderator_results", [])
    state.rob_assessments = graph_result.get("rob_assessments", [])
    state.stats_engine_info = graph_result.get("stats_engine_info")
    state.validation_flags = graph_result.get("validation_flags", [])

    return state


class MetaAnalysisOrchestrator:
    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = output_dir
        ensure_dir(output_dir)
        # The raw GraphState dict from the most recent completing call below
        # -- stashed here because _to_pipeline_state() (below) discards
        # several fields PipelineState doesn't carry (e.g. n_search_retrieved/
        # n_screened_excluded/n_eligibility_excluded stay 0 on PipelineState
        # post-conversion). persistence/run_service.py (Phase 3) reads this
        # to persist the richer raw state -- purely additive, no existing
        # caller of run()/continue_after_review()/run_downstream() needs to
        # change; this is populated whether or not anything ever reads it.
        self.last_graph_state: Optional[dict] = None

    def run(
        self,
        user_prompt: str,
        paper_files: Optional[List[str]] = None,
        pooling_model: Optional[str] = None,
    ) -> PipelineState:
        """Run the full pipeline via LangGraph StateGraph."""
        from pipeline_graph import build_graph, GraphState

        setup_logging(logging.INFO)
        logger.info("=== Starting Automated Meta-Analysis Pipeline ===")
        logger.info(f"    Prompt: {user_prompt}")

        if paper_files:
            mode = "manual"
            logger.info(f"    Mode: Manual Upload ({len(paper_files)} files)")
        else:
            mode = "search"
            logger.info("    Mode: Database Search")

        graph = build_graph()
        initial: GraphState = _initial_graph_state(
            user_prompt, self.output_dir, paper_files, pooling_model
        )

        result = graph.invoke(initial)
        self.last_graph_state = result

        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")

        logger.info("=== FULL PIPELINE COMPLETE ===")
        return _to_pipeline_state(result)

    def run_until_review(
        self,
        user_prompt: str,
        paper_files: Optional[List[str]] = None,
        pooling_model: Optional[str] = None,
    ) -> dict:
        """Run search mode through eligibility and write paper_tracking.csv."""
        from pipeline_graph import build_graph, GraphState

        setup_logging(logging.INFO)
        logger.info("=== Starting Automated Meta-Analysis Pipeline ===")
        logger.info(f"    Prompt: {user_prompt}")
        if paper_files:
            logger.info(f"    Mode: Manual Upload ({len(paper_files)} files)")
        else:
            logger.info("    Mode: Database Search")

        graph = build_graph(stop_after_eligibility=True)
        initial: GraphState = _initial_graph_state(
            user_prompt, self.output_dir, paper_files, pooling_model
        )
        result = graph.invoke(initial)
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== PAPER REVIEW READY ===")
        return result

    def run_until_search_review(
        self,
        user_prompt: str,
        paper_files: Optional[List[str]] = None,
        pooling_model: Optional[str] = None,
    ) -> dict:
        """Run search mode through the search agent and pause there, so the
        user can decline found papers and add further PDFs before full-text
        retrieval (see continue_after_search_review)."""
        from pipeline_graph import build_graph, GraphState

        setup_logging(logging.INFO)
        logger.info("=== Starting Automated Meta-Analysis Pipeline ===")
        logger.info(f"    Prompt: {user_prompt}")
        logger.info("    Mode: Database Search")

        graph = build_graph(stop_after_search=True)
        initial: GraphState = _initial_graph_state(
            user_prompt, self.output_dir, paper_files, pooling_model
        )
        result = graph.invoke(initial)
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== PAPER SELECTION READY ===")
        return result

    def continue_after_search_review(
        self,
        graph_state: dict,
        excluded_ids: Optional[List[str]] = None,
        pdf_paths: Optional[List[str]] = None,
    ) -> dict:
        """Resume after the paper-selection pause: apply the user's choices
        (declined papers removed, uploaded PDFs added) and run full-text
        retrieval. Returns the state at the full-text pause, exactly like
        run_until_fulltext_review() does, so the caller can reuse the
        full-text upload logic."""
        from pipeline_graph import build_post_search_graph
        from agents.paper_reading_agent import apply_paper_selection

        setup_logging(logging.INFO)
        logger.info("=== Continuing Pipeline After Paper Selection ===")
        graph_state = dict(graph_state)
        graph_state["output_dir"] = self.output_dir
        graph_state, _summary = apply_paper_selection(
            graph_state, list(excluded_ids or []), list(pdf_paths or []), self.output_dir
        )
        graph = build_post_search_graph()
        result = graph.invoke(graph_state)
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== FULL-TEXT REVIEW READY ===")
        return result

    def run_until_fulltext_review(
        self,
        user_prompt: str,
        paper_files: Optional[List[str]] = None,
        pooling_model: Optional[str] = None,
    ) -> dict:
        """Run search mode through full-text fetch and pause there.

        The caller (dashboard) decides whether to actually show the
        human-in-the-loop upload dialog: if `papers_no_fulltext` in the
        returned state is empty, nothing was dropped and it should call
        continue_after_fulltext_review() immediately without prompting the
        user, so behavior is unchanged when every paper's full text was
        retrieved automatically.
        """
        from pipeline_graph import build_graph, GraphState

        setup_logging(logging.INFO)
        logger.info("=== Starting Automated Meta-Analysis Pipeline ===")
        logger.info(f"    Prompt: {user_prompt}")
        logger.info("    Mode: Database Search")

        graph = build_graph(stop_after_fulltext=True)
        initial: GraphState = _initial_graph_state(
            user_prompt, self.output_dir, paper_files, pooling_model
        )
        result = graph.invoke(initial)
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== FULL-TEXT REVIEW READY ===")
        return result

    def continue_after_fulltext_review(
        self,
        graph_state: dict,
        uploaded_papers: Optional[list] = None,
    ) -> dict:
        """Resume after the full-text upload pause.

        Merges any manually-uploaded papers (already matched and full-text
        extracted by agents.paper_reading_agent.ingest_uploaded_fulltext_pdfs)
        into papers_eligible so they flow through eligibility exactly like an
        automatically-retrieved paper, then runs eligibility and stops again
        for the existing paper-tracking review gate -- matching the standard
        search-mode UX (dashboard.py always stops there).
        """
        from pipeline_graph import build_post_fulltext_graph

        setup_logging(logging.INFO)
        logger.info("=== Continuing Pipeline After Full-Text Upload ===")
        graph_state = dict(graph_state)
        graph_state["output_dir"] = self.output_dir

        if uploaded_papers:
            matched_ids = {p.id for p in uploaded_papers}
            graph_state["papers_eligible"] = list(graph_state.get("papers_eligible", [])) + list(uploaded_papers)
            graph_state["papers_no_fulltext"] = [
                pid for pid in graph_state.get("papers_no_fulltext", []) if pid not in matched_ids
            ]
            reasons = dict(graph_state.get("papers_no_fulltext_reasons", {}))
            for pid in matched_ids:
                reasons.pop(pid, None)
            graph_state["papers_no_fulltext_reasons"] = reasons
            logger.info(f"[Pipeline] {len(uploaded_papers)} manually-uploaded paper(s) injected before eligibility.")

        graph = build_post_fulltext_graph(stop_after_eligibility=True)
        result = graph.invoke(graph_state)
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== PAPER REVIEW READY ===")
        return result

    def continue_after_review(self, graph_state: dict) -> PipelineState:
        """Resume the pipeline after the user accepts paper_tracking.csv."""
        from pipeline_graph import build_post_eligibility_graph

        setup_logging(logging.INFO)
        logger.info("=== Continuing Pipeline After Paper Review ===")
        graph_state = dict(graph_state)
        graph_state["output_dir"] = self.output_dir
        graph = build_post_eligibility_graph()
        result = graph.invoke(graph_state)
        self.last_graph_state = result
        if result.get("errors"):
            for err in result["errors"]:
                logger.error(f"[Pipeline] Error: {err}")
        logger.info("=== FULL PIPELINE COMPLETE ===")
        return _to_pipeline_state(result)

    def run_downstream(self, user_prompt: str) -> PipelineState:
        """Re-run stages 5-9 on an already-existing meta_ready_results.json."""
        from pipeline_graph import GraphState
        from langgraph.graph import StateGraph, END
        from agents.effect_size_agent   import effect_size_node
        from agents.meta_analysis_agent import meta_analysis_node
        from agents.moderator_agent     import moderator_node
        from agents.bias_agent          import bias_node
        from agents.risk_of_bias_agent  import risk_of_bias_node
        from agents.report_agent        import report_node
        from pipeline_graph import _route_after_effects

        setup_logging(logging.INFO)
        logger.info("=== Starting Downstream Analysis (Stages 5-9) ===")

        plan_path = os.path.join(self.output_dir, "plan.json")
        plan = None
        if os.path.exists(plan_path):
            try:
                plan = MetaAnalysisPlan(**load_json(plan_path))
            except Exception:
                pass

        meta_ready_path = os.path.join(self.output_dir, "meta_ready_results.json")
        if not os.path.exists(meta_ready_path):
            logger.error("[Downstream] meta_ready_results.json not found.")
            return PipelineState()

        g = StateGraph(GraphState)
        g.add_node("effect_size_node",   effect_size_node)
        g.add_node("meta_analysis_node", meta_analysis_node)
        g.add_node("moderator_node",     moderator_node)
        g.add_node("bias_node",          bias_node)
        g.add_node("risk_of_bias_node",  risk_of_bias_node)
        g.add_node("report_node",        report_node)
        g.set_entry_point("effect_size_node")
        g.add_conditional_edges("effect_size_node", _route_after_effects, {
            "risk_of_bias_node":  "risk_of_bias_node",
            "meta_analysis_node": "meta_analysis_node",
        })
        g.add_edge("meta_analysis_node", "moderator_node")
        g.add_edge("moderator_node",     "bias_node")
        g.add_edge("bias_node",          "risk_of_bias_node")
        g.add_edge("risk_of_bias_node",  "report_node")
        g.add_edge("report_node",        END)
        downstream_graph = g.compile()

        initial: GraphState = {
            "user_prompt": user_prompt, "mode": "manual",
            "paper_files": [],
            "output_dir":  self.output_dir,
            "plan": plan,
            "papers_eligible": [], "study_maps": {},
            "rq_maps": {},
            "paper_results": [], "mapped_results": [],
            "coded_csv_path": meta_ready_path,
            "effect_sizes": [], "meta_result": None,
            "meta_plots": {}, "meta_interpretation": {},
            "meta_results": [], "meta_group_plots": {}, "meta_group_interpretation": {},
            "stats_engine_info": None,
            "moderator_results": [], "combined_model": {},
            "bias_result": None, "bias_funnel_path": "",
            "bias_interpretation": {},
            "rob_assessments": [], "rob_plot_paths": {},
            "all_retrieved_papers": [], "screening_decisions": {},
            "eligibility_decisions": {}, "search_rejected_papers": [],
            "papers_no_fulltext": [],
            "papers_no_fulltext_reasons": {},
            "report_path": "", "prisma_flowchart_path": "", "audit_csv_path": "",
            "review_tracking_csv_path": "",
            "n_search_retrieved": 0, "n_duplicates_removed": 0,
            "n_screened_excluded": -1,
            "n_eligibility_excluded": -1, "errors": [],
        }

        result = downstream_graph.invoke(initial)
        self.last_graph_state = result
        logger.info("=== DOWNSTREAM ANALYSIS COMPLETE ===")
        return _to_pipeline_state(result)
