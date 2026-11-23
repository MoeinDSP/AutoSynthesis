# Behavioural Support for Tobacco Cessation Compared With Brief Advice, No Intervention, or Matched Pharmacotherapy Alone: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Behavioural support — structured counselling, behavioural programmes, or multi-session support delivered face-to-face or remotely — is routinely recommended alongside or instead of pharmacotherapy for tobacco cessation. Its incremental contribution over brief advice, no intervention, or a matched pharmacotherapy-only background remains an important question for guideline developers and service commissioners.

**Objective.** To quantify the effect of behavioural support for smoking cessation (delivered alone, added to nicotine replacement therapy [NRT], or added to varenicline) versus a matched comparator without behavioural support (brief advice or no intervention; brief advice + NRT; or varenicline alone) on tobacco abstinence at the longest reported follow-up.

**Methods.** A systematic search and screening pipeline identified 7 eligible randomised controlled trials, of which 6 contributed extractable dichotomous abstinence data (quitters / randomised per arm) and were pooled. Random-effects meta-analysis was performed on the risk-ratio scale using restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was summarised with Cochran's Q, I², and τ². Publication bias was assessed with Egger's regression test and trim-and-fill.

**Results.** Six trials comprising 1,665 randomised participants were pooled. The pooled risk ratio (RR) for abstinence at longest follow-up was 1.529 (95% CI 0.984 to 2.376; p = 0.0591). Per the pre-specified direction field, the pooled result favours **neither arm** — the confidence interval includes the null, so the comparison is statistically a tie at the conventional 5% threshold despite a point estimate suggesting an approximately 53% relative increase in quit rates. Between-study heterogeneity was moderate: I² = 50.0%, τ² = 0.138516, Q = 9.525 (df = 5), p = 0.0899. Study-level standardized effects ranged from g = −0.017 (95% CI −0.203 to 0.170) to g = 0.931 (95% CI 0.437 to 1.426). Egger's test showed no funnel asymmetry (intercept = 0.3045, p = 0.8891) and trim-and-fill imputed no missing studies (k₀ = 0); publication-bias risk was rated low.

**Conclusions.** Behavioural support was associated with a point estimate favouring higher abstinence rates, but with a 95% confidence interval that crosses 1.0, the evidence from this small body of six trials does not establish a statistically significant benefit at the longest reported follow-up. The direction and magnitude of the point estimate are consistent with the wider cessation literature, and the non-significance is most plausibly attributable to limited power (k = 6) and moderate heterogeneity rather than to a demonstrated absence of effect. Larger and more homogeneous trial sets, and subgroup analyses by pharmacotherapy background and support intensity, are required before firm conclusions can be drawn.

**Registration.** Not registered; this report documents a retrospective, pipeline-assembled synthesis.

## 1. Introduction

Tobacco smoking remains the single largest preventable cause of premature mortality worldwide. Cessation interventions fall broadly into two families: pharmacological aids (nicotine replacement therapy [NRT], varenicline, bupropion, cytisine) and behavioural support (individual or group counselling, structured behavioural programmes, telephone or digital support, and multi-session self-help with contact). International guidance consistently recommends that pharmacotherapy be offered *with* behavioural support, and that behavioural support be offered even when pharmacotherapy is declined. The empirical basis for this recommendation rests on the assumption that behavioural support confers an incremental benefit over minimal intervention — typically operationalised in trials as "brief advice" or "usual care" — and that this incremental benefit persists when a pharmacological background is held constant across arms.

Testing that assumption requires a comparison in which the *only* systematic difference between arms is the presence or absence of behavioural support. Three such matched contrasts recur in the trial literature:

1. Behavioural support alone versus brief advice or no intervention;
2. Behavioural support + NRT versus brief advice + NRT;
3. Behavioural support + varenicline versus varenicline alone.

Pooling across these three contrast families is defensible because each isolates the same active ingredient (behavioural support) against a matched pharmacotherapy background, but it also introduces a predictable source of clinical heterogeneity: the marginal value of counselling may plausibly differ depending on whether participants are already receiving an efficacious pharmacotherapy.

### 1.1 Objective

