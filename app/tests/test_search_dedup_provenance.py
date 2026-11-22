"""
agents/search_agent.py -- provenance-preserving merge dedup (replaces the
old discard-on-repeat `seen_titles: set`), and the unified candidate stream:
API-retrieved and manually-imported records must merge/dedup/screen through
the exact same path, with no special treatment for either side.

search_top_per_db() is mocked here for determinism (no real network calls) --
the manual-import side uses REAL file I/O through the real parser, since
that's the piece under test that must behave identically to an API result.
"""

import os
from unittest.mock import patch

from agents.search_agent import search_node
from models import MetaAnalysisPlan


def _plan(**overrides):
    defaults = dict(
        research_question="Does medication review reduce mortality?",
        treatment_label="medication review", control_label="standard care",
        outcome_description="mortality", positive_direction="lower is better",
        search_queries=["medication review trial"], inclusion_criteria=[], exclusion_criteria=[],
        moderators_to_extract=[], search_start_year=2015,
    )
    defaults.update(overrides)
    return MetaAnalysisPlan(**defaults)


_SAME_PAPER_TITLE = "Impact of systematic medication review on hospital readmission"

_RIS_SAMPLE = f"""TY  - JOUR
TI  - {_SAME_PAPER_TITLE}
AU  - Smith, J.
PY  - 2019
AB  - Manually-imported abstract text.
DO  - 10.1000/shared.doi
ER  -
"""


def _run_search_node(tmp_path, manual_paths=()):
    state = {"plan": _plan(), "output_dir": str(tmp_path)}
    with patch("agents.search_agent.MANUAL_IMPORT_PATHS", tuple(manual_paths)):
        return search_node(state)


def test_same_paper_from_two_api_sources_merges_provenance_not_duplicates(tmp_path):
    """Same title (by normalized-title dedup key) from two different
    'databases' must become ONE PaperRecord with both sources in
    provenance -- not two separate candidates, not a silently-dropped
    second sighting."""
    fake_results = {
        "pubmed": [{"id": "pubmed:1", "title": _SAME_PAPER_TITLE, "abstract": "",
                    "authors": ["Smith J"], "year": 2019, "source": "pubmed", "doi": "10.1000/shared.doi"}],
        "arxiv": [{"id": "arxiv:1", "title": _SAME_PAPER_TITLE, "abstract": "An arXiv-side abstract.",
                   "authors": ["Smith J"], "year": 2019, "source": "arxiv", "doi": "10.1000/shared.doi"}],
    }
    with patch("agents.search_agent.search_top_per_db", return_value=fake_results):
        result = _run_search_node(tmp_path)

    all_retrieved = result["all_retrieved_papers"]
    assert len(all_retrieved) == 1, "duplicate must merge into one candidate, not two"
    merged = all_retrieved[0]
    assert set(merged.provenance) == {"pubmed", "arxiv"}
    # Backfill: pubmed's empty abstract gets filled from arxiv's non-empty one.
    assert merged.abstract == "An arXiv-side abstract."


def test_distinct_papers_stay_distinct(tmp_path):
    fake_results = {
        "pubmed": [
            {"id": "pubmed:1", "title": "Paper One", "abstract": "", "authors": [], "year": 2019, "source": "pubmed"},
            {"id": "pubmed:2", "title": "Paper Two", "abstract": "", "authors": [], "year": 2020, "source": "pubmed"},
        ],
    }
    with patch("agents.search_agent.search_top_per_db", return_value=fake_results):
        result = _run_search_node(tmp_path)
    assert len(result["all_retrieved_papers"]) == 2


def test_manual_import_and_api_result_for_same_paper_merge_into_one_candidate(tmp_path):
    """THE smoke test this feature is built around: a manually-imported RIS
    record and an API-found record for the SAME paper must merge into one
    unified candidate carrying both sources in provenance -- proving
    manual-import records enter the exact same downstream stream as
    API-retrieved ones, not a parallel/special-cased path."""
    ris_path = os.path.join(str(tmp_path), "embase_export.ris")
    with open(ris_path, "w") as f:
        f.write(_RIS_SAMPLE)

    fake_results = {
        "pubmed": [{"id": "pubmed:1", "title": _SAME_PAPER_TITLE, "abstract": "",
                    "authors": ["Smith J"], "year": 2019, "source": "pubmed", "doi": "10.1000/shared.doi"}],
    }
    with patch("agents.search_agent.search_top_per_db", return_value=fake_results):
        result = _run_search_node(tmp_path, manual_paths=[ris_path])

    all_retrieved = result["all_retrieved_papers"]
    assert len(all_retrieved) == 1, "manual import + API hit for the same paper must merge, not duplicate"
    merged = all_retrieved[0]
    assert "pubmed" in merged.provenance
    assert "manual_import:embase_export" in merged.provenance
    # Manual import's abstract backfills pubmed's empty one.
    assert merged.abstract == "Manually-imported abstract text."
    # The merged candidate went through screening exactly once, same as any other.
    assert merged.id in result["screening_decisions"]


def test_manual_import_only_record_gets_full_screening_treatment(tmp_path):
    """A manually-imported record with NO API counterpart still goes
    through the same prescreen (_prefetch_screen_paper) as an API result --
    it must not bypass screening."""
    ris_path = os.path.join(str(tmp_path), "cinahl_export.ris")
    with open(ris_path, "w") as f:
        f.write(_RIS_SAMPLE)

    with patch("agents.search_agent.search_top_per_db", return_value={}):
        result = _run_search_node(tmp_path, manual_paths=[ris_path])

    assert len(result["all_retrieved_papers"]) == 1
    paper = result["all_retrieved_papers"][0]
    assert paper.id in result["screening_decisions"]
    assert result["screening_decisions"][paper.id]["decision"] in {"include", "exclude"}
    assert paper.provenance == ["manual_import:cinahl_export"]


def test_manual_import_records_can_be_screened_out_same_as_api_records(tmp_path):
    """A manually-imported record that looks non-empirical/off-topic is
    screened OUT exactly like an API-found one would be -- no special
    inclusion privilege."""
    ris_path = os.path.join(str(tmp_path), "review_like.ris")
    with open(ris_path, "w") as f:
        f.write(
            "TY  - JOUR\n"
            "TI  - A systematic review and meta-analysis of unrelated topics\n"
            "AU  - Nobody\n"
            "PY  - 2018\n"
            "AB  - " + ("This narrative review discusses unrelated background material. " * 10) + "\n"
            "ER  -\n"
        )
    with patch("agents.search_agent.search_top_per_db", return_value={}):
        result = _run_search_node(tmp_path, manual_paths=[ris_path])

    paper = result["all_retrieved_papers"][0]
    assert result["screening_decisions"][paper.id]["decision"] == "exclude"
    assert paper not in result["papers_eligible"]
