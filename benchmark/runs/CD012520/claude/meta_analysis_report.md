# Multifaceted implementation interventions and adherence to evidence-based processes of care in patients hospitalised with acute stroke: a systematic review and random-effects meta-analysis

## Abstract

**Background.** Evidence-based processes of care for acute stroke — thrombolysis for eligible patients, dysphagia screening, venous thromboembolism prophylaxis, fever/hyperglycaemia/swallowing protocols, and structured care pathways — are reliably associated with better patient outcomes, yet adherence in routine hospital practice remains incomplete. Multifaceted implementation interventions (combinations of clinician education, audit and feedback, local champions, written protocols or clinical pathways, with or without redesign of care delivery) are widely used to close this gap, but their effect on process-of-care adherence has not been quantified consistently.

**Objective.** To estimate whether, in people hospitalised with acute stroke, multifaceted implementation interventions increase the proportion of patients (or eligible patients) who receive the recommended process of care during the hospital admission, compared with no implementation intervention or usual practice.

**Methods.** A systematic search and structured screening pipeline identified controlled trials (including cluster-randomised trials) comparing a multifaceted implementation intervention against usual practice in acute stroke inpatients, reporting a patient-level adherence or quality-of-care process outcome at the end of the intervention/follow-up period. Events and totals were extracted per arm at the patient level; for cluster trials, cluster-adjusted risk ratios with confidence intervals were used where reported, otherwise standard errors were inflated by the design effect 1 + (average cluster size − 1) × ICC using the trial's own ICC or an assumed ICC of 0.05. Effects were pooled on the risk-ratio scale using a random-effects model estimated by restricted maximum likelihood (REML). Heterogeneity was quantified with Q, I² and τ². Small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** Four studies contributing four effect sizes and 8,899 patients were included. All four individual estimates favoured the implementation intervention and all four had confidence intervals excluding the null, with study-level risk ratios ranging from approximately 1.07 to 3.88. The pooled Risk Ratio (RR) from the random-effects model was 1.734 (95% CI 0.734 to 4.094; p = 0.2094; k = 4; N = 8,899). On the direction field carried with the analysis, this pooled result favours **neither arm** — it is effectively a statistical tie, because the confidence interval spans the null despite every contributing study being individually positive. Heterogeneity was extreme (Q = 75.239, df = 3, p < 0.001; I² = 99.04%; τ² = 0.754487 on the log-RR scale). Egger's test indicated significant funnel asymmetry (intercept = −0.8315, p = 0.0228; overall small-study-effect risk rated "high"), although trim-and-fill imputed only one hypothetical missing study (k₀ = 1) and the bias-adjusted pooled estimate (0.6161 on the log-RR pooling scale, ≈ RR 1.85) was not smaller than the primary estimate. With k = 4, formal moderator analysis and meta-regression were not interpretable and were not performed.

**Conclusions.** Every included trial individually reported higher adherence to the recommended process of care in the multifaceted implementation arm, but the magnitude of benefit differed so profoundly across trials (I² = 99.04%) that the random-effects pooled risk ratio is statistically indistinguishable from no effect and favours neither arm. The honest reading is not "implementation interventions do not work" but "the pooled average is uninformative": the evidence base is too small (k = 4), too heterogeneous, and too asymmetric for a single summary risk ratio to be a trustworthy guide. Certainty in the pooled estimate should be rated very low. Decision-makers should rely on the individual trial estimates, matched to the specific process of care, intervention intensity and setting, rather than on the pooled value.

# Introduction

Stroke care is one of the clearest examples in acute medicine of a well-characterised gap between what is known to work and what is actually delivered. Intravenous thrombolysis for eligible patients, timely dysphagia screening before oral intake, venous thromboembolism prophylaxis, protocolised management of fever, hyperglycaemia and swallowing (the "FeSS" domain), early mobilisation, and admission to organised stroke unit care are all supported by trial or guideline-level evidence, and several are directly linked to death and disability outcomes. Yet national and international audit programmes consistently show that a substantial fraction of eligible stroke inpatients do not receive these processes of care, and that between-hospital variation is large.

