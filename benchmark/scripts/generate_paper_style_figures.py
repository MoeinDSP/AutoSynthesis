"""Figures in the style of Holtdirk et al. (arXiv 2606.13670): AutoSynthesis effect vs the Cochrane ('original') effect.
Effects on the null-at-0 scale (SMD as is; RR/OR/HR on the log scale); 'original' effects are shown as positive values and the model effect is
sign-aligned to them (negative = opposite direction), as in the paper. Only reviews where the model used the same effect measure and a valid result.
Outputs (PDF): paper_fig2_<model>_<strict|broad>.pdf, paper_fig2_grid.pdf, paper_fig3_scatter.pdf, paper_figS9_subfield.pdf, paper_figS10_magnitude.pdf, paper_figS12_agreement.pdf"""
import math, os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde, linregress
from tol_data import rows, MODELS, HERE
from paths import DATA, RUNS, FIG, RESULTS
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.linewidth": .8, "pdf.fonttype": 42})
RED, PALE, GREY, BLUE = "#C4725A", "#EDD5C5", "#3A3A3A", "#5B88BE"
TOL = {"strict": .05, "broad": .20}
def ok(m): return [r for r in rows if r["model"] == m and r["status"] == "ok"]
def orient(r):
    s = 1.0 if r["gx"][0] >= 0 else -1.0
    return abs(r["gx"][0]), s * r["py"][0]
def wilson(k, n, z=1.96):
    if n == 0: return 0, 0
    p = k / n; c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
def stacked(ax, x, within, n, w=.55, show_ci=True, narrow=False):
    p = 100 * within / n if n else 0
    ax.bar(x, p, w, color=PALE); ax.bar(x, 100 - p, w, bottom=p, color=RED)
    fs = 6.5 if narrow else 8
    ax.text(x, max(p / 2, 5) if not show_ci else (p / 2 if p > 14 else p + 7), f"{p:.0f}%", ha="center", va="center", fontsize=fs, fontweight="bold")
    if not narrow and 100 - p > 12: ax.text(x, p + (100 - p) / 2 + (8 if show_ci and abs(p + (100 - p) / 2 - p) < 15 else 0), f"{100-p:.0f}%", ha="center", va="center", fontsize=fs, fontweight="bold")
BLUES = ["#1F3864", "#6C8EBF", "#C9D6EA"]   # strict / broad (beyond strict) / outside -- same blues as the tolerance bars
def stacked3(ax, d, x=0, w=.5, strict=.05, broad=.20):
    """Three-level stacked bar for the absolute differences d: within +/-0.05, within +/-0.20 (beyond 0.05), beyond 0.20."""
    n = len(d); n1 = int((d <= strict).sum()); n2 = int((d <= broad).sum())
    p1 = 100 * n1 / n if n else 0; p2 = 100 * (n2 - n1) / n if n else 0; p3 = 100 - p1 - p2
    for y0, h, col in ((0, p1, BLUES[0]), (p1, p2, BLUES[1]), (p1 + p2, p3, BLUES[2])):
        ax.bar(x, h, w, bottom=y0, color=col)
    for y0, h, col in ((0, p1, "white"), (p1, p2, "white"), (p1 + p2, p3, "#222222")):
        if h >= 7: ax.text(x - .06, y0 + h / 2, f"{h:.0f}%", ha="center", va="center", fontsize=8.5, fontweight="bold", color=col)
