"""
PRISMA Flowchart Agent — Stage 10.

The LLM reads a structured pipeline summary and calls `submit_prisma_data`
with all PRISMA 2020 counts (and meaningful exclusion reasons inferred from
the plan). Python then renders a publication-quality PNG flowchart.
"""

from __future__ import annotations

import logging
import os
import textwrap
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from agents.llm import llm
from pipeline_graph import GraphState, _extract_tool_args
from statistics.plots import _installed_font

logger = logging.getLogger(__name__)

# Arial itself is rarely installed on Linux; Liberation Sans is metric-
# compatible and used as the closest available substitute when true Arial
# is absent (same fallback chain as the other plots in statistics/plots.py).
_SANS_FONT = _installed_font(["Arial", "Liberation Sans", "DejaVu Sans"])

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
    "mathtext.fontset": "custom",
    "mathtext.rm": _SANS_FONT,
    "mathtext.it": f"{_SANS_FONT}:italic",
    "mathtext.bf": f"{_SANS_FONT}:bold",
    "font.size": 15,
    "axes.titlesize": 19,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
})

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a systematic review methodologist generating PRISMA 2020 flowchart data.\n"
    "Read the pipeline summary and call `submit_prisma_data` EXACTLY ONCE.\n\n"
    "Field rules:\n"
    "- n_identified: total distinct papers retrieved from databases after deduplication.\n"
    "- n_duplicates_removed: copy the exact value given in the pipeline summary — it is "
    "the real count of records merged as duplicates by the search node's dedup index, "
    "not an estimate.\n"
    "- n_screened: papers assessed by title/abstract. Use -1 if mode is manual.\n"
    "- n_excluded_screening: papers excluded at screening. Use -1 if screening was skipped.\n"
    "- n_assessed_eligibility: n_screened minus n_excluded_screening. Use -1 if skipped.\n"
    "- n_excluded_eligibility: papers excluded at full-text eligibility. Use -1 if skipped.\n"
    "- n_included: papers that passed all filters (provided in summary).\n"
    "- n_effect_sizes: total effect sizes computed (provided in summary).\n"
    "- screening_exclusion_reasons: 2-3 concise labels, e.g. 'Not related to research "
    "topic', 'Non-empirical / review paper'. Empty list if screening was skipped.\n"
    "- eligibility_exclusion_reasons: 2-3 concise labels derived from the plan's exclusion "
    "criteria, e.g. 'Insufficient study design', 'No quantitative outcome data', "
    "'Wrong population or intervention'. Empty list if eligibility was skipped."
)

# ── Tool ──────────────────────────────────────────────────────────────────────

@tool
def submit_prisma_data(
    n_identified: int,
    n_duplicates_removed: int,
    n_screened: int,
    n_excluded_screening: int,
    screening_exclusion_reasons: List[str],
    n_assessed_eligibility: int,
    n_excluded_eligibility: int,
    eligibility_exclusion_reasons: List[str],
    n_included: int,
    n_effect_sizes: int,
) -> str:
    """Submit PRISMA 2020 flowchart counts. Use -1 for stages that were skipped."""
    return "prisma_data_submitted"


# ── Colour palette ────────────────────────────────────────────────────────────
# Matches the official PRISMA 2020 template look: plain white boxes with a
# black border, an amber "Identification of studies via ..." banner, and a
# light blue-lavender phase strip down the left side.

_BOX_FC    = "#ffffff"
_BANNER_FC = "#f5c451"
_PHASE_FC  = "#c9d7f0"
_EDGE      = "#1f2937"
_PHASE_TXT = "#1e3a5f"


# ── Drawing primitives ────────────────────────────────────────────────────────

def _box(ax, x: float, y: float, w: float, h: float,
         text: str, fc: str = _BOX_FC, fontsize: int = 14, bold: bool = False,
         ha: str = "left"):
    """Draw a (near-)rectangular box with wrapped text (left-aligned by default,
    matching the official PRISMA template)."""
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.1,
        edgecolor=_EDGE,
        facecolor=fc,
        zorder=2,
    ))
    text_x = x + 0.18 if ha == "left" else x + w / 2
    ax.text(
        text_x, y + h / 2, text,
        ha=ha, va="center",
        fontsize=fontsize,
        fontweight="bold" if bold else "normal",
        multialignment="left" if ha == "left" else "center",
        zorder=3,
    )


