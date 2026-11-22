"""Pure functions mapping a (raw, Pydantic-instances-included) `GraphState`
dict to the normalized child-table row lists described in
migrations/0001_initial.sql. NO DATABASE ACCESS HERE -- these are plain
functions of a dict, independently unit-testable without Postgres, called
by run_store.persist_snapshot() (Phase 3) which does the actual writing.

Field names mirror the corresponding models.py class field-for-field (see
each function's docstring for which class) -- never invent new names here.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from models import PaperRecord, StudyData, EffectSizeRecord, MetaAnalysisGroupResult


def _model_dict(obj: Any) -> Dict[str, Any]:
    """model_dump(mode='json') for a Pydantic instance, or pass a plain
    dict through unchanged -- snapshot functions accept either, since some
    callers (tests) build fixtures as plain dicts."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    return dict(obj)


def derive_run_summary(graph_state: Dict[str, Any]) -> Dict[str, Any]:
    """Scalar `runs`-table fields derivable from GraphState -- deliberately
    read from the RAW GraphState, not PipelineState, since several of
    PipelineState's equivalent counters are dead (always 0) post-conversion
    (see orchestrator.py::_to_pipeline_state()). Returns only the keys it
    can derive; callers merge this into their own UPDATE."""
    plan = graph_state.get("plan")
    papers_eligible = graph_state.get("papers_eligible") or []
    effect_sizes = graph_state.get("effect_sizes") or []
    stats_engine_info = graph_state.get("stats_engine_info")

    out: Dict[str, Any] = {
        "n_search_retrieved": graph_state.get("n_search_retrieved"),
        "n_screened_excluded": graph_state.get("n_screened_excluded"),
        "n_eligibility_excluded": graph_state.get("n_eligibility_excluded"),
        "n_papers_eligible": len(papers_eligible) if papers_eligible else None,
        "n_effect_sizes": len(effect_sizes) if effect_sizes else None,
    }
    if plan is not None:
        plan_dict = _model_dict(plan)
        out["plan_json"] = plan_dict
    if stats_engine_info:
        out["stats_engine"] = dict(stats_engine_info)
    return {k: v for k, v in out.items() if v is not None}


