"""Unit-free comparison for ALL effect measures (incl. MD, RD): rel = |theta_auto - theta_Cochrane| / width of the Cochrane 95% CI.
Cut-offs 0.10 and 0.25 of the CI width. Standardized measures (SMD, RR, OR, HR) and difference measures (MD, RD) are kept visibly separate.
Outputs: unitfree_tolerance_bars.pdf, unitfree_double_whisker.pdf, unitfree_breakdown.pdf"""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import pearsonr
from rel_data import rows, ok, MODELS, HERE, T1, T2
from paths import DATA, RUNS, FIG, RESULTS
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude"}
COL = {"GPT": "#0072B2", "Gemini": "#E69F00", "Claude": "#009E73"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "pdf.fonttype": 42})
C = ["#1F3864", "#6C8EBF", "#C9D6EA"]
def clean(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
def bars():
    fig, axes = plt.subplots(1, 2, figsize=(14, 3.9), sharex=True)
    for ax, grp, title in zip(axes, ("std", "diff"), ("Standardized measures (SMD, RR, OR, HR)", "Difference measures (MD, RD)")):
        for y, m in enumerate(reversed(MODELS)):
            v = np.array([r["rel"] for r in ok(m, group=grp)]); n = len(v); a = (v <= T1).sum(); b = ((v > T1) & (v <= T2)).sum(); c = (v > T2).sum(); left = 0
            for k, col in zip((a, b, c), C):
                ax.barh(y, 100 * k / n, left=left, color=col, edgecolor="white", height=.62)
                if k / n > .06: ax.text(left + 50 * k / n, y, f"{100*k/n:.0f}%", ha="center", va="center", color="white" if col != C[2] else "#222222", fontweight="bold")
                left += 100 * k / n
            ax.text(101, y, f"≤{T2}: {100*(a+b)/n:.0f}%", va="center", fontsize=11)
        ax.set_yticks(range(3)); ax.set_yticklabels([f"{NAMES[m]} ($n$={len(ok(m, group=grp))})" for m in reversed(MODELS)]); ax.set_xlim(0, 100)
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold"); ax.set_xlabel("Share of reviews with a comparable result (%)"); clean(ax)
    fig.legend(handles=[Patch(fc=C[0], label=f"within {T1}"), Patch(fc=C[1], label=f"within {T2} (beyond {T1})"), Patch(fc=C[2], label=f"beyond {T2}")], loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.07))
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "unitfree_tolerance_bars.pdf"), bbox_inches="tight"); plt.close(fig)
def whisker():
    L = 4.0; fig, axes = plt.subplots(1, 3, figsize=(15, 5.4), sharex=True, sharey=True)
    for ax, m in zip(axes, MODELS):
        R = ok(m); ax.fill_between([-L, L], [-L - T2, L - T2], [-L + T2, L + T2], color="#E8E8E8", lw=0, zorder=0)
        ax.plot([-L, L], [-L, L], color="#888888", lw=1); ax.axhline(0, color="#BBBBBB", lw=.8); ax.axvline(0, color="#BBBBBB", lw=.8)
        off = 0
        for r in R:
            W = r["W"]; gx = r["gx"][0] / W; (py, plo, phi) = (v / W for v in r["py"]); gl, gh = r["gx"][1] / W, r["gx"][2] / W
            if max(abs(gx), abs(py)) > L: off += 1
            c = COL[m]; mk = "o" if r["group"] == "std" else "s"
            ax.plot([gl, gh], [py, py], color=c, alpha=.3, lw=1, zorder=2); ax.plot([gx, gx], [plo, phi], color=c, alpha=.3, lw=1, zorder=2)
            ax.plot(gx, py, mk, color=c if r["group"] == "std" else "white", mec=c, ms=5.5 if mk == "o" else 6, mew=1.2, zorder=3)
        xs_ = [r["gx"][0] / r["W"] for r in R]; ys_ = [r["py"][0] / r["W"] for r in R]
        rr, pp = pearsonr(xs_, ys_); ptxt = "$p$ < 0.001" if pp < .001 else f"$p$ = {pp:.3f}"
        ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect("equal"); ax.set_title(f"{NAMES[m]}  ($n$={len(R)})", loc="left", fontsize=13, fontweight="bold")
        ax.text(.97, .04, f"$r$ = {rr:.2f}, {ptxt}", transform=ax.transAxes, ha="right", va="bottom", fontsize=12, fontweight="bold", bbox=dict(fc="white", ec="none", alpha=.85, pad=2))
        print(f"{NAMES[m]}: r={rr:.3f} p={pp:.2g} n={len(R)}")
        ax.set_xlabel("Cochrane effect (unit-free)"); clean(ax)
        print(f"[caption note] {NAMES[m]}: {off} of {len(R)} reviews outside the axis range (|value| > {L}), not shown")
    axes[0].set_ylabel("AutoSynthesis effect (unit-free)")
    fig.legend(handles=[plt.Line2D([], [], marker="o", ls="", color="#555555", label="SMD, RR, OR, HR"), plt.Line2D([], [], marker="s", ls="", mfc="white", mec="#555555", label="MD, RD"), Patch(fc="#E8E8E8", label=f"±{T2} band")], loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.1))
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "unitfree_double_whisker.pdf"), bbox_inches="tight"); plt.close(fig)
ERAS = ["≤2009", "2010–2015", "2016–2020", "2021+", "Year unknown"]
SUBS = ["Mental health & neurology", "Cardiovascular, kidney & critical care", "Women's health, pregnancy & neonatal", "Public health & behaviour", "Infection, respiratory & immune", "Musculoskeletal, pain & surgery", "Cancer"]
def breakdown(T=T2, fname="unitfree_breakdown.pdf"):
    """All 100 reviews, every measure. A review with no comparable result (different measure / invalid) counts as 'not within'."""
    def grp(key, g): return lambda r: (r[key] or "Year unknown") == g
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), gridspec_kw={"width_ratios": [1, 1.55]})
    for ax, key, groups, title in ((axes[0], "era", ERAS, "Year of first publication"), (axes[1], "subfield", SUBS, "Subfield")):
        for gi, g in enumerate(groups):
            y = len(groups) - 1 - gi
            for k, m in enumerate(MODELS):
                R = [r for r in rows if r["model"] == m and grp(key, g)(r)]
                v = 100 * sum(r["status"] == "ok" and r["rel"] <= T for r in R) / len(R)
                ax.plot(v, y + (1 - k) * .2, "o", color=COL[m], ms=9, label=NAMES[m] if gi == 0 else None)
            ax.axhline(y, color="#EEEEEE", lw=1, zorder=0)
        ns = [len([r for r in rows if r["model"] == "GPT" and grp(key, g)(r)]) for g in groups]; assert sum(ns) == 100
        ax.set_yticks(range(len(groups))); ax.set_yticklabels([f"{g}  ($n$={n})" for g, n in zip(reversed(groups), reversed(ns))])
        ax.set_xlim(0, 105); ax.set_xlabel(f"Within {T:.2f} (%)"); ax.set_title(title, loc="left", fontsize=13, fontweight="bold"); clean(ax)
    h, l = axes[1].get_legend_handles_labels(); fig.legend(h, l, loc="lower center", bbox_to_anchor=(.5, -.04), ncol=3, frameon=False)
    fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(os.path.join(FIG, fname), bbox_inches="tight"); plt.close(fig)
if __name__ == "__main__":
    bars(); whisker(); breakdown(); breakdown(T1, "unitfree_breakdown_strict.pdf"); print("done")
