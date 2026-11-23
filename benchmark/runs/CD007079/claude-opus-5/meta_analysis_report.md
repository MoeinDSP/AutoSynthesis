# High-Dose Calcium Supplementation (≥1 g/day) During Pregnancy and the Risk of Preterm Birth Before 37 Weeks' Gestation: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Calcium supplementation during pregnancy is recommended in populations with low dietary calcium intake, primarily for the prevention of pre-eclampsia. Whether high-dose supplementation (≥1 g elemental calcium per day) also reduces the risk of preterm birth remains uncertain, and dose-stratified evidence has not been synthesised separately from pooled all-dose analyses.

**Objective.** To estimate the effect of high-dose calcium supplementation (≥1 g elemental calcium/day) during pregnancy, versus placebo or no calcium, on the risk of preterm birth before 37 completed weeks' gestation.

**Methods.** We systematically screened randomised controlled trials and trial arms administering ≥1 g/day elemental calcium during pregnancy that reported dichotomous preterm birth (<37 weeks) data as the number of women with an event and the number randomised per arm. Only the dose-stratified high-dose comparison was eligible; non-dose-stratified pooled analyses and timing-stratified ("calcium started before/after X weeks") analyses of the same outcome were excluded as separate analyses, and trials with zero events in both arms were treated as not estimable. Effects were pooled on the native risk ratio (RR) scale using restricted maximum likelihood (REML) random-effects models. Heterogeneity was quantified with Cochran's Q, τ² and I². Small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** Eleven study records entered the data-extraction stage and seven yielded an extractable high-dose preterm birth effect estimate. Six estimates (n = 13,567 randomised women) were poolable for the primary outcome group *preterm birth before 37 weeks' gestation (measure = RR)*. The pooled Risk Ratio (RR) was **0.691 (95% CI 0.456 to 1.048; p = 0.0823; k = 6)**. Native-scale pooling was confirmed for this estimate. On the direction field carried with the result, the pooled estimate favours **neither arm** — it is statistically compatible with no effect, the confidence interval crossing the null, and the sign convention of a ratio measure means favourability depends on which event was counted. Heterogeneity was substantial: Q = 14.742 (df = 5, p = 0.0115), I² = 86.23%, τ² = 0.159037. A second outcome group (same outcome reported on the odds ratio scale) contained only one trial (n = 524; standardized effect −0.371) and is **flagged as insufficient data — it could not be pooled and no pooled value is reported for it**. Egger's test indicated significant funnel asymmetry (intercept = −0.0381, p = 0.0141; overall small-study-effect risk rated **high**), although trim-and-fill imputed no missing studies (k₀ = 0), leaving the adjusted estimate identical to the unadjusted one.

**Conclusions.** In this dose-stratified synthesis, high-dose calcium supplementation during pregnancy was associated with a point estimate suggesting a ~31% relative reduction in preterm birth before 37 weeks, but the 95% confidence interval included the null (0.456–1.048) and the result did not reach conventional statistical significance. Between-trial heterogeneity was substantial (I² = 86.23%) and evidence of small-study effects was significant, with the largest trials showing the smallest or null effects. The present evidence does not support a confirmed benefit of high-dose antenatal calcium on preterm birth and should be regarded as inconclusive and potentially optimistic.


## 1. Introduction

Preterm birth — delivery before 37 completed weeks of gestation — remains the leading direct cause of neonatal mortality and a major contributor to long-term neurodevelopmental and respiratory morbidity worldwide. Interventions that are inexpensive, widely available, and deliverable through routine antenatal care are therefore of high public-health interest.

Calcium supplementation during pregnancy has an established evidence base for the prevention of hypertensive disorders of pregnancy, and the World Health Organization recommends supplementation in populations with low dietary calcium intake. A frequently cited secondary benefit is a reduction in preterm birth, plausibly mediated through reduced pre-eclampsia and associated iatrogenic (medically indicated) preterm delivery, and possibly through direct effects of extracellular calcium on myometrial smooth-muscle excitability and parathyroid hormone–renin axis signalling.

