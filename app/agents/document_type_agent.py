"""Document Type agent -- manual-mode-only gate between manual_ingest_node and
study_detection_node (see pipeline_graph.py's manual-mode edges).

Root-cause context: manual-upload mode deliberately skips eligibility_node
(the only place with a "not an original empirical study -- systematic review,
meta-analysis, protocol..." exclusion check), by design -- manual mode trusts
the user's own topical curation of which PAPERS to analyze. But it never
distinguishes DOCUMENT TYPE at all: if a Cochrane review PDF (or a split/
duplicate fragment of one) is accidentally included among the uploaded
"primary study" files, it flows straight through to extraction and gets
treated as if it were itself a trial. This node closes exactly that gap --
and ONLY that gap; it does not re-apply eligibility's other criteria
(population, data availability, etc.), which manual mode still intentionally
skips.

Generic by construction: classification is driven by DOCUMENT STRUCTURE
(section headings, reference density, how many independent "Methods"/
"Participants" subsections one document contains) and a closed-vocabulary
LLM judgment -- never by filename, review ID, or any topic-specific keyword.
"""

import logging
import os
import re
from difflib import SequenceMatcher
from typing import Dict, List, Literal, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from models import PaperRecord, ValidationFlag
from pipeline_graph import _extract_tool_args, GraphState
from utils.trial_matching import assign_trial_clusters
from core_utils import save_json

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You classify a single uploaded document by what KIND of document it is, for a "
    "meta-analysis pipeline that expects primary-study reports as input. You are not "
    "judging quality, relevance, or eligibility -- only document type."
)

DocumentType = Literal[
    "primary_study",
    "systematic_review_or_meta_analysis",
    "protocol_or_registration",
    "guideline_or_consensus_statement",
    "narrative_review_or_commentary",
    "unclear",
]


@tool
def record_document_type(
    paper_id: str,
    document_type: DocumentType,
    rationale: str,
    evidence_quote: str,
) -> str:
    """Classify what kind of document this is.
    primary_study: reports the results of ONE study's own newly collected/analyzed data
      (a randomized trial, cohort study, case-control study, etc.) -- this is what the
      pipeline needs as input.
    systematic_review_or_meta_analysis: synthesizes/pools results ACROSS multiple other
      studies (has its own "included studies" list, forest plots, pooled effect estimates).
    protocol_or_registration: describes a planned study that has not yet reported results
      (a trial-registry record or a published study protocol).
    guideline_or_consensus_statement: a clinical practice guideline or expert consensus
      document, not a primary study.
    narrative_review_or_commentary: a non-systematic review, editorial, or opinion piece.
    unclear: genuinely cannot tell from the available text -- do not guess."""
    return "document_type_recorded"


# ── Structural pre-signals (regex-based, generic to the review/primary-study
# document GENRE -- no disease/study-name-specific patterns) ────────────────

_REVIEW_MARKERS = [
    r"\bsearch strategy\b",
    r"\bPRISMA\b",
    r"\bcharacteristics of included studies\b",
    r"\bcharacteristics of excluded studies\b",
    r"\brisk of bias\b.{0,40}\bincluded studies\b",
    r"\bdata and analyses\b",
    r"\bforest plot\b",
    r"\bsummary of findings\b",
    r"\bcochrane (systematic )?review\b",
]
_METHODS_SUBSECTION_RE = re.compile(r"\b(methods?|participants)\b\s*[:\n]", re.IGNORECASE)
_REFERENCE_LINE_RE = re.compile(r"^\s*\d{1,3}[.\)]\s+\S", re.MULTILINE)


