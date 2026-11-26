# Tutorial

This tutorial goes from the quickest check to running a full meta-analysis. Parts 1–3 need no API key and make no LLM calls.

| Part | What you do | Time | Needs |
|---|---|---|---|
| [1](#1-reproduce-the-benchmark) | Reproduce the benchmark numbers and figures | ~1 min | Python |
| [2](#2-inspect-one-review-step-by-step) | Follow one review from the prompt to the pooled estimate, and re-pool it yourself | ~10 min | Python |
| [3](#3-open-the-web-app-with-the-demo) | Start the web app and browse the paper's three case studies | ~15 min (first build) | Docker |
| [4](#4-run-your-own-meta-analysis) | Run a new meta-analysis | 30–120 min | Docker, OpenRouter API key |

```bash
git clone https://github.com/MoeinDSP/AutoSynthesis.git
cd AutoSynthesis
```

---

## 1. Reproduce the benchmark

```bash
pip install -r benchmark/requirements.txt
bash benchmark/reproduce.sh
```

Expected output:

```
1/2  Benchmark metrics ...
2/2  Figures ...
Done. Figures in benchmark/figures/, tables in benchmark/results/.
```

What you get:

* `benchmark/results/benchmark_audit_per_review.csv`: one row per review and model, with Cochrane's pooled result, AutoSynthesis' pooled result, and whether they agree (direction, significance, CI overlap).
* `benchmark/results/benchmark_summary.json`: the counts behind the agreement numbers in the paper.
* `benchmark/figures/*.pdf`: the benchmark figures. [`README.md`](README.md#list-of-figures-and-programs) shows which script makes each one.

> **Tip.** For figures that look exactly like the paper's, install the *Liberation Sans* font (`apt install fonts-liberation`). Without it, matplotlib uses DejaVu Sans and prints a `findfont` warning. The numbers are the same.

---

## 2. Inspect one review step by step

We use **CD007044** (Cochrane review, outcome measured as a risk ratio) and the GPT run. Every run folder in `benchmark/runs/<review>/<model>/` has the same files.

**The prompt** given to AutoSynthesis is in `benchmark/data/reviews.csv`:

```bash
grep CD007044 benchmark/data/reviews.csv
```

**The plan** that the planning agent made from the prompt (outcome, comparison, effect measure, inclusion criteria):

```bash
python -m json.tool benchmark/runs/CD007044/gpt-5.6-sol/plan.json | head -30
```

**Which papers were kept, and why the others were excluded:**

```bash
column -s, -t < benchmark/runs/CD007044/gpt-5.6-sol/paper_tracking.csv | less -S
```

**The extracted data.** For each study, `meta_ready_results.json` holds the numbers taken from the paper together with the source text. `effect_sizes.json` holds the inputs used for the effect size:

```bash
python -c "import json; [print(s['study_id'], s['raw_measure_inputs']) for s in json.load(open('benchmark/runs/CD007044/gpt-5.6-sol/effect_sizes.json'))]"
```

**Re-pool it yourself.** Save this as `repool.py` in the repository root and run `python repool.py`:

```python
import json, math

studies = json.load(open("benchmark/runs/CD007044/gpt-5.6-sol/effect_sizes.json"))
y, v = [], []
for s in studies:
    x = s["raw_measure_inputs"]                      # events and sample sizes per arm, as extracted
    a, c, n1, n2 = x["events_treatment"], x["events_control"], x["n_treatment"], x["n_control"]
    y.append(math.log((a / n1) / (c / n2)))          # log risk ratio
    v.append(1 / a - 1 / n1 + 1 / c - 1 / n2)        # its variance

# DerSimonian-Laird random-effects pooling
w = [1 / vi for vi in v]
fixed = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
q = sum(wi * (yi - fixed) ** 2 for wi, yi in zip(w, y))
tau2 = max(0.0, (q - (len(y) - 1)) / (sum(w) - sum(wi ** 2 for wi in w) / sum(w)))
w = [1 / (vi + tau2) for vi in v]
est, se = sum(wi * yi for wi, yi in zip(w, y)) / sum(w), (1 / sum(w)) ** 0.5
print(f"RR {math.exp(est):.3f} [{math.exp(est - 1.96 * se):.3f}, {math.exp(est + 1.96 * se):.3f}], k = {len(y)}")
```

```
RR 0.871 [0.786, 0.964], k = 10
```

Compare this with:

* **AutoSynthesis**, in `meta_analysis_result.json`: RR 0.871 [0.787, 0.963] (REML, computed with R `metafor`)
* **Cochrane**, in `benchmark/data/cochrane_ground_truth.csv`: RR 0.85 [0.78, 0.93], k = 13

The small difference between your result and AutoSynthesis' comes from the estimator: DerSimonian–Laird here, REML in the pipeline. AutoSynthesis found 10 of Cochrane's 13 studies, which explains most of the difference to Cochrane.

`benchmark/scripts/audit_statistics.py` runs this check for ten reviews with R `metafor`. It needs `rpy2` and R.

---

## 3. Open the web app with the demo

```bash
cd app
cp .env.example .env           # set POSTGRES_PASSWORD and SESSION_SECRET to any value
docker compose up --build -d
docker compose --profile tools run --rm db-migrate    # first start only
```

Open <http://localhost:8000> and click **Demo**. It loads the paper's three case studies: semaglutide, tirzepatide and intermittent fasting for weight loss. You can browse them like a finished run: the PRISMA diagram, the forest and funnel plots, risk of bias and the report. No LLM is called.

To stop the app: `docker compose down`.

---

## 4. Run your own meta-analysis

1. Add your OpenRouter key to `app/.env` (`OPENROUTER_API_KEY=...`) and restart: `docker compose up -d`.
2. In the web app, choose the model and write a focused question. Name the population, intervention, comparison and one outcome, and if you want, the effect measure. For example (`case_studies/CD016018/prompt.txt`):

   > In adults living with obesity, what is the effect of tirzepatide compared with placebo on percentage body weight change from baseline? Pool as a mean difference using a random-effects model. Evaluate ONLY percentage body weight change.

3. Optionally choose the **Pooling model** (fixed effect, a random-effects estimator, or UWLS). If you leave it on *Automatic*, AutoSynthesis uses the model named in your question, or random effects with REML.
4. Choose a mode:
   * **Manual mode**: upload the PDFs of the studies you want to include. This is how the benchmark was run.
   * **Search mode**: AutoSynthesis searches the sources listed in `ENABLED_SEARCH_DATABASES` in `.env`. The template enables a web deep-research search, PubMed, Semantic Scholar, arXiv and OSF; Scopus and Web of Science also need their API keys. It then screens the records and retrieves the open-access full texts.
5. The run pauses at **review gates**:
   * after the search, so you can drop found papers or add your own PDFs (search mode only);
   * if some full texts could not be downloaded, so you can upload those PDFs or continue without them;
   * after the full-text eligibility check, so you can review the included papers before the extraction and analysis.

   At each gate, check the papers, then click **Continue**.
6. When the run finishes, the results page shows the pooled estimate and all figures. Every file (the report, `effect_sizes.json`, the figures) can be downloaded, and is also saved in `app/outputs/`.

A run with about 10–15 studies takes roughly 30–60 minutes in manual mode. Search mode takes longer. The cost depends on the model and on the number of papers.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `findfont: Font family 'Liberation Sans' not found` | Only a warning. Install `fonts-liberation` for identical figure fonts. |
| `POSTGRES_PASSWORD must be set in .env` | Set any value in `app/.env`. |
| The app starts but runs fail at the first step | Check `OPENROUTER_API_KEY` in `app/.env` and the credit on your OpenRouter account. |
| `ImportError` from `rpy2` outside Docker | Install R (≥ 4.3) and the `metafor` package, or use Docker. |