The response to this gap has typically been *multifaceted implementation interventions*: bundles that combine some mixture of clinician and team education, audit and feedback of local performance data, identification and support of local clinical champions or opinion leaders, introduction of written protocols, standing orders or clinical pathways, and — in some programmes — redesign of how care is delivered (for example, nurse-initiated protocols, reorganisation of the admission pathway, or dedicated acute stroke teams). The theoretical case is strong: single-component strategies such as passive guideline dissemination are known to be weak, and multifaceted bundles address several barriers at once. The empirical case is less settled. Trials of implementation bundles in stroke differ in which process they target, how intensively the bundle is delivered, whether care-delivery redesign is included, the baseline level of adherence in the control arm, and whether randomisation is at the cluster (hospital) or individual level — all of which can plausibly shift the achievable effect size by an order of magnitude.

This review addresses a single, specific question: **in people hospitalised with acute stroke, do multifaceted implementation interventions, compared with no implementation intervention or usual practice, increase the proportion of patients (or eligible patients) who receive the recommended, evidence-based process of care during the hospital admission?** The outcome of interest is each trial's own primary adherence or quality-of-care process measure, extracted at the patient level as the number adherent out of the number of patients in each arm at the end of the intervention period. A risk ratio above 1 indicates that patients in the implementation arm were *more* likely to receive the recommended process of care.

# Methods

## Protocol and reporting

The review was conducted and is reported in accordance with the PRISMA 2020 statement. The analysis plan — population (adults hospitalised with acute stroke), intervention (multifaceted implementation intervention), comparator (no implementation intervention / usual practice), outcome (patient-level proportion receiving the recommended process of care at end of intervention), and effect measure (risk ratio) — was specified before pooling. The requested effect measure was the risk ratio; this was recorded in the analysis metadata as an explicit user request, no conflicting measure was detected, and native risk-ratio pooling was used (`native_pooling_used = true`), so the pooled statistic reported below is a genuine native-scale risk ratio rather than a standardized fallback.

## Eligibility criteria

**Included:** controlled trials (individually randomised, cluster-randomised, or controlled before–after designs with a concurrent control) in which (i) the population was patients hospitalised with acute stroke (ischaemic, haemorrhagic, or mixed, including transient ischaemic attack cohorts managed as inpatients); (ii) the intervention was a multifaceted implementation strategy combining two or more of education, audit and feedback, local champions/opinion leaders, protocols or clinical pathways, with or without care-delivery redesign; (iii) the comparator was no implementation intervention, usual care, or "practice as normal"; and (iv) the trial reported a patient-level adherence or quality-of-care process outcome as a count of adherent patients out of patients (or eligible patients) per arm during the post-intervention/follow-up window.

**Excluded:** studies reporting only hospital- or cluster-level numerators and denominators with no patient-level data; single-component implementation strategies (e.g. guideline mailing alone); interventions whose primary target was post-discharge or community care; studies reporting only clinical endpoints (death, modified Rankin Scale) with no process measure; narrative reviews, editorials, protocols without results, and duplicate reports of the same trial and outcome.

## Information sources and search

Bibliographic databases covering the biomedical, nursing and implementation-science literature were searched using controlled vocabulary and free-text terms for the three concept blocks — stroke/cerebrovascular disease AND implementation terms (implementation, quality improvement, audit and feedback, clinical pathway, care bundle, guideline adherence, opinion leader, champion, knowledge translation) AND trial design terms (randomised, cluster, controlled trial, before-after). Reference lists of included reports and of relevant systematic reviews were screened, and forward citation tracking was performed on included trials.

## Study selection and data extraction

Records were de-duplicated and screened in two stages (title/abstract, then full text) against the criteria above. For each included trial, the following were extracted: trial identifier, design (individual vs cluster randomisation), setting, components of the implementation bundle, the specific process of care constituting the primary adherence outcome, the timing of outcome ascertainment, and — for each arm — the number of patients adherent (events) and the number of patients (total). Where a trial reported several process measures, the trial's own designated primary adherence/quality-of-care process measure was used, so that each trial contributed exactly one effect size and no double-counting of patients occurred within the pooled analysis.

## Handling of cluster-randomised trials

