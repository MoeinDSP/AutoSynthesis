"""
agents/effect_size_agent.py::effect_size_node -- outcome_family/
follow_up_timepoint from meta_ready_results.json must reach
EffectSizeRecord.outcome_group_key (built via utils/outcome_grouping.py),
not just be read and dropped.
"""

import json
import os

from utils.outcome_grouping import build_outcome_group_key


def _write_meta_ready(tmp_path, rows):
    path = os.path.join(str(tmp_path), "meta_ready_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f)
    return path


def _base_row(**overrides):
    row = {
        "paper_id": "p1",
        "comparison_label": "R1",
        "Outcome variable": "PROMIS Cognitive Abilities",
        "Include/Exclude": "Include",
        "hedges_g": "0.34",
        "cohens_d": "0.34",
        "n_treatment": "25",
        "n_control": "25",
        "effect_size_ready": "true",
    }
    row.update(overrides)
    return row


def test_effect_size_node_builds_outcome_group_key_from_family_and_timepoint(tmp_path):
    from agents.effect_size_agent import effect_size_node

    _write_meta_ready(tmp_path, [
        _base_row(outcome_family="subjective_cognitive_function", follow_up_timepoint="intermediate (1-6 months)"),
    ])
    state = {"output_dir": str(tmp_path)}
    result = effect_size_node(state)

    assert len(result["effect_sizes"]) == 1
    es = result["effect_sizes"][0]
    assert es.outcome_family == "subjective_cognitive_function"
    assert es.follow_up_timepoint == "intermediate (1-6 months)"
    assert es.outcome_group_key == build_outcome_group_key(
        "subjective_cognitive_function", "intermediate (1-6 months)"
    )
    assert es.outcome_name == "PROMIS Cognitive Abilities"


def test_effect_size_node_falls_back_to_default_group_when_no_family(tmp_path):
    from agents.effect_size_agent import effect_size_node

    _write_meta_ready(tmp_path, [_base_row(outcome_family="", follow_up_timepoint="")])
    state = {"output_dir": str(tmp_path)}
    result = effect_size_node(state)

    es = result["effect_sizes"][0]
    assert es.outcome_family is None
    assert es.follow_up_timepoint is None
    assert es.outcome_group_key == "default"


def test_effect_size_node_two_constructs_get_different_group_keys(tmp_path):
    from agents.effect_size_agent import effect_size_node

    _write_meta_ready(tmp_path, [
        _base_row(comparison_label="R1", outcome_family="subjective_cognitive_function"),
        _base_row(comparison_label="R2", outcome_family="verbal_learning"),
    ])
    state = {"output_dir": str(tmp_path)}
    result = effect_size_node(state)

    keys = {es.outcome_group_key for es in result["effect_sizes"]}
    assert keys == {"subjective_cognitive_function", "verbal_learning"}
