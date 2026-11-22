# Mental Health First Aid Training and Recognition of Depression at Six Months or Later: A Systematic Review and Random-Effects Meta-Analysis of Randomised Controlled Trials

## Abstract

## Abstract

**Background:** Mental Health First Aid (MHFA) training is intended to improve trainees’ ability to recognise mental health problems and respond appropriately. This review evaluated whether MHFA improves correct recognition of depression in a case vignette at the first follow-up occurring at least six months after training.

**Methods:** Eligible studies were randomised controlled trials comparing a recognised MHFA programme with a waiting-list, no-training, or unrelated-activity control. The outcome was the proportion correctly identifying a depression vignette as depression or an equivalent diagnostic label. One effect was selected per trial. The prespecified effect measure was the odds ratio (OR), with correct recognition as the counted event. Trial log ORs were synthesised using a random-effects restricted maximum-likelihood (REML) model. The supplied pipeline identified five studies, of which three contributed effect estimates.

**Results:** Three comparisons involving 894 trainees were pooled. Their log ORs were 1.068054 (95% CI 0.847 to 1.290; n=358), 0.162898 (95% CI −0.097 to 0.423; n=262), and 0.278652 (95% CI 0.041 to 0.517; n=274). The pooled **Odds Ratio (OR)** was 2.686355171384576 (95% CI 0.934 to 7.728; p=0.06680353244215156). The supplied result classified favourability as “neither (essentially a tie, or a ratio measure where favourability depends on which event was counted).” Statistical heterogeneity was considerable (I²=87.84%; τ²=0.732595; Q=19.702, p=0.0001). Egger’s intercept was 5.9837 (p=0.0551); trim-and-fill imputed no studies (k₀=0). Publication-bias risk was rated moderate.

**Conclusions:** The pooled point estimate was above the null OR of 1, but its confidence interval included 1 and the test of the pooled effect was not statistically significant. Considerable between-study heterogeneity, only three analysable comparisons, incomplete reporting of screening and trial characteristics, and limited power to evaluate small-study effects substantially reduce certainty. The available results do not establish a reliable long-term effect of MHFA on correct depression recognition.

# Introduction

Mental Health First Aid (MHFA) programmes train members of the public and other non-specialists to recognise possible mental health problems, offer initial support, and encourage appropriate professional help. Correct identification of depression is a proximal competency that may plausibly influence subsequent helping responses. Immediate post-training improvements, however, do not necessarily demonstrate durable knowledge. The clinically and educationally relevant question addressed here was therefore whether any recognition advantage persists at the first assessment conducted at least six months after training.

The review question was: among trainees in randomised controlled trials, what is the effect of MHFA training, compared with a waiting-list, no-training, or unrelated-activity control, on correct recognition of depression in a case vignette at the first follow-up occurring at least six months after training?

The eligible intervention encompassed face-to-face, e-learning, and other recognised MHFA delivery variants. The outcome was narrowly defined as the proportion of trainees identifying a vignette depicting depression as depression or an equivalent diagnostic label, such as major depression. Open-ended and closed-choice recognition items were eligible. General mental-health knowledge, recognition of other disorders, treatment beliefs, stigma, helping confidence or behaviour, and outcomes among recipients of help were outside the outcome definition.

# Search/Screening

The supplied analysis pipeline recorded five studies and three analysable effect sizes. No bibliographic database list, search dates, full search strings, language restrictions, deduplication counts, title/abstract screening counts, full-text exclusion reasons, protocol registration, or reviewer procedures were provided. Consequently, a complete PRISMA flow diagram and a reproducible account of the search cannot be reconstructed from the available results.

Eligibility was defined by the following PICOS elements:

- **Population:** trainees participating in randomised controlled trials;
- **Intervention:** recognised MHFA training, including face-to-face, e-learning, and other delivery variants;
- **Comparator:** waiting list, no training, or an unrelated control activity;
- **Outcome:** correct recognition of a depression vignette as depression or an equivalent diagnosis;
- **Timing:** the first available follow-up at or after six months; and
- **Design:** randomised controlled trial.

One eligible comparison was to be retained per trial to avoid statistical double-counting. Of five studies recorded by the pipeline, three contributed to the quantitative synthesis. The available information does not identify why the other two studies did not contribute effect estimates—for example, whether they lacked an eligible time point, did not report usable outcome data, or were otherwise ineligible for pooling.

# Included Studies

The three pooled comparisons were represented by anonymised labels `study_1_R1`, `study_3_R3`, and `study_4_R4`. Their sample sizes were 358, 262, and 274, respectively, giving a pooled total of 894 participants. No study names, publication years, countries, recruitment settings, trainee characteristics, intervention formats or durations, control conditions, attrition rates, item formats, or risk-of-bias assessments were supplied. These omissions prevent a detailed clinical and methodological comparison of the trials.

The individual samples and analysis inputs were:

| Comparison | Total n | Log OR | 95% CI on log-OR scale | OR derived from point estimate |
|---|---:|---:|---:|---:|
| `study_1_R1` | 358 | 1.068054 | 0.847 to 1.290 | 2.909711 |
| `study_3_R3` | 262 | 0.162898 | −0.097 to 0.423 | 1.176917 |
| `study_4_R4` | 274 | 0.278652 | 0.041 to 0.517 | 1.321307 |