def _banner(ax, x: float, y: float, w: float, h: float, text: str):
    """Draw the amber 'Identification of studies via ...' header banner."""
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.1,
        edgecolor=_EDGE,
        facecolor=_BANNER_FC,
        zorder=2,
    ))
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=15, fontweight="bold",
        zorder=3,
    )


def _down(ax, x: float, y_from: float, y_to: float):
    """Draw a downward arrow from y_from to y_to."""
    ax.annotate(
        "", xy=(x, y_to), xytext=(x, y_from),
        arrowprops=dict(arrowstyle="-|>", color=_EDGE, lw=1.2),
        annotation_clip=False, zorder=4,
    )


def _right(ax, x_from: float, x_to: float, y: float):
    """Draw a rightward arrow."""
    ax.annotate(
        "", xy=(x_to, y), xytext=(x_from, y),
        arrowprops=dict(arrowstyle="-|>", color=_EDGE, lw=1.2),
        annotation_clip=False, zorder=4,
    )


def _phase_strip(ax, label: str, x: float, y_bot: float, height: float, width: float = 0.45):
    """Draw a vertical phase label strip."""
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y_bot), width, height,
        boxstyle="round,pad=0.01",
        facecolor=_PHASE_FC, edgecolor="#a9bfe0", linewidth=0.8, zorder=1,
    ))
    ax.text(
        x + width / 2, y_bot + height / 2, label,
        ha="center", va="center",
        fontsize=14, fontweight="bold", color=_PHASE_TXT,
        rotation=90, zorder=2,
    )


def _reason_counts(decisions: dict) -> List[tuple[str, int]]:
    """Aggregate real per-reason exclusion counts from a screening/eligibility
    decisions dict (paper_id -> {"decision": "include"|"exclude", "reason": str}).
    Far more precise than an LLM-guessed 2-3 label summary since it's counted
    directly from every paper's actual recorded reason."""
    from collections import Counter
    counts: Counter = Counter()
    for info in (decisions or {}).values():
        if (info.get("decision") or "").strip().lower() != "exclude":
            continue
        reason = (info.get("reason") or "Unspecified").strip()
        reason = f"{reason[:1].upper()}{reason[1:]}" if reason else "Unspecified"
        counts[reason] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def _flat_reason_counts(reasons: dict) -> List[tuple[str, int]]:
    """Same idea as `_reason_counts` but for a plain {id: reason_string} dict
    (e.g. `papers_no_fulltext_reasons`) rather than a decision dict."""
    from collections import Counter
    counts: Counter = Counter()
    for reason in (reasons or {}).values():
        reason = (reason or "Unspecified").strip()
        reason = f"{reason[:1].upper()}{reason[1:]}" if reason else "Unspecified"
        counts[reason] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


_SOURCE_LABELS = {
    "arxiv": "arXiv",
    "semantic_scholar": "Semantic Scholar",
    "crossref": "CrossRef",
    "osf": "OSF",
    "pubmed": "PubMed",
    "deep_research": "AI web search",
}


def _source_breakdown(all_retrieved_papers) -> List[tuple[str, int]]:
    """Per-database record counts for the 'Records identified from:' box,
    tallied from the actual retrieved-paper list rather than guessed."""
    from collections import Counter
    counts: Counter = Counter()
    for paper in all_retrieved_papers or []:
        src = getattr(paper, "source", None) if not isinstance(paper, dict) else paper.get("source")
        src = (src or "unknown").strip().lower()
        counts[_SOURCE_LABELS.get(src, src.replace("_", " ").title())] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def _wrap_item(text: str, suffix: str, width: int, indent: str = "    ") -> List[str]:
    """Word-wrap `text` to `width` chars with a hanging indent, then append
    `suffix` (e.g. "($n$ = 3)") to the last line only -- never split mid-line,
    since a "$n$" mathtext span broken across two Text objects would render
    as broken/unbalanced math.

    Continuation lines are indented to the same width as `indent` but with any
    bullet character blanked out -- otherwise a bullet like "  • " would repeat
    on every wrapped line of the SAME item, making a single wrapped reason read
    as several separate list items."""
    wrapped = textwrap.wrap(text, width=width) or [""]
    blank_indent = " " * len(indent)
    lines = [f"{indent}{wrapped[0]}"]
    lines += [f"{blank_indent}  {w}" for w in wrapped[1:]]
    lines[-1] = f"{lines[-1]} {suffix}"
    return lines


