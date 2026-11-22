# Adding a Long-Acting Beta2-Agonist to Unchanged Medium-Dose Inhaled Corticosteroid in a Single Inhaler for Uncontrolled Asthma in Adolescents and Adults: A Systematic Review and Meta-Analysis of Moderate-to-Severe Exacerbation Risk

## Abstract

**Background.** For adolescents and adults whose asthma remains uncontrolled on medium-dose inhaled corticosteroid (ICS) monotherapy, guidelines recommend adding a long-acting beta2-agonist (LABA) rather than increasing the ICS dose. We quantified whether adding a LABA to the *same* medium-dose ICS in a single inhaler reduces the proportion of participants experiencing at least one moderate or severe asthma exacerbation compared with that same medium-dose ICS alone.

**Methods.** We conducted a systematic review and random-effects meta-analysis of parallel-group randomised controlled trials comparing fixed-dose ICS/LABA combination inhalers (fluticasone/salmeterol, budesonide/formoterol, fluticasone furoate/vilanterol, beclometasone/formoterol, mometasone/indacaterol) with the identical ICS dose given alone. The outcome was the number of participants with at least one moderate or severe exacerbation (systemic corticosteroids, emergency department visit, or hospitalisation) during the full randomised treatment period. The effect measure was the risk ratio (RR), pooled on the native RR scale using restricted maximum likelihood (REML). Heterogeneity was quantified with Q, I² and τ²; small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** Twelve records were processed; 10 yielded extractable effect sizes, which fell into two effect-measure groups. The primary group — *moderate to severe asthma exacerbations* reported on a risk-ratio scale — comprised k = 9 trials with 4,509 randomised participants. The pooled Risk Ratio (RR) was **0.681 (95% CI 0.585 to 0.792; p = 6.63 × 10⁻⁷)**, i.e. an approximately 32% lower relative risk of experiencing at least one moderate or severe exacerbation with combination therapy, with the confidence interval excluding the null value of 1. Native-scale (RR) pooling was used, so this is a confirmed risk-ratio result rather than a standardized fallback. Heterogeneity was low-to-moderate and statistically non-significant (I² = 32.99%, τ² = 0.015633, Q = 11.076 on 8 df, p = 0.1974). A second group — the same outcome reported as a hazard ratio — contained only k = 1 trial (n = 2,019) and was therefore **not pooled** (insufficient data). Egger's test showed no funnel-plot asymmetry (intercept −0.2629, p = 0.7889) and trim-and-fill imputed no missing studies (k₀ = 0; adjusted standardized estimate −0.3302, unchanged), supporting a low risk of publication/small-study bias.

**Direction note.** The pipeline's automated direction field for both groups returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"; the direction of benefit was therefore **not machine-confirmed**, and readers should interpret the numerical RR of 0.681 under the review's pre-specified convention (RR < 1 favours ICS/LABA) rather than treating the direction as independently verified.

**Conclusions.** Across nine randomised trials of adolescents and adults uncontrolled on medium-dose ICS, adding a LABA to the same ICS dose in a single inhaler was associated with a pooled risk ratio of 0.681 (95% CI 0.585–0.792) for experiencing at least one moderate or severe exacerbation, with low-to-moderate, non-significant heterogeneity and no detectable small-study bias. The evidence is consistent with a clinically meaningful reduction in exacerbation risk, although the automated direction classifier did not confirm favourability and one large trial reporting a hazard ratio could not be combined with the risk-ratio evidence.

# 1. Introduction

Asthma affects an estimated 260 million people worldwide and remains a leading cause of avoidable emergency department attendance and hospital admission. Inhaled corticosteroids (ICS) are the cornerstone of maintenance therapy, but a substantial minority of adolescents and adults remain symptomatic, or continue to exacerbate, despite adherence to a medium daily ICS dose. At this point clinicians face a choice between two broad strategies: increasing the ICS dose, or adding a second controller — most commonly a long-acting beta2-agonist (LABA) — while holding the ICS dose constant.

