"""
Shared, minimal RIS (Research Information Systems bibliographic format)
reader -- used by BOTH cochrane_benchmark/sources/structured/datapackage_parser.py
(Cochrane's CSV+RIS Data Package ground-truth backend) and
utils/manual_import.py (general-purpose manual search-result import for the
production retrieval pipeline), so the tag-parsing logic lives in exactly
one place instead of two copies that could drift.

Relocated verbatim from datapackage_parser.py (that module now imports this
one) -- not a new implementation, same behaviour, same known limitation
(a minimal reader good enough for standard bibliographic tags, not a full
RIS-spec validator).
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, List


def parse_ris_records(text: str) -> List[Dict[str, List[str]]]:
    """Minimal RIS reader: blank-line-separated records, each a sequence of
    `TAG  - value` lines ending in `ER  - `. Repeated tags (e.g. AU) keep
    every value; others keep the last. Good enough for the bibliographic
    fields commonly needed (AU/TI/T1/CT/PY/DA/DO/NS/TY/AB/N1/UR/SP/JO) --
    not a general RIS validator."""
    records: List[Dict[str, List[str]]] = []
    current: Dict[str, List[str]] = defaultdict(list)
    for line in text.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        m = re.match(r"^([A-Z][A-Z0-9])\s+-\s?(.*)$", line)
        if not m:
            continue
        tag, value = m.group(1), m.group(2).strip()
        if tag == "ER":
            if current:
                records.append(dict(current))
            current = defaultdict(list)
            continue
        current[tag].append(value)
    if current:
        records.append(dict(current))
    return records