def _structural_signals(text: str) -> Dict[str, float]:
    """Cheap, generic structural features -- fed to the LLM as CONTEXT, not
    used as a hard rule on their own (a primary study can legitimately
    mention "risk of bias" once; a review mentions review-genre markers
    repeatedly and combines them with many independent Methods sections and
    an unusually large reference list relative to body length)."""
    if not text:
        return {"review_marker_hits": 0, "methods_subsections": 0, "reference_density": 0.0, "length": 0}
    review_marker_hits = sum(1 for pat in _REVIEW_MARKERS if re.search(pat, text, re.IGNORECASE))
    methods_subsections = len(_METHODS_SUBSECTION_RE.findall(text))
    reference_lines = len(_REFERENCE_LINE_RE.findall(text))
    words = max(len(text.split()), 1)
    return {
        "review_marker_hits": review_marker_hits,
        "methods_subsections": methods_subsections,
        "reference_density": round(reference_lines / words * 1000, 3),  # refs per 1000 words
        "length": len(text),
    }


_MAX_CHARS = 40_000
_DUP_PREFIX_CHARS = 6_000       # cap for near-duplicate comparison -- full-text diffing
_DUP_QUICK_THRESHOLD = 0.85     # SequenceMatcher.quick_ratio() is a fast upper bound;
_DUP_REAL_THRESHOLD = 0.90      # only compute the slower exact ratio() when it clears this


