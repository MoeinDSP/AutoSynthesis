# Fenoldopam for the Prevention of Acute Kidney Injury: A PRISMA-Compliant Systematic Review and Random-Effects Meta-Analysis of Randomised Controlled Trials

## Abstract

**Background.** Fenoldopam mesylate, a selective dopamine D1-receptor agonist, increases renal cortical and medullary blood flow and has been proposed as a renoprotective agent across critically ill, surgical, contrast-exposed and cardiac surgery populations. Whether it reduces the incidence of acute kidney injury (AKI) remains contested.

**Objective.** To quantify the effect of intravenous fenoldopam, compared with control (placebo, normal saline, or no fenoldopam), on the incidence of new-onset AKI/acute renal dysfunction across all patient populations.

**Methods.** A systematic search and screening pipeline identified eight randomised controlled trials contributing eight independent effect estimates (total N = 1,149 randomised participants). The pre-specified effect measure was the risk ratio (RR) for AKI incidence, pooled on the native binary scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Cochran's Q, I² and τ². Publication bias was assessed with Egger's regression test and Duval–Tweedie trim-and-fill. One trial (study_3) reported its result only as an odds ratio and lacked the raw event counts required for native RR pooling; it was therefore handled as a separate, non-poolable outcome group, leaving k = 7 trials (N = 1,069) in the primary synthesis.

**Results.** For the primary outcome group (*acute kidney injury incidence*, measure = RR; k = 7, N = 1,069), the pooled **Risk Ratio was 0.683 (95% CI 0.472 to 0.987; p = 0.0425)**. Native-scale (RR) pooling was confirmed for this estimate (`native_pooling_used = true`), so the value is a confirmed native-scale risk ratio rather than a standardized fallback. The automated direction field for this estimate records **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**, reflecting that favourability of a ratio measure cannot be assigned mechanically without knowing which event was tabulated; under the protocol's pre-specified direction convention (RR below 1 = fewer AKI events with fenoldopam), the point estimate lies on the side of fenoldopam. Between-study heterogeneity was moderate: I² = 47.72%, τ² = 0.098675, Q = 12.048 (df = 6), p = 0.0609. A second outcome group (*acute kidney injury incidence*, OR-reporting stratum; k = 1, N = 80) was flagged **insufficient_data** and could not be pooled; its single standardized effect was g = −0.528. Egger's test showed no funnel asymmetry (intercept = 0.03, p = 0.315) and trim-and-fill imputed no missing studies (k₀ = 0), indicating low risk of small-study/publication bias.

**Conclusions.** Pooled evidence from seven randomised trials indicates an approximately 32% relative reduction in AKI incidence with intravenous fenoldopam, with a confidence interval that only marginally excludes the null (upper bound 0.987) and moderate unexplained heterogeneity. The result is statistically fragile, the automated direction classifier returned an undetermined/tie verdict for this ratio measure, and one eligible trial could not be incorporated because of effect-measure incompatibility. Fenoldopam should be regarded as a promising but unconfirmed renoprotective intervention pending adequately powered, uniformly defined (KDIGO) trials.


## 1. Introduction

Acute kidney injury (AKI) complicates 5–25% of hospital admissions depending on the population studied, and is independently associated with prolonged mechanical ventilation, longer intensive care and hospital stay, chronic kidney disease, and short- and long-term mortality. Because established AKI has no disease-modifying therapy, pharmacological prophylaxis has been a persistent research priority, particularly in populations with a predictable renal insult: cardiac surgery with cardiopulmonary bypass, major vascular and abdominal surgery, iodinated contrast exposure, and sepsis or shock in the critically ill.

Fenoldopam mesylate is a selective post-synaptic dopamine D1-receptor agonist. Unlike low-dose dopamine, it has no α- or β-adrenergic or D2 activity, and it produces dose-dependent systemic vasodilation together with a disproportionate increase in renal cortical *and* medullary perfusion, natriuresis and diuresis. These pharmacodynamic properties provide a coherent mechanistic rationale for renoprotection, and fenoldopam has accordingly been evaluated in a series of randomised controlled trials (RCTs) against placebo or normal saline across heterogeneous at-risk populations. Individual trials have been variously positive, neutral and — in the contrast-nephropathy setting — frankly negative, and the attendant risk of clinically significant hypotension has limited enthusiasm for routine use.

### 1.1 Objective and review question

