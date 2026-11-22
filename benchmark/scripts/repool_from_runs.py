"""Re-pool a model's own extracted study data in the Cochrane effect measure.

Used for benchmark rows a formula cannot convert (MD <-> SMD needs the study SDs) and for invalid pooled results.
Nothing is re-extracted: the per-study inputs come from the run's saved effect_sizes.json (raw means/SDs/counts,
Hedges' g + variance), plus the mean/SD the pipeline itself estimated from medians (Wan et al. 2014), which it
records in meta_ready_results.json. Pooling: DerSimonian-Laird random effects, 95% z-interval (as RevMan).

Writes repooled_results.csv: id, model, fam, eff, lo, hi, k, k_run, note. benchmark_metrics.harmonize() uses it.
"""
import csv, io, contextlib, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bench_load import HERE, MODELS, RATIO

from paths import DATA, RUNS, FIG, RESULTS
RUN_DIR = {"GPT": "gpt-5.6-sol", "Gemini": "gemini-3.8-flash", "Claude": "claude"}
OUT = os.path.join(DATA, "repooled_results.csv")

# unit -> (dimension, factor to the dimension's base unit)
UNITS = {"s": ("time", 1 / 60), "sec": ("time", 1 / 60), "second": ("time", 1 / 60), "min": ("time", 1.0), "minute": ("time", 1.0),
         "h": ("time", 60.0), "hr": ("time", 60.0), "hour": ("time", 60.0),
         "mm": ("length", 0.1), "cm": ("length", 1.0), "m": ("length", 100.0),
         "g": ("mass", 0.001), "kg": ("mass", 1.0)}


def _unit(u):
    u = (u or "").strip().lower()
    m = re.match(r"^([a-z]+?)s?\b", u)
    return UNITS.get(m.group(1)) if m else None