Because implementation interventions are usually delivered at hospital level, clustering was handled explicitly. Where a trial reported a cluster-adjusted risk ratio (or odds ratio) with a confidence interval, that adjusted estimate was used and the confidence interval converted to a standard error of the log risk ratio; odds ratios were converted to risk ratios only where the control-arm baseline risk was reported. Where no cluster-adjusted estimate was available, the naïve standard error was inflated by the design effect 1 + (average cluster size − 1) × ICC, using the trial's own reported intracluster correlation coefficient where available and an assumed ICC of 0.05 otherwise. Denominators remained patient-level throughout; hospitals and clusters were never used as the unit of analysis.

## Statistical analysis

Effects were pooled on the risk-ratio scale (analysis performed on the log scale and exponentiated for reporting) using a random-effects model with the between-study variance estimated by restricted maximum likelihood (REML). Heterogeneity was quantified by Cochran's Q with its p-value, the I² statistic, and τ² (on the log-RR scale). Small-study effects were examined with Egger's regression of the standardized effect on precision and with Duval and Tweedie's trim-and-fill procedure. A cumulative meta-analysis ordered by precision, the distribution of effect sizes, a bubble plot of effect size against study size/precision, and a heterogeneity summary were generated as sensitivity and diagnostic displays. All analyses were two-sided with α = 0.05.

# Search and Screening

The search-and-screening pipeline proceeded through de-duplication, title/abstract screening and full-text assessment against the eligibility criteria set out above. After full-text assessment, **four studies met all inclusion criteria** and contributed **four effect sizes** (one per study) to the quantitative synthesis, with a combined patient-level sample of **8,899 patients**. Records excluded at full text were removed for the standard reasons captured by the criteria: absence of a patient-level process-of-care numerator and denominator, single-component rather than multifaceted implementation strategies, non-inpatient or post-discharge targets, and reports that were reviews, protocols or duplicate publications of an already-included trial. Because each trial contributed exactly one primary adherence outcome, there is no within-study double-counting of patients in the pooled estimate. A PRISMA-style flow of records through identification, screening, eligibility and inclusion follows this structure, terminating in the four studies analysed below.

It should be stated plainly at the outset that four studies is a very small evidence base for a meta-analysis. It is sufficient to compute a pooled estimate, but it is at the lower bound of what permits reliable estimation of between-study variance and it is below the conventional threshold (k ≥ 10) for trustworthy assessment of funnel-plot asymmetry. Both of those limitations bear directly on the interpretation of the results that follow.

# Included Studies

The four included studies are reported here under the pipeline identifiers `study_1` through `study_4`, each contributing a single primary adherence effect size (`R1`–`R4`).

| Study ID | Effect ID | Patients analysed (N) | Study-level estimate (log-RR scale) | 95% CI (log scale) | Corresponding RR (95% CI) | Share of total sample |
|---|---|---|---|---|---|---|
| study_1 | R1 | 1,176 | 0.2450 | 0.130 to 0.360 | 1.28 (1.14 to 1.43) | 13.2% |
| study_2 | R2 | 5,194 | 0.0631 | 0.009 to 0.118 | 1.07 (1.01 to 1.13) | 58.4% |
| study_3 | R3 | 872 | 1.3567 | 1.207 to 1.506 | 3.88 (3.34 to 4.51) | 9.8% |
| study_4 | R4 | 1,657 | 0.2521 | 0.155 to 0.349 | 1.29 (1.17 to 1.42) | 18.6% |
| **Total** | — | **8,899** | — | — | **Pooled RR 1.734 (0.734 to 4.094)** | 100% |

All four trials compared a bundled implementation strategy — education plus some combination of audit and feedback, local champions, and written protocols or clinical pathways, in some cases accompanied by redesign of care delivery — against usual practice in acute stroke inpatients, and all four reported a patient-level process-of-care adherence proportion at the end of the intervention period. The largest trial (`study_2`, 5,194 patients, 58.4% of the pooled sample) contributed the smallest effect; the smallest trial (`study_3`, 872 patients, 9.8% of the sample) contributed by far the largest effect. That inverse pattern between study size and effect magnitude is the central feature of this dataset and recurs in every section below.

# Effect Sizes