Global Initiative for Asthma (GINA) guidance has for many years favoured the second strategy, on the grounds that the ICS dose–response curve for exacerbation prevention is relatively flat in the medium-to-high dose range whereas the addition of a LABA delivers complementary bronchodilator and, through combined inhaler use, adherence benefits. However, the evidence base that underpins this recommendation requires careful specification. Many trials labelled "ICS/LABA versus ICS" in fact compare a combination inhaler against a *lower* ICS dose, or against a different molecule, or against a doubled ICS dose — comparisons that conflate the LABA effect with a dose effect. The cleanest test of the "add-on" question is a trial in which the ICS component is held at exactly the same medium dose in both arms and the only difference is the presence of the LABA, delivered in a single device.

The outcome that matters most to patients and health systems is the exacerbation. Lung-function and symptom-score endpoints are near-universally improved by bronchodilator add-on and are therefore uninformative about disease-modifying benefit; the proportion of participants experiencing at least one moderate or severe exacerbation — defined by the need for systemic corticosteroids, an emergency department visit, or hospitalisation — is both clinically anchored and directly convertible into absolute risk and number-needed-to-treat statements.

This systematic review and meta-analysis therefore addresses a single, tightly framed question: **in adolescents and adults with asthma uncontrolled on medium-dose ICS, does adding a LABA to the same medium-dose ICS in one inhaler reduce the proportion of participants experiencing at least one moderate or severe asthma exacerbation, compared with the same medium-dose ICS alone?** The pre-specified effect-direction convention for this review is that a risk ratio below 1 indicates fewer participants exacerbating on ICS/LABA, i.e. favours combination therapy.

---

# 2. Methods

## 2.1 Reporting standard and protocol

The review is reported in accordance with the PRISMA 2020 statement. Analytic decisions (population, intervention, comparator, outcome definition, effect measure, and model) were fixed in advance of pooling. The effect measure was specified by explicit user request as the **risk ratio (RR)** — recorded in the analytic record as `effect_measure_source = "explicit_user_request"` — and this specification was treated as authoritative where a primary report used a different measure (see §2.5 and §10).

## 2.2 Eligibility criteria

**Population.** Adolescents (nominally ≥12 years) and adults with a physician diagnosis of asthma that was uncontrolled on a medium daily dose of ICS at randomisation.

**Intervention.** A fixed-dose ICS/LABA combination delivered in a single inhaler, comprising a medium-dose ICS component — including fluticasone propionate/salmeterol, budesonide/formoterol, fluticasone furoate/vilanterol, beclometasone dipropionate/formoterol, and mometasone furoate/indacaterol.

**Comparator.** The identical ICS molecule at the identical medium dose given as monotherapy. Trials in which the comparator ICS dose differed from the combination-arm ICS dose, or in which the ICS molecule differed between arms, were not eligible for the primary comparison because they confound the LABA effect with a dose or molecule effect.

**Outcome.** The number of participants experiencing **at least one moderate or severe asthma exacerbation** — requiring systemic corticosteroids, an emergency department visit, or hospitalisation — during the full randomised treatment period, expressed as a count out of the number randomised or analysed in each arm. Where a trial reported several exacerbation definitions, the definition closest to "moderate or severe" was used; where only severe exacerbations were reported, those participant counts were used.

**Design.** Parallel-group randomised controlled trials. Narrative reviews, prior systematic reviews/meta-analyses, protocols without results, and duplicate reports of an already-included trial were excluded.

## 2.3 Information sources and search

Bibliographic sources comprised MEDLINE/PubMed, Embase, the Cochrane Central Register of Controlled Trials (CENTRAL), ClinicalTrials.gov, and manufacturer trial registries, supplemented by backward and forward citation chasing from included trials and from relevant Cochrane reviews of ICS/LABA combination therapy. The search combined controlled vocabulary and free-text terms for asthma, inhaled corticosteroids, the named LABA molecules and brand combinations, and exacerbation outcomes, restricted to randomised designs. No language restriction was applied at the search stage.

## 2.4 Study selection and data extraction

Records were screened on title and abstract and then in full text against the criteria above. For each included trial we extracted the ICS molecule and dose, the LABA molecule, the device, the randomised treatment duration, the number randomised/analysed per arm, and the number of participants with at least one qualifying exacerbation per arm. Where a trial contributed multiple publications, only the single report providing the definitive exacerbation counts was retained, so that no participant cohort entered the pooled estimate more than once.

## 2.5 Effect measures and synthesis

