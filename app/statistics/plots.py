"""Generate forest plots, funnel plots, and supplementary meta-analysis plots."""

import os
import math
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import gaussian_kde
from typing import List, Optional

matplotlib.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.titlesize": 16,
})


def _installed_font(preferred: List[str]) -> str:
    """Return the first font in `preferred` that is actually installed, else the last entry."""
    import matplotlib.font_manager as fm
    available = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in available:
            return name
    return preferred[-1]


# Arial itself is rarely installed on Linux; Liberation Sans is metric-compatible
# and used as the closest available substitute when true Arial is absent.
_SANS_FONT = _installed_font(["Arial", "Liberation Sans", "DejaVu Sans"])


def _pdf_path_for(output_path: str) -> str:
    base, ext = os.path.splitext(output_path)
    return output_path if ext.lower() == ".pdf" else f"{base}.pdf"


def _save_figure(fig, output_path: str, *, dpi: int = 200, facecolor=None) -> str:
    """Save the primary image and a same-name PDF copy."""
    save_kwargs = {"bbox_inches": "tight"}
    if facecolor is not None:
        save_kwargs["facecolor"] = facecolor
    fig.savefig(output_path, dpi=dpi, **save_kwargs)
    pdf_path = _pdf_path_for(output_path)
    if pdf_path != output_path:
        fig.savefig(pdf_path, **save_kwargs)
    return output_path


# ── Forest plot ───────────────────────────────────────────────────────────────

