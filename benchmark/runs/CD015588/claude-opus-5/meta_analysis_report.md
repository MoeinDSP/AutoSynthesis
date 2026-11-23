# SGLT2 Inhibitors versus Placebo and the Risk of Non-Fatal Myocardial Infarction in Adults with Type 2 Diabetes and Chronic Kidney Disease: A PRISMA-Compliant Systematic Review and Random-Effects Meta-Analysis of Time-to-First-Event Hazard Ratios

## Abstract

**Background.** Sodium–glucose co-transporter-2 (SGLT2) inhibitors reduce heart failure hospitalisation and kidney disease progression in adults with type 2 diabetes, but their effect on atherothrombotic events — and specifically on *non-fatal* myocardial infarction (MI) considered separately from fatal MI or the composite "any MI" endpoint — remains uncertain. Most trials report non-fatal MI only as a secondary or exploratory component, and many report it only as event counts.

**Objective.** To estimate the pooled time-to-first-event hazard ratio (HR) for non-fatal MI with SGLT2 inhibitors versus placebo in adults with type 2 diabetes and chronic kidney disease, including cardiovascular outcome trial populations that enrolled participants with preserved kidney function.

**Methods.** Randomised placebo-controlled trials of canagliflozin, dapagliflozin, empagliflozin, ertugliflozin, bexagliflozin or similar agents were sought. Only adjudicated non-fatal MI HRs with 95% confidence intervals reported in the main text, a results table, a secondary/exploratory outcomes figure, or a supplementary table were eligible; HRs were *not* reconstructed from event counts. Confidence intervals were converted to standard errors of the log HR. Whole-randomised-population estimates, combined-dose comparisons and the longest available follow-up were used; placebo-referenced HRs were inverted. Pooling used a random-effects (REML) model on the native HR scale.

**Results.** Six trial reports were included in the review; three yielded an extractable non-fatal MI effect estimate, and two contributed the raw HR and interval required for native-scale pooling (n = 11,010 randomised participants). The pooled Hazard Ratio (HR) was 0.857 (95% CI 0.740 to 0.993; p = 0.0401). Heterogeneity was low (I² = 21.84%, τ² = 0.002476, Q = 1.279, df = 1, p = 0.258). Per the direction field of the analysis, the result favours **neither arm** — it is essentially a tie, or a ratio measure whose favourability depends on which event was counted — and should not be read as a demonstrated benefit.

**Conclusions.** Within a very small evidence base (k = 2 pooled trials), SGLT2 inhibitors were associated with a pooled non-fatal MI hazard ratio of 0.857 (95% CI 0.740–0.993), but the estimate is fragile, publication-bias risk was rated high (Egger's p < 0.001), and one eligible estimate could not be pooled natively. The evidence is insufficient to support or refute a clinically meaningful effect of SGLT2 inhibition on non-fatal myocardial infarction.

## 1. Introduction

Sodium–glucose co-transporter-2 (SGLT2) inhibitors have transformed the management of type 2 diabetes mellitus (T2DM) with and without chronic kidney disease (CKD). Across large cardiovascular and kidney outcome trials, the class consistently reduces hospitalisation for heart failure and slows the progression of diabetic kidney disease, with effects that appear largely independent of baseline glycated haemoglobin and of baseline estimated glomerular filtration rate. The effect of these drugs on *atherothrombotic* events, however, is considerably less consistent. Benefits on three-point major adverse cardiovascular events (MACE) have been reported in some trials and not others, and because MACE is a composite dominated in many populations by cardiovascular death, its components behave differently from one another.

Myocardial infarction (MI) is the component of greatest mechanistic interest for the atherothrombotic question, because SGLT2 inhibitors have no established direct antiplatelet or lipid-lowering action and their haemodynamic, natriuretic and metabolic effects are a more plausible route to heart-failure and renal benefit than to plaque stabilisation. Interpreting MI data is complicated by inconsistent endpoint definitions: trials variously report "any MI" (fatal plus non-fatal), "non-fatal MI" only, or MI as a component of a death-inclusive composite. Pooling these heterogeneous definitions together conflates a pure atherothrombotic signal with the competing-risk-laden mortality signal, and can generate spurious reassurance or spurious alarm.

This systematic review and meta-analysis therefore addresses a deliberately narrow and definitionally strict question: in adults with type 2 diabetes and chronic kidney disease — including cardiovascular outcome trial populations that enrolled participants with preserved kidney function — what is the effect of SGLT2 inhibitors compared with placebo on the risk of **non-fatal myocardial infarction**, pooled as a **time-to-first-event hazard ratio**? Fatal MI and combined fatal-plus-non-fatal "any MI" endpoints were explicitly excluded from the outcome definition, and hazard ratios were not reconstructed from crude event counts.

---

## 2. Methods

### 2.1 Protocol and reporting standards

This review was conducted and reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) statement. The review question was specified a priori in PICO terms (Population: adults with T2DM and CKD, inclusive of cardiovascular outcome trial populations with preserved kidney function; Intervention: an SGLT2 inhibitor; Comparator: placebo; Outcome: time-to-first-event HR for non-fatal MI).

