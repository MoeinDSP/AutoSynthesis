# Atorvastatin versus Placebo or No Treatment and Withdrawal Due to Adverse Effects in Adults: A Systematic Review and Meta-Analysis of Randomized Controlled Trials

## Abstract

**Background.** Statins are among the most widely prescribed drugs worldwide, and concerns about tolerability — myalgia, transaminase elevation, and gastrointestinal complaints — are a principal driver of non-adherence and discontinuation. Withdrawal from a randomized trial because of adverse effects is a pragmatic, patient-relevant composite index of drug tolerability. We synthesised randomized evidence comparing atorvastatin with placebo or no treatment for this outcome in adults.

**Methods.** A systematic search and screening pipeline identified randomized controlled trials of atorvastatin versus placebo or no treatment in adults that reported the number of randomized participants in each arm who discontinued the assigned drug or dropped out because of adverse events, intolerance, or side effects. Event counts per arm were extracted and pooled as an odds ratio (OR) using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Cochran's Q, I², and τ². An OR below 1 denotes fewer adverse-effect withdrawals with atorvastatin (better tolerability); an OR above 1 denotes more.

**Results.** Six records met the review's inclusion criteria at the study level, of which two contributed extractable arm-level withdrawal event counts and entered the quantitative synthesis (k = 2; N = 118 randomized participants). The pooled odds ratio was 0.974 (95% CI 0.132 to 7.193; p = 0.9797). Per the pre-specified direction field, this result favours *neither* arm — it is essentially a tie, and because the measure is a ratio of event counts, no direction of benefit or harm can be established. Statistical heterogeneity was nil (Q = 0.001 on 1 df, p = 0.9799; I² = 0.0%; τ² = 0.0000), but with only two studies these dispersion statistics are extremely imprecise and must not be read as positive evidence of consistency. Publication bias could not be assessed: funnel-plot asymmetry tests and regression-based small-study diagnostics are uninterpretable at k = 2. The effect measure was the odds ratio as explicitly requested, and native binary-outcome pooling was used (native_pooling_used = true), so the pooled value is a confirmed native-scale result rather than a standardized conversion.

**Conclusions.** The randomized evidence on atorvastatin-related withdrawal due to adverse effects, as captured by this synthesis, is too sparse and too imprecise to support any conclusion. The point estimate sits almost exactly on the line of no effect, but the 95% confidence interval (0.132 to 7.193) is compatible with both a nearly eight-fold reduction and a more than seven-fold increase in tolerability-related discontinuation. The certainty of the evidence should be downgraded severely for imprecision, and this analysis should be regarded as uninformative rather than as demonstrating equivalence.


## 1. Introduction

Hydroxymethylglutaryl-CoA reductase inhibitors ("statins") are a cornerstone of lipid-lowering therapy for both primary and secondary prevention of atherosclerotic cardiovascular disease. Atorvastatin, a synthetic, lipophilic, long-half-life statin, is one of the most frequently dispensed medicines in the world and is used across a very broad range of baseline risk, from high-risk secondary prevention to primary prevention in people with modest dyslipidaemia.

Because statins are taken indefinitely by largely asymptomatic people, tolerability matters as much as efficacy. Discontinuation rates in routine practice are substantially higher than in clinical trials, and patient-reported muscle symptoms, gastrointestinal complaints, and biochemical abnormalities such as alanine aminotransferase elevation are commonly cited reasons for stopping. Yet the relationship between statin exposure and *attributable* intolerance remains contested: n-of-1 and blinded re-challenge designs (e.g. the SAMSON and StatinWISE paradigms) suggest that a large fraction of symptoms reported on statins also occur on placebo, implying a substantial nocebo component.

Against this background, the number of randomized participants who withdraw from a trial *because of* adverse effects is an attractive composite endpoint. It is pragmatic, it is captured in blinded conditions where attribution bias is at least partly controlled, and it integrates both the frequency and the clinical severity of adverse experiences: a symptom that does not lead to discontinuation is, by definition, tolerated. It is, however, a comparatively rare event, which makes it statistically demanding — a point that proves central to the present analysis.

