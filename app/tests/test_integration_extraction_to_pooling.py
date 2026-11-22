"""
Integration test: raw extracted rows -> conversion -> effect sizes -> pooled
groups, chaining the REAL modules together (utils/paper_results_converter.py,
agents/effect_size_agent.py, agents/meta_analysis_agent.py -- real R/metafor
pooling, only the LLM interpretation call mocked) rather than re-testing any
one module in isolation (see test_paper_results_converter_ratio_measures.py,
test_effect_measures_resolution.py, test_meta_analysis_node_grouping.py for
those unit-level tests).

Outcome_family/comparison_family/follow_up_timepoint are set directly on the
synthetic input rows, standing in for what agents/cross_paper_outcome_
mapper_agent.py's mapping_node would have already written by the time
export_table_node (convert_paper_results) runs in the real graph -- that
LLM-driven classification step has its own dedicated, mocked-LLM test file
(test_cross_paper_outcome_mapper_wiring.py) and isn't re-exercised here.
trial_cluster_id is set directly on synthetic PaperRecords, standing in for
what agents/document_type_agent.py's assign_trial_clusters() would have
already computed (see test_trial_matching.py for that).

Covers, in one review-sized synthetic dataset: binary outcomes, continuous
outcomes, different effect measures (OR/RR/HR/SMD) kept separate, a 3-arm
trial split into pairwise comparisons, median/IQR conversion, a genuinely
unusable row, and two "papers" reporting the same trial (deduped at pooling).
"""

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from models import PaperRecord
from utils.paper_results_converter import convert_paper_results


def _row(**kwargs):
    base = dict(
        paper_id="p", paper_title="t", true_research_question="q",
        study_label="Study 1", task_or_measure="m", outcome_name="o",
        result_role="primary_outcome", comparison_type="between_subjects",
        statistic_type="other", evidence_quote="q", page_or_section="Results",
        outcome_family=None, comparison_family=None, follow_up_timepoint=None,
    )
    base.update(kwargs)
    return base