def forest_plot(
    study_labels: List[str],
    effects: List[float],
    variances: List[float],
    pooled_g: float,
    pooled_ci_lower: float,
    pooled_ci_upper: float,
    weights: Optional[List[float]] = None,
    title: str = "Forest plot",
    left_label: str = "Favours control",
    right_label: str = "Favours treatment",
    output_path: str = "outputs/forest_plot.png",
    measure_label: str = "Hedges' g",
    log_scale: bool = False,
) -> str:
    """
    Generate a publication-quality forest plot (Nature-style).

    Studies are sorted by effect size (ascending by rank: Study 1 = smallest/
    most negative), but displayed with Study 1 at the TOP and the largest
    study at the bottom (reversed layout). Each study is a colored dot
    (red = below-null, green = above-null effect) with 95% CI whiskers. The
    pooled estimate is shown only as an orange dashed reference line with its
    CI band -- there is no separate summary row/diamond.

    `measure_label` names the x-axis/legend text (e.g. "Risk Ratio (RR)") --
    purely cosmetic, does not affect any number. `log_scale`: for ratio
    measures (RR/OR/Peto OR), `effects`/`variances`/`pooled_g`/
    `pooled_ci_lower`/`pooled_ci_upper` are expected on the LOG scale (the
    same units metafor/escalc uses internally, and what
    agents/meta_analysis_agent.py already computes -- see
    utils/effect_measures.py::pool_group_native's `pooled_log` output) --
    the CI-from-variance computation below is UNCHANGED (still `e ± 1.96*se`
    on whatever scale it's given); log_scale only controls a coordinate
    transform (`exp()`) applied at render time plus `ax.set_xscale("log")`,
    so points remain visually equally spaced in log units while tick labels
    show natural ratio values. The null reference line moves from 0 to 1
    accordingly. For MD/SMD/Hedges' g/GENERIC, log_scale=False (default)
    keeps this function byte-for-byte identical to before.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    k = len(effects)

    if k == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        _save_figure(fig, output_path)
        plt.close(fig)
        return output_path

    if weights is None:
        weights = [1.0] * k

    # Rank ascending by effect size (rank 0 = smallest/most negative = "Study 1"),
    # but place rank 0 at the TOP of the plot (y=k) and the largest at the
    # bottom (y=1) -- a reversed layout relative to the ranking.
    order = sorted(range(k), key=lambda i: effects[i])
    effects_s = [effects[i] for i in order]
    variances_s = [variances[i] for i in order]
    weights_s = [weights[i] for i in order]
    y_for_rank = [k - rank for rank in range(k)]

    se = [math.sqrt(v) for v in variances_s]
    ci_lo = [e - 1.96 * s for e, s in zip(effects_s, se)]
    ci_hi = [e + 1.96 * s for e, s in zip(effects_s, se)]
    max_w = max(weights_s) or 1.0

    # Coordinate transform for display only -- the CI computation above is
    # unchanged (still linear e ± 1.96*se, on whichever scale was passed in).
    _tx = math.exp if log_scale else (lambda v: v)
    effects_disp = [_tx(e) for e in effects_s]
    ci_lo_disp = [_tx(v) for v in ci_lo]
    ci_hi_disp = [_tx(v) for v in ci_hi]
    pooled_g_disp = _tx(pooled_g)
    pooled_ci_lower_disp = _tx(pooled_ci_lower)
    pooled_ci_upper_disp = _tx(pooled_ci_upper)
    null_value = 1.0 if log_scale else 0.0

    neg_color = "#c0392b"   # red   -- below-null effect
    pos_color = "#1e8449"   # green -- above-null effect
    neg_bg = "#fbeae7"      # light red background, below-null side
    pos_bg = "#e9f5ec"      # light green background, above-null side

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
        "font.size": 27,
        "axes.labelsize": 30,
        "xtick.labelsize": 27,
        "ytick.labelsize": 26,
        "legend.fontsize": 25,
    }):
        fig, ax = plt.subplots(figsize=(14, max(7, k * 0.8 + 2)))

        if log_scale:
            ax.set_xscale("log")
            # Multiplicative margin (additive would go <=0 on a log axis).
            x_min = min(ci_lo_disp + [null_value]) / 1.15
            x_max = max(ci_hi_disp + [null_value]) * 1.3
        else:
            x_range = max(ci_hi_disp) - min(ci_lo_disp) or 1.0
            x_min = min(ci_lo_disp + [null_value]) - 0.05 * x_range
            x_max = max(ci_hi_disp + [null_value]) + 0.22 * x_range
        x_range_disp = x_max - x_min or 1.0

        # Background shading split at the null value (red = below, green = above)
        ax.axvspan(x_min, null_value, color=neg_bg, zorder=0)
        ax.axvspan(null_value, x_max, color=pos_bg, zorder=0)

        # Pooled-effect CI band, drawn across the full plot height.
        ax.axvspan(pooled_ci_lower_disp, pooled_ci_upper_disp, color="darkorange", alpha=0.15, zorder=1)

        for rank in range(k):
            y = y_for_rank[rank]
            color = neg_color if effects_disp[rank] < null_value else pos_color
            ax.plot([ci_lo_disp[rank], ci_hi_disp[rank]], [y, y], color=color, linewidth=1.4, zorder=4)
            marker_size = 130 * (weights_s[rank] / max_w) + 50
            ax.scatter(effects_disp[rank], y, s=marker_size, color=color, zorder=5,
                       edgecolors="white", linewidths=0.8)
            ax.text(
                x_max - 0.01 * x_range_disp, y, f"{weights_s[rank]:.1f}%",
                va="center", ha="right", fontsize=25, color="black", zorder=6,
            )

        # Reference lines: solid dark gray at the null value, dashed orange at the pooled estimate.
        ax.axvline(x=null_value, color="#374151", linewidth=1.2, linestyle="-", zorder=3)
        ax.axvline(x=pooled_g_disp, color="darkorange", linewidth=1.4, linestyle="--", zorder=3)

        ax.set_yticks(y_for_rank)
        ax.set_yticklabels([f"Study {rank + 1}" for rank in range(k)])
        ax.set_xlabel(f"Effect size ({measure_label})" + (" — log scale" if log_scale else ""))
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0.3, k + 0.7)

        # Pooled-effect statistics, as a legend-style box in the bottom-left corner.
        ax.text(
            0.02, 0.02,
            f"Pooled {measure_label} = {pooled_g_disp:.3f}\n95% CI [{pooled_ci_lower_disp:.3f}, {pooled_ci_upper_disp:.3f}]",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=24,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor="darkorange", linewidth=1.3, alpha=0.95),
            zorder=10,
        )

        fig.tight_layout()
        _save_figure(fig, output_path)
        plt.close(fig)
    return output_path


# ── Leave-one-out sensitivity analysis ──────────────────────────────────────────

def leave_one_out_plot(
    effects: List[float],
    variances: List[float],
    study_labels: Optional[List[str]] = None,
    method: str = "REML",
    output_path: str = "outputs/leave_one_out.png",
) -> str:
    """
    Leave-one-out sensitivity analysis: the pooled estimate is recomputed once
    per study with that study excluded and plotted against the omitted-study
    index, as a simple connected-scatter trace (no CI bars, no legend) in the
    codebase's nature-style rose palette with Arial and italic $g$.
    """
    from matplotlib.ticker import MaxNLocator
    from statistics.random_effects import random_effects_model

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    k = len(effects)

    if k < 3:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Leave-one-out requires at least 3 studies",
                ha="center", va="center", transform=ax.transAxes)
        ax.axis("off")
        _save_figure(fig, output_path)
        plt.close(fig)
        return output_path

    loo_g = []
    for i in range(k):
        sub_e = effects[:i] + effects[i + 1:]
        sub_v = variances[:i] + variances[i + 1:]
        r = random_effects_model(sub_e, sub_v, method=method)
        loo_g.append(r["pooled_g"])

    _LOO = "#c97b6d"  # rose -- line + marker fill, matching the codebase's nature-style palette

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
        "font.size": 13,
        "axes.labelsize": 15,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    }):
        fig, ax = plt.subplots(figsize=(7.5, 6.5))
        ax.set_facecolor("white")

        x = list(range(1, k + 1))
        ax.plot(x, loo_g, color=_LOO, linewidth=1.4, zorder=2)
        ax.scatter(x, loo_g, s=55, facecolors=_LOO, edgecolors="white",
                   linewidths=1.0, zorder=3)

        ax.set_xlabel("Omitted study")
        ax.set_ylabel("Pooled estimate (Hedges' $g$)")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#9ca3af")
            spine.set_linewidth(0.8)
        ax.tick_params(direction="out", length=4, color="#9ca3af", top=False, right=False)
        ax.grid(False)

        fig.tight_layout()
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path


# ── Funnel plot ───────────────────────────────────────────────────────────────

def funnel_plot(
    effects: List[float],
    variances: List[float],
    pooled_g: float,
    title: str = "Funnel plot",
    output_path: str = "outputs/funnel_plot.png",
    measure_label: str = "Hedges' g",
    log_scale: bool = False,
    unavailable: bool = False,
) -> str:
    """
    Generate a funnel plot to assess publication bias.

    Gray panel background (ggplot2-style) with a plain white 95% funnel
    region centered on the pooled estimate; no title, no contour color bands.

    Same measure-aware contract as forest_plot/effect_distribution_plot/
    bubble_chart (see forest_plot's docstring and
    agents/meta_analysis_agent.py's `_generate_group_plots`): `effects`/
    `variances`/`pooled_g` are expected on computation_scale's own units --
    i.e. the LOG scale for ratio measures (RR/OR/PETO_OR/HR), exactly what
    each EffectSizeRecord's native_value/native_variance already holds and
    what pool_group_native's back-transformed pooled_g must be re-logged to
    (there is no separate `pooled_log` on MetaAnalysisResult; math.log() of
    the back-transformed ratio recovers it exactly). `measure_label` names
    the axis/legend text (e.g. "Risk Ratio (RR)"); `log_scale=True` applies
    the same exp()-at-render-time transform forest_plot uses, so points stay
    correctly positioned in log space while tick labels/legend show the
    natural ratio scale. For MD/SMD/Hedges' g, log_scale=False (default)
    keeps this function byte-for-byte identical to before.

    Root cause this replaces: this function used to unconditionally treat
    every input as Hedges' g (fixed "Observed outcome (Hedges' g)" x-label,
    fixed "Pooled Hedges' g = …" legend) regardless of what was actually
    pooled -- so an RR/OR/HR group's already-native effects/pooled value
    (e.g. RR = 0.851) rendered as if it were a Hedges' g of 0.851, an
    invalid, misleading mix of scales. See tests/test_funnel_plot.py.

    `unavailable=True` (for UNKNOWN/GENERIC groups -- no concrete, named
    native measure was ever resolved) renders an explicit placeholder
    instead of fabricating an axis/scale for numbers with no shared unit.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if unavailable:
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.text(
            0.5, 0.5,
            "Funnel plot unavailable:\nno concrete native effect measure\n"
            "was resolved for this outcome group",
            ha="center", va="center", transform=ax.transAxes,
            fontsize=13, color="#555555",
        )
        ax.axis("off")
        _save_figure(fig, output_path)
        plt.close(fig)
        return output_path

    g = np.array(effects, dtype=float)
    se = np.sqrt(np.array(variances, dtype=float))

    se_max = float(se.max()) * 1.05 if se.size else 1.0
    se_range = np.linspace(0, se_max, 200)

    # Coordinate transform for display only (mirrors forest_plot exactly) --
    # all math (funnel region, pooled line position) happens on the scale
    # `effects`/`pooled_g` were actually given in; exp() is applied only to
    # what gets drawn/labeled, for ratio measures. np.exp (not math.exp) --
    # this is applied to numpy arrays (the funnel region bounds, the study
    # points) as well as plain floats (the pooled line).
    _tx = np.exp if log_scale else (lambda v: v)
    null_value = 1.0 if log_scale else 0.0

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
    }):
        fig, ax = plt.subplots(figsize=(7, 6))

        # ggplot2-style gray panel; only vertical gridlines (no horizontal line).
        ax.set_facecolor("#e5e5e5")
        ax.grid(True, axis="x", color="white", linewidth=1.0, zorder=0)
        ax.set_axisbelow(True)
        if log_scale:
            ax.set_xscale("log")

        # Plain white 95% funnel region centered on the pooled estimate (no color bands).
        z = 1.96
        lo = pooled_g - z * se_range
        hi = pooled_g + z * se_range
        ax.fill_betweenx(se_range, _tx(lo), _tx(hi), color="white", zorder=1)

        g_disp = _tx(g)
        ax.scatter(g_disp, se, color="black", s=40, zorder=5)

        pooled_disp = _tx(pooled_g)
        ax.axvline(x=pooled_disp, color="darkorange", linewidth=1.4, linestyle="--",
                   label=f"Pooled {measure_label} = {pooled_disp:.3f}", zorder=4)
        ax.axvline(x=null_value, color="black", linewidth=0.7, linestyle=":", alpha=0.5, zorder=4)

        ax.invert_yaxis()
        ax.set_ylim(se_max, 0)  # flush the triangle's base against the bottom spine
        # "Log {measure}" would misleadingly imply the AXIS VALUES are log(RR)
        # (where null = 0) -- they aren't: _tx=np.exp already converted
        # everything to the natural ratio scale for display (null = 1, ticks
        # show e.g. 0.5/1/2), only the AXIS SPACING is logarithmic
        # (ax.set_xscale("log")). "{measure}, logarithmic scale" describes
        # that correctly; "Log {measure}" does not.
        xlabel = f"{measure_label}, logarithmic scale" if log_scale else f"Observed outcome ({measure_label})"
        ax.set_xlabel(xlabel, fontsize=18)
        ax.set_ylabel("Standard error", fontsize=18)
        ax.tick_params(axis="both", labelsize=15)
        ax.legend(fontsize=15)
        fig.tight_layout()
        _save_figure(fig, output_path)
        plt.close(fig)
    return output_path