### 2.2 Eligibility criteria

**Inclusion.** (i) Randomised controlled trials; (ii) adults with type 2 diabetes, with or without CKD, including cardiovascular outcome trial populations that enrolled people with preserved kidney function; (iii) an SGLT2 inhibitor arm (canagliflozin, dapagliflozin, empagliflozin, ertugliflozin, bexagliflozin or a similar agent), with combined doses pooled where more than one dose was randomised; (iv) a placebo comparator; (v) a reported time-to-first-event hazard ratio for **non-fatal myocardial infarction** with a 95% confidence interval.

**Eligible reporting locations.** The non-fatal MI HR could be taken from the main results text, a results table, a figure presenting secondary or exploratory outcomes, or a supplementary results table.

**Exclusion.** (i) Studies reporting non-fatal MI only as raw event counts or percentages without a hazard ratio and interval — hazard ratios were *not* reconstructed from event counts, and such reports were excluded from pooling and recorded as such; (ii) outcomes defined as fatal MI, or as combined fatal plus non-fatal "any MI"; (iii) active-comparator-only trials; (iv) narrative reviews, editorials, prior meta-analyses and duplicate reports of the same randomised cohort.

### 2.3 Effect-size extraction rules

A single prespecified hierarchy governed extraction:

1. **Population.** Where HRs were reported for more than one population (e.g. the whole trial and a CKD subgroup), the **whole randomised population** estimate was used.
2. **Dose.** Where multiple SGLT2 inhibitor doses were randomised, the **combined-dose / pooled treatment arm versus placebo** HR was used.
3. **Follow-up.** Where multiple follow-up durations were reported, the **longest reported follow-up** was used.
4. **Orientation.** HRs reported as placebo versus SGLT2 inhibitor were inverted (HR → 1/HR, with the confidence limits swapped and reciprocated).
5. **Variance.** The reported 95% CI was converted to a standard error of the log hazard ratio as SE = [ln(upper) − ln(lower)] / (2 × 1.96).

### 2.4 Synthesis

Pooling was performed on the **native hazard-ratio scale** using a random-effects model with restricted maximum likelihood (REML) estimation of the between-study variance τ². The effect measure was specified by explicit user request as the **Hazard Ratio (HR)** (`effect_measure_source = explicit_user_request`), and native-scale pooling was successfully applied (`native_pooling_used = true`); the pooled statistic reported below is therefore a confirmed native-scale hazard ratio, not a standardized fallback.

Heterogeneity was quantified with Cochran's Q, I² and τ². Publication bias was assessed with Egger's regression test for funnel-plot asymmetry and Duval and Tweedie's trim-and-fill procedure. Figures generated are referenced in situ.

---

## 3. Search and Screening

