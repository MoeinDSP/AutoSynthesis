"""Time and cost of the fully automatic runs (search -> screening -> full text -> analysis, no human input).
Input: fully_automatic/<model>/time_and_cost.csv. Prints per-model averages, ranges and totals."""
import csv, os
from paths import BENCH

for model in sorted(os.listdir(os.path.join(BENCH, "fully_automatic"))):
    p = os.path.join(BENCH, "fully_automatic", model, "time_and_cost.csv")
    if not os.path.exists(p):
        continue
    rows = [r for r in csv.DictReader(open(p)) if r["status"] == "completed"]
    t = [float(r["wall_clock_min"]) for r in rows]
    c = [float(r["openrouter_cost_usd"]) for r in rows if r["openrouter_cost_usd"]]
    pooled = sum(1 for r in rows if r["pooled_effect"] not in ("", "None"))
    print(f"{model}: {len(rows)} runs, {pooled} with a pooled estimate | time {sum(t)/len(t):.0f} min (range {min(t):.0f}-{max(t):.0f}) "
          f"| cost ${sum(c)/len(c):.2f} per review, ${sum(c):.2f} total")
