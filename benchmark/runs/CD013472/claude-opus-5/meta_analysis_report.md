# Music and Voice Interventions and Heart Rate During the Intervention Session in Preterm Infants: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Auditory interventions — recorded music, live music therapy, maternal singing and recorded parental voice or lullabies, delivered alone or in combination with kangaroo/skin-to-skin care — are widely used in neonatal intensive care units (NICUs) on the premise that they promote autonomic stability in preterm infants. Heart rate measured *while the stimulus is being delivered* is the most direct physiological index of that proposed effect, yet published syntheses have frequently merged during-session, post-session and follow-up measurements.

**Objective.** To quantify the effect of music or voice interventions versus standard care, the usual NICU environment, silence or no music on heart rate (bpm) recorded during the intervention session in infants born at <37 weeks' gestation.

**Methods.** Records identified by the review pipeline were screened against pre-specified PICO criteria. Only during-session heart rate was extracted (mean, SD, n per arm); final during-session values were preferred to change scores, and standard errors were converted to SDs as SE × √n. Effects were pooled on the native raw scale as a mean difference (MD) using a random-effects model with REML estimation of between-study variance; per-study standardized effects (Hedges' g) were computed for descriptive comparison. Heterogeneity was assessed with Q, I² and τ²; small-study effects with Egger's regression and trim-and-fill.

**Results.** Eleven studies entered data extraction, 7 yielded a usable during-session heart-rate effect size, and 6 studies (n = 284 infants) contributed the raw means, SDs and sample sizes required for native MD pooling. The pooled Mean Difference (MD) was **+1.15 bpm (95% CI −5.54 to 7.85; p = 0.7356)**, a non-significant result that nominally favours *standard care / usual NICU environment / silence / no music*. Heterogeneity was substantial to considerable: Q = 27.812 (df = 5, p < 0.001), I² = 86.9%, τ² = 56.164 bpm² (τ ≈ 7.5 bpm), with per-study Hedges' g ranging from −0.90 to +1.98 and effects in both directions. Egger's test was non-significant (intercept 1.216, p = 0.4636) and trim-and-fill imputed one study (k₀ = 1, adjusted estimate 0.3764); publication-bias risk was nonetheless rated **moderate** because of low test power at k = 6.

**Conclusions.** Across the pooled evidence there is no confirmed difference in during-session heart rate between music/voice interventions and standard care in preterm infants, and the direction of the point estimate nominally favours the control condition. However, the confidence interval is wide, heterogeneity is considerable, and individual trials report large effects in opposite directions, so the pooled null should be read as an unresolved rather than a settled question. Larger, protocol-standardized trials reporting during-session physiology separately from post-session recovery are required.


## 1. Introduction

Preterm infants (<37 weeks' gestation) spend their first weeks in an acoustic environment that differs radically from the intrauterine one: alarms, ventilators, telephones and staff conversation produce sound-pressure levels that routinely exceed recommended NICU thresholds, while the biologically expected signal — the maternal voice — is largely absent. Structured auditory interventions have therefore become one of the most widely adopted non-pharmacological supportive therapies in neonatology. These interventions span a heterogeneous family: pre-recorded instrumental or vocal music, live music therapy delivered by a credentialled therapist, live maternal or paternal singing, and recorded parental voice or lullabies, each sometimes combined with kangaroo mother care (skin-to-skin holding).

The dominant physiological rationale is autonomic: by providing a predictable, rhythmic, low-intensity auditory stimulus, music or voice is hypothesised to shift autonomic balance toward parasympathetic predominance, producing a measurable reduction in heart rate, more stable respiration and improved behavioural state. Heart rate is the most frequently reported outcome in this literature because it is continuously monitored, objectively captured and clinically meaningful — sustained tachycardia in preterm infants reflects stress and increases metabolic demand at a time when energy is needed for growth.

A methodological issue has nevertheless clouded the evidence base. Heart rate is reported at several distinct timepoints — baseline, during the stimulus, immediately after it, and at delayed follow-up — and these timepoints answer different questions. The *during-session* value tests whether the stimulus itself acutely modulates autonomic tone; post-session values test carry-over or recovery. Previous syntheses have often pooled these timepoints together, or pooled heart rate with oxygen saturation, respiratory rate, pain scores and behavioural state into a single "physiological stability" construct, which obscures the direct question.

This review therefore addresses a single, deliberately narrow question: **in preterm infants, what is the effect of music or voice interventions, compared with standard care, usual NICU environment, silence or no music, on heart rate in beats per minute measured during the intervention session?** Oxygen saturation, respiratory rate, pain, weight gain, length of stay, sleep, feeding and neurodevelopmental outcomes were explicitly not pooled, and heart rate recorded before, immediately after, or later than the session was not used.

### Direction-of-effect convention

Two sign conventions appear in this report and must be distinguished:

- **Per-study standardized effects (Hedges' g).** A **positive g indicates that the intervention produced a LOWER heart rate during the session than standard care**, i.e. g > 0 favours music/voice.
- **Pooled native-scale effect (Mean Difference, bpm).** The MD retains the raw statistical convention **treatment minus control**, so a **negative MD (< 0 bpm) corresponds to a lower heart rate with music** and favours the intervention, whereas a **positive MD corresponds to a higher heart rate in the music arm** and nominally favours the control condition.

Accordingly, the pooled MD and the per-study g values carry *opposite* signs for the same underlying direction. Throughout, the arm favoured by the pooled result is reported using the analysis engine's explicit `favors` field rather than inferred from the sign.

---

## 2. Search and Screening

### 2.1 Information sources and eligibility

The review followed PRISMA 2020 reporting principles. Records were assembled by the automated retrieval and screening pipeline and assessed against the following pre-specified PICO framework:

| Element | Criterion |
|---|---|
| **Population** | Infants born at <37 weeks' gestation, studied in a neonatal unit |
| **Intervention** | Music or voice intervention — recorded music, live music therapy, live singing, parental voice or lullaby — with or without kangaroo/skin-to-skin care |
| **Comparator** | Standard care, usual NICU environment, silence, or no music |
| **Outcome** | Heart rate (bpm) recorded **during** the intervention session |
| **Design** | Controlled comparative designs (randomised, cross-over or quasi-experimental) reporting mean, SD and n per arm |

Exclusion criteria were: term-born populations; no concurrent or within-subject control condition; heart rate reported only at baseline, immediately post-session, or at delayed follow-up; and reports providing no extractable dispersion statistic.

### 2.2 Screening outcome

Eleven studies passed full-text screening and entered data extraction. Of these:

- **7 studies** yielded a computable during-session heart-rate effect size (`study_1`, `study_2`, `study_3`, `study_4`, `study_6`, `study_10`, `study_11`);
- **4 studies** (`study_5`, `study_7`, `study_8`, `study_9`) were retained in the review but contributed **no** poolable during-session heart-rate datum, because the reported heart-rate values corresponded to an ineligible timepoint, were presented graphically only, or lacked a usable measure of dispersion;
- **6 studies** (n = 284 infants) supplied the complete raw inputs — arm-level means, SDs and sample sizes — required for pooling on the native mean-difference scale. One further study (`study_4`, n = 17) produced a standardized effect size but lacked the raw inputs needed for native MD pooling and was therefore excluded from the primary pooled estimate (see §9, Data Quality & Validation Notes).

### 2.3 Data extraction rules

Extraction was restricted to heart rate measured while the auditory stimulus was being delivered. Where both final during-session values and change-from-baseline values were reported, **final during-session values were preferred**; where only change scores were available, change scores were used for *both* arms and the record flagged. Standard errors or SEMs were converted to standard deviations as **SD = SE × √n**. No imputation of missing SDs from other studies was performed; records without a recoverable dispersion statistic were left unpooled rather than imputed.

---

## 3. Included Studies

Bibliographic identifiers were not carried through the extraction layer of this pipeline, so included studies are designated by their pipeline identifiers (`study_1`–`study_11`). Characteristics relevant to the analysis are summarised below for the seven studies with a computable during-session heart-rate effect.

| Study ID | Total n (both arms) | Hedges' g (during-session HR) | 95% CI for g | Contributed to native MD pool |
|---|---|---|---|---|
| `study_1_R1` | 40 | +1.975 | 1.219 to 2.731 | Yes |
| `study_2_R2` | 62 | +0.165 | −0.334 to 0.664 | Yes |
| `study_3_R3` | 34 | −0.682 | −1.374 to 0.009 | Yes |
| `study_4_R4` | 17 | −0.198 | −1.153 to 0.756 | **No** (raw inputs unavailable) |
| `study_6_R6` | 60 | +0.029 | −0.477 to 0.535 | Yes |
| `study_10_R10` | 18 | −0.899 | −1.868 to 0.071 | Yes |
| `study_11_R11` | 70 | +0.946 | 0.452 to 1.441 | Yes |

Total sample across all seven effect sizes: **301 infants**; total sample in the primary pooled analysis: **284 infants** across **6 studies**. Sample sizes per study were small to moderate (range 17–70, median 40), which is typical of NICU physiological trials and has direct consequences for precision and for the power of bias diagnostics.

The intervention family itself was heterogeneous by design, spanning recorded music, live music therapy, live and recorded parental singing, and lullaby delivery, with some protocols layered on kangaroo/skin-to-skin care. Comparators likewise ranged from fully "usual NICU environment" (ambient noise unchanged) to deliberately imposed silence or headphone-without-sound conditions. This clinical and methodological diversity was anticipated to be a principal driver of statistical heterogeneity, and it is.

---

## 4. Effect Sizes

### 4.1 Per-study standardized effects

Per-study standardized mean differences were computed as Hedges' g with the small-sample correction applied, using the convention that **g > 0 denotes a lower during-session heart rate under music/voice**. The seven available effects were:

**+1.975, +0.946, +0.165, +0.029, −0.198, −0.682, −0.899**

Several features are immediately apparent:

1. **Effects run in both directions.** Three studies point toward a lower heart rate with music (g > 0 appreciably), three point toward a *higher* heart rate with music (g < 0), and one is essentially null (g = +0.029).
2. **Only two confidence intervals exclude zero**, both favouring the intervention: `study_1` (g = +1.975, 95% CI 1.219 to 2.731) and `study_11` (g = +0.946, 95% CI 0.452 to 1.441). `study_3` (g = −0.682, 95% CI −1.374 to 0.009) and `study_10` (g = −0.899, 95% CI −1.868 to 0.071) approach but do not cross the conventional threshold in the opposite direction.
3. **Magnitude is inversely related to precision.** The largest absolute effects come from among the smaller samples (`study_1`, n = 40; `study_10`, n = 18), while the three largest studies (`study_11`, n = 70; `study_2`, n = 62; `study_6`, n = 60) span g = +0.946 to +0.029 — one large and two essentially null.

The distribution of effect sizes is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, which shows a dispersed, non-unimodal spread rather than a tight cluster around a common value.

### 4.2 Native-scale pooling

Because the review question is framed in clinically interpretable units (bpm), the primary synthesis was performed on the **native mean-difference scale**. The effect measure was set to MD by explicit specification (`effect_measure_source = explicit_user_request`) and **native pooling was successfully used** (`native_pooling_used = true`) — that is, the pooled value reported below is a genuine mean difference in beats per minute computed from arm-level means and SDs, not a standardized fallback. Native MD pooling required raw arm-level inputs, which were available for 6 of the 7 studies.

---

## 5. Meta-Analytic Result

A single outcome/timepoint group was analysed (during-session heart rate); no separate `meta_analysis_groups` were present, so one pooled estimate is reported.

| Quantity | Value |
|---|---|
| Effect measure | **Mean Difference (MD)**, bpm |
| Model | Random effects, REML between-study variance estimation |
| Studies pooled (k) | **6** |
| Infants (n) | **284** |
| **Pooled Mean Difference (MD)** | **+1.1535 bpm** |
| 95% confidence interval | **−5.542 to 7.849 bpm** |
| p-value | **0.7356** |
| Favours (per `favors` field) | **Standard care / usual NICU environment / silence / no music** |
| τ² | 56.164 bpm² |
| I² | 86.9% |
| Q (df = 5) | 27.812, p < 0.001 |

**Interpretation.** The pooled Mean Difference of **+1.15 bpm (95% CI −5.54 to 7.85; p = 0.7356)** is statistically indistinguishable from zero. In the raw treatment-minus-control convention, a positive MD corresponds to a *higher* heart rate in the music/voice arm, and the analysis engine's direction field accordingly records the point estimate as nominally favouring **standard care / usual NICU environment / silence / no music**. This must, however, be stated with the appropriate strength: the result is not statistically significant, the interval comfortably contains zero and extends roughly 5.5 bpm in the direction favouring music and 7.8 bpm in the direction favouring control, and the magnitude of the point estimate (about one beat per minute) is far below any plausible threshold of clinical importance in a population whose normal heart rate is 120–160 bpm. The honest reading is therefore **no confirmed difference in during-session heart rate**, with a point estimate that leans trivially toward the control condition.

The forest plot is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. A cumulative meta-analysis, which shows how the pooled estimate evolves as studies accumulate, is at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`; it illustrates that the summary estimate has not stabilised and remains sensitive to the inclusion of individual studies.

**Precision.** Back-calculating from the confidence limits, the standard error of the pooled MD is approximately 3.42 bpm; the corresponding test statistic is z ≈ 0.34, consistent with the reported p = 0.7356. A 95% prediction interval — the interval within which the true effect of a *new* study would be expected to fall — is approximately **−22 to +24 bpm**, which is the single most informative number in this report: the between-study variance is so large that the model cannot predict even the *direction* of effect in a future trial.

---

## 6. Heterogeneity

Heterogeneity was **considerable** by any conventional benchmark:

- **Cochran's Q = 27.812 on 5 degrees of freedom, p < 0.001** — the null hypothesis of a common underlying effect is decisively rejected.
- **I² = 86.9%** — approximately 87% of the observed variability in effect estimates reflects genuine between-study differences rather than within-study sampling error. Under the Cochrane classification this falls in the "considerable heterogeneity" band (75–100%).
- **τ² = 56.164 bpm²**, i.e. **τ ≈ 7.49 bpm**. The standard deviation of true effects across studies is roughly seven and a half beats per minute — several times the magnitude of the pooled point estimate itself.

A visual summary of the heterogeneity diagnostics is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

The practical consequence is that the random-effects summary should not be interpreted as "the" effect of music on preterm heart rate. With τ ≈ 7.5 bpm and effects ranging from a substantial reduction (`study_1`, g = +1.98) to a substantial increase (`study_10`, g = −0.90) in heart rate during the session, the studies are better described as estimating *different* effects in different settings than as noisy estimates of a shared one. Averaging them produces a number that describes no individual study well.

Plausible sources of this dispersion include:

1. **Intervention type and intensity** — live music therapy titrated in real time to infant cues is a fundamentally different exposure from a fixed-volume recorded lullaby played through a speaker, and the two may plausibly have opposite autonomic consequences if the recorded condition adds sound energy to an already noisy environment.
2. **Co-intervention with kangaroo/skin-to-skin care** — skin-to-skin holding itself alters heart rate, so protocols layering music on kangaroo care confound two active exposures and may show effects attributable to either.
3. **Comparator definition** — comparing music with imposed silence is a far stronger contrast than comparing it with the usual NICU soundscape, and the two comparators are not exchangeable.
4. **Baseline state and gestational age** — autonomic responsiveness matures with postmenstrual age, and an infant studied asleep at 34 weeks is not comparable to one studied awake at 28 weeks.
5. **Measurement window and summarisation** — "during the session" encompasses windows from a few minutes to over an hour, averaged in different ways.
6. **Design** — cross-over/within-subject designs and parallel-group designs carry different correlation structures and were analysed on the same scale here.

---

## 7. Moderator Analyses

Formal moderator analysis was **not undertaken as an inferential exercise**, and no meta-regression coefficients are reported, for a straightforward reason: with **k = 6 studies** in the pooled analysis, the available degrees of freedom cannot support meta-regression. Standard guidance recommends a minimum of approximately ten studies per covariate; fitting even a single moderator here would produce an estimate with essentially no power and a high risk of spurious findings, and subgroup analyses would reduce to comparisons of two or three studies each.

A descriptive exploration of the relationship between study size and effect magnitude is presented in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. The pattern visible there is descriptive only and should not be treated as a tested association: the two largest absolute effects (`study_1`, g = +1.975, n = 40; `study_10`, g = −0.899, n = 18) arise from comparatively small samples, while the two largest studies (`study_11`, n = 70; `study_2`, n = 62) and the third-largest (`study_6`, n = 60) span one moderate positive effect and two near-null effects. This is the classic visual signature of either small-study effects or genuine effect modification by study-level features that co-vary with sample size, and the present data cannot distinguish between those explanations.

Candidate moderators that *should* be examined when a larger evidence base becomes available — intervention modality (live vs recorded; music vs voice), presence of kangaroo care, comparator type (silence vs usual environment), gestational age at study, behavioural state at measurement, session duration, and design (cross-over vs parallel) — are listed here as a research agenda, not as analyses performed.

---

## 8. Publication Bias and Small-Study Effects

Two diagnostics were applied, both acknowledged to be underpowered at k = 6.

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | **1.216** |
| Egger's test p-value | **0.4636** |
| Trim-and-fill imputed studies (k₀) | **1** |
| Trim-and-fill adjusted estimate | **0.3764** |
| Overall risk rating | **Moderate** |

Egger's regression test showed no statistically significant funnel-plot asymmetry (intercept 1.216, p = 0.4636), and the trim-and-fill procedure imputed only a single hypothetical missing study (k₀ = 1), with an adjusted estimate of 0.3764 — that is, the pooled estimate would be essentially unchanged, and would remain non-significant and trivially small, after adjustment. Taken at face value, these results provide **no positive evidence of small-study effects or publication bias** in this body of literature.

The **"moderate" risk rating is nevertheless appropriate**, and should not be read as contradicting the statistics above. Egger's test has low statistical power when fewer than roughly ten studies are pooled, so a non-significant result cannot establish the *absence* of bias; with k = 6 the test is close to uninformative. Similarly, trim-and-fill behaves erratically in small, highly heterogeneous datasets, and with I² = 86.9% the funnel plot's asymmetry is dominated by true between-study variance rather than by selection processes. The correct summary is that **publication bias is not detected here but cannot be confidently excluded**: the findings are *consistent with*, rather than *proof of*, an unbiased evidence base.

One further consideration cuts in the opposite direction from the conventional expectation. Because the pooled result is null, the usual concern — that selective publication of favourable results inflates the summary effect — is less pressing; if anything, selective publication in this field would be expected to favour positive (heart-rate-lowering) results, and the observed pooled estimate shows none. The more material threat to validity here is the unavailability of extractable during-session data from four of the eleven included studies (§9), which is a form of selective *reporting* within studies rather than selective publication of studies.

---

## 9. Data Quality & Validation Notes

The following issues were flagged during data handling and are reported plainly rather than smoothed over:

1. **One study excluded from the primary pooled estimate for lacking raw inputs.** `study_4` (n = 17; Hedges' g = −0.198, 95% CI −1.153 to 0.756) produced a computable standardized effect but did not supply the arm-level means, SDs and sample sizes required for pooling on the native mean-difference scale. It was therefore excluded from native MD pooling (engine note: *"1 row(s) excluded from native MD pooling for lacking raw inputs: ['study_4']"*). The primary analysis consequently rests on **k = 6 of the 7** available effect sizes and 284 of the 301 extracted infants. Given that `study_4` was small and near-null, its exclusion is unlikely to have materially shifted the pooled estimate, but the discrepancy between "7 effect sizes" and "k = 6" is attributable entirely to this exclusion and should be understood as such.

2. **Four of eleven included studies contributed no poolable outcome.** `study_5`, `study_7`, `study_8` and `study_9` passed eligibility screening but yielded no extractable during-session heart-rate mean with dispersion. They are counted in the review but not in the analysis. This is a substantial attrition of information (36% of included studies) and is the principal reporting-quality limitation of this synthesis.

3. **Effect-measure specification.** The effect measure (MD) was set by explicit user specification rather than inferred from the data, and native pooling on that scale was confirmed (`native_pooling_used = true`). The pooled value is therefore a genuine native-scale mean difference in bpm and **not** a standardized fallback. Per-study Hedges' g values are reported alongside it for descriptive comparability only; the pooled statistic should be named **Mean Difference (MD)** and must not be described as Hedges' g.

4. **Sign-convention mismatch between tables.** As set out in §1, per-study g values and the pooled MD carry opposite signs for the same clinical direction. Readers comparing the study-level table in §3 with the pooled result in §5 should take care not to read the discrepancy as an inconsistency in the data.

5. **Change-score handling.** The extraction protocol permitted change-from-baseline values to substitute for final during-session values where the latter were unavailable, with such records flagged. Mixing final and change scores on a common MD scale is defensible when baseline is balanced but introduces additional between-study variance and may contribute to the observed τ².

6. **Within-subject designs analysed on a between-group scale.** Several NICU music studies use cross-over or own-control designs. Where such data were pooled using between-arm means and SDs without accounting for within-subject correlation, the resulting standard errors are conservative (too wide) and the study is underweighted. This is a known limitation of the extraction schema applied here.

---

## 10. Discussion

This meta-analysis addressed a deliberately precise question — heart rate measured *while* music or voice is being delivered to preterm infants — and returned a precise answer that is also a negative one. Across six studies and 284 infants, the pooled Mean Difference was **+1.15 bpm (95% CI −5.54 to 7.85; p = 0.7356)**, nominally favouring standard care but statistically and clinically indistinguishable from no effect.

Three observations shape the interpretation.

**First, the null is not a well-estimated null.** A confidence interval spanning roughly 13 bpm, and a prediction interval spanning roughly 46 bpm, do not exclude effects that would be clinically meaningful in either direction. This is an *uninformative* result rather than a demonstration of equivalence. A 5 bpm reduction in heart rate sustained across a session would be a worthwhile physiological benefit in a growing preterm infant, and the data neither establish nor refute it.

**Second, the heterogeneity is the finding.** I² = 86.9% and τ ≈ 7.5 bpm, with individual studies reporting large effects in opposite directions, indicate that "music or voice intervention" is not a single exposure. Live, contingent, therapist- or parent-delivered singing titrated to the infant's state is mechanistically distinct from a recorded track played at fixed volume; adding sound to an already overstimulating environment could plausibly *raise* heart rate in some infants while contingent live voice lowers it in others. The two studies with the clearest heart-rate-lowering effects (`study_1`, g = +1.975; `study_11`, g = +0.946) and the two leaning toward heart-rate elevation (`study_10`, g = −0.899; `study_3`, g = −0.682) may well be measuring genuinely different interventions in genuinely different populations. Pooling them yields an average of incommensurables. Until the evidence base is large enough to stratify by modality, comparator and co-intervention, the summary estimate should carry little weight in clinical decision-making relative to the underlying dispersion.

**Third, the restriction to during-session measurement matters.** Much of the clinical enthusiasm for NICU music therapy rests on outcomes other than acute autonomic change — behavioural state organisation, feeding efficiency, parental bonding, reduced length of stay, and post-session calming. None of those were eligible here, and nothing in this analysis speaks against them. It is entirely coherent for an intervention to have no measurable effect on heart rate *during* delivery while still producing benefits in recovery, sleep or parent–infant interaction. The present result constrains one specific mechanistic claim — that music acutely slows the preterm heart while playing — and constrains it weakly.

Set against the wider literature, this finding sits on the more conservative side. Earlier syntheses of music therapy in neonatal care have frequently reported favourable pooled effects on physiological stability, but those analyses typically combined timepoints and outcomes, included term infants, or pooled standardized effects across heterogeneous measures. The narrower lens applied here — one outcome, one timepoint, one population, native-scale pooling — removes much of the apparent signal, which is itself informative about how that signal was generated.

---

## 11. Limitations

1. **Very small number of pooled studies.** With k = 6, the between-study variance estimate (τ² = 56.164) is itself imprecise, the random-effects confidence interval is likely anti-conservative despite its width, and meta-regression is infeasible.
2. **Loss of eligible data.** Four of eleven included studies, plus one further study with a computable g, contributed nothing to the primary estimate (§9). A synthesis using 6 of 11 studies is vulnerable to the possibility that the unavailable data differ systematically from the available data.
3. **Unexplained considerable heterogeneity.** I² = 86.9% is left unexplained because the dataset cannot support moderator analysis. No subgroup, sensitivity or leave-one-out inference is offered beyond the descriptive cumulative plot.
4. **Clinical and methodological diversity treated as a single exposure.** Recorded music, live music therapy, parental singing and lullabies, with and without kangaroo care, were pooled; comparators ranged from imposed silence to the unmodified NICU soundscape.
5. **Risk of bias in included studies not formally assessed.** No RoB 2 / ROBINS-I domain-level appraisal was available at the analysis layer. Blinding of an auditory intervention is intrinsically difficult, outcome assessment via automated monitors mitigates but does not eliminate detection bias, and allocation concealment in small single-centre physiological studies is frequently unreported.
6. **Design heterogeneity not modelled.** Cross-over and parallel designs were pooled on the same scale without adjustment for within-subject correlation (§9, item 6).
7. **Mixed outcome definitions.** Final during-session and change-from-baseline values were both admissible, and SE-to-SD conversion (SE × √n) was applied where necessary; both introduce additional variance.
8. **Publication-bias diagnostics underpowered.** Egger's test (p = 0.4636) and trim-and-fill (k₀ = 1) are reassuring in appearance but near-uninformative at k = 6 with I² = 86.9%; the moderate risk rating reflects this.
9. **Bibliographic opacity.** Included studies are identified by pipeline identifier rather than citation, limiting independent verification of extraction decisions at the study level.
10. **Single outcome, single timepoint.** By design, no conclusions can be drawn about oxygen saturation, respiratory rate, pain, growth, sleep, feeding, length of stay or neurodevelopment, nor about heart rate after the session ends.

---

## 12. Conclusion

In preterm infants, pooled evidence from six studies (284 infants) shows **no confirmed difference in heart rate measured during the intervention session** between music or voice interventions and standard care, the usual NICU environment, silence or no music. The pooled **Mean Difference was +1.15 bpm (95% CI −5.54 to 7.85; p = 0.7356)**; by the analysis engine's direction field this point estimate nominally **favours standard care / usual NICU environment / silence / no music**, but it is not statistically significant and is clinically negligible in magnitude. Heterogeneity was considerable (I² = 86.9%; τ² = 56.164 bpm²; Q = 27.812, df = 5, p < 0.001), with individual studies reporting substantial effects in both directions, so the summary estimate describes no single study well and the 95% prediction interval cannot even specify the direction of effect in a future trial. Publication-bias diagnostics were non-significant (Egger's p = 0.4636; trim-and-fill k₀ = 1, adjusted estimate 0.3764) but underpowered, and risk was rated moderate.

Clinically, these data provide **no support for the specific claim that music or voice acutely lowers preterm heart rate while it is being delivered**, and equally no evidence of acute autonomic harm. They do not bear on the broader rationale for music therapy in the NICU — behavioural state, parental involvement, feeding and post-session calming were outside scope. For research, the priorities are clear: adequately powered trials that (i) report during-session physiology separately from post-session recovery, (ii) specify and standardise intervention modality (live vs recorded; music vs voice; with vs without kangaroo care), (iii) define the comparator explicitly in terms of measured ambient sound, (iv) publish arm-level means and SDs so that native-scale pooling is possible, and (v) pre-register the heart-rate measurement window. Until such trials exist, the honest statement is that the effect of music and voice on during-session heart rate in preterm infants remains **unresolved rather than absent**.

---

## Figures

| Figure | Path |
|---|---|
| Forest plot (pooled MD, k = 6) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect size vs study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. *Introduction to Meta-Analysis*. 2nd ed. Chichester: Wiley; 2021.
4. Hedges LV. Distribution theory for Glass's estimator of effect size and related estimators. *J Educ Stat*. 1981;6(2):107–128.
5. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
6. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
7. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
9. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
10. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
11. Standley JM. A meta-analysis of the efficacy of music therapy for preterm infants. *J Pediatr Nurs*. 2002;17(2):107–113.
12. Hodges AL, Wilson LL. Effects of music therapy on preterm infants in the neonatal intensive care unit. *Altern Ther Health Med*. 2010;16(5):72–77.
13. van der Heijden MJE, Oliai Araghi S, Jeekel J, Reiss IKM, Hunink MGM, van Dijk M. Do hospitalized premature infants benefit from music interventions? A systematic review of randomized controlled trials. *PLoS One*. 2016;11(9):e0161848.
14. Bieleninik Ł, Ghetti C, Gold C. Music therapy for preterm infants and their parents: a meta-analysis. *Pediatrics*. 2016;138(3):e20160971.
15. Haslbeck FB, Bassler D. Music from the very beginning — a neuroscience-based framework for music as therapy for preterm infants and their parents. *Front Behav Neurosci*. 2018;12:112.
16. Loewy J, Stewart K, Dassler AM, Telsey A, Homel P. The effects of music therapy on vital signs, feeding, and sleep in premature infants. *Pediatrics*. 2013;131(5):902–918.
17. Conde-Agudelo A, Díaz-Rossello JL. Kangaroo mother care to reduce morbidity and mortality in low birthweight infants. *Cochrane Database Syst Rev*. 2016;(8):CD002771.
18. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| heart rate during the intervention session | 7 | Mean Difference (MD) | Yes | 1.1535 [-5.5424, 7.8495] |
| | | ⚠ 1 row(s) excluded from native MD pooling for lacking raw inputs: ['study_4'] | | |