However, the evidence for preterm birth is complicated by three issues. First, trials have used widely differing doses, from <1 g/day ("low-dose", often combined with other micronutrients) to ≥2 g/day. Pooling across doses mixes biologically distinct exposures. Second, the same outcome is frequently re-analysed within reviews under several stratifications (by dose, by gestational age at initiation of supplementation), creating a risk of double-counting the same randomised participants if these strata are naively combined. Third, trial sizes are extremely unequal, ranging from a few dozen to several thousand participants, which makes the synthesis vulnerable to small-study effects.

This report addresses a single, narrowly specified question: **among pregnant women randomised to ≥1 g/day elemental calcium versus placebo or no calcium, what is the relative risk of preterm birth before 37 weeks' gestation?** Only the dose-stratified high-dose comparison is treated as eligible, so that the estimate reflects a defined exposure rather than a dose-heterogeneous average.

---

## 2. Methods

### 2.1 Protocol and reporting

The review follows the PRISMA 2020 reporting framework. The analysis was specified around a single PICO:

| Element | Specification |
|---|---|
| **Population** | Pregnant women (any parity, any baseline risk, any baseline dietary calcium intake) |
| **Intervention** | High-dose calcium supplementation during pregnancy, ≥1 g elemental calcium per day |
| **Comparator** | Placebo or no calcium supplementation |
| **Outcome** | Preterm birth, defined as delivery before 37 completed weeks' gestation |
| **Study design** | Randomised controlled trials (or eligible high-dose arms thereof) |

### 2.2 Eligibility and analysis-selection rules

Three analysis-level rules were applied, and they materially shape the included dataset:

1. **Dose restriction.** Only trials, or trial arms, administering ≥1 g/day elemental calcium were eligible. Low-dose comparisons were excluded.
2. **One analysis per outcome.** Only the *dose-stratified* high-dose comparison for preterm birth <37 weeks was eligible. Non-dose-stratified pooled analyses of the same outcome, and timing-stratified analyses ("started to take calcium before/after X weeks' gestation"), were **excluded as separate analyses** because they re-report the same randomised participants and would double-count them.
3. **Estimability.** Trials reporting **zero preterm birth events in both arms** were treated as **not estimable** and excluded from pooling, since no risk ratio can be computed.

### 2.3 Data extraction

For each eligible trial/arm we extracted the number of women (or pregnancies) with a preterm birth event and the total number randomised in each arm. Where the source reported an odds ratio rather than a risk ratio for the same outcome, this was recorded and handled as a distinct effect-measure group rather than silently converted (see §8, Data Quality & Validation Notes).

### 2.4 Statistical analysis

The primary effect measure was the **Risk Ratio (RR)**, specified by explicit user request (`effect_measure_source = explicit_user_request`). Pooling was performed on the **native RR scale** (`computation_scale = RR`; `native_pooling_used = true`), i.e. the pooled estimate is a confirmed native-scale risk ratio and not a back-transformed standardized surrogate. Random-effects models were fitted by **restricted maximum likelihood (REML)**.

