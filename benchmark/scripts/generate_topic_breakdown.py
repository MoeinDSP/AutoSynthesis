"""Unit-free breakdown by Cochrane's own 'Browse by Topic' (one topic per review, from
cochrane_benchmark/cochrane_titles_codes - cochrane_titles_codes.csv.csv), all 100 reviews, every effect measure.
Same measure as unitfree_breakdown.pdf: share of reviews whose pooled effect lies within T of the Cochrane effect (unit-free);
a review with no comparable result counts as 'not within', so the n of all topics sums to 100.
Outputs: topic_breakdown_unitfree_025.pdf (unit-free cut-off 0.25, all 100 reviews) and topic_breakdown_strict_005.pdf
(the paper's strict tolerance +/-0.05, standardized measures only = 76 reviews; the n of all topics sums to 76)."""
import csv, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rel_data import rows, MODELS, HERE, T1, T2
from paths import DATA, FIG
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude Opus 5"}
COL = {"GPT": "#0072B2", "Gemini": "#E69F00", "Claude": "#009E73"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "pdf.fonttype": 42})
TOPIC_FILE = os.path.join(DATA, "reviews.csv")
FIX = {"Kidney condition": "Kidney conditions"}   # singular/plural typo in the sheet; same Cochrane topic

topic = {}
for r in csv.DictReader(open(TOPIC_FILE, encoding="utf-8-sig")):
    t = r["cochrane_topic"].strip()
    topic[r["id"].strip()] = FIX.get(t, t)
assert len(topic) == 100 and all(topic.values())


MIN_N = 4


def breakdown(T, fname, pool=False):
    """pool=True: topics with fewer than MIN_N reviews are pooled into 'Other topics (k topics)' so every row is readable."""
    tp = dict(topic)
    if pool:
        cnt = {g: sum(v == g for v in topic.values()) for g in set(topic.values())}
        small = [g for g, c in cnt.items() if c < MIN_N]
        lab = f"Other topics ({len(small)} topics)"
        tp = {i: (lab if cnt[t] < MIN_N else t) for i, t in topic.items()}
    groups = sorted({t for t in tp.values()}, key=lambda g: (g.startswith("Other topics"), -sum(v == g for v in tp.values()), g))
    ns = [sum(v == g for v in tp.values()) for g in groups]
    assert sum(ns) == 100
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(groups) + 1.6))
    for gi, g in enumerate(groups):
        y = len(groups) - 1 - gi
        for k, m in enumerate(MODELS):
            R = [r for r in rows if r["model"] == m and tp[r["id"]] == g]
            v = 100 * sum(r["status"] == "ok" and r["rel"] <= T for r in R) / len(R)
            ax.plot(v, y + (1 - k) * .2, "o", color=COL[m], ms=8, label=NAMES[m] if gi == 0 else None)
        ax.axhline(y, color="#EEEEEE", lw=1, zorder=0)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels([f"{g}  ($n$={n})" for g, n in zip(reversed(groups), reversed(ns))])
    ax.set_xlim(-3, 105)
    ax.set_xlabel(f"Within {T:.2f} (%)")
    ax.set_title("Cochrane topic", loc="left", fontsize=13, fontweight="bold")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.01))
    fig.tight_layout(rect=(0, .04, 1, 1))
    fig.savefig(os.path.join(FIG, fname), bbox_inches="tight")
    plt.close(fig)
    print(fname, len(groups), "topics")


ERAS = ["≤2009", "2010–2015", "2016–2020", "2021+", "Year unknown"]