Effect sizes were computed on the risk-ratio scale as specified. A note on labelling is warranted for transparency: the per-study estimates are carried in the analysis pipeline's generic effect-size field (named `hedges_g` in the data structure), but the analysis metadata records `effect_measure = "RR"`, `computation_scale = "RR"`, `measure_label = "Risk Ratio (RR)"` and `native_pooling_used = true`. The study-level values and their intervals are therefore reported above both on the log-RR pooling scale (as supplied) and as exponentiated risk ratios. **The pooled statistic reported in this review is a Risk Ratio (RR), not a Hedges' g**, and no standardized-mean-difference fallback was used.

The four study-level estimates were:

- **study_1 (R1):** 0.2450 (95% CI 0.130 to 0.360) on the log-RR scale → **RR ≈ 1.28 (1.14 to 1.43)**, n = 1,176. Approximately a 28% relative increase in the proportion of patients receiving the recommended process of care.
- **study_2 (R2):** 0.0631 (95% CI 0.009 to 0.118) → **RR ≈ 1.07 (1.01 to 1.13)**, n = 5,194. A small but statistically detectable 7% relative increase, in much the largest trial.
- **study_3 (R3):** 1.3567 (95% CI 1.207 to 1.506) → **RR ≈ 3.88 (3.34 to 4.51)**, n = 872. A near-quadrupling of the adherence proportion — an outlier of a magnitude rarely seen in implementation trials, and most plausibly reflecting a near-zero baseline adherence rate in the control arm for the process being measured.
- **study_4 (R4):** 0.2521 (95% CI 0.155 to 0.349) → **RR ≈ 1.29 (1.17 to 1.42)**, n = 1,657. Closely concordant with study_1.

Three of the four estimates (study_1, study_3 excepted, study_4) cluster in the RR 1.07–1.29 band; study_3 sits almost an order of magnitude away on the ratio scale. Critically, **all four individual confidence intervals exclude the null (RR = 1)** and all four point in the same direction — towards greater adherence in the implementation arm. The disagreement between trials is therefore entirely about *magnitude*, not about *direction*.

The distribution of effect sizes is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between effect magnitude and study size/precision in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

# Meta-Analytic Result(s)

A single meta-analytic group was specified (one outcome domain — adherence to the recommended process of care at end of intervention), so one pooled estimate is reported; no separate outcome or timepoint groups required independent pooling, and no group was flagged as having insufficient data.

**Random-effects (REML) pooled result, k = 4, N = 8,899 patients:**

| Quantity | Value |
|---|---|
| Effect measure | Risk Ratio (RR) — native pooling confirmed |
| Pooled RR | **1.734** |
| 95% confidence interval | **0.734 to 4.094** |
| p-value | **0.2094** |
| Favours | **Neither arm** (essentially a tie; ratio measure whose favourability depends on which event was counted) |
| k (studies) | 4 |
| N (patients) | 8,899 |
| τ² (log-RR scale) | 0.754487 |
| I² | 99.04% |
| Q (df = 3) | 75.239 (p < 0.001) |
| Estimator | REML |

The point estimate of 1.734 corresponds, taken at face value, to patients in the multifaceted implementation arm being roughly 73% more likely to receive the recommended process of care than patients under usual practice. However, **the 95% confidence interval (0.734 to 4.094) crosses the null and the result is not statistically significant (p = 0.2094)**. In accordance with the direction field carried with this analysis, the pooled result **favours neither arm**: it is compatible both with a reduction in adherence of about one quarter and with a more than fourfold increase. The pooled average is, in plain terms, uninformative about the true average effect.

This creates an apparent paradox that deserves to be stated explicitly rather than smoothed over: every one of the four contributing trials individually showed a statistically significant *increase* in adherence, yet the pooled estimate is non-significant. This is not an error. It is the direct arithmetic consequence of extreme between-study heterogeneity. Because τ² (0.754487) is one to three orders of magnitude larger than the within-study sampling variances (which range from approximately 0.0008 to 0.0058 on the log scale), the random-effects model assigns the four studies almost identical weights (each approximately 25%, irrespective of whether a trial enrolled 872 or 5,194 patients), and then widens the confidence interval around the average to reflect the enormous dispersion of the underlying true effects. With only three degrees of freedom and τ² of that size, the uncertainty about *where the centre of the distribution of true effects lies* swamps the precision of any individual trial. A random-effects model with k = 4 and I² of 99% is being asked to estimate a distribution from four points that do not agree; it correctly returns a wide, null-spanning answer.

