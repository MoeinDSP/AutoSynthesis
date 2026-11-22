# tests/test_effect_size_node.py
from unittest.mock import patch, MagicMock


def _make_state(effect_sizes=None, output_dir="/tmp"):
    return {
        "user_prompt": "test", "mode": "manual", "paper_files": [],
        "output_dir": output_dir,
        "plan": None, "papers_eligible": [], "study_maps": {},
        "paper_results": [], "mapped_results": [], "coded_csv_path": "",
        "effect_sizes": effect_sizes or [],
        "meta_result": None, "meta_plots": {}, "meta_interpretation": {},
        "moderator_results": [], "combined_model": {},
        "bias_result": None, "bias_funnel_path": "", "bias_interpretation": {},
        "report_path": "", "errors": [],
    }


def test_effect_size_node_returns_empty_list_when_no_meta_ready(tmp_path):
    from agents.effect_size_agent import effect_size_node
    state = _make_state(output_dir=str(tmp_path))
    # no meta_ready_results.json in tmp_path → empty effect sizes
    result = effect_size_node(state)
    assert result["effect_sizes"] == []


def test_export_table_node_calls_converter(tmp_path):
    import json
    from agents.effect_size_agent import export_table_node

    # create a minimal paper_results.json so converter has something to read
    paper_results_path = tmp_path / "paper_results.json"
    paper_results_path.write_text("[]")

    state = _make_state(output_dir=str(tmp_path))
    state["paper_results"] = []
    with patch("agents.effect_size_agent.convert_paper_results") as mock_conv:
        mock_conv.return_value = []
        result = export_table_node(state)
    mock_conv.assert_called_once()
    assert "coded_csv_path" in result


def _write_meta_ready(tmp_path, rows):
    import json
    (tmp_path / "meta_ready_results.json").write_text(json.dumps(rows))


def test_explicit_exclude_is_never_reincluded_via_precomputed_hedges_g(tmp_path):
    from agents.effect_size_agent import effect_size_node
    _write_meta_ready(tmp_path, [{
        "Study_ID": "study_1", "Report_ID": "R1",
        "Include/Exclude": "Exclude",
        "hedges_g": 0.627, "cohens_d": 0.6, "variance": 0.17, "n_total": 25,
        "Comment": "excluded by outcome classification: meta_analysis_candidate=False",
    }])
    state = _make_state(output_dir=str(tmp_path))
    result = effect_size_node(state)
    assert result["effect_sizes"] == []


def test_missing_include_exclude_field_still_uses_legacy_precomputed_fallback(tmp_path):
    from agents.effect_size_agent import effect_size_node
    _write_meta_ready(tmp_path, [{
        "Study_ID": "study_1", "Report_ID": "R1",
        "hedges_g": 0.3, "cohens_d": 0.3, "variance": 0.02, "n_total": 40,
    }])
    state = _make_state(output_dir=str(tmp_path))
    result = effect_size_node(state)
    assert len(result["effect_sizes"]) == 1


def test_explicit_include_row_is_kept(tmp_path):
    from agents.effect_size_agent import effect_size_node
    _write_meta_ready(tmp_path, [{
        "Study_ID": "study_1", "Report_ID": "R1",
        "Include/Exclude": "Include",
        "hedges_g": 0.3, "cohens_d": 0.3, "variance": 0.02, "n_total": 40,
    }])
    state = _make_state(output_dir=str(tmp_path))
    result = effect_size_node(state)
    assert len(result["effect_sizes"]) == 1


def test_zero_rows_overwrites_a_stale_effect_sizes_json_from_a_prior_run(tmp_path):
    from agents.effect_size_agent import effect_size_node
    # Built directly from a real CD014821 bug: output_dir is reused across
    # runs within one dashboard session. When every meta_ready row is
    # excluded (as here: percentage-only reporting, no raw event counts),
    # effect_sizes.json used to simply never be written -- leaving a
    # PREVIOUS, unrelated run's effect_sizes.json (a different review's
    # outcomes) sitting there and later read by meta_analysis_node as if it
    # were this run's real data.
    import json
    (tmp_path / "effect_sizes.json").write_text(json.dumps(
        [{"study_id": "some_other_review_study", "hedges_g": -0.99}]
    ))
    _write_meta_ready(tmp_path, [{
        "Study_ID": "study_1", "Report_ID": "R1",
        "Include/Exclude": "Exclude",
        "Comment": "only rounded arm percentages reported, no raw event counts",
    }])
    state = _make_state(output_dir=str(tmp_path))
    result = effect_size_node(state)

    assert result["effect_sizes"] == []
    on_disk = json.loads((tmp_path / "effect_sizes.json").read_text())
    assert on_disk == []