Per-study effect sizes are additionally reported by the pipeline on a standardized (Hedges'-*g*-type) scale for display and for small-study-effect diagnostics; on that scale a **negative** value denotes fewer preterm births in the calcium arm. The pooled statistic reported below is the native RR, where a value **below 1** on the raw scale denotes fewer preterm births in the calcium arm. Readers should note that the pipeline's `pooled_effect` / `pooled_g` fields carry the raw statistical sign convention; the arm favoured is therefore reported throughout using the explicit `favors` field accompanying each result, not inferred from the sign.

Heterogeneity was quantified using Cochran's **Q**, between-study variance **τ²**, and **I²**. Small-study effects / publication bias were assessed using **Egger's regression test** of funnel-plot asymmetry and the **Duval & Tweedie trim-and-fill** procedure. Because the outcome data fell into more than one effect-measure group, each group was analysed and reported separately; groups with too few studies to pool are reported as insufficient rather than estimated.

---

## 3. Search and Screening

The screening and data-flow for this synthesis is summarised below.

- **Records entering data extraction:** 11 study records were carried into the extraction stage as potentially containing a high-dose calcium versus placebo/no-treatment comparison for preterm birth <37 weeks.
- **Records yielding an extractable effect estimate:** 7 of the 11 records yielded a usable dose-stratified high-dose effect estimate for preterm birth <37 weeks (`n_effect_sizes = 7`).
- **Records not contributing an estimate:** 4 records did not contribute an estimable high-dose effect for this outcome. The pre-specified reasons for non-contribution are (a) the trial contributed only to a non-eligible analysis (non-dose-stratified or timing-stratified) for this outcome, (b) the trial's eligible arm was below the ≥1 g/day dose threshold, or (c) the trial reported **zero preterm birth events in both arms** and was therefore **not estimable**.
- **Estimates entering the primary pooled analysis:** 6 (one of the 7 extractable estimates fell into a separate effect-measure group and could not be combined with the other six; see §4.2 and §8).

Because the eligibility rules deliberately admit only one analysis per outcome per trial, no participant is counted twice in the primary pooled estimate.

PRISMA flow at the analysis stage:

```
Records carried into extraction .................. 11
      │
      ├── No estimable high-dose <37 wk effect .....  4
      │     (ineligible analysis stratum / dose <1 g per day /
      │      zero events in both arms = not estimable)
      │
      └── Extractable high-dose effect estimates ....  7
                │
                ├── Outcome group: <37 wk, measure = RR ..  6  → POOLED (n = 13,567)
                └── Outcome group: <37 wk, measure = OR ..  1  → NOT POOLED
                                                               (insufficient data, k = 1, n = 524)
```

---

## 4. Included Studies

### 4.1 Characteristics

Six trials contributed to the primary pooled analysis, together randomising **13,567 women**. The defining feature of this evidence base is extreme imbalance in trial size: two trials contributed 8,080 and 4,589 randomised women respectively (together 93.3% of the total sample), while the remaining four trials contributed between 63 and 524 women each. Any random-effects pooling of such a dataset will down-weight the two large trials relative to a fixed-effect analysis, and the pooled estimate is consequently highly sensitive to the τ² estimate (see §6).

All included comparisons administered ≥1 g/day elemental calcium against placebo or no calcium, and all reported preterm birth before 37 completed weeks as a count of affected women/pregnancies per randomised arm.

### 4.2 Outcome groups

The extracted data resolved into **two** outcome/effect-measure groups for the same clinical outcome:

| Group | Outcome | Effect measure group | k | n randomised | Poolable? |
|---|---|---|---|---|---|
| 1 | Preterm birth before 37 weeks' gestation | measure = RR | 6 | 13,567 | Yes |
| 2 | Preterm birth before 37 weeks' gestation | measure = OR (as reported by source) | 1 | 524 | **No — insufficient data** |

Group 2 contains a **single** trial and therefore **cannot be meta-analysed**; no pooled effect, confidence interval, or heterogeneity statistic exists for it, and none is invented here. Its single standardized effect estimate is −0.371 (n = 524), which on the standardized display scale is directionally consistent with fewer preterm births in the calcium arm, but as a single unreplicated estimate it provides no independent pooled evidence.

---

## 5. Effect Sizes

Study-level estimates as computed by the pipeline are shown below on the standardized display scale (negative = fewer preterm births in the calcium arm). The pooled analysis in §6 was nonetheless carried out on the **native RR scale**.

| Study label | Standardized effect | 95% CI | n | Outcome group |
|---|---|---|---|---|
| study_1_R1 | −0.6580 | [−0.951, −0.365] | 189 | RR group (pooled) |
| study_3_R3 | −0.6088 | [−0.900, −0.318] | 190 | RR group (pooled) |
| study_5_R5 | −0.4519 | [−0.638, −0.266] | 456 | RR group (pooled) |
| study_6_R6 | −0.0520 | [−0.096, −0.008] | 8,080 | RR group (pooled) |
| study_7_R7 | −0.3707 | [−0.544, −0.198] | 524 | **OR group (not pooled)** |
| study_9_R9 | +0.0488 | [−0.009, 0.107] | 4,589 | RR group (pooled) |
| study_10_R10 | −0.2123 | [−0.709, 0.284] | 63 | RR group (pooled) |

Two features are immediately apparent and drive everything that follows.

1. **A monotone size–effect gradient.** The three smallest trials with precise estimates (study_1_R1, n = 189; study_3_R3, n = 190; study_5_R5, n = 456) report the largest protective effects (−0.66, −0.61, −0.45). The two largest trials report effects that are near-null in magnitude: study_6_R6 (n = 8,080) at −0.052 and study_9_R9 (n = 4,589) at **+0.049**, the latter being the only estimate pointing in the direction of *more* preterm births in the calcium arm. The smallest trial (study_10_R10, n = 63) is imprecise and non-significant (−0.212, CI crossing zero).
2. **Directional discordance at the extremes.** study_9_R9 is positive while every other estimate is negative. This single discordance, in a trial carrying one third of the total sample, is a principal source of the heterogeneity documented in §6.

Study-level effects and weights are displayed in the forest plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The distribution of effect sizes across trials is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

---

## 6. Meta-Analytic Results

### 6.1 Group 1 — Preterm birth before 37 weeks' gestation (measure = RR)

Random-effects (REML) pooling of the six eligible high-dose comparisons gave:

| Quantity | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** (`measure_label`) |
| Native-scale pooling confirmed | **Yes** (`native_pooling_used = true`) |
| Number of comparisons (k) | 6 |
| Participants randomised (n) | 13,567 |
| **Pooled Risk Ratio (RR)** | **0.691** |
| 95% confidence interval | **0.456 to 1.048** |
| p-value | **0.0823** |
| Cochran's Q (df = 5) | 14.742 (p = 0.0115) |
| τ² | 0.159037 |
| I² | 86.23% |
| Model | Random effects, REML |
| **Favours** | **Neither arm** — essentially a tie, or a ratio measure where favourability depends on which event was counted (`favors` field) |

The point estimate of 0.691 corresponds nominally to a 30.9% relative reduction in the risk of preterm birth before 37 weeks with high-dose calcium. **However, the 95% confidence interval (0.456–1.048) crosses the null value of 1 and the two-sided p-value is 0.0823**, so the result does not meet conventional thresholds for statistical significance at α = 0.05. In accordance with the direction field carried with this result, the pooled estimate is reported as favouring **neither arm**: the interval is compatible with a large benefit (RR 0.46, a 54% relative reduction) and with a small harm (RR 1.05, a 5% relative increase) alike. The effect measure here is a confirmed native-scale risk ratio, not a standardized fallback.

Because τ² is large relative to the within-study variances, the pooled mean is a poor summary of what a new trial would observe. An approximate 95% prediction interval computed post hoc from τ² = 0.159 and the pooled standard error spans roughly RR 0.20 to RR 2.4 — i.e. the data are consistent with future high-dose trials showing either a substantial reduction or a substantial increase in preterm birth. This interval should be read as indicative, as it was derived from the reported summary statistics rather than reported directly by the model.

A cumulative meta-analysis, ordered by study precision, is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`; it illustrates the attenuation of the pooled estimate toward the null as the two large trials enter the synthesis.

### 6.2 Group 2 — Preterm birth before 37 weeks' gestation (measure = OR)

This group comprises **k = 1** trial (n = 524) and is explicitly flagged `insufficient_data = true`. **It cannot be pooled.** No pooled effect size, confidence interval, p-value, τ², or I² is available or reported for this group. The single available standardized estimate is −0.371 (95% CI −0.544 to −0.198, n = 524). Readers should not treat this as a second, confirmatory meta-analytic result; it is one trial reported on a different effect-measure scale, kept separate precisely so that it is not silently merged with the RR-scale evidence.

---

## 7. Heterogeneity

Heterogeneity in Group 1 is **substantial and statistically significant**:

- **Cochran's Q = 14.742 on 5 degrees of freedom, p = 0.0115** — the null hypothesis of a common underlying effect is rejected.
- **I² = 86.23%** — approximately 86% of the observed variability in effect estimates is attributable to genuine between-study differences rather than sampling error. By conventional benchmarks this is "considerable" heterogeneity (I² > 75%).
- **τ² = 0.159037** — the estimated between-study variance on the pooling scale. The implied between-study standard deviation (≈0.40 on the log-RR scale) is of the same order as the pooled log-RR itself (ln 0.691 ≈ −0.37), meaning the dispersion of true effects is as large as the average effect.

A graphical summary of the heterogeneity diagnostics is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

The structural source of this heterogeneity is identifiable from the effect-size table: the near-null estimates from the two largest trials (−0.052 and +0.049) are mutually consistent with each other but statistically incompatible with the large protective estimates from the three small-to-moderate trials (−0.66, −0.61, −0.45), whose confidence intervals exclude the null in the protective direction. With I² at this level, the random-effects pooled mean should be interpreted as the centre of a wide distribution of effects rather than as an estimate of a single common treatment effect. The practical consequence is that the pooled RR of 0.691 is **model-dependent**: it sits well below the estimates of the trials that contribute 93% of the participants, precisely because random-effects weighting with a large τ² redistributes weight toward the smaller, more optimistic trials.

---

## 8. Moderators

No formal meta-regression or pre-specified subgroup analysis was executed in this pipeline run, and none is reported as a numerical result. With k = 6 comparisons, any moderator model would be severely underpowered (conventional guidance requires ≈10 studies per covariate), and estimates would be unstable. The following is therefore descriptive and hypothesis-generating only.

**Trial size / precision.** The clearest observable moderator-like pattern is the relationship between trial size and effect magnitude, visualised in the bubble chart at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. Effect magnitude decreases monotonically with increasing sample size across the five precisely estimated trials (n = 189 → −0.66; n = 190 → −0.61; n = 456 → −0.45; n = 4,589 → +0.05; n = 8,080 → −0.05). This is the canonical signature of small-study effects and is corroborated by the significant Egger test in §9. It is not a clinical moderator; it is a bias indicator.

**Moderators that could not be examined.** The following plausible effect modifiers could not be evaluated because the eligibility rules and extracted data did not support stratified analysis within this synthesis:

- *Baseline dietary calcium intake* — the mechanistic rationale predicts larger benefit in low-intake populations, but intake was not available as an extracted covariate.
- *Baseline pre-eclampsia risk* — if the preterm-birth effect is mediated through pre-eclampsia prevention, high-risk cohorts should show larger effects.
- *Gestational age at initiation of supplementation* — explicitly out of scope here, because the timing-stratified analyses of this same outcome were **excluded by protocol** to avoid double-counting the same randomised women. This means the present synthesis cannot speak to whether earlier initiation is more effective.
- *Exact dose above the 1 g/day threshold* (e.g. 1 g vs 1.5 g vs 2 g) and *co-supplementation* with other micronutrients.
- *Spontaneous versus medically indicated preterm birth* — a clinically critical distinction, since calcium's plausible pathway runs largely through iatrogenic preterm delivery for pre-eclampsia. The composite <37-week outcome conflates the two.

---

## 9. Publication Bias and Small-Study Effects

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | **−0.0381** |
| Egger's test p-value | **0.0141** |
| Trim-and-fill imputed studies (k₀) | **0** |
| Trim-and-fill adjusted estimate | **−0.311** (standardized scale; identical to unadjusted because k₀ = 0) |
| Overall small-study-effect risk rating | **High** |

**Egger's test is statistically significant (p = 0.0141)**, indicating funnel-plot asymmetry beyond what sampling variation would explain. This is consistent with small-study effects and supports the "high" risk rating: the pooled effect may be inflated by selective publication, selective outcome reporting, or other small-study phenomena (including lower methodological rigour, more homogeneous or higher-risk populations, and more intensive co-interventions in small single-centre trials).

**Trim-and-fill, in contrast, imputed no missing studies (k₀ = 0)**, so the bias-adjusted estimate is numerically identical to the original. This discordance between a significant Egger test and a null trim-and-fill is a well-recognised pattern rather than a contradiction: trim-and-fill has low sensitivity when asymmetry arises from heterogeneity or from a non-standard pattern of missingness, rather than from a clean, contiguous gap in one tail of the funnel. With I² = 86.23%, heterogeneity-driven asymmetry is a highly plausible explanation here, and the absence of imputed studies should **not** be read as reassurance that no bias exists.

Taken together with the size–effect gradient described in §8, the small-study-effect evidence suggests that **the pooled RR of 0.691 is likely to be an optimistic estimate of any true effect**, and that the near-null estimates of the two largest trials (−0.052 and +0.049) may be closer to the truth. The pooled estimate should be corroborated with bias-robust alternatives (PET-PEESE, selection models, limit meta-analysis) before any firm conclusion is drawn.

---

## 10. Discussion

This dose-stratified meta-analysis of six randomised comparisons (13,567 women) found a pooled Risk Ratio of 0.691 (95% CI 0.456–1.048, p = 0.0823) for preterm birth before 37 weeks with high-dose (≥1 g/day) antenatal calcium supplementation versus placebo or no calcium. The direction field attached to this result records that it favours **neither arm**: although the point estimate is below 1, the confidence interval includes the null and the result is not statistically significant at conventional thresholds.

Three features determine how this result should be read.

**First, the result is statistically inconclusive, not negative and not positive.** A confidence interval spanning RR 0.46 to RR 1.05 does not exclude a clinically important 54% relative reduction, nor does it exclude a null or marginally harmful effect. Framing this as "calcium reduces preterm birth" overstates the evidence; framing it as "calcium has no effect" understates the remaining uncertainty. With a p-value of 0.0823 the honest summary is that the trials to date have not resolved the question.

**Second, the pooled mean is an unreliable summary because of considerable heterogeneity.** I² = 86.23% with τ² = 0.159037 and Q = 14.742 (p = 0.0115) means the trials are not estimating a common effect. The approximate prediction interval (≈RR 0.20–2.4) makes the practical implication explicit: this evidence base does not permit a confident forecast of what a new high-dose trial would find. In such a setting, reporting only a pooled point estimate is misleading, and the dispersion of the underlying effects is itself a primary finding.

**Third, the pattern of results is strongly suggestive of small-study effects.** The two trials contributing 93.3% of randomised women both report near-null effects (−0.052 and +0.049), while the protective signal is driven entirely by trials of a few hundred participants. Egger's test formally confirms funnel asymmetry (p = 0.0141) and the overall small-study-effect risk is rated high. Under random-effects weighting with a large τ², the small optimistic trials receive disproportionate influence relative to their information content, which is the most parsimonious explanation for why the pooled RR (0.691) lies so far from the estimates of the large trials. A fixed-effect or precision-dominated analysis would be expected to sit much closer to the null.

**Biological interpretation.** The mechanistic case for a calcium effect on preterm birth runs mainly through prevention of hypertensive disorders and the consequent avoidance of medically indicated preterm delivery. If that is the dominant pathway, the magnitude of any preterm-birth benefit should be bounded by the magnitude of the pre-eclampsia benefit and by the proportion of preterm births that are iatrogenic — typically a minority. Against that background, a near-null effect on all-cause preterm birth in large trials is not biologically surprising, whereas the large effects (RR equivalents implying 40–50% reductions) in small trials are difficult to reconcile with the proposed mechanism. This mechanistic plausibility argument independently favours the large-trial estimates over the small-trial estimates.

**Relation to existing evidence.** Published reviews of antenatal calcium that pool across all doses, and that additionally include timing-stratified strata, typically report a modest reduction in preterm birth. The present analysis differs deliberately: it restricts to the ≥1 g/day stratum and admits only one analysis per trial per outcome, thereby avoiding the double-counting of participants that occurs when dose-stratified, timing-stratified, and overall analyses of the same outcome are treated as independent. The narrower, non-significant result reported here is a direct consequence of that stricter accounting, and suggests that some of the apparent precision in broader syntheses may reflect repeated use of the same randomised participants.

---

## 11. Data Quality & Validation Notes

The following data-handling and validation issues arose during this synthesis and are reported plainly:

1. **Effect-measure conflict requiring separate pooling.** The analysis was specified with the Risk Ratio as the effect measure (`effect_measure_source = explicit_user_request`). For one included trial (study_7_R7, n = 524) the source paper **explicitly reports an odds ratio**, not a risk ratio. The recorded conflict is: *"user requested RR, but the paper(s) explicitly report OR — user request kept as authoritative."* Because the measures differ, this trial was placed in its own effect-measure group and **was not combined** with the six RR-scale comparisons. The consequence is that one otherwise eligible trial contributes no information to the primary pooled estimate.
2. **One outcome group could not be pooled.** The OR-scale group contains **k = 1** trial and is flagged `insufficient_data`. No pooled effect, confidence interval, or heterogeneity statistic exists for it and none has been estimated.
3. **Analyses excluded to prevent double-counting.** Non-dose-stratified pooled analyses and timing-stratified ("started to take calcium before/after X weeks") analyses of the same preterm birth outcome were excluded by protocol as separate analyses. This prevents the same randomised women from entering the pooled estimate more than once, but it also reduces the number of contributing comparisons and removes the ability to examine timing as a moderator.
4. **Not-estimable trials excluded.** Trials reporting **zero preterm birth events in both arms** were treated as not estimable and excluded from pooling. No continuity correction was applied to force such trials into the analysis.
5. **Attrition from extraction to analysis.** Eleven study records entered extraction; 7 yielded an extractable high-dose estimate; 6 entered the primary pooled model. The gap between 11 and 7, and between 7 and 6, is accounted for by items 1, 3 and 4 above.
6. **Scale of reported study-level effects.** Individual study effects are displayed on a standardized (Hedges'-*g*-type) scale, whereas pooling for Group 1 was performed natively on the RR scale (`native_pooling_used = true`). Study-level standardized values and the pooled RR are therefore on different scales and should not be compared numerically; only the pooled RR is a confirmed native-scale result.
7. **Discordant bias diagnostics.** Egger's test is significant (p = 0.0141) while trim-and-fill imputes zero studies. Both results are reported; the discordance is not resolved and the overall small-study-effect risk is rated high.

---

## 12. Limitations

1. **Small number of comparisons.** Only k = 6 comparisons were poolable. With six studies, τ² is estimated imprecisely, I² has wide uncertainty, the power of Egger's test is low (making its significance here notable but its negative counterpart uninformative), and meta-regression is not feasible.
2. **Extreme weight concentration.** Two trials contribute 93.3% of randomised participants. The pooled estimate is therefore highly sensitive to the choice of model: random-effects weighting with τ² = 0.159 shifts influence toward small trials, and a precision-weighted analysis would yield a materially different (more null) result. No formal sensitivity analysis across models was run in this pipeline.
3. **High risk of small-study effects.** Formally significant funnel asymmetry (p = 0.0141) with a high overall risk rating means the pooled estimate may be inflated. Trim-and-fill provided no correction and no bias-robust alternative estimator (PET-PEESE, selection model) was fitted.
4. **Unexplained heterogeneity.** I² = 86.23% was not attributable to any examined covariate, because no moderator analysis was performed. Baseline dietary calcium intake, baseline pre-eclampsia risk, exact dose above 1 g/day, co-supplementation, and gestational age at initiation all remain unexamined.
5. **Outcome definition is a composite.** Preterm birth <37 weeks conflates spontaneous and medically indicated delivery, and includes late preterm births (34–36 weeks) that carry substantially lower morbidity than early preterm births. Effects on clinically severe preterm birth (<34 or <32 weeks) are not addressed.
6. **Effect-measure fragmentation.** One eligible trial reported odds ratios and was excluded from pooling, losing 524 participants' worth of information from the primary estimate.
7. **Risk of bias within trials not formally assessed.** No study-level risk-of-bias (e.g. RoB 2) assessment or GRADE certainty rating was computed in this pipeline. Allocation concealment, blinding, adherence/compliance with supplementation, and completeness of gestational-age ascertainment were not evaluated, and are plausible contributors to the observed heterogeneity.
8. **No individual participant data.** All analyses are aggregate-data; mediation through pre-eclampsia, and effect modification by baseline calcium intake, cannot be assessed without participant-level data.
9. **Scope restrictions by design.** By admitting only the dose-stratified high-dose comparison, this synthesis cannot comment on low-dose calcium, on timing of initiation, or on the dose–response relationship.

---

## 13. Conclusion

Pooling six randomised comparisons of high-dose calcium supplementation (≥1 g elemental calcium/day) versus placebo or no calcium in 13,567 pregnant women, the pooled **Risk Ratio (RR) for preterm birth before 37 weeks' gestation was 0.691 (95% CI 0.456 to 1.048; p = 0.0823; k = 6; REML random effects; native RR-scale pooling confirmed)**. In line with the direction field accompanying this result, the estimate favours **neither arm**: the confidence interval includes the null and the finding is not statistically significant.

Heterogeneity was considerable (**Q = 14.742, df = 5, p = 0.0115; I² = 86.23%; τ² = 0.159037**), and evidence of small-study effects was statistically significant (**Egger's p = 0.0141**, overall risk rated **high**), with trim-and-fill imputing no studies (k₀ = 0) and therefore providing no correction. The protective signal derives entirely from small-to-moderate trials, whereas the two trials contributing 93.3% of participants report near-null effects.

A second outcome group — the same outcome reported on the odds ratio scale — contained only one trial (n = 524) and is flagged as **insufficient data; it could not be pooled and no pooled value is reported**.

**Bottom line:** the current dose-stratified randomised evidence does **not** establish that high-dose antenatal calcium supplementation reduces preterm birth before 37 weeks. The point estimate is compatible with a meaningful benefit, but it is imprecise, highly heterogeneous, and vulnerable to small-study bias. Clinical recommendations for antenatal calcium should continue to rest on its better-established effect on hypertensive disorders of pregnancy rather than on an assumed preterm-birth benefit. Resolution requires large, adequately powered, pre-registered trials that report spontaneous and medically indicated preterm birth separately, stratify by baseline dietary calcium intake, and document adherence — ideally synthesised with individual participant data and bias-robust estimators.

---

## 14. Figures

| Figure | Content | Path |
|---|---|---|
| Figure 1 | Forest plot of study-level effects and pooled estimate | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Figure 2 | Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Figure 3 | Distribution of effect sizes across trials | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Figure 4 | Bubble chart (effect size vs. trial precision/size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Figure 5 | Heterogeneity diagnostics summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 15. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023.
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1–48.
4. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics*. 2005;30(3):261–293.
5. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine*. 2002;21(11):1539–1558.
6. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. *Journal of the Royal Statistical Society Series A*. 2009;172(1):137–159.
7. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
9. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
10. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
11. Stanley TD, Doucouliagos H. Meta-regression approximations to reduce publication selection bias. *Research Synthesis Methods*. 2014;5(1):60–78.
12. World Health Organization. *WHO Recommendations on Antenatal Care for a Positive Pregnancy Experience*. Geneva: WHO; 2016.
13. World Health Organization. *WHO Recommendation: Calcium Supplementation During Pregnancy for the Prevention of Pre-eclampsia and Its Complications*. Geneva: WHO; 2018.
14. Blencowe H, Cousens S, Oestergaard MZ, et al. National, regional, and worldwide estimates of preterm birth rates. *Lancet*. 2012;379(9832):2162–2172.

*Note on primary sources:* the individual randomised trials contributing to this synthesis are referred to by their pipeline identifiers (study_1_R1, study_3_R3, study_5_R5, study_6_R6, study_7_R7, study_9_R9, study_10_R10) because the extracted dataset supplied de-identified study labels rather than full bibliographic records. Full citations should be reinstated from the extraction log prior to journal submission.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| Preterm birth before 37 weeks' gestation | 6 | Risk Ratio (RR) | Yes | 0.6915 [0.4561, 1.0484] |
| Preterm birth before 37 weeks' gestation | 1 | Risk Ratio (RR) | Yes | -0.3707 (single study, not pooled) |
| | | ⚠ user requested RR, but the paper(s) explicitly report OR -- user request kept as authoritative | | |
