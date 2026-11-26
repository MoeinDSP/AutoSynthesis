"""Sensitivity analysis: does the agreement with Cochrane depend on the pooling model?

For every review and LLM, the run's own study-level data (rebuilt in Cochrane's effect measure, see
repool_from_runs.study_effects) are pooled again with

  REML  random effects, restricted maximum likelihood (the AutoSynthesis default)
  DL    random effects, DerSimonian-Laird
  FE    fixed effect (inverse variance)
  UWLS  unrestricted weighted least squares (Stanley & Doucouliagos 2015)
  Cochrane model   the model of the Cochrane analysis itself: DL when Cochrane used random effects
                   (as RevMan), FE when it used a fixed effect (data/cochrane_pooling_models.csv)

and each result is compared with Cochrane's estimate, with the same metrics as the main benchmark:
|delta| on the null-at-0 scale within 0.05 / 0.20 (standardized measures: SMD, RR, OR, HR), Pearson r,
and the same conclusion (direction and significance, all reviews). Nothing is re-extracted and no LLM is called.
Where a run's study data cannot be rebuilt in Cochrane's measure (for example no 2x2 counts), the review is
left out for that LLM and counted in `not_rebuilt`.

Writes results/sensitivity_pooling_models.csv (per review, LLM and model) and
results/sensitivity_pooling_models_summary.csv, and figures/sensitivity_pooling_models.pdf.
"""
import csv, io, contextlib, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats

with contextlib.redirect_stdout(io.StringIO()):
    from benchmark_metrics import d, ids
from bench_load import MODELS, RATIO
from paths import DATA, FIG, RESULTS
from repool_from_runs import study_effects

STD = {"SMD", "RR", "OR", "HR"}
Z = stats.norm.ppf(0.975)
METHODS = ["REML", "DL", "FE", "UWLS", "Cochrane model"]


# ── pooling models (numpy; checked against R metafor in the AutoSynthesis test suite) ──────────────────────
def _fe(y, v):
    w = 1 / v
    est = (w * y).sum() / w.sum()
    return est, math.sqrt(1 / w.sum())


def _re(y, v, tau2):
    w = 1 / (v + tau2)
    est = (w * y).sum() / w.sum()
    return est, math.sqrt(1 / w.sum())


def tau2_dl(y, v):
    w = 1 / v
    fe = (w * y).sum() / w.sum()
    q = (w * (y - fe) ** 2).sum()
    c = w.sum() - (w ** 2).sum() / w.sum()
    return max(0.0, (q - (len(y) - 1)) / c) if c > 0 else 0.0


def tau2_reml(y, v, tol=1e-10, maxit=1000):
    """REML estimate of tau^2 by Fisher scoring, starting from DL, truncated at 0 (as metafor)."""
    t2 = tau2_dl(y, v)
    for _ in range(maxit):
        w = 1 / (v + t2)
        est = (w * y).sum() / w.sum()
        # REML score and information for tau^2
        P_trace = w.sum() - (w ** 2).sum() / w.sum()
        res = y - est
        score = 0.5 * ((w ** 2 * res ** 2).sum() - P_trace)
        info = 0.5 * ((w ** 2).sum() - 2 * (w ** 3).sum() / w.sum() + ((w ** 2).sum() / w.sum()) ** 2)
        new = max(0.0, t2 + score / info)
        if abs(new - t2) < tol:
            return new
        t2 = new
    return t2


