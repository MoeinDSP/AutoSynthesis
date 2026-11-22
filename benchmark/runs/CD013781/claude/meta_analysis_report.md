# Perioperative Levosimendan versus Placebo and All-Cause Mortality in Adult Cardiac Surgery: A PRISMA-Compliant Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Low cardiac output syndrome is a leading driver of mortality after cardiac surgery. Levosimendan, a calcium-sensitising inodilator with ATP-sensitive potassium channel–opening properties, has been proposed as a perioperative cardioprotective agent, but individual randomised trials have been underpowered for mortality and large pragmatic trials have reported null results.

**Objective.** To quantify the effect of perioperative levosimendan infusion compared with placebo on all-cause mortality in adults undergoing cardiac surgery.

**Methods.** A systematic search and screening pipeline identified 13 eligible primary randomised reports, of which 10 contributed extractable all-cause mortality data (deaths and number randomised per arm; in-hospital, 30-day, or longest reported follow-up). One document was excluded from the primary-study set at the document-type gate because it was itself a PRISMA-compliant, PROSPERO-registered network meta-analysis of 29 trials. Effects were pooled on the native risk-ratio scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Cochran's Q, I² and τ². Publication bias was assessed with Egger's regression test and Duval–Tweedie trim-and-fill.

**Results.** Ten trials randomising 1,875 patients were pooled. The pooled Risk Ratio (RR) for all-cause mortality was 0.681 (95% CI 0.428 to 1.084; p = 0.1056; k = 10; N = 1,875), a point estimate corresponding to an approximately 32% relative reduction in deaths with levosimendan, but with a confidence interval that crosses the line of no effect. In accordance with the pipeline's direction field, the pooled result favours *neither* arm — it is statistically indeterminate, and for this ratio measure favourability depends on which event was counted. Native risk-ratio pooling was confirmed (native_pooling_used = true; effect measure specified by explicit user request), so the result is a confirmed native-scale risk ratio rather than a standardised fallback. Heterogeneity was low and non-significant (I² = 20.45%, τ² = 0.1059, Q = 9.534, df = 9, p = 0.3895). Egger's test showed no significant funnel asymmetry (intercept = −0.1116, p = 0.3577) and trim-and-fill imputed only one hypothetically missing study (k₀ = 1; adjusted estimate −0.3205 on the analysis scale, ≈ RR 0.73); overall publication-bias risk was nonetheless rated **moderate** because these diagnostics are underpowered at k = 10.

**Conclusions.** Perioperative levosimendan was associated with a point estimate suggesting fewer deaths than placebo after adult cardiac surgery, but the effect was not statistically significant and the evidence does not establish a mortality benefit. The confidence interval remains compatible with both a clinically important reduction and a small increase in mortality. Heterogeneity was low, so the imprecision reflects limited event numbers rather than conflicting effects. Routine prophylactic use cannot be recommended on mortality grounds; targeted use in high-risk subgroups warrants adequately powered confirmatory trials.

**Registration.** Not registered; retrospective synthesis of an automated evidence-screening pipeline.

# Introduction

Cardiac surgery with cardiopulmonary bypass exposes the myocardium to ischaemia–reperfusion injury, and post-operative low cardiac output syndrome (LCOS) occurs in roughly 3–14% of patients, carrying a several-fold increase in mortality, renal replacement therapy, and intensive care unit length of stay. Conventional inotropes (catecholamines, phosphodiesterase-III inhibitors) increase myocardial oxygen consumption and intracellular calcium loading, and observational data have linked their use to adverse outcomes.

Levosimendan is a calcium-sensitising inodilator that augments contractility by stabilising the troponin C–calcium complex without increasing cytosolic calcium, and opens mitochondrial and sarcolemmal ATP-sensitive potassium channels, conferring a putative preconditioning-like cardioprotective effect. Its long-acting metabolite OR-1896 sustains haemodynamic effects for up to a week, making it biologically plausible as a *perioperative prophylactic* rather than purely a rescue agent.

Early single-centre randomised controlled trials (RCTs) reported striking reductions in LCOS, inotrope requirement, and mortality, and earlier meta-analyses of these small trials suggested a survival benefit. However, three large multicentre placebo-controlled trials published subsequently were neutral for their primary composite endpoints, prompting the question of whether the earlier mortality signal was an artefact of small-study effects, heterogeneous risk profiles, and sparse events. This systematic review and meta-analysis addresses a single, focused question:

