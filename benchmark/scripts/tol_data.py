"""Per-review tolerance table: |theta_auto - theta_GT| on the null-at-0 scale (log for ratios), for standardized measures (SMD, RR, OR, HR)."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from benchmark_metrics import d, ids, valid, tr, scale
from bench_load import MODELS, HERE
from paths import DATA, RUNS, FIG, RESULTS
STD = {"SMD", "RR", "OR", "HR"}
meta = {r["id"]: r for r in csv.DictReader(open(os.path.join(DATA, "reviews.csv")))}
def era(y):
    if not y: return None
    y = int(y); return "≤2009" if y <= 2009 else "2010–2015" if y <= 2015 else "2016–2020" if y <= 2020 else "2021+"
rows = []
for i in ids:
    g = d[(i, "GT")]
    if g["fam"] not in STD: continue
    tg = tr(g)
    for m in MODELS:
        p = d[(i, m)]; r = dict(id=i, model=m, fam=g["fam"], subfield=meta[i]["subfield"], era=era(meta[i]["first_year"]), status="ok")
        sc, inferred = scale(p)
        if not valid(p): r["status"] = "invalid"
        elif p["fam"] != g["fam"] or inferred: r["status"] = "other_measure"
        else:
            tp = tr(p); r.update(delta=abs(tp[0] - tg[0]), gx=tg, py=tp)
        rows.append(r)
if __name__ == "__main__":
    import collections
    for m in MODELS:
        rr = [r for r in rows if r["model"] == m]; ok = [r for r in rr if r["status"] == "ok"]
        print(m, len(rr), "ok", len(ok), "<=.05", sum(r["delta"] <= .05 for r in ok), "<=.20", sum(r["delta"] <= .20 for r in ok), collections.Counter(r["status"] for r in rr))
    print(collections.Counter(r["era"] for r in rows if r["model"] == "GPT"))
    print(collections.Counter(r["subfield"] for r in rows if r["model"] == "GPT"))