def pool(y, v, method):
    """-> (estimate, ci_lower, ci_upper) on the scale of y."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    if k == 1:
        se = math.sqrt(v[0]); return y[0], y[0] - Z * se, y[0] + Z * se
    if method == "FE":
        est, se = _fe(y, v)
    elif method == "DL":
        est, se = _re(y, v, tau2_dl(y, v))
    elif method == "REML":
        est, se = _re(y, v, tau2_reml(y, v))
    elif method == "UWLS":
        est, se_fe = _fe(y, v)
        mse = ((y - est) ** 2 / v).sum() / (k - 1)
        se = se_fe * math.sqrt(mse)
        t = stats.t.ppf(0.975, k - 1)
        return est, est - t * se, est + t * se
    else:
        raise ValueError(method)
    return est, est - Z * se, est + Z * se


# ── Cochrane's own pooling model per review ───────────────────────────────────────────────────────────────
CMODEL = {r["review_id"]: r for r in csv.DictReader(open(os.path.join(DATA, "cochrane_pooling_models.csv")))}


def to0(fam, e, lo, hi):
    """Effect and CI on the null-at-0 scale (log for ratios)."""
    return (math.log(e), math.log(lo), math.log(hi)) if fam in RATIO else (e, lo, hi)


def category(lo, hi):
    return "sig_neg" if hi < 0 else ("sig_pos" if lo > 0 else "ns")


rows = []
for i in ids:
    g = d[(i, "GT")]
    fam = g["fam"]
    tg = to0(fam, g["eff"], g["lo"], g["hi"])
    cm = CMODEL[i]["model"]
    for m in MODELS:
        ys, notes, _k_run = study_effects(i, m, fam)
        if not ys:
            rows.append(dict(id=i, llm=m, measure=fam, cochrane_model=cm, method="", status="not_rebuilt"))
            continue
        y = [a for a, _ in ys]; v = [b for _, b in ys]
        for method in METHODS:
            use = ("DL" if cm == "Random" else "FE") if method == "Cochrane model" else method
            est, lo, hi = pool(y, v, use)
            delta = abs(est - tg[0])
            rows.append(dict(
                id=i, llm=m, measure=fam, cochrane_model=cm, method=method, fitted_as=use, k=len(y), status="ok",
                estimate=round(math.exp(est) if fam in RATIO else est, 4),
                ci_lower=round(math.exp(lo) if fam in RATIO else lo, 4),
                ci_upper=round(math.exp(hi) if fam in RATIO else hi, 4),
                cochrane_estimate=g["eff"], cochrane_ci_lower=g["lo"], cochrane_ci_upper=g["hi"],
                abs_delta=round(delta, 4) if fam in STD else "",
                same_conclusion=int(category(lo, hi) == category(tg[1], tg[2])),
                _y=est, _g=tg[0]))

os.makedirs(RESULTS, exist_ok=True)
fields = ["id", "llm", "measure", "cochrane_model", "method", "fitted_as", "k", "status", "estimate", "ci_lower",
          "ci_upper", "cochrane_estimate", "cochrane_ci_lower", "cochrane_ci_upper", "abs_delta", "same_conclusion"]
with open(os.path.join(RESULTS, "sensitivity_pooling_models.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def wilson(x, n):
    if n == 0: return (float("nan"),) * 2
    p = x / n; den = 1 + Z ** 2 / n
    c = (p + Z ** 2 / (2 * n)) / den; h = Z * math.sqrt(p * (1 - p) / n + Z ** 2 / (4 * n * n)) / den
    return c - h, c + h


summary = []
for m in MODELS:
    not_rebuilt = sum(1 for r in rows if r["llm"] == m and r["status"] == "not_rebuilt")
    for method in METHODS:
        R = [r for r in rows if r["llm"] == m and r["method"] == method and r["status"] == "ok"]
        S = [r for r in R if r["measure"] in STD]
        dl_ = np.array([r["abs_delta"] for r in S], float)
        n = len(S); w05 = int((dl_ <= 0.05).sum()); w20 = int((dl_ <= 0.20).sum())
        r_ = stats.pearsonr([r["_y"] for r in S], [r["_g"] for r in S])[0] if n > 2 else float("nan")
        conc = sum(r["same_conclusion"] for r in R)
        lo05, hi05 = wilson(w05, n); lo20, hi20 = wilson(w20, n)
        summary.append(dict(llm=m, method=method, n_standardized=n, within_0_05=w05, pct_0_05=round(100 * w05 / n, 1),
                            ci_0_05=f"[{100 * lo05:.1f}, {100 * hi05:.1f}]", within_0_20=w20, pct_0_20=round(100 * w20 / n, 1),
                            ci_0_20=f"[{100 * lo20:.1f}, {100 * hi20:.1f}]", median_abs_delta=round(float(np.median(dl_)), 3),
                            pearson_r=round(float(r_), 3), n_all=len(R), same_conclusion=conc,
                            pct_same_conclusion=round(100 * conc / len(R), 1), not_rebuilt=not_rebuilt))
with open(os.path.join(RESULTS, "sensitivity_pooling_models_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)

# ── figure: share within +/-0.20 and +/-0.05 per pooling model and LLM ─────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"],
                     "font.size": 9, "pdf.fonttype": 42})
NAMES = {"GPT": "GPT-5.6 Sol", "Gemini": "Gemini 3.8 Flash", "Claude": "Claude Opus 5"}
COLORS = {"GPT": "#2b6cb0", "Gemini": "#2f855a", "Claude": "#c05621"}
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
x = np.arange(len(METHODS)); bw = 0.26
for ax, (col, ci_col, title) in zip(axes, [("pct_0_20", "ci_0_20", "Within ±0.20"), ("pct_0_05", "ci_0_05", "Within ±0.05")]):
    for j, m in enumerate(MODELS):
        S = [s for s in summary if s["llm"] == m]
        vals = [s[col] for s in S]
        cis = [[float(t) for t in s[ci_col].strip("[]").split(",")] for s in S]
        err = np.array([[v - c[0] for v, c in zip(vals, cis)], [c[1] - v for v, c in zip(vals, cis)]])
        ax.bar(x + (j - 1) * bw, vals, bw, color=COLORS[m], label=NAMES[m], yerr=err, capsize=1.5,
               error_kw=dict(lw=0.6, ecolor="#444"))
    ax.set_xticks(x); ax.set_xticklabels(["REML", "DL", "FE", "UWLS", "Cochrane's\nmodel"])
    ax.set_title(title, fontsize=9); ax.set_ylim(0, 100)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("Reviews (%)")
axes[1].legend(frameon=False, fontsize=7.5, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "sensitivity_pooling_models.pdf"))

if __name__ == "__main__":
    for s in summary:
        print(f"{s['llm']:7s} {s['method']:15s} n={s['n_standardized']:3d} ±0.20 {s['within_0_20']:3d} ({s['pct_0_20']:5.1f}%) "
              f"±0.05 {s['within_0_05']:3d} ({s['pct_0_05']:5.1f}%) r={s['pearson_r']:.3f} "
              f"conclusion {s['same_conclusion']}/{s['n_all']}  not rebuilt {s['not_rebuilt']}")
