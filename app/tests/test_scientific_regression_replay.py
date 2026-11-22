"""Phase 5, layer 1 of the infra-migration's scientific verification: a
bit-exact, no-LLM replay (a minute or so, dominated by rpy2/R + metafor
package startup rather than any real computation) of the fully deterministic segment
of the pipeline (effect_size_node -> meta_analysis_node, the R/metafor-
driven statistics core) against real frozen inputs/outputs captured BEFORE
this migration touched anything.

Why this is the actual proof (not the benchmark comparison in
test_cochrane_benchmark_regression.py): planning/extraction/classification
are LLM-driven and genuinely non-deterministic run to run, so a full
pipeline before/after diff can never be bit-exact and asserting so would be
dishonest. The statistics core downstream of extraction has NO such
excuse -- given the same `meta_ready_results.json`, effect_size_node and
meta_analysis_node are pure functions of that file plus config (no LLM
calls, no network, no randomness), so their output must match a frozen
historical run to full float precision, forever. If it ever doesn't, the
migration (or literally anything else) broke the scientific core.

Fixtures (tests/fixtures/replay/<case>/) are `meta_ready_results.json` +
`expected_meta_analysis_result.json`, copied verbatim from real Cochrane
benchmark runs captured in cochrane_benchmark/runs/<review>/historical/
before any of this session's infrastructure work began (see
baselines/before/git_commit.txt for the exact commit). Both cases were
chosen because their PRIMARY outcome group actually pools (k>=2, not the
k=1 "insufficient_data" case that skips R entirely).
"""

import json
import shutil
from pathlib import Path

import pytest

from agents.effect_size_agent import effect_size_node
from agents.meta_analysis_agent import meta_analysis_node

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "replay"
CASES = sorted(p.name for p in FIXTURES_DIR.iterdir() if p.is_dir()) if FIXTURES_DIR.exists() else []


def _replay(case_dir: Path, tmp_path: Path):
    shutil.copy(case_dir / "meta_ready_results.json", tmp_path / "meta_ready_results.json")
    state = {"output_dir": str(tmp_path), "papers_eligible": [], "validation_flags": []}
    state.update(effect_size_node(state))
    return meta_analysis_node(state)


@pytest.mark.parametrize("case", CASES)
class TestDeterministicReplay:
    def test_pooled_statistics_match_frozen_output_to_full_precision(self, case, tmp_path):
        case_dir = FIXTURES_DIR / case
        expected = json.loads((case_dir / "expected_meta_analysis_result.json").read_text())
        result = _replay(case_dir, tmp_path)
        mr = result["meta_result"]
        assert mr is not None, f"{case}: replay produced no pooled result (expected a real one)"

        # Exact equality, not approximate -- this is the entire point: the
        # SAME input must produce the IDENTICAL output, not merely a close
        # one. Any of these being off (even in the last float digit) means
        # something changed in the deterministic core.
        for field in ["pooled_g", "pooled_se", "ci_lower", "ci_upper", "z_value", "p_value",
                      "tau_squared", "tau", "i_squared", "h_squared",
                      "q_statistic", "q_df", "q_p_value", "k", "n_total"]:
            assert getattr(mr, field) == expected[field], (
                f"{case}: field {field!r} drifted from the frozen historical "
                f"value ({getattr(mr, field)!r} != {expected[field]!r})"
            )
        assert mr.effect_measure.value == expected["effect_measure"]
        assert mr.computation_scale.value == expected["computation_scale"]

    def test_replay_is_itself_reproducible(self, case, tmp_path, tmp_path_factory):
        """Not just frozen-vs-live -- two independent replays of the same
        input must agree with each other too (rules out any hidden
        nondeterminism -- dict ordering, float formatting, etc. -- in the
        replay harness itself, separate from the real engine)."""
        case_dir = FIXTURES_DIR / case
        tmp2 = tmp_path_factory.mktemp("replay2")
        r1 = _replay(case_dir, tmp_path)["meta_result"]
        r2 = _replay(case_dir, tmp2)["meta_result"]
        assert r1.model_dump() == r2.model_dump()


def test_fixtures_are_present():
    """If this fails, the fixture directory is empty/missing -- every other
    test in this file will have silently collected zero cases (pytest
    parametrize with an empty list just skips, it doesn't fail), which
    would hide a real loss of regression coverage."""
    assert len(CASES) >= 2, (
        f"expected at least 2 replay fixture cases in {FIXTURES_DIR}, found {CASES}"
    )