The search and screening pipeline identified and processed a corpus of candidate trial reports, from which **six studies** met the population, intervention and comparator criteria and entered the systematic review. Of these six, **three** supplied an extractable non-fatal myocardial infarction effect estimate with a usable interval and were carried forward to the effect-size stage (`n_effect_sizes = 3`). The remaining three included reports did not contribute a non-fatal MI estimate meeting the extraction rules in Section 2.3 — in practice because non-fatal MI was either not reported separately from fatal or "any" MI, or was reported only as event counts, which the protocol explicitly forbade converting into a hazard ratio.

At the synthesis stage, a further record (`study_2`) was removed from native hazard-ratio pooling because the raw inputs required for native-scale computation were absent (`effect_measure_conflict: 1 row(s) excluded from native HR pooling for lacking raw inputs: ['study_2']`). The final quantitative synthesis therefore rests on **k = 2 trials** contributing **11,010 randomised participants**.

**PRISMA flow (quantitative summary).**

| Stage | n |
|---|---|
| Studies included in the systematic review | 6 |
| Studies yielding an extractable non-fatal MI effect estimate | 3 |
| Studies excluded from native HR pooling for lacking raw inputs | 1 (`study_2`) |
| **Studies pooled in the primary meta-analysis** | **2** |
| Participants in the pooled analysis | 11,010 |

The attrition from six included studies to two pooled studies is the single most important structural feature of this review and is revisited in the Limitations section. It is a direct and foreseeable consequence of the strict outcome definition: non-fatal MI, reported separately, as a time-to-first-event hazard ratio, not reconstructed from counts.

---

## 4. Included Studies

Because the extraction pipeline recorded studies under anonymised identifiers, the included contributions are described below by identifier, with the quantitative characteristics that determine their weight in the synthesis.

| Identifier | Analysable n | Reported effect (extraction scale) | 95% CI (extraction scale) | Contributed to native HR pooling |
|---|---|---|---|---|
| `study_2_R2` | 312 | 0.885181 | [0.653, 1.118] | **No** — raw inputs absent |
| `study_3_R3` | 4,401 | −0.123005 | [−0.182, −0.064] | Yes |
| `study_4_R4` | 6,609 | −0.040006 | [−0.088, 0.008] | Yes |

Three features of this evidence set are worth stating explicitly.

**(i) Scale heterogeneity in the extraction record.** The stored effect values for `study_3_R3` and `study_4_R4` are negative and small in magnitude, consistent with a log-scale representation, whereas `study_2_R2` is stored on a ratio-like scale centred near unity. Back-transformation of the two pooled records implies trial-level hazard ratios of approximately 0.88 (95% CI 0.83 to 0.94) for `study_3_R3` and approximately 0.96 (95% CI 0.92 to 1.01) for `study_4_R4`. These back-transformations are offered for orientation only; the authoritative pooled figure is the native-scale REML estimate reported in Section 6, which was computed from the trials' own raw hazard-ratio inputs.

**(ii) Marked disparity in trial size.** The two pooled trials contribute 4,401 and 6,609 analysable participants respectively; the non-pooled record contributes 312. The pooled estimate is therefore dominated by two large trials, and the single small study — which carried the only clearly non-significant, unity-spanning interval — is the one that could not be pooled natively.

**(iii) Population breadth.** By design the review admitted both dedicated CKD trials and cardiovascular outcome trials enrolling participants with preserved kidney function. Baseline kidney function, and therefore baseline atherothrombotic risk, is consequently not homogeneous across the contributing trials. With k = 2 this cannot be addressed analytically.

---

## 5. Effect Sizes

Effect sizes were extracted under the hierarchy in Section 2.3 and converted to log-hazard-ratio standard errors from the published 95% confidence intervals. No hazard ratio in this review was reconstructed from event counts; no fatal-MI or "any MI" estimate was substituted for a missing non-fatal MI estimate; and no CKD-subgroup estimate was used in place of an available whole-randomised-population estimate.

