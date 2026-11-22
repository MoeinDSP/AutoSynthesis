"""
Pipeline Audit Node — final stage (pure Python, no LLM).

Generates two clean CSV files:

  meta_analysis_summary.csv
      One row. Columns: user_prompt, retrieved_count, screened_in_count,
      screened_out_count, eligible_count, included_count,
      overlap_with_original_count, overlap_with_original_pct.

  study_screening.csv
      One row per paper. Columns: title, year, retrieval_status,
      screening_status, exclusion_stage, exclusion_reason, final_status,
      match_type, matched_gt_title.

Tracks exactly where each study was lost and why:
  - search_relevance_filter  : found by database but rejected as off-topic
  - screening                : excluded at title/abstract screening
  - full_text_fetch          : no full text found from any retrieval strategy (dropped)
  - eligibility              : excluded at full-text eligibility assessment
  - study_detection          : study structure detection failed or no studies found
  - extraction               : no quantitative outcomes extractable
  - effect_size_computation  : insufficient statistics to compute an effect size

Papers for which no full text could be retrieved are dropped before
eligibility assessment — abstract-only fallback is no longer used.

Ground truth (GT) comparison is optional. To enable it, place gt_papers.csv
(with at minimum a 'title' column, optionally 'doi') in the session output
directory or in the project root. A plain text gt_papers.txt (one title per
line) also works.
"""

from __future__ import annotations

import csv
import json as _json
import logging
import os
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

from pipeline_graph import GraphState

logger = logging.getLogger(__name__)

_NEAR_THRESHOLD = 0.85


# ── String helpers ─────────────────────────────────────────────────────────────

def _norm(title: str) -> str:
    t = unicodedata.normalize("NFKD", title.lower())
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _pct(num: int | float, denom: int | float) -> str:
    if not denom:
        return "N/A"
    return f"{100 * num / denom:.1f}%"


# ── Ground-truth loading ───────────────────────────────────────────────────────

def _load_gt(output_dir: str) -> List[Dict]:
    for path in [
        os.path.join(output_dir, "gt_papers.csv"),
        "gt_papers.csv",
        os.path.join(output_dir, "gt_papers.txt"),
        "gt_papers.txt",
    ]:
        if not os.path.exists(path):
            continue
        entries: List[Dict] = []
        if path.endswith(".csv"):
            try:
                with open(path, newline="", encoding="utf-8-sig") as f:
                    for row in csv.DictReader(f):
                        title = (row.get("title") or row.get("Title") or "").strip()
                        if title:
                            entries.append({
                                "title": title,
                                "doi":   (row.get("doi") or row.get("DOI") or "").strip(),
                                "_norm": _norm(title),
                            })
            except Exception as exc:
                logger.warning(f"[Audit] Cannot read GT CSV {path}: {exc}")
        else:
            try:
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        t = line.strip()
                        if t:
                            entries.append({"title": t, "doi": "", "_norm": _norm(t)})
            except Exception as exc:
                logger.warning(f"[Audit] Cannot read GT txt {path}: {exc}")
        if entries:
            logger.info(f"[Audit] Loaded {len(entries)} GT papers from {path}")
            return entries
    return []


def _match(paper_norm: str, paper_doi: str, gt: List[Dict]) -> Tuple[str, str]:
    """Return (match_type, matched_gt_title). match_type: direct|near_match|no_match."""
    for e in gt:
        if paper_doi and paper_doi == e.get("doi", ""):
            return "direct", e["title"]
        if paper_norm == e["_norm"]:
            return "direct", e["title"]
    for e in gt:
        if _sim(paper_norm, e["_norm"]) >= _NEAR_THRESHOLD:
            return "near_match", e["title"]
    return "no_match", ""


# ── CSV writer ─────────────────────────────────────────────────────────────────

