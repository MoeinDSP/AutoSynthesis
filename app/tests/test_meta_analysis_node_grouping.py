"""
agents/meta_analysis_agent.py -- per-outcome-group pooling.

Regression tests built directly from the CD008754 root-cause investigation
(see cochrane_benchmark/README.md): AutoSynthesis correctly extracted and
classified a distinct "subjective_cognitive_function" outcome from
Stuifbergen 2018 (alongside CVLT/PASAT/SDMT/COWAT rows classified into other
families), but meta_analysis_node used to pool ALL of them into one
undifferentiated model regardless of construct. These tests exercise the
real R/metafor pooling path (statistics/metafor_engine.py) and real plot
generation -- only the LLM interpretation call is mocked, since it isn't
part of what's being verified here.
"""

from unittest.mock import MagicMock, patch

import pytest

from models import EffectSizeRecord, MetaAnalysisPlan
from utils.outcome_grouping import build_outcome_group_key


def _plan(**kwargs):
    defaults = dict(
        research_question="q", treatment_label="t", control_label="c",
        outcome_description="o", positive_direction="p", search_queries=[],
        inclusion_criteria=[], exclusion_criteria=[], moderators_to_extract=[],
    )
    defaults.update(kwargs)
    return MetaAnalysisPlan(**defaults)


def _es(study_id, report_id, family=None, timepoint=None, comparison=None,
        reported_effect_measure=None, g=0.3, var=0.02, n=50, split_by_timepoint=False,
        trial_cluster_id=None, raw_measure_inputs=None):
    raw_measure_inputs = raw_measure_inputs if raw_measure_inputs is not None else {}
    return EffectSizeRecord(
        study_id=study_id,
        report_id=report_id,
        cohens_d=g,
        hedges_g=g,
        variance=var,
        se=var ** 0.5,
        ci_lower=g - 1.96 * var ** 0.5,
        ci_upper=g + 1.96 * var ** 0.5,
        n_total=n,
        computation_method="means_sds",
        outcome_name=report_id,
        outcome_family=family,
        comparison_family=comparison,
        follow_up_timepoint=timepoint,
        reported_effect_measure=reported_effect_measure,
        trial_cluster_id=trial_cluster_id,
        raw_measure_inputs=raw_measure_inputs,
        outcome_group_key=build_outcome_group_key(
            family, timepoint, comparison_family=comparison, split_by_timepoint=split_by_timepoint,
        ),
    )


def _counts(events_t, n_t, events_c, n_c):
    """Raw 2x2 event-count inputs -- the exact shape
    utils.effect_measures.compute_native_row_effect's dichotomous branch
    (and escalc_or_from_counts/escalc_rr_from_counts) reads."""
    return {
        "events_treatment": events_t, "n_treatment": n_t,
        "events_control": events_c, "n_control": n_c,
    }


