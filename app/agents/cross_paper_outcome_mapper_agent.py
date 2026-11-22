"""Cross-Paper Outcome Mapper — Stage 4B.

Two-pass, closed-vocabulary outcome classification:
  Phase 1 (taxonomy): the LLM looks at THIS batch's own extracted outcome
    text and proposes a small, run-specific list of outcome families --
    never a fixed/hardcoded vocabulary, generated fresh from the data at
    hand every run (see record_outcome_taxonomy).
  Phase 2 (classification): every result row is classified against ONLY
    that closed list (validated in the tool body, not just prompted --
    see _make_record_mapped_result()), plus an explicit "doesn't fit any
    defined family" option so a row is never forced into the wrong bucket.

Root-cause context (CD008986 investigation): the previous single-pass,
freeform-text design merged its output back onto rows via an EXACT STRING
match on source_outcome_name -- any row the LLM paraphrased or never called
the tool for silently got outcome_family="" and fell into the undifferentiated
"default" pooling bucket alongside unrelated outcomes. This version merges by
row_index instead (assigned deterministically before the call, echoed back by
the tool) -- eliminates that whole class of merge failures outright, and any
row the LLM still never calls the tool for is now explicitly logged and
flagged (see models.ValidationFlag) instead of silently absorbed.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from pipeline_graph import _all_tool_args, _extract_tool_args, GraphState
from models import ValidationFlag
from core_utils import save_json

logger = logging.getLogger(__name__)

TAXONOMY_SYSTEM_PROMPT = (
    "You define a small, closed set of outcome families for a batch of extracted "
    "statistical results from a meta-analysis pipeline. You do NOT classify individual "
    "results in this phase -- only propose the vocabulary that Phase 2 will classify against."
)

CLASSIFY_SYSTEM_PROMPT = (
    "You map extracted statistical results to meta-analysis targets, using ONLY the "
    "closed outcome-family vocabulary already defined for this batch. Your job is to "
    "decide which results from different papers measure the same construct and can be "
    "compared in a meta-analysis."
)

# Sentinel outcome_family value for a row that genuinely doesn't fit any
# family defined in Phase 1 -- distinct from an empty/missing classification
# (which would previously fall silently into the "default" bucket). Rows
# with this value still get an explicit ValidationFlag, but are never forced
# into a wrong family just to avoid it.
UNCLASSIFIED = "UNCLASSIFIED"


@tool
def record_outcome_taxonomy(
    families: List[Dict[str, Any]],
    timepoints: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Phase 1: define this batch's own closed set of outcome families (and,
    if relevant, follow-up-timepoint labels), BEFORE classifying any
    individual row.

    families: a list of {"name": str, "description": str, "synonyms": [str, ...]}.
    The number of families is NOT capped -- it should match however many
    distinct outcomes/constructs THIS batch actually contains, which can
    legitimately be well over 10 for an outcome-rich review (e.g. a cognitive
    or neuropsychological review reporting a dozen+ different named tests and
    scales). Give EVERY genuinely distinct construct actually present in the
    batch's own text its own family, including a specific named test,
    instrument, or scale (e.g. "MoCA", "Boston Naming Test", "RBANS total
    score") when it measures something no broader family already covers --
    do not fold a distinct named instrument into an unrelated family just to
    keep the list short, and do not leave it out and rely on Phase 2's
    "doesn't fit" option as a substitute for defining it here. Conversely,
    never invent a family with no supporting rows, and never invent a generic
    catch-all like "other" (Phase 2 has its own explicit "doesn't fit" option
    for genuinely unclassifiable rows -- you don't need to pre-create one).
    Two rows that describe the same underlying construct with different
    wording (e.g. "all-cause mortality" and "overall survival" and "deceased
    within 1 year") belong under ONE family, not separate ones -- merge by
    MEANING, not by exact text. But two DIFFERENT named tests that both
    happen to measure a related domain (e.g. two different memory tests) are
    still separate families unless the batch's own text treats them as
    interchangeable -- do not merge distinct instruments just because they
    sound topically similar.

    timepoints: a list of {"name": str, "description": str}, defining a
    small, closed set of canonical follow-up/assessment-window labels (e.g.
    "immediate", "intermediate (1-6 months)", "long-term (>6 months)") --
    ONLY include this if the batch's own text actually distinguishes between
    multiple genuine follow-up windows for the same outcome (as opposed to
    each study just happening to report at a different single point in
    time). If the batch has no meaningful timepoint structure, return an
    empty list -- Phase 2 will then leave follow_up_timepoint null for every
    row rather than inventing ad hoc, inconsistent labels. Keep this list
    SMALL (typically 2-4 entries) and coarse -- it exists to let genuinely
    comparable follow-up windows across different studies collapse onto the
    same label, not to preserve every raw wording verbatim."""
    return "taxonomy_recorded"