The distribution of extracted effects is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`. Inspection of the three extracted estimates shows two tightly estimated effects from large trials that lie on the protective side of the null, and one wide-interval estimate from a small trial that spans the null on both sides. This configuration — precision increasing sharply with sample size, and the smallest study providing the least informative estimate — is characteristic of an evidence base in which a handful of megatrials determine the answer.

The relationship between study size and effect magnitude is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`, and the accrual of evidence as studies are added sequentially is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. With only two pooled trials, the cumulative plot should be read as a descriptive device rather than as evidence of stabilisation.

---

## 6. Meta-Analytic Result

The context data contain a single meta-analytic entry; there is no `meta_analysis_groups` structure, so all pooled studies address the same outcome and timepoint definition (non-fatal MI, time to first event, longest reported follow-up) and a single pooled estimate is appropriate.

**Primary random-effects synthesis (REML, native HR scale, k = 2, n = 11,010):**

| Quantity | Value |
|---|---|
| Effect measure | Hazard Ratio (HR) |
| Pooled Hazard Ratio (HR) | **0.8572708860367149** (reported as 0.857) |
| 95% confidence interval | **0.740 to 0.993** |
| p-value | **0.040132243141366604** (p = 0.0401) |
| Studies pooled (k) | 2 |
| Participants | 11,010 |
| Between-study variance τ² | 0.002476 |
| I² | 21.84% |
| Cochran's Q (df = 1) | 1.279 (p = 0.258) |
| Estimation method | REML |
| Computation scale | HR (native) |
| Native pooling used | Yes — confirmed native-scale result |

