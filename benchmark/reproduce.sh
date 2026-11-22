#!/usr/bin/env bash
# Reproduces every benchmark number and figure of the paper from the files in data/ and runs/.
# Usage:  bash benchmark/reproduce.sh        (takes about a minute, no API key needed)
set -euo pipefail
PY="${PYTHON:-python3}"
cd "$(dirname "$0")/scripts"
export BENCH_HARMONIZE=1   # put every model result on Cochrane's effect measure (see README, "Harmonization")

echo "1/3  Benchmark metrics ..."
"$PY" repool_from_runs.py      > /dev/null   # re-pool rows a formula cannot convert -> data/repooled_results.csv
"$PY" benchmark_metrics.py     > /dev/null   # per-review audit + summary -> results/

echo "2/3  Figures ..."
for s in generate_tolerance_bars generate_double_whisker generate_paper_style_figures generate_unitfree_figures \
         generate_topic_breakdown generate_funnel_flow generate_venn_search; do
  "$PY" "$s.py" > /dev/null
done

echo "3/3  Fully automatic runs ..."
"$PY" summarize_fully_automatic.py

echo "Done. Figures in benchmark/figures/, tables in benchmark/results/."