def dl(effects):
    """DerSimonian-Laird random effects. effects: [(y, v)] -> (est, lo, hi)."""
    w = [1 / v for _, v in effects]
    fe = sum(wi * y for (y, _), wi in zip(effects, w)) / sum(w)
    q = sum(wi * (y - fe) ** 2 for (y, _), wi in zip(effects, w))
    c = sum(w) - sum(wi * wi for wi in w) / sum(w)
    tau2 = max(0.0, (q - (len(effects) - 1)) / c) if c > 0 else 0.0
    ws = [1 / (v + tau2) for _, v in effects]
    est = sum(wi * y for (y, _), wi in zip(effects, ws)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    return est, est - 1.96 * se, est + 1.96 * se


def _wan_estimates(run):
    """study_label 'Study N' -> (mean_t, sd_t, mean_c, sd_c) the pipeline estimated from medians and logged."""
    out = {}
    p = os.path.join(run, "meta_ready_results.json")
    if not os.path.exists(p): return out
    for r in json.load(open(p)):
        m = re.search(r"treatment mean=([-\d.]+) SD=([-\d.]+), control mean=([-\d.]+) SD=([-\d.]+)", r.get("Comment") or "")
        lab = re.search(r"(\d+)$", str(r.get("study_label") or ""))
        if m and lab: out[f"study_{lab.group(1)}"] = tuple(float(x) for x in m.groups())
    return out


def repool(cid, model, fam):
    run = os.path.join(RUNS, cid, RUN_DIR[model])
    p = os.path.join(run, "effect_sizes.json")
    if not os.path.exists(p):
        # no saved study data: use a rerun (same prompt and PDFs) when one exists and pooled in the Cochrane measure
        rr = os.path.join(RUNS, f"{cid}_rerun", RUN_DIR[model], "meta_analysis_result.json")
        if os.path.exists(rr):
            m = json.load(open(rr))
            if (m.get("effect_measure") or "").upper() == fam and None not in (m.get("pooled_effect"), m.get("ci_lower"), m.get("ci_upper")):
                return dict(id=cid, model=model, fam=fam, eff=m["pooled_effect"], lo=m["ci_lower"], hi=m["ci_upper"], k=m.get("k"),
                            k_run=m.get("k"), note="rerun (same prompt and PDFs; original run saved no study data)"), None
        return None, "no saved study data (run produced no effect sizes)"
    rows = json.load(open(p)); wan = _wan_estimates(run)
    ys, notes = [], []
    if fam == "MD":
        per = []
        for r in rows:
            x = r.get("raw_measure_inputs") or {}
            mt, st_, mc, sc = (x.get(k) for k in ("mean_treatment", "sd_treatment", "mean_control", "sd_control"))
            nt, nc = x.get("n_treatment"), x.get("n_control")
            if None in (mt, mc) and r["study_id"] in wan:
                mt, st_, mc, sc = wan[r["study_id"]]; notes.append(f"{r['study_id']} mean/SD from median (Wan)")
            if None in (mt, st_, mc, sc, nt, nc) or not (st_ > 0 and sc > 0): notes.append(f"{r['study_id']} dropped: no mean/SD"); continue
            per.append((mt - mc, st_ ** 2 / nt + sc ** 2 / nc, _unit(r.get("outcome_units"))))
        dims = [u for _, _, u in per if u]
        if dims:                                           # bring every study to the most common unit
            from collections import Counter
            base = Counter(dims).most_common(1)[0][0]
            for y, v, u in per:
                f = (u[1] / base[1]) if (u and u[0] == base[0]) else 1.0
                if f != 1.0: notes.append(f"unit rescaled x{f:.4g}")
                ys.append((y * f, v * f * f))
        else:
            ys = [(y, v) for y, v, _ in per]
    elif fam == "SMD":
        ys = [(r["hedges_g"], r["variance"]) for r in rows if r.get("hedges_g") is not None and r.get("variance")]
    elif fam in RATIO:                                     # binary counts -> log RR (log OR for OR)
        for r in rows:
            x = r.get("raw_measure_inputs") or {}
            a, c, n1, n2 = (x.get(k) for k in ("events_treatment", "events_control", "n_treatment", "n_control"))
            if None in (a, c, n1, n2): notes.append(f"{r['study_id']} dropped: no counts"); continue
            if a == 0 or c == 0: a, c, n1, n2 = a + .5, c + .5, n1 + 1, n2 + 1
            if fam == "OR": ys.append((math.log(a / (n1 - a) / (c / (n2 - c))), 1 / a + 1 / (n1 - a) + 1 / c + 1 / (n2 - c)))
            else: ys.append((math.log((a / n1) / (c / n2)), 1 / a - 1 / n1 + 1 / c - 1 / n2))
    if not ys: return None, "; ".join(notes) or "no usable study data"
    est, lo, hi = dl(ys)
    if fam in RATIO: est, lo, hi = math.exp(est), math.exp(lo), math.exp(hi)
    return dict(id=cid, model=model, fam=fam, eff=est, lo=lo, hi=hi, k=len(ys), k_run=len(rows), note="; ".join(dict.fromkeys(notes))), None


if __name__ == "__main__":
    os.environ["BENCH_HARMONIZE_NO_REPOOL"] = "1"         # find what formulas alone cannot convert
    with contextlib.redirect_stdout(io.StringIO()):
        from benchmark_metrics import d, ids, valid, scale
    out, failed = [], []
    for i in ids:
        g = d[(i, "GT")]
        for m in MODELS:
            p = d[(i, m)]
            if valid(p) and p["fam"] == g["fam"] and not scale(p)[1]: continue
            r, why = repool(i, m, g["fam"])
            if r: out.append(r); print(f"{i} {m}: {g['fam']} {r['eff']:.3f} [{r['lo']:.3f}, {r['hi']:.3f}] k={r['k']}/{r['k_run']} | GT {g['eff']} [{g['lo']}, {g['hi']}] {r['note']}")
            else: failed.append((i, m, why)); print(f"{i} {m}: NOT RECOVERED - {why}")
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "model", "fam", "eff", "lo", "hi", "k", "k_run", "note"]); w.writeheader(); w.writerows(out)
    print(f"\nrecovered {len(out)}, still need a rerun {len(failed)}: {[(i, m) for i, m, _ in failed]}")