def _normalize_for_dedup(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()[:_DUP_PREFIX_CHARS]


def _find_near_duplicates(papers: List[PaperRecord]) -> Dict[str, str]:
    """Pairwise full-TEXT content similarity (never filenames) within one
    upload batch. Returns {dropped_paper_id: kept_paper_id} for every
    detected near-duplicate/split-fragment pair -- the SHORTER of the two
    (the more likely fragment) is dropped."""
    normed = [(p.id, _normalize_for_dedup(p.full_text)) for p in papers if p.full_text]
    dropped: Dict[str, str] = {}
    for i in range(len(normed)):
        id_a, text_a = normed[i]
        if id_a in dropped or not text_a:
            continue
        for j in range(i + 1, len(normed)):
            id_b, text_b = normed[j]
            if id_b in dropped or not text_b:
                continue
            sm = SequenceMatcher(None, text_a, text_b, autojunk=True)
            if sm.quick_ratio() < _DUP_QUICK_THRESHOLD:
                continue
            if sm.ratio() >= _DUP_REAL_THRESHOLD:
                shorter, longer = (id_a, id_b) if len(text_a) <= len(text_b) else (id_b, id_a)
                dropped[shorter] = longer
    return dropped


def document_type_node(state: GraphState) -> dict:
    """Manual-mode-only: classify each uploaded document and drop anything
    that isn't a primary study (a review, protocol, guideline, or a near-
    duplicate/split fragment of another uploaded document), before it ever
    reaches study_detection_node/extraction_node."""
    logger.info("=== STAGE 1B: Document Type Gate (manual mode) ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    validation_flags: List[ValidationFlag] = list(state.get("validation_flags", []))

    if not papers:
        return {"papers_eligible": papers}

    agent = create_react_agent(llm, [record_document_type], prompt=SYSTEM_PROMPT)
    kept: List[PaperRecord] = []
    excluded: List[dict] = []

    for paper in papers:
        text = (paper.full_text or "")[:_MAX_CHARS]
        signals = _structural_signals(paper.full_text or "")
        user_msg = (
            f"Paper ID: {paper.id}\nTitle: {paper.title}\n\n"
            f"Structural signals (context only -- use your own judgment of the actual text, "
            f"these are hints, not a verdict): {signals}\n\n"
            f"Document text (may be truncated):\n{text}\n\n"
            "Call record_document_type once for this document."
        )
        try:
            result = agent.invoke({"messages": [("user", user_msg)]})
            args = _extract_tool_args(result["messages"], "record_document_type")
        except Exception as exc:
            logger.error(f"[DocumentType] {paper.id}: classification failed — {exc}")
            args = {}

        doc_type = args.get("document_type") or "unclear"
        paper.document_type = doc_type

        if doc_type == "primary_study" or doc_type == "unclear":
            if doc_type == "unclear":
                # Ambiguous, never silently dropped -- kept (manual mode's
                # existing default is to trust the user's curation), but
                # flagged so it's visible in the audit trail.
                validation_flags.append(ValidationFlag(
                    stage="document_type_gate", severity="warning", subject_id=paper.id,
                    message=f"Could not confidently classify document type for '{paper.title}'; "
                            "kept as input (manual mode trusts user curation by default).",
                    auto_action="none",
                ))
            kept.append(paper)
        else:
            rationale = args.get("rationale") or "(no rationale returned)"
            logger.warning(f"[DocumentType] {paper.id}: excluded as {doc_type} — {rationale}")
            excluded.append({"paper_id": paper.id, "title": paper.title, "document_type": doc_type, "rationale": rationale})
            validation_flags.append(ValidationFlag(
                stage="document_type_gate", severity="warning", subject_id=paper.id,
                message=f"Excluded from primary-study set: classified as {doc_type} -- {rationale}",
                auto_action="excluded_paper",
            ))

    # ── Near-duplicate / split-file detection among the SURVIVING papers ───
    dup_map = _find_near_duplicates(kept)
    if dup_map:
        kept = [p for p in kept if p.id not in dup_map]
        by_id = {p.id: p for p in state.get("papers_eligible", [])}
        for dropped_id, kept_id in dup_map.items():
            dropped_title = by_id[dropped_id].title if dropped_id in by_id else dropped_id
            kept_title = by_id[kept_id].title if kept_id in by_id else kept_id
            logger.warning(f"[DocumentType] {dropped_id} ('{dropped_title}') dropped — near-duplicate of {kept_id} ('{kept_title}')")
            excluded.append({"paper_id": dropped_id, "title": dropped_title, "document_type": "duplicate", "rationale": f"near-duplicate of {kept_id}"})
            validation_flags.append(ValidationFlag(
                stage="document_type_gate", severity="warning", subject_id=dropped_id,
                message=f"Excluded as a near-duplicate/split fragment of '{kept_title}' ({kept_id}), "
                        "detected via full-text content similarity.",
                auto_action="excluded_paper",
            ))

    # ── Trial clustering (study/trial vs. publication -- see
    # utils/trial_matching.py) -- run on the SURVIVING primary-study papers.
    # Only sets trial_cluster_id where a companion publication was actually
    # detected (registry ID or DOI match); everything else is unaffected.
    # Actual double-counting exclusion happens later, at pooling time (see
    # agents/meta_analysis_agent.py), not here -- a companion publication
    # may still contribute a DIFFERENT, non-overlapping outcome.
    assign_trial_clusters(kept)
    clustered = {p.trial_cluster_id for p in kept if p.trial_cluster_id}
    if clustered:
        logger.info(f"[DocumentType] {len(clustered)} trial cluster(s) detected among {len(kept)} kept paper(s).")
        for cid in clustered:
            members = [p.id for p in kept if p.trial_cluster_id == cid]
            validation_flags.append(ValidationFlag(
                stage="trial_dedup", severity="info", subject_id=cid,
                message=f"Papers {members} appear to report the same underlying trial "
                        f"(cluster {cid}); duplicate outcomes will be excluded from pooling, not the papers themselves.",
                auto_action="none",
            ))

    output_dir = state.get("output_dir")
    if output_dir:
        save_json(
            {"kept": [p.id for p in kept], "excluded": excluded,
             "trial_clusters": {p.id: p.trial_cluster_id for p in kept if p.trial_cluster_id}},
            os.path.join(output_dir, "document_type_gate.json"),
        )

    logger.info(f"[DocumentType] {len(kept)}/{len(papers)} document(s) kept as primary studies.")
    # document_type_excluded: separate from papers_eligible/validation_flags
    # so agents/pipeline_audit_agent.py can surface these as real rows in
    # paper_tracking.csv -- manual mode's "all_papers" there is papers_eligible
    # itself (no separate all_retrieved_papers list the way search mode has),
    # so a paper dropped here would otherwise vanish from the audit trail
    # entirely instead of showing up as an explained exclusion.
    return {"papers_eligible": kept, "validation_flags": validation_flags, "document_type_excluded": excluded}