def breakdown_year_topic(T=T2, fname="unitfree_breakdown_year_topic_025.pdf"):
    """Two panels, all 100 reviews, every effect measure: year of first publication | Cochrane topic (topics with < MIN_N reviews pooled).
    Share of reviews within T of the Cochrane CI width; reviews with no comparable result count as 'not within'."""
    cnt = {g: sum(v == g for v in topic.values()) for g in set(topic.values())}
    small = [g for g, c in cnt.items() if c < MIN_N]
    lab = f"Other topics ({len(small)} topics)"
    tp = {i: (lab if cnt[t] < MIN_N else t) for i, t in topic.items()}
    tg = sorted(set(tp.values()), key=lambda g: (g.startswith("Other topics"), -sum(v == g for v in tp.values()), g))
    panels = [("Year of first publication", ERAS, lambda r: r["era"] or "Year unknown"), ("Cochrane topic", tg, lambda r: tp[r["id"]])]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={"width_ratios": [1, 1.35]})
    for ax, (title, groups, f) in zip(axes, panels):
        ns = []
        for gi, g in enumerate(groups):
            y = len(groups) - 1 - gi
            for k, m in enumerate(MODELS):
                R = [r for r in rows if r["model"] == m and f(r) == g]
                v = 100 * sum(r["status"] == "ok" and r["rel"] <= T for r in R) / len(R)
                ax.plot(v, y + (1 - k) * .2, "o", color=COL[m], ms=8, label=NAMES[m] if gi == 0 else None)
            ax.axhline(y, color="#EEEEEE", lw=1, zorder=0)
            ns.append(len([r for r in rows if r["model"] == "GPT" and f(r) == g]))
        assert sum(ns) == 100, ns
        ax.set_yticks(range(len(groups))); ax.set_yticklabels([f"{g}  ($n$={n})" for g, n in zip(reversed(groups), reversed(ns))])
        ax.set_xlim(-3, 105); ax.set_xlabel(f"Within {T:.2f} (%)"); ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    h, l = axes[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.01))
    fig.tight_layout(rect=(0, .05, 1, 1)); fig.savefig(os.path.join(FIG, fname), bbox_inches="tight"); plt.close(fig)
    print(fname)


BLUES = ["#1F3864", "#6C8EBF", "#C9D6EA"]   # within strict / within broad (beyond strict) / beyond -- the blues of the tolerance-bar slide


def breakdown_strict(fname="topic_breakdown_strict_005.pdf"):
    """Three-level version with the paper's tolerances: within +/-0.05, within +/-0.20 (beyond 0.05) and beyond +/-0.20, per Cochrane topic,
    one panel per model. Standardized measures (SMD, RR, OR, HR; ratios on the log scale) = 76 reviews; each bar is a share of the reviews of that
    topic with a comparable result for that model (its n is printed at the right end of the bar)."""
    from tol_data import rows as trows
    ids = sorted({r["id"] for r in trows})
    groups = sorted({topic[i] for i in ids}, key=lambda g: (-sum(topic[i] == g for i in ids), g))
    ns = [sum(topic[i] == g for i in ids) for g in groups]
    assert sum(ns) == 76 == len(ids)
    fig, axes = plt.subplots(1, 3, figsize=(14, 0.36 * len(groups) + 1.7), sharey=True)
    for ax, m in zip(axes, MODELS):
        for gi, g in enumerate(groups):
            y = len(groups) - 1 - gi
            d = [r["delta"] for r in trows if r["model"] == m and topic[r["id"]] == g and r["status"] == "ok"]
            n = len(d)
            if n:
                p1 = 100 * sum(x <= .05 for x in d) / n
                p2 = 100 * sum(.05 < x <= .20 for x in d) / n
                p3 = 100 - p1 - p2
                left = 0
                for p, col, tcol in ((p1, BLUES[0], "white"), (p2, BLUES[1], "white"), (p3, BLUES[2], "#222222")):
                    ax.barh(y, p, left=left, height=.72, color=col, edgecolor="white", lw=.6)
                    if p >= 14: ax.text(left + p / 2, y, f"{p:.0f}%", ha="center", va="center", fontsize=7.5, fontweight="bold", color=tcol)
                    left += p
            ax.text(102, y, f"$n$={n}" if n else "not comparable", va="center", fontsize=8, color="#555555")
        ax.set_xlim(0, 100); ax.set_ylim(-.6, len(groups) - .4)
        ax.set_title(NAMES[m], loc="left", fontsize=12, fontweight="bold")
        ax.set_xlabel("Share of reviews (%)", fontsize=10)
        for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(groups)))
    axes[0].set_yticklabels([f"{g}  ($n$={n})" for g, n in zip(reversed(groups), reversed(ns))], fontsize=10)
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(fc=BLUES[0], label="within ±0.05"), Patch(fc=BLUES[1], label="within ±0.20 (beyond ±0.05)"), Patch(fc=BLUES[2], label="beyond ±0.20")],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.005))
    fig.tight_layout(rect=(0, .035, 1, 1))
    fig.savefig(os.path.join(FIG, fname), bbox_inches="tight")
    plt.close(fig)
    print(fname, len(groups), "topics")


if __name__ == "__main__":
    breakdown(T2, "topic_breakdown_unitfree_025.pdf")
    breakdown(T2, "topic_breakdown_unitfree_025_pooled.pdf", pool=True)
    breakdown_year_topic()
    breakdown_strict()