The present meta-analysis addresses a single, pre-specified question:

> What is the effect of behavioural support, compared with brief advice or no intervention (with matched pharmacotherapy background where applicable), on tobacco use cessation?

The outcome of interest is tobacco abstinence at the longest reported follow-up, accepting continuous, prolonged, sustained, or 7-day point-prevalence definitions, whether biochemically validated or self-reported, extracted as the number of quitters out of the number randomised in each arm (i.e. an intention-to-treat denominator with non-responders treated as continuing smokers where the trial applied that convention).

### 1.2 Direction of effect

By construction, a risk ratio above 1.0 indicates that participants allocated to behavioural support achieved **higher** abstinence (quit) rates than those allocated to brief advice, no intervention, or the matched pharmacotherapy-only control. A risk ratio below 1.0 would indicate the reverse.

---

## 2. Methods

### 2.1 Search and screening

Records were identified and processed through an automated systematic-review pipeline that applied the eligibility criteria below to candidate reports of randomised controlled trials of behavioural smoking-cessation support. Screening proceeded in the conventional two stages (title/abstract, then full text), with reports excluded at full text if they did not present a matched no-behavioural-support comparator, did not report dichotomous abstinence counts, or duplicated a trial already represented in the dataset.

### 2.2 Eligibility criteria

- **Population.** Adults who smoke tobacco, recruited in any setting (community, primary care, hospital, workplace, or specialist cessation service).
- **Intervention.** Behavioural support for smoking cessation — counselling or a structured behavioural programme — delivered alone, added to NRT, or added to varenicline.
- **Comparator.** A matched comparator without behavioural support: brief advice or no intervention; brief advice + NRT; or varenicline alone. The pharmacotherapy background was required to be identical across arms within a trial.
- **Outcome.** Tobacco abstinence at the longest reported follow-up (continuous, prolonged, sustained, or 7-day point prevalence; biochemically validated or self-reported), extracted as quitters / randomised per arm.
- **Design.** Randomised controlled trial.

### 2.3 Data extraction

For each included trial, the number of quitters and the number randomised were extracted for the behavioural-support arm and the matched comparator arm. Where a trial reported multiple abstinence definitions or multiple follow-up points, the longest reported follow-up was taken, in line with the pre-specified outcome definition.

### 2.4 Statistical analysis

The primary effect measure was the **Risk Ratio (RR)**, specified explicitly in the review question (`effect_measure_source: explicit_user_request`). Pooling was performed **natively on the risk-ratio scale** (`native_pooling_used: true`; `computation_scale: RR`), so the headline pooled estimate reported below is a confirmed native-scale risk ratio and not a back-transformed standardized surrogate. No conflict between the requested and detected effect measures was recorded.

A random-effects model was fitted using **restricted maximum likelihood (REML)** estimation of the between-study variance τ², which is appropriate given the anticipated clinical and methodological diversity across contrast families. Heterogeneity was characterised by:

- **Cochran's Q** with its associated p-value (a test of the null hypothesis of homogeneity);
- **I²**, the proportion of total variability attributable to between-study heterogeneity rather than sampling error;
- **τ²**, the absolute between-study variance on the analysis scale.

For descriptive and diagnostic purposes, each trial's effect was additionally expressed as a standardized mean difference (Hedges' *g*) with a 95% confidence interval, which permits visual comparison of effect magnitude and precision on a common scale and supports the small-study-effect diagnostics. These per-study *g* values are descriptive companions to, not replacements for, the native risk-ratio pooling.

Publication bias and small-study effects were assessed using **Egger's regression test** of funnel-plot asymmetry and the **Duval and Tweedie trim-and-fill** procedure.

All analyses were conducted within the review pipeline; figures referenced in this report are stored at the paths given in Section 9.

---

## 3. Search and Screening Results

The pipeline identified and retained **7 studies** meeting the eligibility criteria. Of these, **6 contributed an extractable effect size** for the primary outcome and were carried forward into the quantitative synthesis; **1 eligible study did not yield usable dichotomous abstinence counts at the longest reported follow-up** and therefore appears in the narrative inventory of included studies but not in the pooled estimate. This discrepancy between the number of included studies (7) and the number of pooled effect sizes (6) is reported transparently rather than reconciled by imputation.

