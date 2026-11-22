"""Search agent - Stage 1 (Deep Research paper discovery mode).

Uses OpenRouter o4-mini Deep Research first to find candidate papers, then runs
a cheap deterministic title/abstract screen before downstream full-text fetch.
Academic databases are used later by the paper-reading stage to retrieve paper
content and metadata for the discovered records.
"""

from __future__ import annotations

import logging
import json
import os
import re
import uuid
from typing import Dict, List, Optional, TYPE_CHECKING, Tuple

from config import (
    ENABLED_SEARCH_DATABASES,
    MANUAL_IMPORT_PATHS,
    MAX_PAPERS_PER_QUERY,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    SEARCH_QUERY_VARIANTS,
    SEARCH_QUERY_VARIANT_MODEL,
    USE_LLM_SEARCH_QUERY_VARIANTS,
)
from langchain_openai import ChatOpenAI
from core_utils import save_json
from database_search import search_top_per_db
from models import MetaAnalysisPlan, PaperRecord
from utils.manual_import import load_manual_import

if TYPE_CHECKING:
    from pipeline_graph import GraphState

logger = logging.getLogger(__name__)

query_variant_llm = ChatOpenAI(
    model=SEARCH_QUERY_VARIANT_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    timeout=120,
    max_retries=2,
)

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "between", "by", "can",
    "control", "controlled", "does", "effect", "effects", "for", "from",
    "has", "have", "how", "in", "intervention", "is", "it", "of", "on",
    "or", "outcome", "outcomes", "paper", "participants", "study",
    "studies", "than", "that", "the", "their", "this", "to", "treatment",
    "using", "versus", "vs", "what", "when", "with",
}

_QUERY_INTENT_TERMS = (
    "experiment", "experimental", "trial", "randomized", "randomised",
    "controlled", "comparison", "quantitative", "outcome", "effect",
)

_STATISTICAL_SIGNAL_PATTERNS = [
    r"\bp\s*[<=>]\s*0?\.\d+",
    r"\b[tfzr]\s*\(\s*\d+",
    r"\b[tfzr]\s*[=<>]\s*-?\d+(?:\.\d+)?",
    r"\b(?:anova|regression|correlation|odds ratio|confidence interval)\b",
    r"\b(?:mean|means|sd|standard deviation|standard error)\b",
    r"\b(?:cohen'?s d|hedges'? g|effect size)\b",
    r"\bn\s*[=]\s*\d+",
    r"\b\d+(?:\.\d+)?\s*%\b",
]

_NON_EMPIRICAL_PATTERNS = [
    r"\bsystematic review\b",
    r"\bmeta-analysis\b",
    r"\bmetaanalysis\b",
    r"\bscoping review\b",
    r"\bnarrative review\b",
    r"\bliterature review\b",
    r"\breview article\b",
    r"\beditorial\b",
    r"\bcommentary\b",
    r"\bopinion\b",
    r"\bperspective\b",
    r"\bprotocol\b",
    r"\btheoretical\b",
]


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _tokens(text: str) -> set:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9-]{2,}", (text or "").lower())
        if token not in _STOPWORDS
    }


def _dedupe_key(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (title or "").lower()).strip()


def _contains_query_intent(query: str) -> bool:
    q = (query or "").lower()
    return any(term in q for term in _QUERY_INTENT_TERMS)


def _dedupe_queries(candidates: List[str], max_variants: int) -> List[str]:
    """Clean and deduplicate query strings while preserving order."""
    seen: set = set()
    out: List[str] = []
    for query in candidates:
        query = _clean_text(query)
        key = query.lower()
        if not query or key in seen:
            continue
        seen.add(key)
        out.append(query)
        if len(out) >= max(1, max_variants):
            break
    return out


def _build_rule_based_intent_queries(plan: MetaAnalysisPlan, max_variants: int) -> List[str]:
    """Return deterministic intent-focused discovery queries for the plan."""
    candidates: List[str] = []

    for query in plan.search_queries or []:
        cleaned = _clean_text(query)
        if cleaned:
            candidates.append(cleaned)
            if not _contains_query_intent(cleaned):
                candidates.append(f"{cleaned} quantitative effect")

    treatment = _clean_text(plan.treatment_label)
    control = _clean_text(plan.control_label)
    outcome = _clean_text(plan.outcome_description)
    rq = _clean_text(plan.research_question)

    generated = [
        f"{treatment} {control} {outcome} quantitative",
        f"{treatment} {outcome} experiment controlled",
        f"{treatment} {outcome} trial comparison",
        f"{rq} quantitative outcome",
    ]
    candidates.extend(q for q in generated if _clean_text(q))

    return _dedupe_queries(candidates, max_variants)