@pytest.fixture(autouse=True)
def _mock_llm_interpretation():
    """meta_analysis_node calls llm.invoke() for a prose interpretation per
    group -- not what these tests check, and not something that should make
    them depend on network access. Real R/metafor pooling and real plot
    generation are left untouched."""
    mock_resp = MagicMock()
    mock_resp.content = "Mocked interpretation."
    with patch("agents.meta_analysis_agent.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_resp
        yield mock_llm


def _run(effect_sizes, tmp_path, plan=None):
    from agents.meta_analysis_agent import meta_analysis_node

    state = {"effect_sizes": effect_sizes, "output_dir": str(tmp_path), "plan": plan}
    return meta_analysis_node(state)


# ---------------------------------------------------------------------------
# Backward compatibility: no outcome_family anywhere -> exactly one group,
# behaves like the pre-grouping implementation.
# ---------------------------------------------------------------------------

def test_backward_compat_single_group_when_no_outcome_family(tmp_path):
    effect_sizes = [
        _es("paper_1", "R1", g=0.3, var=0.02),
        _es("paper_2", "R2", g=0.5, var=0.03),
        _es("paper_3", "R3", g=0.2, var=0.01),
    ]
    result = _run(effect_sizes, tmp_path)

    assert len(result["meta_results"]) == 1
    assert result["meta_results"][0].outcome_group_key == "default"
    assert result["meta_results"][0].k == 3
    assert not result["meta_results"][0].insufficient_data

    # Legacy top-level aliases still populated exactly as before.
    assert result["meta_result"] is not None
    assert result["meta_result"].k == 3
    assert result["meta_plots"]["forest"].endswith("forest_plot.png")  # unsuffixed
    assert result["meta_interpretation"] == {"overall": "Mocked interpretation."}


# ---------------------------------------------------------------------------
# The "default" (uncategorized) bucket must never be picked as the headline
# "primary" result just because it happens to have more contributing rows
# than any single real outcome family -- see the CD008754 screenshot
# investigation (Pooled Hedges' G=0.9349, k=9, was actually the unrelated
# leftover pile, not a real outcome).
# ---------------------------------------------------------------------------

def test_default_bucket_never_wins_primary_even_when_it_is_the_largest_group(tmp_path):
    effect_sizes = [
        # "default" (unclassified) bucket: 4 unrelated rows -- larger than
        # any single real family below.
        _es("d1", "D1", family=None, g=0.9, var=0.05),
        _es("d2", "D2", family=None, g=1.1, var=0.05),
        _es("d3", "D3", family=None, g=0.8, var=0.05),
        _es("d4", "D4", family=None, g=1.0, var=0.05),
        # Real classified family: only 2 rows, but a REAL construct.
        _es("p1", "subj_1", family="subjective_cognitive_function", g=0.2, var=0.02),
        _es("p2", "subj_2", family="subjective_cognitive_function", g=0.3, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert groups["default"].k == 4
    assert groups["subjective_cognitive_function"].k == 2

    # The UI's headline "Key Statistics" (meta_result) must be the real,
    # classified outcome -- never the bigger-but-meaningless default pile.
    assert result["meta_result"].k == 2
    assert result["meta_result"] is groups["subjective_cognitive_function"].result


def test_default_bucket_is_primary_when_it_is_the_only_group(tmp_path):
    # Legacy/degenerate case must be unaffected: if "default" is the ONLY
    # group that exists at all (nothing was ever classified), it must still
    # become primary -- see test_backward_compat_single_group_when_no_outcome_family.
    effect_sizes = [
        _es("paper_1", "R1", g=0.3, var=0.02),
        _es("paper_2", "R2", g=0.5, var=0.03),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert result["meta_result"] is groups["default"].result


# ---------------------------------------------------------------------------
# Distinct constructs must never be pooled together.
# ---------------------------------------------------------------------------

def test_distinct_outcome_families_are_pooled_separately(tmp_path):
    effect_sizes = [
        _es("p1", "subj_1", family="subjective_cognitive_function", g=0.2, var=0.02),
        _es("p2", "subj_2", family="subjective_cognitive_function", g=0.3, var=0.02),
        _es("p3", "verbal_1", family="verbal_learning", g=0.6, var=0.03),
        _es("p4", "verbal_2", family="verbal_learning", g=0.7, var=0.03),
        _es("p5", "proc_1", family="processing_speed", g=0.4, var=0.02),
        _es("p6", "proc_2", family="processing_speed", g=0.5, var=0.02),
        _es("p7", "work_1", family="working_memory", g=0.1, var=0.02),
        _es("p8", "work_2", family="working_memory", g=0.15, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert set(groups.keys()) == {
        "subjective_cognitive_function", "verbal_learning", "processing_speed", "working_memory",
    }
    for key, group in groups.items():
        assert group.k == 2
        assert not group.insufficient_data
        expected_ids = {es.study_id for es in effect_sizes if es.outcome_group_key == key}
        assert set(group.study_ids) == expected_ids
    # No cross-contamination: the subjective-memory group's study_ids are
    # exactly its own two papers, none of the other constructs' papers.
    assert set(groups["subjective_cognitive_function"].study_ids) == {"p1", "p2"}
    assert set(groups["verbal_learning"].study_ids) == {"p3", "p4"}


def test_same_construct_different_timepoint_pools_together_by_default(tmp_path):
    # Requirement 3: do NOT auto-split into timepoint subgroups unless the
    # plan explicitly requests it -- default (plan=None / split_by_timepoint
    # unset) is Cochrane's own convention: ONE pooled number per outcome,
    # regardless of each study's individual follow-up length.
    effect_sizes = [
        _es("p1", "immediate_1", family="subjective memory", timepoint="immediate", g=0.15, var=0.02),
        _es("p2", "immediate_2", family="subjective memory", timepoint="immediate", g=0.2, var=0.02),
        _es("p3", "interm_1", family="subjective memory", timepoint="intermediate (1-6 months)", g=0.25, var=0.02),
        _es("p4", "interm_2", family="subjective memory", timepoint="intermediate (1-6 months)", g=0.3, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 1
    key = build_outcome_group_key("subjective memory")
    assert set(groups.keys()) == {key}
    assert groups[key].k == 4
    assert set(groups[key].study_ids) == {"p1", "p2", "p3", "p4"}
    # follow_up_timepoint is still preserved as per-row metadata even though
    # it didn't fragment the pooling group.
    assert {es.follow_up_timepoint for es in effect_sizes} == {"immediate", "intermediate (1-6 months)"}


def test_same_construct_different_timepoint_split_when_plan_requests_it(tmp_path):
    plan = _plan(split_by_timepoint=True)
    effect_sizes = [
        _es("p1", "immediate_1", family="subjective memory", timepoint="immediate", g=0.15, var=0.02, split_by_timepoint=True),
        _es("p2", "immediate_2", family="subjective memory", timepoint="immediate", g=0.2, var=0.02, split_by_timepoint=True),
        _es("p3", "interm_1", family="subjective memory", timepoint="intermediate (1-6 months)", g=0.25, var=0.02, split_by_timepoint=True),
        _es("p4", "interm_2", family="subjective memory", timepoint="intermediate (1-6 months)", g=0.3, var=0.02, split_by_timepoint=True),
    ]
    result = _run(effect_sizes, tmp_path, plan=plan)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 2
    immediate_key = build_outcome_group_key("subjective memory", "immediate", split_by_timepoint=True)
    intermediate_key = build_outcome_group_key("subjective memory", "intermediate (1-6 months)", split_by_timepoint=True)
    assert set(groups.keys()) == {immediate_key, intermediate_key}
    assert set(groups[immediate_key].study_ids) == {"p1", "p2"}
    assert set(groups[intermediate_key].study_ids) == {"p3", "p4"}


def test_different_comparisons_on_same_outcome_are_pooled_separately(tmp_path):
    # Requirement 4: multiple comparisons within one review must never be
    # pooled together just because they share an outcome.
    effect_sizes = [
        _es("p1", "a_1", family="mortality", comparison="drug_a_vs_placebo", g=0.1, var=0.02),
        _es("p2", "a_2", family="mortality", comparison="drug_a_vs_placebo", g=0.15, var=0.02),
        _es("p3", "b_1", family="mortality", comparison="drug_b_vs_placebo", g=0.4, var=0.02),
        _es("p4", "b_2", family="mortality", comparison="drug_b_vs_placebo", g=0.45, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 2
    a_key = build_outcome_group_key("mortality", comparison_family="drug_a_vs_placebo")
    b_key = build_outcome_group_key("mortality", comparison_family="drug_b_vs_placebo")
    assert set(groups.keys()) == {a_key, b_key}
    assert set(groups[a_key].study_ids) == {"p1", "p2"}
    assert set(groups[b_key].study_ids) == {"p3", "p4"}


def test_incompatible_effect_measures_in_one_group_are_auto_split(tmp_path):
    # Regression test for the CD008986 bug: rows landing in the same
    # outcome_group_key (e.g. an undifferentiated "default" bucket) but
    # reporting DIFFERENT effect measures (HR vs OR) must never be silently
    # pooled together on a common Hedges' g fallback.
    effect_sizes = [
        _es("p1", "hr_1", family="mortality", reported_effect_measure="hazard ratio", g=0.1, var=0.02),
        _es("p2", "hr_2", family="mortality", reported_effect_measure="hazard ratio", g=0.15, var=0.02),
        _es("p3", "or_1", family="mortality", reported_effect_measure="odds ratio", g=0.4, var=0.02),
        _es("p4", "or_2", family="mortality", reported_effect_measure="odds ratio", g=0.45, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 2
    base_key = build_outcome_group_key("mortality")
    hr_key = f"{base_key}::measure=HR"
    or_key = f"{base_key}::measure=OR"
    assert set(groups.keys()) == {hr_key, or_key}
    assert set(groups[hr_key].study_ids) == {"p1", "p2"}
    assert set(groups[or_key].study_ids) == {"p3", "p4"}
    # Never silent -- both split groups record why.
    assert groups[hr_key].split_reason is not None
    assert "HR" in groups[hr_key].split_reason and "OR" in groups[hr_key].split_reason
    assert groups[or_key].split_reason == groups[hr_key].split_reason


def test_unlabeled_rows_join_rr_over_or_on_a_genuine_tie(tmp_path):
    # Preference hierarchy (tie-breaker only, never absolute -- see
    # utils/effect_measures.py::dichotomous_tie_break()): when an explicit
    # RR bucket and an explicit OR bucket are EXACTLY tied in size, rows with
    # no stated measure at all should join the RR bucket (Cochrane's own
    # dichotomous-outcome default), not whichever bucket happened to be
    # built first.
    effect_sizes = [
        _es("p1", "rr_1", family="mortality", reported_effect_measure="risk ratio", g=0.1, var=0.02),
        _es("p2", "or_1", family="mortality", reported_effect_measure="odds ratio", g=0.4, var=0.02),
        _es("p3", "u_1", family="mortality", reported_effect_measure=None, g=0.2, var=0.02),
        _es("p4", "u_2", family="mortality", reported_effect_measure=None, g=0.25, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    base_key = build_outcome_group_key("mortality")
    rr_key = f"{base_key}::measure=RR"
    or_key = f"{base_key}::measure=OR"
    assert set(groups.keys()) == {rr_key, or_key}
    # The two unlabeled rows (p3, p4) joined the RR bucket, not OR.
    assert set(groups[rr_key].study_ids) == {"p1", "p3", "p4"}
    assert set(groups[or_key].study_ids) == {"p2"}


def test_unlabeled_rows_do_not_force_rr_over_a_real_hr_majority(tmp_path):
    # The other half of the same guarantee: this is a TIE-BREAKER only.
    # 2 explicit HR rows genuinely outnumber 1 explicit RR row -- the
    # unlabeled row must join the real majority (HR), never be pulled
    # toward RR just because RR is preferred on ties.
    effect_sizes = [
        _es("p1", "hr_1", family="mortality", reported_effect_measure="hazard ratio", g=0.1, var=0.02),
        _es("p2", "hr_2", family="mortality", reported_effect_measure="hazard ratio", g=0.15, var=0.02),
        _es("p3", "rr_1", family="mortality", reported_effect_measure="risk ratio", g=0.4, var=0.02),
        _es("p4", "u_1", family="mortality", reported_effect_measure=None, g=0.2, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    base_key = build_outcome_group_key("mortality")
    hr_key = f"{base_key}::measure=HR"
    rr_key = f"{base_key}::measure=RR"
    assert set(groups[hr_key].study_ids) == {"p1", "p2", "p4"}
    assert set(groups[rr_key].study_ids) == {"p3"}


def test_unlabeled_rows_with_raw_counts_reroute_to_dichotomous_over_hr(tmp_path):
    # Root-cause regression test for the real CD008986 re-run bug: HR is
    # the explicit plurality (5 rows in the real case; 2 here), but rows
    # with NO stated measure that DO carry raw 2x2 event counts must join
    # the dichotomous (RR) bucket instead -- HR has no counts-
    # reconstruction path at all, so joining it would make them permanent,
    # avoidable dead weight excluded from every pooled result.
    effect_sizes = [
        _es("p1", "hr_1", family="mortality", reported_effect_measure="hazard ratio", g=0.1, var=0.02),
        _es("p2", "hr_2", family="mortality", reported_effect_measure="hazard ratio", g=0.15, var=0.02),
        _es("p3", "rr_1", family="mortality", reported_effect_measure="risk ratio", g=0.4, var=0.02,
            raw_measure_inputs=_counts(10, 100, 15, 100)),
        _es("p4", "u_1", family="mortality", reported_effect_measure=None, g=0.2, var=0.02,
            raw_measure_inputs=_counts(8, 90, 12, 88)),
        _es("p5", "u_2", family="mortality", reported_effect_measure=None, g=0.22, var=0.02,
            raw_measure_inputs=_counts(9, 95, 14, 92)),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    base_key = build_outcome_group_key("mortality")
    hr_key = f"{base_key}::measure=HR"
    rr_key = f"{base_key}::measure=RR"

    # p4/p5 (unlabeled, but with usable raw counts) joined RR, not HR.
    assert set(groups[hr_key].study_ids) == {"p1", "p2"}
    assert set(groups[rr_key].study_ids) == {"p3", "p4", "p5"}
    # And they're genuinely POOLABLE there, not just structurally present --
    # this is the actual point of the fix, not merely bucket membership.
    assert groups[rr_key].k == 3
    assert groups[rr_key].result is not None
    assert not groups[rr_key].insufficient_data


def test_unlabeled_rows_reroute_only_when_individually_reconstructable(tmp_path):
    # Mixed case: of two unlabeled rows, only ONE actually carries raw
    # counts -- routing must be decided per-row, not as a single
    # all-or-nothing decision for the whole unlabeled set.
    effect_sizes = [
        _es("p1", "hr_1", family="mortality", reported_effect_measure="hazard ratio", g=0.1, var=0.02),
        _es("p2", "hr_2", family="mortality", reported_effect_measure="hazard ratio", g=0.15, var=0.02),
        _es("p3", "rr_1", family="mortality", reported_effect_measure="risk ratio", g=0.4, var=0.02,
            raw_measure_inputs=_counts(10, 100, 15, 100)),
        _es("p4", "u_with_counts", family="mortality", reported_effect_measure=None, g=0.2, var=0.02,
            raw_measure_inputs=_counts(8, 90, 12, 88)),
        _es("p5", "u_no_counts", family="mortality", reported_effect_measure=None, g=0.2, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    base_key = build_outcome_group_key("mortality")
    hr_key = f"{base_key}::measure=HR"
    rr_key = f"{base_key}::measure=RR"

    assert set(groups[hr_key].study_ids) == {"p1", "p2", "p5"}  # p5 has nothing to reconstruct with -- stays put
    assert set(groups[rr_key].study_ids) == {"p3", "p4"}


def test_unlabeled_rows_with_counts_reroute_to_or_when_or_is_the_only_alternative(tmp_path):
    # Same feasibility principle, OR instead of RR -- not an RR-specific
    # special case.
    effect_sizes = [
        _es("p1", "hr_1", family="mortality", reported_effect_measure="hazard ratio", g=0.1, var=0.02),
        _es("p2", "hr_2", family="mortality", reported_effect_measure="hazard ratio", g=0.15, var=0.02),
        _es("p3", "or_1", family="mortality", reported_effect_measure="odds ratio", g=0.4, var=0.02,
            raw_measure_inputs=_counts(10, 100, 15, 100)),
        _es("p4", "u_1", family="mortality", reported_effect_measure=None, g=0.2, var=0.02,
            raw_measure_inputs=_counts(8, 90, 12, 88)),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    base_key = build_outcome_group_key("mortality")
    hr_key = f"{base_key}::measure=HR"
    or_key = f"{base_key}::measure=OR"

    assert set(groups[hr_key].study_ids) == {"p1", "p2"}
    assert set(groups[or_key].study_ids) == {"p3", "p4"}


# ---------------------------------------------------------------------------
# Safeguard: tiny groups are reported, never silently merged.
# ---------------------------------------------------------------------------

def test_insufficient_data_group_is_reported_not_merged(tmp_path):
    effect_sizes = [
        _es("p1", "verbal_1", family="verbal_learning", g=0.4, var=0.02),
        _es("p2", "verbal_2", family="verbal_learning", g=0.5, var=0.02),
        _es("p3", "subj_lone", family="subjective_cognitive_function", g=0.34, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 2

    lone = groups["subjective_cognitive_function"]
    assert lone.insufficient_data is True
    assert lone.k == 1
    assert lone.result is None
    assert lone.single_effect_g == pytest.approx(0.34)
    assert lone.study_ids == ["p3"]

    verbal = groups["verbal_learning"]
    assert verbal.insufficient_data is False
    assert verbal.k == 2
    assert verbal.result is not None
    # The lone study must not have leaked into the other group.
    assert "p3" not in verbal.study_ids

    # The largest VALID group (verbal_learning) becomes the backward-compat
    # primary, never the insufficient one.
    assert result["meta_result"] is not None
    assert result["meta_result"].k == 2


def test_empty_effect_sizes_overwrites_a_stale_result_from_a_prior_run(tmp_path):
    # Built directly from a real CD014821 bug: output_dir is reused across
    # runs within one dashboard session (run_service.py keys it off
    # session_id, not run id). When a run genuinely has zero poolable
    # effect sizes, meta_analysis_node used to return early WITHOUT writing
    # meta_analysis_result.json/meta_analysis_results_by_group.json at all
    # -- leaving a PREVIOUS, unrelated run's files (a different Cochrane
    # review, a different outcome) sitting there looking like this run's
    # real answer. It must always write a fresh, genuinely-empty result.
    import json
    stale_result = {"pooled_g": -0.99, "k": 15, "n_total": 1308}
    stale_by_group = [{"outcome_group_key": "some_other_review_outcome", "k": 15}]
    (tmp_path / "meta_analysis_result.json").write_text(json.dumps(stale_result))
    (tmp_path / "meta_analysis_results_by_group.json").write_text(json.dumps(stale_by_group))

    result = _run([], tmp_path)

    assert result["meta_result"] is None
    assert result["meta_results"] == []
    on_disk = json.loads((tmp_path / "meta_analysis_result.json").read_text())
    assert on_disk == {}
    on_disk_by_group = json.loads((tmp_path / "meta_analysis_results_by_group.json").read_text())
    assert on_disk_by_group == []


def test_all_groups_insufficient_yields_no_primary_result(tmp_path):
    effect_sizes = [
        _es("p1", "a", family="construct_a", g=0.3, var=0.02),
        _es("p2", "b", family="construct_b", g=0.4, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    assert len(result["meta_results"]) == 2
    assert all(g.insufficient_data for g in result["meta_results"])
    assert result["meta_result"] is None
    assert result["meta_plots"] == {}


# ---------------------------------------------------------------------------
# Direct reproduction of the diagnosed CD008754 scenario: Stuifbergen 2018
# contributes 5 rows across 4 different constructs from ONE paper; the
# correctly-classified subjective-memory row must end up in its own group,
# never pooled with the CVLT/PASAT/SDMT/COWAT rows.
# ---------------------------------------------------------------------------

def test_stuifbergen_2018_subjective_memory_row_stays_in_correct_group(tmp_path):
    paper_id = "deep_research:9370855"  # Stuifbergen 2018, real paper_id from the CD008754 run
    effect_sizes = [
        _es(paper_id, "CVLT Delayed", family="verbal_learning", g=0.45, var=0.03),
        _es(paper_id, "PASAT 3-sec", family="processing_speed", g=0.31, var=0.02),
        _es(paper_id, "PROMIS Cognitive Abilities", family="subjective_cognitive_function", g=0.34, var=0.02),
        _es(paper_id, "SDMT", family="processing_speed", g=0.28, var=0.02),
        _es(paper_id, "COWAT", family="verbal_fluency", g=0.19, var=0.02),
        # A second paper's subjective-memory row, so that group has k=2 and
        # actually gets pooled (rather than reported as insufficient_data,
        # which would otherwise mask the "stays in the correct group" check).
        _es("other_paper", "Subjective memory scale", family="subjective_cognitive_function", g=0.22, var=0.02),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    subj = groups["subjective_cognitive_function"]

    assert subj.k == 2
    assert not subj.insufficient_data
    subj_report_ids = {
        es.report_id for es in effect_sizes if es.outcome_group_key == "subjective_cognitive_function"
    }
    assert subj_report_ids == {"PROMIS Cognitive Abilities", "Subjective memory scale"}

    # The other 4 Stuifbergen rows must NOT be in the subjective-memory group.
    assert paper_id in subj.study_ids  # PROMIS row is there...
    other_families_present = {"verbal_learning", "processing_speed", "verbal_fluency"}
    assert other_families_present.isdisjoint(set(groups.keys()) & {"subjective_cognitive_function"})
    # Each of those 3 other constructs is its own (k=1, insufficient) group,
    # not folded into subjective_cognitive_function or into each other.
    for fam in ("verbal_learning", "processing_speed", "verbal_fluency"):
        assert fam in groups
        assert groups[fam].outcome_group_key != subj.outcome_group_key
    assert groups["processing_speed"].k == 2  # PASAT + SDMT share this construct
    assert groups["processing_speed"].insufficient_data is False


def test_same_trial_cluster_only_one_row_contributes_to_pooling(tmp_path):
    # Two different PAPERS describing the SAME trial (same trial_cluster_id)
    # must not both count as independent evidence within one outcome group --
    # the larger-N row is kept, the other excluded with a recorded reason.
    effect_sizes = [
        _es("paperA", "r1", family="mortality", g=0.1, var=0.02, n=200, trial_cluster_id="trial_xyz"),
        _es("paperB", "r2", family="mortality", g=0.9, var=0.02, n=50, trial_cluster_id="trial_xyz"),
        _es("paperC", "r3", family="mortality", g=0.2, var=0.02, n=80),
    ]
    result = _run(effect_sizes, tmp_path)

    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert len(groups) == 1
    group = list(groups.values())[0]
    assert group.k == 2  # paperA (kept, larger n) + paperC -- paperB excluded
    assert set(group.study_ids) == {"paperA", "paperC"}

    flags = result["validation_flags"]
    assert any(f.stage == "trial_dedup" and "paperB" in f.message for f in flags)


def test_unclustered_rows_unaffected_by_trial_dedup(tmp_path):
    effect_sizes = [
        _es("p1", "r1", family="mortality", g=0.1, var=0.02, n=50),
        _es("p2", "r2", family="mortality", g=0.2, var=0.02, n=60),
    ]
    result = _run(effect_sizes, tmp_path)
    groups = {g.outcome_group_key: g for g in result["meta_results"]}
    assert list(groups.values())[0].k == 2