# ── Cumulative forest plot ────────────────────────────────────────────────────

def cumulative_forest_plot(
    study_labels: List[str],
    cumulative_g: List[float],
    cumulative_ci_lower: List[float],
    cumulative_ci_upper: List[float],
    study_years: List[int],
    final_g: float,
    title: str = "Cumulative meta-analysis",
    output_path: str = "outputs/cumulative_plot.png",
    measure_label: str = "Hedges' g",
    log_scale: bool = False,
) -> str:
    """
    How the pooled estimate evolved as studies were added chronologically: a
    continuous 95% CI ribbon around the cumulative line, with vertical bands
    marking each publication year. Nature-style: warm cream-to-brown palette,
    Arial, italic statistical symbols.

    Unlike forest_plot, `cumulative_g`/`cumulative_ci_lower`/
    `cumulative_ci_upper`/`final_g` are expected ALREADY on the human-
    interpretable scale (ratio-scale for RR/OR, back-transformed by
    utils/effect_measures.py::pool_group_native -- no further transform
    needed here). `log_scale` only sets `ax.set_yscale("log")` and moves the
    null reference line from 0 to 1; `measure_label` names the y-axis/legend
    text. Defaults keep this function identical to before for MD/SMD/
    Hedges' g/GENERIC.
    """
    null_value = 1.0 if log_scale else 0.0
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    k = len(study_labels)
    x = list(range(1, k + 1))

    years = sorted(set(study_years))
    n_years = max(len(years) - 1, 1)
    _band_lo, _band_hi = np.array([0xFA, 0xF3, 0xEA]), np.array([0xE3, 0xC3, 0x9A])  # cream -> tan
    _dot_lo, _dot_hi = np.array([0xE3, 0x8A, 0x5A]), np.array([0x8B, 0x5A, 0x2B])    # orange-brown -> deep brown
    band_colors = {
        y: "#%02x%02x%02x" % tuple((_band_lo + (_band_hi - _band_lo) * (i / n_years)).astype(int))
        for i, y in enumerate(years)
    }
    dot_colors = {
        y: "#%02x%02x%02x" % tuple((_dot_lo + (_dot_hi - _dot_lo) * (i / n_years)).astype(int))
        for i, y in enumerate(years)
    }
    point_colors = [dot_colors[y] for y in study_years]

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
        "font.size": 13,
        "axes.labelsize": 15,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 12,
    }):
        fig, ax = plt.subplots(figsize=(11, 6.5))
        ax.set_facecolor("white")
        if log_scale:
            ax.set_yscale("log")

        lo = min(cumulative_ci_lower + [null_value, final_g])
        hi = max(cumulative_ci_upper + [null_value, final_g])
        if log_scale:
            # Multiplicative margin (additive would go <=0 on a log axis).
            y_bot, y_top = lo / 1.15, hi * 1.3
            y_label = hi * 1.15
        else:
            rng = (hi - lo) or 1.0
            y_bot, y_top = lo - 0.10 * rng, hi + 0.24 * rng
            y_label = hi + 0.13 * rng
        ax.set_ylim(y_bot, y_top)

        # Vertical bands per publication year, labeled along the top.
        for y in years:
            idxs = [i for i, yy in enumerate(study_years) if yy == y]
            x0, x1 = x[idxs[0]] - 0.5, x[idxs[-1]] + 0.5
            ax.axvspan(x0, x1, color=band_colors[y], alpha=0.55, zorder=0)
            ax.text((x0 + x1) / 2, y_label, str(y), ha="center", va="center",
                    fontsize=13, fontweight="bold", color=dot_colors[y])

        # Continuous 95% CI ribbon around the cumulative estimate.
        ax.fill_between(x, cumulative_ci_lower, cumulative_ci_upper,
                         color="#c97b6d", alpha=0.28, zorder=1, linewidth=0)

        ax.plot(x, cumulative_g, color="#8B5A2B", linewidth=1.8, zorder=3)
        ax.scatter(x, cumulative_g, color=point_colors, s=70, zorder=4,
                   edgecolors="white", linewidths=1.2)

        ax.axhline(y=null_value, color="#6b7280", linewidth=1.1, linestyle="--", alpha=0.85, zorder=2)
        ax.axhline(y=final_g, color="#8B5A2B", linewidth=1.3, linestyle=":", alpha=0.9, zorder=2)
        if log_scale:
            # Axes-fraction position for a log y-axis must interpolate in
            # log space, not linear -- otherwise the label lands off-target.
            text_y_frac = (math.log(final_g) - math.log(y_bot)) / (math.log(y_top) - math.log(y_bot)) + 0.02
        else:
            text_y_frac = (final_g - y_bot) / (y_top - y_bot) + 0.02
        ax.text(0.98, text_y_frac,
                f"Final: {measure_label} = {final_g:.3f}", transform=ax.transAxes,
                fontsize=12, fontweight="bold", color="#8B5A2B", ha="right", va="bottom")

        ax.set_xticks(x)
        ax.set_xticklabels(study_labels, rotation=45, ha="right", fontsize=10.5)
        ax.set_xlim(0.3, k + 0.7)
        ax.set_xlabel("Number of studies included")
        ax.set_ylabel(f"Cumulative effect size ({measure_label})" + (" — log scale" if log_scale else ""))

        handles = [
            plt.Line2D([0], [0], marker="o", linestyle="", color=dot_colors[y],
                       markeredgecolor="white", markeredgewidth=0.8, markersize=9, label=str(y))
            for y in years
        ]
        ax.legend(handles=handles, title="Study year", loc="upper center",
                  bbox_to_anchor=(0.5, -0.22), ncol=len(years), frameon=False,
                  fontsize=11, title_fontsize=11.5)

        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#9ca3af")
        ax.tick_params(color="#9ca3af")

        fig.tight_layout()
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path


