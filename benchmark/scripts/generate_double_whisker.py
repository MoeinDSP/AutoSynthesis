"""Double-whisker plot: Cochrane effect (x) vs AutoSynthesis effect (y), each with its 95% CI, one panel per model.
Null-at-0 scale (log for ratios), standardized measures (SMD, RR, OR, HR). Grey band = +/-0.20 around the diagonal. Output: effect_double_whisker.pdf"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from tol_data import rows, MODELS, HERE
from paths import DATA, RUNS, FIG, RESULTS
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude Opus 5"}
COL = {"GPT": "#0072B2", "Gemini": "#E69F00", "Claude": "#009E73"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "pdf.fonttype": 42})
L = 2.0
def make(models, suffix):
    fig, axes = plt.subplots(1, len(models), figsize=(5.2 * len(models) - (0 if len(models) > 1 else .2), 5.4), sharex=True, sharey=True, squeeze=False); axes = axes[0]
    for ax, m in zip(axes, models):
        ok = [r for r in rows if r["model"] == m and r["status"] == "ok"]
        ax.fill_between([-L, L], [-L - .2, L - .2], [-L + .2, L + .2], color="#E8E8E8", lw=0, zorder=0)
        ax.plot([-L, L], [-L, L], color="#888888", lw=1, zorder=1); ax.axhline(0, color="#BBBBBB", lw=.8); ax.axvline(0, color="#BBBBBB", lw=.8)
        for r in ok:
            (gx, glo, ghi), (py, plo, phi) = r["gx"], r["py"]
            ax.plot([glo, ghi], [py, py], color=COL[m], alpha=.35, lw=1, zorder=2)
            ax.plot([gx, gx], [plo, phi], color=COL[m], alpha=.35, lw=1, zorder=2)
            ax.plot(gx, py, "o", color=COL[m], ms=5.5, zorder=3)
        out = sum(abs(r["gx"][0]) > L or abs(r["py"][0]) > L for r in ok)
        ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect("equal")
        ax.set_title(f"{NAMES[m]}  ($n$={len(ok)})", loc="left", fontsize=14, fontweight="bold")
        rr, pp = pearsonr([r["gx"][0] for r in ok], [r["py"][0] for r in ok]); ptxt = "$p$ < 0.001" if pp < .001 else f"$p$ = {pp:.3f}"
        ax.text(.97, .04, f"$r$ = {rr:.2f}, {ptxt}", transform=ax.transAxes, ha="right", va="bottom", fontsize=13, fontweight="bold", bbox=dict(fc="white", ec="none", alpha=.85, pad=2))
        print(f"{NAMES[m]}: r={rr:.3f} p={pp:.2g} n={len(ok)}")
        ax.set_xlabel("Cochrane effect")
        print(f"[caption note] {NAMES[m]}: {out} of {len(ok)} reviews outside the axis range (|effect| > {L}), not shown")
        for s in ("top", "right"): ax.spines[s].set_visible(False)
    axes[0].set_ylabel("AutoSynthesis effect")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f"effect_double_whisker{suffix}.pdf"), bbox_inches="tight")
make(MODELS, '')
make(['GPT'], '_gpt')
make(['Gemini', 'Claude'], '_gemini_claude')
