"""utils/outcome_grouping.py -- the declarative outcome_group_key builder
shared by agents/effect_size_agent.py (production pipeline) and
cochrane_benchmark/evaluation/meta_eval.py (benchmark re-evaluation)."""

from utils.outcome_grouping import (
    DEFAULT_GROUP_KEY,
    MIN_K_FOR_POOLING,
    build_outcome_group_key,
    group_label,
    safe_filename_fragment,
)


def test_no_outcome_family_falls_back_to_default_key():
    # Legacy/degenerate case -- no classification available at all -- must
    # collapse to ONE group so single-outcome runs keep behaving as before.
    assert build_outcome_group_key(None, None) == DEFAULT_GROUP_KEY
    assert build_outcome_group_key("", "") == DEFAULT_GROUP_KEY
    assert build_outcome_group_key(None, "intermediate") == DEFAULT_GROUP_KEY


def test_family_alone_builds_normalised_key():
    assert build_outcome_group_key("Subjective memory") == "subjective memory"
    assert build_outcome_group_key("  Subjective   Memory  ") == "subjective memory"


def test_timepoint_is_metadata_only_by_default_not_a_split():
    # Requirement 3: do NOT auto-split into timepoint subgroups unless
    # explicitly requested (split_by_timepoint=True) -- default is False, so
    # the SAME construct at two different reported timepoints pools together
    # as ONE group by default, matching Cochrane's own "one outcome, one
    # pooled number" convention.
    key1 = build_outcome_group_key("subjective_cognitive_function", "intermediate (1-6 months)")
    key2 = build_outcome_group_key("subjective_cognitive_function", "immediate")
    assert key1 == key2 == "subjective_cognitive_function"


def test_split_by_timepoint_true_restores_timepoint_fragmentation():
    key1 = build_outcome_group_key(
        "subjective_cognitive_function", "intermediate (1-6 months)", split_by_timepoint=True
    )
    key2 = build_outcome_group_key(
        "subjective_cognitive_function", "immediate", split_by_timepoint=True
    )
    assert key1 != key2
    assert key1 == "subjective_cognitive_function::intermediate (1-6 months)"


def test_same_construct_different_timepoint_never_collides_when_split_requested():
    a = build_outcome_group_key("verbal memory", "immediate", split_by_timepoint=True)
    b = build_outcome_group_key("verbal memory", "long-term (>6 months)", split_by_timepoint=True)
    assert a != b


def test_comparison_family_always_splits_regardless_of_timepoint_flag():
    # Two different comparisons on the SAME outcome must never pool together
    # -- this is not gated by split_by_timepoint (that flag only concerns
    # follow_up_timepoint).
    a = build_outcome_group_key("mortality", comparison_family="drug_a_vs_placebo")
    b = build_outcome_group_key("mortality", comparison_family="drug_b_vs_placebo")
    assert a != b
    assert a == "mortality::drug_a_vs_placebo"


def test_comparison_and_timepoint_can_combine():
    key = build_outcome_group_key(
        "mortality", "long-term (>6 months)",
        comparison_family="drug_a_vs_placebo", split_by_timepoint=True,
    )
    assert key == "mortality::drug_a_vs_placebo::long-term (>6 months)"


def test_case_and_whitespace_insensitive():
    a = build_outcome_group_key("Verbal Memory", "Intermediate", split_by_timepoint=True)
    b = build_outcome_group_key("verbal   memory", "  intermediate ", split_by_timepoint=True)
    assert a == b


def test_different_families_never_share_a_key():
    subjective = build_outcome_group_key("subjective_cognitive_function", None)
    verbal = build_outcome_group_key("verbal_learning", None)
    processing = build_outcome_group_key("processing_speed", None)
    assert len({subjective, verbal, processing}) == 3


def test_group_label_human_readable():
    assert group_label(None, None) == "All outcomes (undifferentiated)"
    assert group_label("Subjective memory", None) == "Subjective memory"
    # Timepoint absent from the label by default, mirroring the key builder.
    assert group_label("Subjective memory", "Intermediate") == "Subjective memory"
    assert group_label(
        "Subjective memory", "Intermediate", split_by_timepoint=True
    ) == "Subjective memory (Intermediate)"
    assert group_label(
        "mortality", None, comparison_family="drug_a_vs_placebo"
    ) == "mortality (drug_a_vs_placebo)"


def test_safe_filename_fragment_sanitises_key():
    frag = safe_filename_fragment("subjective_cognitive_function::intermediate (1-6 months)")
    assert " " not in frag
    assert "(" not in frag and ")" not in frag
    assert frag  # non-empty


def test_min_k_for_pooling_is_the_smallest_defensible_value():
    # Not an arbitrary large threshold (requirement 9) -- 2 is the smallest
    # k for which a random-effects tau^2 estimate is even defined.
    assert MIN_K_FOR_POOLING == 2
