"""
Declarative outcome-group-key construction.

Root-cause context (see cochrane_benchmark/ CD008754 investigation): the
pipeline's cross_paper_outcome_mapper_agent already classifies every result
row into a normalised `outcome_family` (and, since this module was added,
an optional `follow_up_timepoint`) -- but that classification used to be
computed and then discarded before pooling. effect_size_node and
meta_analysis_node pooled every row from every paper into ONE undifferentiated
random-effects model regardless of how many distinct constructs the rows
actually measured.

This module supplies the single, shared rule for turning that classification
into a grouping key, used by both agents/effect_size_agent.py (production
pipeline) and cochrane_benchmark/evaluation/meta_eval.py (benchmark
re-evaluation), so the two never drift out of sync.

Deliberately NOT a lookup table of known outcome names -- the key is built
purely from whatever the upstream classifier (an LLM, working from the
paper's own text) already produced for that row. No outcome name, construct,
or timepoint vocabulary is hardcoded here.
"""

from __future__ import annotations

import re
from typing import Optional

# Below this many contributing effect sizes, a group cannot support a
# random-effects heterogeneity estimate (tau^2 is undefined for k=1) -- not
# an arbitrary editorial threshold, the smallest statistically meaningful one.
MIN_K_FOR_POOLING = 2

DEFAULT_GROUP_KEY = "default"


def _normalise(value: Optional[str]) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def build_outcome_group_key(
    outcome_family: Optional[str],
    follow_up_timepoint: Optional[str] = None,
    comparison_family: Optional[str] = None,
    split_by_timepoint: bool = False,
) -> str:
    """Build a declarative grouping key from already-extracted/classified fields.

    - No outcome_family at all -> DEFAULT_GROUP_KEY ("default"). This is the
      legacy/degenerate case: every row collapses into one group, so a run
      with a single homogeneous outcome (or one predating this classification
      step) behaves exactly as it did before this change -- one pooled result.
    - outcome_family present -> the normalised family, optionally suffixed:
        - "::<comparison>" whenever comparison_family is present -- so two
          different comparisons on the SAME outcome (e.g. "drug A vs
          placebo" and "drug B vs placebo") are never pooled together. This
          is always applied when the field is populated; it isn't gated by
          split_by_timepoint (that flag only concerns follow_up_timepoint).
        - "::<timepoint>" ONLY when split_by_timepoint=True -- Cochrane's own
          convention is to pool an outcome as ONE number regardless of each
          study's individual follow-up length, unless the review itself
          explicitly analyzes it by timepoint (see
          models.MetaAnalysisPlan.split_by_timepoint). follow_up_timepoint is
          still captured as metadata on the record either way -- this flag
          only controls whether it fragments the POOLING group.

    A group with both a comparison and a timepoint suffix reads as
    "family::comparison::timepoint".
    """
    family = _normalise(outcome_family)
    if not family:
        return DEFAULT_GROUP_KEY

    key = family
    comparison = _normalise(comparison_family)
    if comparison:
        key = f"{key}::{comparison}"
    if split_by_timepoint:
        timepoint = _normalise(follow_up_timepoint)
        if timepoint:
            key = f"{key}::{timepoint}"
    return key


def group_label(
    outcome_family: Optional[str],
    follow_up_timepoint: Optional[str],
    comparison_family: Optional[str] = None,
    split_by_timepoint: bool = False,
) -> str:
    """Human-readable label for a group, for reports/plots/interpretation prompts.

    Mirrors build_outcome_group_key()'s own gating: the timepoint only
    appears in the label when split_by_timepoint actually put it in the key,
    so the label never implies a split that didn't happen."""
    family = (outcome_family or "").strip()
    if not family:
        return "All outcomes (undifferentiated)"

    parts = [family]
    comparison = (comparison_family or "").strip()
    if comparison:
        parts.append(comparison)
    if split_by_timepoint:
        timepoint = (follow_up_timepoint or "").strip()
        if timepoint:
            parts.append(timepoint)

    if len(parts) == 1:
        return family
    return f"{family} ({', '.join(parts[1:])})"


def safe_filename_fragment(key: str) -> str:
    """Sanitise a group key for use inside a filename."""
    frag = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    return frag[:80] or "group"
