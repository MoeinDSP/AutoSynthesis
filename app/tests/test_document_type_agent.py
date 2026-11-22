"""
agents/document_type_agent.py -- the manual-mode-only gate that keeps a
Cochrane review PDF (or a split/duplicate fragment of one) accidentally
included among manually-uploaded "primary study" files from being treated
as a primary study itself.

Generic by construction: structural signals + a closed-vocabulary LLM
classification, no filename or review-ID checks anywhere; near-duplicate
detection is full-text content similarity, never filenames.
"""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

# Must be imported before agents.document_type_agent (which itself imports
# from pipeline_graph) -- same circular-import hazard documented elsewhere
# in this test suite.
import pipeline_graph  # noqa: F401

from models import PaperRecord
from agents.document_type_agent import (
    _structural_signals,
    _find_near_duplicates,
    document_type_node,
)


# ---------------------------------------------------------------------------
# Structural signals -- pure function, no LLM involved
# ---------------------------------------------------------------------------

def test_structural_signals_detect_review_markers():
    text = (
        "Search strategy: we searched CENTRAL, MEDLINE...\n"
        "Characteristics of included studies\n"
        "Risk of bias in included studies\n"
        "Data and analyses\n"
        "Forest plot of comparison 1\n"
    )
    signals = _structural_signals(text)
    assert signals["review_marker_hits"] >= 4


def test_structural_signals_low_for_plain_primary_study_text():
    text = (
        "Methods: 100 patients were randomized to intervention or control.\n"
        "Participants: adults aged 18-65 with hypertension.\n"
        "Results: the intervention group showed lower blood pressure.\n"
    )
    signals = _structural_signals(text)
    assert signals["review_marker_hits"] == 0


def test_structural_signals_empty_text_handled():
    signals = _structural_signals("")
    assert signals["length"] == 0


# ---------------------------------------------------------------------------
# Near-duplicate / split-file detection -- content similarity, never filenames
# ---------------------------------------------------------------------------

def test_near_duplicate_pair_detected_by_content_not_filename():
    shared_text = "Introduction. " + ("Lorem ipsum dolor sit amet. " * 200)
    papers = [
        PaperRecord(id="a", title="totally_different_name_1", abstract="", year=2020, source="manual", full_text=shared_text),
        PaperRecord(id="b", title="totally_different_name_2", abstract="", year=2020, source="manual", full_text=shared_text[:-50]),
    ]
    dups = _find_near_duplicates(papers)
    # Exactly one of the pair is dropped (content-similarity match), keyed
    # to the OTHER one -- which specific one is dropped is an implementation
    # tie-break detail, not a guarantee this test should pin down.
    assert len(dups) == 1
    dropped_id, kept_id = next(iter(dups.items()))
    assert {dropped_id, kept_id} == {"a", "b"}


def test_genuinely_different_papers_not_flagged_as_duplicates():
    papers = [
        PaperRecord(id="a", title="t1", abstract="", year=2020, source="manual",
                    full_text="A randomized trial of drug X in patients with condition Y. " * 50),
        PaperRecord(id="b", title="t2", abstract="", year=2021, source="manual",
                    full_text="An observational cohort study of exposure Z and outcome W. " * 50),
    ]
    dups = _find_near_duplicates(papers)
    assert dups == {}


# ---------------------------------------------------------------------------
# document_type_node -- LLM classification mocked, one invoke() per paper
# ---------------------------------------------------------------------------

def _fake_result(document_type, rationale="because"):
    return {"messages": [
        HumanMessage(content="classify..."),
        AIMessage(content="", tool_calls=[{
            "name": "record_document_type",
            "args": {
                "paper_id": "x", "document_type": document_type,
                "rationale": rationale, "evidence_quote": "quote",
            },
            "id": "call_1",
        }]),
        ToolMessage(content="ok", tool_call_id="call_1"),
        AIMessage(content="done"),
    ]}


def test_review_document_is_excluded_generically(tmp_path):
    papers = [PaperRecord(id="p1", title="Some Review", abstract="", year=2020, source="manual",
                           full_text="Search strategy... characteristics of included studies...")]
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = _fake_result("systematic_review_or_meta_analysis", "has its own included-studies list")

    with patch("agents.document_type_agent.create_react_agent", return_value=mock_agent):
        result = document_type_node({"papers_eligible": papers, "output_dir": str(tmp_path)})

    assert result["papers_eligible"] == []
    flags = result["validation_flags"]
    assert any(f.stage == "document_type_gate" and f.subject_id == "p1" for f in flags)

    # document_type_excluded (paper_id/title/document_type/rationale) is what
    # lets agents/pipeline_audit_agent.py surface this as a real row in
    # paper_tracking.csv -- manual mode has no separate all_retrieved_papers
    # list, so without this the paper would vanish from the audit trail.
    excluded = result["document_type_excluded"]
    assert len(excluded) == 1
    assert excluded[0]["paper_id"] == "p1"
    assert excluded[0]["title"] == "Some Review"
    assert excluded[0]["document_type"] == "systematic_review_or_meta_analysis"


def test_primary_study_document_is_kept(tmp_path):
    papers = [PaperRecord(id="p1", title="A Trial", abstract="", year=2020, source="manual",
                           full_text="Methods: 100 patients randomized...")]
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = _fake_result("primary_study")

    with patch("agents.document_type_agent.create_react_agent", return_value=mock_agent):
        result = document_type_node({"papers_eligible": papers, "output_dir": str(tmp_path)})

    assert [p.id for p in result["papers_eligible"]] == ["p1"]
    assert result["papers_eligible"][0].document_type == "primary_study"


def test_unclear_document_kept_but_flagged(tmp_path):
    papers = [PaperRecord(id="p1", title="Ambiguous", abstract="", year=2020, source="manual", full_text="short text")]
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = _fake_result("unclear")

    with patch("agents.document_type_agent.create_react_agent", return_value=mock_agent):
        result = document_type_node({"papers_eligible": papers, "output_dir": str(tmp_path)})

    assert [p.id for p in result["papers_eligible"]] == ["p1"]
    assert any(f.stage == "document_type_gate" and f.severity == "warning" for f in result["validation_flags"])


def test_mixed_batch_review_dropped_primary_study_kept(tmp_path):
    papers = [
        PaperRecord(id="review", title="The Review Itself", abstract="", year=2020, source="manual",
                    full_text="Search strategy... PRISMA... characteristics of included studies..."),
        PaperRecord(id="trial1", title="Actual Trial", abstract="", year=2019, source="manual",
                    full_text="Methods: patients randomized to drug or placebo..."),
    ]
    responses = {
        "The Review Itself": _fake_result("systematic_review_or_meta_analysis"),
        "Actual Trial": _fake_result("primary_study"),
    }
    mock_agent = MagicMock()

    def _invoke(payload):
        msg = payload["messages"][0][1]
        for title, resp in responses.items():
            if title in msg:
                return resp
        return _fake_result("unclear")

    mock_agent.invoke.side_effect = _invoke

    with patch("agents.document_type_agent.create_react_agent", return_value=mock_agent):
        result = document_type_node({"papers_eligible": papers, "output_dir": str(tmp_path)})

    kept_ids = {p.id for p in result["papers_eligible"]}
    assert kept_ids == {"trial1"}


def test_no_papers_returns_empty_without_calling_agent(tmp_path):
    with patch("agents.document_type_agent.create_react_agent") as mock_create:
        result = document_type_node({"papers_eligible": [], "output_dir": str(tmp_path)})
    mock_create.assert_not_called()
    assert result == {"papers_eligible": []}