def build_paper_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.PaperRecord + models.ScreeningDecision +
    models.EligibilityDecision, joined by paper_id. Source lists:
    `all_retrieved_papers`/`papers_eligible` (PaperRecord.id is the join
    key, NOT a field literally named paper_id) and the
    `screening_decisions`/`eligibility_decisions` dicts (keyed by paper_id
    -- see pipeline_graph.GraphState)."""
    papers_by_id: Dict[str, Dict[str, Any]] = {}
    for source_key in ("all_retrieved_papers", "papers_eligible"):
        for paper in graph_state.get(source_key) or []:
            d = _model_dict(paper)
            pid = d.get("id")
            if not pid:
                continue
            # papers_eligible wins over all_retrieved_papers on conflict --
            # it's the more-authoritative, later-stage list.
            if pid not in papers_by_id or source_key == "papers_eligible":
                papers_by_id[pid] = d

    screening = {d.get("paper_id"): d for d in (graph_state.get("screening_decisions") or {}).values()} \
        if isinstance(graph_state.get("screening_decisions"), dict) else \
        {getattr(d, "paper_id", None) or d.get("paper_id"): _model_dict(d) for d in (graph_state.get("screening_decisions") or [])}
    eligibility = {d.get("paper_id"): d for d in (graph_state.get("eligibility_decisions") or {}).values()} \
        if isinstance(graph_state.get("eligibility_decisions"), dict) else \
        {getattr(d, "paper_id", None) or d.get("paper_id"): _model_dict(d) for d in (graph_state.get("eligibility_decisions") or [])}

    rows: List[Dict[str, Any]] = []
    for pid, p in papers_by_id.items():
        scr = screening.get(pid) or {}
        elig = eligibility.get(pid) or {}
        rows.append({
            "paper_id": pid,
            "title": p.get("title"),
            "authors": p.get("authors") or [],
            "year": p.get("year"),
            "doi": p.get("doi"),
            "pmid": p.get("pmid"),
            "url": p.get("url"),
            "pdf_url": p.get("pdf_url"),
            "source": p.get("source"),
            "provenance": p.get("provenance") or [],
            "document_type": p.get("document_type"),
            "trial_registry_id": p.get("trial_registry_id"),
            "trial_cluster_id": p.get("trial_cluster_id"),
            "is_uploaded": (p.get("source") == "manual"),
            "has_full_text": bool(p.get("full_text")),
            "full_text_chars": len(p["full_text"]) if p.get("full_text") else None,
            "screening_decision": scr.get("decision"),
            "screening_reason": scr.get("reason"),
            "eligibility_decision": elig.get("decision"),
            "eligibility_reason": elig.get("reason"),
            "exclusion_criterion": elig.get("exclusion_criterion"),
        })
    return rows


def build_study_rows(included_studies: Optional[List[Any]]) -> List[Dict[str, Any]]:
    """Mirrors models.StudyData. Takes an explicit list rather than reading
    it off GraphState directly -- GraphState itself has no single
    "studies" key; the closest equivalent (`PipelineState.included_studies`)
    is derived downstream by orchestrator.py::_to_pipeline_state(). Callers
    (run_service) pass that derived list in."""
    rows: List[Dict[str, Any]] = []
    for s in included_studies or []:
        d = _model_dict(s)
        rows.append({
            "study_id": d.get("study_id"),
            "paper_id": d.get("paper_id") or None,
            "title": d.get("title"),
            "treatment_label": d.get("treatment_label"),
            "control_label": d.get("control_label"),
            "n_participants": d.get("n_participants"),
            "n_treatment": d.get("n_treatment"),
            "n_control": d.get("n_control"),
            "moderators": d.get("moderators") or {},
        })
    return rows


def build_effect_size_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.EffectSizeRecord field-for-field. Note EffectSizeRecord
    has no `paper_id` field of its own (only `study_id`/`report_id`) -- the
    paper_id column stays NULL here; a future phase could backfill it via a
    study_id/report_id -> paper_id join through paper_results, but that's
    not needed for round-trip correctness so it's deliberately deferred."""
    rows: List[Dict[str, Any]] = []
    for es in graph_state.get("effect_sizes") or []:
        d = _model_dict(es)
        rows.append({
            "study_id": d.get("study_id"),
            "report_id": d.get("report_id"),
            "paper_id": None,
            "outcome_group_key": d.get("outcome_group_key"),
            "outcome_name": d.get("outcome_name"),
            "outcome_family": d.get("outcome_family"),
            "comparison_family": d.get("comparison_family"),
            "follow_up_timepoint": d.get("follow_up_timepoint"),
            "unit_of_analysis": d.get("unit_of_analysis"),
            "trial_cluster_id": d.get("trial_cluster_id"),
            "effect_measure": d.get("effect_measure"),
            "computation_scale": d.get("computation_scale"),
            "reported_effect_measure": d.get("reported_effect_measure"),
            "outcome_units": d.get("outcome_units"),
            "cohens_d": d.get("cohens_d"),
            "hedges_g": d.get("hedges_g"),
            "native_value": d.get("native_value"),
            "native_variance": d.get("native_variance"),
            "variance": d.get("variance"),
            "se": d.get("se"),
            "ci_lower": d.get("ci_lower"),
            "ci_upper": d.get("ci_upper"),
            "weight": d.get("weight"),
            "n_total": d.get("n_total"),
            "computation_method": d.get("computation_method"),
            "conversion_method": d.get("conversion_method"),
            "effect_direction": d.get("effect_direction"),
            "raw": d.get("raw_measure_inputs") or {},
        })
    return rows


