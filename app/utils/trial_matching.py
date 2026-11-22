"""
Same-trial detection for the production pipeline -- distinguishes a
"study/trial" from the individual publication(s) that report it, so two
different papers describing the SAME underlying trial are never both pooled
into one meta-analysis group as if they were independent evidence.

Deliberately production-only and NOT an import from cochrane_benchmark (see
utils/effect_measures.py's module docstring for the same production/
benchmark import-boundary rule, enforced by
tests/test_cochrane_benchmark_leakage_prevention.py) -- this module is the
canonical, reusable home for trial-matching logic;
cochrane_benchmark/evaluation/matching.py is free to depend on it (not the
reverse) if the two are ever unified, but that refactor is out of scope here.

Conservative by design: only registry-ID and DOI exact matches count as a
same-trial match. No fuzzy title/author heuristics -- unlike matching a
retrieved paper against a Cochrane ground-truth study (where the ground
truth is trusted and one side often lacks a real title at all, see
cochrane_benchmark/evaluation/matching.py's citation-key tier), two
DIFFERENT AutoSynthesis-collected papers usually have completely different
titles even when they report the same trial (a primary-outcome paper vs. a
secondary-analysis paper), so title similarity is not a reliable signal here
-- a false-positive merge would silently discard real data, which is worse
than a false negative (an occasional missed companion-publication pair,
which just leaves both papers pooled independently, exactly like today).
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from models import PaperRecord

# Generic trial-registry ID patterns -- NCT (ClinicalTrials.gov), ISRCTN,
# EudraCT, and the WHO ICTRP universal trial number (UTN) format. None of
# these are disease/study-name-specific; they are registry ID SHAPES.
_REGISTRY_ID_PATTERNS = [
    re.compile(r"\bNCT\d{8}\b", re.IGNORECASE),
    re.compile(r"\bISRCTN\d{8,9}\b", re.IGNORECASE),
    re.compile(r"\bEUCTR\d{4}-\d{6}-\d{2}(?:-[A-Z]{2,3})?\b", re.IGNORECASE),
    re.compile(r"\bU1111-\d{4}-\d{4}\b"),  # WHO UTN
]


def extract_registry_ids(text: Optional[str]) -> List[str]:
    """Every trial-registry ID found in `text` (title, abstract, or full
    text), normalized to uppercase, deduplicated, order-preserving. Generic
    regex shapes only -- no study/disease-specific vocabulary."""
    if not text:
        return []
    found: List[str] = []
    seen = set()
    for pat in _REGISTRY_ID_PATTERNS:
        for m in pat.finditer(text):
            rid = m.group(0).upper().replace(" ", "")
            if rid not in seen:
                seen.add(rid)
                found.append(rid)
    return found


def _norm_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    d = doi.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d or None


def _paper_registry_ids(paper: PaperRecord) -> List[str]:
    ids = extract_registry_ids(paper.trial_registry_id)
    ids += extract_registry_ids(paper.title)
    ids += extract_registry_ids(paper.full_text[:5000] if paper.full_text else None)
    # dedupe, preserve order
    seen = set()
    out = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def match_same_trial(a: PaperRecord, b: PaperRecord) -> Tuple[bool, str, float]:
    """Returns (is_same_trial, reason, confidence). Tries each tier in
    priority order, returns on the first one that fires:
      1. trial_registry_id -- exact match on a registry ID found on EITHER
         paper (its own metadata field, or extracted from title/full text).
      2. doi -- exact match (the trivial case: same publication indexed
         under slightly different PaperRecord entries).
    Returns (False, "none", 0.0) when neither tier finds anything -- NOT
    evidence the papers are unrelated, just insufficient evidence to merge
    them, so both are left as independent evidence (safe default)."""
    ids_a = _paper_registry_ids(a)
    ids_b = _paper_registry_ids(b)
    if ids_a and ids_b:
        shared = set(ids_a) & set(ids_b)
        if shared:
            return True, f"trial_registry_id:{sorted(shared)[0]}", 1.0

    doi_a, doi_b = _norm_doi(a.doi), _norm_doi(b.doi)
    if doi_a and doi_b and doi_a == doi_b:
        return True, "doi_exact", 1.0

    return False, "none", 0.0


def assign_trial_clusters(papers: List[PaperRecord]) -> None:
    """Mutates each PaperRecord's `.trial_cluster_id` in place. Papers found
    to describe the same trial (via match_same_trial(), any tier) get the
    SAME cluster id -- a stable hash of the cluster's sorted paper ids, never
    derived from a study/author name. Papers with no detected companion keep
    trial_cluster_id=None (unchanged) -- clustering only ever adds
    information, never removes a paper from consideration here."""
    import hashlib

    n = len(papers)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            is_same, _reason, _conf = match_same_trial(papers[i], papers[j])
            if is_same:
                union(i, j)

    clusters: dict = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)

    for members in clusters.values():
        if len(members) < 2:
            continue
        ids = sorted(papers[i].id for i in members)
        cluster_id = "trial_" + hashlib.sha1("|".join(ids).encode("utf-8")).hexdigest()[:12]
        for i in members:
            papers[i].trial_cluster_id = cluster_id
