"""Share of reviews whose AutoSynthesis effect is within +/-0.05 and +/-0.20 of the Cochrane effect (null-at-0 scale; log for ratios).
Standardized measures only (SMD, RR, OR, HR); denominator = reviews where the model used the same measure and a valid result. Output: effect_tolerance_bars.pdf"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tol_data import rows, MODELS, HERE
from paths import DATA, RUNS, FIG, RESULTS
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "pdf.fonttype": 42})
C = ["#1F3864", "#6C8EBF", "#C9D6EA", "#E4E4E4"]
fig, ax = plt.subplots(figsize=(10, 3.6))
for y, m in enumerate(reversed(MODELS)):
    rr = [r for r in rows if r["model"] == m and r["status"] == "ok"]; n = len(rr)
    a = sum(r["status"] == "ok" and r["delta"] <= .05 for r in rr)
    b = sum(r["status"] == "ok" and .05 < r["delta"] <= .20 for r in rr)
    c = sum(r["status"] == "ok" and r["delta"] > .20 for r in rr)
    e = 0
    left = 0
    for v, col, hatch in zip((a, b, c), C[:3], (None, None, None)):
        ax.barh(y, 100 * v / n, left=left, color=col, edgecolor="white" if not hatch else "#999999", hatch=hatch, height=.62, lw=1)
        if v and v / n > .05: ax.text(left + 50 * v / n, y, f"{100*v/n:.0f}%", ha="center", va="center", color="white" if col in C[:2] else "#222222", fontsize=13, fontweight="bold")
        left += 100 * v / n
    ax.text(101, y, f"≤0.20: {100*(a+b)/n:.0f}%", va="center", fontsize=12, color="#222222")
ax.set_yticks(range(3)); ax.set_yticklabels([f"{NAMES[m]} ($n$={sum(r['model']==m and r['status']=='ok' for r in rows)})" for m in reversed(MODELS)])
ax.set_xlim(0, 100); ax.set_xlabel("Share of reviews with a comparable result (%)")
for s in ("top", "right"): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=C[0], label="within ±0.05"), Patch(fc=C[1], label="within ±0.20 (beyond ±0.05)"), Patch(fc=C[2], label="beyond ±0.20")],
          loc="upper center", bbox_to_anchor=(.45, -.22), ncol=3, frameon=False, fontsize=11, handlelength=1.2, columnspacing=1.2)
fig.savefig(os.path.join(FIG, "effect_tolerance_bars.pdf"), bbox_inches="tight")
