# Cochrane benchmark

AutoSynthesis was run on **100 Cochrane intervention reviews** across 26 clinical topics. Each review was run with three LLM backbones: GPT-5.6 Sol, Gemini 3.8 Flash, and Claude Opus 5. For each review, one meta-analysis (one comparison and one outcome) was selected, and the pooled result of AutoSynthesis is compared with the one reported by Cochrane.

```bash
pip install -r requirements.txt
bash reproduce.sh          # about one minute, no API key needed
```

## Folder layout

```
benchmark/
├── data/              inputs: Cochrane values, AutoSynthesis values, review list and prompts
├── runs/              AutoSynthesis outputs per review and model (study-level data)
├── scripts/           analysis and figure scripts
├── figures/           generated figures (PDF)
└── results/           generated tables
```

## Data

| File | Content |
|---|---|
| `data/reviews.csv` | The 100 reviews: Cochrane ID, title, Cochrane topic, subfield, publication years, and the **prompt** given to AutoSynthesis |
| `data/cochrane_ground_truth.csv` | Pooled result reported by Cochrane for the selected meta-analysis: effect measure, effect, 95% CI, k, N, p-value, I² |
| `data/autosynthesis_{gpt,gemini,claude}.csv` | The same fields as produced by AutoSynthesis with each backbone |
| `data/repooled_results.csv` | Rows re-pooled from the run's own study-level data (see [Harmonization](#harmonization)); made by `scripts/repool_from_runs.py` |
| `data/search_overlap_<model>.csv` | Per review: papers found by the search agent, Cochrane's included studies, and the overlap (GPT and Gemini) |
| `data/prisma_counts.json` | Papers per pipeline stage (in pipeline, document type, extraction, effect size), from each run's `paper_tracking.csv` |

`runs/<review>/<model>/` contains the saved outputs of each run:

| File | Content |
|---|---|
| `plan.json` | Structured plan made from the prompt (outcome, comparison, effect measure, criteria) |
| `paper_tracking.csv`, `study_screening.csv` | Every paper and the reason it was kept or excluded |
| `meta_ready_results.json` | Extracted statistics per study (means, SDs, counts, reported effects) with the source text |
| `effect_sizes.json` | Per-study effect size and variance, with the raw inputs used to compute them |
| `meta_analysis_result.json` | Pooled estimate, CI, k, heterogeneity, publication-bias tests |
| `rob_assessments.json` | Risk-of-bias judgments per study and domain (RoB 2 / ROBINS-I), with rationale and quotes |
| `meta_analysis_report.md` | The final report |
| `search_agent/` | Search queries and search summary (records found, time) |

The full texts of the included papers are not distributed (copyright). `runs/CD011044_rerun/` is a rerun of one review whose original run saved no study-level data (same prompt and PDFs).

## Comparison with Cochrane

**Harmonization.** Each AutoSynthesis result is compared with Cochrane on Cochrane's effect measure:

* RR, OR and HR are compared on the log scale.
* SMD and log OR are converted with the Chinn (2000) formula, ln OR = SMD · π/√3.
* When the two analyses use a mean difference and a standardized mean difference, the run's own study-level data are re-pooled in Cochrane's measure (DerSimonian–Laird random effects, as in RevMan).

Nothing is re-extracted: the inputs come from `effect_sizes.json` and `meta_ready_results.json`. The column `conversion` in `results/benchmark_audit_per_review.csv` records what was done for each row.

**Metrics.**

| Metric | Reviews | Definition |
|---|---|---|
| Absolute agreement | 76 reviews with a standardized measure (SMD, RR, OR, HR) | \|Δ\| = \|θ_AutoSynthesis − θ_Cochrane\| on the null-at-0 scale (log for ratios); share within ±0.05 (strict) and ±0.20 (broad), with Wilson 95% CIs |
| Unit-free agreement | all 100 reviews | \|Δ\| divided by the width of Cochrane's 95% CI |
| Correlation | 76 reviews | Pearson r between AutoSynthesis and Cochrane effects |
| Conclusion | all 100 reviews | Same direction and same statistical significance as Cochrane |

## Scripts and figures

| Script | Output |
|---|---|
| `benchmark_metrics.py` | `results/benchmark_audit_per_review.csv`, `results/benchmark_summary.json` |
| `repool_from_runs.py` | `data/repooled_results.csv` |
| `generate_tolerance_bars.py` | `effect_tolerance_bars.pdf` |
| `generate_double_whisker.py` | `effect_double_whisker*.pdf` |
| `generate_paper_style_figures.py` | `paper_fig2_*.pdf`, `paper_figS12_agreement.pdf` |
| `generate_unitfree_figures.py`, `generate_topic_breakdown.py` | `unitfree_*.pdf`, `topic_breakdown_*.pdf` |
| `generate_funnel_flow.py` | `funnel_flow_gpt.pdf` |
| `generate_venn_search.py` | `venn_search_vs_truth_gpt.pdf` |
| `audit_statistics.py` | Optional independent check: recomputes each study's effect from the raw inputs and re-pools with R `metafor` (REML and DL). Needs `rpy2` and R. |

Shared helpers: `paths.py` (folder layout), `bench_load.py` (reads the CSVs), `tol_data.py` and `rel_data.py` (per-review comparison tables).