def build_outcome_group_and_pooled_rows(graph_state: Dict[str, Any]) -> tuple:
    """Mirrors models.MetaAnalysisGroupResult (-> run_outcome_groups) and its
    nested `result: MetaAnalysisResult` (-> run_pooled_results). `is_primary`
    is determined by object identity against `meta_result` (the top-level
    alias set by meta_analysis_node -- see agents/meta_analysis_agent.py),
    the SAME technique dashboard.py's _results_from_pipeline_state() already
    uses, so this table's notion of "primary" never drifts from what the
    dashboard shows. Returns (outcome_group_rows, pooled_result_rows)."""
    groups = graph_state.get("meta_results") or []
    primary_result = graph_state.get("meta_result")

    group_rows: List[Dict[str, Any]] = []
    pooled_rows: List[Dict[str, Any]] = []
    for g in groups:
        gd = _model_dict(g)
        result = getattr(g, "result", None) if hasattr(g, "result") else gd.get("result")
        is_primary = bool(primary_result) and result is primary_result
        group_rows.append({
            "outcome_group_key": gd.get("outcome_group_key"),
            "label": gd.get("label"),
            "outcome_family": gd.get("outcome_family"),
            "comparison_family": gd.get("comparison_family"),
            "follow_up_timepoint": gd.get("follow_up_timepoint"),
            "k": gd.get("k"),
            "n_total": gd.get("n_total"),
            "insufficient_data": bool(gd.get("insufficient_data")),
            "single_effect_g": gd.get("single_effect_g"),
            "split_reason": gd.get("split_reason"),
            "study_ids": gd.get("study_ids") or [],
            "effect_measure": gd.get("effect_measure"),
            "computation_scale": gd.get("computation_scale"),
            "effect_measure_source": gd.get("effect_measure_source"),
            "effect_measure_conflict": gd.get("effect_measure_conflict"),
            "is_primary": is_primary,
        })
        if result is not None:
            rd = _model_dict(result)
            pooled_rows.append({
                "outcome_group_key": gd.get("outcome_group_key"),
                "pooled_effect": rd.get("pooled_effect"),
                "pooled_g": rd.get("pooled_g"),
                "pooled_se": rd.get("pooled_se"),
                "ci_lower": rd.get("ci_lower"),
                "ci_upper": rd.get("ci_upper"),
                "z_value": rd.get("z_value"),
                "p_value": rd.get("p_value"),
                "tau_squared": rd.get("tau_squared"),
                "tau": rd.get("tau"),
                "i_squared": rd.get("i_squared"),
                "h_squared": rd.get("h_squared"),
                "q_statistic": rd.get("q_statistic"),
                "q_df": rd.get("q_df"),
                "q_p_value": rd.get("q_p_value"),
                "k": rd.get("k"),
                "n_total": rd.get("n_total"),
                "method": rd.get("method"),
                "effect_measure": rd.get("effect_measure"),
                "computation_scale": rd.get("computation_scale"),
                "effect_measure_source": rd.get("effect_measure_source"),
                "effect_measure_conflict": rd.get("effect_measure_conflict"),
                "is_primary": is_primary,
            })
    return group_rows, pooled_rows


def build_moderator_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.ModeratorResult. moderator_results is not currently
    grouped by outcome_group_key in GraphState, so that column stays NULL."""
    rows = []
    for m in graph_state.get("moderator_results") or []:
        d = _model_dict(m)
        rows.append({
            "outcome_group_key": None,
            "moderator_name": d.get("moderator_name"),
            "qm_statistic": d.get("qm_statistic"),
            "qm_df": d.get("qm_df"),
            "qm_p_value": d.get("qm_p_value"),
            "reference_category": d.get("reference_category"),
            "subgroups": d.get("subgroups") or [],
            "coefficients": d.get("coefficients") or {},
        })
    return rows


def build_bias_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.BiasResult. Today's pipeline computes ONE bias result
    for the whole run (not per outcome group), so at most one row."""
    bias = graph_state.get("bias_result")
    if bias is None:
        return []
    d = _model_dict(bias)
    return [{
        "outcome_group_key": None,
        "eggers_intercept": d.get("eggers_intercept"),
        "eggers_se": d.get("eggers_se"),
        "eggers_t_value": d.get("eggers_t_value"),
        "eggers_p_value": d.get("eggers_p_value"),
        "trim_fill_k0": d.get("trim_fill_k0"),
        "trim_fill_side": d.get("trim_fill_side"),
        "trim_fill_g": d.get("trim_fill_g"),
        "trim_fill_ci_lower": d.get("trim_fill_ci_lower"),
        "trim_fill_ci_upper": d.get("trim_fill_ci_upper"),
        "bias_risk": d.get("bias_risk"),
    }]


def build_rob_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.RiskOfBiasAssessment (domain_judgments -- a list of
    RoBDomainJudgment -- stored as jsonb verbatim)."""
    rows = []
    for r in graph_state.get("rob_assessments") or []:
        d = _model_dict(r)
        rows.append({
            "paper_id": d.get("paper_id"),
            "paper_title": d.get("paper_title"),
            "design_classification": d.get("design_classification"),
            "design_rationale": d.get("design_rationale"),
            "tool_used": d.get("tool_used"),
            "overall_risk": d.get("overall_risk"),
            "overall_summary": d.get("overall_summary"),
            "domain_judgments": d.get("domain_judgments") or [],
        })
    return rows


def build_validation_flag_rows(graph_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mirrors models.ValidationFlag."""
    rows = []
    for f in graph_state.get("validation_flags") or []:
        d = _model_dict(f)
        rows.append({
            "stage": d.get("stage"),
            "severity": d.get("severity"),
            "subject_id": d.get("subject_id"),
            "message": d.get("message"),
            "auto_action": d.get("auto_action"),
        })
    return rows