The source data labelled these individual values as `hedges_g`, but that label conflicts with the explicitly requested binary effect measure and the native OR pooling documented in the meta-analysis output. They are therefore reported here as log ORs rather than as Hedges’ g. This interpretation is also numerically coherent with the reported pooled OR. The exponentiated study-level estimates shown above are derived values and not separately supplied event-count estimates.

# Effect Sizes

For each trial, the intended effect was

\[
\log(OR)=\log\left(\frac{p_{MHFA}/(1-p_{MHFA})}{p_C/(1-p_C)}\right),
\]

where the event was correct recognition of depression. Under the protocol’s stated direction, a positive log OR (OR>1) denotes greater odds of correct recognition following MHFA. The meta-analysis metadata confirms that the **Odds Ratio (OR)** was used on its native scale (`native_pooling_used=true`) and that the effect measure came from the explicit user request.

The three log ORs were 1.068054, 0.162898, and 0.278652. Their supplied 95% confidence intervals were 0.847 to 1.290, −0.097 to 0.423, and 0.041 to 0.517, respectively. Approximate standard errors derived from the widths of these rounded intervals are 0.113010, 0.132653, and 0.121429. Because the confidence-limit inputs were rounded, these standard errors should not be treated as more precise than the source intervals.

The trial estimates varied appreciably. `study_1_R1` had a much larger point estimate than the other two comparisons. The confidence interval for `study_3_R3` crossed the log-OR null of zero, whereas those for `study_1_R1` and `study_4_R4` did not. These are study-specific findings and should not substitute for the prespecified random-effects synthesis.

The forest plot is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The effect-distribution plot is at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

# Meta-Analytic Result(s)

A random-effects model fitted using restricted maximum likelihood (REML) pooled three comparisons and 894 participants. The pooled **Odds Ratio (OR)** was **2.686355171384576** (95% CI **0.934 to 7.728**; p=**0.06680353244215156**).

The point estimate was above the null OR of 1, but the confidence interval included 1 and the pooled-effect test did not meet a conventional two-sided 0.05 significance threshold. The interval was wide, ranging from a value slightly below the null to a potentially large association.

The result metadata assigned the `favors` classification: **“neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)”**. This classification is reported verbatim as required. Separately, the outcome definition confirms that the event entered into the ratio was correct depression recognition; readers should retain that coding information when interpreting the OR.

A cumulative meta-analysis plot was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. Numerical cumulative estimates and the ordering rule used in that plot were not provided, so no additional quantitative conclusions are drawn from it.

# Heterogeneity

Between-study inconsistency was considerable:

- **I²:** 87.84%;
- **τ²:** 0.732595 on the log-OR scale;
- **Cochran’s Q:** 19.702;
- **Q-test p value:** 0.0001; and
- **Number of comparisons:** 3.

The Q test indicates that the observed dispersion was unlikely to reflect sampling error alone under a common-effect assumption. I² suggests that a large proportion of observed variation was attributable to between-study heterogeneity rather than within-study sampling variation. The τ² estimate is also substantial relative to the study-level log ORs. Nevertheless, all heterogeneity statistics are imprecise when based on only three studies; τ² in particular can be unstable with such a small evidence base.

Potential sources include differences in MHFA delivery format, participant populations, control conditions, follow-up duration beyond the six-month threshold, vignette wording, open-ended versus closed-choice response formats, baseline recognition, attrition, and analytic handling of missing data. None could be tested with the information supplied.

The heterogeneity summary figure is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

# Moderators

No trial-level moderator variables or meta-regression coefficients were provided. Therefore, no valid subgroup analysis or meta-regression could be conducted for delivery format, control type, response format, follow-up time, trainee group, or other study characteristics. Moreover, with only three pooled comparisons, moderator analyses would be severely underpowered and at high risk of spurious findings even if covariates were available.