This review asks: **does fenoldopam, compared with control (placebo, normal saline, or no fenoldopam), reduce the incidence of acute kidney injury across all patient populations (critically ill, surgical, contrast-exposed and cardiac surgery patients)?**

- **Population (P):** adult patients at risk of AKI — critically ill, surgical, contrast-exposed, or cardiac surgery populations.
- **Intervention (I):** fenoldopam by intravenous infusion, any dose or duration.
- **Comparator (C):** control — placebo, normal saline, or no fenoldopam.
- **Outcome (O):** incidence of new-onset AKI / acute renal failure / acute renal dysfunction, as defined by each trial (RIFLE, AKIN, KDIGO, creatinine-rise thresholds, or need for renal replacement therapy where that constituted the trial's reported AKI endpoint), extracted as the number of AKI events and the number randomised per arm.
- **Study design (S):** randomised controlled trials.

### 1.2 Pre-specified effect direction convention

The protocol specifies that a **risk ratio below 1 (equivalently, a positive Hedges' g under the report's sign convention) indicates that fenoldopam reduced AKI risk relative to control** — that is, a result on the side of fenoldopam. This convention is stated here because the raw statistical sign of the pooled estimate follows a treatment-minus-control convention and, for ratio measures, the automated favourability classifier does not assign an arm without knowing which event was tabulated (see Section 5.2).

---

## 2. Methods

### 2.1 Protocol and reporting standard

The review is reported in accordance with the PRISMA 2020 statement. The analysis plan — eligible designs, the AKI outcome definition, the comparator definition, the random-effects model, and the pre-specification of the risk ratio as the effect measure — was fixed before synthesis. The effect-measure specification is recorded in the analytic record as `effect_measure_source = "explicit_user_request"`, i.e. RR was requested a priori by the review team and treated as authoritative where a primary report used a different metric.

### 2.2 Search and information sources

A systematic literature search and automated screening pipeline was executed to identify randomised comparisons of intravenous fenoldopam versus placebo, saline or no fenoldopam reporting AKI incidence. The search targeted bibliographic databases of biomedical literature and trial registries, supplemented by citation chasing of prior systematic reviews on fenoldopam and renal protection. Records were screened in two stages — title/abstract, then full text — against the PICOS criteria above.

**Transparency note.** The pipeline summary available to this report records the *output* of screening (8 included studies contributing 8 effect sizes) but does not preserve stage-by-stage record counts (records identified per database, duplicates removed, abstracts screened, full texts assessed, reasons for each full-text exclusion). A complete PRISMA flow diagram with numeric counts at each node therefore **cannot** be reconstructed from the available data, and none is fabricated here. Readers should treat the screening description as a faithful account of the procedure and the included-study count as verified, while recognising that the intermediate counts are not auditable from this record.

### 2.3 Eligibility criteria

**Included:** randomised controlled trials; adult at-risk populations (critical illness, surgery, contrast exposure, cardiac surgery); intravenous fenoldopam at any dose/duration; placebo, saline or no-fenoldopam control; AKI incidence reported as an event count (or recoverable as such) with the number randomised per arm.

**Excluded:** narrative and systematic reviews, editorials and commentaries; non-randomised and single-arm studies; duplicate reports of the same trial population (the most complete report retained, to avoid double-counting); active-comparator-only designs (e.g. fenoldopam versus dopamine without a placebo/saline arm); studies reporting only continuous renal function surrogates (creatinine clearance, urine output) without a dichotomous AKI endpoint.

### 2.4 Data extraction

For each trial, the number of AKI events and the number randomised were extracted per arm, together with the trial's own AKI definition, population, fenoldopam dose and infusion duration, and comparator. Where a report presented an adjusted effect measure (e.g. an odds ratio from a logistic model) without recoverable raw event counts, this was recorded and flagged, since such a record cannot enter a native risk-ratio synthesis.

### 2.5 Statistical synthesis

Effects were pooled on the **native binary scale as risk ratios (RR)** using a random-effects model with **restricted maximum likelihood (REML)** estimation of τ². The record confirms `computation_scale = "RR"` and `native_pooling_used = true` for the primary synthesis, meaning the pooled value is a genuine native-scale risk ratio and **not** a standardized fallback. Standardized mean differences (Hedges' g) were additionally computed study-by-study on a common standardized metric, solely to permit uniform display, precision weighting, funnel-based bias diagnostics, and comparability of the single non-poolable trial; these g values are descriptive companions to, not substitutes for, the RR synthesis.

Where the included studies spanned more than one distinct outcome/effect-measure group, each group was analysed **separately** with its own k, pooled effect, confidence interval and heterogeneity statistics, rather than being merged. Groups containing too few studies to pool were reported as such without an invented pooled value.

Heterogeneity was quantified by Cochran's Q with its p-value, I² (proportion of total variability attributable to between-study heterogeneity) and τ² (absolute between-study variance on the log-RR scale). Publication/small-study bias was assessed with Egger's regression of effect size on precision and the Duval–Tweedie trim-and-fill procedure. Statistical significance was two-sided at α = 0.05.

---

## 3. Search and Screening Results

Screening yielded **8 randomised controlled trials** meeting all eligibility criteria, contributing **8 independent effect estimates** (one per trial; no trial contributed multiple arms or timepoints to the same outcome group). The total randomised sample across all eight trials is **1,149 participants** (45 + 300 + 80 + 78 + 193 + 283 + 92 + 78).

Of these, **7 trials (N = 1,069)** supplied the raw per-arm event counts required for native risk-ratio pooling and constitute the primary synthesis. **One trial (study_3, N = 80)** reported its renal outcome explicitly as an **odds ratio** without recoverable raw inputs; in accordance with the pre-specified rule that the user-requested RR measure is authoritative, this record was *not* force-converted into the native RR pool but was instead assigned to its own outcome group, which — containing a single study — is flagged `insufficient_data` and is not pooled (Sections 5.3 and 8).

Exclusions applied during screening followed the criteria in Section 2.3, including removal of reviews and of duplicate reports of the same randomised population to prevent double-counting of participants. As noted in Section 2.2, per-reason exclusion counts are not preserved in the analytic record and are not reconstructed here.

---

## 4. Included Studies

Table 1 summarises the eight included effect estimates as recorded in the analytic pipeline. Study identifiers are the de-identified pipeline labels (`study_n_Rn`); the per-study standardized effect (Hedges' g) and its 95% confidence interval are shown alongside the randomised sample size.

**Table 1. Included studies and per-study standardized effect estimates.**

| Study label | N randomised | Hedges' g | 95% CI | CI excludes null? | In primary RR pool? |
|---|---:|---:|---|---|---|
| study_1_R1 | 45 | −0.4946 | [−1.088, 0.099] | No | Yes |
| study_2_R2 | 300 | −0.4152 | [−0.644, −0.186] | Yes | Yes |
| study_3_R3 | 80 | −0.5283 | [−0.974, −0.082] | Yes | **No** (OR-only; separate group) |
| study_4_R4 | 78 | +0.0331 | [−0.411, 0.477] | No | Yes |
| study_5_R5 | 193 | −0.5311 | [−0.818, −0.244] | Yes | Yes |
| study_6_R6 | 283 | +0.0574 | [−0.176, 0.291] | No | Yes |
| study_7_R7 | 92 | −0.2484 | [−0.659, 0.162] | No | Yes |
| study_8_R8 | 78 | −1.2285 | [−1.713, −0.744] | Yes | Yes |

**Distributional features.** Six of the eight estimates (study_1, 2, 3, 5, 7, 8) carry a negative g — fewer AKI events in the fenoldopam arm under this sign convention — while two (study_4, g = +0.033; study_6, g = +0.057) are essentially null and marginally on the control side. Four estimates have confidence intervals excluding the null (study_2, study_3, study_5, study_8), all in the direction of fewer AKI events with fenoldopam. The estimates range from g = −1.2285 (study_8, the largest single effect, from a small 78-patient trial) to g = +0.0574 (study_6, the second-largest trial at N = 283). Sample sizes span 45 to 300, with a median of 86 and a strong inverse association between trial size and effect magnitude among the extremes: the two largest neutral trials (study_6, N = 283; study_4, N = 78) and the most extreme positive trial (study_8, N = 78) illustrate the small-trial effect-inflation pattern that the heterogeneity and bias analyses address in Sections 6 and 7.

The per-study distribution is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between study precision and observed effect is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

---

## 5. Effect Sizes and Meta-Analytic Results

### 5.1 Primary outcome group — acute kidney injury incidence (RR stratum)

**Outcome group key:** `acute kidney injury incidence::measure=RR`

| Quantity | Value |
|---|---|
| Studies pooled (k) | **7** |
| Participants (N) | **1,069** |
| Effect measure (`measure_label`) | **Risk Ratio (RR)** |
| Computation scale | RR (native) |
| `native_pooling_used` | **true** — confirmed native-scale result |
| Effect-measure source | explicit user request (a priori) |
| **Pooled Risk Ratio** | **0.683** |
| 95% confidence interval | **[0.472, 0.987]** |
| p-value | **0.0425** |
| Model | Random effects, REML |
| I² | 47.72% |
| τ² | 0.098675 |
| Cochran's Q (df = 6) | 12.048 |
| Q p-value | 0.0609 |

The pooled **Risk Ratio was 0.683 (95% CI 0.472–0.987; p = 0.0425)** across 7 trials and 1,069 participants. Because `native_pooling_used = true` and the computation scale is RR, this is a **confirmed native-scale risk ratio** — it is correct to call it a *pooled risk ratio*, and it is **not** a standardized fallback and **not** a Hedges' g. On the relative scale, the point estimate corresponds to a **31.7% relative reduction** in the risk of AKI, with the interval spanning a 52.8% reduction at the lower bound to a 1.3% reduction at the upper bound. The upper confidence limit of 0.987 sits immediately adjacent to the line of no effect, and the p-value of 0.0425 is only marginally below the conventional α = 0.05 threshold; the finding is therefore statistically *fragile* in the sense that it would not survive modest perturbation of the data or the inclusion of one additional neutral trial.

The forest plot for this synthesis is at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`, and the cumulative (sequentially accumulated) analysis is at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`.

### 5.2 Direction of effect — as recorded

The `favors` field for the primary meta-analysis records:

> **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**

and, in the per-group record, **"neither (tie or undetermined)"**. This is the authoritative direction statement for this result and is reported here without reinterpretation: the automated classifier did **not** assign the result to the fenoldopam arm or to the control arm. The reason is structural rather than substantive — for a ratio measure, which arm is favoured depends on whether the tabulated event is the adverse outcome (AKI) or its complement, and that mapping was not confirmed in the record, so the classifier abstained.

Separately, and as a matter of protocol rather than inference, the review's pre-specified direction convention (Section 1.2) states that an RR below 1 denotes reduced AKI risk with fenoldopam. Readers should therefore note both facts: the pooled point estimate of 0.683 lies below 1 on the scale the protocol defined as favouring fenoldopam, while the analytic record's own direction classification for this estimate is **undetermined / neither arm**. We do not resolve this tension by asserting a favoured arm beyond what the record supports.

### 5.3 Second outcome group — acute kidney injury incidence (OR-reporting stratum)

**Outcome group key:** `acute kidney injury incidence::measure=OR`

| Quantity | Value |
|---|---|
| Studies (k) | **1** |
| Participants (N) | **80** |
| Status | **insufficient_data — not pooled** |
| Single standardized effect | g = −0.5283 |
| Contributing study | study_3 |
| Effect-measure conflict | user requested RR, but the paper explicitly reports OR |

This group contains a **single trial (study_3, N = 80)** and is explicitly flagged `insufficient_data`. **No pooled effect, confidence interval, p-value, I², τ² or Q statistic can be or is reported for this group** — one study cannot support a meta-analytic synthesis or any between-study heterogeneity estimate. The only quantity available is the single trial's standardized effect, **g = −0.5283 (95% CI −0.974 to −0.082 from Table 1)**, which under the report's sign convention lies on the side of fewer AKI events with fenoldopam. This estimate is reported descriptively and is *not* combined with the primary RR synthesis.

### 5.4 Why the two groups were not merged

The two outcome groups address the *same clinical construct* (AKI incidence) but are separated by **effect measure**, not by population or timepoint. Study_3 reported an odds ratio explicitly and did not supply the raw per-arm event counts needed to reconstruct a risk ratio. Because RR was the authoritative, a priori measure, the pipeline declined to silently treat an OR as an RR — a conversion that is biased upward in magnitude whenever the outcome is not rare, as AKI frequently is not. The consequence is a deliberate, documented trade-off: statistical purity of the native RR pool (k = 7) at the cost of excluding one otherwise-eligible trial (N = 80, 7.0% of the total randomised sample) from the pooled estimate. This is recorded in Section 8.

---

## 6. Heterogeneity

For the primary RR synthesis (k = 7):

- **I² = 47.72%** — moderate heterogeneity; just under half of the observed variability in effects exceeds what sampling error alone would produce.
- **τ² = 0.098675** — between-study variance on the log-RR scale, corresponding to τ ≈ 0.314. This implies that the *typical* deviation of a true study-specific log RR from the pooled log RR is roughly a factor of e^0.314 ≈ 1.37 in either direction.
- **Cochran's Q = 12.048 on 6 degrees of freedom, p = 0.0609** — does not reach conventional significance, though Q is well known to be underpowered with k = 7.

The interpretation is therefore one of **moderate, borderline-significant, and unexplained heterogeneity**. The pooled RR of 0.683 should be read as the centre of a distribution of true effects rather than as a single common effect. An approximate 95% prediction interval, computed by the reviewers from the reported τ² and the standard error implied by the confidence interval (SE of the pooled log RR ≈ 0.188), spans roughly **RR 0.33 to 1.37** on a normal approximation — and wider still (approximately 0.27 to 1.75) if a t-distribution with k − 2 = 5 degrees of freedom is used. In plain terms: while the *average* effect is a risk reduction, the available data do not exclude the possibility that in some future populations fenoldopam confers no benefit, or even modest harm, with respect to AKI incidence. This prediction interval is an auxiliary reviewer calculation and is not part of the deterministic analytic record.

Visual inspection supports this reading: study_8 (g = −1.2285) and, at the other extreme, study_6 (g = +0.0574) and study_4 (g = +0.0331) are the principal contributors to dispersion, with study_8 sitting well outside the cluster formed by the remaining estimates. The heterogeneity diagnostics are summarised graphically in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

Clinically plausible sources of this heterogeneity include: (i) divergent AKI definitions across trials (RIFLE vs AKIN vs KDIGO vs ad hoc creatinine thresholds vs renal replacement therapy as a surrogate), which alters both baseline event rates and the sensitivity of the endpoint; (ii) differing baseline AKI risk across critically ill, contrast-exposed, general surgical and cardiac surgery populations; (iii) variation in fenoldopam dose (typically 0.03–0.1 µg/kg/min) and infusion duration; (iv) differences in co-interventions such as hydration protocols, N-acetylcysteine, and vasopressor management; and (v) small-trial effect inflation, given that the most extreme estimate arises from one of the smallest trials.

---

## 7. Moderator Analyses

**No formal moderator or subgroup analyses were performed, and none should be inferred from this report.** With k = 7 studies in the only poolable group, meta-regression is not defensible: conventional guidance requires approximately 10 studies per covariate, and with 7 studies even a single moderator would leave the model overfitted and the resulting coefficient uninterpretable. Accordingly, no meta-regression slopes, subgroup pooled effects, or between-subgroup tests are reported, and none were computed.

The clinically important moderators that *would* have been tested, had k permitted, are: (a) **patient population** (critically ill vs cardiac surgery vs contrast-exposed vs other surgical) — the most likely source of true effect modification, since the contrast-nephropathy literature is the most consistently negative; (b) **AKI definition** (RIFLE/AKIN/KDIGO vs creatinine threshold vs RRT surrogate); (c) **fenoldopam dose and infusion duration**; (d) **timing of initiation** relative to the renal insult (pre-, intra- or post-insult); and (e) **baseline renal function and control-arm event rate**. The absence of these analyses is a substantive limitation (Section 10), not a neutral omission: the moderate I² of 47.72% is precisely the pattern that moderator analysis exists to explain, and it remains unexplained here.

The one precision-related pattern that can be described descriptively rather than tested inferentially is visible in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`: smaller trials tend to report larger effects (study_8, N = 78, g = −1.2285) while the largest neutral trial reports essentially no effect (study_6, N = 283, g = +0.0574). This is a *description* of the data, not a statistical test, and the formal small-study bias diagnostics in Section 9 did not find this pattern to be statistically significant.

---

## 8. Data Quality & Validation Notes

The analytic record carries one substantive validation flag, reported here in plain language without softening:

1. **Effect-measure conflict and consequent exclusion from the pooled estimate.** For the outcome group `acute kidney injury incidence::measure=OR`, the record states: *"user requested RR, but the paper(s) explicitly report OR — user request kept as authoritative; 1 row(s) excluded from native RR pooling for lacking raw inputs: ['study_3']."* In plain terms: the review pre-specified the risk ratio as the effect measure; one eligible trial (**study_3**, N = 80) reported its renal outcome only as an odds ratio and did not provide the per-arm event counts needed to compute an RR. Rather than convert an OR into an RR — a conversion that systematically exaggerates effect magnitude for non-rare outcomes such as AKI — the pipeline excluded that trial from the native RR pool. **The consequence is that the headline pooled estimate rests on 7 of the 8 included trials (1,069 of 1,149 randomised participants, 93.0%); one eligible randomised trial's data are not represented in the pooled risk ratio.**

2. **One outcome group could not be pooled.** The OR-reporting group contains k = 1 study and is flagged `insufficient_data`. No pooled effect, confidence interval or heterogeneity statistic exists for it, and none has been invented. Only the single-study standardized effect (g = −0.5283) is reported.

3. **Two distinct effect-measure strata were kept separate rather than merged.** Per the analysis plan, the RR stratum (k = 7) and the OR stratum (k = 1) are reported with their own k, N and statistics. They were deliberately not combined into a single overall number.

4. **Direction of effect returned as undetermined.** For the primary synthesis, the `favors` field records *"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"* rather than naming fenoldopam or control. This is reported as given (Section 5.2); the review does not override it.

5. **Exclusion of reviews and duplicate trial reports.** Screening excluded narrative/systematic reviews and duplicate publications of the same randomised population, the latter specifically to prevent double-counting of participants. Per-category counts for these exclusions are not preserved in the analytic record (Section 2.2).

6. **Mixed native-scale and standardized quantities co-exist in this report.** The headline pooled result is a confirmed native-scale risk ratio (`native_pooling_used = true`). The per-study values in Table 1, the trim-and-fill adjusted value, and the single effect for study_3 are standardized (Hedges' g) quantities. These are on different scales and must not be compared numerically with the pooled RR.

---

## 9. Publication Bias

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | 0.03 |
| Egger's test p-value | **0.315** |
| Trim-and-fill imputed studies (k₀) | **0** |
| Trim-and-fill adjusted effect (standardized scale) | g = −0.3979 |
| Overall risk rating | **Low** |

Egger's regression test showed **no statistically significant funnel-plot asymmetry (intercept = 0.03, p = 0.315)**, indicating no detectable relationship between effect magnitude and study precision. Consistent with this, the **Duval–Tweedie trim-and-fill procedure imputed no missing studies (k₀ = 0)**, so the pooled estimate is unchanged after adjustment; the adjusted standardized value of **g = −0.3979** is reported on the standardized scale and is not directly comparable with the native pooled RR of 0.683. Taken together, these results support a **low risk of publication (small-study) bias**.

**Caveat (as recorded).** These tests have limited statistical power, particularly when fewer than approximately 10 studies are pooled — as here, with k = 7 — or when between-study heterogeneity is appreciable, as it is here (I² = 47.72%). A null result should therefore be read as **"no evidence of bias" rather than "evidence of no bias."** Confidence in the low-risk rating would be strengthened by visual funnel-plot inspection and by an explicit search of grey literature, trial registries and unpublished data. This caveat has particular force given the descriptive pattern noted in Section 7, in which the largest observed effect comes from one of the smallest trials — a configuration that Egger's test with k = 7 may simply lack the power to detect.

---

## 10. Discussion

### 10.1 Principal findings

Across 7 randomised trials and 1,069 participants, intravenous fenoldopam was associated with a **pooled risk ratio for AKI of 0.683 (95% CI 0.472–0.987; p = 0.0425)**, a point estimate corresponding to roughly a one-third relative reduction in AKI incidence. The effect measure is a confirmed native-scale risk ratio. Six of eight included trials pointed in the direction of fewer AKI events with fenoldopam, four of them with confidence intervals excluding the null. Heterogeneity was moderate (I² = 47.72%, τ² = 0.098675) and Cochran's Q was borderline (p = 0.0609). Formal diagnostics found no evidence of publication bias.

Three qualifications are integral rather than peripheral to this finding. First, the **upper confidence bound of 0.987** is within 1.3 percentage points of the null on the relative scale, and p = 0.0425 clears α = 0.05 by a narrow margin — the result is statistically fragile and should not be described as robust. Second, the **automated direction classification for this estimate is "neither (tie or undetermined)"**, not "favours fenoldopam"; the protocol's convention places RR < 1 on the fenoldopam side, but the record itself abstained from assigning an arm. Third, the **prediction interval** implied by τ² (approximately RR 0.33–1.37 by reviewer calculation) crosses 1, so the average benefit observed does not guarantee benefit in any particular future setting.

### 10.2 Relationship to prior evidence and mechanism

The direction of the pooled estimate is biologically coherent. Fenoldopam's selective D1 agonism increases renal blood flow in both cortex and the hypoxia-vulnerable outer medulla — the segment where ischaemic tubular injury concentrates — and does so without the α/β-adrenergic effects that undermined low-dose dopamine. The heterogeneity observed is equally coherent: the trials most likely to be neutral or negative are those in which the dominant injury mechanism is not primarily haemodynamic. In contrast-associated nephropathy, direct tubular toxicity and oxidative injury contribute substantially, which plausibly explains why contrast-exposure trials have been the most consistently null in this literature, while cardiac surgery and critical illness — where renal hypoperfusion and ischaemia-reperfusion predominate — are the settings in which the positive signals cluster. In this dataset, the two essentially null estimates (study_4, g = +0.0331; study_6, g = +0.0574) sit alongside markedly positive ones (study_8, g = −1.2285), a dispersion more readily explained by true population-level effect modification than by chance alone.

Because no moderator analysis was feasible at k = 7, this mechanistic account **remains a hypothesis generated by the pattern of results, not a finding of this review**. The review cannot state which populations benefit and which do not.

### 10.3 Clinical implications

The evidence is best characterised as a **plausible but unconfirmed signal of renoprotection**. The point estimate is clinically meaningful — a 32% relative risk reduction in an outcome with no disease-modifying therapy would be important — but the interval nearly includes the null, the direction classification is formally undetermined, the heterogeneity is unexplained, one eligible trial is absent from the pooled estimate, and the total evidence base (1,069 pooled participants) is small for a binary outcome of this importance. Against this must be weighed fenoldopam's principal harm, dose-dependent systemic vasodilation and hypotension, which is itself a mechanism of renal hypoperfusion and which this review did not assess, since the pre-specified outcome was AKI incidence alone.

These findings do not support routine prophylactic fenoldopam in unselected at-risk patients. They do support continued evaluation in the populations where the haemodynamic mechanism is most plausible — cardiac surgery and the haemodynamically unstable critically ill — using uniform KDIGO criteria, pre-registered protocols, concurrent reporting of hypotension and vasopressor exposure, and sample sizes powered for AKI rather than for surrogate renal endpoints. Individual participant data meta-analysis would be the most efficient route to resolving the population-level effect modification that aggregate data at k = 7 cannot address.

---

## 11. Limitations

1. **Small number of pooled studies.** Only k = 7 trials entered the primary synthesis (N = 1,069). This limits precision, renders Cochran's Q and Egger's test underpowered, makes the REML estimate of τ² itself imprecise, and precludes moderator analysis entirely.
2. **One eligible trial excluded from the pooled estimate.** Study_3 (N = 80) reported an odds ratio without recoverable raw event counts and was therefore excluded from native RR pooling. 7.0% of the randomised evidence base is not represented in the headline result.
3. **A second outcome group could not be pooled.** The OR-reporting group has k = 1 and is flagged `insufficient_data`; no pooled statistic exists for it.
4. **Direction of effect formally undetermined.** The analytic record's `favors` field returns "neither (tie or undetermined)" for the primary estimate rather than naming an arm, limiting how assertively the result can be framed.
5. **Statistical fragility.** With p = 0.0425 and an upper CI bound of 0.987, the finding is sensitive to the addition or removal of a single trial. No formal leave-one-out sensitivity analysis is available in the record; given that study_8 (g = −1.2285, N = 78) is the most extreme estimate, its influence on the pooled result is likely substantial but is not quantified here.
6. **Moderate unexplained heterogeneity.** I² = 47.72% and τ² = 0.098675 with no moderator analysis possible; the prediction interval crosses the null.
7. **Outcome definition inconsistency.** AKI was defined by each trial's own criteria — RIFLE, AKIN, KDIGO, creatinine-rise thresholds, or renal replacement therapy as a surrogate. These are not interchangeable: RRT-based endpoints capture only the most severe stratum, while creatinine-threshold definitions capture milder injury, producing non-comparable baseline event rates and endpoint sensitivities across trials.
8. **Clinical heterogeneity of populations and dosing.** Pooling critically ill, cardiac surgery, contrast-exposed and general surgical patients, across varying doses, infusion durations and timings relative to insult, assumes a transportable average effect that the data cannot verify.
9. **Incomplete PRISMA flow reporting.** Stage-by-stage screening counts and per-reason full-text exclusion counts are not preserved in the analytic record, so a fully numeric PRISMA flow diagram cannot be reproduced and has not been fabricated.
10. **No formal risk-of-bias assessment reported.** Domain-level risk-of-bias ratings (e.g. Cochrane RoB 2: randomisation, allocation concealment, blinding, missing outcome data, outcome measurement, selective reporting) and GRADE certainty ratings are not available in the analytic record for the included trials. Their absence means the pooled estimate's internal validity is unverified at the study level, and the certainty of evidence cannot be graded.
11. **Harms not assessed.** Hypotension, vasopressor requirement, mortality, length of stay and dialysis dependence lie outside the single pre-specified outcome and are not evaluated, so no benefit–harm balance can be drawn.
12. **Publication bias diagnostics are weak at this k.** The low-risk rating reflects absence of detected asymmetry, not demonstrated absence of bias, and no grey-literature or registry search for unpublished negative trials is documented.

---

## 12. Conclusion

In a random-effects meta-analysis of 7 randomised controlled trials comprising 1,069 participants, intravenous fenoldopam versus placebo, saline or no fenoldopam yielded a **pooled Risk Ratio for acute kidney injury of 0.683 (95% CI 0.472–0.987; p = 0.0425)**, a confirmed native-scale risk-ratio result corresponding to an approximately 32% relative reduction in AKI incidence. Heterogeneity was moderate and unexplained (I² = 47.72%, τ² = 0.098675, Q = 12.048 on 6 df, p = 0.0609), and formal diagnostics showed no evidence of publication bias (Egger's p = 0.315; trim-and-fill k₀ = 0). A second outcome group comprising a single OR-reporting trial (k = 1, N = 80, g = −0.5283) was flagged `insufficient_data` and could not be pooled.

The signal is encouraging but should not be over-read. Its confidence interval barely excludes the null, the analytic record's own direction field classifies the result as favouring **neither** arm, the prediction interval crosses unity, one eligible randomised trial is absent from the pooled estimate because of effect-measure incompatibility, and neither study-level risk of bias nor the harms of fenoldopam (notably hypotension) were assessed. **Fenoldopam is best regarded as a biologically plausible, statistically fragile, and as-yet unconfirmed renoprotective intervention.** Adequately powered, population-specific randomised trials using uniform KDIGO AKI criteria and reporting both renal and haemodynamic outcomes — ideally supplemented by individual participant data synthesis — are required before any recommendation for clinical use can be made.

---

## References

**Included studies (de-identified pipeline labels; full citations held in the review's extraction file).**

1. Study 1 (`study_1_R1`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 45.
2. Study 2 (`study_2_R2`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 300.
3. Study 3 (`study_3_R3`) — randomised controlled trial of intravenous fenoldopam versus control; renal outcome reported as an odds ratio; N = 80. *Excluded from native risk-ratio pooling (see Section 8).*
4. Study 4 (`study_4_R4`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 78.
5. Study 5 (`study_5_R5`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 193.
6. Study 6 (`study_6_R6`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 283.
7. Study 7 (`study_7_R7`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 92.
8. Study 8 (`study_8_R8`) — randomised controlled trial of intravenous fenoldopam versus control for prevention of acute kidney injury; N = 78.

**Methodological references.**

9. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
10. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
11. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med.* 2002;21(11):1539–1558.
12. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw.* 2010;36(3):1–48.
13. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *J Educ Behav Stat.* 2005;30(3):261–293.
14. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
15. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
16. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routine prediction intervals in reports of meta-analysis. *BMJ Open.* 2016;6(7):e010247.
17. Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis.* Orlando, FL: Academic Press; 1985.
18. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ.* 2019;366:l4898.
19. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ.* 2008;336(7650):924–926.
20. Kidney Disease: Improving Global Outcomes (KDIGO) Acute Kidney Injury Work Group. KDIGO Clinical Practice Guideline for Acute Kidney Injury. *Kidney Int Suppl.* 2012;2(1):1–138.

---

## Figures

| Figure | Path |
|---|---|
| Forest plot (primary RR synthesis, k = 7) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect vs. precision) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| acute kidney injury incidence | 7 | Risk Ratio (RR) | Yes | 0.6829 [0.4723, 0.9872] |
| acute kidney injury incidence | 1 | Risk Ratio (RR) | Yes | -0.5283 (single study, not pooled) |
| | | ⚠ user requested RR, but the paper(s) explicitly report OR -- user request kept as authoritative; 1 row(s) excluded from native RR pooling for lacking raw inputs: ['study_3'] | | |
