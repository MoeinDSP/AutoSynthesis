"""Unit-free comparison for ALL measures: rel = |theta_auto - theta_GT| / (width of the Cochrane 95% CI), on the null-at-0 scale (log for ratios).
Only reviews where the model used the same effect measure as Cochrane and gave a valid result. 'std' = SMD, RR, OR, HR; 'diff' = MD, RD."""
import csv, io, contextlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from benchmark_metrics import d, ids, valid, tr, scale
from bench_load import MODELS, HERE
from paths import DATA, RUNS, FIG, RESULTS
meta = {r["id"]: r for r in csv.DictReader(open(os.path.join(DATA, "reviews.csv")))}
def era(y):
    if not y: return None
    y = int(y); return "≤2009" if y <= 2009 else "2010–2015" if y <= 2015 else "2016–2020" if y <= 2020 else "2021+"
T1, T2 = .10, .25
rows = []
for i in ids:
    g = d[(i, "GT")]; tg = tr(g); W = tg[2] - tg[1]
    grp = "std" if g["fam"] in ("SMD", "RR", "OR", "HR") else "diff"
    for m in MODELS:
        p = d[(i, m)]; sc, inf = scale(p)
        r = dict(id=i, model=m, fam=g["fam"], group=grp, subfield=meta[i]["subfield"], era=era(meta[i]["first_year"]), W=W, status="ok")
        if not valid(p): r["status"] = "invalid"
        elif p["fam"] != g["fam"] or inf: r["status"] = "other_measure"
        else:
            tp = tr(p); r.update(gx=tg, py=tp, rel=abs(tp[0] - tg[0]) / W)
        rows.append(r)
def ok(m, **kw): return [r for r in rows if r["model"] == m and r["status"] == "ok" and all(r[k] == v for k, v in kw.items())]
if __name__ == "__main__":
    import numpy as np
    for m in MODELS:
        for grp in ("std", "diff"):
            R = ok(m, group=grp); v = np.array([r["rel"] for r in R])
            print(m, grp, len(R), "<=.10:", (v <= T1).sum(), "<=.25:", (v <= T2).sum(), "median %.3f mean %.3f max %.2f" % (np.median(v), v.mean(), v.max()))
        R = ok(m); x = np.array([r["gx"][0] / r["W"] for r in R]); print("  theta/W range", x.min().round(1), x.max().round(1), "pct |.|>4:", (abs(x) > 4).sum())