def _extract_json_object(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}


def _build_llm_intent_queries(plan: MetaAnalysisPlan, max_variants: int) -> List[str]:
    """Ask the LLM to interpret the planned topic as database-search queries."""
    prompt = (
        "You are helping run a systematic literature search for a meta-analysis.\n"
        "Rewrite the planned research question into concise academic database search queries.\n"
        f"Return exactly {max(1, max_variants)} query string(s), unless fewer are truly appropriate.\n\n"
        f"Research question: {plan.research_question}\n"
        f"Treatment/intervention: {plan.treatment_label}\n"
        f"Control/comparator: {plan.control_label}\n"
        f"Outcome: {plan.outcome_description}\n"
        f"Existing draft queries: {', '.join(plan.search_queries or [])}\n\n"
        "Guidelines:\n"
        "- Use short keyword phrases, not long sentences.\n"
        "- Include empirical intent words when natural, such as experiment, trial, controlled, comparison, quantitative, outcome, or effect.\n"
        "- Avoid phrases that mainly retrieve reviews, systematic reviews, meta-analyses, editorials, protocols, or opinion pieces.\n"
        "- Do not use Boolean operators unless they are essential.\n\n"
        'Return only JSON in this schema: {"queries": ["query one", "query two"]}'
    )
    try:
        resp = query_variant_llm.invoke(prompt)
    except Exception as exc:
        logger.warning(f"[SearchAgent] LLM query expansion failed; using fallback queries: {exc}")
        return []

    content = getattr(resp, "content", "") or str(resp)
    payload = _extract_json_object(content)
    queries = payload.get("queries") if isinstance(payload, dict) else None
    if not isinstance(queries, list):
        logger.warning("[SearchAgent] LLM query expansion returned no query list; using fallback queries.")
        return []
    deduped = _dedupe_queries([str(q) for q in queries], max_variants)
    logger.info("[SearchAgent] LLM-generated search queries: %s", deduped)
    return deduped


def _build_intent_queries_with_method(plan: MetaAnalysisPlan) -> Tuple[List[str], str]:
    """Same as _build_intent_queries but also reports how the queries were built.

    Returns (queries, method) where method is "llm" or "rule_based".
    """
    max_variants = max(1, SEARCH_QUERY_VARIANTS)
    if USE_LLM_SEARCH_QUERY_VARIANTS:
        llm_queries = _build_llm_intent_queries(plan, max_variants)
        if llm_queries:
            logger.info("[SearchAgent] Using LLM search query variants: %s", llm_queries)
            return llm_queries, "llm"
    fallback_queries = _build_rule_based_intent_queries(plan, max_variants)
    logger.info("[SearchAgent] Using rule-based search query variants: %s", fallback_queries)
    return fallback_queries, "rule_based"


def _build_intent_queries(plan: MetaAnalysisPlan) -> List[str]:
    """Return deduplicated, intent-focused discovery queries for the plan."""
    queries, _method = _build_intent_queries_with_method(plan)
    return queries


def _save_search_queries(
    state: "GraphState", plan: MetaAnalysisPlan, queries: List[str], method: str
) -> None:
    """Persist the user's question and the generated query variants for download via the UI."""
    output_dir = state.get("output_dir", "")
    if not output_dir:
        return
    payload = {
        "user_prompt": state.get("user_prompt", ""),
        "planned_search_queries": list(plan.search_queries or []),
        "query_generation_method": method,
        "intent_queries_used": queries,
    }
    save_json(payload, os.path.join(output_dir, "search_queries.json"))


def _plan_keywords(plan: MetaAnalysisPlan) -> set:
    parts: List[str] = [
        plan.research_question,
        plan.treatment_label,
        plan.control_label,
        plan.outcome_description,
        " ".join(plan.search_queries or []),
    ]
    return _tokens(" ".join(parts))


def _statistical_signal_score(text: str) -> int:
    text = text or ""
    score = 0
    for pattern in _STATISTICAL_SIGNAL_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            score += 1
    return score


def _has_statistical_signal(text: str) -> bool:
    """Cheap deterministic signal for quantitative empirical results."""
    return _statistical_signal_score(text) > 0


def _looks_non_empirical(title: str, abstract: str) -> bool:
    title_l = (title or "").lower()
    text_l = f"{title_l} {(abstract or '').lower()}"
    return any(re.search(pattern, text_l) for pattern in _NON_EMPIRICAL_PATTERNS)


def _topic_overlap_score(paper: dict, plan: MetaAnalysisPlan) -> int:
    paper_terms = _tokens(f"{paper.get('title', '')} {paper.get('abstract', '')}")
    return len(paper_terms & _plan_keywords(plan))


