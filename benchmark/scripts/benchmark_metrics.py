"""Recompute the 100-review benchmark metrics (AutoSynthesis models vs Cochrane) and write a per-review audit CSV."""
import csv, json, math, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bench_load import load, MODELS, RATIO, HERE
from paths import DATA, RUNS, FIG, RESULTS

def scale(row):
    """-> ('ratio'|'diff'|None, inferred_bool). A blank measure is inferred from where the estimate sits inside its CI."""
    if row["fam"] in RATIO: return "ratio", False
    if row["fam"] in ("MD", "SMD", "RD"): return "diff", False
    e, lo, hi = row["eff"], row["lo"], row["hi"]
    if None in (e, lo, hi): return None, True
    if lo > 0 and abs(e - math.sqrt(lo * hi)) < abs(e - (lo + hi) / 2): return "ratio", True
    return "diff", True

def valid(row):
    e, lo, hi = row["eff"], row["lo"], row["hi"]
    if None in (e, lo, hi) or lo > hi: return False
    if not (lo - 1e-9 <= e <= hi + 1e-9): return False                  # estimate outside its own CI
    sc, _ = scale(row)
    if sc == "ratio" and (lo <= 0 or e <= 0): return False              # a ratio cannot be <= 0
    return sc is not None

def tr(row):
    """effect, lo, hi on the scale where the null is 0."""
    sc, _ = scale(row)
    f = math.log if sc == "ratio" else (lambda x: x)
    return f(row["eff"]), f(row["lo"]), f(row["hi"])

def category(t):
    e, lo, hi = t
    return "sig_neg" if hi < 0 else ("sig_pos" if lo > 0 else "ns")

CHINN = math.pi / math.sqrt(3)        # ln(OR) = SMD * pi/sqrt(3)  (Chinn 2000)
STD_DIFF = {"SMD"}

def _shape(row):
    """Scale implied by where the estimate sits in its CI: 'ratio' (geometric centre) or 'diff' (arithmetic centre)."""
    e, lo, hi = row["eff"], row["lo"], row["hi"]
    if None in (e, lo, hi): return None
    if lo > 0 and abs(e - math.sqrt(lo * hi)) < abs(e - (lo + hi) / 2): return "ratio"
    return "diff"

def harmonize(p, g):
    """Bring a model result onto the Cochrane measure with standard formulas, so it can be compared.
    Returns (row, conv). conv: None (already same measure), 'relabel' (label missing/wrong but the CI shape shows the
    scale), 'ratio' (RR/OR/HR used for one another on the log scale), 'chinn' (SMD <-> ln OR). Not convertible
    (MD <-> SMD needs the SDs; invalid results) -> (p, None) unchanged."""
    if not valid(p) or (p["fam"] == g["fam"]): return p, None
    gs = "ratio" if g["fam"] in RATIO else "diff"
    shape = _shape(p)
    q = dict(p)
    # 1) label blank/OTHER, or labelled SMD/MD but the CI is clearly ratio-shaped (or vice versa): trust the numbers
    lab = "ratio" if p["fam"] in RATIO else ("diff" if p["fam"] in ("SMD", "MD", "RD") else None)
    if lab is None or (lab != shape and shape == "ratio" and p["lo"] > 0):
        if shape == gs:
            q["fam"] = g["fam"]; return q, "relabel"
        if shape == "ratio" and g["fam"] in STD_DIFF:
            q.update(fam="SMD", eff=math.log(p["eff"]) / CHINN, lo=math.log(p["lo"]) / CHINN, hi=math.log(p["hi"]) / CHINN); return q, "chinn"
        return p, None
    # 2) ratio <-> ratio
    if p["fam"] in RATIO and g["fam"] in RATIO:
        q["fam"] = g["fam"]; return q, "ratio"
    # 3) SMD <-> ratio (Chinn)
    if p["fam"] == "SMD" and g["fam"] in RATIO:
        q.update(fam=g["fam"], eff=math.exp(p["eff"] * CHINN), lo=math.exp(p["lo"] * CHINN), hi=math.exp(p["hi"] * CHINN)); return q, "chinn"
    if p["fam"] in RATIO and g["fam"] == "SMD":
        q.update(fam="SMD", eff=math.log(p["eff"]) / CHINN, lo=math.log(p["lo"]) / CHINN, hi=math.log(p["hi"]) / CHINN); return q, "chinn"
    return p, None                                      # MD <-> SMD, RD, ...: needs the per-study data