### 1.1 Objective

To estimate the effect of atorvastatin, compared with placebo or no treatment, on withdrawal (discontinuation) from randomized studies due to adverse effects or adverse events in adults.

### 1.2 Pre-specified direction of effect

The outcome is harmful in nature (an unwanted event), and it was extracted as event counts per arm and pooled as an odds ratio. Accordingly:

- An odds ratio **below 1.0** indicates **fewer** adverse-effect-related withdrawals with atorvastatin — i.e. atorvastatin is better tolerated than placebo or no treatment (a "positive effect" in the terms of the research question).
- An odds ratio **above 1.0** indicates **more** adverse-effect-related withdrawals with atorvastatin — i.e. a tolerability disadvantage.
- An odds ratio at or very near 1.0, particularly with a wide confidence interval, indicates that the data cannot distinguish between these possibilities.

Throughout this report, the arm favoured by the pooled estimate is reported using the analysis's own pre-specified `favors` field rather than being inferred from the sign or position of the point estimate.

---

## 2. Methods

### 2.1 Eligibility criteria

**Population.** Adults (≥18 years), any indication for which atorvastatin was administered.

**Intervention.** Atorvastatin at any dose, any duration, administered orally.

**Comparator.** Placebo or no treatment (including usual care without a lipid-lowering comparator drug). Active-comparator trials (atorvastatin versus another statin or another lipid-lowering agent) were not eligible for this comparison.

**Outcome.** Withdrawal (discontinuation) from the study due to adverse effects or adverse events — specifically, the number of randomized participants in each arm who stopped the assigned drug or dropped out because of adverse events, intolerance, or side effects, including but not limited to myalgia, liver enzyme (transaminase) elevation, and gastrointestinal complaints. The outcome had to be reported, or be reconstructible, as event counts per randomized arm so that a 2 × 2 table could be formed.

**Design.** Randomized controlled trials with a parallel-group or equivalent randomized allocation to atorvastatin versus placebo/no treatment.

### 2.2 Information sources and search

A structured systematic search and automated screening pipeline was used to retrieve candidate records and to classify each record by population, intervention, comparator, outcome, and design. Records were then assessed against the eligibility criteria above, and arm-level event counts for adverse-effect-related withdrawal were extracted for each eligible trial.

### 2.3 Data extraction

For each eligible trial, the following were extracted: the number of participants randomized to each arm, and the number in each arm who withdrew or discontinued because of adverse effects. These counts formed the 2 × 2 contingency table used for pooling. Where a trial reported withdrawals only in aggregate (all causes combined) without an adverse-effect-specific breakdown by arm, the trial could not contribute to the quantitative synthesis.

### 2.4 Effect measure and synthesis