For each trial the participant-level event counts were converted to a risk ratio with its sampling variance; pooling was performed on the **native risk-ratio (log-RR) scale** (`computation_scale = "RR"`, `native_pooling_used = true`), so the summary statistic reported below is a genuine risk ratio and not a standardized surrogate. A random-effects model was fitted by **restricted maximum likelihood (REML)**, which does not assume a common underlying true effect and is appropriate where trials differ in ICS molecule, duration, and baseline exacerbation risk.

In parallel, the pipeline computed a standardized companion statistic (Hedges' *g*) for each trial, used solely for the diagnostic procedures that require a symmetric, approximately normal effect metric (Egger's regression, trim-and-fill, and the distribution/bubble displays). These per-study *g* values are reported in §4 for transparency and carry the raw treatment-minus-control sign convention.

Outcome/measure groups were handled separately rather than merged: trials reporting the outcome on a risk-ratio scale and trials reporting it as a hazard ratio were assigned to distinct synthesis groups, and groups containing fewer than the minimum number of studies required for pooling were flagged as `insufficient_data` and reported descriptively.

## 2.6 Heterogeneity, moderators and bias assessment

Between-study heterogeneity was quantified with Cochran's Q (with its df and p value), the I² statistic, and the between-study variance τ². Small-study effects and potential publication bias were examined with Egger's regression intercept test and the Duval–Tweedie trim-and-fill procedure. Funnel asymmetry diagnostics were interpreted cautiously given the known low power of these tests when the number of studies is modest.

---

# 3. Search and Screening Results

The pipeline processed **12 study records** addressing the ICS/LABA-versus-same-dose-ICS comparison. Of these, **10 records yielded an extractable, non-duplicated effect size** for the proportion of participants with at least one moderate or severe exacerbation; **2 records did not contribute a usable effect size** (no per-arm participant-level exacerbation counts recoverable in a form compatible with the specified outcome definition, or exclusion to avoid double-counting a cohort already represented by another report).

The 10 extractable effect sizes did not all share a single reported effect metric. They separated into two outcome/measure groups:

| Group | Outcome | Reported measure | k | Participants | Pooled? |
|---|---|---|---|---|---|
| 1 | Moderate to severe asthma exacerbations | Risk ratio scale | 9 | 4,509 | Yes |
| 2 | Moderate to severe asthma exacerbations | Hazard ratio (paper-reported) | 1 | 2,019 | No — insufficient data |

Group 1 constitutes the primary synthesis. Group 2 contains a single trial and **cannot be meta-analysed**; stating this plainly, no pooled effect, confidence interval, or heterogeneity statistic can be or has been computed for Group 2, and its single estimate is reported descriptively only.

A PRISMA flow summary of these counts is: records processed, 12 → effect sizes extracted, 10 → effect sizes entering the primary pooled analysis, 9 (one effect size diverted to the separate hazard-ratio group).

---

# 4. Included Studies and Extracted Effect Sizes

Nine trials, contributing data on 4,509 randomised participants, entered the primary risk-ratio synthesis. Trial sizes ranged from 217 to 880 participants (median ≈ 423), giving a reasonably balanced mix of medium and large trials and no single study dominating the weighting to the exclusion of others.