def _prefetch_screen_paper(paper: dict, plan: MetaAnalysisPlan) -> Tuple[bool, str, Dict[str, int | bool]]:
    """Permissive deterministic title/abstract screen before full-text fetch."""
    title = _clean_text(paper.get("title", ""))
    abstract = _clean_text(paper.get("abstract", ""))
    combined = f"{title}. {abstract}"
    stat_score = _statistical_signal_score(combined)
    topic_score = _topic_overlap_score(paper, plan)
    non_empirical = _looks_non_empirical(title, abstract)

    details = {
        "topic_overlap": topic_score,
        "statistical_signal_score": stat_score,
        "non_empirical_signal": non_empirical,
        "abstract_chars": len(abstract),
    }

    if not title:
        return False, "missing title", details

    if not abstract:
        return True, "no abstract; keep for full-text check", details

    if non_empirical and stat_score == 0:
        return False, "non-empirical or review-like record", details

    if topic_score == 0 and stat_score == 0 and len(abstract) >= 250:
        return False, "off topic and no statistical signal", details

    if topic_score == 0:
        return True, "weak topic match; kept as borderline", details

    if stat_score == 0:
        return True, "topic match; quantitative signal deferred", details

    return True, "topic and statistical signals present", details


def _paper_from_raw(raw: dict, db_name: str) -> PaperRecord:
    return PaperRecord(
        id=raw.get("id") or f"search:{uuid.uuid4().hex[:8]}",
        title=raw.get("title", ""),
        abstract=raw.get("abstract", ""),
        authors=raw.get("authors", []),
        year=raw.get("year", 0),
        url=raw.get("url"),
        source=raw.get("source", db_name),
        pdf_url=raw.get("open_access_pdf"),
        doi=raw.get("doi"),
        pmid=raw.get("pmid"),
        trial_registry_id=raw.get("trial_registry_id"),
        provenance=[raw.get("source", db_name)],
    )


def _doi_key(doi: Optional[str]) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (doi or "").strip().lower())


class _CandidateIndex:
    """Provenance-preserving merge dedup: a duplicate (by normalized title,
    or by DOI when both sides have one) does NOT get discarded -- its
    source is appended to the existing record's `provenance` list and the
    existing record's empty fields are backfilled from the duplicate,
    instead of the second sighting being dropped on the floor. Replaces the
    previous `seen_titles: set` (discard-on-repeat) so a paper found by two
    databases keeps a record of both, per this feature's explicit
    requirement -- and so a manually-imported record for the SAME paper an
    API already found merges into one candidate rather than screening the
    same paper twice."""

    def __init__(self):
        self._by_title: Dict[str, PaperRecord] = {}
        self._by_doi: Dict[str, PaperRecord] = {}

    def find_existing(self, title_key: str, doi_key: str) -> Optional[PaperRecord]:
        return self._by_title.get(title_key) or (self._by_doi.get(doi_key) if doi_key else None)

    def add(self, title_key: str, doi_key: str, paper: PaperRecord) -> None:
        self._by_title[title_key] = paper
        if doi_key:
            self._by_doi[doi_key] = paper

    def merge_into(self, existing: PaperRecord, new_source: str, raw: dict) -> None:
        if new_source not in existing.provenance:
            existing.provenance.append(new_source)
        # Backfill fields the earlier sighting left empty -- never overwrite
        # a value the first source already provided.
        if not existing.abstract and raw.get("abstract"):
            existing.abstract = raw["abstract"]
        if not existing.doi and raw.get("doi"):
            existing.doi = raw["doi"]
        if not existing.pdf_url and raw.get("open_access_pdf"):
            existing.pdf_url = raw["open_access_pdf"]
        if not existing.pmid and raw.get("pmid"):
            existing.pmid = raw["pmid"]
        if not existing.trial_registry_id and raw.get("trial_registry_id"):
            existing.trial_registry_id = raw["trial_registry_id"]