The effect measure was the **odds ratio (OR)**, specified explicitly for this analysis (`effect_measure_source`: explicit user request; no conflict with the pipeline's own outcome classification was recorded). Pooling was performed on the **native binary-outcome scale** — that is, log odds ratios were computed directly from the arm-level event counts and combined, rather than being back-transformed from a standardized mean difference. The field `native_pooling_used` is **true** for this analysis, so the reported value is a confirmed native-scale odds ratio and **not** a standardized fallback.

Studies were combined in a **random-effects model** with between-study variance estimated by **restricted maximum likelihood (REML)**. Results are reported as the pooled OR with a 95% confidence interval and a two-sided p-value for the test of the null hypothesis OR = 1.

### 2.5 Assessment of heterogeneity

Between-study heterogeneity was quantified with Cochran's Q statistic and its p-value, the I² statistic (proportion of total variability attributable to between-study heterogeneity rather than sampling error), and τ² (the absolute between-study variance on the log-odds scale). These statistics were interpreted with explicit reference to the number of contributing studies, since all three are known to be severely under-powered and unstable when k is very small.

### 2.6 Assessment of reporting bias

Assessment of small-study effects and publication bias (funnel plot inspection, Egger's regression, trim-and-fill) was pre-specified as conditional on at least ten contributing studies, consistent with standard Cochrane guidance. Below that threshold, such tests have essentially no power to distinguish asymmetry from chance.

---

## 3. Search and Screening

The screening pipeline identified **six studies** that satisfied the review's study-level eligibility criteria for the atorvastatin versus placebo/no-treatment comparison in adults.

Of these six studies, **two** reported — or permitted reconstruction of — arm-level event counts for withdrawal due to adverse effects and therefore contributed to the quantitative synthesis of this outcome. The remaining four eligible studies did not supply an adverse-effect-specific, arm-level withdrawal count and so could not be entered into the 2 × 2 pooling; they are retained in the narrative inclusion set but contribute no weight to the pooled estimate. This is a common pattern for tolerability outcomes, which are frequently reported either as a single all-cause attrition figure, as a narrative statement that "no patient discontinued because of adverse events", or only as pooled totals across arms.

The quantitative dataset therefore comprises **k = 2 studies** with a combined **N = 118 randomized participants**.

---

## 4. Included Studies

Two studies contributed arm-level withdrawal event counts:

| Study identifier | Total N (both arms) | Standardized effect size (Hedges' g, for display only) | 95% CI (g scale) |
|---|---|---|---|
| study_4_R4 | 38 | 0.000 | −0.636 to 0.636 |
| study_6_R6 | 80 | −0.028 | −0.466 to 0.410 |
| **Total** | **118** | — | — |

Two points about this table require emphasis.

First, the per-study values displayed above are **standardized (Hedges' g) representations**, generated by the pipeline for cross-study display and plotting on a common axis. They are **not** the quantities that were pooled. The meta-analysis itself was carried out on the **native odds-ratio scale** using the extracted event counts. The g values should therefore be read only as a visual indication of effect magnitude and direction, not as the analytic result; no result in this report is a Hedges' g.

Second, both per-study estimates sit essentially on the null. study_4_R4 has a standardized effect of exactly 0.000, which for a binary outcome extracted as counts is the signature of either identical event proportions in the two arms or, more commonly for this endpoint, zero or near-zero adverse-effect withdrawals in both arms. study_6_R6 has a standardized effect of −0.028, again indistinguishable from zero. Neither individual trial's confidence interval excludes the null, and both are wide relative to the effect sizes typically of interest for a tolerability endpoint.

The small total sample (N = 118) means the synthesis is based on very few actual withdrawal events. For a rare binary outcome, the information content of a meta-analysis is governed by the **event count**, not the participant count, and a dataset of this size can realistically contain only a handful of events in total. This is the dominant determinant of the result reported below.

---

## 5. Effect Sizes

Arm-level event counts were converted to log odds ratios with their sampling variances and pooled. The individual study contributions and the pooled summary are displayed in the forest plot:

- **Forest plot:** `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`

The distribution of study-level effect estimates is shown in:

- **Effect distribution plot:** `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`

Both contributing studies produced effect estimates lying essentially on the line of no effect, with confidence intervals that overlap each other almost completely. There is no visible divergence between the two trials in either magnitude or direction.

The cumulative plot, which adds studies sequentially and re-pools, is provided for completeness:

- **Cumulative meta-analysis plot:** `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`

With only two studies, the cumulative display necessarily contains just two steps and should not be interpreted as evidence about the stability of the estimate over accumulating evidence; it simply shows that adding the second study did not move the point estimate away from the null.

A bubble chart relating study-level effect size to study size is available at:

- **Bubble chart:** `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`

With k = 2, this plot cannot support any inference about a size–effect relationship and is included only for transparency of the underlying data.

---

## 6. Meta-Analytic Results

### 6.1 Primary pooled estimate

**Outcome: Withdrawal due to adverse effects (atorvastatin vs placebo or no treatment)**

| Quantity | Value |
|---|---|
| Effect measure | **Odds Ratio (OR)** |
| Native-scale pooling used | **Yes** (confirmed native binary pooling) |
| Number of studies (k) | 2 |
| Total participants (N) | 118 |
| Model | Random effects, REML |
| **Pooled odds ratio** | **0.974** |
| 95% confidence interval | **0.132 to 7.193** |
| p-value | **0.9797** |
| Favours | **Neither arm** — essentially a tie; because this is a ratio measure of event counts, favourability depends on which event was counted, and no direction of benefit or harm can be determined |
| I² | 0.0% |
| τ² | 0.0000 |
| Cochran's Q | 0.001 (1 df), p = 0.9799 |

The pooled odds ratio for withdrawal due to adverse effects was **0.974 (95% CI 0.132 to 7.193; p = 0.9797)**. The point estimate is 2.6% below unity on the odds scale — a difference that is both clinically negligible and statistically indistinguishable from zero effect (p = 0.9797 is about as close to a perfect null as a two-sided test can produce).

In accordance with the analysis's pre-specified direction field, this result **favours neither atorvastatin nor placebo/no treatment**. It is essentially a tie. It must not be reported as "atorvastatin had slightly fewer withdrawals", because the displacement of the point estimate from 1.0 is trivially small relative to the uncertainty around it and carries no interpretive weight.

### 6.2 Precision and what the interval actually permits

The width of the confidence interval is the single most important feature of this result. On the odds scale, the interval spans from **0.132** to **7.193** — a ratio of upper to lower bound of approximately **54-fold**. On the log-odds scale the interval runs from about −2.03 to +1.97, implying a standard error of roughly 1.02 log-odds units. This is an exceptionally imprecise estimate.

Concretely, the data are equally compatible with:

- atorvastatin **reducing** the odds of adverse-effect withdrawal by about **87%** (OR 0.132), and
- atorvastatin **increasing** the odds of adverse-effect withdrawal by about **seven-fold** (OR 7.193).

Both extremes would, if true, be of major clinical consequence and would lead to opposite prescribing conclusions. An analysis whose confidence interval contains both of these scenarios does not constrain clinical belief in any useful way.

It is therefore essential to distinguish between two very different statements:

1. *"There is no evidence of a difference in adverse-effect withdrawal."* — This is supported.
2. *"There is evidence of no difference in adverse-effect withdrawal (i.e. equivalence)."* — This is **not** supported.

Demonstrating equivalence would require the confidence interval to lie wholly inside a pre-specified margin of clinical indifference. Here the interval exceeds any plausible such margin by a very large factor. The analysis is **uninformative**, not reassuring.

### 6.3 Why the estimate is so imprecise

Three factors compound:

1. **Very small k.** Only two studies contributed, so the random-effects model has one degree of freedom for heterogeneity and the pooled standard error is dominated by within-study sampling error from two sources.
2. **Small total sample.** N = 118 participants across both arms of both trials.
3. **Rare event.** Withdrawal specifically attributed to adverse effects is uncommon in short-to-medium-duration statin trials. With few events, the variance of the log odds ratio (approximately the sum of the reciprocals of the four cell counts) is very large. Where one or more cells approach zero, the variance inflates dramatically — and a study-level standardized effect of exactly 0.000, as seen in study_4_R4, is consistent with precisely this situation.

---

## 7. Heterogeneity

| Statistic | Value | Interpretation |
|---|---|---|
| Cochran's Q | 0.001 (df = 1) | Observed dispersion essentially identical to that expected by chance alone |
| Q p-value | 0.9799 | No statistical signal of between-study inconsistency |
| I² | 0.0% | Zero percent of observed variability attributed to between-study heterogeneity |
| τ² | 0.0000 | Estimated between-study variance of zero on the log-odds scale |

A heterogeneity summary graphic is provided at:

- **Heterogeneity summary:** `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

On their face, these statistics describe a perfectly homogeneous evidence base: Q (0.001) is smaller than its degrees of freedom (1), I² is pinned at its lower boundary of 0%, and REML has estimated the between-study variance as exactly zero, collapsing the random-effects model onto the fixed-effect solution.

**These values must not be over-interpreted.** With k = 2 studies there is a single degree of freedom for the Q test, and that test has almost no power to detect real heterogeneity. I² and τ² are correspondingly unstable: with two studies, τ² is routinely estimated at exactly zero by REML whenever the two observed effects do not happen to diverge, regardless of whether the underlying true effects differ. An I² of 0.0% here is best read as *"the two observed point estimates happen to coincide"*, not as *"atorvastatin's tolerability profile is consistent across populations, doses, and durations"*.

Furthermore, because both studies have point estimates sitting almost exactly on the null, apparent homogeneity is partly an artefact of both studies being uninformative in the same way. Two imprecise null results agree with each other trivially. Homogeneity among uninformative studies conveys no reassurance.

A prediction interval — the range within which the true effect in a new, exchangeable study would be expected to fall — is not reported, because with k = 2 and τ² estimated at zero such an interval would be spuriously narrow and would misrepresent the true state of knowledge.

---

## 8. Moderators and Subgroup Analyses

**No moderator, subgroup, or meta-regression analyses were performed, and none are interpretable with this dataset.**

Clinically meaningful moderators for statin tolerability would include atorvastatin dose (e.g. 10 mg vs 40–80 mg, given the well-described dose-dependence of muscle and hepatic adverse effects), treatment duration, baseline cardiovascular risk and indication, participant age, sex distribution, renal function, concomitant medications with cytochrome P450 3A4 interactions, comparator type (placebo versus open no-treatment, which affects nocebo-related discontinuation), and blinding status.

Each of these would require, at minimum, several studies per stratum to support even a crude subgroup comparison, and conventional guidance recommends roughly ten studies per covariate for meta-regression. With two contributing studies there are not enough degrees of freedom to fit any covariate, and any subgroup split would reduce each stratum to a single study — that is, to a narrative report of one trial rather than a meta-analysis.

The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) is presented as a data-transparency device only; the apparent relationship between sample size and effect size in a two-point scatter is not estimable.

One structural observation can be made without formal analysis: open-label or no-treatment comparators generally produce *more* discontinuation attributed to drug side effects in the active arm than blinded placebo comparators do, because unblinded participants attribute background symptoms to the drug they know they are taking. If the contributing trials differ in comparator type, this would be a plausible source of true heterogeneity that the present statistics are far too under-powered to detect.

---

## 9. Publication Bias and Small-Study Effects

**Publication bias could not be assessed.**

With k = 2 contributing studies, every standard diagnostic is inapplicable:

- **Funnel plot inspection** requires enough points to perceive asymmetry; two points define a line and convey nothing.
- **Egger's regression test** and related regression-based asymmetry tests cannot be fitted meaningfully with two observations and have essentially zero power below approximately ten studies.
- **Trim-and-fill** cannot impute missing studies from a two-study distribution.
- **Selection models** and **p-curve / p-uniform** approaches require far more studies and a non-degenerate distribution of p-values.

Accordingly, no statement — in either direction — can be made about whether small or unfavourable trials of atorvastatin tolerability are missing from this evidence base.

Two qualitative considerations nevertheless deserve recording, because they bear on how the sparse result should be read:

1. **Outcome reporting bias is a live concern for this endpoint.** Four of the six eligible studies did not report arm-level adverse-effect-specific withdrawal counts. Tolerability outcomes are notoriously selectively reported: trials in which discontinuation was unremarkable may omit the breakdown entirely, while trials in which it was notable may report it in detail — or the reverse, depending on sponsorship. The missingness here is therefore unlikely to be entirely at random, and the two studies that did report the outcome are not guaranteed to be representative of the six.

2. **The direction of any such bias is unknown.** Industry-sponsored trials have historically been argued to under-report statin adverse effects (through run-in periods that exclude intolerant participants before randomization, through narrow adverse-event definitions, and through per-protocol reporting), while post-marketing and media-influenced literature has been argued to over-attribute symptoms. Without more studies, neither tendency can be quantified.

---

## 10. Discussion

### 10.1 Principal finding

Pooling the two randomized trials that reported arm-level data yielded a pooled odds ratio for withdrawal due to adverse effects of **0.974 (95% CI 0.132 to 7.193; p = 0.9797)**, with nil statistical heterogeneity (I² = 0.0%, τ² = 0.0000, Q = 0.001, p = 0.9799). The result **favours neither arm** and is best characterised as a statistical tie with extremely wide uncertainty.

The headline message of this review is therefore not a finding about atorvastatin's tolerability. It is a finding about the **evidence base as captured by this synthesis**: it is too sparse, and the resulting estimate too imprecise, to inform clinical or regulatory judgement about adverse-effect-related discontinuation.

### 10.2 Interpretation in context

It is tempting to read a point estimate of 0.974 with a p-value of 0.98 as reassuring — as showing that atorvastatin is no worse tolerated than placebo. That reading is not justified by these data, for the reasons set out in Section 6.2: the confidence interval encompasses an 87% relative reduction at one end and a seven-fold relative increase at the other. A result this imprecise is consistent with almost any hypothesis about statin tolerability, including hypotheses that the clinical community actively debates.

That said, the direction-neutral finding here is not in conflict with the broader literature. Large blinded randomized trials and systematic reviews of statins have generally found that rates of discontinuation attributed to adverse effects are similar, or only marginally higher, on statin than on placebo, and blinded n-of-1 re-challenge studies have shown that a substantial share of statin-attributed symptoms also occur on placebo. The present analysis neither supports nor contradicts that body of work; it is simply far too small to contribute to it. Readers seeking an evidence-based estimate of statin tolerability should rely on the large-trial literature and on individual-participant-data syntheses rather than on this two-study pooled estimate.

### 10.3 Measurement considerations for this endpoint

"Withdrawal due to adverse effects" is a composite that depends heavily on reporting conventions:

- **Attribution** is investigator-determined and subjective. Whether a participant who stops because of myalgia is coded as an adverse-effect withdrawal, a protocol deviation, or a loss to follow-up varies across trials.
- **Severity threshold** varies. Some trials discontinue for any grade of transaminase elevation; others only above three times the upper limit of normal.
- **Run-in periods** systematically deflate observed intolerance. Trials that run all participants on active drug before randomization exclude intolerant individuals *before* the randomized phase, so the randomized comparison underestimates real-world discontinuation.
- **Blinding** modulates nocebo-driven discontinuation; no-treatment comparators are not equivalent to placebo for this outcome.
- **Duration** matters: muscle symptoms often emerge weeks to months into therapy, so short trials systematically under-count.

None of these can be addressed with two studies, but all of them limit the external validity of even a well-powered synthesis of this endpoint.

### 10.4 Statistical considerations for rare binary outcomes

Where adverse-effect withdrawals are rare, the odds ratio computed from sparse 2 × 2 tables is known to behave poorly: it is biased away from the null in small samples, its normal-approximation confidence interval is anti-conservative or, with continuity corrections, unstable, and zero-event arms require either correction factors or alternative methods. For future, larger versions of this synthesis, methods better suited to sparse data — the Peto odds ratio, the Mantel–Haenszel approach without continuity correction, beta-binomial models, or exact generalized linear mixed models — would be preferable to the inverse-variance random-effects approach used here. With k = 2 the choice of method is largely academic, since no method can rescue information that is not present in the data.

---

## 11. Data Quality and Validation Notes

No formal validation flags were attached to this analysis. The following factual observations about the dataset are nevertheless recorded plainly, because they materially affect interpretation:

- **Six studies** met study-level eligibility, but only **two (33%)** provided arm-level event counts for withdrawal due to adverse effects and entered the pooled analysis. The remaining four eligible studies contribute **zero weight** to the reported odds ratio. The pooled estimate therefore reflects a minority of the identified eligible evidence.
- The pooled analysis is based on **k = 2** studies and **N = 118** randomized participants. This is below any conventional threshold for a stable random-effects synthesis.
- The **effect measure is the odds ratio**, specified by explicit request (`effect_measure_source`: explicit_user_request). **No effect-measure conflict** was recorded against the pipeline's own outcome classification.
- **Native pooling was used** (`native_pooling_used`: true). The pooled value of 0.974 is a confirmed native-scale odds ratio derived from arm-level event counts. It is **not** a standardized fallback and is **not** a Hedges' g.
- The **per-study values reported in the effect-size table are standardized Hedges' g conversions provided for display and plotting only.** They are on a different scale from the pooled odds ratio and should not be compared numerically with it, nor cited as study-level odds ratios.
- **Heterogeneity statistics (I² = 0.0%, τ² = 0.0000, Q = 0.001) are reported as computed but are not reliable at k = 2** and should not be cited as evidence of consistency across trials.
- **Publication bias was not assessed** and could not be assessed at k = 2. Absence of a bias assessment is not evidence of absence of bias.
- **No subgroup or meta-regression analyses were performed**; none are estimable with two studies.

---

## 12. Limitations

1. **Severe imprecision.** The dominant limitation. A 95% confidence interval of 0.132 to 7.193 spans a 54-fold range and renders the estimate uninformative for any clinical purpose.
2. **Very small number of contributing studies (k = 2).** This precludes reliable estimation of between-study variance, prediction intervals, moderator effects, and small-study effects, and makes the random-effects model effectively indistinguishable from a fixed-effect model.
3. **Small total sample and rare event count (N = 118).** For a binary endpoint, statistical information scales with events, not participants; the event total here is necessarily very low, and one study's exactly-null standardized effect is consistent with near-zero events in one or both arms.
4. **Incomplete outcome availability among eligible studies.** Four of six eligible studies did not report arm-level adverse-effect withdrawal counts, raising the prospect of selective outcome reporting; the two reporting studies may not represent the six.
5. **Unassessable reporting bias.** No funnel-plot, regression, or selection-model diagnostics could be applied.
6. **Heterogeneity statistics not trustworthy.** I² = 0.0% and τ² = 0.0000 are boundary estimates at k = 2 and do not establish consistency.
7. **Unexamined clinical and methodological diversity.** Atorvastatin dose, treatment duration, comparator type (placebo vs no treatment), blinding, run-in design, adverse-event definitions, participant age and comorbidity, and concomitant interacting medications were not available as moderators and could not be explored.
8. **Composite, attribution-dependent outcome.** "Withdrawal due to adverse effects" depends on investigator attribution and local discontinuation thresholds and is not standardized across trials.
9. **Risk-of-bias assessment not incorporated into the quantitative synthesis.** No domain-level risk-of-bias weighting or sensitivity analysis restricted to low-risk studies was possible with two studies.
10. **Sparse-data method choice.** Inverse-variance pooling of log odds ratios is not the optimal estimator for rare events; alternative sparse-data methods were not applied because they could not materially alter a two-study, essentially event-free analysis.
11. **Short follow-up relative to the natural history of statin intolerance.** Muscle symptoms frequently emerge months into therapy; trials of limited duration systematically under-capture them.

### Certainty of the evidence

Applying GRADE-style reasoning to this single outcome, the certainty of the evidence for atorvastatin versus placebo or no treatment on withdrawal due to adverse effects should be rated **very low**, downgraded principally and severely for **imprecision** (a confidence interval spanning large benefit and large harm, with very few events), and additionally for **suspected publication/reporting bias** (two of six eligible studies reporting the outcome, with no possibility of formal assessment) and for **indirectness/inconsistency that cannot be excluded** (unexamined clinical diversity with heterogeneity statistics that are uninformative at k = 2).

---

## 13. Conclusion

Across the two randomized trials that provided arm-level data (k = 2; N = 118 participants), the pooled **odds ratio** for withdrawal due to adverse effects with atorvastatin versus placebo or no treatment was **0.974 (95% CI 0.132 to 7.193; p = 0.9797)**, computed with native binary-outcome pooling under a REML random-effects model. Statistical heterogeneity was nil (I² = 0.0%; τ² = 0.0000; Q = 0.001, p = 0.9799), but these dispersion estimates are not reliable with only two studies.

This result **favours neither atorvastatin nor placebo/no treatment**. It is a statistical tie, and because the measure is a ratio of event counts, no direction of benefit or harm can be determined.

The principal conclusion is one about evidence rather than about the drug: **the available randomized evidence on atorvastatin-related withdrawal due to adverse effects, as captured by this synthesis, is too sparse and too imprecise to support any conclusion.** The confidence interval is compatible with both a large tolerability advantage and a large tolerability disadvantage, so the analysis is uninformative rather than evidence of equivalence. This estimate should not be cited as showing that atorvastatin is as well tolerated as placebo, nor that it is worse tolerated.

**Implications for practice.** Clinicians should not revise prescribing on the basis of this analysis. Decisions about atorvastatin tolerability should rest on the much larger blinded randomized and individual-participant-data literature, and on individualized, ideally blinded, re-challenge in patients reporting intolerance.

**Implications for research.** Priorities are: (i) complete, arm-level, pre-specified reporting of discontinuation attributed to adverse effects in all statin trials, including explicit zero counts; (ii) standardized definitions and attribution procedures for adverse-effect withdrawal, with reporting of symptom category (myalgia, transaminase elevation, gastrointestinal) separately; (iii) avoidance of active run-in periods, or transparent reporting of pre-randomization intolerance exclusions; (iv) individual-participant-data syntheses that can support dose- and duration-stratified estimates; and (v) use of sparse-data-appropriate pooling methods when event counts are low.

---

## 14. Figures

| Figure | Path |
|---|---|
| Forest plot (study-level and pooled estimates) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect size vs study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

No funnel plot is presented, because funnel-plot-based assessment of small-study effects is uninterpretable with k = 2 studies.

---

## 15. References

Methodological and background sources consulted in the design, conduct, and interpretation of this review:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.

2. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA (editors). *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023.

3. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.

4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1–48.

5. IntHout J, Ioannidis JPA, Borm GF. The Hartung–Knapp–Sidik–Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian–Laird method. *BMC Medical Research Methodology*. 2014;14:25.

6. von Hippel PT. The heterogeneity statistic I² can be biased in small meta-analyses. *BMC Medical Research Methodology*. 2015;15:35.

7. Sweeting MJ, Sutton AJ, Lambert PC. What to add to nothing? Use and avoidance of continuity corrections in meta-analysis of sparse data. *Statistics in Medicine*. 2004;23(9):1351–1375.

8. Bradburn MJ, Deeks JJ, Berlin JA, Russell Localio A. Much ado about nothing: a comparison of the performance of meta-analytical methods with rare events. *Statistics in Medicine*. 2007;26(1):53–77.

9. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.

10. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.

11. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines 6: rating the quality of evidence — imprecision. *Journal of Clinical Epidemiology*. 2011;64(12):1283–1293.

12. Kirkham JJ, Dwan KM, Altman DG, et al. The impact of outcome reporting bias in randomised controlled trials on a cohort of systematic reviews. *BMJ*. 2010;340:c365.

13. Cholesterol Treatment Trialists' (CTT) Collaboration. Interpretation of the evidence for the efficacy and safety of statin therapy. *The Lancet*. 2016;388(10059):2532–2561.

14. Howard JP, Wood FA, Finegold JA, et al. Side effect patterns in a crossover trial of statin, placebo, and no treatment (SAMSON). *Journal of the American College of Cardiology*. 2021;78(12):1210–1222.

15. Herrett E, Williamson E, Brack K, et al. Statin treatment and muscle symptoms: series of randomised, placebo controlled n-of-1 trials (StatinWISE). *BMJ*. 2021;372:n135.

16. Newman CB, Preiss D, Tobert JA, et al. Statin safety and associated adverse events: a scientific statement from the American Heart Association. *Arteriosclerosis, Thrombosis, and Vascular Biology*. 2019;39(2):e38–e81.

*Note: the two primary trials contributing event counts to the quantitative synthesis are identified in this report by their pipeline identifiers (study_4_R4 and study_6_R6); full bibliographic citations correspond to the records retrieved by the systematic search for this comparison.*


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| withdrawal due to adverse effects | 2 | Odds Ratio (OR) | Yes | 0.9743 [0.1320, 7.1932] |