A bubble chart was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`, but the moderator represented, its coding, regression estimate, confidence interval, and p value were not supplied. The figure should therefore be regarded as descriptive only and cannot support a claim of effect modification.

# Publication Bias

Egger’s regression produced an intercept of **5.9837** with p=**0.0551**. This was borderline but did not cross the conventional 0.05 threshold. The result may suggest small-study effects, but it does not provide conclusive evidence of funnel-plot asymmetry.

Trim-and-fill estimated **k₀=0**, meaning that no missing studies were imputed. The pipeline also supplied a trim-and-fill value of **0.506**, although its scale and relationship to the native OR analysis were not documented. It is therefore not interpreted as an adjusted OR. Overall publication-bias risk was rated **moderate**.

These analyses have major limitations. Asymmetry tests are generally not recommended for firm inference with so few studies because statistical power is extremely low and regression results can be unstable. Trim-and-fill also performs poorly when the number of studies is small or heterogeneity is substantial. Here, k=3 and I²=87.84%; consequently, neither the non-significant Egger test nor k₀=0 should be interpreted as evidence that reporting bias is absent.

# Discussion

This synthesis addressed a focused, longer-term outcome: correct identification of depression at the first follow-up conducted at least six months after MHFA training. Across three randomised comparisons involving 894 trainees, the REML pooled OR was 2.686355171384576. However, the 95% confidence interval was 0.934 to 7.728, and the pooled p value was 0.06680353244215156. Thus, the available analysis did not establish a statistically reliable difference at the conventional 0.05 level.

Interpretation should focus on both uncertainty and inconsistency rather than on the point estimate alone. The confidence interval permits effects ranging from slightly below the null to a large increase in the odds of correct recognition. Meanwhile, I²=87.84%, τ²=0.732595, and Q=19.702 (p=0.0001) show marked dispersion. The largest comparison-specific log OR, 1.068054, was substantially greater than the other two estimates, 0.162898 and 0.278652. Such variation raises the possibility that intervention implementation, participant context, measurement format, or trial conduct materially affects long-term recognition outcomes.

The analysis is directly aligned with the prespecified binary outcome and uses an appropriate odds-ratio metric. It also limits multiplicity by selecting one effect per trial and targets the first follow-up at or beyond six months. These design choices improve interpretability relative to combining different disorders, knowledge domains, or repeated time points.

Nevertheless, statistical non-significance should not be equated with proof of no effect. The wide confidence interval indicates limited precision, while substantial heterogeneity means that a single average may not adequately characterise every setting. Conversely, the point estimate should not be presented as definitive evidence of benefit because the interval crosses the null, results differ markedly across trials, and only three comparisons were available.

No risk-of-bias assessments were supplied, so confidence in randomisation, allocation concealment, missing-outcome handling, selective reporting, and outcome measurement cannot be evaluated. Recognition outcomes are also susceptible to measurement differences: closed-choice questions may cue an answer, whereas open-ended questions may impose a more stringent threshold. The absence of study-level details prevents assessment of whether such differences explain the observed heterogeneity.

Publication-bias diagnostics do not resolve this uncertainty. Egger’s p value of 0.0551 is borderline, but k=3 is far below the number generally considered adequate for dependable asymmetry testing. The moderate risk rating and the possibility of small-study effects warrant cautious interpretation despite trim-and-fill imputing no studies.

# Limitations

1. **Incomplete search and screening documentation:** Search sources, dates, terms, screening counts, exclusion reasons, and reviewer procedures were unavailable, preventing full verification of PRISMA compliance and review reproducibility.
2. **Few analysable trials:** Although five studies were recorded, only three supplied effect estimates. The reasons the other two did not enter the synthesis were not reported.
3. **Limited study information:** Bibliographic details, participant characteristics, settings, intervention formats, control activities, follow-up times, attrition, and response formats were unavailable.
4. **No trial risk-of-bias assessment:** The internal validity of the included comparisons could not be judged.
5. **Considerable heterogeneity:** I² was 87.84%, and the heterogeneity test was statistically significant. This limits the adequacy of a single pooled estimate.
6. **Imprecise pooled effect:** The 95% CI of 0.934 to 7.728 was wide and crossed the null.
7. **No moderator analysis:** Potential explanations for heterogeneity could not be tested, and k=3 would make such analyses unreliable.
8. **Underpowered reporting-bias diagnostics:** Egger’s test and trim-and-fill are not dependable with only three comparisons, particularly in the presence of substantial heterogeneity.
9. **Source-field inconsistency:** Individual effects were stored under a field named `hedges_g`, although the requested and pooled native measure was the OR. The individual numbers were treated as log ORs because that interpretation matches the explicit effect-measure specification and native pooling metadata.
10. **Undocumented trim-and-fill scale:** The supplied trim-and-fill value of 0.506 lacked a confirmed scale and was not interpreted as a native-scale adjusted OR.
11. **No certainty-of-evidence assessment:** The information required for a formal GRADE assessment was not supplied.

# Conclusion

Three randomised comparisons involving 894 trainees contributed to the quantitative synthesis of correct depression recognition at the first follow-up occurring at least six months after MHFA training. The REML pooled **Odds Ratio (OR)** was **2.686355171384576** (95% CI **0.934 to 7.728**; p=**0.06680353244215156**), with the supplied favourability classification of **neither**. Heterogeneity was considerable (I²=87.84%; τ²=0.732595; Q=19.702, p=0.0001).

Accordingly, the current evidence does not establish a precise or statistically reliable long-term effect of MHFA on correct depression recognition. Better-reported randomised trials, consistent binary outcome definitions, transparent event counts, prespecified longer-term follow-up, and enough studies to examine effect modifiers are needed.

# References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71.
2. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA, eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315:629-634. doi:10.1136/bmj.315.7109.629.
4. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56:455-463. doi:10.1111/j.0006-341X.2000.00455.x.
5. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1-48. doi:10.18637/jss.v036.i03.

*Individual trial reports could not be listed because bibliographic citations were not included in the supplied context data.*

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| correct recognition of depression in a case vignette | 3 | Odds Ratio (OR) | Yes | 2.6864 [0.9338, 7.7278] |
