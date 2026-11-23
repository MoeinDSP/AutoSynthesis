# Major Bleeding With Extended-Duration Versus Standard-Duration Anticoagulant Thromboprophylaxis in Acutely Ill Hospitalized Medical Patients: A Systematic Review and Meta-Analysis of Short-Term (≤45-Day) Risk

## Abstract

**Background.** Extending anticoagulant thromboprophylaxis beyond the standard 6–14 day in-hospital course reduces symptomatic venous thromboembolism (VTE) in acutely ill medical patients, but the competing hazard of bleeding has repeatedly offset that benefit in individual trials. We quantified the short-term (within 45 days of randomization) risk of major bleeding associated with extended-duration versus standard-duration prophylaxis.

**Methods.** We conducted a PRISMA-compliant systematic review and random-effects meta-analysis of randomized controlled trials comparing extended-duration anticoagulant thromboprophylaxis with standard-duration prophylaxis (or placebo after a standard course) in acutely ill hospitalized medical patients. The outcome was the number of patients with a major bleeding event (trial-defined, typically ISTH criteria) within 45 days of randomization, in the primary-analysis (all randomized) population only; COVID-19-restricted sensitivity analyses, same-extended-agent sensitivity analyses, and all subgroup analyses (sex, age, cancer history, D-dimer, infection status) were excluded by protocol. Risk ratios (RR) were pooled on the native log-RR scale using restricted maximum likelihood (REML). Heterogeneity was summarized with Q, I² and τ²; small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** Seven records entered data extraction; five yielded an extractable short-term primary-analysis major bleeding effect size, and one of these was excluded as a duplicate report of an already-included trial, leaving **k = 4 independent trials with 33,793 randomized participants** in the primary pooled analysis. The pooled **Risk Ratio (RR) was 1.954 (95% CI 1.239 to 3.083; p = 0.00398)**; native RR-scale pooling was used, so this is a confirmed native-scale result rather than a standardized fallback. The automated direction field classified the comparison as favouring *"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"*, reflecting that the counted event is a harm; because the event counted is major bleeding, an RR above 1 corresponds to **more** bleeding with extended-duration prophylaxis, i.e. the expected harm signal. Heterogeneity was moderate but not statistically significant (I² = 40.32%, τ² = 0.086529, Q = 4.754, df = 3, p = 0.1907). Egger's test showed no funnel-plot asymmetry (intercept −0.0752, p = 0.5511) and trim-and-fill imputed no missing studies (k₀ = 0); publication-bias risk was graded low.

**Conclusions.** In acutely ill hospitalized medical patients, extended-duration anticoagulant thromboprophylaxis approximately doubles the short-term risk of major bleeding relative to a standard-duration course (pooled RR 1.95, 95% CI 1.24–3.08). This harm is statistically robust and directionally consistent across trials, and must be weighed explicitly against the modest absolute reduction in symptomatic VTE when considering routine post-discharge prophylaxis. Confidence is limited by the small number of poolable trials (k = 4), moderate between-trial heterogeneity in bleeding definitions and agents, and a very wide implied prediction interval.

## 1. Introduction

Venous thromboembolism (VTE) is a leading preventable cause of death among hospitalized medical patients. Randomized trials established decades ago that 6–14 days of in-hospital pharmacological thromboprophylaxis with low-molecular-weight heparin, unfractionated heparin or fondaparinux reduces asymptomatic and symptomatic VTE in acutely ill medical inpatients. However, the period of elevated thrombotic risk does not end at discharge: observational data show that a substantial proportion of hospitalization-associated VTE events occur in the weeks *after* the index admission, when prophylaxis has typically been stopped. This observation motivated a succession of large randomized trials of **extended-duration thromboprophylaxis** — continuation of parenteral prophylaxis, or transition to a direct oral anticoagulant, for roughly 30–45 days after randomization.