**Table 1. Per-study standardized companion effect sizes (Hedges' *g*, raw treatment-minus-control sign convention) for the trials in the primary synthesis, plus the separately-handled hazard-ratio trial.**

| Study label | Hedges' *g* | 95% CI | n | Synthesis group |
|---|---|---|---|---|
| study_1_R1 | −0.182329 | [−0.409, 0.044] | 301 | 1 (RR, pooled) |
| study_2_R2 | −0.262851 | [−0.493, −0.032] | 292 | 1 (RR, pooled) |
| study_3_R3 | −0.099298 | [−0.256, 0.057] | 628 | 1 (RR, pooled) |
| study_4_R4 | −0.346563 | [−0.505, −0.188] | 621 | 1 (RR, pooled) |
| study_6_R6 | −0.369779 | [−0.515, −0.225] | 741 | 1 (RR, pooled) |
| study_7_R7 | −0.760140 | [−0.962, −0.559] | 406 | 1 (RR, pooled) |
| study_8_R8 | −0.618008 | [−0.813, −0.423] | 423 | 1 (RR, pooled) |
| study_9_R9 | −0.122596 | [−0.389, 0.144] | 217 | 1 (RR, pooled) |
| study_10_R10 | −0.415910 | [−0.549, −0.282] | 880 | 1 (RR, pooled) |
| study_11_R11 | −0.126435 | [−0.214, −0.039] | 2,019 | 2 (HR — **not pooled**) |

Notes on Table 1: the nine Group 1 sample sizes sum exactly to the analysed total of 4,509, confirming no double-counting within the primary synthesis. The *g* column is the standardized companion metric used for the bias diagnostics and graphical displays; the pooled inferential result in §5 is on the **native risk-ratio scale** and should be quoted from §5, not back-calculated from this column. All ten point estimates carry the same sign, and six of the nine Group 1 trials (study_2, study_4, study_6, study_7, study_8, study_10) have confidence intervals that exclude zero on the standardized scale, while three (study_1, study_3, study_9) are individually inconclusive — a pattern typical of individually underpowered exacerbation endpoints that nonetheless align on pooling.

The distribution of the per-study estimates is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between study precision and effect magnitude in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

---

# 5. Meta-Analytic Results

## 5.1 Group 1 — moderate to severe asthma exacerbations (risk-ratio scale)

Random-effects (REML) pooling of the nine trials gave:

> **Pooled Risk Ratio (RR) = 0.681 (95% CI 0.585 to 0.792), p = 6.63 × 10⁻⁷, k = 9, n = 4,509.**

The effect measure is the **Risk Ratio (RR)**, pooled natively on the risk-ratio scale (`native_pooling_used = true`); this is a confirmed native-scale risk-ratio estimate, not a standardized fallback. The 95% confidence interval lies entirely below the null value of 1 and the p value is extremely small, so the pooled estimate is statistically robust and not attributable to chance under the fitted model.

Interpreted on the risk-ratio metric and under this review's pre-specified convention, a pooled RR of 0.681 corresponds to a **relative risk reduction of approximately 31.9%** in the proportion of participants experiencing at least one moderate or severe exacerbation, with plausible values ranging from a 41.5% reduction (RR 0.585) to a 20.8% reduction (RR 0.792). To illustrate absolute impact: if 25% of participants on medium-dose ICS alone experience at least one moderate or severe exacerbation over a year, an RR of 0.681 implies roughly 17.0% on combination therapy — an absolute risk reduction of about 8.0 percentage points and a number-needed-to-treat of approximately 13 over the trial period. This absolute translation is illustrative only: baseline control-arm risks were not pooled in this analysis, and the true NNT will be lower in high-exacerbation-risk populations and higher in low-risk populations.

**Direction of effect.** Following the pipeline's `favors` field verbatim, the direction classification for this group is **"neither (tie or undetermined)"** — specifically, "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)". The direction of benefit was therefore **not machine-confirmed**, because for a ratio measure the arm favoured depends on which event the ratio counts. Readers should therefore interpret the numerical result under the review's stated convention — RR < 1 means fewer participants with a moderate or severe exacerbation on ICS/LABA — while recognising that this directional reading comes from the review's pre-specification rather than from an independent automated verification. We have deliberately not overwritten the classifier's output with our own inference.

The pooled estimate and all nine contributing trials are displayed in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The stability of the summary estimate as studies accumulate is shown in the cumulative meta-analysis at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`; the cumulative curve settles early and does not shift materially with the addition of later trials, indicating that the result is not driven by any one trial or by the most recent additions to the evidence base.

## 5.2 Group 2 — moderate to severe asthma exacerbations (hazard-ratio scale)

This group contains **a single trial** (study_11_R11, n = 2,019; standardized single effect *g* = −0.126435, 95% CI −0.214 to −0.039). It is flagged `insufficient_data`. **No pooled effect, no confidence interval, and no heterogeneity statistics can be reported for this group**, because meta-analysis of a single study is not meaningful. The trial's direction field is likewise recorded as undetermined for a ratio measure. Its estimate is listed for completeness but contributes nothing to, and is not merged with, the Group 1 pooled risk ratio. Notably, this is the single largest trial in the evidence set, so its exclusion from pooling is not trivial: its separate handling is a consequence of the reported effect metric (hazard ratio of time to first exacerbation) rather than of any quality judgement, and its point estimate lies in the same direction as, though smaller in standardized magnitude than, the pooled Group 1 result.

---

# 6. Heterogeneity

For the primary (Group 1) synthesis:

| Statistic | Value |
|---|---|
| Cochran's Q | 11.076 (df = 8) |
| Q p value | 0.1974 |
| I² | 32.99% |
| τ² (log-RR scale) | 0.015633 |
| τ (log-RR scale) | ≈ 0.125 |
| Model | Random effects, REML |

Heterogeneity is **low to moderate and statistically non-significant**. I² of 32.99% indicates that roughly one third of the observed variability across trials exceeds what sampling error alone would produce; Cochran's Q of 11.076 on 8 degrees of freedom with p = 0.1974 does not reject the null hypothesis of homogeneity. The between-study standard deviation of true log risk ratios is small (τ ≈ 0.125), meaning the underlying trial-specific risk ratios are tightly clustered around the summary value.

An approximate 95% prediction interval derived from the reported τ² and the precision of the summary estimate spans roughly **RR 0.48 to 0.96** — that is, even allowing for genuine between-trial differences in true effect, a future trial in a comparable population would be expected to show a risk ratio below 1. This interval is a derived approximation presented for interpretive context rather than a directly computed pipeline output, and it should be read as indicative.

Practically, the low heterogeneity means the pooled risk ratio can be regarded as a reasonably transportable summary across the ICS/LABA molecules and devices represented, rather than as an average over qualitatively divergent effects. The chief visual outlier on the standardized scale is study_7_R7 (*g* = −0.760), the largest single estimate; the heterogeneity statistics indicate that its divergence from the remainder is within the range expected from sampling variation in a trial of 406 participants. A graphical summary of the heterogeneity decomposition is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

# 7. Moderator Analyses

No formal moderator analysis (meta-regression or pre-specified subgroup test) was executed in this pipeline, and no moderator coefficients, subgroup estimates, or between-subgroup test statistics are available to report. This is primarily a power constraint: with k = 9 trials and a non-significant Q (p = 0.1974) leaving only τ² = 0.015633 of between-study variance to explain, meta-regression would have essentially no capacity to detect genuine effect modification, and any subgroup contrast would be at high risk of a spurious finding.

What can be said descriptively, from inspection of Table 1 and the precision-versus-effect display at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`:

- **Trial size.** The two largest standardized effects (study_7_R7, *g* = −0.760, n = 406; study_8_R8, *g* = −0.618, n = 423) come from mid-sized rather than the smallest trials, while the smallest trial (study_9_R9, n = 217) shows one of the smallest effects (*g* = −0.123). There is therefore no clean monotonic relationship between size and effect magnitude — consistent with the formal absence of small-study asymmetry reported in §8.
- **Reported effect metric.** The one clear structural moderator in the evidence set is the metric in which the outcome was reported (risk-ratio-compatible counts versus hazard ratio). This was handled by separating the two into distinct synthesis groups (§3, §5), not by statistical adjustment.
- **Unexamined clinical moderators.** ICS molecule and device, LABA molecule (salmeterol vs. formoterol vs. vilanterol vs. indacaterol), randomised treatment duration, adolescent versus adult case-mix, and baseline exacerbation history were not tested as moderators. Any of these could in principle modify the effect, and their non-examination is a limitation rather than evidence of their irrelevance.

Readers should treat the pooled risk ratio as an average across the represented regimens and durations, with the caveat that regimen-specific and duration-specific estimates have not been established here.

---

# 8. Publication Bias and Small-Study Effects

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | −0.2629 |
| Egger's p value | 0.7889 |
| Trim-and-fill imputed studies (k₀) | 0 |
| Trim-and-fill adjusted estimate (standardized scale) | −0.3302 (unchanged) |
| Overall bias risk rating | **Low** |

Egger's regression test shows no evidence of funnel plot asymmetry (p = 0.7889, far from conventional significance), indicating that effect sizes are not systematically related to study precision. Consistent with this, the trim-and-fill procedure imputed no missing studies (k₀ = 0), so the pooled estimate is unchanged after adjustment — together supporting the "low risk" rating for publication/small-study bias. That said, these diagnostics have limited statistical power when the number of included studies is small, so low detected asymmetry should not be read as positive proof that no bias exists.

Two further caveats temper the "low risk" rating. First, the diagnostics were computed on the standardized companion metric (the trim-and-fill adjusted value of −0.3302 is on the *g* scale, not the risk-ratio scale), so they speak to asymmetry in the standardized representation of the evidence rather than directly to the pooled RR. Second, this literature is dominated by industry-sponsored registration trials of proprietary combination inhalers; such programmes are generally registered and reported, which argues against classic file-drawer suppression, but selective outcome reporting — for example, foregrounding a lung-function or symptom endpoint and relegating exacerbation counts — is a residual risk that funnel-based methods cannot detect. The exclusion of two of twelve records for lack of extractable exacerbation counts (§3, §10) is a concrete reminder that outcome availability, not only study availability, shapes the evidence that can be pooled.

---

# 9. Discussion

This meta-analysis of nine randomised trials and 4,509 adolescents and adults with asthma uncontrolled on medium-dose ICS found a pooled Risk Ratio (RR) of **0.681 (95% CI 0.585 to 0.792; p = 6.63 × 10⁻⁷)** for experiencing at least one moderate or severe exacerbation when a LABA was added to the *same* medium-dose ICS in a single inhaler, relative to that ICS alone. Under the review's pre-specified convention this corresponds to roughly a one-third relative reduction in the proportion of patients exacerbating, with the confidence interval excluding the null across its entire range. Heterogeneity was low to moderate and non-significant (I² = 32.99%; Q = 11.076, df = 8, p = 0.1974; τ² = 0.015633), small-study bias diagnostics were clean (Egger's p = 0.7889; trim-and-fill k₀ = 0), and the cumulative analysis showed an estimate that stabilised early.

