import csv

from models import PaperRecord


def test_preliminary_paper_tracking_marks_eligible_as_pending(tmp_path):
    from agents.pipeline_audit_agent import write_preliminary_paper_tracking_csv

    included = PaperRecord(
        id="p1",
        title="Included paper",
        abstract="",
        authors=[],
        year=2024,
        source="deep_research",
        doi="10.1234/included",
        url="https://example.test/included",
    )
    excluded = PaperRecord(
        id="p2",
        title="Excluded paper",
        abstract="",
        authors=[],
        year=2023,
        source="deep_research",
    )

    path = write_preliminary_paper_tracking_csv({
        "output_dir": str(tmp_path),
        "mode": "search",
        "all_retrieved_papers": [included, excluded],
        "papers_eligible": [included],
        "screening_decisions": {
            "p1": {"decision": "include"},
            "p2": {"decision": "include"},
        },
        "eligibility_decisions": {
            "p1": {"decision": "include"},
            "p2": {"decision": "exclude", "reason": "wrong population"},
        },
        "search_rejected_papers": [],
        "papers_no_fulltext": [],
        "papers_no_fulltext_reasons": {},
    })

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows[0]["title"] == "Included paper"
    assert rows[0]["doi"] == "10.1234/included"
    assert rows[0]["url"] == "https://example.test/included"
    assert rows[0]["eligibility_status"] == "Eligible"
    assert rows[0]["final_status"] == "Pending Downstream"
    assert rows[1]["title"] == "Excluded paper"
    assert rows[1]["loss_stage"] == "Eligibility"
    assert rows[1]["loss_reason"] == "wrong population"


def test_preliminary_paper_tracking_does_not_duplicate_screened_out_rows(tmp_path):
    from agents.pipeline_audit_agent import write_preliminary_paper_tracking_csv

    rejected = PaperRecord(
        id="p1",
        title="Rejected paper",
        abstract="",
        authors=[],
        year=2022,
        source="arxiv",
    )

    path = write_preliminary_paper_tracking_csv({
        "output_dir": str(tmp_path),
        "mode": "search",
        "all_retrieved_papers": [rejected],
        "papers_eligible": [],
        "screening_decisions": {
            "p1": {"decision": "exclude", "reason": "review article"},
        },
        "eligibility_decisions": {},
        "search_rejected_papers": [{
            "id": "p1",
            "title": "Rejected paper",
            "year": 2022,
            "source": "arxiv",
            "doi": "10.1234/rejected",
            "url": "https://example.test/rejected",
            "reason": "review article",
        }],
        "papers_no_fulltext": [],
        "papers_no_fulltext_reasons": {},
    })

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert [row["title"] for row in rows] == ["Rejected paper"]
    assert rows[0]["loss_stage"] == "Screening"