> **What is the effect of perioperative levosimendan compared with placebo on all-cause mortality in adults undergoing cardiac surgery?**

A pooled risk ratio below 1 in the favourable direction indicates fewer deaths in the levosimendan arm.

---

# Methods

## Search and Screening

Records were identified through an automated systematic search-and-screening pipeline covering bibliographic databases of randomised controlled trials of levosimendan in adult cardiac surgery. Eligibility followed PICO criteria:

- **Population (P):** adults (≥18 years) undergoing cardiac surgery (coronary artery bypass grafting, valve surgery, or combined procedures), with or without reduced left ventricular ejection fraction.
- **Intervention (I):** perioperative intravenous levosimendan infusion (pre-operative, intra-operative, or initiated at induction/ICU admission), at any dose, with or without a loading bolus.
- **Comparator (C):** placebo.
- **Outcome (O):** all-cause mortality, reported as the number of deaths and the total number randomised in each arm, at any of in-hospital, 30-day, or longest reported follow-up.
- **Study design (S):** randomised controlled trial reporting primary data.

Screening proceeded in stages: (i) a **document-type gate** that removed non-primary evidence (systematic reviews, network meta-analyses, narrative reviews, editorials, protocols); (ii) a **PICO relevance gate**; (iii) an **outcome-extractability gate** requiring arm-level deaths and denominators; and (iv) a **de-duplication check** to prevent double-counting of multiple reports of the same trial cohort.

The document-type gate excluded one record (identifier `manual:f7d556cc`) that was explicitly a PRISMA-compliant, PROSPERO-registered **network meta-analysis** pooling 29 RCTs (4,509 patients), complete with search strategy, risk-of-bias assessment, SUCRA rankings, and pooled standardised mean differences. Because this document reports synthesis across studies rather than primary data collection, including it would have duplicated the primary trials already captured. This exclusion is logged in the *Data Quality & Validation Notes* section.

Thirteen primary randomised reports passed screening and constitute the included-study set. Of these, **10 contributed extractable all-cause mortality data** in the required deaths/total format and entered the quantitative synthesis; the remaining 3 were retained in the review but could not be pooled because arm-level mortality counts were not recoverable from the available report.

## Data Extraction and Effect-Size Computation

For each pooled trial, the number of deaths and the number randomised were extracted for the levosimendan and placebo arms. Because the outcome is binary, the **risk ratio (RR)** was pre-specified as the effect measure (`effect_measure_source = explicit_user_request`), and pooling was performed **natively on the log-risk-ratio scale** (`native_pooling_used = true`, `computation_scale = RR`). No effect-measure conflict was detected (`effect_measure_conflict = null`). The pooled estimate reported below is therefore a **confirmed native-scale Risk Ratio (RR)** and not a standardised or back-transformed fallback.