The forest plot — showing each study's estimate, confidence interval and weight alongside the pooled diamond — is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The cumulative meta-analysis, which shows how the pooled estimate and its interval evolve as studies are added in order of precision, is at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`; it illustrates how the addition of the single high-effect trial (study_3) pulls the pooled point estimate upward while simultaneously inflating τ² and widening the interval to span the null.

A 95% prediction interval — the range within which the true effect in a new, comparable trial would be expected to fall — was not part of the pre-specified output, but given τ² = 0.754487 and k = 4 it would necessarily extend from far below RR = 1 to far above RR = 4. No useful prediction for a future trial can be made from these data.

# Heterogeneity

Heterogeneity in this dataset is at the practical maximum:

- **Cochran's Q = 75.239 on 3 degrees of freedom, p < 0.001** — the hypothesis that all four trials estimate a common effect is decisively rejected. Q is roughly 25 times its expected value under homogeneity.
- **I² = 99.04%** — essentially all of the observed variability in effect estimates reflects real differences in underlying effects rather than sampling error. Conventional thresholds describe I² above 75% as "considerable"; 99% is beyond the range in which averaging is ordinarily considered meaningful.
- **τ² = 0.754487** on the log-RR scale, i.e. a between-study standard deviation of τ ≈ 0.869 in log units. Interpreted on the ratio scale, this implies that trial-to-trial variation in the true risk ratio spans roughly a factor of e^(±1.96 × 0.869) ≈ ×/÷ 5.5 around the central value — consistent with the observed spread from RR 1.07 to RR 3.88.

The heterogeneity diagnostics are summarised graphically at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

What drives it? With k = 4 this cannot be tested, but the structure of the data points clearly at study_3, whose RR of 3.88 lies far outside the 1.07–1.29 band formed by the other three. Removing study_3 would leave three trials with closely overlapping estimates in a narrow range and would almost certainly yield a small, precise, statistically significant pooled benefit of roughly RR 1.1–1.3; retaining it produces the null-spanning result reported above. Substantively, the most likely explanations for such an outlier in implementation research are (i) a floor effect — a process of care that was essentially never performed under usual practice, so that any improvement produces a very large ratio from a tiny denominator of baseline events; (ii) a different and more "switch-like" process of care (e.g. introduction of a screening step that simply did not exist before) compared with incremental improvements in already-common practices; and (iii) differences in intervention intensity, particularly the presence or absence of care-delivery redesign on top of education and feedback. All three are entirely plausible mechanisms and none can be adjudicated with four studies.

The key interpretive consequence is that **the pooled risk ratio of 1.734 should not be read as "the" effect of multifaceted implementation interventions in stroke**. There is no single effect to estimate here. There is, instead, a consistent direction of benefit across heterogeneous programmes whose magnitude depends profoundly on what is being implemented, from what baseline.

# Moderators

No moderator or subgroup analyses were conducted. With **k = 4 studies and a single effect size per study**, meta-regression is not interpretable: any single covariate would consume one or more of the three available degrees of freedom, confidence intervals on moderator coefficients would be uninformative, and the risk of spurious findings is very high. Pre-specified moderators of substantive interest — the specific process of care targeted (thrombolysis vs dysphagia screening vs protocolised fever/glucose/swallow management vs general pathway adherence), the number and type of bundle components, the presence or absence of care-delivery redesign, randomisation unit (cluster vs individual), control-arm baseline adherence, and risk of bias — could not be examined.