def _write(path: str, header: List[str], rows: List[List]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


_STAGE_DISPLAY = {
    "search_relevance_filter": "Search Relevance Filter",
    "screening":               "Screening",
    "full_text_fetch":         "Full-Text Fetch",
    "eligibility":             "Eligibility",
    "study_detection":         "Study Detection",
    "extraction":              "Extraction",
    "effect_size_computation": "Effect Size Computation",
    "retrieval":               "Retrieval",
    "document_type_gate":      "Document Type Gate",
    "unknown":                 "Unknown",
    "-":                       "-",
}

_TRACKING_HEADER = [
    "title",
    "year",
    "source",
    "doi",
    "url",
    "retrieval_status",
    "screening_status",
    "eligibility_status",
    "final_status",
    "loss_stage",
    "loss_reason",
]


def write_preliminary_paper_tracking_csv(state: GraphState) -> str:
    """Write paper_tracking.csv immediately after eligibility for user review."""
    output_dir            = state["output_dir"]
    mode                  = state.get("mode", "search")
    papers_eligible       = state.get("papers_eligible", [])
    all_retrieved         = state.get("all_retrieved_papers", [])
    screening_decisions   = state.get("screening_decisions", {})
    eligibility_decisions = state.get("eligibility_decisions", {})
    search_rejected       = state.get("search_rejected_papers", [])
    no_fulltext_ids       = set(state.get("papers_no_fulltext", []))
    no_fulltext_reasons   = state.get("papers_no_fulltext_reasons", {})
    papers_eligible_ids   = {p.id for p in papers_eligible}
    written_ids: set[str] = set()

    all_papers = all_retrieved if mode == "search" and all_retrieved else papers_eligible
    rows: List[List] = []

    for p in all_papers:
        written_ids.add(p.id)
        scr = screening_decisions.get(p.id, {})
        elig = eligibility_decisions.get(p.id, {})

        if scr.get("decision") == "exclude":
            screening_status = "Screened Out"
            eligibility_status = "N/A"
            final_status = "Not Included"
            loss_stage = "Screening"
            loss_reason = scr.get("reason") or "excluded at title/abstract screening"
        elif p.id in no_fulltext_ids:
            screening_status = "Screened In" if mode == "search" else "N/A"
            eligibility_status = "N/A"
            final_status = "Not Included"
            loss_stage = "Full-Text Fetch"
            loss_reason = no_fulltext_reasons.get(
                p.id, "no full text available from any retrieval strategy"
            )
        elif elig.get("decision") == "exclude":
            screening_status = "Screened In" if mode == "search" else "N/A"
            eligibility_status = "Not Eligible"
            final_status = "Not Included"
            loss_stage = "Eligibility"
            loss_reason = elig.get("reason") or "excluded at eligibility assessment"
        elif elig.get("decision") == "include" or p.id in papers_eligible_ids:
            screening_status = "Screened In" if mode == "search" else "N/A"
            eligibility_status = "Eligible"
            final_status = "Pending Downstream"
            loss_stage = "-"
            loss_reason = "-"
        else:
            screening_status = "Screened In" if mode == "search" else "N/A"
            eligibility_status = "N/A"
            final_status = "Not Included"
            loss_stage = "Unknown"
            loss_reason = "paper dropped from eligible list (reason unknown)"

        rows.append([
            p.title,
            p.year or "",
            getattr(p, "source", ""),
            getattr(p, "doi", "") or "",
            getattr(p, "url", "") or "",
            "Retrieved",
            screening_status,
            eligibility_status,
            final_status,
            loss_stage,
            loss_reason,
        ])

    for rej in search_rejected:
        rej_id = rej.get("id", "")
        if rej_id and rej_id in written_ids:
            continue
        rows.append([
            rej.get("title", ""),
            rej.get("year", ""),
            rej.get("source", ""),
            rej.get("doi", ""),
            rej.get("url", ""),
            "Retrieved",
            "Screened Out",
            "N/A",
            "Not Included",
            "Search Relevance Filter",
            rej.get("reason") or "off-topic: rejected by initial relevance check",
        ])

    path = os.path.join(output_dir, "paper_tracking.csv")
    _write(path, _TRACKING_HEADER, rows)
    logger.info(f"[Review] paper_tracking.csv written for user review ({len(rows)} rows).")
    return path


def paper_tracking_review_node(state: GraphState) -> dict:
    """Pause-point node: write post-eligibility tracking CSV for user review."""
    logger.info("=== STAGE 3C: Paper Tracking Review ===")
    path = write_preliminary_paper_tracking_csv(state)
    return {"review_tracking_csv_path": path}


# ── Effect-size failure reason ─────────────────────────────────────────────────

def _effect_size_reason(rows: List[Dict]) -> str:
    """Derive a specific reason why effect size computation failed for these rows."""
    if not rows:
        return "insufficient statistics to compute effect size"

    all_excluded = all(
        str(r.get("Include/Exclude", "")).strip().lower() == "exclude"
        for r in rows
    )
    if all_excluded:
        comments = [str(r.get("Comment", "")).strip() for r in rows if r.get("Comment")]
        if comments:
            unique = list(dict.fromkeys(c for c in comments if c))
            return "excluded by converter: " + "; ".join(unique[:2])
        return "excluded by effect size converter (insufficient data)"

    missing_parts: List[str] = []

    no_effect = all(
        r.get("hedges_g") in (None, "") and r.get("cohens_d") in (None, "")
        for r in rows
    )
    if no_effect:
        missing_parts.append("no effect size value extractable")

    no_n = all(
        r.get("n_treatment") in (None, "")
        and r.get("n_control") in (None, "")
        and r.get("n_total") in (None, "")
        for r in rows
    )
    if no_n:
        missing_parts.append("missing sample sizes (n_treatment / n_control)")

    if not missing_parts:
        # Effect size or sample size present but variance could not be computed
        missing_parts.append("variance could not be computed from available statistics")

    return "; ".join(missing_parts)


# ── Paper fate determination ───────────────────────────────────────────────────

def _fate(
    paper_id: str,
    mode: str,
    screening_decisions: Dict,
    eligibility_decisions: Dict,
    papers_eligible_ids: set,
    study_map_ids: set,
    result_ids: set,
    effect_ids: set,
    *,
    study_maps: Optional[Dict] = None,
    papers_no_fulltext: Optional[set] = None,
    papers_no_fulltext_reasons: Optional[Dict[str, str]] = None,
    meta_ready_by_study: Optional[Dict] = None,
    document_type_exclusions: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Return dict with screening_status, exclusion_stage, exclusion_reason,
    final_status.  Produces specific reasons at every loss point.
    """
    scr  = screening_decisions.get(paper_id, {})
    elig = eligibility_decisions.get(paper_id, {})
    no_fulltext = paper_id in (papers_no_fulltext or set())
    fulltext_reason = (papers_no_fulltext_reasons or {}).get(
        paper_id,
        "no full text available from any retrieval strategy",
    )

    # ── Excluded at title/abstract screening ──────────────────────────────────
    if scr.get("decision") == "exclude":
        reason = scr.get("reason", "excluded at title/abstract screening") or "excluded at title/abstract screening"
        return {
            "screening_status": "screened_out",
            "exclusion_stage":  "screening",
            "exclusion_reason": reason,
            "final_status":     "excluded",
        }

    # ── Excluded at full-text eligibility ─────────────────────────────────────
    if elig.get("decision") == "exclude":
        reason = elig.get("reason", "") or (
            elig.get("exclusion_criterion", "").replace("_", " ")
        ) or "excluded at eligibility assessment"
        return {
            "screening_status": "screened_in",
            "exclusion_stage":  "eligibility",
            "exclusion_reason": reason,
            "final_status":     "excluded",
        }

    # ── Passed both LLM filters (or they weren't applied) ────────────────────
    screening_status = "screened_in" if mode == "search" else "not_applicable"

    # ── Dropped at full-text fetch (no full text found from any strategy) ─────
    if no_fulltext and paper_id not in papers_eligible_ids:
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "full_text_fetch",
            "exclusion_reason": fulltext_reason,
            "final_status":     "excluded",
        }

    # ── Excluded by the manual-mode document-type gate (see
    # agents/document_type_agent.py) -- a review PDF, protocol, or
    # near-duplicate that never got a screening/eligibility decision (those
    # LLM filters don't run in manual mode) but still needs a real reason
    # here instead of falling into the generic "unknown" branch below. ───────
    if paper_id in (document_type_exclusions or {}):
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "document_type_gate",
            "exclusion_reason": (document_type_exclusions or {})[paper_id],
            "final_status":     "excluded",
        }

    # ── Paper not in eligible list (reason unknown) ────────────────────────────
    if paper_id not in papers_eligible_ids:
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "unknown",
            "exclusion_reason": "paper dropped from eligible list (reason unknown)",
            "final_status":     "excluded",
        }

    # ── Study detection failure ───────────────────────────────────────────────
    study_info = (study_maps or {}).get(paper_id)
    if paper_id not in study_map_ids:
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "study_detection",
            "exclusion_reason": "not processed by study detector",
            "final_status":     "excluded",
        }
    if study_info is not None and study_info.get("total_studies", 1) == 0:
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "study_detection",
            "exclusion_reason": "study detection failed due to processing error",
            "final_status":     "excluded",
        }

    # ── Extraction failure ────────────────────────────────────────────────────
    if paper_id not in result_ids:
        # Check whether the study had only a default placeholder
        default_study = (
            study_info is not None
            and any(
                s.get("evidence_quote", "") == "(default — detection failed)"
                for s in study_info.get("studies", [])
            )
        )
        if default_study:
            reason = "no studies detectable in text; no quantitative data extracted"
        else:
            reason = "no quantitative outcomes extractable from full text"
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "extraction",
            "exclusion_reason": reason,
            "final_status":     "excluded",
        }

    # ── Effect size computation failure ───────────────────────────────────────
    if paper_id not in effect_ids:
        rows = (meta_ready_by_study or {}).get(paper_id, [])
        reason = _effect_size_reason(rows)
        return {
            "screening_status": screening_status,
            "exclusion_stage":  "effect_size_computation",
            "exclusion_reason": reason,
            "final_status":     "excluded",
        }

    # ── Included ──────────────────────────────────────────────────────────────
    return {
        "screening_status": screening_status,
        "exclusion_stage":  "-",
        "exclusion_reason": "-",
        "final_status":     "included",
    }


# ── Final results CSV ───────────────────────────────────────────────────────────

def _num(value, decimals: int = 4) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def write_final_results_csv(state: GraphState) -> str:
    """Write final_results_summary.csv — the pipeline's headline statistics, downloadable via the UI."""
    output_dir = state["output_dir"]
    plan = state.get("plan")
    meta_result = state.get("meta_result")
    bias_result = state.get("bias_result")
    effect_sizes = state.get("effect_sizes", []) or []

    rows: List[List] = [
        ["Research Question", plan.research_question if plan else "N/A"],
        ["Treatment", plan.treatment_label if plan else "N/A"],
        ["Control", plan.control_label if plan else "N/A"],
        ["Studies (k)", meta_result.k if meta_result else len(effect_sizes)],
        ["Total N", meta_result.n_total if meta_result else "N/A"],
        ["Pooled Hedges' g", _num(meta_result.pooled_g) if meta_result else "N/A"],
        # Pooled Hedges' g above ALWAYS uses the raw (treatment - control)/SD sign, matching
        # Cochrane/RevMan's own convention -- this row is the separate, explicit answer to
        # "which side does the number favor", derived from plan.higher_score_is_worse rather
        # than from the sign itself (see EffectSizeRecord.favors_treatment's docstring).
        ["Favors", (
            (plan.treatment_label if plan else "Treatment") if meta_result and meta_result.favors_treatment is True
            else (plan.control_label if plan else "Control") if meta_result and meta_result.favors_treatment is False
            else "Neither (tie or undetermined)" if meta_result
            else "N/A"
        )],
        ["Pooled SE", _num(meta_result.pooled_se) if meta_result else "N/A"],
        ["95% CI Lower", _num(meta_result.ci_lower) if meta_result else "N/A"],
        ["95% CI Upper", _num(meta_result.ci_upper) if meta_result else "N/A"],
        ["Z-value", _num(meta_result.z_value) if meta_result else "N/A"],
        ["P-value", _num(meta_result.p_value, 5) if meta_result else "N/A"],
        ["I² (%)", _num(meta_result.i_squared, 1) if meta_result else "N/A"],
        ["Tau²", _num(meta_result.tau_squared, 5) if meta_result else "N/A"],
        ["Tau", _num(meta_result.tau) if meta_result else "N/A"],
        ["H²", _num(meta_result.h_squared) if meta_result else "N/A"],
        ["Q-statistic", _num(meta_result.q_statistic) if meta_result else "N/A"],
        ["Q df", meta_result.q_df if meta_result else "N/A"],
        ["Q p-value", _num(meta_result.q_p_value, 5) if meta_result else "N/A"],
        ["Model", meta_result.method if meta_result else "N/A"],
        ["Publication Bias Risk", bias_result.bias_risk if bias_result else "N/A"],
        ["Egger's Intercept", _num(bias_result.eggers_intercept) if bias_result else "N/A"],
        ["Egger's SE", _num(bias_result.eggers_se) if bias_result else "N/A"],
        ["Egger's t", _num(bias_result.eggers_t_value) if bias_result else "N/A"],
        ["Egger's p", _num(bias_result.eggers_p_value, 5) if bias_result else "N/A"],
        ["Trim-and-Fill k₀", bias_result.trim_fill_k0 if bias_result else "N/A"],
        ["Trim-and-Fill Side", bias_result.trim_fill_side if bias_result else "N/A"],
        ["Trim-and-Fill Adjusted g", _num(bias_result.trim_fill_g) if bias_result else "N/A"],
        ["Trim-and-Fill CI Lower", _num(bias_result.trim_fill_ci_lower) if bias_result else "N/A"],
        ["Trim-and-Fill CI Upper", _num(bias_result.trim_fill_ci_upper) if bias_result else "N/A"],
    ]

    path = os.path.join(output_dir, "final_results_summary.csv")
    _write(path, ["Metric", "Value"], rows)
    logger.info("[Audit] final_results_summary.csv written.")
    return path


def write_final_results_by_group_csv(state: GraphState) -> str:
    """Write final_results_summary_by_outcome_group.csv — one row per
    outcome_group_key, so each meta-analysis group (construct/timepoint
    combination) that meta_analysis_node pooled separately is represented on
    its own instead of only the single "primary" group that
    final_results_summary.csv (backward-compat alias) shows."""
    output_dir = state["output_dir"]
    groups = state.get("meta_results", []) or []

    header = [
        "outcome_group_key", "outcome_family", "follow_up_timepoint", "label",
        "k", "n_total", "insufficient_data", "single_effect_g",
        "pooled_g", "ci_lower", "ci_upper", "p_value", "i_squared", "tau_squared", "q_p_value",
    ]
    rows: List[List] = []
    for g in groups:
        r = g.result
        rows.append([
            g.outcome_group_key, g.outcome_family or "", g.follow_up_timepoint or "", g.label,
            g.k, g.n_total, g.insufficient_data, _num(g.single_effect_g) if g.single_effect_g is not None else "",
            _num(r.pooled_g) if r else "N/A",
            _num(r.ci_lower) if r else "N/A",
            _num(r.ci_upper) if r else "N/A",
            _num(r.p_value, 5) if r else "N/A",
            _num(r.i_squared, 1) if r else "N/A",
            _num(r.tau_squared, 5) if r else "N/A",
            _num(r.q_p_value, 5) if r else "N/A",
        ])

    path = os.path.join(output_dir, "final_results_summary_by_outcome_group.csv")
    _write(path, header, rows)
    logger.info(f"[Audit] final_results_summary_by_outcome_group.csv written ({len(rows)} group(s)).")
    return path


# ── Node ──────────────────────────────────────────────────────────────────────

def pipeline_audit_node(state: GraphState) -> dict:
    """Final stage: write meta_analysis_summary.csv, study_screening.csv, and final_results_summary.csv."""
    logger.info("=== STAGE 11: Pipeline Audit CSV ===")

    output_dir            = state["output_dir"]
    mode                  = state.get("mode", "search")
    papers_eligible       = state.get("papers_eligible", [])
    all_retrieved         = state.get("all_retrieved_papers", [])
    screening_decisions   = state.get("screening_decisions", {})
    eligibility_decisions = state.get("eligibility_decisions", {})
    study_maps            = state.get("study_maps", {})
    paper_results         = state.get("paper_results", [])
    effect_sizes          = state.get("effect_sizes", [])
    search_rejected       = state.get("search_rejected_papers", [])
    no_fulltext_ids       = set(state.get("papers_no_fulltext", []))
    no_fulltext_reasons   = state.get("papers_no_fulltext_reasons", {})
    document_type_excluded = state.get("document_type_excluded", [])
    document_type_exclusion_reasons = {
        d.get("paper_id", ""): f"classified as {d.get('document_type', '?')} -- {d.get('rationale', '')}"
        for d in document_type_excluded if d.get("paper_id")
    }
    user_prompt           = state.get("user_prompt", "")

    # ── Build lookup sets ──────────────────────────────────────────────────────
    papers_eligible_ids = {p.id for p in papers_eligible}
    study_map_ids = set(study_maps.keys())
    if not study_map_ids:
        study_maps_path = os.path.join(output_dir, "study_maps.json")
        if os.path.exists(study_maps_path):
            try:
                with open(study_maps_path, encoding="utf-8") as _f:
                    loaded = _json.load(_f)
                    study_maps    = loaded
                    study_map_ids = set(loaded.keys())
            except Exception:
                pass

    result_ids = {r.get("paper_id", "") for r in paper_results if r.get("paper_id")}
    if not result_ids:
        paper_results_path = os.path.join(output_dir, "paper_results.json")
        if os.path.exists(paper_results_path):
            try:
                with open(paper_results_path, encoding="utf-8") as _f:
                    for row in _json.load(_f):
                        pid = row.get("paper_id", "")
                        if pid:
                            result_ids.add(pid)
            except Exception:
                pass

    # ── Effect-size IDs (read meta_ready_results.json directly) ───────────────
    # EffectSizeRecord.study_id is unreliable (falls back to "study_N") because
    # meta_ready_results.json uses Study_ID not paper_id.  Read the JSON file
    # directly and also build the per-paper rows dict for failure-reason lookup.
    effect_ids: set = set()
    meta_ready_by_study: Dict[str, List[Dict]] = {}
    meta_ready_path = os.path.join(output_dir, "meta_ready_results.json")
    if os.path.exists(meta_ready_path):
        try:
            with open(meta_ready_path, encoding="utf-8") as _f:
                for row in _json.load(_f):
                    pid = row.get("paper_id") or row.get("Study_ID") or ""
                    if pid:
                        meta_ready_by_study.setdefault(pid, []).append(row)
                        inc = str(row.get("Include/Exclude", "")).strip().lower()
                        has_g = row.get("hedges_g") not in (None, "")
                        has_d = row.get("cohens_d") not in (None, "")
                        if inc == "include" and (has_g or has_d):
                            effect_ids.add(pid)
        except Exception as exc:
            logger.warning(f"[Audit] Cannot read meta_ready_results.json: {exc}")
    # Fallback to EffectSizeRecord objects (study_id may be "study_N")
    if not effect_ids:
        for e in effect_sizes:
            sid = getattr(e, "study_id", "") or ""
            if sid:
                effect_ids.add(sid)

    # ── Canonical "all papers" list for this run ───────────────────────────────
    if mode == "search" and all_retrieved:
        all_papers = all_retrieved
    else:
        all_papers = papers_eligible   # pdf/manual: no screening, eligible == all

    n_retrieved     = len(all_papers) + len(search_rejected)
    n_scr_excluded  = state.get("n_screened_excluded", -1)
    n_elig_excluded = state.get("n_eligibility_excluded", -1)
    n_eligible      = len(papers_eligible)
    n_included      = len([p for p in papers_eligible if p.id in effect_ids])

    # ── GT comparison ──────────────────────────────────────────────────────────
    gt_entries = _load_gt(output_dir)
    gt_loaded  = len(gt_entries) > 0

    gt_results: Dict[str, Tuple[str, str]] = {}
    if gt_loaded:
        for p in all_papers:
            doi = getattr(p, "doi", "") or ""
            gt_results[p.id] = _match(_norm(p.title), doi, gt_entries)

    n_direct  = sum(1 for v in gt_results.values() if v[0] == "direct")
    n_near    = sum(1 for v in gt_results.values() if v[0] == "near_match")
    n_overlap = n_direct + n_near

    # ── meta_analysis_summary.csv ──────────────────────────────────────────────
    summary_header = [
        "user_prompt",
        "retrieved_count",
        "screened_in_count",
        "screened_out_count",
        "eligible_count",
        "included_count",
        "overlap_with_original_count",
        "overlap_with_original_pct",
    ]

    if mode == "search":
        # Count search_rejected as screened_out if no explicit LLM screening
        if n_scr_excluded >= 0:
            screened_out = n_scr_excluded
            screened_in  = n_retrieved - n_scr_excluded
        else:
            screened_out = len(search_rejected)
            screened_in  = len(all_papers)
    else:
        screened_out = "N/A (not applicable)"
        screened_in  = "N/A (not applicable)"

    summary_row = [
        user_prompt,
        n_retrieved,
        screened_in,
        screened_out,
        n_eligible,
        n_included,
        n_overlap if gt_loaded else "N/A (no gt_papers.csv provided)",
        _pct(n_overlap, len(gt_entries)) if gt_loaded else "N/A",
    ]

    _write(
        os.path.join(output_dir, "meta_analysis_summary.csv"),
        summary_header,
        [summary_row],
    )
    logger.info("[Audit] meta_analysis_summary.csv written.")

    # ── study_screening.csv ────────────────────────────────────────────────────
    screening_header = [
        "title",
        "year",
        "retrieval_status",
        "screening_status",
        "exclusion_stage",
        "exclusion_reason",
        "final_status",
        "match_type",
        "matched_gt_title",
    ]

    screening_rows = []

    # Papers that passed the relevance filter (all modes)
    for p in all_papers:
        fate = _fate(
            p.id, mode,
            screening_decisions, eligibility_decisions,
            papers_eligible_ids, study_map_ids, result_ids, effect_ids,
            study_maps=study_maps,
            papers_no_fulltext=no_fulltext_ids,
            papers_no_fulltext_reasons=no_fulltext_reasons,
            meta_ready_by_study=meta_ready_by_study,
            document_type_exclusions=document_type_exclusion_reasons,
        )
        if gt_loaded:
            mtype, gtitle = gt_results.get(p.id, ("no_match", ""))
        else:
            mtype, gtitle = "N/A", "N/A"

        screening_rows.append([
            p.title,
            p.year or "",
            "retrieved",
            fate["screening_status"],
            fate["exclusion_stage"],
            fate["exclusion_reason"],
            fate["final_status"],
            mtype,
            gtitle,
        ])

    # Papers found by DB search but rejected by the initial relevance filter
    written_screening_ids = {getattr(p, "id", "") for p in all_papers}
    for rej in search_rejected:
        rej_id = rej.get("id", "")
        if rej_id and rej_id in written_screening_ids:
            continue
        title = rej.get("title", "")
        if gt_loaded:
            mtype, gtitle = _match(_norm(title), "", gt_entries)
        else:
            mtype, gtitle = "N/A", "N/A"
        screening_rows.append([
            title,
            rej.get("year", ""),
            "found_but_rejected",
            "screened_out",
            "search_relevance_filter",
            "off-topic: rejected by initial relevance check",
            "excluded",
            mtype,
            gtitle,
        ])

    # GT papers never retrieved at all
    if gt_loaded:
        retrieved_norms = {_norm(p.title) for p in all_papers}
        retrieved_norms |= {_norm(r.get("title", "")) for r in search_rejected}
        retrieved_dois  = {getattr(p, "doi", "") or "" for p in all_papers}
        for e in gt_entries:
            if e["_norm"] not in retrieved_norms and e.get("doi", "") not in retrieved_dois:
                screening_rows.append([
                    e["title"],
                    "",
                    "not_retrieved",
                    "N/A",
                    "retrieval",
                    "not found by database search",
                    "excluded",
                    "N/A",
                    "",
                ])

    _write(
        os.path.join(output_dir, "study_screening.csv"),
        screening_header,
        screening_rows,
    )
    logger.info(f"[Audit] study_screening.csv written ({len(screening_rows)} rows).")

    # ── paper_tracking.csv ────────────────────────────────────────────────────
    tracking_rows = []

    for p in all_papers:
        fate = _fate(
            p.id, mode,
            screening_decisions, eligibility_decisions,
            papers_eligible_ids, study_map_ids, result_ids, effect_ids,
            study_maps=study_maps,
            papers_no_fulltext=no_fulltext_ids,
            papers_no_fulltext_reasons=no_fulltext_reasons,
            meta_ready_by_study=meta_ready_by_study,
            document_type_exclusions=document_type_exclusion_reasons,
        )
        scr_fate   = fate["screening_status"]   # screened_in | screened_out | not_applicable
        excl_stage = fate["exclusion_stage"]

        screening_status = {
            "screened_in":    "Screened In",
            "screened_out":   "Screened Out",
            "not_applicable": "N/A",
        }.get(scr_fate, "N/A")

        elig_dec = eligibility_decisions.get(p.id, {})
        if excl_stage == "eligibility":
            eligibility_status = "Not Eligible"
        elif scr_fate == "screened_out" or excl_stage == "screening":
            eligibility_status = "N/A"
        elif elig_dec.get("decision") == "include":
            eligibility_status = "Eligible"
        elif elig_dec.get("decision") == "exclude":
            eligibility_status = "Not Eligible"
        else:
            eligibility_status = "N/A"

        final_status = "Included" if fate["final_status"] == "included" else "Not Included"
        loss_stage   = _STAGE_DISPLAY.get(excl_stage, excl_stage) if fate["final_status"] != "included" else "-"
        loss_reason  = fate["exclusion_reason"] if fate["final_status"] != "included" else "-"

        tracking_rows.append([
            p.title,
            p.year or "",
            getattr(p, "source", ""),
            getattr(p, "doi", "") or "",
            getattr(p, "url", "") or "",
            "Retrieved",
            screening_status,
            eligibility_status,
            final_status,
            loss_stage,
            loss_reason,
        ])

    written_tracking_ids = {getattr(p, "id", "") for p in all_papers}
    for rej in search_rejected:
        rej_id = rej.get("id", "")
        if rej_id and rej_id in written_tracking_ids:
            continue
        tracking_rows.append([
            rej.get("title", ""),
            rej.get("year", ""),
            rej.get("source", ""),
            rej.get("doi", ""),
            rej.get("url", ""),
            "Retrieved",
            "Screened Out",
            "N/A",
            "Not Included",
            "Search Relevance Filter",
            "off-topic: rejected by initial relevance check",
        ])

    # Manual-mode-only: papers agents/document_type_agent.py dropped before
    # study_detection_node -- by this point they're no longer in
    # papers_eligible (manual mode's own "all_papers" above), so without
    # this they'd vanish from the audit trail instead of showing up as an
    # explained exclusion (see models.ValidationFlag's parallel record in
    # validation_report.csv for the same information in that format).
    for doc in document_type_excluded:
        doc_id = doc.get("paper_id", "")
        if doc_id and doc_id in written_tracking_ids:
            continue
        tracking_rows.append([
            doc.get("title", ""),
            "",
            "manual",
            "",
            "",
            "Retrieved",
            "N/A",
            "N/A",
            "Not Included",
            _STAGE_DISPLAY.get("document_type_gate", "Document Type Gate"),
            f"classified as {doc.get('document_type', '?')} -- {doc.get('rationale', '')}",
        ])

    _write(
        os.path.join(output_dir, "paper_tracking.csv"),
        _TRACKING_HEADER,
        tracking_rows,
    )
    logger.info(f"[Audit] paper_tracking.csv written ({len(tracking_rows)} rows).")

    write_final_results_csv(state)
    write_final_results_by_group_csv(state)
    write_validation_report(state)

    return {
        "audit_csv_path": os.path.join(output_dir, "meta_analysis_summary.csv"),
    }


def write_validation_report(state: GraphState) -> str:
    """validation_report.csv/.json -- the outcome/effect-size-level counterpart
    to paper_tracking.csv's paper-level loss_stage/loss_reason tracking (see
    module docstring above). Aggregates every models.ValidationFlag appended
    anywhere in the pipeline (agents/cross_paper_outcome_mapper_agent.py's
    classification misses, agents/document_type_agent.py's exclusions,
    agents/meta_analysis_agent.py's measure-splits and trial-dedup exclusions,
    etc.) into one auditable file -- never a substitute for fixing the
    underlying issue, just a permanent record of what happened and why."""
    output_dir = state["output_dir"]
    flags = state.get("validation_flags", [])
    rows = [
        [f.stage, f.severity, f.subject_id, f.message, f.auto_action or ""]
        for f in flags
    ]
    csv_path = os.path.join(output_dir, "validation_report.csv")
    _write(csv_path, ["stage", "severity", "subject_id", "message", "auto_action"], rows)

    json_path = os.path.join(output_dir, "validation_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        _json.dump(
            [f.model_dump() if hasattr(f, "model_dump") else f for f in flags],
            f, indent=2,
        )

    by_stage: Dict[str, int] = {}
    for f in flags:
        by_stage[f.stage] = by_stage.get(f.stage, 0) + 1
    if flags:
        logger.info(f"[Audit] validation_report.csv written ({len(flags)} flag(s): {by_stage}).")
    else:
        logger.info("[Audit] validation_report.csv written (0 flags — nothing to report).")
    return csv_path