A PRISMA-style accounting of the final stage is therefore:

| Stage | n |
|---|---|
| Studies meeting eligibility criteria (included) | 7 |
| Studies contributing extractable effect sizes | 6 |
| Studies in the pooled random-effects analysis (k) | 6 |
| Participants randomised across pooled studies | 1,665 |

Upstream record counts (records identified, duplicates removed, titles/abstracts screened, full texts assessed) were handled within the automated pipeline and are not itemised in the available context; readers should treat the screening cascade above as the portion of the PRISMA flow that can be reported with confidence. No separate set of excluded-at-full-text reports with reasons was returned by the pipeline, and no validation flags (e.g. reviews removed, unclassifiable outcomes, or trial reports dropped to prevent double-counting) were raised for this dataset.

---

## 4. Included Studies

Six trials contributed data to the meta-analysis. Table 1 summarises their standardized effect estimates and analysed sample sizes. Study labels follow the pipeline's internal record identifiers; where the original citations are available they should be substituted in the final published version.

**Table 1. Studies contributing to the pooled analysis**

| Study label | Hedges' *g* | 95% CI | n analysed |
|---|---|---|---|
| study_2_R2 | 0.330 | 0.154 to 0.505 | 506 |
| study_3_R3 | 0.807 | 0.619 to 0.994 | 474 |
| study_4_R4 | 0.113 | −0.317 to 0.544 | 85 |
| study_5_R5 | −0.017 | −0.203 to 0.170 | 442 |
| study_6_R6 | 0.032 | −0.404 to 0.468 | 81 |
| study_7_R7 | 0.931 | 0.437 to 1.426 | 77 |
| **Total** | — | — | **1,665** |

A seventh eligible study (not listed above) met the inclusion criteria but did not provide extractable quitters/randomised counts at the longest follow-up and is excluded from all quantitative results.

Sample sizes were markedly unbalanced across the evidence base: three trials were comparatively large (n = 442–506) and three were small (n = 77–85). Together the three largest trials (study_2_R2, study_3_R3, study_5_R5) account for 1,422 of the 1,665 randomised participants (85.4%), and will therefore dominate an inverse-variance-weighted pooled estimate.

---

## 5. Effect Sizes

### 5.1 Study-level estimates

Four of the six trials produced point estimates favouring behavioural support (g = 0.032 to 0.931), one produced an essentially null estimate marginally on the side of the comparator (g = −0.017), and none produced a statistically significant estimate favouring the comparator arm. Three trials had confidence intervals excluding zero, all in the direction of higher abstinence with behavioural support:

- **study_3_R3**: g = 0.807 (95% CI 0.619 to 0.994), n = 474 — the largest statistically significant effect among the well-powered trials;
- **study_2_R2**: g = 0.330 (95% CI 0.154 to 0.505), n = 506 — a modest but precisely estimated benefit;
- **study_7_R7**: g = 0.931 (95% CI 0.437 to 1.426), n = 77 — the largest point estimate overall, but from the smallest trial and with correspondingly wide bounds.

The remaining three trials had confidence intervals spanning zero:

- **study_5_R5**: g = −0.017 (95% CI −0.203 to 0.170), n = 442 — a precisely estimated null;
- **study_4_R4**: g = 0.113 (95% CI −0.317 to 0.544), n = 85;
- **study_6_R6**: g = 0.032 (95% CI −0.404 to 0.468), n = 81.

The distribution of these estimates is plotted in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between effect magnitude and study size is visualised in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

### 5.2 A note on the two scales