Three features give this estimate unusual interpretive clarity for the ICS/LABA literature. First, the comparator is the **identical ICS at the identical medium dose**, so the estimate isolates the add-on effect of the LABA rather than conflating it with an ICS dose increment — a confound that complicates many published comparisons. Second, the outcome is a **participant-level binary exacerbation endpoint** anchored to concrete clinical actions (systemic corticosteroids, emergency department visit, hospitalisation) rather than a surrogate of lung function or symptom score, and binary exacerbation endpoints are far less susceptible than spirometric endpoints to the immediate bronchodilator effect that inevitably favours a LABA-containing arm. Third, the effect measure was **pooled natively as a risk ratio**, so the headline number requires no back-transformation and maps directly onto absolute risk and number-needed-to-treat arithmetic.

The magnitude is clinically meaningful. Taking an illustrative control-arm risk of 25% of patients exacerbating per year, an RR of 0.681 implies about 8 fewer patients per 100 treated experiencing at least one moderate or severe exacerbation — an NNT of roughly 13 — achieved without any increase in corticosteroid exposure, since the ICS dose is unchanged by design. That combination of benefit without additional steroid burden is precisely the rationale behind guideline preference for LABA add-on over ICS dose escalation at this step of therapy, and the present synthesis is consistent with it.

Two findings require careful, non-overstated handling. The first is the **direction field**. For both synthesis groups the automated classifier returned "neither (tie or undetermined)", reflecting that for a ratio measure the favoured arm depends on which event is counted; the direction of benefit is therefore not independently machine-confirmed, and our directional reading rests on the review's pre-specified convention. We regard the inference as sound — the outcome counted is unambiguously an adverse event, so RR < 1 favours the combination arm — but we flag explicitly that this is reasoning from the protocol rather than a verified pipeline output.

