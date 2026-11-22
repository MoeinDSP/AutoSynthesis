"""Independent audit of the statistical analysis for a sample of benchmark runs (GPT-5.6 Sol).

For each review: recompute every study's effect in the Cochrane measure from the raw inputs the pipeline extracted,
re-pool with metafor (REML, as the pipeline; and DerSimonian-Laird, as RevMan), compare with the pipeline's pooled
result, and run sanity checks (duplicates, impossible values, extracted numbers present verbatim in the paper text).
Run inside the app container (needs R + metafor via rpy2). Writes audit_statistics.csv and prints a report.
"""
import csv, glob, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from benchmark_metrics import d as BENCH
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
metafor = importr("metafor")

from paths import DATA, RUNS, FIG, RESULTS
SAMPLE = ["CD007044", "CD004661", "CD002290", "CD013844", "CD001396", "CD004692", "CD006761", "CD012746", "CD003677", "CD014805"]
RATIO = {"RR", "OR", "HR"}


def study_effect(es, fam):
    """(yi, vi, note) for one study in the Cochrane measure, from the raw extracted inputs; None if not computable."""
    x = es.get("raw_measure_inputs") or {}
    if fam in ("RR", "OR"):
        a, c, n1, n2 = (x.get(k) for k in ("events_treatment", "events_control", "n_treatment", "n_control"))
        if None not in (a, c, n1, n2):
            if a == 0 or c == 0 or a == n1 or c == n2: a, c, n1, n2 = a + .5, c + .5, n1 + 1, n2 + 1
            if fam == "RR": return math.log((a / n1) / (c / n2)), 1 / a - 1 / n1 + 1 / c - 1 / n2, "counts"
            return math.log(a / (n1 - a) / (c / (n2 - c))), 1 / a + 1 / (n1 - a) + 1 / c + 1 / (n2 - c), "counts"
        r, lo, hi = x.get("reported_ratio"), x.get("reported_ratio_ci_lower"), x.get("reported_ratio_ci_upper")
        if None not in (r, lo, hi) and min(r, lo, hi) > 0:
            return math.log(r), ((math.log(hi) - math.log(lo)) / 3.92) ** 2, f"reported {x.get('reported_ratio_measure')}"
        return None
    if fam == "HR":
        r, lo, hi = x.get("reported_ratio"), x.get("reported_ratio_ci_lower"), x.get("reported_ratio_ci_upper")
        if None not in (r, lo, hi) and min(r, lo, hi) > 0:
            return math.log(r), ((math.log(hi) - math.log(lo)) / 3.92) ** 2, f"reported {x.get('reported_ratio_measure')}"
        return None
    mt, st, mc, sc, nt, nc = (x.get(k) for k in ("mean_treatment", "sd_treatment", "mean_control", "sd_control", "n_treatment", "n_control"))
    if fam == "MD" and None not in (mt, st, mc, sc, nt, nc) and st > 0 and sc > 0:
        return mt - mc, st ** 2 / nt + sc ** 2 / nc, "means/SDs"
    if fam == "SMD" and es.get("hedges_g") is not None and es.get("variance"):
        return es["hedges_g"], es["variance"], es.get("computation_method") or "g"
    return None


def pool(yi, vi, method):
    res = metafor.rma(yi=ro.FloatVector(yi), vi=ro.FloatVector(vi), method=method)
    g = lambda k: float(res.rx2(k)[0])
    return g("b"), g("ci.lb"), g("ci.ub")


