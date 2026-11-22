"""Flow-style funnel (centered bars joined by smooth bands) of the Cochrane benchmark, one panel per model, same scale.
Stages (papers = PDFs tracked in the full run): In the pipeline (found by search + added by hand) -> Document type OK -> Data extracted -> Effect size computed (kept).
Percentages are of the papers in the pipeline. Stage counts: data/prisma_counts.json (from each run's paper_tracking.csv);
retrieved/screened: runs/<id>/<model>/search_agent/search_summary.json. Output: figures/funnel_flow_gpt.pdf"""
import json, glob, os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
from paths import DATA, RUNS, FIG, RESULTS
D = json.load(open(os.path.join(DATA, "prisma_counts.json")))
NAME = {"GPT": "GPT", "Gemini": "Gemini", "Claude": "Claude"}
import glob
FOUND = {}
for k, m in (("GPT", "gpt-5.6-sol"),):
    S = [json.load(open(p)) for p in glob.glob(os.path.join(RUNS, "CD*", m, "search_agent", "search_summary.json"))]
    assert len(S) == 100
    FOUND[k] = sum(x["n_found_unique"] for x in S)
STAGES = ["Retrieved", "Screened", "Eligible", "Included"]
COLS = ["#EEE6D8", "#DEC5B8", "#CFA194", "#C08272"]
plt.rcParams.update({"font.family": ["Liberation Sans", "DejaVu Sans"], "font.size": 11, "pdf.fonttype": 42})
SM = {"GPT": "gpt-5.6-sol", "Gemini": "gemini-3.8-flash"}
for k, m in SM.items():
    S = [json.load(open(p)) for p in glob.glob(os.path.join(RUNS, "CD*", m, "search_agent", "search_summary.json"))]
    assert len(S) == 100
    D[k]["retrieved"] = sum(x["n_found_unique"] for x in S); D[k]["screened"] = sum(x["n_prescreen_included"] for x in S)
YM = max(d["inpipe"] for d in D.values())
BW, GAP = .62, .38
def make(keys, suffix):
    fig, axes = plt.subplots(1, len(keys), figsize=(5 * len(keys), 5.2), sharey=True, squeeze=False); axes = axes[0]
    for ax, k in zip(axes, keys):
        d = D[k]
        n0 = d["inpipe"]; n1 = n0 - d["doc"]; n2 = n1 - d["ext"]; n3 = d["kept"]
        assert n3 == n2 - d["eff"]
        vals = [n0, n1, n2, n3]
        for s, v in enumerate(vals):
            x = s * (BW + GAP)
            ax.add_patch(plt.Rectangle((x, -v / 2), BW, v, fc=COLS[s], ec="none", zorder=3))
            ax.text(x + BW / 2, v / 2 + YM * .075, str(v), ha="center", va="bottom", fontsize=17, fontweight="bold", color="#1F1F2E")
            ax.text(x + BW / 2, v / 2 + YM * .005, f"({100 * v / n0:.0f}%)", ha="center", va="bottom", fontsize=9.5, color="#666666")
            if s < 3:
                t = np.linspace(0, 1, 60); e = t * t * (3 - 2 * t)
                xs = x + BW + t * GAP; hw = (vals[s] + (vals[s + 1] - vals[s]) * e) / 2
                ax.fill_between(xs, -hw, hw, color=COLS[s], alpha=.45, lw=0, zorder=2)
        ax.set_xlim(-.1, 3 * (BW + GAP) + BW + .1); ax.set_ylim(-YM / 2 * 1.05, YM / 2 * 1.35)
        ax.set_xticks([s * (BW + GAP) + BW / 2 for s in range(4)]); ax.set_xticklabels(STAGES, fontsize=11, fontweight="bold")
        ax.set_yticks([]); ax.tick_params(axis="x", length=0, pad=8)
        for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color("#BBBBBB")
        ax.set_title(NAME[k], loc="left", fontsize=14, fontweight="bold", pad=10)
        if k in FOUND:
            ax.annotate(f"found {FOUND[k]:,} papers", xy=(0, 1), xycoords="axes fraction", xytext=(len(NAME[k]) * 9.5 + 12, 11.5), textcoords="offset points", fontsize=11, color="#666666", va="baseline")
    axes[0].set_ylabel("Number of papers")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, f"funnel_flow{suffix}.pdf"), bbox_inches="tight")

make(['GPT'], '_gpt')
print('ok')