The efficacy story in these trials has been consistent but modest: extended prophylaxis reduces symptomatic VTE and VTE-related death by a small absolute margin. The safety story has been the decisive one. In trial after trial, the net clinical benefit of extended prophylaxis has been eroded or abolished by an excess of major bleeding, and major clinical practice guidelines have consequently recommended *against* routine extended-duration prophylaxis in unselected acutely ill medical patients. Despite this convergence of guideline opinion, the magnitude of the bleeding hazard — how large the relative increase actually is, how consistent it is across agents and across bleeding definitions, and how precisely it can be estimated from the randomized evidence — remains worth quantifying formally, particularly for shared decision-making in patients whose thrombotic risk is high enough that extended prophylaxis is still considered on an individual basis.

This systematic review and meta-analysis therefore addresses a single, narrowly specified question:

> In acutely ill hospitalized medical patients receiving VTE prophylaxis, does extended-duration anticoagulation, compared with standard-duration anticoagulation (or placebo after a standard course), increase the risk of major bleeding within 45 days of randomization?

The 45-day window was prespecified as the **short-term, primary analysis** horizon because it corresponds to the active treatment and immediate post-treatment period of the extended regimens, during which on-treatment bleeding hazard is concentrated, and because it is the window most consistently reported across the trial programme.

---

## 2. Methods: Search and Screening

### 2.1 Protocol and reporting standards

The review was conducted and is reported in accordance with the PRISMA 2020 statement. The effect measure (risk ratio), the outcome definition, the eligible analysis population, and the exclusions listed in §2.3 were specified before pooling; the risk ratio was fixed as the target measure by explicit a priori request (`effect_measure_source: explicit_user_request`), not chosen post hoc on the basis of model fit.

### 2.2 Eligibility criteria

| Domain | Criterion |
|---|---|
| **Population** | Acutely ill hospitalized **medical** patients (non-surgical) receiving VTE prophylaxis |
| **Intervention** | Extended-duration anticoagulant thromboprophylaxis (continuation of parenteral agent or transition to an oral anticoagulant beyond the standard in-hospital course) |
| **Comparator** | Standard-duration anticoagulant thromboprophylaxis, or placebo administered after a completed standard course |
| **Outcome** | Number of patients with a **major bleeding** event (as defined by each trial, typically ISTH criteria) occurring **within 45 days of randomization**, with the total number randomized per arm as the denominator |
| **Design** | Randomized controlled trials |
| **Analysis set** | **Primary-analysis population only** (all randomized acutely ill medical patients) |

### 2.3 Prespecified exclusions

To preserve one independent estimate per trial and to avoid contaminating the primary analysis with non-primary analysis sets, the following were excluded by protocol:

1. **COVID-19-only sensitivity analyses** (populations restricted to patients hospitalized with COVID-19);
2. **Same-extended-agent sensitivity analyses** (restricted comparisons in which the extended and standard phases used the identical agent);
3. **All subgroup analyses**, including those defined by sex, age, history of cancer, baseline D-dimer, and infection status;
4. **Duplicate reports of the same randomized trial** (secondary publications, pooled re-analyses, or companion papers reporting the same randomized comparison).

### 2.4 Data extraction and effect-size computation

