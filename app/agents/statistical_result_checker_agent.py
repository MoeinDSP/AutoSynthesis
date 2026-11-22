"""Statistical Result Checker — Stage 4 (validation). Pattern 1: record-output tool."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from models import PaperRecord

if TYPE_CHECKING:
    from pipeline_graph import GraphState

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a rigorous statistical fact-checker for meta-analysis.\n\n"
    "You are given the full text of a research paper and a list of statistical "
    "results that were automatically extracted from it. Your job is to verify "
    "each result by locating the exact numbers in the paper text.\n\n"
    "Rules:\n"
    "1. Only accept a number as verified if it appears VERBATIM (or within "
    "   rounding) in the paper text — in the Results section, tables, or "
    "   figure captions.\n"
    "2. Do NOT accept numbers from Introduction, Related Work, or Discussion "
    "   sections that describe OTHER studies.\n"
    "3. If a value is wrong but the correct value is in the text, issue a "
    "   'corrected' verdict and provide the corrected value.\n"
    "4. If a value cannot be located anywhere in the text, mark it in "
    "   failed_stats.\n"
    "5. Mark the result 'hallucinated' only if the CORE numbers (test "
    "   statistic, p-value, or means) are absent from the paper text entirely.\n"
    "6. Call `record_validation` once per extracted result row.\n"
    "7. Be precise: 3.77 and 3.78 are NOT the same."
)

_MAX_CHARS = 100_000
_NUMERIC_FIELDS = [
    "test_statistic", "df1", "df2", "p_value",
    "group_1_n", "group_1_mean", "group_1_sd",
    "group_2_n", "group_2_mean", "group_2_sd",
]
_CORE_NUMERIC_FIELDS = {
    "test_statistic", "p_value",
    "group_1_mean", "group_1_sd", "group_1_n",
    "group_2_mean", "group_2_sd", "group_2_n",
}
_STAT_CONTEXT_RE = re.compile(
    r"\b(?:p\s*[<=>]|t\s*\(|f\s*\(|z\s*\(|anova|mean|sd|standard deviation|"
    r"confidence interval|odds ratio|cohen'?s d|hedges'? g|effect size)\b",
    flags=re.IGNORECASE,
)


def _all_tool_args(messages: list, tool_name: str) -> list:
    """Return args dicts for every call to `tool_name` in message history."""
    results = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == tool_name:
                    results.append(dict(tc["args"]))
    return results


@tool
def record_validation(
    row_index: int,
    paper_id: str,
    study_label: str,
    outcome_name: str,
    verdict: str,
    confidence: str,
    evidence_quote: str,
    verified_stats: Optional[List[str]] = None,
    failed_stats: Optional[List[str]] = None,
    corrections: Optional[Dict[str, Any]] = None,
    validation_notes: Optional[str] = None,
) -> str:
    """Record validation verdict for one extracted result row.
    row_index: 1-based row number exactly as shown in the validation prompt.
    verdict: verified | corrected | unverifiable | hallucinated
    confidence: high | medium | low"""
    return "validation_recorded"


def _coerce_number(value: Any) -> Optional[float]:
    if value in (None, "", "NA", "N/A", "not reported"):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    # In this extraction schema, 0 means "not reported" for numeric fields.
    if number == 0:
        return None
    return number


def _numeric_variants(value: float) -> List[str]:
    variants = {
        f"{value:g}",
        f"{value:.1f}",
        f"{value:.2f}",
        f"{value:.3f}",
    }
    if 0 < abs(value) < 1:
        variants.add(f"{value:.2f}".replace("0.", "."))
        variants.add(f"{value:.3f}".replace("0.", "."))
    if float(value).is_integer():
        variants.add(str(int(value)))
    return sorted(variants, key=len, reverse=True)


def _number_appears(value: Any, text: str) -> bool:
    number = _coerce_number(value)
    if number is None or not text:
        return False

    compact_text = re.sub(r"\s+", " ", text)
    for variant in _numeric_variants(number):
        if re.search(rf"(?<!\d){re.escape(variant)}(?!\d)", compact_text):
            return True

    tolerance = max(0.01, abs(number) * 0.005)
    for match in re.finditer(r"(?<![A-Za-z])-?\d+(?:\.\d+)?", compact_text):
        try:
            candidate = float(match.group(0))
        except ValueError:
            continue
        if abs(candidate - number) <= tolerance:
            return True
    return False


def _quote_appears(quote: Any, text: str) -> bool:
    quote_text = re.sub(r"\s+", " ", str(quote or "")).strip()
    if len(quote_text) < 16 or not text:
        return False
    haystack = re.sub(r"\s+", " ", text)
    if quote_text in haystack:
        return True
    # Use a distinctive excerpt for OCR/table conversions that alter spacing.
    excerpt = quote_text[:120]
    return len(excerpt) >= 32 and excerpt in haystack


def _deterministic_row_signal(row: Dict[str, Any], text: str) -> Dict[str, Any]:
    """Detect whether a result row has numeric/statistical support in text."""
    checked_stats = [
        field for field in _NUMERIC_FIELDS
        if _coerce_number(row.get(field)) is not None
    ]
    verified_stats = [
        field for field in checked_stats
        if _number_appears(row.get(field), text)
    ]
    core_verified = [field for field in verified_stats if field in _CORE_NUMERIC_FIELDS]
    evidence_quote_found = _quote_appears(row.get("evidence_quote"), text)
    has_statistical_context = bool(_STAT_CONTEXT_RE.search(text or ""))

    return {
        "checked_stats": checked_stats,
        "verified_stats": verified_stats,
        "core_verified_stats": core_verified,
        "evidence_quote_found": evidence_quote_found,
        "has_statistical_context": has_statistical_context,
        "strong_match": (
            evidence_quote_found
            or len(core_verified) >= 1
            or len(verified_stats) >= 2
        ),
    }


def validation_node(state: GraphState) -> dict:
    """Stage 4 (validation): verify extracted results against paper text."""
    logger.info("=== STAGE 4: Validation ===")
    papers: List[PaperRecord] = state.get("papers_eligible", [])
    paper_results: List[dict] = state.get("paper_results", [])
    logger.info(f"[Checker] Starting validation of {len(paper_results)} result rows across {len(papers)} papers.")

    if not paper_results:
        return {"paper_results": []}

    paper_lookup = {p.id: p for p in papers}
    cleaned_results: List[dict] = []

    for paper_id, results_for_paper in _group_by_paper(paper_results).items():
        logger.info(f"[Checker] Validating {paper_id} ({len(results_for_paper)} rows)...")
        paper = paper_lookup.get(paper_id)
        if not paper:
            cleaned_results.extend(results_for_paper)
            continue

        text = (paper.full_text or paper.abstract or "")[:_MAX_CHARS]

        result_lines = []
        deterministic_signals: List[Dict[str, Any]] = []
        for i, r in enumerate(results_for_paper, start=1):
            signal = _deterministic_row_signal(r, text)
            deterministic_signals.append(signal)
            line = (
                f"[Row {i}] study_label={r.get('study_label')!r} "
                f"outcome_name={r.get('outcome_name')!r} "
                f"statistic_type={r.get('statistic_type')!r} "
                f"test_statistic={r.get('test_statistic')} "
                f"df1={r.get('df1')} df2={r.get('df2')} "
                f"p_value={r.get('p_value')} "
                f"group_1_label={r.get('group_1_label')!r} "
                f"group_1_n={r.get('group_1_n')} "
                f"group_1_mean={r.get('group_1_mean')} "
                f"group_1_sd={r.get('group_1_sd')} "
                f"group_2_label={r.get('group_2_label')!r} "
                f"group_2_n={r.get('group_2_n')} "
                f"group_2_mean={r.get('group_2_mean')} "
                f"group_2_sd={r.get('group_2_sd')} "
                f"evidence_quote={r.get('evidence_quote')!r} "
                f"deterministic_verified_stats={signal['verified_stats']} "
                f"deterministic_evidence_quote_found={signal['evidence_quote_found']}"
            )
            result_lines.append(line)

        user_msg = (
            f"Paper ID : {paper_id}\n"
            f"Title    : {paper.title}\n\n"
            f"Full paper text:\n{text}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "EXTRACTED RESULTS TO VALIDATE\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            + "\n".join(result_lines)
            + "\n\n"
            "For each row above, call record_validation with:\n"
            "  • row_index: the exact 1-based Row number shown above. This is mandatory.\n"
            "  • verdict: verified / corrected / unverifiable / hallucinated\n"
            "  • verified_stats: field names whose values appear verbatim in the text\n"
            "  • failed_stats: field names whose values cannot be located\n"
            "  • corrections: {field_name: correct_value} for any wrong values\n"
            "  • evidence_quote: verbatim text from the paper supporting your verdict\n\n"
            "If two rows have the same study_label and outcome_name, row_index is the "
            "only reliable identifier; do not merge them.\n\n"
            "Check every numeric field: test_statistic, df1, df2, p_value, "
            "group_1_mean, group_1_sd, group_2_mean, group_2_sd, group_1_n, group_2_n.\n"
            "A 0 in any numeric field means 'not reported' — treat it as missing.\n\n"
            "SAMPLE SIZE VERIFICATION — pay special attention:\n"
            "  1. Locate where the paper states per-condition Ns (table headers, footnotes, "
            "Methods section, or inline '(n=X)' in Results).\n"
            "  2. Distinguish enrolled/recruited N from final analysed N — always verify "
            "against the analysed N.\n"
            "  3. Consistency check: group_1_n + group_2_n should ≈ n_total reported in the row. "
            "If the sum is wrong, issue a 'corrected' verdict with the right values.\n"
            "  4. DF cross-check: for an independent-samples t-test, df = group_1_n + group_2_n − 2. "
            "If the extracted df and Ns are inconsistent, correct the Ns to match df.\n"
            "  5. If only total N is in the paper and the groups appear equal, "
            "set group_1_n = group_2_n = N/2 via a 'corrected' verdict.\n\n"
            "Mark 'hallucinated' only if the test statistic AND p-value are both "
            "absent from the paper text."
        )

        agent = create_react_agent(llm, [record_validation], prompt=SYSTEM_PROMPT)
        result = agent.invoke({"messages": [("user", user_msg)]})

        # Key by row index so duplicate (study_label, outcome_name) pairs are handled correctly.
        raw_validations = _all_tool_args(result["messages"], "record_validation")
        validations_by_index: Dict[int, dict] = {}
        validations_by_key: Dict[tuple, dict] = {}
        for v in raw_validations:
            try:
                idx = int(v.get("row_index", 0)) - 1
                if idx >= 0:
                    validations_by_index[idx] = v
            except (TypeError, ValueError):
                pass
            validations_by_key[(v.get("study_label", ""), v.get("outcome_name", ""))] = v

        for i, row in enumerate(results_for_paper):
            val = validations_by_index.get(i) or validations_by_key.get(
                (row.get("study_label", ""), row.get("outcome_name", "")), {}
            )
            verdict = val.get("verdict", "unverifiable")
            signal = deterministic_signals[i] if i < len(deterministic_signals) else {}
            if verdict == "hallucinated":
                if signal.get("strong_match"):
                    logger.info(
                        "[Checker] Keeping row marked hallucinated by LLM because "
                        f"deterministic signal found support: [{i}] "
                        f"{row.get('study_label')} / {row.get('outcome_name')}"
                    )
                    cleaned_results.append(row)
                    continue
                logger.info(f"[Checker] Removed hallucinated result: [{i}] {row.get('study_label')} / {row.get('outcome_name')}")
                continue
            if verdict == "corrected" and val.get("corrections"):
                row.update(val["corrections"])
            cleaned_results.append(row)

    logger.info(
        f"[Checker] {len(cleaned_results)}/{len(paper_results)} results passed validation."
    )
    return {"paper_results": cleaned_results}


def _group_by_paper(results: List[dict]) -> Dict[str, List[dict]]:
    groups: Dict[str, List[dict]] = {}
    for r in results:
        pid = r.get("paper_id", "unknown")
        groups.setdefault(pid, []).append(r)
    return groups