@pytest.fixture(autouse=True)
def _mock_llm_interpretation():
    mock_resp = MagicMock()
    mock_resp.content = "Mocked interpretation."
    with patch("agents.meta_analysis_agent.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_resp
        yield mock_llm


def _build_fixture_rows():
    return [
        # Paper A: binary outcome, event counts -> mortality (default measure resolution)
        _row(paper_id="paperA", outcome_name="mortality", statistic_type="proportion",
             group_1_n=100, group_2_n=100, group_1_mean=0.30, group_2_mean=0.20,
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        # Paper B: continuous outcome, means/SDs -> quality of life
        _row(paper_id="paperB", outcome_name="quality of life", statistic_type="descriptive",
             group_1_n=50, group_2_n=50, group_1_mean=40.0, group_1_sd=8.0,
             group_2_mean=45.0, group_2_sd=8.5,
             outcome_family="quality_of_life", comparison_family="drug_vs_placebo"),
        # Paper C: directly-reported HR -> mortality (different measure than paper A)
        _row(paper_id="paperC", outcome_name="mortality", statistic_type="regression",
             group_1_n=150, group_2_n=150, hazard_ratio=1.4, ci_lower_hr=1.05, ci_upper_hr=1.9,
             reported_effect_measure="hazard ratio",
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        # Paper D: directly-reported RR -> readmissions
        _row(paper_id="paperD", outcome_name="readmissions", statistic_type="proportion",
             group_1_n=120, group_2_n=120, risk_ratio=0.8, ci_lower_rr=0.62, ci_upper_rr=1.03,
             reported_effect_measure="risk ratio",
             outcome_family="readmissions", comparison_family="drug_vs_placebo"),
        # Paper E: median/IQR -> quality of life, long-term timepoint
        _row(paper_id="paperE", outcome_name="quality of life (long-term)", statistic_type="descriptive",
             group_1_n=60, group_2_n=60,
             group_1_median=42, group_1_iqr_lower=35, group_1_iqr_upper=50,
             group_2_median=48, group_2_iqr_lower=40, group_2_iqr_upper=55,
             outcome_family="quality_of_life", comparison_family="drug_vs_placebo",
             follow_up_timepoint="long-term (>6 months)"),
        # Paper F: 3-arm trial -> mortality. Row-per-arm shape (group_label/
        # mean/sd/n) is what build_pairwise_comparisons() expects as input --
        # it collapses these into 2 pairwise rows (high_dose vs control,
        # low_dose vs control), selecting "control" as the reference arm.
        # Both non-control arms explicitly report an odds ratio -- gives the
        # "incompatible measures within one outcome group" scenario below TWO
        # rows on OR (vs. paperC's one row on HR), so the auto-split actually
        # has two real sub-buckets to form (a lone dissenting row would
        # instead trigger the pre-existing "too few rows for the native
        # scale -> fall back to Hedges g for the whole group" backstop).
        _row(paper_id="paperF", outcome_name="mortality", statistic_type="proportion",
             comparison_type="descriptive_only", result_role="primary_outcome",
             group_label="control", mean=15.0, sd=4.0, n=80,
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        _row(paper_id="paperF", outcome_name="mortality", statistic_type="proportion",
             comparison_type="descriptive_only", result_role="primary_outcome",
             group_label="high_dose", mean=8.0, sd=3.5, n=80,
             odds_ratio=0.5, ci_lower_or=0.3, ci_upper_or=0.85, reported_effect_measure="odds ratio",
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        _row(paper_id="paperF", outcome_name="mortality", statistic_type="proportion",
             comparison_type="descriptive_only", result_role="primary_outcome",
             group_label="low_dose", mean=11.0, sd=3.8, n=80,
             odds_ratio=0.65, ci_lower_or=0.4, ci_upper_or=1.05, reported_effect_measure="odds ratio",
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        # Paper G: genuinely unusable -- only a p-value, nothing else
        _row(paper_id="paperG", outcome_name="mortality", statistic_type="unclear",
             p_value=0.04,
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        # Paper H / H2: two DIFFERENT papers reporting the SAME trial's mortality
        # outcome (deduped at pooling time via trial_cluster_id, not here).
        _row(paper_id="paperH", outcome_name="mortality", statistic_type="proportion",
             group_1_n=200, group_2_n=200, group_1_mean=0.22, group_2_mean=0.18,
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
        _row(paper_id="paperH2", outcome_name="mortality (companion report)", statistic_type="proportion",
             group_1_n=200, group_2_n=200, group_1_mean=0.21, group_2_mean=0.17,
             outcome_family="mortality", comparison_family="drug_vs_placebo"),
    ]


def test_full_extraction_to_pooling_integration(tmp_path):
    from agents.effect_size_agent import effect_size_node
    from agents.meta_analysis_agent import meta_analysis_node

    input_path = os.path.join(tmp_path, "paper_results.json")
    with open(input_path, "w") as f:
        json.dump(_build_fixture_rows(), f)

    # --- Conversion (utils/paper_results_converter.py, real) ---
    converted = convert_paper_results(input_path=input_path, output_dir=str(tmp_path))
    by_paper = {r["Study_ID"]: r for r in converted}

    # Binary/continuous/HR/RR/median-IQR all convert successfully.
    assert by_paper["paperA"]["Include/Exclude"] == "Include"
    assert by_paper["paperB"]["Include/Exclude"] == "Include"
    assert by_paper["paperC"]["Include/Exclude"] == "Include"
    assert by_paper["paperC"]["conversion_method"] == "hr_to_d_approx"
    assert by_paper["paperD"]["Include/Exclude"] == "Include"
    assert by_paper["paperD"]["conversion_method"] == "reported_rr"
    assert by_paper["paperE"]["Include/Exclude"] == "Include"
    assert by_paper["paperE"]["conversion_method"] == "median_iqr_wan2014_approx"

    # 3-arm trial (paper F) split into 2 pairwise comparison rows -- both convert.
    f_rows = [r for r in converted if r["Study_ID"] == "paperF"]
    assert len(f_rows) == 2
    assert all(r["Include/Exclude"] == "Include" for r in f_rows)

    # Genuinely unusable row (paper G) explicitly excluded, not silently dropped.
    assert by_paper["paperG"]["Include/Exclude"] == "Exclude"
    assert by_paper["paperG"]["Comment"]  # has a stated reason

    # --- Effect sizes (agents/effect_size_agent.py, real) ---
    papers_eligible = [
        PaperRecord(id="paperH", title="H", abstract="", year=2020, source="manual", trial_cluster_id="trial_hh"),
        PaperRecord(id="paperH2", title="H2", abstract="", year=2021, source="manual", trial_cluster_id="trial_hh"),
    ]
    state = {"output_dir": str(tmp_path), "papers_eligible": papers_eligible, "plan": None}
    es_result = effect_size_node(state)
    effect_sizes = es_result["effect_sizes"]
    # Every included row (paperG excluded, 3-arm paper F contributes 2 rows) produced an EffectSizeRecord.
    assert len(effect_sizes) == len(converted) - 1  # -1 for paperG

    # --- Pooling (agents/meta_analysis_agent.py, real R/metafor) ---
    meta_state = {"effect_sizes": effect_sizes, "output_dir": str(tmp_path), "plan": None}
    meta_result = meta_analysis_node(meta_state)
    groups = {g.outcome_group_key: g for g in meta_result["meta_results"]}

    # Different outcomes never pooled together.
    assert "quality_of_life::drug_vs_placebo" in groups
    assert "readmissions::drug_vs_placebo" in groups

    # Mortality: paperA/paperF(x2)/paperG(excluded)/paperH/paperH2 report a
    # proportions-derived measure, paperC reports HR -- incompatible, must
    # auto-split into separate groups (not silently pooled as one).
    mortality_groups = {k: g for k, g in groups.items() if k.startswith("mortality::drug_vs_placebo")}
    assert len(mortality_groups) >= 2
    hr_groups = [g for g in mortality_groups.values() if "HR" in (g.split_reason or "")]
    assert hr_groups, f"expected an HR-measure split group, got: {list(mortality_groups.keys())}"

    # Trial dedup: paperH and paperH2 share a trial_cluster_id -- only ONE of
    # them may contribute to whichever mortality sub-group they land in.
    all_study_ids = [sid for g in mortality_groups.values() for sid in g.study_ids]
    assert not ({"paperH", "paperH2"} <= set(all_study_ids))

    flags = meta_result["validation_flags"]
    assert any(f.stage == "trial_dedup" for f in flags)
