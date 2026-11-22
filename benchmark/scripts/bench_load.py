"""Loader + comparison helpers for the 100-review benchmark CSVs."""
import csv, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
from paths import DATA as CSV_DIR
FILES = {"GT": "cochrane_ground_truth.csv",
         "GPT": "autosynthesis_gpt.csv",
         "Gemini": "autosynthesis_gemini.csv",
         "Claude": "autosynthesis_claude.csv"}
MODELS = ["GPT", "Gemini", "Claude"]
def num(v):
    v = (v or "").strip().replace(",", "").replace("−", "-").replace("–", "-")
    if v in ("", "-", "NA", "N/A", "NR", "NP"): return None
    m = re.search(r"-?\d+(?:\.\d+)?(?:[eE]-?\d+)?", v)
    return float(m.group()) if m else None
def ci(v):
    v = (v or "").replace("−", "-").replace("–", "-")
    nums = re.findall(r"-?\d+(?:\.\d+)?(?:[eE]-?\d+)?", v.replace(",", " ").replace(" to ", " "))
    return (float(nums[0]), float(nums[1])) if len(nums) >= 2 else (None, None)
def family(raw):
    r = (raw or "").upper().replace("−", "-")
    if r.startswith(("SMD", "STANDARDI", "HEDGES", "COHEN")): return "SMD"
    if r.startswith(("MD", "MEAN DIFF", "WMD")): return "MD"
    if r.startswith(("RR", "RISK RATIO", "RELATIVE RISK")): return "RR"
    if r.startswith(("OR", "ODDS")): return "OR"
    if r.startswith(("HR", "HAZARD")): return "HR"
    if r.startswith(("RD", "RISK DIFF")): return "RD"
    return "OTHER"
RATIO = {"RR", "OR", "HR"}
def load():
    """Robust loader: finds the CI field ('[lo, hi]') and reads Effect/k/N by position relative to it, so rows
    shifted by a stray empty or duplicated column are still read correctly."""
    out = {}
    for key, fn in FILES.items():
        for r in csv.reader(open(os.path.join(CSV_DIR, fn), encoding="utf-8-sig")):
            if not r or not r[0].strip().startswith("CD") : continue
            r = [c.strip() for c in r]
            cid = r[0]
            ci_idx = next((j for j, c in enumerate(r) if re.match(r"^\[.*\]$", c) and j >= 6), None)
            if ci_idx is None:
                out[(cid, key)] = dict(fam="OTHER", raw="", eff=None, lo=None, hi=None, k=None, n=None, topic=r[1], outcome=r[2], shifted=False, nociI=True); continue
            lo, hi = ci(r[ci_idx])
            eff, k, n = num(r[ci_idx-3]), num(r[ci_idx-2]), num(r[ci_idx-1])
            raw = r[ci_idx-4] if ci_idx-4 >= 5 else ""
            if raw and num(raw) is not None and not re.search(r"[A-Za-z]", raw): raw = ""     # a number, not a measure name
            shifted = ci_idx != 9
            out[(cid, key)] = dict(fam=family(raw), raw=raw, eff=eff, lo=lo, hi=hi, k=k, n=n, topic=r[1], outcome=r[2], shifted=shifted, nociI=False)
    return out
def to_null_scale(d):
    """effect, lo, hi on the 'difference' scale where the null is 0 (log for ratios)."""
    if d["eff"] is None: return None
    if d["fam"] in RATIO:
        if d["eff"] <= 0: return None
        e = math.log(d["eff"])
        lo = math.log(d["lo"]) if d["lo"] and d["lo"] > 0 else None
        hi = math.log(d["hi"]) if d["hi"] and d["hi"] > 0 else None
        return e, lo, hi
    return d["eff"], d["lo"], d["hi"]