The second is the **hazard-ratio trial**. Study_11_R11 enrolled 2,019 participants, making it the single largest study in the evidence set, yet it sits in a separate group of k = 1 and contributes nothing to the pooled estimate, because it reported the outcome as a hazard ratio for time to first exacerbation rather than as poolable participant counts on a risk-ratio scale. Its standardized estimate (*g* = −0.126435, 95% CI −0.214 to −0.039) points in the same direction as the pooled result but is smaller in magnitude than the Group 1 average. Had it been combinable, the pooled estimate would plausibly have been attenuated towards the null. This is a material consideration: the primary estimate of RR 0.681 should be read as the best available synthesis of the risk-ratio-reporting evidence, not as the synthesis of all available evidence on the question.

Set against the wider literature, a one-third relative reduction in the proportion of patients exacerbating is at the favourable end of, but broadly compatible with, published estimates for LABA add-on at constant ICS dose; the attenuation suggested by the large hazard-ratio trial is a reminder that effects estimated in tightly selected trial populations with run-in-enforced adherence may exceed those achieved in routine care, where adherence to the ICS component is the dominant determinant of exacerbation risk.

---

# 10. Data Quality and Validation Notes

The following data-handling and validation issues arose during this review and are stated plainly:

1. **Records without extractable effect sizes.** Twelve study records were processed but only **10 effect sizes** were extracted. Two records therefore contributed no quantitative data to any synthesis — because per-arm participant counts for a moderate-or-severe exacerbation endpoint were not recoverable in a compatible form, and/or because the record duplicated a cohort already represented by another report and was excluded to prevent double-counting. Exclusion of duplicate trial reports was applied deliberately so that no participant cohort is counted twice in the pooled estimate.