The per-study values in Table 1 are standardized mean differences (Hedges' *g*), used here for descriptive comparison and diagnostics. The pooled inferential result in Section 6 is a **native-scale Risk Ratio**, as requested in the review question and as confirmed by the pipeline (`native_pooling_used: true`). Readers should not attempt to reconcile the numerical value of the pooled RR with the arithmetic average of the *g* values; they are different metrics with different scales and different weighting behaviour. The deterministic Effect Measure Summary table appended to this report is authoritative on measure labelling.

---

## 6. Meta-Analytic Result

A single outcome group was analysed; the context data contain no `meta_analysis_groups` entry, so there is no need to report separate pooled estimates by outcome or timepoint, and no group was flagged as having insufficient data for pooling.

**Table 2. Random-effects pooled result (REML)**

| Parameter | Value |
|---|---|
| Effect measure | Risk Ratio (RR) |
| Native-scale pooling | Yes (confirmed) |
| Number of studies (k) | 6 |
| Participants (N) | 1,665 |
| **Pooled risk ratio** | **1.529** |
| 95% confidence interval | 0.984 to 2.376 |
| p-value | 0.0591 |
| Favours | **Neither arm** (essentially a tie; a ratio measure where favourability depends on which event was counted) |
| τ² | 0.138516 |
| I² | 50.0% |
| Cochran's Q (df = 5) | 9.525 |
| Q p-value | 0.0899 |
| Estimator | REML |

The pooled risk ratio for tobacco abstinence at longest follow-up was **RR = 1.529 (95% CI 0.984 to 2.376; p = 0.0591)**. Interpreted on the relative-risk scale, the point estimate corresponds to approximately a 53% relative increase in the probability of abstinence for participants receiving behavioural support compared with those receiving brief advice, no intervention, or the matched pharmacotherapy-only control.

However, in accordance with the pipeline's pre-specified direction field, this result **favours neither arm**: the 95% confidence interval includes the null value of 1.0 (lower bound 0.984), and the p-value of 0.0591 does not cross the conventional 5% significance threshold. The analysis is therefore statistically a tie. The confidence interval is compatible with anything from a negligible 1.6% *relative reduction* in quitting at its lower bound to a 138% *relative increase* at its upper bound — a range that is clinically very wide and that does not permit a confident statement about either the presence or the absence of benefit.

It is worth stating plainly why the point estimate and the inference diverge. With only six trials and three of them small, the pooled estimate carries substantial uncertainty; the lower confidence bound sits 1.6% below the null, meaning the result is "marginally non-significant" in the familiar and uninformative sense. Nothing in these data refutes a meaningful benefit of behavioural support; equally, nothing in these data demonstrates one at conventional thresholds.

The forest plot showing individual study estimates, weights, and the pooled summary is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. A cumulative meta-analysis, ordering studies and showing the evolution of the pooled estimate as evidence accrues, is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`.

---

## 7. Heterogeneity

Between-study heterogeneity was **moderate**:

- **I² = 50.0%** — exactly half of the observed variability in effect estimates is attributable to genuine between-study differences rather than within-study sampling error. By the conventional Cochrane benchmarks (25% low, 50% moderate, 75% substantial), this sits precisely at the moderate threshold.
- **τ² = 0.138516** — the estimated between-study variance on the analysis scale, implying a between-study standard deviation of approximately 0.372 (√0.138516). This is a non-trivial dispersion of true effects.
- **Cochran's Q = 9.525 on 5 degrees of freedom, p = 0.0899** — the homogeneity test is not rejected at the 5% level, but is suggestive at the 10% level. Q is well known to be underpowered when k is small, so a p-value of 0.0899 with k = 6 should not be read as reassurance of homogeneity; the I² and τ² estimates are the more informative heterogeneity indicators here.

Taken together, these statistics indicate that the six trials are unlikely to be estimating a single common effect. The pattern in Table 1 is consistent with this: two large trials (study_2_R2, study_3_R3) show clear benefit of differing magnitude, while a third large trial of comparable precision (study_5_R5) shows essentially no effect at all. The contrast between study_3_R3 (g = 0.807, CI 0.619 to 0.994) and study_5_R5 (g = −0.017, CI −0.203 to 0.170) is particularly striking, as their confidence intervals do not overlap — strong evidence that these two trials are not estimating the same quantity.

Because the random-effects model incorporates τ² into the standard error of the pooled estimate, this moderate heterogeneity directly widens the confidence interval and is a proximate cause of the non-significant p-value. Had the same point estimates arisen with no between-study variance, the interval would have been appreciably narrower.

A graphical summary of the heterogeneity diagnostics is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 8. Moderators

No formal moderator analysis (meta-regression or subgroup analysis) was conducted, and none could be conducted responsibly with k = 6. Standard guidance recommends a minimum of roughly ten studies per covariate for meta-regression; with six studies, any moderator model would be overfitted and its coefficients uninterpretable.

Three moderators were, however, anticipated a priori as plausible explanations for the moderate heterogeneity observed, and are flagged here as priorities for future, better-powered synthesis:

1. **Pharmacotherapy background** (behavioural support alone vs. added to NRT vs. added to varenicline). The marginal benefit of counselling is expected to be larger against a minimal-intervention background than against an efficacious pharmacotherapy background, because the comparator arm in the latter case already achieves substantially elevated quit rates, compressing the achievable relative difference. This is the single most likely driver of the dispersion in Table 1.
2. **Intensity and modality of behavioural support** (number of sessions, total contact time, individual vs. group, in-person vs. telephone vs. digital). Dose–response relationships for behavioural support are well documented in the broader literature.
3. **Outcome definition and verification** (continuous/prolonged abstinence vs. 7-day point prevalence; biochemically validated vs. self-reported). Point-prevalence definitions and unvalidated self-report typically yield higher absolute quit rates and can shift relative effects.

The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) displays effect size against study size and provides an informal visual check for a size–effect relationship; the two largest observed effects (study_7_R7, g = 0.931; study_3_R3, g = 0.807) come from trials at opposite ends of the size distribution (n = 77 and n = 474 respectively), which argues against a simple small-study explanation for the heterogeneity.

---

## 9. Publication Bias

Two complementary diagnostics were applied.

**Egger's regression test** showed no evidence of funnel-plot asymmetry: intercept = 0.3045, **p = 0.8891**. This p-value is far from conventional significance, indicating that effect sizes were not systematically related to their standard errors and that small-study effects are unlikely in this dataset.

**Trim-and-fill** imputed **no missing studies (k₀ = 0)**. Consequently the adjusted pooled estimate is identical to the unadjusted one, and the funnel plot is essentially symmetric. The trim-and-fill routine reports its adjusted summary on the standardized scale as g = 0.3605; because no studies were imputed, this value is simply the standardized-scale restatement of the unchanged pooled effect and should not be confused with the native-scale pooled risk ratio of 1.529 reported in Section 6.

The overall publication-bias risk was rated **low**.

**Caveat.** These converging results support the "low risk" rating, but publication-bias tests have limited statistical power, particularly when the number of included studies is small (fewer than 10, as here, with k = 6) or when between-study heterogeneity is appreciable (as here, I² = 50.0%). Egger's test is specifically known to be unreliable below ten studies. A null result therefore reflects an **absence of detectable asymmetry rather than proof that no bias exists**. Grey literature, unpublished trial arms, and selectively reported outcome definitions remain possible sources of bias that these tests cannot exclude.

**Figure inventory.**

| Figure | Path |
|---|---|
| Forest plot | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect vs. study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 10. Discussion

### 10.1 Principal findings

Across six randomised trials and 1,665 randomised participants, behavioural support for smoking cessation yielded a pooled risk ratio for abstinence at longest follow-up of 1.529 (95% CI 0.984 to 2.376; p = 0.0591) relative to brief advice, no intervention, or a matched pharmacotherapy-only comparator. Per the pre-specified direction field, this result favours **neither arm**. The point estimate is substantial and in the expected direction, but the interval crosses the null and the result does not reach conventional statistical significance.

This is best characterised as an *underpowered confirmation of direction* rather than either a positive or a negative finding. Four of six trials, including the two largest contributors to the pooled weight, pointed towards higher abstinence with behavioural support, and three trials individually achieved intervals excluding the null — all in the pro-behavioural-support direction. No trial produced a statistically significant result in the opposite direction. The non-significance of the pooled estimate arises from the combination of a small number of trials, three of them very small, and moderate between-study heterogeneity (I² = 50.0%, τ² = 0.1385) that inflates the random-effects standard error.

### 10.2 Relation to existing evidence

The direction and approximate magnitude of the point estimate are consistent with the established cessation literature, in which behavioural support typically yields relative increases in abstinence in the range of roughly 40% to 80% when added to minimal intervention, and smaller incremental gains when added to an efficacious pharmacotherapy. The present pooled RR of 1.529 falls squarely within that range. What this synthesis adds is not a new magnitude estimate but a demonstration of how fragile that estimate becomes when restricted to a small set of strictly matched-comparator trials with mixed pharmacotherapy backgrounds.

### 10.3 Interpretation of heterogeneity

The most clinically interpretable feature of these data is the non-overlap between study_3_R3 (g = 0.807, CI 0.619 to 0.994) and study_5_R5 (g = −0.017, CI −0.203 to 0.170). Two well-powered trials addressing nominally the same question reached incompatible conclusions. The most parsimonious explanation, given the review's design, is that these trials occupy different cells of the pharmacotherapy-background moderator: behavioural support added to minimal intervention has considerable room to improve on a low baseline quit rate, whereas behavioural support added to varenicline competes against an already-effective pharmacological comparator. If so, the pooled estimate of 1.529 is an average over genuinely different effects and should not be applied uniformly across clinical contexts. With k = 6 this explanation cannot be tested, and it remains a hypothesis.

### 10.4 Implications for practice and policy

These results should not be read as grounds for withdrawing behavioural support from cessation services. The point estimate favours behavioural support, the direction is consistent across most trials, publication-bias diagnostics are reassuring, and the intervention is low-risk and inexpensive relative to its potential benefit. What these results *do* counsel against is the citation of a precise, single-number efficacy figure for behavioural support across all pharmacotherapy contexts. Commissioners should expect the incremental value of counselling to vary with the pharmacological background against which it is delivered.

### 10.5 Implications for research

Priority needs are: (i) more matched-comparator trials, particularly in the varenicline-background contrast where the comparator is strongest; (ii) consistent reporting of biochemically validated continuous abstinence at a common follow-up point (e.g. 6 and 12 months) to reduce outcome-definition heterogeneity; and (iii) explicit reporting of behavioural-support dose (sessions, contact minutes, modality) to permit dose–response meta-regression once k is sufficient.

---

## 11. Data Quality & Validation Notes

No formal validation flags were returned by the analysis pipeline for this dataset. Three data-quality observations nonetheless warrant plain statement:

1. **One included study contributed no effect size.** Seven studies met the eligibility criteria but only six yielded extractable quitters/randomised counts at the longest reported follow-up. The pooled analysis therefore rests on six of seven eligible trials, and the excluded trial's direction of effect is unknown to this synthesis.
2. **Two measurement scales appear in this report.** Per-study estimates are reported as Hedges' *g* (descriptive and diagnostic), while the pooled inferential estimate is a native-scale Risk Ratio. The pipeline confirmed that native risk-ratio pooling was used (`native_pooling_used: true`), so the headline figure of RR = 1.529 is a confirmed native-scale result and not a standardized fallback. The trim-and-fill output (g = 0.3605) is reported on the standardized scale and is not comparable with the pooled RR.
3. **Upstream PRISMA counts are not itemised.** Records identified, de-duplicated, title/abstract-screened, and full-text-assessed were handled inside the automated pipeline and were not returned in a form permitting itemisation here. No list of full-text exclusions with reasons is available. Readers should treat the screening account in Section 3 as partial.

No documents were flagged as reviews or duplicates requiring removal, no outcomes were flagged as unclassifiable, no effect measures required separate pooling, and no trial reports were flagged for exclusion to prevent double-counting.

---

## 12. Limitations

1. **Very small evidence base.** With k = 6, the analysis is underpowered for its primary comparison, cannot support moderator analysis, and yields unstable estimates of τ². The REML estimate of between-study variance is itself imprecise at this k.
2. **Marginal non-significance.** The lower confidence bound of 0.984 sits only 1.6% below the null. Inferences drawn from either side of this boundary are fragile, and a single additional trial could move the result across the conventional threshold in either direction.
3. **Unexplained moderate heterogeneity.** I² = 50.0% with non-overlapping confidence intervals between two large trials indicates genuine effect-size diversity that this analysis cannot attribute to any specific source.
4. **Pooling across three contrast families.** Behavioural support alone, added to NRT, and added to varenicline were combined. These are conceptually distinct comparisons with plausibly different true effects, and their combination is a source of clinical heterogeneity that was not stratified.
5. **Heterogeneous outcome definitions.** Continuous, prolonged, sustained, and 7-day point-prevalence abstinence, biochemically validated or self-reported, were all admissible. "Longest reported follow-up" varies across trials in absolute duration, so the pooled estimate does not refer to a single common timepoint.
6. **Self-report and verification bias.** Where abstinence was self-reported without biochemical validation, differential misreporting between arms is possible, and participants receiving intensive behavioural contact may be more susceptible to social-desirability bias in favour of reporting abstinence.
7. **Risk-of-bias assessment not reported.** No domain-level risk-of-bias appraisal (e.g. RoB 2) was available from the pipeline, so the internal validity of individual trials — particularly allocation concealment, blinding of outcome assessment, and handling of loss to follow-up — could not be incorporated into the synthesis or used for sensitivity analysis.
8. **Publication-bias tests underpowered.** Egger's test and trim-and-fill are unreliable below ten studies; their null results reduce but do not eliminate concern about small-study effects and selective reporting.
9. **Limited external validity information.** Setting, country, baseline dependence, and population characteristics were not available for the included trials, limiting judgements about the generalisability of the pooled estimate.
10. **No certainty-of-evidence grading.** A formal GRADE assessment was not performed; given imprecision (interval crossing the null) and inconsistency (I² = 50%), the certainty of this body of evidence would most likely be rated low.

---

## 13. Conclusion

In a random-effects meta-analysis of six randomised trials and 1,665 participants, behavioural support for smoking cessation — delivered alone, added to NRT, or added to varenicline — produced a pooled risk ratio for tobacco abstinence at longest follow-up of **1.529 (95% CI 0.984 to 2.376; p = 0.0591)** compared with brief advice, no intervention, or a matched pharmacotherapy-only control. In line with the pre-specified direction field, this result **favours neither arm**: the confidence interval includes the null and the comparison is statistically a tie at the 5% level.

The point estimate nonetheless lies in the direction of benefit and is of a magnitude consistent with the broader cessation literature, and most contributing trials pointed the same way. Between-study heterogeneity was moderate (I² = 50.0%, τ² = 0.138516, Q = 9.525, p = 0.0899), most plausibly reflecting differences in the pharmacotherapy background against which behavioural support was tested. Publication-bias risk was rated low (Egger's p = 0.8891; trim-and-fill k₀ = 0), with the standard caveat that these tests have little power at k = 6.

The appropriate conclusion is therefore one of **unresolved but directionally encouraging evidence**: this small, heterogeneous set of matched-comparator trials is insufficient to confirm a statistically significant benefit of behavioural support at the longest reported follow-up, and is equally insufficient to exclude one. Larger trial sets, stratified by pharmacotherapy background and support intensity and using harmonised, biochemically validated abstinence outcomes, are needed to resolve the question.

---

## 14. References

The analysis pipeline returned internal record identifiers rather than bibliographic citations. Full references for the six pooled trials and the one eligible-but-unextractable trial should be inserted in place of the identifiers below before publication.

1. study_2_R2. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 506.
2. study_3_R3. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 474.
3. study_4_R4. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 85.
4. study_5_R5. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 442.
5. study_6_R6. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 81.
6. study_7_R7. Randomised controlled trial of behavioural support for smoking cessation versus matched comparator. [Full citation to be supplied.] n = 77.
7. [Seventh eligible study — included at full text, no extractable dichotomous abstinence data at longest follow-up; not pooled. Full citation to be supplied.]

### Methodological references

- Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
- Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327:557–560.
- Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
- Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315:629–634.
- Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56:455–463.
- Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis*. Academic Press; 1985.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| tobacco use cessation (smoking abstinence) | 6 | Risk Ratio (RR) | Yes | 1.5290 [0.9838, 2.3764] |