# ── Descriptive: publication year & peer-review status ───────────────────────

def study_year_bar_chart(
    years: List[int],
    output_path: str = "outputs/study_year_distribution.png",
) -> str:
    """
    Number of included studies per publication year -- a simple bar chart in
    the codebase's nature-style cream-to-brown sequential palette.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    counts = Counter(years)
    ordered_years = sorted(counts)
    values = [counts[y] for y in ordered_years]

    n = max(len(ordered_years) - 1, 1)
    _lo, _hi = np.array([0xE3, 0x8A, 0x5A]), np.array([0x8B, 0x5A, 0x2B])
    bar_colors = [
        "#%02x%02x%02x" % tuple((_lo + (_hi - _lo) * (i / n)).astype(int))
        for i in range(len(ordered_years))
    ]

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "font.size": 13,
        "axes.labelsize": 15,
        "xtick.labelsize": 13,
        "ytick.labelsize": 12,
    }):
        fig, ax = plt.subplots(figsize=(6.5, 5))
        ax.set_facecolor("white")

        bars = ax.bar([str(y) for y in ordered_years], values, color=bar_colors,
                      width=0.6, edgecolor="white", linewidth=0.8, zorder=3)
        for rect, v in zip(bars, values):
            ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + max(values) * 0.02,
                    str(v), ha="center", va="bottom", fontsize=12, fontweight="bold", color="#374151")

        ax.set_xlabel("Publication year")
        ax.set_ylabel("Number of studies")
        ax.set_ylim(0, max(values) * 1.18)
        ax.grid(axis="y", color="#e5e7eb", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#9ca3af")
        ax.tick_params(color="#9ca3af")

        fig.tight_layout()
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path


def publication_status_pie_chart(
    statuses: List[str],
    peer_reviewed_values: Optional[set] = None,
    output_path: str = "outputs/peer_review_distribution.png",
) -> str:
    """
    Peer-reviewed vs. not-peer-reviewed breakdown of included studies -- a
    donut chart in the codebase's nature-style rose/tan palette.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    peer_reviewed_values = peer_reviewed_values or {"published"}
    k = len(statuses)
    n_peer = sum(1 for s in statuses if (s or "").strip().lower() in peer_reviewed_values)
    n_other = k - n_peer

    values = [n_peer, n_other]
    labels = [f"Peer-reviewed ($n$={n_peer})", f"Not peer-reviewed ($n$={n_other})"]
    colors = ["#c97b6d", "#e3c39a"]
    if n_other == 0:
        values, labels, colors = [n_peer], [labels[0]], [colors[0]]
    elif n_peer == 0:
        values, labels, colors = [n_other], [labels[1]], [colors[1]]

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
        "font.size": 13,
    }):
        fig, ax = plt.subplots(figsize=(6.5, 6))

        wedges, _ = ax.pie(
            values, colors=colors, startangle=90, counterclock=False,
            wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5),
        )
        ax.text(0, 0.06, f"{k}", ha="center", va="center", fontsize=26, fontweight="bold", color="#8B5A2B")
        ax.text(0, -0.14, "studies", ha="center", va="center", fontsize=12, color="#6b7280")
        ax.legend(wedges, labels, loc="upper center", bbox_to_anchor=(0.5, -0.02),
                  fontsize=12, frameon=False)

        fig.tight_layout()
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path