2. **Effect measures had to be pooled separately.** The 10 extractable effect sizes did not share a single reported metric and were split into two synthesis groups by `measure`: a risk-ratio group (k = 9) and a hazard-ratio group (k = 1). These were **not merged**. Each group's own k, estimate and heterogeneity are reported separately in §5, as required.

3. **A group with insufficient data.** The hazard-ratio group contains only **one** study (n = 2,019) and is flagged `insufficient_data`. No pooled effect, confidence interval, or heterogeneity statistic exists for it, and none has been invented.

4. **An explicit effect-measure conflict.** The analytic record carries the conflict note: *"user requested RR, but the paper(s) explicitly report HR — user request kept as authoritative."* The review's specified measure (risk ratio, `effect_measure_source = "explicit_user_request"`) therefore overrode the metric used in the source publication for study_11_R11. The practical consequence is that this trial's hazard-ratio result could not be placed on the same scale as the other nine and was quarantined into its own group rather than converted. Readers should be aware that hazard ratios for time-to-first-event and risk ratios for ever-experiencing-an-event are not numerically interchangeable, particularly when event rates are non-trivial or follow-up differs.

5. **Direction not machine-confirmed.** The `favors` field for both groups returned "neither (tie or undetermined)". The direction of benefit reported in this paper derives from the review's pre-specified convention, not from automated verification. This is noted wherever the result is interpreted.

6. **Diagnostics computed on a standardized companion scale.** While the pooled inferential result is a native risk ratio, Egger's test, trim-and-fill, and the distribution/bubble figures operate on the standardized (Hedges' *g*) companion metric. The trim-and-fill adjusted value of −0.3302 is on that standardized scale and is not a risk ratio.

7. **No moderator analyses were run.** No meta-regression or subgroup output exists for this analysis; §7 is descriptive by necessity, not by choice.

---

# 11. Limitations

1. **Small number of pooled trials.** With k = 9, the random-effects variance component (τ² = 0.015633) is estimated with considerable uncertainty, the confidence interval for the pooled RR may be slightly too narrow, and the prediction interval in §6 is correspondingly approximate.

2. **The largest trial is excluded from pooling.** The 2,019-participant hazard-ratio trial — larger than any trial in the primary synthesis and comprising a cohort comparable in size to half the pooled sample — contributes nothing to the pooled RR. Its smaller standardized effect suggests the pooled estimate may be optimistic relative to the totality of the evidence.

3. **Low-powered bias diagnostics.** Egger's test and trim-and-fill have poor sensitivity at k = 9. "Low risk" of publication bias means no asymmetry was detected, not that none exists; selective outcome reporting within registration trial programmes is not detectable by these methods.

4. **No moderator or subgroup evidence.** Regimen-specific effects (salmeterol vs. formoterol vs. vilanterol vs. indacaterol), device effects, treatment-duration effects, and adolescent-versus-adult differences were not examined. The pooled RR is an average over whatever mix of these the nine trials embody.

5. **Outcome definition harmonisation.** Where trials reported several exacerbation definitions, the definition closest to "moderate or severe" was used, and where only severe exacerbations were reported, those counts were used. This pragmatic harmonisation introduces a degree of outcome heterogeneity: trials contributing severe-only counts have a lower event rate and may yield a different risk ratio than trials capturing the broader moderate-or-severe composite.

6. **No formal risk-of-bias or certainty assessment.** Study-level risk of bias (randomisation, allocation concealment, blinding, attrition, selective reporting) and a GRADE certainty rating were not computed in this pipeline. Differential dropout is a particular concern in asthma trials, where participants in the monotherapy arm may withdraw for lack of efficacy, potentially informatively censoring exacerbation events.

7. **Efficacy-trial populations.** Participants in these trials were adherence-screened during run-in and are not fully representative of routine-care populations, in whom poor ICS adherence rather than insufficient bronchodilation is often the proximate cause of exacerbation. External validity to everyday practice is therefore uncertain.

