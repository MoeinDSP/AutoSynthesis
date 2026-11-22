# Case studies

The three example meta-analyses shown in the paper, each based on a recent Cochrane review. They were run with GPT-5.6 Sol. The same results load in the web app with the **Demo** button, without any API calls.

| Review | Question | Effect measure | Studies pooled | AutoSynthesis result [95% CI] |
|---|---|---|---|---|
| [CD015092](CD015092) | Semaglutide vs placebo in adults living with obesity: % body weight change | MD | 11 | −10.41 [−11.98, −8.84] |
| [CD016018](CD016018) | Tirzepatide vs placebo in adults living with obesity: % body weight change | MD | 9 | −16.72 [−19.05, −14.38] |
| [CD015610](CD015610) | Intermittent fasting vs regular dietary advice in adults with overweight or obesity: % body weight change | MD | 14 | 0.09 [−0.64, 0.82] |

Each folder contains:

* `prompt.txt`: the prompt given to AutoSynthesis
* `figures/`: forest plot, funnel plot, cumulative meta-analysis, heterogeneity summary, effect distribution, bubble chart, PRISMA flow diagram and risk-of-bias traffic-light plot (PDF)
* `meta_analysis_report.md`: the full report
* `meta_analysis_result.json`, `effect_sizes.json`, `meta_ready_results.json`, `rob_assessments.json`, `moderator_results.json`, `prisma_flowchart.json`, `plan.json`, `paper_tracking.csv`: the outputs behind the figures and the report