def numbers_in_text(es, text):
    """Share of distinctive extracted numbers (decimals and counts >= 10) that appear verbatim in the paper text."""
    x = es.get("raw_measure_inputs") or {}
    vals = []
    for k, v in x.items():
        if not isinstance(v, (int, float)) or k.startswith("scale_"): continue
        if float(v).is_integer():
            if v >= 10: vals.append(str(int(v)))
        else:
            vals.append(f"{v:g}")
    if not vals: return None, []
    missing = [v for v in vals if not re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", text)]
    return 1 - len(missing) / len(vals), missing


rows = []
for cid in SAMPLE:
    run = os.path.join(RUNS, cid, "gpt-5.6-sol")
    es = json.load(open(os.path.join(run, "effect_sizes.json")))
    meta = json.load(open(os.path.join(run, "meta_analysis_result.json")))
    mr = {}
    for r in json.load(open(os.path.join(run, "meta_ready_results.json"))):
        mnum = re.search(r"(\d+)$", str(r.get("study_label") or ""))
        if mnum: mr["study_" + mnum.group(1)] = r
    texts = {os.path.basename(p): open(p, errors="ignore").read() for p in glob.glob(os.path.join(run, "fulltext_*.md"))}
    g = BENCH[(cid, "GT")]; fam = g["fam"]
    yi, vi, notes, issues = [], [], [], []
    seen = {}
    for e in es:
        r = study_effect(e, fam)
        key = json.dumps(e.get("raw_measure_inputs"), sort_keys=True)
        if key in seen: issues.append(f"{e['study_id']} has identical inputs to {seen[key]} (possible double counting)")
        seen[key] = e["study_id"]
        x = e.get("raw_measure_inputs") or {}
        for a, n in (("events_treatment", "n_treatment"), ("events_control", "n_control")):
            if x.get(a) is not None and x.get(n) is not None and x[a] > x[n]: issues.append(f"{e['study_id']}: events > n")
        if r is None: issues.append(f"{e['study_id']}: no raw inputs for {fam} (method {e.get('computation_method')})"); continue
        yi.append(r[0]); vi.append(r[1]); notes.append(r[2])
        # verbatim check against the paper this study came from
        title = (mr.get(e["study_id"]) or {}).get("Title") or ""
        sid = ((mr.get(e["study_id"]) or {}).get("Study_ID") or "").split(":")[-1]
        txt = next((t for f, t in texts.items() if sid and sid in f), None)
        if txt is None and title:
            words = [w for w in re.findall(r"[a-z]{5,}", title.lower())][:6]
            txt = next((t for t in texts.values() if words and sum(w in t.lower()[:4000] for w in words) >= max(3, len(words) - 2)), None)
        if txt is not None:
            share, missing = numbers_in_text(e, txt)
            if share is not None and share < 1: issues.append(f"{e['study_id']}: not found verbatim in paper: {missing}")
            if share is not None: notes[-1] += f" | verbatim {share:.0%}"
        else:
            notes[-1] += " | paper text not matched"
    out = dict(id=cid, fam=fam, k_pipeline=meta.get("k"), k_recomputed=len(yi), k_cochrane=g["k"])
    pe, plo, phi = meta["pooled_effect"], meta["ci_lower"], meta["ci_upper"]
    out.update(pipeline=f"{pe:.3f} [{plo:.3f}, {phi:.3f}]", cochrane=f"{g['eff']} [{g['lo']}, {g['hi']}]")
    if len(yi) >= 2:
        for m in ("REML", "DL"):
            b, lo, hi = pool(yi, vi, m)
            if fam in RATIO: b, lo, hi = math.exp(b), math.exp(lo), math.exp(hi)
            out[f"recomputed_{m}"] = f"{b:.3f} [{lo:.3f}, {hi:.3f}]"
        b = float(out["recomputed_REML"].split()[0])
        rel = abs(b - pe) / max(abs(pe), 1e-9)
        out["matches_pipeline"] = "yes" if rel < 0.02 else f"no ({rel:.0%} diff)"
    out["issues"] = "; ".join(issues) or "none"
    out["inputs"] = "; ".join(sorted(set(n.split(" | ")[0] for n in notes)))
    out["verbatim"] = ", ".join(n.split(" | ")[1] for n in notes if " | " in n)
    rows.append(out)
    print(f"\n== {cid} ({fam}) k pipeline/recomputed/Cochrane = {out['k_pipeline']}/{out['k_recomputed']}/{out['k_cochrane']}")
    for k in ("pipeline", "recomputed_REML", "recomputed_DL", "cochrane", "matches_pipeline", "inputs", "verbatim", "issues"):
        print(f"   {k}: {out.get(k)}")

with open(os.path.join(RESULTS, "audit_statistics.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(dict.fromkeys(k for r in rows for k in r))); w.writeheader(); w.writerows(rows)