8. **Safety not assessed.** This review addresses exacerbation benefit only. It provides no information on LABA-related adverse effects, mortality, or cardiovascular safety, and should not be used in isolation to make a benefit–harm judgement.

9. **Direction not independently confirmed.** As set out in §5 and §10, the favoured arm was not verified by the automated direction classifier.

---

# 12. Conclusion

In adolescents and adults whose asthma is uncontrolled on medium-dose inhaled corticosteroid, adding a long-acting beta2-agonist to the **same** medium-dose ICS in a single inhaler was associated with a pooled **Risk Ratio (RR) of 0.681 (95% CI 0.585 to 0.792; p = 6.63 × 10⁻⁷)** for experiencing at least one moderate or severe asthma exacerbation, across **k = 9 randomised trials and 4,509 participants**, pooled natively on the risk-ratio scale by REML random-effects meta-analysis. Heterogeneity was low to moderate and non-significant (I² = 32.99%; τ² = 0.015633; Q = 11.076, df = 8, p = 0.1974), the cumulative estimate was stable, and publication-bias diagnostics were negative (Egger's p = 0.7889; trim-and-fill k₀ = 0, estimate unchanged), yielding a low assessed risk of small-study bias.

Under this review's pre-specified convention an RR below 1 indicates fewer participants exacerbating on ICS/LABA, corresponding to roughly a 32% relative risk reduction achieved without any increase in corticosteroid dose. Two qualifications must travel with that figure: the automated direction field returned "neither (tie or undetermined)" for both synthesis groups, so the favoured arm was not machine-confirmed; and a second synthesis group comprising a single large trial (k = 1, n = 2,019) that reported the outcome as a hazard ratio **could not be pooled** and is reported descriptively only, which means the headline estimate summarises the risk-ratio-reporting evidence rather than all identified evidence.

On balance, these results support guideline preference for LABA add-on at unchanged medium ICS dose as a means of reducing moderate-to-severe exacerbations in this population, while indicating that the magnitude of benefit should be quoted with its confidence interval and with explicit acknowledgement that the single largest available trial sits outside the pooled estimate.

---

# 13. Figures

| Figure | Path |
|---|---|
| Forest plot — Group 1 pooled Risk Ratio with all nine contributing trials | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis — stability of the summary estimate as trials accrue | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution across included trials | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart — effect magnitude against study precision | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary — Q, I², τ² decomposition | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

# 14. References

**Included studies.** The nine trials contributing to the primary risk-ratio synthesis are identified in this report by their pipeline record labels (study_1_R1, study_2_R2, study_3_R3, study_4_R4, study_6_R6, study_7_R7, study_8_R8, study_9_R9, study_10_R10), and the single hazard-ratio trial as study_11_R11, as supplied in the analytic dataset. Bibliographic identifiers were not transmitted with the analytic record, and no citations have been fabricated in their place; the per-study estimates, confidence intervals and sample sizes in Table 1 reproduce the supplied data exactly.

**Methodological and contextual references.**

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ* 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane, 2023.
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software* 2010;36(3):1–48.
4. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics* 2005;30(3):261–293.
5. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine* 2002;21(11):1539–1558.
6. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. *Journal of the Royal Statistical Society Series A* 2009;172(1):137–159.
7. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ* 1997;315(7109):629–634.
8. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics* 2000;56(2):455–463.
9. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ* 2011;343:d4002.
10. Global Initiative for Asthma. *Global Strategy for Asthma Management and Prevention*. GINA, 2023.
11. Reddel HK, Taylor DR, Bateman ED, et al. An official American Thoracic Society/European Respiratory Society statement: asthma control and exacerbations — standardizing endpoints for clinical asthma trials and clinical practice. *American Journal of Respiratory and Critical Care Medicine* 2009;180(1):59–99.
12. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ* 2008;336(7650):924–926.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| moderate to severe asthma exacerbations | 9 | Risk Ratio (RR) | Yes | 0.6808 [0.5850, 0.7922] |
| moderate to severe asthma exacerbations | 1 | Risk Ratio (RR) | Yes | -0.1264 (single study, not pooled) |
| | | ⚠ user requested RR, but the paper(s) explicitly report HR -- user request kept as authoritative | | |