def fig2(model, mode):
    tol = TOL[mode]; R = ok(model); n = len(R)
    pts = sorted((orient(r) + (r,) for r in R), key=lambda t: t[0]); orig = np.array([t[0] for t in pts]); llm = np.array([t[1] for t in pts])
    delta = np.abs(llm - orig); within = delta <= tol
    fig = plt.figure(figsize=(11, 6.2)); gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], height_ratios=[1, 1], wspace=.28, hspace=.35)
    a = fig.add_subplot(gs[:, 0]); y = np.arange(1, n + 1)
    a.axvline(0, color="black", ls=":", lw=.8)
    a.plot(orig, y, "s", color=GREY, ms=3.4, label="Original (Cochrane)"); a.plot(llm, y, "o", color=BLUE, ms=3.4, label=f"AutoSynthesis")
    a.set_xlabel("Effect size (standardized; log for ratios)"); a.set_ylabel("Review"); a.legend(loc="lower right", frameon=False, fontsize=8); clean(a)
    a.text(-.1, 1.02, "a", transform=a.transAxes, fontweight="bold", fontsize=11)
    sub = gs[0, 1].subgridspec(2, 1, height_ratios=[3, 2], hspace=0)
    b1 = fig.add_subplot(sub[0]); b2 = fig.add_subplot(sub[1], sharex=b1); top = max(delta.max() * 1.05, .5)
    xs = np.linspace(0, top, 300); kd = gaussian_kde(np.r_[delta, -delta], bw_method=.25); dens = 2 * kd(xs)
    b1.fill_between(xs, dens, color=RED, alpha=.55); b1.plot(xs, dens, color=RED, lw=1); b1.axvline(tol, color="#555555", ls="--", lw=.8, label=f"{mode.capitalize()} tolerance")
    b1.set_yticks([]); b1.legend(loc="upper right", frameon=False, fontsize=8); plt.setp(b1.get_xticklabels(), visible=False)
    for s in ("top", "right", "left"): b1.spines[s].set_visible(False)
    b2.boxplot(delta, vert=False, positions=[.8], widths=.3, showfliers=False, boxprops=dict(color="black"), medianprops=dict(color="black"), whiskerprops=dict(color="black"), capprops=dict(color="black"))
    rng = np.random.default_rng(1); b2.scatter(delta, rng.uniform(.0, .55, n), s=7, color=RED, alpha=.6, lw=0); b2.axvline(tol, color="#555555", ls="--", lw=.8)
    b2.set_ylim(-.05, 1.1); b2.set_yticks([]); b2.set_xlim(0, top); b2.set_xlabel("|Δ| = |θ_AutoSynthesis − θ_Cochrane|")
    for s in ("top", "right", "left"): b2.spines[s].set_visible(False)
    b1.text(-.05, 1.05, "b", transform=b1.transAxes, fontweight="bold", fontsize=11)
    c = gs[1, 1].subgridspec(1, 3, wspace=.5)
    groups = [("Full dataset", np.ones(n, bool)), ("SMD", np.array([t[2]["fam"] == "SMD" for t in pts])), ("Ratio\n(RR, OR, HR)", np.array([t[2]["fam"] != "SMD" for t in pts]))]
    for k, (lab, mask) in enumerate(groups):
        ax = fig.add_subplot(c[k]); stacked3(ax, delta[mask]); ax.set_xlim(-.45, .45); ax.set_ylim(0, 100); ax.set_xticks([0])
        ax.set_xticklabels([f"{lab}\n($N$={int(mask.sum())})"], fontsize=8); clean(ax)
        if k == 0: ax.set_ylabel("AutoSynthesis reanalysis (%)")
        else: ax.set_yticklabels([]); ax.spines["left"].set_visible(False); ax.set_yticks([])
        ax.text(-.2 if k == 0 else -.1, 1.04, "cde"[k], transform=ax.transAxes, fontweight="bold", fontsize=11)
    fig.legend(handles=[Patch(fc=BLUES[0], label="within ±0.05"), Patch(fc=BLUES[1], label="within ±0.20 (beyond ±0.05)"), Patch(fc=BLUES[2], label="beyond ±0.20")], loc="lower right", bbox_to_anchor=(1.0, -.07), ncol=3, frameon=False, fontsize=8)
    fig.suptitle(f"{NAMES[model]}: tolerance ±{tol:.2f}", x=.06, ha="left", fontsize=11, fontweight="bold")
    fig.savefig(os.path.join(FIG, f"paper_fig2_{model}_{mode}.pdf"), bbox_inches="tight"); plt.close(fig)
def stacked_side(ax, within, n, x=0, w=.5):
    """Stacked within/outside bar (no error bars)."""
    p = 100 * within / n if n else 0
    ax.bar(x, p, w, color=PALE); ax.bar(x, 100 - p, w, bottom=p, color=RED)
    ax.text(x - .06, p / 2 if p > 12 else p + 7, f"{p:.0f}%", ha="center", va="center", fontsize=9, fontweight="bold")
    if 100 - p > 12: ax.text(x - .06, p + (100 - p) / 2, f"{100-p:.0f}%", ha="center", va="center", fontsize=9, fontweight="bold")