def search_node(state: GraphState) -> dict:
    """Stage 1 (search mode): discover papers and screen before full-text fetch."""
    plan: MetaAnalysisPlan = state["plan"]
    logger.info("=== STAGE 1: Literature Search ===")
    queries, query_generation_method = _build_intent_queries_with_method(plan)
    _save_search_queries(state, plan, queries, query_generation_method)
    logger.info(
        "[SearchAgent] Running Deep Research-first literature search "
        f"({len(queries)} intent queries, top-{MAX_PAPERS_PER_QUERY} per enabled source)."
    )
    total_cap = MAX_PAPERS_PER_QUERY if set(ENABLED_SEARCH_DATABASES or ()) == {"arxiv"} else None
    source_caps = {"arxiv": MAX_PAPERS_PER_QUERY}
    source_counts: Dict[str, int] = {}

    index = _CandidateIndex()
    all_retrieved: List[PaperRecord] = []
    papers: List[PaperRecord] = []
    rejected: List[dict] = []
    screening_decisions: Dict[str, Dict] = {}
    n_duplicates_removed = 0

    def _ingest(raw: dict, db_name: str) -> None:
        """Shared ingest path for BOTH API-retrieved and manually-imported
        raw paper dicts -- same dedup-merge, same prescreen, same
        PaperRecord conversion either way. A duplicate (by title or DOI)
        merges provenance into the existing candidate instead of being
        screened a second time; a genuinely new paper goes through
        _prefetch_screen_paper exactly as before."""
        nonlocal n_duplicates_removed
        title_key = _dedupe_key(raw.get("title") or "")
        doi_key = _doi_key(raw.get("doi"))
        if not title_key:
            return
        existing = index.find_existing(title_key, doi_key)
        if existing is not None:
            index.merge_into(existing, raw.get("source", db_name), raw)
            n_duplicates_removed += 1
            return
        paper = _paper_from_raw(raw, db_name)
        index.add(title_key, doi_key, paper)
        all_retrieved.append(paper)
        source_counts[db_name] = source_counts.get(db_name, 0) + 1

        include, reason, details = _prefetch_screen_paper(raw, plan)
        screening_decisions[paper.id] = {
            "decision": "include" if include else "exclude",
            "reason": reason,
            "title": paper.title,
            "source": paper.source,
            **details,
        }

        if include:
            papers.append(paper)
            logger.info(f"[SearchAgent] [{db_name}] SCREENED IN: {paper.title[:80]} ({reason})")
        else:
            rejected.append({
                "id": paper.id,
                "title": paper.title,
                "year": paper.year,
                "source": paper.source,
                "doi": paper.doi or "",
                "url": paper.url or "",
                "reason": reason,
                **details,
            })
            logger.info(f"[SearchAgent] [{db_name}] SCREENED OUT: {paper.title[:80]} ({reason})")

    # Manual imports (RIS/CSV/BibTeX) are loaded ONCE per run, not per query
    # -- they aren't query-dependent -- and go through the IDENTICAL ingest
    # path above: same dedup/merge, same prescreen, no special treatment.
    for path in MANUAL_IMPORT_PATHS:
        try:
            manual_papers = load_manual_import(path)
        except Exception as exc:
            logger.warning(f"[SearchAgent] Manual import failed for {path}: {exc}")
            continue
        logger.info(f"[SearchAgent] [manual_import] {len(manual_papers)} record(s) loaded from {path}")
        for raw in manual_papers:
            _ingest(raw, raw.get("source", "manual_import"))

    for query in queries:
        try:
            top_per_db = search_top_per_db(
                query,
                start_year=plan.search_start_year,
                top_n=MAX_PAPERS_PER_QUERY,
            )
        except Exception as exc:
            logger.warning(f"[SearchAgent] Search failed for query '{query}': {exc}")
            continue

        for db_name, raw_list in top_per_db.items():
            if not raw_list:
                logger.debug(f"[SearchAgent] [{db_name}] no results for query: {query!r}")
                continue
            if db_name in source_caps and source_counts.get(db_name, 0) >= source_caps[db_name]:
                logger.info(f"[SearchAgent] [{db_name}] source cap reached ({source_caps[db_name]}).")
                continue
            for raw in raw_list:
                if total_cap is not None and len(all_retrieved) >= total_cap:
                    break
                if db_name in source_caps and source_counts.get(db_name, 0) >= source_caps[db_name]:
                    break
                _ingest(raw, db_name)
            if total_cap is not None and len(all_retrieved) >= total_cap:
                break
        if total_cap is not None and len(all_retrieved) >= total_cap:
            logger.info(f"[SearchAgent] Reached arXiv-only search cap: {total_cap} unique papers.")
            break

    logger.info(
        f"[SearchAgent] {len(all_retrieved)} unique papers identified "
        f"({n_duplicates_removed} duplicate record(s) merged); "
        f"{len(papers)} screened in, {len(rejected)} screened out."
    )
    return {
        "papers_eligible":        papers,
        "n_search_retrieved":     len(all_retrieved),
        "all_retrieved_papers":   all_retrieved,
        "search_rejected_papers": rejected,
        "screening_decisions":    screening_decisions,
        "n_screened_excluded":    len(rejected),
        "n_duplicates_removed":   n_duplicates_removed,
    }