The bubble plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` displays effect size against study size/precision and is presented as a descriptive diagnostic only, not as a fitted moderator model. It shows the inverse size–effect pattern already noted: the largest study has the smallest effect and the smallest study the largest effect. Whether this reflects genuine clinical differences (small trials of "switch-like" processes from near-zero baselines) or small-study bias cannot be separated with these data — and that ambiguity is precisely what the next section addresses.

Readers should treat the absence of moderator analysis as a substantive finding, not an omission: the heterogeneity in this literature is extreme and completely unexplained, and explaining it is the single highest-value target for future research.

# Publication Bias

Small-study effects were assessed despite k = 4 falling well below the recommended minimum of 10 studies for such tests, so the following results carry low statistical power and wide uncertainty and should be read as hypothesis-generating.

- **Egger's regression:** intercept = **−0.8315**, **p = 0.0228**. The test is statistically significant, indicating funnel-plot asymmetry consistent with small-study effects.
- **Trim-and-fill (Duval and Tweedie):** **k₀ = 1** study imputed; bias-adjusted pooled estimate **0.6161** on the log-RR pooling scale (≈ RR 1.85).
- **Overall small-study-effect risk rating: high.**

The two diagnostics tell a partially discordant story, and both halves should be reported. On the one hand, Egger's test is significant, and the overall risk rating is "high", which suggests the pooled estimate may be distorted by selective publication or other small-study mechanisms — a serious concern in implementation research, where small, enthusiastically-run local quality-improvement projects with dramatic before/after contrasts are considerably more likely to be written up and published than null ones. On the other hand, trim-and-fill imputed only **one** hypothetical missing study, and the resulting bias-adjusted estimate (≈ RR 1.85) is not smaller than the primary estimate of RR 1.734 — so the *magnitude* of distortion implied by trim-and-fill is modest, and the adjusted estimate does not overturn the primary finding in either direction.

Three caveats temper any causal reading of the asymmetry. First, with k = 4, Egger's regression is fitted on two residual degrees of freedom; a single influential point (study_3) can generate a significant intercept on its own. Second, funnel asymmetry in this dataset is indistinguishable from the extreme heterogeneity documented above — when I² is 99.04%, asymmetry is expected even under complete absence of publication bias, because effect size is correlated with study characteristics (baseline adherence, process type) that also correlate with study size. Third, in implementation science specifically, small trials genuinely tend to target low-baseline, high-headroom processes in motivated single centres, which produces large true effects rather than biased ones.

The operational implication is therefore: report the trim-and-fill–adjusted estimate alongside the primary result (done above), and **downgrade certainty for publication bias** in any GRADE-style assessment — while recognising that the detected asymmetry may arise from heterogeneity and methodological diversity rather than from suppression alone.

# Discussion

This meta-analysis of four controlled trials and 8,899 hospitalised stroke patients produced a pooled Risk Ratio of **1.734 (95% CI 0.734 to 4.094; p = 0.2094)** for adherence to the recommended process of care with multifaceted implementation interventions versus usual practice. Per the direction field accompanying the analysis, the pooled result **favours neither arm**.

The most important message of this review is the dissociation between the consistency of the individual trials and the uninformativeness of their average. All four trials reported a statistically significant improvement in the proportion of patients receiving the recommended process of care, with relative increases of approximately 7%, 28%, 29% and 288%. Not one trial found harm, and not one found a null effect. Yet because the magnitudes differ so radically (I² = 99.04%, τ² = 0.754487), the random-effects model — which must estimate both the centre and the spread of a distribution of true effects from four points — returns a confidence interval wide enough to include no effect at all. Interpreting this as evidence that implementation interventions do not increase adherence would be a serious misreading. The correct interpretation is that **the average effect is not estimable with useful precision from the available evidence**, while the *direction* of effect is strikingly consistent.

This pattern is familiar in implementation science and has a straightforward explanation. The "effect" of an implementation bundle is not a property of the bundle alone; it is a joint property of the bundle, the process being implemented, and the headroom available in the control arm. Improving a process already performed for 85% of patients cannot yield a risk ratio above about 1.18 by arithmetic necessity, however excellent the intervention — which is the likely situation in the large study_2 (RR 1.07). Introducing a process performed for only a small minority of patients at baseline can yield a risk ratio of 3.88 (study_3) with a programme that is not necessarily any better designed. Ratio measures are intrinsically baseline-dependent, which is exactly the caveat embedded in the direction field's note that for a ratio measure favourability depends on which event was counted. Pooling such effects on the ratio scale across heterogeneous processes mixes together quantities that are not commensurable, and I² of 99% is the model's way of saying so.

Clinically, three of the four trials converge on a modest but real improvement of roughly 7–29% relative increase in process adherence — plausible, consistent with the wider literature on audit and feedback and on multifaceted quality-improvement strategies, and worth having at scale, since process measures such as dysphagia screening, thrombolysis delivery and protocolised fever/glucose/swallow management are themselves linked to patient outcomes. The fourth trial suggests that where a recommended process is essentially absent at baseline, a well-constructed bundle can transform practice. Neither finding justifies the pooled point estimate of 1.734 as a planning figure for a new programme; a service planning an implementation initiative would do better to identify the trial whose target process and baseline adherence most closely resemble its own situation and to use that estimate.

Methodologically, this review illustrates a general point about small, heterogeneous meta-analyses: a non-significant pooled result with I² = 99% and k = 4 conveys almost no evidence of absence. Statistical power to detect a common effect is not the binding constraint — the binding constraint is that no common effect exists to detect.

# Data Quality and Validation Notes

No automated validation flags were raised for this analysis. For completeness and transparency, the following data-handling points apply:

- **Effect-measure provenance.** The pooled statistic is a Risk Ratio (RR). The measure was set by explicit user request, no conflicting measure specification was detected (`effect_measure_conflict = null`), and **native risk-ratio pooling was used** (`native_pooling_used = true`). The result is therefore a confirmed native-scale risk ratio, not a standardized fallback. Per-study values are stored in the pipeline's generic effect-size field but were computed and pooled on the risk-ratio (log) scale; readers should not interpret them as Hedges' g.
- **Single outcome group.** Only one meta-analytic group was defined, so all four studies were pooled together; no outcome or timepoint group was split off, and no group was flagged as having insufficient data for pooling.
- **No double-counting.** Each trial contributed exactly one effect size (its own primary adherence/process measure), so no patients are counted more than once in the pooled total of 8,899.
- **Unit of analysis.** All denominators are patient-level. Cluster-randomised trials, where present, were handled by using reported cluster-adjusted estimates or by design-effect inflation of the standard error (ICC assumed 0.05 where not reported); hospitals/clusters were never used as the unit of analysis.
- **Small-study diagnostics below recommended k.** Egger's test and trim-and-fill were run on k = 4, below the conventional minimum of 10 studies; both are reported with that limitation stated explicitly.

# Limitations

1. **Very small number of studies (k = 4).** Four trials is at the lower limit for random-effects pooling. The between-study variance τ² is itself estimated with great imprecision from three degrees of freedom, which propagates directly into the width of the pooled confidence interval and is a major reason the interval spans the null.
2. **Extreme, unexplained heterogeneity (I² = 99.04%, τ² = 0.754487, Q = 75.239, p < 0.001).** The assumption underlying any pooled average — that the studies estimate effects drawn from a reasonably coherent distribution — is strained to breaking point. The pooled risk ratio should be regarded as a descriptive summary of four disparate numbers rather than an estimate of a meaningful common quantity.
3. **No moderator analysis possible.** Process type, bundle composition, presence of care-delivery redesign, baseline adherence, randomisation unit and risk of bias could not be examined as explanations for the heterogeneity, because k = 4 leaves no usable degrees of freedom.
4. **Evidence of small-study effects (Egger's p = 0.0228, risk rated "high").** Although trim-and-fill imputed only one study and did not reduce the estimate, the significant asymmetry means that selective publication cannot be excluded, and certainty must be downgraded accordingly. Conversely, the asymmetry test is itself unreliable at this k and may simply be detecting the heterogeneity.
5. **Baseline-dependence of the ratio measure.** Risk ratios for process adherence are bounded by control-arm baseline performance. Pooling across trials with very different baselines (plausibly from near-zero to high) mixes non-commensurable quantities; a risk-difference or odds-ratio analysis, or stratification by baseline adherence, might behave differently, but could not be undertaken with the available extracted data.
6. **Heterogeneity of the outcome construct.** "The recommended process of care" encompasses materially different targets across trials (thrombolysis delivery, dysphagia screening, protocolised management, pathway adherence). Each trial's own primary process measure was used, which maximises fidelity to trial design but reduces the clinical coherence of the pooled construct.
7. **Clustering and design assumptions.** Where cluster-adjusted estimates were unavailable, an assumed ICC of 0.05 was applied. Over- or under-estimation of the true ICC would respectively over- or under-state precision for the affected trials, although with τ² dominating the weights, the practical impact on the pooled estimate is likely to be small.
8. **Risk of bias in included trials.** Blinding of clinicians to an implementation intervention is impossible by design, and outcome ascertainment often relies on routine documentation, which the intervention itself may improve (documentation vs care-delivery artefact). Some apparent adherence gains may partly reflect better recording rather than better care.
9. **No patient outcomes.** This review addresses process adherence only. Whether the observed process improvements translated into reductions in death or disability was not assessed and cannot be inferred.
10. **No prospective registration of this specific synthesis** and no formal GRADE table were produced; certainty judgements offered here are narrative.

# Conclusion

Across four controlled trials and 8,899 patients hospitalised with acute stroke, multifaceted implementation interventions — education, audit and feedback, local champions and protocols or clinical pathways, with or without care-delivery redesign — were associated with higher adherence to recommended processes of care in **every individual trial**, with relative increases ranging from approximately 7% to nearly fourfold and all four confidence intervals excluding the null. However, the random-effects pooled **Risk Ratio of 1.734 (95% CI 0.734 to 4.094; p = 0.2094)** is not statistically significant and, per the direction field for this analysis, **favours neither arm**, because between-study heterogeneity is extreme (I² = 99.04%, τ² = 0.754487, Q = 75.239, p < 0.001) and the number of studies is very small (k = 4). Egger's test indicated significant funnel asymmetry (p = 0.0228, risk rated high), although trim-and-fill imputed only one study (k₀ = 1) and its adjusted estimate (≈ RR 1.85) was no smaller than the primary result.

The honest summary is therefore twofold. **Direction:** the available trials are unanimous that multifaceted implementation interventions increase the proportion of acute stroke inpatients who receive recommended care. **Magnitude:** the size of that increase varies so enormously with the process targeted and the baseline level of performance that no single pooled risk ratio describes it, and the pooled average should not be used as a planning estimate. Certainty in the pooled effect is **very low**, downgraded for imprecision, very serious inconsistency, and suspected publication bias.

For practice, services should expect a multifaceted bundle to improve process adherence, with the greatest absolute and relative gains where current performance is poorest, and should select comparator evidence matched to their own target process and baseline. For research, the priority is no longer to ask *whether* multifaceted implementation works, but to build an evidence base large enough and sufficiently standardised — common process definitions, reported baseline adherence, reported ICCs, risk-difference as well as ratio measures, and pre-specified bundle taxonomies — to explain *why* its effects differ by a factor of five between hospitals.

# References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. *Introduction to Meta-Analysis*. 2nd ed. Chichester: Wiley; 2021.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
5. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *J Educ Behav Stat*. 2005;30(3):261–293.
6. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
7. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
8. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
9. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
10. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
11. Donner A, Klar N. *Design and Analysis of Cluster Randomization Trials in Health Research*. London: Arnold; 2000.
12. Campbell MK, Piaggio G, Elbourne DR, Altman DG; CONSORT Group. CONSORT 2010 statement: extension to cluster randomised trials. *BMJ*. 2012;345:e5661.
13. Ivers N, Jamtvedt G, Flottorp S, et al. Audit and feedback: effects on professional practice and healthcare outcomes. *Cochrane Database Syst Rev*. 2012;(6):CD000259.
14. Grimshaw JM, Eccles MP, Lavis JN, Hill SJ, Squires JE. Knowledge translation of research findings. *Implement Sci*. 2012;7:50.
15. Powell BJ, Waltz TJ, Chinman MJ, et al. A refined compilation of implementation strategies: results from the Expert Recommendations for Implementing Change (ERIC) project. *Implement Sci*. 2015;10:21.
16. Middleton S, McElduff P, Ward J, et al. Implementation of evidence-based treatment protocols to manage fever, hyperglycaemia, and swallowing dysfunction in acute stroke (QASC): a cluster randomised controlled trial. *Lancet*. 2011;378(9804):1699–1706.
17. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336(7650):924–926.

## Figures

- **Forest plot** (study-level risk ratios, confidence intervals, weights and pooled diamond): `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
- **Cumulative meta-analysis** (pooled estimate by accumulating evidence): `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
- **Effect-size distribution**: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
- **Bubble chart** (effect size vs study size/precision; descriptive only): `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`
- **Heterogeneity summary**: `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| Adherence to evidence-based recommended processes of acute stroke care | 4 | Risk Ratio (RR) | Yes | 1.7338 [0.7342, 4.0940] |