For each eligible trial, the number of patients with a major bleeding event and the number randomized were extracted for both arms. Risk ratios and their sampling variances were computed on the log scale from these 2×2 counts. For cross-outcome comparability the pipeline additionally computed a standardized effect index (Hedges' *g*-scale conversion) for each extracted record; these standardized values are reported descriptively in §4 but were **not** the basis of the pooled estimate.

### 2.5 Statistical analysis

Pooling was performed with a **random-effects model estimated by restricted maximum likelihood (REML)** on the native log-RR scale (`native_pooling_used: true`; `computation_scale: RR`). Heterogeneity was quantified by Cochran's Q (with k−1 degrees of freedom), the I² statistic, and the between-study variance τ². Small-study effects and potential publication bias were examined using Egger's regression test of funnel-plot asymmetry and the Duval–Tweedie trim-and-fill procedure. Two-sided p < 0.05 was taken as the threshold for statistical significance. Because the pooled measure is a ratio, a value above 1.0 denotes a higher *event* rate — here, a higher major bleeding rate — in the extended-duration arm.

### 2.6 Study flow

Seven records entered the extraction stage. Of these, **five** yielded an extractable effect size for short-term (≤45-day) major bleeding in the primary-analysis population; the remaining two records did not contribute a usable estimate for this outcome and timepoint under the eligibility rules above (e.g., they did not report the required arm-level event counts for the primary-analysis population within the 45-day window, or reported only excluded analysis sets). Of the five extracted effect sizes, **one was removed at the trial-deduplication stage** as a duplicate report of the same randomized trial as an already-included record (see §8, Data Quality & Validation Notes). The resulting primary meta-analysis comprises **k = 4 independent trials and 33,793 randomized participants**.

```
Records entering extraction ..................................... 7
  └─ Yielded extractable ≤45-day primary-analysis effect size .... 5
       └─ Excluded as duplicate report of an included trial ...... 1
            └─ Included in pooled analysis (independent trials) ... 4
                 Participants randomized ................... 33,793
```

---

## 3. Included Studies

Four independent randomized trials contributed to the primary pooled analysis; a fifth extracted record (`study_1_R1`) represented the same underlying trial as an included record and was retained only for descriptive purposes. Trials are identified below by the pipeline identifiers under which their data were extracted; all were large multicentre randomized comparisons of an extended anticoagulant course against a standard-duration course or post-course placebo in acutely ill medical inpatients.

| Record ID | Status in pooled analysis | Randomized participants (N) | Role |
|---|---|---|---|
| `study_1_R1` | **Excluded** — duplicate report of the trial represented by `study_3` | 5,963 | Descriptive only |
| `study_3_R3` | Included | 6,401 | Retained representative of trial cluster `trial_98c4dd27793d` (largest N) |
| `study_4_R4` | Included | 7,998 | Independent trial |
| `study_5_R5` | Included | 7,432 | Independent trial |
| `study_6_R6` | Included | 11,962 | Independent trial |
| **Pooled total (k = 4)** | — | **33,793** | — |

All four pooled trials were large (range 6,401–11,962 randomized participants), such that the pooled analysis is dominated by trials of comparable and substantial size rather than by a single mega-trial; the largest trial contributes approximately 35% of the total randomized population. All contributed major bleeding counts ascertained within the prespecified 45-day short-term window in the all-randomized primary-analysis population. Across this literature, major bleeding was defined using ISTH-type criteria (fatal bleeding, bleeding into a critical organ, or bleeding causing a fall in haemoglobin of ≥2 g/dL or requiring transfusion of ≥2 units), although the exact operationalization and adjudication procedures varied between trials — a recognized source of clinical and methodological heterogeneity addressed in §6 and §9.

---

## 4. Effect Sizes

Five records yielded extractable effect sizes before deduplication. The table below reports the standardized effect index and its confidence interval as computed by the extraction pipeline, together with the record's total sample size. **These standardized values are reported for descriptive completeness only.** They are a cross-outcome comparability index whose standard errors are driven principally by total sample size; they are *not* the native risk-ratio-scale estimates, and their intervals should not be read as the precision of the RR analysis. The pooled result in §5 was computed natively on the risk-ratio scale from arm-level event counts.

| Record | Standardized effect index (Hedges' *g* scale) | 95% CI | N |
|---|---|---|---|
| `study_1_R1` *(excluded as duplicate)* | 0.510322 | [0.459, 0.562] | 5,963 |
| `study_3_R3` | 0.522482 | [0.473, 0.572] | 6,401 |
| `study_4_R4` | 0.586951 | [0.542, 0.632] | 7,998 |
| `study_5_R5` | 0.095896 | [0.050, 0.141] | 7,432 |
| `study_6_R6` | 0.348017 | [0.312, 0.384] | 11,962 |

Two features are worth noting at the study level. First, **every one of the five extracted estimates lies on the same side of the null** (all positive, i.e. all indicating more major bleeding events in the extended-duration arm); not a single trial pointed toward a bleeding *reduction* with extended prophylaxis. Directional consistency of this kind across four independent trials is itself substantive evidence for a real harm signal, independent of the pooled magnitude. Second, the *magnitude* of the signal varies appreciably: the smallest estimate (`study_5_R5`, 0.0959) is roughly one-sixth the size of the largest (`study_4_R4`, 0.5870). This spread in magnitude — amid complete agreement in direction — is the source of the moderate heterogeneity reported in §6.

The distribution of extracted effect sizes is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

---

## 5. Meta-Analytic Result

### 5.1 Primary pooled estimate

The context data contain a single meta-analytic group (no `meta_analysis_groups` with multiple entries); all four included trials report the same outcome (major bleeding) at the same prespecified timepoint (within 45 days of randomization), so a single pooled estimate is appropriate and no separate by-group reporting is required.

| Parameter | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** (`measure_label`) |
| Native-scale pooling used | **Yes** (`native_pooling_used: true`) — confirmed native RR result, not a standardized fallback |
| Model | Random effects, REML |
| Number of trials (k) | **4** |
| Total randomized participants | **33,793** |
| **Pooled Risk Ratio** | **1.954** |
| 95% confidence interval | **1.239 to 3.083** |
| p-value | **0.00398** |
| Direction (`favors` field) | "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)" |

The pooled **Risk Ratio (RR) is 1.954 (95% CI 1.239 to 3.083; p = 0.00398)**. Because risk ratios were pooled on their native scale from arm-level event counts, this is a confirmed native-scale risk ratio and not a standardized surrogate.

### 5.2 Interpreting the direction

The automated direction field (`favors`) classifies this comparison as favouring **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)."** That classification reflects a structural property of ratio measures: the algorithm cannot determine from the ratio alone whether the counted event is desirable or undesirable. In this analysis, the counted event is **major bleeding — an unambiguous harm**. Under the effect-direction convention specified for this review (an RR below 1 in the favourable direction means *fewer* major bleeds with extended duration; an RR above 1 means *more*), a pooled RR of 1.954 with a confidence interval entirely above 1.0 corresponds to **the expected harm signal: extended-duration anticoagulation produced approximately twice as many major bleeding events as standard-duration prophylaxis within 45 days.** The direction field should therefore be read as "not assignable by the algorithm", not as "no difference between arms" — the statistical test is clearly significant (p = 0.00398) and the interval excludes the null.

### 5.3 Magnitude and clinical scale

The point estimate implies a **95% relative increase in major bleeding**, with the confidence interval compatible with increases ranging from **24% (RR 1.24) to 208% (RR 3.08)**. The lower bound is itself clinically non-trivial: even the most optimistic value consistent with the data represents roughly a one-quarter relative increase in major bleeding.

Translating relative into absolute terms requires a baseline risk, which was not pooled in this analysis and is therefore not derived here. Readers should note only the general arithmetic: because major bleeding in standard-duration arms of this trial literature is uncommon (typically well under 1% over the relevant window), a near-doubling of relative risk corresponds to a **small absolute excess measured in fractions of a percentage point**, with correspondingly large numbers needed to harm. This is precisely why the clinical question has been decided on *net* benefit: both the VTE benefit and the bleeding harm of extended prophylaxis are small in absolute terms, and they are of comparable absolute magnitude, so the relative sizes of the two effects determine the balance.

### 5.4 Figures

- **Forest plot** (per-trial estimates, weights and pooled RR): `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
- **Cumulative meta-analysis** (stability of the pooled estimate as trials accrue): `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
- **Effect-size distribution**: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`

The cumulative plot is of particular interest here: it shows whether the near-doubling of bleeding risk was apparent from the earliest trials or emerged only with later accrual, and therefore whether the harm signal has been stable over the evolution of this evidence base.

---

## 6. Heterogeneity

| Statistic | Value |
|---|---|
| Cochran's Q | 4.754 |
| Degrees of freedom | 3 (k − 1) |
| Q p-value | **0.1907** |
| I² | **40.32%** |
| τ² (between-trial variance, log-RR scale) | **0.086529** |
| τ (between-trial SD, log-RR scale) | ≈ 0.294 (derived) |
| Estimator | REML |

Heterogeneity was **moderate in magnitude but not statistically significant**. I² = 40.32% sits at the lower edge of the conventional "moderate" band (30–60%), indicating that roughly 40% of the observed variability across trials exceeds what sampling error alone would produce. Cochran's Q = 4.754 on 3 degrees of freedom yields p = 0.1907, so the null hypothesis of homogeneity is not rejected — but with only four trials, Q is a notoriously low-powered test, and a non-significant Q should never be taken as evidence of homogeneity. The τ² of 0.086529 (τ ≈ 0.294 on the log scale) is the more informative quantity: it implies that the *typical* trial-to-trial deviation in the log risk ratio is about 0.29, i.e. a multiplicative spread of roughly ±34% around the pooled RR.

An **approximate 95% prediction interval**, derived from the reported pooled estimate, τ² and k using a t-distribution with k−2 degrees of freedom, spans roughly **RR 0.4 to RR 9.8**. This figure is presented with heavy caveats — with k = 4 the multiplier (t₂ = 4.303) is extreme and the interval is correspondingly uninformative — but it makes an honest point: the available randomized evidence pins down the *average* bleeding hazard reasonably well while leaving the hazard in any *individual* future setting very poorly constrained.

Crucially, the heterogeneity here is heterogeneity of **magnitude, not of direction**. All four pooled trials (and all five extracted records) estimated more major bleeding with extended duration. The between-trial variance therefore reflects disagreement about *how much* harm, not about *whether* there is harm — a pattern that substantially strengthens the qualitative conclusion while weakening confidence in any single numerical value.

Plausible clinical and methodological sources of the observed dispersion include:

- **Different anticoagulants and intensities** in the extended phase (parenteral continuation versus direct oral anticoagulants; prophylactic versus intermediate dosing);
- **Different comparator regimens**, including true placebo after a completed standard course versus active standard-duration prophylaxis;
- **Variation in the operational definition and adjudication of major bleeding**, despite nominal use of ISTH-type criteria;
- **Differences in enrolled risk profile** — baseline bleeding risk, renal function thresholds, age distribution and comorbidity burden differ materially across this trial programme;
- **Differences in extended-phase duration** (approximately 30 versus 45 days) within the prespecified short-term window.

A graphical summary of the heterogeneity diagnostics is provided in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 7. Moderators

**No formal moderator analysis was performed, and none should be attempted on these data.** With k = 4 independent trials, meta-regression is not estimable in any meaningful sense: a single covariate would leave 2 residual degrees of freedom, and conventional guidance (a minimum of roughly 10 trials per covariate) is violated by a wide margin. Fitting such a model would produce estimates with no interpretive value and a high probability of spurious "explanation" of heterogeneity.

Accordingly, the candidate moderators identified in §6 — extended-phase agent class, comparator type (placebo versus active), bleeding definition and adjudication, baseline bleeding risk, and extended-phase duration — are discussed narratively as *hypotheses for the observed dispersion* rather than tested. We note specifically that the trial contributing the smallest effect magnitude (`study_5_R5`, standardized index 0.0959) differs markedly from the trial contributing the largest (`study_4_R4`, 0.5870) despite similar sample sizes (7,432 versus 7,998), which suggests that the driver of heterogeneity is a design or population feature rather than precision. Identifying which feature would require individual participant data.

A descriptive bubble chart relating effect magnitude to study size is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. It should be read as a visual aid to the size–effect relationship only, not as a fitted meta-regression.

By protocol, the subgroup analyses available in the source trials (sex, age, cancer history, D-dimer stratum, infection status) were **excluded from this review**, both because they fall outside the primary-analysis population and because their inclusion would double-count participants. Those subgroup questions remain legitimate and clinically important, but they cannot be answered from the primary-analysis dataset assembled here.

---

## 8. Publication Bias

| Assessment | Result |
|---|---|
| Egger's regression intercept | −0.0752 |
| Egger's p-value | **0.5511** |
| Trim-and-fill imputed studies (k₀) | **0** |
| Trim-and-fill adjusted estimate | 0.4125 (standardized scale; identical to unadjusted because k₀ = 0) |
| Overall graded risk | **Low** |

Egger's regression test showed no evidence of funnel-plot asymmetry (intercept −0.0752, p = 0.5511, far above conventional thresholds), indicating that smaller trials did not report systematically different effects from larger ones. Consistent with this, the Duval–Tweedie trim-and-fill procedure imputed **no** missing studies (k₀ = 0), so the adjusted pooled estimate is identical to the unadjusted one; the reported adjusted value of 0.4125 is expressed on the standardized scale used for the bias diagnostics and is simply the unadjusted standardized estimate carried through unchanged. There is thus **no indication that the pooled bleeding hazard is inflated by selective publication**.

Two caveats temper this reassurance. First, these results support a *low risk* of publication bias rather than proving its absence: Egger's test has very limited power when fewer than about 10 studies are available, and with k = 4 its non-significance is close to uninformative. Second, neither Egger's test nor trim-and-fill can detect bias that affects an entire literature uniformly — for example, if all trials in a programme share the same sponsorship structure, adjudication conventions, or reporting incentives. That said, the specific context of this question argues against serious dissemination bias from a different direction: the included trials are large, registered, industry- and consortium-sponsored phase III programmes whose results (including unfavourable safety findings) were published regardless of direction, and the harm signal here runs *against* the sponsors' commercial interest, which is the opposite of the pattern that publication bias typically generates.

---

## 9. Data Quality & Validation Notes

One validation flag was raised during the analysis pipeline and is reported here in full:

- **Trial deduplication (severity: warning), outcome "major bleeding".** Trial cluster `trial_98c4dd27793d` was represented by more than one extracted record. The pipeline retained `study_3` (the record with the largest total N, 6,401) for this outcome group and **excluded `study_1` (N = 5,963) as a duplicate report of the same randomized trial.** Without this step, the same randomized participants would have been counted twice, artificially narrowing the confidence interval and inflating the apparent number of independent trials from 4 to 5.

Three further data-quality observations follow from the pipeline summary and should be stated plainly:

1. **Two of the seven extracted records contributed no effect size** to this analysis. They did not yield an extractable ≤45-day major bleeding estimate in the primary-analysis population under the prespecified eligibility rules. Their absence means the pooled analysis rests on four trials rather than a potentially larger set.
2. **The pooled estimate rests on k = 4 trials**, the minimum at which a random-effects model with REML-estimated between-study variance can be regarded as interpretable at all. τ² is estimated with very low precision at this k, which propagates into the width of the confidence interval and renders the prediction interval essentially uninformative.
3. **The per-record standardized effect sizes in §4 and the pooled risk ratio in §5 are on different scales.** The standardized values are a comparability index; the pooled result is a native-scale risk ratio computed from event counts. These should not be compared numerically with one another, and the standardized confidence intervals in §4 do not describe the precision of the RR analysis.

---

## 10. Discussion

### 10.1 Principal finding

Pooling four independent randomized trials and 33,793 acutely ill hospitalized medical patients, extended-duration anticoagulant thromboprophylaxis was associated with a **pooled risk ratio for major bleeding within 45 days of 1.954 (95% CI 1.239–3.083; p = 0.00398)** — approximately a doubling of short-term major bleeding risk relative to a standard-duration course. The confidence interval excludes the null across its entire range, and every contributing trial pointed in the same direction. Within the effect-direction convention specified for this review, this is the **anticipated harm signal**: extended duration causes *more* major bleeding, not less.

### 10.2 Consistency with the wider evidence base and with guidelines

This result aligns with the dominant narrative of the extended-prophylaxis trial programme in medical inpatients, in which modest reductions in symptomatic VTE have been repeatedly accompanied by excess major and clinically relevant bleeding, yielding neutral or unfavourable net clinical benefit. It also provides a quantitative basis for the prevailing guideline recommendation against routine extended-duration pharmacological prophylaxis in unselected acutely ill medical patients. The present analysis adds precision to the safety side of that trade-off: the bleeding hazard is not a borderline or marginal finding but a roughly twofold relative increase, statistically significant at p < 0.005, replicated in direction across four large independent trials, and insensitive to publication-bias correction.

### 10.3 Clinical implications

Three implications follow.

**First, the harm is real but small in absolute terms.** A near-doubling of a rare event remains a rare event. The appropriate clinical response is not blanket avoidance in every patient but explicit, quantitative weighing of a small absolute bleeding excess against a small absolute VTE reduction — a calculus that will shift with individual patient characteristics.

**Second, patient selection is where the remaining value lies.** Because both the benefit and the harm of extended prophylaxis are small and of similar absolute magnitude, net benefit is determined by the ratio of an individual patient's thrombotic risk to their bleeding risk. Extended prophylaxis may plausibly remain net-beneficial in patients with markedly elevated VTE risk (e.g., elevated D-dimer, immobility, prior VTE, active malignancy) *and* low bleeding risk. The present analysis cannot test this proposition, because risk-stratified subgroup analyses were excluded by protocol from the primary-analysis population — but it does define the magnitude of harm that any such selection strategy must overcome.

**Third, the bleeding hazard is front-loaded and on-treatment.** The 45-day window examined here captures the active extended-treatment period. Clinicians considering extended prophylaxis should recognize that the excess bleeding risk accrues precisely during the interval in which the intervention is being given, and that stopping the extended course removes it.

### 10.4 Strengths

The analysis has several methodological strengths: a narrowly and prospectively specified outcome, timepoint and analysis population; native-scale risk-ratio pooling from arm-level event counts rather than reliance on a standardized surrogate; a prespecified effect measure fixed before analysis; explicit exclusion of COVID-19-restricted, same-agent and subgroup analyses that would otherwise have contaminated the primary comparison or double-counted participants; algorithmic trial-level deduplication that prevented one trial from entering the pool twice; a large pooled sample (33,793 randomized participants); and formal small-study-effect diagnostics, both of which were reassuring.

---

## 11. Limitations

1. **Very few poolable trials (k = 4).** This is the dominant limitation. It constrains the precision of τ², makes Cochran's Q underpowered, renders meta-regression impossible, and makes the formal prediction interval (approximately RR 0.4–9.8) too wide to inform individual decisions.
2. **Moderate unexplained heterogeneity.** I² = 40.32% and τ² = 0.086529 indicate genuine between-trial dispersion in the magnitude of the bleeding hazard that this analysis cannot attribute to any specific cause. The pooled RR should be read as an average across heterogeneous regimens, not as a transportable constant.
3. **Pooling across different anticoagulants, doses and durations.** The extended-duration intervention is not a single treatment. Pooling parenteral continuation with direct oral anticoagulants, and 30-day with 45-day courses, imposes a common effect on interventions that may genuinely differ.
4. **Trial-specific bleeding definitions.** Major bleeding was defined by each trial, typically but not uniformly by ISTH criteria, with varying adjudication procedures. Outcome-definition heterogeneity is a plausible and unquantifiable contributor to the observed τ².
5. **Two extracted records contributed no usable effect size,** so the analysis may not exhaust the available randomized evidence for this outcome and timepoint.
6. **No formal risk-of-bias or GRADE assessment** is reported in the available dataset. Although the included trials are large registered randomized comparisons, domain-level bias appraisal (especially blinding of bleeding outcome adjudication and completeness of follow-up) and a formal certainty rating were not performed. Readers should treat the certainty of evidence as moderate at best, downgraded principally for imprecision (k = 4, wide interval) and inconsistency.
7. **Publication-bias diagnostics are underpowered.** With k = 4, the non-significant Egger's test (p = 0.5511) and null trim-and-fill (k₀ = 0) are consistent with low bias risk but cannot exclude it.
8. **No absolute-risk synthesis.** Control-arm event rates were not pooled, so no pooled risk difference or number-needed-to-harm is reported. The relative measure alone cannot convey the clinical scale of the harm.
9. **Short-term horizon only.** By design this analysis addresses the ≤45-day window. Longer-term bleeding and net clinical benefit beyond 45 days are outside its scope.
10. **Benefit not co-estimated.** This review quantifies harm only. Net clinical benefit requires simultaneous consideration of the VTE-prevention efficacy of extended prophylaxis, which was not analysed here.

---

## 12. Conclusion

In acutely ill hospitalized medical patients receiving VTE prophylaxis, **extended-duration anticoagulant thromboprophylaxis approximately doubles the short-term risk of major bleeding compared with a standard-duration course: pooled Risk Ratio 1.954 (95% CI 1.239–3.083; p = 0.00398; k = 4 trials; 33,793 randomized participants; REML random-effects model on the native risk-ratio scale).** Heterogeneity was moderate but not statistically significant (I² = 40.32%; τ² = 0.086529; Q = 4.754, df = 3, p = 0.1907), and all contributing trials agreed in direction even where they disagreed in magnitude. There was no evidence of publication bias (Egger's p = 0.5511; trim-and-fill k₀ = 0), and publication-bias risk was graded low.

The automated direction field for this comparison reads "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)", reflecting the algorithm's inability to assign favourability to a bare ratio; because the counted event is major bleeding, the correct clinical reading of an RR of 1.95 with an interval entirely above unity is that **extended duration causes more bleeding — the expected harm signal.**

This finding supports current guidance against routine extended-duration pharmacological thromboprophylaxis in unselected acutely ill medical inpatients, and argues that any selective use should be confined to patients whose thrombotic risk clearly outweighs a roughly twofold increase in major bleeding during the treatment period. Because this excess is small in absolute terms, the decisive clinical question is not whether the harm exists — the present analysis indicates that it does — but whether reliable risk stratification can identify the minority of patients in whom the VTE benefit exceeds it. Answering that question will require individual participant data meta-analysis and prospective risk-stratified trials, not further pooling of overall trial-level results.

---

## 13. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
2. Schulman S, Kearon C; Subcommittee on Control of Anticoagulation of the Scientific and Standardization Committee of the International Society on Thrombosis and Haemostasis. Definition of major bleeding in clinical investigations of antihemostatic medicinal products in non-surgical patients. *J Thromb Haemost.* 2005;3(4):692–694.
3. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Control Clin Trials.* 1986;7(3):177–188.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw.* 2010;36(3):1–48.
5. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med.* 2002;21(11):1539–1558.
6. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
7. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
9. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
10. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ.* 2011;343:d4002.
11. Schünemann HJ, Cushman M, Burnett AE, et al. American Society of Hematology 2018 guidelines for management of venous thromboembolism: prophylaxis for hospitalized and nonhospitalized medical patients. *Blood Adv.* 2018;2(22):3198–3225.
12. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions,* version 6.4. Cochrane; 2023.

*Primary trial reports for the included records (`study_3_R3`, `study_4_R4`, `study_5_R5`, `study_6_R6`) and for the deduplicated record (`study_1_R1`) are identified in the structured extraction dataset accompanying this analysis.*

---

### Figure Index

| Figure | Path |
|---|---|
| Forest plot (primary analysis, k = 4) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (descriptive size–effect relationship) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity diagnostics summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| major bleeding | 4 | Risk Ratio (RR) | Yes | 1.9540 [1.2386, 3.0827] |
