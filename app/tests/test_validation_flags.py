"""models.ValidationFlag and its aggregation into validation_report.csv/.json
(agents/pipeline_audit_agent.py::write_validation_report). Per-mechanism flag
emission is covered where each mechanism lives (test_cross_paper_outcome_
mapper_wiring.py, test_document_type_agent.py, test_meta_analysis_node_
grouping.py) -- this file covers the shared model and the aggregation step."""

import csv
import json
import os

import pytest
from pydantic import ValidationError

# Must be imported before agents.pipeline_audit_agent (which itself imports
# from pipeline_graph) -- same circular-import hazard documented elsewhere
# in this test suite (e.g. test_cross_paper_outcome_mapper_wiring.py).
import pipeline_graph  # noqa: F401

from models import ValidationFlag


def test_validation_flag_requires_a_known_stage():
    with pytest.raises(ValidationError):
        ValidationFlag(stage="not_a_real_stage", severity="warning", subject_id="x", message="m")


def test_validation_flag_requires_a_known_severity():
    with pytest.raises(ValidationError):
        ValidationFlag(stage="extraction", severity="not_a_real_severity", subject_id="x", message="m")


def test_validation_flag_auto_action_optional():
    f = ValidationFlag(stage="extraction", severity="info", subject_id="x", message="m")
    assert f.auto_action is None


def test_write_validation_report_creates_csv_and_json(tmp_path):
    from agents.pipeline_audit_agent import write_validation_report

    flags = [
        ValidationFlag(stage="outcome_classification", severity="warning", subject_id="p1", message="msg1"),
        ValidationFlag(stage="trial_dedup", severity="warning", subject_id="mortality", message="msg2", auto_action="excluded_row"),
    ]
    state = {"output_dir": str(tmp_path), "validation_flags": flags}
    path = write_validation_report(state)

    assert os.path.exists(path)
    with open(path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["stage"] == "outcome_classification"
    assert rows[1]["auto_action"] == "excluded_row"

    json_path = os.path.join(str(tmp_path), "validation_report.json")
    with open(json_path) as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[1]["message"] == "msg2"


def test_write_validation_report_handles_empty_flags(tmp_path):
    from agents.pipeline_audit_agent import write_validation_report

    path = write_validation_report({"output_dir": str(tmp_path), "validation_flags": []})
    with open(path) as f:
        rows = list(csv.DictReader(f))
    assert rows == []