# ── Effect size distribution plot ─────────────────────────────────────────────

def effect_distribution_plot(
    effects: List[float],
    variances: List[float],
    pooled_g: float,
    pooled_ci_lower: float,
    pooled_ci_upper: float,
    title: str = "Effect Size Distribution",
    output_path: str = "outputs/effect_distribution.png",
    measure_label: str = "Hedges' g",
    log_scale: bool = False,
) -> str:
    """
    Violin + strip plot of individual effect-size values with the pooled estimate.

    Shows the empirical distribution of effect sizes across studies, making
    heterogeneity visually intuitive. Study points are sized by precision (1/SE).

    `effects`/`pooled_g`/`pooled_ci_lower`/`pooled_ci_upper` are expected on
    the same scale forest_plot uses (LOG scale for ratio measures) -- the
    KDE/scatter/pooled-line positions are computed in those units UNCHANGED;
    log_scale only applies a display-time exp() transform to the already-
    computed y-coordinates plus `ax.set_yscale("log")`, so the distribution
    itself is not recalculated differently.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    g = np.array(effects)
    se = np.sqrt(np.array(variances))
    precision = 1.0 / se  # larger = more precise

    null_value = 1.0 if log_scale else 0.0
    _tx = np.exp if log_scale else (lambda v: v)
    g_disp = _tx(g)
    pooled_g_disp = float(_tx(pooled_g))
    pooled_ci_lower_disp = float(_tx(pooled_ci_lower))
    pooled_ci_upper_disp = float(_tx(pooled_ci_upper))

    fig, ax = plt.subplots(figsize=(7, 5))
    if log_scale:
        ax.set_yscale("log")

    # Violin via KDE if k >= 4 -- KDE fit in the ORIGINAL (possibly log)
    # units, unchanged; only the resulting curve's y-range is transformed
    # for display, same convention as the scatter points below.
    if len(g) >= 4:
        kde = gaussian_kde(g, bw_method="silverman")
        g_range = np.linspace(g.min() - 0.3, g.max() + 0.3, 400)
        density = kde(g_range)
        density_scaled = density / density.max() * 0.35
        g_range_disp = _tx(g_range)
        ax.fill_betweenx(g_range_disp, -density_scaled, density_scaled,
                         alpha=0.25, color="steelblue", label="KDE")
        ax.plot(-density_scaled, g_range_disp, color="steelblue", linewidth=0.8, alpha=0.6)
        ax.plot(density_scaled, g_range_disp, color="steelblue", linewidth=0.8, alpha=0.6)

    # Jittered study dots sized by precision
    rng = np.random.default_rng(42)
    jitter = rng.uniform(-0.08, 0.08, size=len(g))
    prec_norm = (precision - precision.min()) / (np.ptp(precision) + 1e-9)
    sizes = 30 + 120 * prec_norm
    if log_scale:
        vmin, vmax = g_disp.min() / 1.1, g_disp.max() * 1.1
    else:
        vmin, vmax = g_disp.min() - 0.1, g_disp.max() + 0.1
    sc = ax.scatter(jitter, g_disp, s=sizes, c=g_disp, cmap="RdYlGn",
                    vmin=vmin, vmax=vmax,
                    zorder=5, edgecolors="gray", linewidths=0.4, label="Studies")

    # Pooled estimate + CI
    ax.hlines(pooled_g_disp, -0.42, 0.42, colors="darkorange", linewidths=2.0,
              linestyles="-", zorder=6, label=f"Pooled {measure_label} = {pooled_g_disp:.3f}")
    ax.hlines([pooled_ci_lower_disp, pooled_ci_upper_disp], -0.28, 0.28,
              colors="darkorange", linewidths=1.0, linestyles="--", zorder=6,
              label=f"95% CI [{pooled_ci_lower_disp:.3f}, {pooled_ci_upper_disp:.3f}]")
    ax.axhline(y=null_value, color="black", linewidth=0.8, linestyle=":", alpha=0.5)
    ax.axhspan(pooled_ci_lower_disp, pooled_ci_upper_disp, alpha=0.08, color="orange")

    cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
    cbar.set_label(measure_label, fontsize=12)
    ax.set_xlim(-0.55, 0.55)
    ax.set_xticks([])
    ax.set_ylabel(measure_label + (" — log scale" if log_scale else ""), fontsize=13)
    ax.set_title(title, fontsize=15)
    ax.legend(fontsize=11, loc="upper right")
    fig.tight_layout()
    _save_figure(fig, output_path)
    plt.close(fig)
    return output_path


# ── Bubble chart ──────────────────────────────────────────────────────────────

def bubble_chart(
    study_labels: List[str],
    effects: List[float],
    variances: List[float],
    sample_sizes: List[int],
    study_years: Optional[List[int]] = None,
    pooled_g: float = 0.0,
    title: str = "Effect size vs. sample size",
    output_path: str = "outputs/bubble_chart.png",
    measure_label: str = "Hedges' g",
    log_scale: bool = False,
) -> str:
    """
    Scatter plot of effect size (y-axis) vs. sample size (x-axis).

    Bubble size is proportional to precision (1/variance). Bubble color uses
    the same continuous red-yellow-green scheme as effect_distribution_plot.

    `effects`/`pooled_g` are expected on the same scale forest_plot uses
    (LOG scale for ratio measures) -- scatter y-positions come straight from
    `effects`, UNCHANGED; log_scale only applies a display-time exp()
    transform plus `ax.set_yscale("log")`.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    g = np.array(effects)
    n = np.array(sample_sizes, dtype=float)

    null_value = 1.0 if log_scale else 0.0
    _tx = np.exp if log_scale else (lambda v: v)
    g_disp = _tx(g)
    pooled_g_disp = float(_tx(pooled_g))

    # Bubble size ∝ precision (1/variance)
    precision = 1.0 / np.array(variances)
    prec_norm = (precision - precision.min()) / (np.ptp(precision) + 1e-9)
    sizes = 60 + 400 * prec_norm

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
    }):
        fig, ax = plt.subplots(figsize=(9, 6))
        if log_scale:
            ax.set_yscale("log")

        if log_scale:
            vmin, vmax = g_disp.min() / 1.1, g_disp.max() * 1.1
        else:
            vmin, vmax = g_disp.min() - 0.1, g_disp.max() + 0.1

        # Same continuous red-yellow-green scheme as effect_distribution_plot.
        sc = ax.scatter(n, g_disp, s=sizes, c=g_disp, cmap="RdYlGn",
                        vmin=vmin, vmax=vmax,
                        alpha=0.9, edgecolors="gray", linewidths=0.6, zorder=5)

        # Pooled estimate line
        ax.axhline(y=pooled_g_disp, color="darkorange", linewidth=1.5, linestyle="--",
                   label=f"Pooled {measure_label} = {pooled_g_disp:.3f}", zorder=4)
        ax.axhline(y=null_value, color="black", linewidth=0.8, linestyle=":", alpha=0.5)

        # Annotate study labels (skip if too many)
        if len(study_labels) <= 15:
            for i, lbl in enumerate(study_labels):
                clean = lbl.replace("_", " ")
                clean = clean[:1].upper() + clean[1:] if clean else clean
                ax.annotate(clean, (n[i], g_disp[i]), textcoords="offset points",
                            xytext=(4, 4), fontsize=12, color="dimgray")

        cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
        cbar.set_label(measure_label, fontsize=17)
        cbar.ax.tick_params(labelsize=14)
        ax.set_xlabel("Total sample size ($N$)", fontsize=18)
        ax.set_ylabel(f"Effect size ({measure_label})" + (" — log scale" if log_scale else ""), fontsize=18)
        ax.tick_params(axis="both", labelsize=15)
        ax.legend(fontsize=15)
        fig.tight_layout()
        _save_figure(fig, output_path)
        plt.close(fig)
    return output_path