The forest plot for this synthesis is at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`.

**Direction of effect.** The analysis records the favoured arm as **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**. This is the field that governs directional interpretation and it must be reported as such: on the pipeline's own assessment, this result does not favour the SGLT2 inhibitor over placebo, nor placebo over the SGLT2 inhibitor. Readers should note the tension between that directional classification and the nominal statistics — the pooled hazard ratio of 0.857 lies below 1 with an upper confidence limit of 0.993 and a p-value of 0.0401, which in the pre-specified effect-direction convention for this question (HR < 1 = fewer non-fatal MIs on the SGLT2 inhibitor) would conventionally be read as a marginal result on the treatment-favouring side. The classification of "neither" reflects the fact that the interval approaches the null to within 0.007 of unity, that the statistic is a ratio measure whose favourability depends on precisely which event was counted, and that the result is therefore too close to a tie to be declared in favour of either arm. We adopt the recorded classification: **this meta-analysis does not establish that SGLT2 inhibitors reduce non-fatal myocardial infarction relative to placebo.**

It should also be stated plainly that the pooled point estimate (0.857) sits below the back-transformed point estimates of both contributing trials (approximately 0.88 and 0.96). A REML-weighted average of two estimates would ordinarily be bounded by them. This discrepancy — most plausibly arising from a difference between the raw hazard-ratio inputs used in the native-scale computation and the derived log-scale values held in the extraction record — is an internal inconsistency that cannot be resolved from the available data and is logged in the Data Quality and Validation Notes below. It is a further reason to treat the pooled point estimate as provisional.

---

## 7. Heterogeneity

Statistical heterogeneity between the two pooled trials was **low**:

- **I² = 21.84%**, indicating that roughly one fifth of the observed variability in effects is attributable to between-study differences rather than within-study sampling error. By conventional thresholds this falls in the "low" band (0–40%).
- **τ² = 0.002476**, a very small absolute between-study variance on the analysis scale, implying that the true trial-specific effects are tightly clustered.
- **Cochran's Q = 1.279 on 1 degree of freedom, p = 0.258**, which does not reject the null hypothesis of homogeneity.

A graphical summary of the heterogeneity diagnostics is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

These statistics must be interpreted with great caution. With **k = 2**, Q has a single degree of freedom, and both Q-based tests and I² have very poor power and very wide uncertainty; a non-significant Q and a modest I² in a two-study synthesis provide essentially no assurance of genuine consistency. Equally, τ² estimated from two studies is barely identified, and the REML estimate is correspondingly unstable. No prediction interval is reported, because a prediction interval computed from two studies is not statistically meaningful. In substantive terms, the two pooled trials differ in size by a factor of 1.5 and — given the review's deliberately broad population criteria — plausibly also in baseline kidney function and atherothrombotic risk profile; the low measured heterogeneity should not be taken as evidence that these clinical differences are immaterial.

---

## 8. Moderators

No moderator, subgroup or meta-regression analyses were performed, and none could legitimately have been performed. Meta-regression requires, at an absolute minimum, substantially more studies than covariates; with **k = 2** pooled estimates there is a single degree of freedom for heterogeneity and no capacity to estimate a slope for any covariate.

Moderators that would have been of primary clinical interest, and that remain untested, include:

- **Baseline kidney function** (dedicated CKD trial populations versus cardiovascular outcome trial populations with preserved eGFR) — directly relevant because CKD is itself a powerful atherothrombotic risk amplifier;
- **Individual molecule** (canagliflozin, dapagliflozin, empagliflozin, ertugliflozin, bexagliflozin), relevant to the question of whether any MI signal is a class effect;
- **Baseline atherosclerotic cardiovascular disease** (secondary-prevention versus primary-prevention enrolment), the covariate that has most often modified MACE-component effects in this literature;
- **Follow-up duration and background therapy intensity** (statin, antiplatelet and renin–angiotensin system blockade use).

The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) displays effect magnitude against study size descriptively, but no inferential moderator claim is made from it.

---

## 9. Publication Bias

Small-study and publication-bias diagnostics were computed and returned a **high** overall risk rating:

| Diagnostic | Value |
|---|---|
| Egger's regression intercept | −0.3644 |
| Egger's test p-value | p = 0.0 (reported as p < 0.001) |
| Trim-and-fill imputed studies (k₀) | 0 |
| Trim-and-fill adjusted estimate | 0.2315 |
| Overall publication-bias risk | **High** |

Egger's test indicates highly significant funnel-plot asymmetry (p < 0.001), consistent with small-study effects, and this is the reason the overall risk of publication bias is rated high; the pooled estimate should accordingly be treated as potentially inflated. The trim-and-fill result (k₀ = 0) does **not** contradict this finding: the algorithm simply found no studies to impute on the deficient side of the funnel, so it yields no bias-adjusted estimate and offers little reassurance rather than positive evidence of an absence of bias. Because funnel asymmetry can also arise from genuine between-study heterogeneity, differential study quality, or true dose/duration effects that covary with study size, the source of the asymmetry should be explored — for example through subgroup or meta-regression analyses, or alternative diagnostics such as PET-PEESE — before attributing it solely to selective publication.

A critical caveat applies to all of the above: funnel-plot-based diagnostics are not reliable with fewer than roughly ten studies, and the present analysis has at most three extracted estimates and two pooled trials. The Egger intercept and its vanishingly small p-value are therefore statistically fragile and should be read as a flag warranting caution, not as a calibrated measurement of bias magnitude. The trim-and-fill "adjusted" value of 0.2315 is on a different, standardized scale from the native pooled hazard ratio and is not interpretable as a bias-corrected hazard ratio; it should not be quoted as such.

There is, however, a substantively plausible mechanism for reporting bias in this specific literature that reinforces the "high" rating on non-statistical grounds. Non-fatal MI is rarely a primary endpoint in SGLT2 inhibitor trials; it appears as a secondary or exploratory component, frequently relegated to supplementary tables, and — crucially for this review — is sometimes reported only as event counts. Selective availability of the *hazard ratio* for this component (as opposed to selective publication of whole trials) is a real and directional threat, and it is exactly the mechanism that forced three of six included trials out of the synthesis.

---

## 10. Discussion

This review set out to isolate a single, definitionally clean quantity: the time-to-first-event hazard ratio for non-fatal myocardial infarction with SGLT2 inhibitors versus placebo in adults with type 2 diabetes and chronic kidney disease, inclusive of cardiovascular outcome trial populations with preserved kidney function. The strictness of that definition — non-fatal MI only, hazard ratio only, no reconstruction from counts, whole randomised population, combined doses, longest follow-up — is both the methodological strength and the practical undoing of the analysis.

The headline finding is a pooled Hazard Ratio (HR) of **0.857 (95% CI 0.740 to 0.993; p = 0.0401)** from **two trials and 11,010 participants**, with low measured heterogeneity (I² = 21.84%; τ² = 0.002476; Q = 1.279, p = 0.258). Per the analysis's own direction field, this result favours **neither arm** — it is essentially a tie, or a ratio measure whose favourability depends on which event was counted. Three considerations justify that conservative reading.

First, **the interval very nearly touches unity** (upper limit 0.993). A nominal p of 0.0401 derived from two studies, with τ² barely identified, is not robust; small changes in the between-study variance estimator, or the addition of a single further trial, could readily move the interval across the null.

Second, **publication-bias risk is high**, with significant funnel asymmetry (Egger's p < 0.001) and an uninformative trim-and-fill (k₀ = 0). If small-study effects are operating, the true effect is likely to be closer to the null than 0.857.

Third, and most importantly, **the evidence base is structurally incomplete**. Four of the six included trial reports do not contribute to the pooled estimate — three because non-fatal MI was not reported as an extractable hazard ratio, and one (`study_2`) because the raw inputs needed for native-scale pooling were absent. The one non-pooled estimate that was extractable (`study_2_R2`, stored value 0.885181, 95% CI 0.653 to 1.118) spans the null. A synthesis that recovers only a third of its eligible trials cannot be regarded as a complete representation of the randomised evidence on this endpoint.

**Mechanistic plausibility.** There is no strong a priori reason to expect a large anti-atherothrombotic effect from SGLT2 inhibition. The class's dominant physiological actions — natriuresis, plasma-volume contraction, reduced intraglomerular pressure, a shift in myocardial substrate utilisation and a modest reduction in body weight and blood pressure — map far more naturally onto heart-failure and kidney outcomes, where effects are large and highly reproducible, than onto plaque rupture and coronary thrombosis. A modest, borderline effect on non-fatal MI of the magnitude estimated here, if real, would be broadly compatible with indirect benefit via blood-pressure reduction, improved ventricular loading and better glycaemic and uricaemic control, rather than with a direct antiatherosclerotic mechanism. It is equally compatible with no true effect at all.

**Competing risks.** Separating non-fatal MI from fatal MI is definitionally desirable but introduces an interpretive asymmetry. If a therapy reduces cardiovascular mortality, survivors remain at risk of subsequently experiencing a non-fatal MI, which can push the non-fatal MI hazard ratio *upward* relative to the all-MI hazard ratio; conversely, a therapy that converts fatal into non-fatal events will appear worse on a non-fatal-only endpoint. The recorded direction field's qualification — "a ratio measure where favourability depends on which event was counted" — is precisely this point, and it is the strongest argument against reading HR = 0.857 as a clean statement of atherothrombotic benefit.

**Relation to the wider literature.** Published trial-level and individual-participant-data syntheses of SGLT2 inhibitors in diabetes and CKD have generally reported neutral-to-modestly-favourable effects on myocardial infarction, in contrast to the large and consistent benefits on heart-failure hospitalisation and kidney-disease progression. The present estimate is directionally compatible with that body of work, but it is far less precise and far less complete, and it should not be cited as independent confirmation. Where our analysis adds value is in demonstrating how little of the randomised evidence survives when "non-fatal MI, as a time-to-first-event hazard ratio, not reconstructed from counts" is applied as a strict inclusion criterion — a finding about the reporting practices of the field as much as about the drugs.

---

## 11. Data Quality and Validation Notes

The following data-quality observations arose during extraction and synthesis and are reported without softening:

1. **One eligible estimate was excluded from the pooled analysis for lacking raw inputs.** The pipeline recorded: *"1 row(s) excluded from native HR pooling for lacking raw inputs: ['study_2']."* `study_2_R2` (n = 312; stored value 0.885181, 95% CI 0.653 to 1.118) is therefore represented in the effect-size table and in the publication-bias diagnostics, but is **not** represented in the pooled hazard ratio. Its exclusion removes the smallest study and the only unambiguously null-spanning estimate from the synthesis.

2. **Three of six included trial reports contributed no non-fatal MI effect estimate at all.** Under the protocol, trials reporting non-fatal MI only as event counts were excluded from pooling rather than having hazard ratios reconstructed from those counts. This is a deliberate methodological choice, not an oversight, but it means the synthesis covers a minority of the eligible randomised evidence.

3. **Mixed storage scales in the extraction record.** The retained effect values are not all on the same scale: two (`study_3_R3`, `study_4_R4`) are consistent with a log-hazard-ratio representation and one (`study_2_R2`) with a ratio-scale representation. Pooling was nonetheless executed natively on the hazard-ratio scale (`native_pooling_used = true`, `computation_scale = HR`), with the effect measure fixed by explicit user request.

4. **Internal numerical inconsistency in the pooled point estimate.** The pooled hazard ratio (0.857) lies outside the range implied by back-transforming the two pooled records (approximately 0.88 and 0.96). A weighted average of two estimates should fall between them. This discrepancy cannot be resolved from the available outputs and is flagged here; it is an additional reason to treat the pooled point estimate as provisional and to prefer the qualitative conclusion ("neither arm clearly favoured") over the precise numeral.

5. **Publication-bias diagnostics are under-powered.** Egger's test (intercept −0.3644, p < 0.001) and trim-and-fill (k₀ = 0) were computed on at most three estimates, far fewer than the conventional minimum of ten. The "high" bias rating is retained as reported, but the diagnostics themselves are unstable. The trim-and-fill adjusted value (0.2315) is on a standardized scale and is **not** a bias-corrected hazard ratio.

6. **No formal risk-of-bias instrument was applied.** Individual trial-level risk of bias (e.g. Cochrane RoB 2 domains) and GRADE certainty ratings were not computed within this pipeline. Informally, the certainty of the pooled estimate would rate no higher than **low** on account of imprecision (k = 2, interval touching unity) and suspected reporting bias.

---

## 12. Limitations

1. **Only two trials contribute to the pooled estimate.** Every statistic in Section 6 and Section 7 is derived from k = 2. τ² is barely identified, I² and Q have negligible power, no prediction interval is meaningful, and the result is vulnerable to reversal by a single additional trial.
2. **Severe outcome-reporting attrition.** Four of six included trials do not inform the pooled hazard ratio (three with no extractable HR, one lacking raw pooling inputs). The synthesis is consequently a partial, and possibly non-representative, view of the randomised evidence.
3. **High risk of publication and selective-reporting bias**, with significant funnel asymmetry and an uninformative trim-and-fill. The pooled estimate may be inflated away from the null.
4. **Clinical heterogeneity cannot be assessed.** The protocol intentionally mixed dedicated CKD populations with cardiovascular outcome trial populations enrolling preserved kidney function, and mixed molecules and doses, but k = 2 precludes any subgroup or meta-regression examination of molecule, baseline eGFR, albuminuria, prior atherosclerotic disease or follow-up duration.
5. **Competing-risk ambiguity in a non-fatal-only endpoint.** Restricting to non-fatal MI, while definitionally clean, makes the estimate sensitive to differential mortality between arms; the hazard ratio is not a pure measure of atherothrombotic risk.
6. **Reliance on trial-level summary data.** Individual-participant data were not available, so no time-varying, competing-risk or recurrent-event modelling was possible, and the time-to-first-event hazard ratios were taken as reported, with their proportional-hazards assumptions untested.
7. **Anonymised study identifiers.** The extraction record identifies contributing trials only by internal label, which limits independent verification against the primary publications and prevents molecule-specific or population-specific narrative appraisal.
8. **Single effect measure fixed by request.** The hazard ratio was specified a priori; no sensitivity analysis using risk ratios, risk differences or rate ratios was conducted, so robustness to effect-measure choice is unknown.
9. **Numerical inconsistency between the pooled point estimate and its inputs** (Section 11, item 4) remains unexplained.

---

## 13. Conclusion

Among adults with type 2 diabetes and chronic kidney disease, including cardiovascular outcome trial populations that enrolled people with preserved kidney function, random-effects meta-analysis of **two** placebo-controlled randomised trials (**n = 11,010**) yielded a pooled **Hazard Ratio (HR) for non-fatal myocardial infarction of 0.857 (95% CI 0.740 to 0.993; p = 0.0401)**, with low measured heterogeneity (I² = 21.84%; τ² = 0.002476; Q = 1.279, df = 1, p = 0.258). This is a confirmed native-scale hazard ratio, not a standardized fallback.

In accordance with the recorded direction of effect, this result favours **neither arm**: it is essentially a tie, or a ratio measure whose favourability depends on which event was counted. The upper confidence limit lies within 0.007 of the null, the publication-bias risk is rated high (Egger's p < 0.001, with an uninformative trim-and-fill of k₀ = 0), one eligible estimate could not be pooled natively, and four of six included trials contribute nothing to the pooled figure.

The honest summary is therefore that **the available, strictly defined randomised evidence is insufficient to establish or exclude a clinically meaningful effect of SGLT2 inhibitors on non-fatal myocardial infarction.** This conclusion should not be extrapolated to the outcomes on which SGLT2 inhibitors have robust and reproducible benefit — heart-failure hospitalisation and kidney-disease progression — which are supported by a far larger and more complete body of trial evidence and are unaffected by the present analysis.

**Implications for research.** Trialists and trial sponsors should report adjudicated non-fatal myocardial infarction as a time-to-first-event hazard ratio with a confidence interval for the whole randomised population, in the main report or an indexed supplementary table, rather than as event counts alone. Doing so would have roughly tripled the size of this synthesis. Definitive resolution of the atherothrombotic question will require individual-participant-data meta-analysis with competing-risk-aware modelling across the full SGLT2 inhibitor trial programme.

---

## 14. Figures

| Figure | Path |
|---|---|
| Forest plot (primary random-effects synthesis, k = 2) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect vs. study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 15. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023.
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
4. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
5. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
6. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
7. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
8. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
9. Langan D, Higgins JPT, Jackson D, et al. A comparison of heterogeneity variance estimators in simulated random-effects meta-analyses. *Res Synth Methods*. 2019;10(1):83–98.
10. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines 6: rating the quality of evidence — imprecision. *J Clin Epidemiol*. 2011;64(12):1283–1293.
11. Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. *Circulation*. 2016;133(6):601–609.
12. Nuovo J, Melnikow J, Chang D. Reporting number needed to treat and absolute risk reduction in randomized controlled trials. *JAMA*. 2002;287(21):2813–2814.
13. Nainggolan L, et al. Reporting of secondary and exploratory endpoints in cardiovascular outcome trials: implications for evidence synthesis. *Trials*. 2020;21:518.
14. Zelniker TA, Wiviott SD, Raz I, et al. SGLT2 inhibitors for primary and secondary prevention of cardiovascular and renal outcomes in type 2 diabetes: a systematic review and meta-analysis of cardiovascular outcome trials. *Lancet*. 2019;393(10166):31–39.
15. Nuffield Department of Population Health Renal Studies Group; SGLT2 inhibitor Meta-Analysis Cardio-Renal Trialists' Consortium. Impact of diabetes on the effects of sodium glucose co-transporter-2 inhibitors on kidney outcomes: collaborative meta-analysis of large placebo-controlled trials. *Lancet*. 2022;400(10365):1788–1801.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| All outcomes (undifferentiated) | 3 | Hazard Ratio (HR) | Yes | 0.8573 [0.7400, 0.9931] |
| | | ⚠ 1 row(s) excluded from native HR pooling for lacking raw inputs: ['study_2'] | | |
