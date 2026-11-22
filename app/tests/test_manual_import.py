"""
utils/manual_import.py -- RIS/CSV/BibTeX parsing for manually-exported
search results (used for sources with no live API connector: CENTRAL,
Embase, CINAHL -- see database_search.py's SOURCE_REGISTRY).
"""

import os

from utils.manual_import import load_manual_import, parse_bibtex, parse_csv, parse_ris

_RIS_SAMPLE = """TY  - JOUR
TI  - Impact of systematic medication review in emergency department
AU  - Smith, J.
AU  - Doe, A.
PY  - 2022
AB  - A randomised controlled trial of medication review in the ED.
DO  - 10.1000/example.doi
UR  - https://example.com/paper
ER  -

TY  - JOUR
TI  - Some other unrelated trial
AU  - Lee, K.
PY  - 2019
ER  -
"""

_CSV_SAMPLE = (
    'Title,Authors,Year,DOI,Abstract\n'
    '"Effects of Hospital-Based Comprehensive Medication Reviews","Jones B; Kim C",2020,'
    '10.1000/csv.doi,"Some abstract text."\n'
)

_BIB_SAMPLE = """@article{smith2021,
  title = {A trial of medication review},
  author = {Smith, John and Doe, Anna},
  year = {2021},
  doi = {10.1000/bib.doi},
  abstract = {Some abstract.}
}
"""


def test_parse_ris_extracts_title_authors_year_doi(tmp_path):
    path = os.path.join(str(tmp_path), "sample.ris")
    with open(path, "w") as f:
        f.write(_RIS_SAMPLE)
    records = parse_ris(path)
    assert len(records) == 2
    first = records[0]
    assert first["title"] == "Impact of systematic medication review in emergency department"
    assert first["authors"] == ["Smith, J.", "Doe, A."]
    assert first["year"] == 2022
    assert first["doi"] == "10.1000/example.doi"
    assert first["source"] == "manual_import"


def test_parse_ris_records_missing_optional_fields_dont_crash(tmp_path):
    path = os.path.join(str(tmp_path), "sample.ris")
    with open(path, "w") as f:
        f.write(_RIS_SAMPLE)
    records = parse_ris(path)
    second = records[1]
    assert second["title"] == "Some other unrelated trial"
    assert second["doi"] is None
    assert second["abstract"] == ""


def test_parse_csv_with_default_column_aliases(tmp_path):
    path = os.path.join(str(tmp_path), "sample.csv")
    with open(path, "w") as f:
        f.write(_CSV_SAMPLE)
    records = parse_csv(path)
    assert len(records) == 1
    r = records[0]
    assert r["title"] == "Effects of Hospital-Based Comprehensive Medication Reviews"
    assert r["year"] == 2020
    assert r["doi"] == "10.1000/csv.doi"
    assert set(r["authors"]) == {"Jones B", "Kim C"}


def test_parse_csv_with_explicit_column_map(tmp_path):
    path = os.path.join(str(tmp_path), "weird.csv")
    with open(path, "w") as f:
        f.write("MyTitleCol,MyYearCol\n\"A weird paper\",2018\n")
    records = parse_csv(path, column_map={"title": "MyTitleCol", "year": "MyYearCol"})
    assert len(records) == 1
    assert records[0]["title"] == "A weird paper"
    assert records[0]["year"] == 2018


def test_parse_csv_no_title_column_returns_empty(tmp_path):
    path = os.path.join(str(tmp_path), "no_title.csv")
    with open(path, "w") as f:
        f.write("Foo,Bar\n1,2\n")
    assert parse_csv(path) == []


def test_parse_bibtex_extracts_fields(tmp_path):
    path = os.path.join(str(tmp_path), "sample.bib")
    with open(path, "w") as f:
        f.write(_BIB_SAMPLE)
    records = parse_bibtex(path)
    assert len(records) == 1
    r = records[0]
    assert r["title"] == "A trial of medication review"
    assert r["authors"] == ["Smith, John", "Doe, Anna"]
    assert r["year"] == 2021
    assert r["doi"] == "10.1000/bib.doi"
    assert r["id"] == "manual_import:smith2021"


def test_load_manual_import_dispatches_by_extension(tmp_path):
    ris_path = os.path.join(str(tmp_path), "a.ris")
    csv_path = os.path.join(str(tmp_path), "b.csv")
    bib_path = os.path.join(str(tmp_path), "c.bib")
    with open(ris_path, "w") as f:
        f.write(_RIS_SAMPLE)
    with open(csv_path, "w") as f:
        f.write(_CSV_SAMPLE)
    with open(bib_path, "w") as f:
        f.write(_BIB_SAMPLE)

    assert len(load_manual_import(ris_path)) == 2
    assert len(load_manual_import(csv_path)) == 1
    assert len(load_manual_import(bib_path)) == 1


def test_load_manual_import_unrecognised_extension_returns_empty(tmp_path):
    path = os.path.join(str(tmp_path), "sample.txt")
    with open(path, "w") as f:
        f.write("not a real bibliography file")
    assert load_manual_import(path) == []


def test_load_manual_import_default_source_label_uses_filename(tmp_path):
    path = os.path.join(str(tmp_path), "embase_export.ris")
    with open(path, "w") as f:
        f.write(_RIS_SAMPLE)
    records = load_manual_import(path)
    assert records[0]["source"] == "manual_import:embase_export"