def _side_text(n: int, reason_items: List[tuple[str, int]], label: str, counted: bool,
                width: int = 40) -> str:
    """Build exclusion-box text.

    When `counted` is True, `reason_items` holds real (reason, count) pairs
    tallied directly from the recorded decisions -- each reason is listed with
    its own n, plus a Total line, matching the PRISMA template convention.
    Otherwise `reason_items` holds LLM-guessed reason labels with no reliable
    per-reason count, so they're listed as a plain bullet list under a single
    aggregate (n = ...) header instead.
    """
    if counted and reason_items:
        lines = [f"{label}:"]
        for reason, cnt in reason_items[:6]:
            lines += _wrap_item(reason, f"($n$ = {cnt})", width, indent="  • ")
        lines.append("")
        lines.append(f"    Total ($n$ = {n})")
        return "\n".join(lines)
    text = f"{label}\n($n$ = {n})"
    if reason_items:
        text += "\n\nReasons:"
        for reason, _ in reason_items[:4]:
            text += "\n" + "\n".join(_wrap_item(reason, "", width, indent="  • ")).rstrip()
    return text


def _identified_text(n_identified: int, source_counts: List[tuple[str, int]],
                      width: int = 28) -> str:
    """Build the 'Records identified from:' box text, with a real per-database
    breakdown when available (falls back to a single aggregate line)."""
    if source_counts:
        lines = ["Records identified from:"]
        for src, cnt in source_counts[:6]:
            lines += _wrap_item(src, f"($n$ = {cnt})", width, indent="  • ")
        lines.append("")
        lines.append(f"    Total ($n$ = {n_identified})")
        return "\n".join(lines)
    return f"Records identified from\ndatabases and registers\n($n$ = {n_identified})"


# ── Figure assembly ───────────────────────────────────────────────────────────

def _pdf_path_for(output_path: str) -> str:
    base, ext = os.path.splitext(output_path)
    return output_path if ext.lower() == ".pdf" else f"{base}.pdf"


def _save_figure(fig, output_path: str) -> str:
    save_kwargs = {"bbox_inches": "tight", "facecolor": "white"}
    fig.savefig(output_path, dpi=200, **save_kwargs)
    pdf_path = _pdf_path_for(output_path)
    if pdf_path != output_path:
        fig.savefig(pdf_path, **save_kwargs)
    return output_path

def _write_flow_json(output_path: str, steps: list) -> None:
    """Save the chart's numbers next to it (prisma_flowchart.json) so the web
    UI can show the same counts and reasons without parsing the image.
    Each step is one main box: {"label", "n", optional "items" (breakdown of
    the box itself), optional "note", optional "side": {"kind": "out"|"in",
    "label", "n", "items": [[reason, count|None], ...]}}."""
    import json
    path = os.path.splitext(output_path)[0] + ".json"
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"steps": steps}, fh, indent=1)
    except OSError as exc:
        logger.warning(f"[PRISMA] Could not write {path}: {exc}")


def _items(pairs, counted: bool = True) -> list:
    return [[str(r), (int(n) if counted else None)] for r, n in (pairs or [])]


