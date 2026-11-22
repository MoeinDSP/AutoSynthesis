"""
General-purpose manual search-result import -- for any retrieval source that
has no live API connector (currently CENTRAL, Embase, CINAHL -- see
database_search.py's SOURCE_REGISTRY) but that a human can search through its
own web interface and export results from.

Deliberately NOT Cochrane-benchmark-specific: this is general AutoSynthesis
retrieval infrastructure, usable for any topic/run, per this feature's design.

A record loaded here enters the exact same downstream candidate stream as an
API-retrieved one (agents/search_agent.py::search_node() merges them through
identical dedup/prescreen/PaperRecord-conversion logic) -- it must never
bypass screening or receive special treatment, per explicit instruction.

Supported formats: RIS (.ris), CSV (.csv), BibTeX (.bib). Output shape
matches every other searcher in database_search.py (a plain List[Dict] of
"raw paper" dicts: id/title/abstract/authors/year/url/source/doi/
open_access_pdf, plus the optional pmid/trial_registry_id fields) so
_paper_from_raw() in search_agent.py needs no changes to consume it.
"""

from __future__ import annotations

import csv
import logging
import os
import re
from typing import Dict, List, Optional

from utils.ris_parser import parse_ris_records

logger = logging.getLogger(__name__)


def _first(values: Optional[List[str]]) -> Optional[str]:
    return values[0].strip() if values else None