d = load(); ids = sorted({k[0] for k in d})
CONV = {}                                              # (id, model) -> conversion applied
if os.getenv("BENCH_HARMONIZE", "1") != "0":
    for (i, m), p in list(d.items()):
        if m == "GT": continue
        q, c = harmonize(p, d[(i, "GT")])
        if c: d[(i, m)] = q; CONV[(i, m)] = c
    # still not comparable (MD <-> SMD, invalid): the model's own study data re-pooled in the Cochrane measure
    _rp = os.path.join(DATA, "repooled_results.csv")
    if os.getenv("BENCH_HARMONIZE_NO_REPOOL") != "1" and os.path.exists(_rp):
        for r in csv.DictReader(open(_rp)):
            key = (r["id"], r["model"]); p = d.get(key)
            if p is None or key in CONV: continue
            d[key] = dict(p, fam=r["fam"], raw=r["fam"], eff=float(r["eff"]), lo=float(r["lo"]), hi=float(r["hi"]), k=float(r["k"]))
            CONV[key] = "repooled"
audit = []; S = {m: dict(dir_n=0, dir_ok=0, valid=0, same_measure=0, sig_agree=0, sm_overlap=0, sm_inside=0, sm_concl=0, sm_dir_both_sig=0, sm_both_sig=0,
                         kratio=[], shifted=0, blank_measure=0, invalid=[], diff_measure=[]) for m in MODELS}
for i in ids:
    g = d[(i, "GT")]; assert valid(g), i
    tg = tr(g); cg = category(tg)
    for m in MODELS:
        p = d[(i, m)]; s = S[m]
        sc_p, inferred = scale(p)
        rec = dict(id=i, model=m, gt_measure=g["fam"], gt_eff=g["eff"], gt_lo=g["lo"], gt_hi=g["hi"], gt_k=g["k"], gt_cat=cg,
                   m_measure=p["raw"], m_eff=p["eff"], m_lo=p["lo"], m_hi=p["hi"], m_k=p["k"], status="", same_measure="", sig_agree="",
                   ci_overlap="", est_in_gt_ci="", same_conclusion="", m_cat="", same_direction="", conversion=CONV.get((i, m), ""))
        if p["shifted"]: s["shifted"] += 1
        if not p["raw"]: s["blank_measure"] += 1
        if not valid(p):
            rec["status"] = "invalid"; s["invalid"].append(i); audit.append(rec); continue
        s["valid"] += 1; rec["status"] = "ok"
        tp = tr(p); cp = category(tp); rec["m_cat"] = cp
        if g["k"] and p["k"] is not None and p["k"] > 0: s["kratio"].append(p["k"] / g["k"])
        if tg[0] != 0 and tp[0] != 0:                      # direction = sign on the null-at-0 scale; skip results exactly at no effect
            dok = (tg[0] > 0) == (tp[0] > 0); rec["same_direction"] = int(dok); s["dir_n"] += 1; s["dir_ok"] += dok
        sa = (cg != "ns") == (cp != "ns"); rec["sig_agree"] = int(sa); s["sig_agree"] += sa
        same = (p["fam"] == g["fam"]) and not inferred
        rec["same_measure"] = int(same)
        if same:
            s["same_measure"] += 1
            ov = tp[1] <= tg[2] and tg[1] <= tp[2]; inside = tg[1] <= tp[0] <= tg[2]
            conc = (cp == cg)
            rec["ci_overlap"] = int(ov); rec["est_in_gt_ci"] = int(inside); rec["same_conclusion"] = int(conc)
            s["sm_overlap"] += ov; s["sm_inside"] += inside; s["sm_concl"] += conc
            if cg != "ns" and cp != "ns":
                s["sm_both_sig"] += 1; s["sm_dir_both_sig"] += (cg == cp)
        else:
            s["diff_measure"].append(i)
        audit.append(rec)
with open(os.path.join(RESULTS, "benchmark_audit_per_review.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(audit[0].keys())); w.writeheader(); w.writerows(audit)
summ = {}
for m in MODELS:
    s = S[m]
    summ[m] = dict(same_direction=s["dir_ok"], direction_compared=s["dir_n"], valid=s["valid"], invalid=len(s["invalid"]), invalid_ids=s["invalid"], same_measure=s["same_measure"],
                   sig_agree=s["sig_agree"], ci_overlap=s["sm_overlap"], est_in_gt_ci=s["sm_inside"], same_conclusion=s["sm_concl"],
                   both_sig=s["sm_both_sig"], both_sig_same_dir=s["sm_dir_both_sig"],
                   k_ratio_median=round(st.median(s["kratio"]), 3) if s["kratio"] else None,
                   k_ratio_mean=round(st.mean(s["kratio"]), 3) if s["kratio"] else None, shifted_rows=s["shifted"], blank_measure=s["blank_measure"])
json.dump(summ, open(os.path.join(RESULTS, "benchmark_summary.json"), "w"), indent=1)
for m in MODELS: print(m, json.dumps({k: v for k, v in summ[m].items() if k != "invalid_ids"}), summ[m]["invalid_ids"])