def _generate_prisma_figure(
    data: dict, output_path: str, plan=None,
    screening_decisions: dict | None = None,
    eligibility_decisions: dict | None = None,
    all_retrieved_papers=None,
    papers_no_fulltext_reasons: dict | None = None,
    synthesis_exclusion_reasons: dict | None = None,
) -> str:
    """Render PRISMA 2020 flowchart and save as PNG plus PDF.

    `synthesis_exclusion_reasons` (paper_id -> reason string) is the same shape
    as `papers_no_fulltext_reasons`, but for papers that passed eligibility yet
    were still lost afterward -- e.g. no quantitative outcome extractable, or no
    convertible statistic for a standardized effect size. Without it, the chart
    can silently understate attrition: "assessed for eligibility" minus
    "excluded at eligibility" won't reconcile with the final "included" count,
    and a reader has no way to see why. When provided, an extra
    "Studies eligible for synthesis" / "Studies excluded" row is drawn between
    the eligibility row and the final included box; when omitted, the chart
    falls back to its previous (potentially non-reconciling) behavior."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    mode         = data.get("input_mode", "search")
    n_identified = max(int(data.get("n_identified", 0)), 0)
    n_duplicates = max(int(data.get("n_duplicates_removed", 0)), 0)
    n_screened   = int(data.get("n_screened", -1))
    n_excl_scr   = int(data.get("n_excluded_screening", -1))
    n_assessed   = int(data.get("n_assessed_eligibility", -1))
    n_excl_elig  = int(data.get("n_excluded_eligibility", -1))
    n_included   = max(int(data.get("n_included", 0)), 0)
    n_effects    = max(int(data.get("n_effect_sizes", 0)), 0)

    # `mode` is deterministic (read straight from pipeline state, never
    # LLM-controlled); `n_screened` comes from the LLM's submit_prisma_data
    # tool call, which is instructed to use -1 only for manual-mode runs but
    # isn't 100% reliable. Don't let an LLM slip silently swap the whole
    # chart layout for a real search-mode run -- if mode says "search" but
    # n_screened came back -1/missing, treat it as "all identified records
    # were screened" instead of falling back to the manual-mode chart.
    if mode == "search" and n_screened < 0:
        logger.warning(
            f"[PRISMA] mode=search but n_screened={n_screened} (LLM likely "
            f"mis-set it) -- defaulting to n_identified={n_identified} instead "
            f"of falling back to the manual-mode chart."
        )
        n_screened = n_identified
    search_mode = (mode == "search")

    # Real per-reason counts straight from the recorded decisions, falling back
    # to the LLM's free-text reason labels (no counts) only when unavailable.
    scr_counted = _reason_counts(screening_decisions or {})
    elig_counted = _reason_counts(eligibility_decisions or {})
    scr_is_counted = bool(scr_counted)
    elig_is_counted = bool(elig_counted)
    scr_items = scr_counted or [(r, 0) for r in data.get("screening_exclusion_reasons", [])]
    elig_items = elig_counted or [(r, 0) for r in data.get("eligibility_exclusion_reasons", [])]

    source_counts = _source_breakdown(all_retrieved_papers)
    not_retrieved_items = _flat_reason_counts(papers_no_fulltext_reasons or {})
    n_not_retrieved = sum(cnt for _, cnt in not_retrieved_items)

    synth_excl_items = _flat_reason_counts(synthesis_exclusion_reasons or {})
    n_excl_synth = sum(cnt for _, cnt in synth_excl_items)

    title = "PRISMA flow diagram"

    if search_mode:
        _draw_search_chart(
            title, n_identified, n_duplicates, source_counts,
            n_screened, n_excl_scr, scr_items, scr_is_counted,
            not_retrieved_items, n_not_retrieved,
            n_assessed, n_excl_elig, elig_items, elig_is_counted,
            synth_excl_items, n_excl_synth,
            n_included, n_effects, output_path,
        )
    else:
        _draw_simple_chart(title, n_identified, n_included, n_effects, mode, output_path)

    logger.info(f"[PRISMA] Flowchart saved: {output_path}")
    return output_path


def _row_layout(row_top: float, main_h: float, side_h: float) -> tuple:
    """Vertically centre a row's main box and side box on one shared line, so
    the horizontal arrow between them meets both boxes at their middle.
    Returns (main_y, side_y, centre_y)."""
    centre = row_top - max(main_h, side_h) / 2
    return centre - main_h / 2, centre - side_h / 2, centre


def _box_h(n_lines: int, line_h: float = 0.34, pad: float = 0.26, min_h: float = 1.1) -> float:
    """Content-driven box height so boxes hug their text instead of a fixed
    generous constant -- this is what actually removes the dead space."""
    return max(min_h, pad * 2 + line_h * (n_lines - 1))


def _draw_search_chart(
    title, n_identified, n_duplicates, source_counts,
    n_screened, n_excl_scr, scr_items, scr_is_counted,
    not_retrieved_items, n_not_retrieved,
    n_assessed, n_excl_elig, elig_items, elig_is_counted,
    synth_excl_items, n_excl_synth,
    n_included, n_effects, output_path,
):
    # Geometry constants -- kept as narrow as the (wrapped) text allows, no
    # more full-width columns. Text is word-wrapped to these widths below, so
    # box height is derived from the real wrapped line count, not guessed.
    # Side (exclusion-reason) boxes are now the same width as the main boxes,
    # and the phase strip is a thin bar rather than a wide column.
    PHASE_W = 0.45
    MX, MW = PHASE_W + 0.15, 4.0   # main column: x start and width
    SX, SW = MX + MW + 0.5, 4.0    # side column: x start and width
    MXC    = MX + MW / 2   # x-centre of main column
    GAP    = 0.45          # vertical gap between stacked rows (room for the arrow)
    BANNER_H = 0.6
    SIDE_WRAP = 26          # side-column text wrap width, chars -- wider columns
    MAIN_WRAP = 26          # main-column text wrap width, chars -- fold to fewer, shorter lines

    def _h(text: str, line_h: float = 0.34) -> float:
        return _box_h(text.count("\n") + 1, line_h=line_h)

    # ── Build every box's text up front so heights reflect real wrapped lines ──
    identified_txt = _identified_text(n_identified, source_counts, width=MAIN_WRAP)
    dup_txt = "\n".join(
        textwrap.wrap("Records removed before screening:", width=SIDE_WRAP)
        + _wrap_item("Duplicate records removed", f"($n$ = {n_duplicates})", SIDE_WRAP)
    )
    screened_txt = f"Records screened\n($n$ = {n_screened})"
    scr_excl_txt = _side_text(max(n_excl_scr, 0), scr_items, "Records excluded",
                               scr_is_counted, width=SIDE_WRAP)

    n_sought = max(n_screened - max(n_excl_scr, 0), 0)
    sought_txt = f"Reports sought\nfor retrieval\n($n$ = {n_sought})"
    not_retr_txt = _side_text(n_not_retrieved, not_retrieved_items, "Reports not retrieved",
                               bool(not_retrieved_items), width=SIDE_WRAP)

    n_assessed_val = (
        n_assessed if n_assessed >= 0
        else max(n_sought - n_not_retrieved, 0)
    )
    assessed_txt = f"Reports assessed\nfor eligibility\n($n$ = {n_assessed_val})"
    elig_excl_txt = _side_text(max(n_excl_elig, 0), elig_items, "Reports excluded",
                                elig_is_counted, width=SIDE_WRAP)

    # Optional extra row: papers that passed eligibility but were still lost
    # afterward (e.g. during data extraction or effect-size computation). Only
    # drawn when the caller actually supplied reasons for that gap -- otherwise
    # the chart falls back to its previous behavior (no row, no reconciliation
    # against n_included).
    has_synth_row = n_excl_synth > 0
    if has_synth_row:
        n_eligible_val = max(n_assessed_val - max(n_excl_elig, 0), 0)
        eligible_txt = f"Studies eligible\nfor synthesis\n($n$ = {n_eligible_val})"
        synth_excl_txt = _side_text(n_excl_synth, synth_excl_items, "Studies excluded",
                                     bool(synth_excl_items), width=SIDE_WRAP)

    effects_label = f"{n_effects} effect size{'s' if n_effects != 1 else ''}"
    included_txt = (f"Studies included\nin synthesis\n$k$ = {n_included} studies"
                     f"\n{effects_label}")

    flow_steps = [
        {"label": "Records identified", "n": n_identified, "items": _items(source_counts),
         "side": {"kind": "out", "label": "Duplicates removed", "n": n_duplicates, "items": []}},
        {"label": "Records screened", "n": n_screened,
         "side": {"kind": "out", "label": "Excluded at title/abstract screening", "n": max(n_excl_scr, 0),
                  "items": _items(scr_items, scr_is_counted)}},
        {"label": "Reports sought for retrieval", "n": n_sought,
         "side": {"kind": "out", "label": "Reports not retrieved", "n": n_not_retrieved,
                  "items": _items(not_retrieved_items)}},
        {"label": "Reports assessed for eligibility", "n": n_assessed_val,
         "side": {"kind": "out", "label": "Excluded at full-text eligibility", "n": max(n_excl_elig, 0),
                  "items": _items(elig_items, elig_is_counted)}},
    ]
    if has_synth_row:
        flow_steps.append(
            {"label": "Studies eligible for synthesis", "n": n_eligible_val,
             "side": {"kind": "out", "label": "Excluded before synthesis", "n": n_excl_synth,
                      "items": _items(synth_excl_items)}})
    flow_steps.append({"label": "Studies included in synthesis", "n": n_included, "note": effects_label,
                       "final": True})
    _write_flow_json(output_path, flow_steps)

    MH   = _h(screened_txt)
    S0_H = _h(identified_txt)
    S1_H = _h(dup_txt)
    S2_H = _h(scr_excl_txt)
    S3_H = _h(not_retr_txt)
    S4_H = _h(elig_excl_txt)
    B5_H = _h(included_txt, line_h=0.36)

    row1_h = max(S0_H, S1_H)
    row2_h = max(MH, S2_H)
    row3_h = max(MH, S3_H)
    row4_h = max(MH, S4_H)

    if has_synth_row:
        S4B_H = _h(synth_excl_txt)
        row4b_h = max(MH, S4B_H)
    else:
        row4b_h = 0.0

    top = (BANNER_H + row1_h + GAP + row2_h + GAP + row3_h + GAP + row4_h + GAP
           + (row4b_h + GAP if has_synth_row else 0.0) + B5_H + 0.7)
    fig_w = SX + SW + 0.5
    fig_h = max(9.0, top * 0.85)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.axis("off")
    ax.set_title(title, fontsize=22, fontweight="bold", pad=14)

    y = top - 0.3  # top margin

    # ── Banner ────────────────────────────────────────────────────────────────
    banner_top = y
    _banner(ax, MX, banner_top - BANNER_H, SX + SW - MX, BANNER_H,
            "Identification of studies via databases and registers")
    y = banner_top - BANNER_H - 0.25

    # ── Row 1: Records identified / Duplicates removed ──────────────────────
    row1_top = y
    B1_Y, S1_Y, c1 = _row_layout(row1_top, S0_H, S1_H)
    _box(ax, MX, B1_Y, MW, S0_H, identified_txt)
    _box(ax, SX, S1_Y, SW, S1_H, dup_txt)
    _right(ax, MX + MW, SX, c1)
    y = row1_top - row1_h - GAP

    # ── Row 2: Records screened / Excluded at screening ─────────────────────
    row2_top = y
    B2_Y, S2_Y, c2 = _row_layout(row2_top, MH, S2_H)
    _box(ax, MX, B2_Y, MW, MH, screened_txt)
    _down(ax, MXC, B1_Y, B2_Y + MH)
    _box(ax, SX, S2_Y, SW, S2_H, scr_excl_txt)
    _right(ax, MX + MW, SX, c2)
    y = row2_top - row2_h - GAP

    # ── Row 3: Reports sought for retrieval / Reports not retrieved ─────────
    row3_top = y
    B3_Y, S3_Y, c3 = _row_layout(row3_top, MH, S3_H)
    _box(ax, MX, B3_Y, MW, MH, sought_txt)
    _down(ax, MXC, B2_Y, B3_Y + MH)
    _box(ax, SX, S3_Y, SW, S3_H, not_retr_txt)
    _right(ax, MX + MW, SX, c3)
    y = row3_top - row3_h - GAP

    # ── Row 4: Assessed for eligibility / Excluded at eligibility ───────────
    row4_top = y
    B4_Y, S4_Y, c4 = _row_layout(row4_top, MH, S4_H)
    _box(ax, MX, B4_Y, MW, MH, assessed_txt)
    _down(ax, MXC, B3_Y, B4_Y + MH)
    _box(ax, SX, S4_Y, SW, S4_H, elig_excl_txt)
    _right(ax, MX + MW, SX, c4)
    y = row4_top - row4_h - GAP

    # ── Row 4b (optional): Eligible for synthesis / Excluded from synthesis ──
    last_box_y = B4_Y
    row_for_screening_bottom = row4_top - row4_h
    if has_synth_row:
        row4b_top = y
        B4B_Y, S4B_Y, c4b = _row_layout(row4b_top, MH, S4B_H)
        _box(ax, MX, B4B_Y, MW, MH, eligible_txt)
        _down(ax, MXC, B4_Y, B4B_Y + MH)
        _box(ax, SX, S4B_Y, SW, S4B_H, synth_excl_txt)
        _right(ax, MX + MW, SX, c4b)
        y = row4b_top - row4b_h - GAP
        last_box_y = B4B_Y
        row_for_screening_bottom = row4b_top - row4b_h

    # ── Row 5: Studies included ──────────────────────────────────────────────
    row5_top = y
    B5_Y = row5_top - B5_H
    _box(ax, MX, B5_Y, MW, B5_H, included_txt, fontsize=15)
    _down(ax, MXC, last_box_y, row5_top)

    bottom = B5_Y - 0.3
    ax.set_ylim(bottom, top)

    # Matches the official PRISMA template's 3-way grouping: Screening covers
    # everything from "Records screened" through "Reports assessed for
    # eligibility" (and the optional synthesis-attrition row) as one continuous
    # phase, not a separate Eligibility strip.
    screening_bottom = row_for_screening_bottom
    _phase_strip(ax, "Identification", 0.0, row1_top - row1_h, row1_h + BANNER_H + 0.25)
    _phase_strip(ax, "Screening",      0.0, screening_bottom,
                 (row2_top - screening_bottom))
    _phase_strip(ax, "Included",       0.0, bottom,            row5_top - bottom)

    plt.tight_layout()
    _save_figure(fig, output_path)
    plt.close(fig)


def _draw_simple_chart(title, n_identified, n_included, n_effects, mode, output_path):
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title(title, fontsize=22, fontweight="bold", pad=14)

    MX, MW = 0.8, 5.5
    MXC = MX + MW / 2
    mode_label = "PDF files uploaded manually" if mode == "manual" else "records identified"
    _write_flow_json(output_path, [
        {"label": f"Papers provided ({mode_label})", "n": n_identified},
        {"label": "Studies included in synthesis", "n": n_included,
         "note": f"{n_effects} effect size{'s' if n_effects != 1 else ''}", "final": True},
    ])

    _phase_strip(ax, "Identification", 0.0, 4.2, 2.3)
    _box(ax, MX, 4.5, MW, 1.4,
         f"Papers provided ({mode_label})\n($n$ = {n_identified})")

    _phase_strip(ax, "Included", 0.0, 1.0, 3.0)
    effects_label = f"{n_effects} effect size{'s' if n_effects != 1 else ''}"
    _box(ax, MX, 1.3, MW, 1.8,
         f"Studies included in synthesis\n$k$ = {n_included} studies"
         f"\n{effects_label}", fontsize=15)

    _down(ax, MXC, 4.5, 1.3 + 1.8)

    plt.tight_layout()
    _save_figure(fig, output_path)
    plt.close(fig)


# ── Agent node ────────────────────────────────────────────────────────────────

_agent = create_react_agent(llm, [submit_prisma_data], prompt=SYSTEM_PROMPT)


def prisma_node(state: GraphState) -> dict:
    """Stage 10: generate PRISMA 2020 flowchart from pipeline counts."""
    logger.info("=== STAGE 10: PRISMA Flowchart ===")

    output_dir  = state["output_dir"]
    mode        = state.get("mode", "search")
    plan        = state.get("plan")
    papers      = state.get("papers_eligible", [])
    effects     = state.get("effect_sizes", [])

    n_identified = state.get("n_search_retrieved", len(papers))
    n_duplicates = state.get("n_duplicates_removed", 0)
    n_scr_excl   = state.get("n_screened_excluded", -1 if mode != "search" else 0)
    n_elig_excl  = state.get("n_eligibility_excluded", -1 if mode != "search" else 0)

    plan_info = ""
    if plan:
        plan_info = (
            f"Research question: {plan.research_question}\n"
            f"Inclusion criteria: {'; '.join(plan.inclusion_criteria)}\n"
            f"Exclusion criteria: {'; '.join(plan.exclusion_criteria)}\n"
        )

    summary = (
        f"Pipeline mode: {mode}\n"
        f"{plan_info}"
        f"\nStage counts:\n"
        f"  n_search_retrieved (identified, after dedup): {n_identified}\n"
        f"  n_duplicates_removed (merged by the search node's dedup index): {n_duplicates}\n"
        f"  n_screened_excluded (excluded at title/abstract): {n_scr_excl}"
        f"{'  (-1 = screening not run)' if n_scr_excl == -1 else ''}\n"
        f"  n_eligibility_excluded (excluded at full-text): {n_elig_excl}"
        f"{'  (-1 = eligibility not run)' if n_elig_excl == -1 else ''}\n"
        f"  n_included (passed all filters): {len(papers)}\n"
        f"  n_effect_sizes: {len(effects)}\n"
    )

    logger.info(
        f"[PRISMA] mode={mode} n_identified={n_identified} "
        f"n_duplicates={n_duplicates} "
        f"n_scr_excl={n_scr_excl} n_elig_excl={n_elig_excl} "
        f"n_included={len(papers)} n_effects={len(effects)}"
    )

    result = _agent.invoke({"messages": [("user",
        "Generate PRISMA 2020 flowchart data from the pipeline summary below.\n\n"
        f"{summary}\n\n"
        "Call `submit_prisma_data` once with all counts filled in."
    )]})

    args = _extract_tool_args(result["messages"], "submit_prisma_data")
    if not args:
        logger.warning("[PRISMA] LLM did not call submit_prisma_data — using raw counts.")
        args = {
            "n_identified":                  n_identified,
            "n_duplicates_removed":          n_duplicates,
            "n_screened":                    n_identified if mode == "search" else -1,
            "n_excluded_screening":          n_scr_excl,
            "screening_exclusion_reasons":   [],
            "n_assessed_eligibility":        -1,
            "n_excluded_eligibility":        n_elig_excl,
            "eligibility_exclusion_reasons": [],
            "n_included":                    len(papers),
            "n_effect_sizes":                len(effects),
        }

    args["input_mode"] = mode
    # n_duplicates_removed is a deterministic pipeline count (see search_node's
    # _CandidateIndex merge counter) -- always override whatever the LLM
    # returned rather than trust it to copy the summary value correctly, same
    # rationale as the input_mode override above.
    args["n_duplicates_removed"] = n_duplicates
    output_path = os.path.join(output_dir, "prisma_flowchart.png")

    try:
        _generate_prisma_figure(
            args, output_path, plan=plan,
            screening_decisions=state.get("screening_decisions", {}),
            eligibility_decisions=state.get("eligibility_decisions", {}),
            all_retrieved_papers=state.get("all_retrieved_papers", []),
            papers_no_fulltext_reasons=state.get("papers_no_fulltext_reasons", {}),
        )
    except Exception as exc:
        logger.error(f"[PRISMA] Chart generation failed: {exc}", exc_info=True)
        return {"errors": state.get("errors", []) + [f"PRISMA chart: {exc}"]}

    return {"prisma_flowchart_path": output_path}