For display and cross-study comparability, the pipeline additionally computed a standardised per-study effect size (Hedges' *g*) for each trial. These standardised values are reported in the *Effect Sizes* section for descriptive purposes only; they are **not** the metric of the pooled result, and the pooled result must not be described as a Hedges' *g*.

## Statistical Synthesis

A random-effects model with **restricted maximum likelihood (REML)** estimation of τ² was fitted to the log risk ratios, with results exponentiated for presentation. Heterogeneity was characterised by Cochran's Q, the I² statistic, and τ². Publication bias and small-study effects were evaluated with Egger's regression test of funnel-plot asymmetry and the Duval–Tweedie trim-and-fill procedure. A two-sided α of 0.05 was used throughout. Only one outcome/timepoint group was defined by the pipeline (no `meta_analysis_groups` with multiple entries), so a single pooled analysis is reported.

---

# Included Studies

Thirteen primary randomised reports met eligibility criteria. Ten provided analysable all-cause mortality data and were pooled, together randomising **1,875 patients**. Trial sizes spanned two orders of magnitude, from 24 to 849 randomised participants:

| Study ID | Participants randomised (N) | Size stratum |
|---|---|---|
| study_1_R1 | 50 | small |
| study_3_R3 | 40 | small |
| study_4_R4 | 33 | small |
| study_7_R7 | 200 | medium |
| study_8_R8 | 252 | medium |
| study_9_R9 | 32 | small |
| study_10_R10 | 60 | small |
| study_11_R11 | 24 | small |
| study_12_R12 | 335 | large |
| study_13_R13 | 849 | large |
| **Total (k = 10)** | **1,875** | — |

Seven of the ten pooled trials enrolled fewer than 100 patients, while the two largest trials (study_13_R13, N = 849; study_12_R12, N = 335) together account for 63.1% of the pooled sample. This asymmetric size distribution is central to interpreting both the pooled estimate and the small-study diagnostics below.

Three of the 13 included reports could not be entered into the quantitative synthesis because arm-level death counts and denominators were not extractable; they are described narratively and do not contribute to any pooled statistic reported here.

---

# Effect Sizes

Per-study standardised effect sizes (Hedges' *g*) with 95% confidence intervals, as computed by the pipeline for display, are shown below. Negative values indicate an effect in the direction of fewer deaths in the levosimendan arm; positive values indicate the opposite. Again, these are descriptive standardised quantities — the pooled synthesis was performed on the native risk-ratio scale.

| Study ID | Standardised effect (Hedges' *g*) | 95% CI | N | Direction |
|---|---|---|---|---|
| study_1_R1 | −0.6434 | [−1.212, −0.075] | 50 | favours levosimendan (CI excludes 0) |
| study_3_R3 | −0.6538 | [−1.290, −0.018] | 40 | favours levosimendan (CI excludes 0) |
| study_4_R4 | −0.7026 | [−1.406, 0.001] | 33 | favours levosimendan (CI touches 0) |
| study_7_R7 | +0.0122 | [−0.265, 0.289] | 200 | null |
| study_8_R8 | −0.7013 | [−0.956, −0.447] | 252 | favours levosimendan (CI excludes 0) |
| study_9_R9 | −0.9344 | [−1.664, −0.205] | 32 | favours levosimendan (CI excludes 0) |
| study_10_R10 | −0.9127 | [−1.444, −0.381] | 60 | favours levosimendan (CI excludes 0) |
| study_11_R11 | +0.6292 | [−0.191, 1.449] | 24 | favours placebo (CI includes 0) |
| study_12_R12 | +0.1723 | [−0.042, 0.387] | 335 | favours placebo (CI includes 0) |
| study_13_R13 | −0.1440 | [−0.279, −0.009] | 849 | favours levosimendan (CI narrowly excludes 0) |

Descriptively, the distribution is bimodal with respect to trial size. Six of the seven trials with N < 100 or mid-sized single-centre design (study_1_R1, study_3_R3, study_4_R4, study_8_R8, study_9_R9, study_10_R10) yielded moderate-to-large effects in favour of levosimendan (*g* between −0.64 and −0.93), whereas the two largest trials produced much smaller effects in opposite directions (study_13_R13, *g* = −0.144; study_12_R12, *g* = +0.172) and one medium trial was precisely null (study_7_R7, *g* = +0.012). The single most extreme effect favouring placebo came from the smallest trial in the set (study_11_R11, N = 24, *g* = +0.629), whose confidence interval spans a width of 1.64 units and is therefore uninformative in isolation.

The per-study forest plot is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`, and the distribution of effect sizes across studies at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

---

# Meta-Analytic Result

A single outcome group was analysed (all-cause mortality: in-hospital, 30-day, or longest reported follow-up, as reported by each trial).

| Quantity | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** (`measure_label`) |
| Native-scale pooling confirmed | **Yes** (`native_pooling_used = true`) |
| Pooling model | Random effects, REML |
| Number of trials (k) | 10 |
| Total participants (N) | 1,875 |
| **Pooled Risk Ratio (RR)** | **0.681** |
| 95% confidence interval | **0.428 to 1.084** |
| p-value | **0.1056** |
| τ² | 0.1059 |
| I² | 20.45% |
| Cochran's Q (df = 9) | 9.534 (p = 0.3895) |
| Direction (`favors`) | **neither** — essentially a tie, or a ratio measure where favourability depends on which event was counted |

The pooled **Risk Ratio (RR) was 0.681 (95% CI 0.428 to 1.084; p = 0.1056)**. Taken at face value, the point estimate corresponds to a **31.9% relative reduction** in all-cause mortality with perioperative levosimendan. However, the 95% confidence interval crosses the null value of 1.0 and the result does not reach conventional statistical significance.

Consistent with the pipeline's `favors` field, this pooled result **favours neither arm**: it is statistically indeterminate. The interval is compatible with effects ranging from a substantial 57% relative reduction in mortality (RR 0.428) to an 8% relative *increase* (RR 1.084). Because this is a ratio measure of a harm event, the apparent favourability of a value below 1 depends on the event actually counted being death; readers should not over-interpret the sign of the point estimate as a demonstrated benefit.

Because native risk-ratio pooling was confirmed and the measure was explicitly specified, this value is a **confirmed native-scale risk ratio**, not a standardised fallback requiring caveated back-transformation.

An approximate 95% prediction interval, derived from the reported pooled standard error and τ², spans roughly **RR 0.27 to 1.72**, indicating that the true effect in a new, exchangeable trial could plausibly be either a large benefit or a moderate harm.

---

# Heterogeneity

Between-study heterogeneity was **low and statistically non-significant**:

- **Cochran's Q = 9.534** on 9 degrees of freedom, **p = 0.3895** — the observed dispersion of effects is entirely consistent with sampling error alone.
- **I² = 20.45%** — only about one-fifth of the observed variability in effects is attributable to true between-study differences rather than chance; by conventional thresholds this falls in the "low" band (<40%).
- **τ² = 0.1059** (on the log-risk-ratio scale, τ ≈ 0.326) — a modest but non-zero estimate of true between-study variance in log risk ratios.

This combination is informative. The non-significant Q and low I² indicate that the apparent visual contrast between the small positive trials and the large neutral trials is not statistically resolvable at this sample size: the small trials have wide confidence intervals that overlap substantially with the large trials' estimates, so the data do not demonstrate genuinely conflicting treatment effects. At the same time, τ² is not zero, and because I² is a *relative* measure it is attenuated when within-study variance is large (as it is here, with seven trials under N ≈ 100 and sparse mortality events). The modest τ² is therefore the more consequential statistic clinically — it is what widens the prediction interval to RR 0.27–1.72 despite the Q test's reassurance.

In short: the **failure to reach significance in this meta-analysis is driven by imprecision (too few deaths), not by heterogeneity (conflicting effects)**. A heterogeneity summary visualisation is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

# Moderators

No pre-specified moderator variables (e.g., baseline left ventricular ejection fraction, procedure type, timing and duration of infusion, use of a loading bolus, cumulative dose, single- versus multi-centre design, year of publication, or risk-of-bias domain ratings) were extracted in structured form by the pipeline, and **no formal meta-regression or subgroup analysis was performed**. With k = 10 trials, any meta-regression would in any case have been severely underpowered — a widely used rule of thumb requires approximately 10 studies per covariate, so even a single moderator could not be estimated reliably, and the non-significant Q test (p = 0.3895) indicates there is little systematic between-study variance available for a moderator to explain.

The following observations are therefore **exploratory and hypothesis-generating only**, based on inspection of the relationship between trial size and effect magnitude (bubble chart: `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`):

1. **Trial size appears to track effect magnitude.** Trials with N ≤ 252 contributed standardised effects between −0.64 and −0.93 in five instances, while the two largest trials (N = 335 and N = 849) contributed effects of +0.172 and −0.144 respectively. This pattern is the classic signature of a small-study effect, which may reflect publication bias, outcome-reporting flexibility, less rigorous allocation concealment and blinding in smaller single-centre trials, or genuine differences in the baseline risk of the enrolled populations.

2. **Baseline risk is a plausible effect modifier.** Smaller early trials frequently enrolled highly selected patients with severely reduced ejection fraction, in whom the absolute mortality risk — and hence the absolute benefit achievable from a cardioprotective inodilator — is greatest. Larger pragmatic trials enrolled broader populations with lower event rates, mechanically diluting any relative effect and reducing power. This remains an untested hypothesis in the present dataset.

3. **Infusion timing and dose** (pre-operative initiation versus initiation after induction or at ICU admission; bolus versus no bolus) differ across the levosimendan literature and are biologically plausible moderators given the agent's active metabolite kinetics, but were not available for analysis here.

These candidate moderators should be addressed in an individual-participant-data meta-analysis rather than inferred from the aggregate pattern described above.

---

# Publication Bias

Two complementary small-study diagnostics were applied:

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | −0.1116 |
| Egger's test p-value | 0.3577 |
| Trim-and-fill imputed studies (k₀) | 1 |
| Trim-and-fill adjusted estimate | −0.3205 (analysis scale; ≈ RR 0.73 when exponentiated) |
| Overall risk rating | **Moderate** |

**Interpretation.** Egger's regression test showed no statistically significant funnel-plot asymmetry (intercept = −0.1116, p = 0.3577), and the trim-and-fill procedure imputed only one hypothetically missing study (k₀ = 1), suggesting that any small-study effect is minor and unlikely to materially shift the pooled estimate. Taken together, these diagnostics provide **no positive evidence of publication bias**. The trim-and-fill–adjusted estimate (−0.3205 on the analysis scale, approximately RR 0.73) is attenuated relative to the primary estimate of RR 0.681 but remains in the same direction and similarly non-significant, so the conclusion is unchanged under this sensitivity analysis.

However, the **"moderate" risk rating reflects that absence of evidence is not evidence of absence**: Egger's test and trim-and-fill have low statistical power when the number of included studies is small or heterogeneity is high, so meaningful bias cannot be confidently ruled out. Standard guidance discourages funnel-plot asymmetry testing with fewer than 10 studies; at exactly k = 10, and with a markedly skewed distribution of trial sizes and sparse mortality events, the test is at the boundary of interpretability. The pooled result should therefore be regarded as **probably robust but interpreted with some caution**, with the trim-and-fill–adjusted estimate (RR ≈ 0.73) serving as the appropriate conservative sensitivity bound.

The qualitative pattern noted in the *Moderators* section — larger effects in the smallest trials, null-to-neutral effects in the largest — is consistent with a residual small-study effect that the formal tests were insufficiently powered to detect.

---

# Discussion

This meta-analysis of 10 randomised trials and 1,875 adults undergoing cardiac surgery found a pooled **Risk Ratio (RR) for all-cause mortality of 0.681 (95% CI 0.428 to 1.084; p = 0.1056)** for perioperative levosimendan versus placebo. The point estimate suggests an approximately one-third relative reduction in deaths, but the confidence interval includes the null and, per the pipeline's direction field, the result **favours neither arm**. The appropriate conclusion is that this body of evidence **does not establish a mortality benefit of perioperative levosimendan**, while also not excluding a clinically important one.

Three features of the dataset shape this interpretation.

**First, imprecision dominates.** With low heterogeneity (I² = 20.45%, Q p = 0.3895) but a confidence interval spanning RR 0.43 to 1.08, the limiting factor is clearly the number of accrued deaths rather than inconsistency between trials. Mortality after elective cardiac surgery is a relatively rare event (commonly 2–6% even in reduced-ejection-fraction cohorts), so 1,875 randomised patients generate few events and correspondingly wide intervals. Seven of the ten trials randomised fewer than 100 patients and, individually, could never have been powered for mortality.

**Second, the evidence base is structurally asymmetric.** The two largest trials contribute 63.1% of participants and both report near-null effects (standardised *g* = −0.144 and +0.172), whereas the moderate-to-large benefits cluster in the smaller trials. This is the architecture that has repeatedly produced optimistic early meta-analyses later contradicted by adequately powered multicentre trials across critical-care pharmacotherapy. Although Egger's test was non-significant and trim-and-fill imputed only one study, these tests are underpowered at k = 10, and the "moderate" bias rating appropriately withholds reassurance. The attenuated trim-and-fill estimate (≈ RR 0.73) is the more defensible figure for decision-making.

**Third, the biological rationale remains intact even if the mortality signal does not.** Levosimendan's calcium-sensitising and K-ATP channel–opening mechanisms have consistent effects on intermediate haemodynamic endpoints — cardiac index, need for rescue inotropes, duration of mechanical ventilation, and incidence of low cardiac output syndrome — in much of the included literature. A mechanism that reliably improves haemodynamics may nonetheless fail to translate into a survival advantage when baseline mortality is low, when competing causes of death predominate, or when the comparator arm receives effective rescue therapy (including open-label levosimendan), which biases the comparison towards the null in pragmatic trials.

The clinical implication is that **routine prophylactic administration of levosimendan to unselected adult cardiac surgical patients cannot be recommended on the basis of mortality**. The possibility of benefit in enriched high-risk populations — severely reduced left ventricular ejection fraction, combined valve-and-coronary procedures, pre-operative mechanical support — remains open and is the most plausible target for a definitive, adequately powered trial. Such a trial would need to enrol substantially more patients than the entire present evidence base to detect a relative risk reduction of the magnitude suggested here with adequate power.

---

# Data Quality & Validation Notes

The following data-quality flags were raised during screening and synthesis and are reported in full:

1. **One document excluded as non-primary evidence (document-type gate; severity: warning).** Record `manual:f7d556cc` was excluded from the primary-study set because it was classified as a systematic review / meta-analysis. Specifically, it is an explicitly PRISMA-compliant, PROSPERO-registered **network meta-analysis pooling 29 RCTs (4,509 patients)**, with its own search strategy, risk-of-bias assessment, SUCRA rankings, and pooled standardised mean differences — i.e., synthesis across studies rather than primary data collection. Including it alongside the individual trials would have double-counted the underlying participants. Its exclusion does not imply that its findings are unreliable; it simply cannot serve as a unit of analysis in a meta-analysis of primary trials.

2. **Three of 13 included reports contributed no pooled estimate.** Thirteen primary randomised reports passed screening, but only 10 provided all-cause mortality in the required format (deaths and total randomised per arm). The remaining three are described narratively and are excluded from every pooled statistic in this report. This 77% extraction yield means the pooled analysis may not represent the full eligible literature, and the direction of the unextracted data is unknown.

3. **Mixed mortality timepoints were pooled into a single group.** The outcome definition deliberately encompasses in-hospital, 30-day, and longest reported follow-up mortality, and the pipeline defined only one outcome group. Trials contributing different timepoints were therefore combined. This is a pragmatic and common approach for all-cause mortality but introduces definitional heterogeneity that the low measured I² may not fully capture; no separate timepoint-specific pooled estimates could be produced.

4. **Per-study display metric differs from the pooled metric.** The per-study effect sizes are presented as standardised Hedges' *g* values, whereas pooling was performed natively on the log-risk-ratio scale (`measure_label = Risk Ratio (RR)`, `native_pooling_used = true`). The two sets of numbers are on different scales and should not be compared arithmetically; the pooled result is a risk ratio and must not be described as a Hedges' *g*.

5. **No effect-measure conflict and no insufficient-data groups.** The effect measure was specified by explicit user request with no detected conflict, and no analysis group was flagged as having too few studies to pool.

---

# Limitations

1. **Statistical power and imprecision.** With k = 10 trials, 1,875 participants, and a rare outcome, the analysis is underpowered to detect plausible mortality effects. The 95% confidence interval (RR 0.428–1.084) and the approximate prediction interval (RR ≈ 0.27–1.72) both remain compatible with meaningful benefit and with modest harm.

2. **Incomplete outcome extraction.** Three of 13 eligible primary reports could not be pooled. If these differ systematically from the extracted set, the pooled estimate is susceptible to selection bias of unknown direction.

3. **Underpowered bias diagnostics.** At exactly 10 studies with a highly skewed size distribution, Egger's test (p = 0.3577) and trim-and-fill (k₀ = 1) have limited sensitivity. The "moderate" publication-bias rating is a statement of residual uncertainty, not of demonstrated integrity.

4. **No risk-of-bias assessment contributed to this synthesis.** Domain-level risk-of-bias ratings (randomisation, allocation concealment, blinding of participants/personnel/outcome assessors, missing data, selective reporting) were not extracted in structured form, so no risk-of-bias–stratified sensitivity analysis or GRADE certainty rating could be computed. Given that small single-centre trials drive the favourable signal, this is a material gap; by GRADE reasoning the certainty of evidence for mortality would likely be rated no higher than *low*, downgraded for imprecision and suspected publication bias.

5. **No moderator or subgroup analyses.** Clinically critical modifiers — baseline ejection fraction, procedure type, infusion timing, dose, and use of a loading bolus — were unavailable. Clinically meaningful treatment-effect modification cannot be excluded or confirmed.

6. **Heterogeneous outcome timing.** Combining in-hospital, 30-day, and longest follow-up mortality in a single pooled estimate conflates timepoints with different competing-risk structures.

7. **Co-intervention and rescue-therapy contamination.** Open-label rescue inotropes, including levosimendan itself, in the placebo arm of pragmatic trials bias comparisons towards the null; this could not be quantified from aggregate data.

8. **Aggregate-data design.** Study-level synthesis cannot address ecological bias or estimate individual-level effect modification; an individual-participant-data meta-analysis would be required.

9. **No prospective registration.** This synthesis was produced retrospectively from an automated pipeline and was not registered in PROSPERO, so the possibility of analytic flexibility cannot be formally excluded.

---

# Conclusion

Across 10 randomised trials comprising 1,875 adults undergoing cardiac surgery, perioperative levosimendan yielded a pooled **Risk Ratio (RR) for all-cause mortality of 0.681 (95% CI 0.428 to 1.084; p = 0.1056)** compared with placebo, estimated by random-effects REML pooling on the confirmed native risk-ratio scale. Although the point estimate corresponds to an approximately 32% relative reduction in deaths, the confidence interval includes no effect and the result **favours neither arm**. Heterogeneity was low and non-significant (I² = 20.45%, τ² = 0.1059, Q = 9.534, df = 9, p = 0.3895), indicating that the inconclusiveness stems from a shortage of events rather than from conflicting trial results. Formal publication-bias diagnostics were negative (Egger's p = 0.3577; trim-and-fill k₀ = 1, adjusted estimate ≈ RR 0.73) but are underpowered at this number of studies, and the overall bias risk was rated moderate; the concentration of large favourable effects in the smallest trials and near-null effects in the two largest warrants caution.

**Bottom line:** current randomised evidence does not demonstrate that perioperative levosimendan reduces all-cause mortality in adult cardiac surgery, and routine prophylactic use cannot be justified on survival grounds. The data remain compatible with a clinically important benefit in appropriately selected high-risk patients, and resolving this will require an adequately powered multicentre trial with pre-specified mortality endpoints — or an individual-participant-data meta-analysis — rather than further small single-centre studies.

---

# Figures

- **Forest plot** (per-study effects and pooled estimate): `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
- **Effect-size distribution** across included studies: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
- **Bubble chart** (effect size against study precision/size): `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`
- **Heterogeneity summary** (Q, I², τ² visualisation): `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

---

# References

## Included studies (pipeline identifiers)

Ten randomised trials contributed all-cause mortality data to the quantitative synthesis and are identified by their pipeline record labels, as de-identified in the source dataset:

1. study_1_R1 — randomised controlled trial, N = 50.
2. study_3_R3 — randomised controlled trial, N = 40.
3. study_4_R4 — randomised controlled trial, N = 33.
4. study_7_R7 — randomised controlled trial, N = 200.
5. study_8_R8 — randomised controlled trial, N = 252.
6. study_9_R9 — randomised controlled trial, N = 32.
7. study_10_R10 — randomised controlled trial, N = 60.
8. study_11_R11 — randomised controlled trial, N = 24.
9. study_12_R12 — randomised controlled trial, N = 335.
10. study_13_R13 — randomised controlled trial, N = 849.

Three further eligible primary randomised reports (study identifiers retained in the screening log) were included in the systematic review but contributed no pooled estimate because arm-level mortality counts were not extractable.

## Excluded at the document-type gate

11. Record `manual:f7d556cc` — PRISMA-compliant, PROSPERO-registered network meta-analysis of 29 randomised controlled trials (4,509 patients) with SUCRA rankings and pooled standardised mean differences. Excluded as secondary synthesis rather than primary data.

## Methodological references

12. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
13. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
14. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software.* 2010;36(3):1–48.
15. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics.* 2005;30(3):261–293.
16. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
17. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
18. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
19. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ.* 2011;343:d4002.
20. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ.* 2008;336(7650):924–926.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| all-cause mortality | 10 | Risk Ratio (RR) | Yes | 0.6813 [0.4281, 1.0844] |