def parse_ris(path: str, source_label: str = "manual_import") -> List[Dict]:
    """RIS export (Embase, CINAHL/EBSCO, CENTRAL/Cochrane Library, Scopus,
    Web of Science, EndNote, Zotero, etc. can all export RIS) -- reuses the
    same shared parser cochrane_benchmark's Data Package backend uses (see
    utils/ris_parser.py), so RIS handling never drifts between the two."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        text = f.read()
    records = parse_ris_records(text)

    papers: List[Dict] = []
    for i, rec in enumerate(records):
        title = _first(rec.get("TI")) or _first(rec.get("T1")) or _first(rec.get("CT"))
        if not title:
            continue
        abstract = _first(rec.get("AB")) or _first(rec.get("N2")) or ""
        authors = rec.get("AU") or rec.get("A1") or []
        year = None
        date = _first(rec.get("PY")) or _first(rec.get("Y1")) or _first(rec.get("DA"))
        if date:
            m = re.search(r"(19|20)\d{2}", date)
            if m:
                year = int(m.group(0))
        doi = _first(rec.get("DO"))
        url_val = _first(rec.get("UR")) or _first(rec.get("L1"))
        an = _first(rec.get("AN")) or _first(rec.get("ID"))  # accession number, when present

        papers.append({
            "id": f"{source_label}:{an or i}",
            "title": title,
            "abstract": abstract,
            "authors": [a.strip() for a in authors if a.strip()],
            "year": year or 0,
            "url": url_val,
            "source": source_label,
            "doi": doi,
            "open_access_pdf": None,
        })
    logger.info(f"[ManualImport] {len(papers)} record(s) parsed from RIS file: {path}")
    return papers


# Common column-name variants seen in exports from Embase/CINAHL/CENTRAL/
# Scopus/Web of Science/PubMed's own CSV export -- matched case-insensitively.
# A caller can always override with an explicit column_map for anything
# unusual instead of relying on this best-effort guess.
_CSV_COLUMN_ALIASES = {
    "title": ["title", "article title", "document title", "ti"],
    "abstract": ["abstract", "ab"],
    "authors": ["authors", "author(s)", "author full names", "au"],
    "year": ["year", "publication year", "pubyear", "py", "date"],
    "doi": ["doi", "digital object identifier"],
    "url": ["url", "link", "source link"],
}


def _resolve_csv_columns(fieldnames: List[str], column_map: Optional[Dict[str, str]]) -> Dict[str, str]:
    if column_map:
        return column_map
    lower_to_actual = {f.strip().lower(): f for f in fieldnames if f}
    resolved: Dict[str, str] = {}
    for target, aliases in _CSV_COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_to_actual:
                resolved[target] = lower_to_actual[alias]
                break
    return resolved


def parse_csv(path: str, source_label: str = "manual_import",
              column_map: Optional[Dict[str, str]] = None) -> List[Dict]:
    """CSV export. Column names vary a lot by platform (Scopus's "Author(s)"
    vs. PubMed's "Authors" vs. a hand-built spreadsheet's "Author") -- best-
    effort alias matching (see _CSV_COLUMN_ALIASES) is used unless an
    explicit `column_map` ({"title": "Article Title", ...}) is given."""
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = _resolve_csv_columns(reader.fieldnames or [], column_map)

    if "title" not in cols:
        logger.warning(f"[ManualImport] Could not identify a title column in {path} -- got fields {list(rows[0].keys()) if rows else []}")
        return []

    papers: List[Dict] = []
    for i, row in enumerate(rows):
        title = (row.get(cols["title"]) or "").strip()
        if not title:
            continue
        year = 0
        raw_year = (row.get(cols.get("year", ""), "") or "").strip()
        m = re.search(r"(19|20)\d{2}", raw_year)
        if m:
            year = int(m.group(0))
        authors_raw = (row.get(cols.get("authors", ""), "") or "").strip()
        authors = [a.strip() for a in re.split(r";\s*|,\s*(?=[A-Z][a-z]+\s)", authors_raw) if a.strip()] if authors_raw else []

        papers.append({
            "id": f"{source_label}:{i}",
            "title": title,
            "abstract": (row.get(cols.get("abstract", ""), "") or "").strip(),
            "authors": authors,
            "year": year,
            "url": (row.get(cols.get("url", ""), "") or "").strip() or None,
            "source": source_label,
            "doi": (row.get(cols.get("doi", ""), "") or "").strip() or None,
            "open_access_pdf": None,
        })
    logger.info(f"[ManualImport] {len(papers)} record(s) parsed from CSV file: {path}")
    return papers


_BIBTEX_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", re.DOTALL)
_BIBTEX_FIELD_RE = re.compile(r'(\w+)\s*=\s*[{"](.*?)[}"]\s*,?\s*$', re.MULTILINE)


def parse_bibtex(path: str, source_label: str = "manual_import") -> List[Dict]:
    """Minimal first-party BibTeX reader (no new dependency, matching this
    codebase's existing preference for small hand-rolled parsers over
    heavier libraries for structured-text formats -- same convention
    utils/ris_parser.py already follows). Handles the common
    `@type{key, field = {value}, field2 = "value2"}` shape; not a full
    BibTeX-grammar parser (nested braces inside a single field value are
    not unwrapped beyond the outer pair)."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    papers: List[Dict] = []
    for i, m in enumerate(_BIBTEX_ENTRY_RE.finditer(text)):
        entry_type, key, body = m.group(1), m.group(2).strip(), m.group(3)
        fields: Dict[str, str] = {}
        for fm in _BIBTEX_FIELD_RE.finditer(body):
            fields[fm.group(1).strip().lower()] = fm.group(2).strip()

        title = fields.get("title", "").strip()
        if not title:
            continue
        year = 0
        if fields.get("year", "").strip().isdigit():
            year = int(fields["year"])
        authors_raw = fields.get("author", "")
        authors = [a.strip() for a in authors_raw.split(" and ") if a.strip()]

        papers.append({
            "id": f"{source_label}:{key or i}",
            "title": title,
            "abstract": fields.get("abstract", ""),
            "authors": authors,
            "year": year,
            "url": fields.get("url") or (f"https://doi.org/{fields['doi']}" if fields.get("doi") else None),
            "source": source_label,
            "doi": fields.get("doi") or None,
            "open_access_pdf": None,
        })
    logger.info(f"[ManualImport] {len(papers)} record(s) parsed from BibTeX file: {path}")
    return papers


def load_manual_import(path: str, source_label: Optional[str] = None) -> List[Dict]:
    """Dispatch by file extension. `source_label` defaults to
    "manual_import:<basename>" so results from two different manual exports
    (e.g. an Embase export and a CINAHL export) stay distinguishable in
    provenance even though both went through this same loader."""
    label = source_label or f"manual_import:{os.path.splitext(os.path.basename(path))[0]}"
    ext = os.path.splitext(path)[1].lower()
    if ext == ".ris":
        return parse_ris(path, source_label=label)
    if ext == ".csv":
        return parse_csv(path, source_label=label)
    if ext in (".bib", ".bibtex"):
        return parse_bibtex(path, source_label=label)
    logger.warning(f"[ManualImport] Unrecognised file extension {ext!r} for {path} -- expected .ris/.csv/.bib")
    return []