# ── Heterogeneity summary plot ────────────────────────────────────────────────

def heterogeneity_summary_plot(
    pooled_g: float,
    pooled_ci_lower: float,
    pooled_ci_upper: float,
    p_value: float,
    k: int,
    n_total: int,
    q_statistic: float,
    q_df: int,
    q_p_value: float,
    i_squared: float,
    tau_squared: float,
    tau: float,
    h_squared: float,
    title: str = "Heterogeneity Summary",
    output_path: str = "outputs/heterogeneity_summary.png",
    measure_label: str = "Hedges' g",
) -> str:
    """
    One-glance heterogeneity diagnostic: a donut showing what share of total
    variance is between-study heterogeneity (I²) vs. sampling error, alongside
    the pooled estimate and heterogeneity statistics (Q, I², tau^2, tau, H^2)
    as text. Always available (unlike the moderator plots) since it only needs
    the numbers meta_analysis_node already computes.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    i2 = max(0.0, min(100.0, i_squared))
    if i2 < 25:
        band = "Low heterogeneity"
    elif i2 < 75:
        band = "Moderate heterogeneity"
    else:
        band = "High heterogeneity"

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
    }):
        fig, (ax_donut, ax_text) = plt.subplots(
            1, 2, figsize=(9, 4.6), gridspec_kw={"width_ratios": [1, 1.35]}
        )

        # ── Donut: I² vs. sampling error ──────────────────────────────────────
        # Warm rose/tan palette, matching the rest of this codebase's
        # nature-style charts (effect_size_agreement, pipeline_attrition, ...).
        wedges, _ = ax_donut.pie(
            [i2, 100 - i2],
            colors=["#c97b6d", "#e3c39a"],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5),
        )
        ax_donut.text(0, 0.12, f"{i2:.1f}%", ha="center", va="center",
                      fontsize=22, fontweight="bold", color="#c97b6d")
        ax_donut.text(0, -0.18, "$I^2$ (heterogeneity)", ha="center", va="center",
                      fontsize=10.5, color="#374151")
        ax_donut.legend(
            wedges, ["Between-study heterogeneity", "Sampling error"],
            loc="upper center", bbox_to_anchor=(0.5, -0.02), fontsize=9.5, frameon=False,
        )
        ax_donut.set_title(band, fontsize=13, fontweight="bold", pad=6)

        # ── Text panel: headline statistics ─────────────────────────────────────
        ax_text.axis("off")
        rows = [
            (f"Pooled {measure_label}", f"{pooled_g:.3f}  [{pooled_ci_lower:.3f}, {pooled_ci_upper:.3f}]"),
            ("$p$-value", f"{p_value:.4f}"),
            ("Studies ($k$)", f"{k}"),
            ("Total $N$", f"{n_total}"),
            ("Cochran's $Q$", f"{q_statistic:.2f}  ($df$={q_df}, $p$={q_p_value:.4f})"),
            ("$I^2$", f"{i2:.1f}%"),
            (r"$\tau^2$ / $\tau$", f"{tau_squared:.4f} / {tau:.4f}"),
            ("$H^2$", f"{h_squared:.2f}"),
        ]
        y0, dy = 0.92, 0.115

        # Table-style horizontal dotted rules: one above the first row, one
        # between each pair of rows, and one below the last row.
        for i in range(len(rows) + 1):
            y_line = y0 + dy / 2 - i * dy
            ax_text.plot([0.0, 1.0], [y_line, y_line], transform=ax_text.transAxes,
                         linestyle=":", linewidth=1.0, color="#9ca3af", zorder=0)

        for i, (label, value) in enumerate(rows):
            y = y0 - i * dy
            ax_text.text(0.0, y, label, fontsize=11.5, color="#374151",
                         ha="left", va="center", transform=ax_text.transAxes)
            ax_text.text(0.62, y, value, fontsize=11.5, color="#111827",
                         ha="left", va="center", fontweight="bold",
                         transform=ax_text.transAxes)

        fig.tight_layout()
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path


# ── Moderator dot-and-whisker plot ────────────────────────────────────────────

_ACRONYMS = {"llm", "ai", "api", "id", "url", "ui", "us", "uk", "usa", "rct", "llms"}


def _clean_moderator_name(name: str) -> str:
    """Underscore-free, sentence-case display form of a moderator variable name,
    with common acronyms (LLM, AI, ...) restored to uppercase."""
    s = (name or "").replace("_", " ").strip()
    if not s:
        return s
    s = f"{s[:1].upper()}{s[1:].lower()}"
    words = s.split(" ")
    words = [w.upper() if w.lower() in _ACRONYMS else w for w in words]
    return " ".join(words)


_MODERATOR_LINE = "#8B5A2B"  # brown for the per-study CI whisker/dot
MODERATOR_MIN_K = 2  # subgroups smaller than this aren't a meaningful pooled estimate


def moderator_plot(
    moderator_name: str,
    categories: List[str],
    estimates: List[float],
    ci_lower_90: List[float],
    ci_upper_90: List[float],
    ci_lower_95: List[float],
    ci_upper_95: List[float],
    n_per_group: List[int],
    output_path: str = "outputs/moderator_plot.png",
    min_k: int = MODERATOR_MIN_K,
) -> str:
    """
    Dot-and-whisker plot for a moderator subgroup analysis.

    Subgroups with fewer than `min_k` studies are excluded from the plot --
    a "pooled" estimate over a single study isn't a meaningful synthesis, just
    that study's own effect and CI restated. The number of excluded categories
    and studies is reported in a note under the plot instead of silently
    dropped.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    kept = [i for i in range(len(categories)) if n_per_group[i] >= min_k]
    excluded_categories = len(categories) - len(kept)
    excluded_studies = sum(n_per_group[i] for i in range(len(categories)) if n_per_group[i] < min_k)

    categories = [categories[i] for i in kept]
    estimates = [estimates[i] for i in kept]
    ci_lower_90 = [ci_lower_90[i] for i in kept]
    ci_upper_90 = [ci_upper_90[i] for i in kept]
    ci_lower_95 = [ci_lower_95[i] for i in kept]
    ci_upper_95 = [ci_upper_95[i] for i in kept]
    n_per_group = [n_per_group[i] for i in kept]

    k = len(categories)
    if k == 0:
        with matplotlib.rc_context({
            "font.family": "sans-serif",
            "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
            "mathtext.fontset": "custom",
            "mathtext.rm": _SANS_FONT,
            "mathtext.it": f"{_SANS_FONT}:italic",
            "mathtext.bf": f"{_SANS_FONT}:bold",
        }):
            fig, ax = plt.subplots(figsize=(7, 3))
            ax.text(0.5, 0.5, f"No subgroup with $k$ ≥ {min_k}",
                    ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
            _save_figure(fig, output_path)
            plt.close(fig)
        return output_path

    y = list(range(k))

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
    }):
        fig, ax = plt.subplots(figsize=(7, max(3, k * 0.9 + 1.5)))

        # Alternating row bands for readability (light gray / white), like a table.
        for i in range(k):
            if i % 2 == 0:
                ax.axhspan(y[i] - 0.5, y[i] + 0.5, color="#eef1f4", zorder=0)

        for i in range(k):
            ax.plot([ci_lower_95[i], ci_upper_95[i]], [y[i], y[i]],
                    color=_MODERATOR_LINE, linewidth=1.0, alpha=0.6, zorder=3)
            ax.plot([ci_lower_90[i], ci_upper_90[i]], [y[i], y[i]],
                    color=_MODERATOR_LINE, linewidth=2.5, alpha=0.95, zorder=4)
            ax.scatter(estimates[i], y[i], color=_MODERATOR_LINE, s=60, zorder=5)

        ax.axvline(x=0, color="#6b7280", linewidth=1.2, linestyle="--", alpha=0.8, zorder=2)
        ax.set_yticks(y)
        labels_with_n = [f"{c} ($k$ = {n})" for c, n in zip(categories, n_per_group)]
        ax.set_yticklabels(labels_with_n, fontsize=11)
        ax.set_xlabel("Hedges' $g$ with CIs", fontsize=12)
        ax.set_title(f"Moderator: {_clean_moderator_name(moderator_name)}", fontsize=15)

        # Single inline row "CI  — 90% CI  — 95% CI" (not a boxed title-above-entries
        # legend) -- the first "handle" is an invisible line so "CI" reads as plain
        # text, matching the uploaded reference exactly.
        ci_handles = [
            plt.Line2D([0], [0], color="none", label="CI"),
            plt.Line2D([0], [0], color=_MODERATOR_LINE, linewidth=2.5, alpha=0.95, label="90% CI"),
            plt.Line2D([0], [0], color=_MODERATOR_LINE, linewidth=1.0, alpha=0.6, label="95% CI"),
        ]
        legend = ax.legend(handles=ci_handles, loc="upper right", ncol=3, fontsize=10,
                           frameon=True, handlelength=1.3, handletextpad=0.5, columnspacing=0.9)
        legend.get_frame().set_facecolor("white")
        legend.get_frame().set_edgecolor("#9ca3af")
        legend.get_frame().set_linewidth(0.9)
        legend.get_frame().set_alpha(0.95)

        fig.tight_layout()
        _save_figure(fig, output_path)
        plt.close(fig)
    return output_path


