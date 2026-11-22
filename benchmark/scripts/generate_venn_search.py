"""Venn diagrams (one per model): papers found by the search agent vs the ground truth (Cochrane's included studies, 863 trials from 100 reviews).
Overlap = included studies found (runs/search_overlap_<model>.csv TOTAL row); search only = found papers - overlap (the Cochrane review itself is already excluded
from the found counts); ground truth only = 863 - overlap. Circles are schematic (not area-proportional).
Output: figures/venn_search_vs_truth_gpt.pdf"""
import csv, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from paths import DATA, RUNS, FIG, RESULTS
M = [("GPT", "gpt-5.6-sol", "#0072B2")]
GT = "#7A7A7A"
plt.rcParams.update({"font.family": ["Liberation Sans", "DejaVu Sans"], "pdf.fonttype": 42})
def make(Ms, suffix):
    fig, axes = plt.subplots(1, len(Ms), figsize=(5 * len(Ms), 5.4), squeeze=False); axes = axes[0]
    for ax, (name, m, col) in zip(axes, Ms):
        t = [r for r in csv.DictReader(open(os.path.join(DATA, f"search_overlap_{m}.csv"), encoding="utf-8")) if r["review_id"].startswith("TOTAL")][0]
        found, gt, ov = int(t["n_found_papers"]), int(t["n_included_studies"]), int(t["n_overlap"])
        ax.add_patch(Circle((-.65, 0), 1.25, fc=col, ec=col, alpha=.28, lw=0)); ax.add_patch(Circle((-.65, 0), 1.25, fc="none", ec=col, lw=2))
        ax.add_patch(Circle((.65, 0), 1.25, fc=GT, ec=GT, alpha=.28, lw=0)); ax.add_patch(Circle((.65, 0), 1.25, fc="none", ec=GT, lw=2))
        for x, v in ((-1.25, found - ov), (0, ov), (1.25, gt - ov)):
            ax.text(x, 0, f"{v:,}", ha="center", va="center", fontsize=18, fontweight="bold", color="#1F1F2E")
        ax.text(-.95, 1.45, "AutoSynthesis", ha="center", va="bottom", fontsize=12, fontweight="bold", color=col, linespacing=1.25)
        ax.text(.95, 1.45, "Benchmark", ha="center", va="bottom", fontsize=12, fontweight="bold", color=GT, linespacing=1.25)
        ax.text(0, -1.6, f"{100 * ov / gt:.1f}% of the benchmark found", ha="center", va="top", fontsize=11.5, color="#444444")
        ax.set_title(name, fontsize=15, fontweight="bold", color=col, pad=8)
        ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1.9, 2.3); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, f"venn_search_vs_truth{suffix}.pdf"), bbox_inches="tight")
make(M, '_gpt')