def fig2_grid():
    """One panel per model, three-level blue bars (within +/-0.05, within +/-0.20 beyond 0.05, beyond +/-0.20) for Full dataset / SMD / Ratio."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True)
    for c, m in enumerate(MODELS):
        ax = axes[c]; R = ok(m); pts = [orient(x) + (x,) for x in R]
        delta = np.array([abs(p[1] - p[0]) for p in pts]); fam = np.array([p[2]["fam"] for p in pts])
        for k, (lab, mask) in enumerate((("Full dataset", np.ones(len(pts), bool)), ("SMD", fam == "SMD"), ("Ratio\n(RR, OR, HR)", fam != "SMD"))):
            stacked3(ax, delta[mask], x=k)
            ax.text(k, -4, f"{lab}\n($N$={int(mask.sum())})", ha="center", va="top", fontsize=8.5)
        ax.set_xlim(-.55, 2.55); ax.set_ylim(0, 100); ax.set_xticks([]); clean(ax)
        if c == 0: ax.set_ylabel("AutoSynthesis reanalysis (%)", fontsize=10)
        ax.set_title(NAMES[m], fontsize=12, fontweight="bold")
    fig.legend(handles=[Patch(fc=BLUES[0], label="within ±0.05"), Patch(fc=BLUES[1], label="within ±0.20 (beyond ±0.05)"), Patch(fc=BLUES[2], label="beyond ±0.20")],
               loc="lower center", ncol=3, frameon=False, fontsize=10, bbox_to_anchor=(.5, -.02))
    fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(os.path.join(FIG, "paper_fig2_grid.pdf"), bbox_inches="tight"); plt.close(fig)
def fig3():
    fig = plt.figure(figsize=(13, 4.8)); outer = fig.add_gridspec(1, 3, wspace=.28)
    for k, m in enumerate(MODELS):
        R = ok(m); pts = [orient(r) for r in R]; x = np.array([p[1] for p in pts]); yv = np.array([p[0] for p in pts]); n = len(R)
        g = outer[k].subgridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=.04, hspace=.04)
        ax = fig.add_subplot(g[1, 0]); hx = fig.add_subplot(g[0, 0], sharex=ax); hy = fig.add_subplot(g[1, 1], sharey=ax)
        lim = 2.0; ax.set_facecolor("#F3F3F3"); ax.plot([-.3, lim], [-.3, lim], color="#777777", lw=.7, ls="--")
        ax.scatter(x, yv, s=12, color=BLUE, alpha=.6, lw=0); ax.axhline(0, color="black", lw=.8); ax.axvline(0, color="black", lw=.8)
        lr = linregress(x, yv); xx = np.array([x.min(), min(x.max(), lim)]); ax.plot(xx, lr.intercept + lr.slope * xx, color="black", lw=1.6)
        ax.set_xlim(-.3, lim); ax.set_ylim(-.1, lim); ax.set_xlabel("AutoSynthesis effect (sign-aligned)"); ax.set_ylabel("Cochrane effect (positive)" if k == 0 else "")
        ax.text(.04, .94, f"$N$ = {n}\nr = {lr.rvalue:.2f}", transform=ax.transAxes, va="top", fontsize=9, style="italic")
        hx.hist(x[(x > -.3) & (x < lim)], bins=24, color=GREY, ec="black", lw=.4, alpha=.8); hy.hist(yv[yv < lim], bins=24, orientation="horizontal", color=BLUE, ec="black", lw=.4, alpha=.8)
        for h in (hx, hy): h.axis("off")
        hx.set_title(NAMES[m], loc="left", fontsize=11, fontweight="bold")
        for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.savefig(os.path.join(FIG, "paper_fig3_scatter.pdf"), bbox_inches="tight"); plt.close(fig)
COL = {"GPT": "#0072B2", "Gemini": "#E69F00", "Claude": "#009E73"}
def dodge_violin(ax, groups, getter, minn=4):
    for gi, g in enumerate(groups):
        for k, m in enumerate(MODELS):
            v = getter(m, g)
            pos = gi + (k - 1) * .27
            if len(v) >= minn:
                vp = ax.violinplot(v, positions=[pos], widths=.25, showextrema=False)
                for b in vp["bodies"]: b.set_facecolor(COL[m]); b.set_alpha(.35); b.set_edgecolor(COL[m])
            if len(v): ax.boxplot(v, positions=[pos], widths=.12, showfliers=False, boxprops=dict(color=COL[m]), medianprops=dict(color=COL[m]), whiskerprops=dict(color=COL[m]), capprops=dict(color=COL[m]))
    ax.axhline(.05, color="#555555", ls="--", lw=.8)
def fig_s9():
    subs = ["Mental health & neurology", "Cardiovascular, kidney & critical care", "Women's health, pregnancy & neonatal", "Public health & behaviour", "Infection, respiratory & immune", "Musculoskeletal, pain & surgery", "Cancer"]
    lab = ["Mental health\n& neurology", "Cardio-, kidney\n& critical care", "Women's health,\npregnancy, neonatal", "Public health\n& behaviour", "Infection, resp.\n& immune", "Musculoskeletal,\npain & surgery", "Cancer"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(19, 5.6), gridspec_kw={"width_ratios": [1.1, 1], "wspace": .12})
    for gi, g in enumerate(subs):
        for k, m in enumerate(MODELS):
            R = [r for r in ok(m) if r["subfield"] == g]; stacked(a, gi + (k - 1) * .27, sum(r["delta"] <= .05 for r in R), len(R), w=.25, show_ci=False, narrow=True)
    a.set_xticks(range(len(subs))); a.set_xticklabels([f"{l}\n($N$={len([r for r in ok('GPT') if r['subfield']==s])}/{len([r for r in ok('Gemini') if r['subfield']==s])}/{len([r for r in ok('Claude') if r['subfield']==s])})" for l, s in zip(lab, subs)], fontsize=7.5)
    a.set_ylabel("% within strict tolerance (±0.05); labels show the within share"); clean(a); a.text(-.08, 1.02, "a", transform=a.transAxes, fontweight="bold", fontsize=11)
    dodge_violin(b, subs, lambda m, g: [r["delta"] for r in ok(m) if r["subfield"] == g]); b.set_ylim(0, 1.6)
    b.set_xticks(range(len(subs))); b.set_xticklabels([l.replace("\n", " ") if False else l for l in lab], fontsize=7.5); b.set_ylabel("|Δ| = |θ_AutoSynthesis − θ_Cochrane|"); clean(b)
    b.text(-.08, 1.02, "b", transform=b.transAxes, fontweight="bold", fontsize=11)
    fig.legend(handles=[Patch(fc=COL[m], alpha=.6, label=NAMES[m]) for m in MODELS], loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.04))
    fig.suptitle("Within-tolerance share and deviation by subfield (bars grouped GPT / Gemini / Claude; N shown in that order)", x=.06, ha="left", fontsize=10)
    fig.savefig(os.path.join(FIG, "paper_figS9_subfield.pdf"), bbox_inches="tight"); plt.close(fig)
def fig_s10():
    bins = [("Negligible\n(|θ_Cochrane| < 0.2)", 0, .2), ("Small\n(0.2 ≤ |θ| < 0.5)", .2, .5), ("Medium\n(0.5 ≤ |θ| < 0.8)", .5, .8), ("Large\n(|θ| ≥ 0.8)", .8, 99)]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    get = lambda m, g: [r["delta"] for r in ok(m) if g[1] <= abs(r["gx"][0]) < g[2]]
    dodge_violin(ax, bins, get); ax.set_ylim(0, 1.6)
    ax.set_xticks(range(4)); ax.set_xticklabels([f"{b[0]}\n$N$={len(get('GPT', b))}/{len(get('Gemini', b))}/{len(get('Claude', b))}" for b in bins], fontsize=8)
    ax.set_ylabel("|Δ| = |θ_AutoSynthesis − θ_Cochrane|"); ax.set_xlabel("Magnitude of the Cochrane effect ($N$: GPT/Gemini/Claude)"); clean(ax)
    ax.legend(handles=[Patch(fc=COL[m], alpha=.6, label=NAMES[m]) for m in MODELS] + [plt.Line2D([], [], color="#555555", ls="--", label="Strict tolerance (±0.05)")], frameon=False, fontsize=8, loc="upper left")
    fig.savefig(os.path.join(FIG, "paper_figS10_magnitude.pdf"), bbox_inches="tight"); plt.close(fig)
def fig_s12():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": .5}); ref = {r["id"]: r for r in ok("GPT")}
    for ax, m in zip(axes, ("Gemini", "Claude")):
        o = {r["id"]: r for r in ok(m)}; ids = sorted(set(o) & set(ref)); M = np.zeros((2, 2), int)
        for i in ids: M[0 if ref[i]["delta"] <= .05 else 1, 0 if o[i]["delta"] <= .05 else 1] += 1
        N = len(ids); ax.imshow(M, cmap="Blues", vmin=0, vmax=M.max() * 1.15)
        for (i, j), v in np.ndenumerate(M): ax.text(j, i, f"{v}\n{100*v/N:.0f}%", ha="center", va="center", fontsize=11, fontweight="bold", color="white" if v > M.max() * .6 else "#222222")
        ax.set_xticks([0, 1]); ax.set_xticklabels(["Within\ntolerance", "Outside\ntolerance"]); ax.set_yticks([0, 1]); ax.set_yticklabels(["Within\ntolerance", "Outside\ntolerance"])
        ax.set_xlabel(NAMES[m]); ax.set_ylabel(NAMES["GPT"]); ax.set_title(f"{NAMES['GPT']} vs {NAMES[m]} ($n$={N})", fontsize=10)
        for s in ax.spines.values(): s.set_visible(False)
        ax.tick_params(length=0)
    fig.savefig(os.path.join(FIG, "paper_figS12_agreement.pdf"), bbox_inches="tight"); plt.close(fig)
if __name__ == "__main__":
    for m in MODELS:
        for mode in TOL: fig2(m, mode)
    fig2_grid(); fig3(); fig_s9(); fig_s10(); fig_s12(); print("done")
