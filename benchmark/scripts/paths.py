"""Folder layout of the benchmark (all paths are relative to this repository)."""
import os
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.dirname(SCRIPTS)
DATA = os.path.join(BENCH, "data")        # inputs: Cochrane values, AutoSynthesis values, review metadata
RUNS = os.path.join(BENCH, "runs")        # per-review AutoSynthesis outputs (study-level data)
FIG = os.path.join(BENCH, "figures")      # generated figures (PDF)
RESULTS = os.path.join(BENCH, "results")  # generated tables
for _d in (FIG, RESULTS):
    os.makedirs(_d, exist_ok=True)