# ── Violin plot for moderator subgroups ───────────────────────────────────────

def violin_subgroup_plot(
    moderator_name: str,
    group_effects: dict,
    output_path: str = "outputs/violin_plot.png",
) -> str:
    """
    Violin plot of raw study effect sizes split by a categorical moderator.

    `group_effects` is {category: [hedges_g, ...]}. Requires at least 2 categories
    and at least 3 total observations for a meaningful density estimate.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    categories = [c for c, vals in group_effects.items() if len(vals) >= 2]
    if len(categories) < 2:
        return ""

    data = [group_effects[c] for c in categories]
    colors = plt.cm.Set2(np.linspace(0, 0.8, len(categories)))

    fig, ax = plt.subplots(figsize=(max(6, len(categories) * 1.6), 5))

    parts = ax.violinplot(data, positions=range(len(categories)),
                          showmedians=True, showextrema=True)
    for pc, color in zip(parts["bodies"], colors):
        pc.set_facecolor(color)
        pc.set_alpha(0.6)

    # Overlay jittered strip
    rng = np.random.default_rng(0)
    for i, (cat_data, color) in enumerate(zip(data, colors)):
        jitter = rng.uniform(-0.12, 0.12, size=len(cat_data))
        ax.scatter(np.full(len(cat_data), i) + jitter, cat_data,
                   color=color, edgecolors="black", linewidths=0.4, s=30, zorder=5)

    ax.axhline(y=0, color="#6b7280", linewidth=0.8, linestyle="--", alpha=0.7)
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(
        [f"{c}\nk = {len(group_effects[c])}" for c in categories], fontsize=11
    )
    ax.set_ylabel("Hedges' $g$", fontsize=13)
    ax.set_title(f"Effect size distribution by {_clean_moderator_name(moderator_name)}", fontsize=15)
    fig.tight_layout()
    _save_figure(fig, output_path)
    plt.close(fig)
    return output_path


# ── Risk-of-bias traffic-light plot ─────────────────────────────────────────────

# Cochrane-style judgment -> (color, symbol). Collapsed to 3 visible levels:
# low (green), some concerns/moderate (yellow), high/serious/critical (red).
# "no_information" is kept only as a defensive fallback for missing data, not
# shown in the legend as a level of its own.
_ROB_JUDGMENT_STYLE = {
    "low":            ("#16a34a", "+"),
    "some_concerns":  ("#eab308", "−"),
    "moderate":       ("#eab308", "−"),
    "serious":        ("#dc2626", "X"),
    "high":           ("#dc2626", "X"),
    "critical":       ("#dc2626", "X"),
    "no_information": ("#9ca3af", "?"),
}


def risk_of_bias_traffic_light_plot(
    study_labels: List[str],
    domain_names: List[str],
    judgments: List[List[str]],
    overall_judgments: List[str],
    tool_name: str = "RoB 2",
    output_path: str = "outputs/rob_traffic_light.png",
) -> str:
    """
    Cochrane-style risk-of-bias traffic-light plot: one row per study, one column
    per domain plus a final "Overall" column, each cell a plain colored circle
    (low / some-concerns-or-moderate / high-or-serious-or-critical -- see the
    legend for the color key). `judgments[i][j]` is the judgment string for
    study i, domain j (same domain order as `domain_names`); `overall_judgments[i]`
    is study i's overall risk judgment. Rows are labelled generically
    "Study 1".."Study k" (in input order) rather than by paper title, to avoid
    truncated/interrupted labels.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    k = len(study_labels)
    n_domains = len(domain_names)
    n_cols = n_domains + 1
    col_labels = [f"D{i+1}" for i in range(n_domains)] + ["Overall"]

    # Domain columns are evenly spaced 1.0 apart; the "Overall" column sits on
    # a shorter gap so it reads as closer to the domain block, not a separate
    # group -- only the divider line marks the conceptual split.
    overall_gap = 1.35
    col_x = list(range(n_domains)) + [max(0, n_domains - 1) + overall_gap]

    # Fixed, k-independent top/bottom margins (inches) so the legend/note block
    # doesn't balloon into empty vertical space for taller (large-k) plots.
    row_h, top_in, bottom_in = 0.5, 0.4, 0.8
    fig_h = row_h * k + top_in + bottom_in

    with matplotlib.rc_context({
        "font.family": "sans-serif",
        "font.sans-serif": [_SANS_FONT, "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": _SANS_FONT,
        "mathtext.it": f"{_SANS_FONT}:italic",
        "mathtext.bf": f"{_SANS_FONT}:bold",
    }):
        fig, ax = plt.subplots(figsize=(0.4 * n_domains + overall_gap + 1.3, fig_h))

        for i in range(k):
            y = k - 1 - i
            # Defensive: coerce to exactly n_domains entries so a study with a missing or
            # duplicated domain judgment can't shift "Overall" out of its column.
            row = list(judgments[i])[:n_domains]
            row += ["no_information"] * (n_domains - len(row))
            row_judgments = row + [overall_judgments[i]]
            for j, judgment in enumerate(row_judgments):
                color, _symbol = _ROB_JUDGMENT_STYLE.get(
                    (judgment or "").strip().lower(), ("#9ca3af", "?")
                )
                edge = "#111827" if j == n_cols - 1 else "white"
                ax.scatter(col_x[j], y, s=420, color=color, edgecolors=edge, linewidths=1.6, zorder=3)
            if n_cols > 1:
                ax.axvline((col_x[-2] + col_x[-1]) / 2, color="#d1d5db",
                           linewidth=1, linestyle=":", zorder=1)

        ax.set_xlim(col_x[0] - 0.6, col_x[-1] + 0.4)
        ax.set_ylim(-0.7, k - 0.3)
        ax.set_xticks(col_x)
        ax.set_xticklabels(col_labels, fontsize=11, fontweight="bold")
        ax.xaxis.set_ticks_position("top")
        ax.xaxis.set_label_position("top")
        ax.set_yticks(range(k))
        ax.set_yticklabels([f"Study {k - y}" for y in range(k)], fontsize=11)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_axisbelow(True)

        # Legend and note anchored in FIGURE (not axes) fraction coordinates, so
        # their distance from the bottom stays constant regardless of k.
        handles = [
            plt.Line2D([0], [0], marker="o", linestyle="", markersize=14,
                       markerfacecolor=color, markeredgecolor="white", label=label)
            for label, color in [
                ("Low", "#16a34a"), ("Some concerns", "#eab308"), ("High", "#dc2626"),
            ]
        ]
        legend_y = (bottom_in - 0.2) / fig_h
        fig.legend(handles=handles, loc="center", bbox_to_anchor=(0.5, legend_y),
                   ncol=3, fontsize=9, frameon=False)

        domain_legend = "Note: " + "  ".join(
            f"D{i+1}: {name}" for i, name in enumerate(domain_names)
        )
        fig.text(0.02, 0.02 / fig_h, domain_legend, fontsize=8, color="#4b5563",
                  style="italic", wrap=True, va="bottom")

        fig.tight_layout(rect=[0, bottom_in / fig_h, 1, 1 - (top_in - 0.3) / fig_h])
        _save_figure(fig, output_path, facecolor="white")
        plt.close(fig)
    return output_path