def _make_record_mapped_result(valid_names: Dict[str, str], valid_timepoints: Dict[str, str]):
    """Build the Phase 2 tool bound to THIS run's closed vocabulary
    (valid_names: lowercased name -> canonical name; valid_timepoints: same
    shape, for follow_up_timepoint -- may be empty when Phase 1 found no
    genuine timepoint structure in this batch). A fresh closure per
    mapping_node() call, same pattern already used elsewhere in this
    codebase for per-run tool state (e.g.
    agents/statistical_result_extractor_agent.py's record_statistical_result)."""

    @tool
    def record_mapped_result(
        row_index: int,
        source_outcome_name: str,
        research_question_id: str,
        research_question_text: str,
        target_construct: str,
        outcome_family: str,
        effect_direction: str,
        meta_analysis_candidate: bool,
        conversion_priority: str,
        conversion_reason: str,
        follow_up_timepoint: Optional[str] = None,
        unit_of_analysis: Optional[str] = None,
        comparison_family: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """Record the mapped outcome for ONE result row.
        row_index: the row's position in the "Extracted statistical results"
          list below (0-based) -- copy it EXACTLY from the row you are
          classifying; this is how your answer gets matched back to that row.
        outcome_family: MUST be one of the family names defined in Phase 1
          (record_outcome_taxonomy), copied exactly, OR the literal string
          "UNCLASSIFIED" if this row genuinely fits none of them -- never
          invent a new family name here, and never force a bad fit just to
          avoid UNCLASSIFIED.
        comparison_family: LEAVE NULL/OMIT for the normal case -- a row whose
          comparison matches the review's own overall treatment-vs-control
          framing (shown in the prompt below). Every study using its own
          program/drug/protocol name for what is still fundamentally the
          SAME kind of comparison is the NORMAL case -- leave this null, do
          NOT invent a per-paper label. This INCLUDES a more/less intensive,
          extended/basic, high/standard-dose, or otherwise differently-
          IMPLEMENTED version of the SAME underlying intervention type --
          e.g. "extended pharmacist intervention" and "basic pharmacist
          intervention" are still ONE comparison_family (implementation
          intensity is a subgroup/moderator question, analyzed separately
          downstream from the study-level data already captured -- it must
          NOT remove a study from the review's main pooled comparison).
          ONLY set a value when this row's comparison is genuinely a
          DIFFERENT, distinct TYPE of intervention or comparator from the
          review's main one (e.g. the review deliberately tests an unrelated
          second intervention -- drug A vs placebo AND an unrelated drug B
          vs placebo -- as separate planned arms of its own design) -- and
          even then, keep the label short and reusable so every OTHER row
          belonging to that same distinct comparison can match it exactly.
          When genuinely unsure whether a difference is "implementation
          variant" or "different intervention type", leave it null -- a
          study wrongly excluded from the main pool is a worse outcome than
          one wrongly included in it.
          CRITICAL DISTINCTION -- do not confuse the above (different
          implementation of the SAME intervention type, stays null) with a
          row whose own control/comparator arm is genuinely ANOTHER
          instance of the intervention type itself, e.g. one app version
          vs. a different app version, when the review's requested
          comparator is "no intervention or minimal/usual care". That row
          has NO group matching the requested comparator at all -- this is
          not a borderline case, set comparison_family to a short label
          (e.g. "app_vs_app") so it is excluded from the main pool. A
          confirmed failure mode: a trial comparing two versions of the
          same smartphone app was pooled into an "app vs no/minimal
          intervention" analysis it should never have joined, because its
          own control arm was another app, not a genuine no/minimal-
          intervention condition.
        conversion_priority: direct | convertible_with_assumptions | not_convertible
        follow_up_timepoint: MUST be an exact name from this batch's closed
          timepoint vocabulary (defined in Phase 1), copied exactly, or
          null/omit when the paper's own text doesn't state a follow-up
          window for this result. If Phase 1 defined NO timepoint vocabulary
          for this batch (no genuine timepoint structure detected), this
          must always be null -- never invent a one-off label here.
        unit_of_analysis: ONLY when the paper explicitly states one (e.g. "per
          participant", "per event", "per limb") -- null/omit otherwise."""
        if row_index is None:
            return "ERROR: row_index is required."
        family_key = (outcome_family or "").strip().lower()
        if family_key != UNCLASSIFIED.lower() and family_key not in valid_names:
            allowed = ", ".join(sorted(valid_names.values())) or "(no families defined)"
            return (
                f"ERROR: outcome_family '{outcome_family}' is not one of this batch's defined "
                f"families ({allowed}) and is not '{UNCLASSIFIED}'. Retry with an exact match, "
                f"or '{UNCLASSIFIED}' if this row truly fits none of them."
            )
        timepoint_key = (follow_up_timepoint or "").strip().lower()
        if timepoint_key and timepoint_key not in valid_timepoints:
            allowed_tp = ", ".join(sorted(valid_timepoints.values())) or "(no timepoints defined for this batch)"
            return (
                f"ERROR: follow_up_timepoint '{follow_up_timepoint}' is not one of this batch's "
                f"defined timepoints ({allowed_tp}). Retry with an exact match, or omit/null it."
            )
        return "result_mapped"

    return record_mapped_result


def mapping_node(state: GraphState) -> dict:
    """Stage 4B: normalise outcome names across papers for comparability."""
    logger.info("=== STAGE 4B: Cross-Paper Mapping ===")
    results: List[dict] = state.get("paper_results", [])
    user_query: str = state.get("user_prompt", "")
    output_dir: str = state["output_dir"]
    plan = state.get("plan")
    validation_flags: List[ValidationFlag] = list(state.get("validation_flags", []))
    logger.info(f"[Mapper] Starting outcome mapping of {len(results)} result rows.")

    if not results:
        return {"mapped_results": []}

    # ── Phase 1: run-specific closed taxonomy ──────────────────────────────
    distinct_outcomes = []
    seen = set()
    for row in results:
        label = (row.get("outcome_name") or row.get("task_or_measure") or "").strip()
        if label and label.lower() not in seen:
            seen.add(label.lower())
            distinct_outcomes.append({
                "outcome_name": row.get("outcome_name"),
                "task_or_measure": row.get("task_or_measure"),
                "evidence_quote": row.get("evidence_quote"),
            })

    taxonomy_agent = create_react_agent(llm, [record_outcome_taxonomy], prompt=TAXONOMY_SYSTEM_PROMPT)
    taxonomy_msg = (
        f"User meta-analysis question:\n{user_query}\n\n"
        f"Distinct outcome labels extracted across all papers in this batch "
        f"({len(distinct_outcomes)} total):\n{distinct_outcomes}\n\n"
        "Define this batch's closed set of outcome families now, via record_outcome_taxonomy. "
        "Also inspect the same text for any genuine follow-up/assessment-timepoint structure "
        "(e.g. the same outcome reported at several distinct follow-up windows across studies) "
        "and, if present, define a small closed timepoints vocabulary for it too -- leave "
        "timepoints empty if the batch has no such structure."
    )
    taxonomy_result = taxonomy_agent.invoke({"messages": [("user", taxonomy_msg)]})
    taxonomy_args = _extract_tool_args(taxonomy_result["messages"], "record_outcome_taxonomy")
    families = taxonomy_args.get("families") or []
    timepoints = taxonomy_args.get("timepoints") or []

    valid_names: Dict[str, str] = {}
    for f in families:
        name = (f.get("name") or "").strip()
        if name:
            valid_names[name.lower()] = name

    # ── Single-outcome override ─────────────────────────────────────────────
    # When the plan itself declares there is exactly ONE target outcome (see
    # models.MetaAnalysisPlan.single_outcome_target), don't let Phase 1
    # freely invent per-instrument sub-families for it (e.g. "PANSS positive
    # symptoms" vs "BPRS positive symptoms" vs "SAPS positive symptoms" all
    # measuring the SAME target construct). Confirmed via a real test run
    # (a single-outcome-scoped prompt over 25 papers) that without this
    # override, one declared target outcome still fragmented into 3 separate
    # pooling groups purely because of which rating scale each study used --
    # this is a deterministic Python-level override, not a hope that the LLM
    # gets it right, and it activates for ANY plan that names one outcome,
    # never a hardcoded list for any specific review.
    single_outcome_target = (
        (getattr(plan, "single_outcome_target", None) or "").strip() if plan else ""
    )
    if single_outcome_target:
        if len(valid_names) != 1 or single_outcome_target.lower() not in valid_names:
            logger.info(
                f"[Mapper] single_outcome_target={single_outcome_target!r} is set -- collapsing "
                f"Phase 1's {len(valid_names)} proposed famil{'y' if len(valid_names) == 1 else 'ies'} "
                f"({sorted(valid_names.values())}) into that one target family."
            )
        valid_names = {single_outcome_target.lower(): single_outcome_target}
        # Keep the vocabulary shown to Phase 2 in sync with the override --
        # `families` is echoed verbatim into classify_msg below, so it must
        # reflect the one collapsed family, not Phase 1's original (possibly
        # multi-family) proposal.
        families = [{"name": single_outcome_target,
                     "description": "This run's single declared target outcome -- classify "
                                     "every result measuring this construct here, regardless of "
                                     "which specific instrument/scale was used."}]

    valid_timepoints: Dict[str, str] = {}
    for t in timepoints:
        name = (t.get("name") or "").strip()
        if name:
            valid_timepoints[name.lower()] = name

    if not valid_names:
        logger.warning("[Mapper] Phase 1 produced no usable taxonomy — every row will be UNCLASSIFIED.")
        validation_flags.append(ValidationFlag(
            stage="outcome_classification", severity="warning", subject_id="(batch)",
            message="Taxonomy pass produced no families; all rows fall back to UNCLASSIFIED.",
            auto_action="none",
        ))
    else:
        logger.info(f"[Mapper] Phase 1 taxonomy: {sorted(valid_names.values())}")
    if valid_timepoints:
        logger.info(f"[Mapper] Phase 1 timepoint vocabulary: {sorted(valid_timepoints.values())}")
    else:
        logger.info("[Mapper] Phase 1 found no genuine timepoint structure; follow_up_timepoint will stay null for this batch.")

    # ── Phase 2: classify every row against ONLY that closed list ──────────
    record_mapped_result = _make_record_mapped_result(valid_names, valid_timepoints)
    classify_agent = create_react_agent(llm, [record_mapped_result], prompt=CLASSIFY_SYSTEM_PROMPT)
    indexed_results = [
        {"row_index": i, **{k: v for k, v in row.items() if k not in ("full_text",)}}
        for i, row in enumerate(results)
    ]
    plan_comparison_hint = (
        f"\nThis review's OWN single treatment-vs-control framing (from the meta-analysis plan): "
        f"'{plan.treatment_label}' vs '{plan.control_label}'.\n"
        if plan and getattr(plan, "treatment_label", None) and getattr(plan, "control_label", None)
        else ""
    )
    single_outcome_hint = (
        f"\nThis run has exactly ONE target outcome, declared by the user's own question: "
        f"'{single_outcome_target}'. Classify EVERY row that measures this construct into this "
        "one family, REGARDLESS of which specific instrument, scale, or named test was used to "
        "measure it (e.g. PANSS vs BPRS vs SAPS positive-symptom subscales, or CDSS vs BDI for "
        "depression, all count as the SAME family if they measure this same target construct) -- "
        "do NOT split by instrument name. Only use UNCLASSIFIED for a row that measures something "
        "genuinely different from this target construct, not merely a different scale for it.\n"
        if single_outcome_target else ""
    )
    classify_msg = (
        f"User meta-analysis question:\n{user_query}\n"
        f"{plan_comparison_hint}"
        f"{single_outcome_hint}\n"
        f"Closed outcome-family vocabulary for this batch (use ONLY these names, or "
        f"'{UNCLASSIFIED}'):\n{families}\n\n"
        f"Closed follow-up-timepoint vocabulary for this batch (use ONLY these names, or "
        f"leave follow_up_timepoint null -- {'this batch has none defined, so it must always be null' if not valid_timepoints else 'do not invent a label outside this list'}):\n{timepoints}\n\n"
        f"Extracted statistical results (classify EVERY row_index below):\n{indexed_results}\n\n"
        "Map each statistical result to a meta-analysis target.\n\n"
        "Rules:\n"
        "1. outcome_family MUST be an exact name from the closed vocabulary above, or "
        f"'{UNCLASSIFIED}' -- never a new/invented family name.\n"
        "2. Results with the same meaning (even worded differently across papers) get the "
        "SAME outcome_family -- classify by MEANING, not exact text.\n"
        "3. comparison_family: LEAVE THIS NULL/OMITTED for the normal case -- a row whose comparison "
        "matches this review's own treatment-vs-control framing above. Every study using its own "
        "program/protocol/brand name for what is still fundamentally the SAME kind of intervention "
        "(e.g. three different named clinical decision-support tools that are all just 'the "
        "intervention vs its comparator') is the NORMAL case -- do NOT invent a per-paper label for "
        "it, leave the field null. This INCLUDES a more/less intensive, extended/basic, or "
        "high/standard-dose version of the SAME underlying intervention type -- implementation "
        "intensity is a subgroup/moderator question analyzed separately, NOT grounds to exclude a "
        "study from the review's main pooled comparison. ONLY set a comparison_family value when "
        "this row's comparison is genuinely a DIFFERENT, distinct TYPE of intervention or comparator "
        "from the review's main one, deliberately part of the review's OWN design (e.g. the review "
        "has both a 'drug A vs placebo' arm and an unrelated 'drug B vs placebo' arm as separate "
        "planned comparisons) -- and even then, reuse the exact same label for every other row "
        "belonging to that same distinct comparison. When genuinely unsure whether a difference is "
        "'implementation variant' or 'different intervention type', leave it null -- a study wrongly "
        "excluded from the main pool is a worse outcome than one wrongly included in it.\n"
        "   CRITICAL DISTINCTION -- do not confuse the above (different implementation of the SAME "
        "intervention type, stays null) with a row whose own control/comparator arm is genuinely "
        "ANOTHER instance of the intervention type itself -- e.g. one app version vs. a different "
        "app version -- when the review's requested comparator is 'no intervention or minimal/usual "
        "care'. That row has NO group matching the requested comparator at all -- this is not a "
        "borderline case, set comparison_family to a short label (e.g. 'app_vs_app') so it is "
        "excluded from the main pool. A confirmed failure mode: a trial comparing two versions of "
        "the same smartphone app was pooled into an 'app vs no/minimal intervention' analysis it "
        "should never have joined, because its own control arm was another app, not a genuine "
        "no/minimal-intervention condition.\n"
        "4. Mark meta_analysis_candidate=True only if the result answers the user's meta-analysis question.\n"
        "5. conversion_priority='direct' for means/SDs, t-tests with n, or simple two-group statistics.\n"
        "6. conversion_priority='convertible_with_assumptions' for odds/risk/hazard ratios, "
        "correlations, one-df F tests, or partial information.\n"
        "7. conversion_priority='not_convertible' for regression-only or mixed-model-only "
        "coefficients without enough information.\n"
        "8. follow_up_timepoint: MUST be an exact name copied from the closed timepoint vocabulary "
        "above, or null. If the result's own outcome_name, task_or_measure, or evidence_quote states "
        "a follow-up window or assessment timepoint that corresponds to one of those vocabulary "
        "entries, record that exact name. Never invent a label that isn't in the vocabulary above -- "
        "if the batch's timepoint vocabulary is empty, or this result's timepoint doesn't correspond "
        "to any entry in it, leave follow_up_timepoint null. Whether it later splits a pooling group "
        "is decided downstream, not by you. Do not guess.\n"
        "   A confirmed failure mode to watch for specifically: when ONE paper reports the SAME "
        "outcome at several timepoints (e.g. immediate, intermediate, AND long-term follow-up), do "
        "NOT default to whichever one is statistically most complete or most significant if its own "
        "text names a DIFFERENT timepoint than the one you're mapping it to -- e.g. a result whose "
        "evidence_quote says 'baseline to long-term follow-up' must be mapped to a long-term-named "
        "vocabulary entry, or left null, NEVER to an intermediate/short-term entry just because it "
        "looked like the best available number for that window. Match what the text says, not what "
        "would be convenient.\n"
        "9. Call record_mapped_result ONCE for every row_index shown above -- do not skip any."
    )
    result = classify_agent.invoke({"messages": [("user", classify_msg)]})

    mapped = _all_tool_args(result["messages"], "record_mapped_result")
    by_index: Dict[int, dict] = {}
    for m in mapped:
        idx = m.get("row_index")
        if idx is not None:
            by_index[idx] = m

    merged: List[dict] = []
    missing_indices: List[int] = []
    for i, row in enumerate(results):
        mapping = by_index.get(i)
        if mapping is None:
            missing_indices.append(i)
            merged.append({**row, **{
                "target_construct": "", "outcome_family": "", "comparison_family": "",
                "effect_direction": "", "meta_analysis_candidate": True,
                "conversion_priority": "direct", "follow_up_timepoint": None,
                "unit_of_analysis": None,
            }})
            continue
        family_raw = (mapping.get("outcome_family") or "").strip()
        outcome_family = "" if family_raw.upper() == UNCLASSIFIED else valid_names.get(family_raw.lower(), family_raw)
        timepoint_raw = (mapping.get("follow_up_timepoint") or "").strip()
        # Normalise to the Phase-1 canonical casing, same as outcome_family
        # above. A value that (despite the tool-level validation) doesn't
        # match the closed vocabulary is dropped to null rather than kept
        # verbatim -- this is exactly the fragmentation bug being fixed: a
        # one-off, non-canonical timepoint string must never reach the
        # pooling key.
        follow_up_timepoint = valid_timepoints.get(timepoint_raw.lower()) if timepoint_raw else None

        # Deterministic safety net for a confirmed real failure mode (the
        # CD008754 Chiaravalloti 2005 investigation): the LLM classifier
        # sometimes assigns an EARLIER timepoint bucket (e.g. "Intermediate")
        # to a result whose own text explicitly names a LATER one (e.g.
        # "baseline to long-term follow-up") -- most likely because that
        # result is more statistically complete/prominent than the
        # genuinely-eligible one, and the classifier defaults to it anyway
        # despite Rule 8's instruction. This is self-contradictory on its
        # face and doesn't need another LLM call to catch: if the row's own
        # extracted text says "long-term" but the assigned bucket's name
        # doesn't, null the assignment (excluding it from pooling, exactly
        # the fallback Rule 8 already specifies for a non-matching
        # timepoint) rather than silently trusting a self-contradicting
        # classification, and record why.
        row_text = " ".join(
            str(row.get(f) or "") for f in ("outcome_name", "task_or_measure", "evidence_quote")
        ).lower()
        if follow_up_timepoint and ("long-term" in row_text or "long term" in row_text) \
                and "long" not in follow_up_timepoint.lower():
            validation_flags.append(ValidationFlag(
                stage="outcome_classification", severity="warning",
                subject_id=row.get("paper_id", f"row_{i}"),
                message=f"Row {i} ('{row.get('outcome_name', '')}') was classified as timepoint "
                        f"'{follow_up_timepoint}', but its own outcome_name/evidence_quote explicitly "
                        "says 'long-term' -- overridden to unclassified (null) rather than silently "
                        "pooled into a timepoint window it contradicts on its face.",
                auto_action="reclassified_null",
            ))
            follow_up_timepoint = None

        merged.append({**row, **{
            "target_construct":    mapping.get("target_construct", ""),
            "outcome_family":      outcome_family,
            "comparison_family":   mapping.get("comparison_family", ""),
            "effect_direction":    mapping.get("effect_direction", ""),
            "meta_analysis_candidate": mapping.get("meta_analysis_candidate", True),
            "conversion_priority": mapping.get("conversion_priority", "direct"),
            "follow_up_timepoint": follow_up_timepoint,
            "unit_of_analysis":    mapping.get("unit_of_analysis") or None,
        }})
        if family_raw.upper() == UNCLASSIFIED:
            validation_flags.append(ValidationFlag(
                stage="outcome_classification", severity="info",
                subject_id=row.get("paper_id", f"row_{i}"),
                message=f"Row {i} ('{row.get('outcome_name', '')}') did not fit any defined "
                        "outcome family; left unclassified rather than forced into the wrong one.",
                auto_action="none",
            ))

    if missing_indices:
        logger.warning(
            f"[Mapper] {len(missing_indices)} row(s) never classified by the LLM "
            f"(indices: {missing_indices}) — left unclassified, not silently defaulted."
        )
        for i in missing_indices:
            validation_flags.append(ValidationFlag(
                stage="outcome_classification", severity="warning",
                subject_id=results[i].get("paper_id", f"row_{i}"),
                message=f"Row {i} ('{results[i].get('outcome_name', '')}') was never classified "
                        "by the mapper (no tool call emitted for it).",
                auto_action="none",
            ))

    save_json(merged, os.path.join(output_dir, "mapped_results.json"))
    logger.info(f"[Mapper] {len(merged)} results mapped ({len(missing_indices)} unclassified).")
    # Also update the in-memory "paper_results" state key, not just
    # "mapped_results" -- export_table_node (the very next stage) reads
    # state["paper_results"], and previously never saw "mapped_results" at
    # all, so outcome_family/follow_up_timepoint were computed here and then
    # silently discarded before they could reach EffectSizeRecord/pooling.
    # `merged` is a strict superset of `results` (every original field plus
    # the mapping ones), so this is safe for every downstream consumer that
    # only reads the original fields.
    return {"mapped_results": merged, "paper_results": merged, "validation_flags": validation_flags}
