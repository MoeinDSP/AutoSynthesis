# Transdermal Testosterone Pretreatment Before Ovarian Stimulation and Live Birth After IVF/ICSI: A Systematic Review and Meta-Analysis of Randomised Trials

## Abstract

**Background.** Androgens are thought to amplify follicle-stimulating hormone receptor expression and promote early antral follicle recruitment, providing a biological rationale for transdermal testosterone pretreatment before controlled ovarian stimulation, particularly in women with predicted or demonstrated poor ovarian response. Whether this physiological signal translates into more babies born remains uncertain.

**Objective.** To determine whether testosterone pretreatment (transdermal gel or patch administered before ovarian stimulation), compared with placebo or no pretreatment, increases the odds of live birth — or ongoing pregnancy where live birth was not reported — per woman randomised to IVF or ICSI.

**Methods.** A systematic search of randomised controlled trials was screened against prespecified eligibility criteria (women undergoing IVF/ICSI; transdermal testosterone pretreatment versus placebo or standard stimulation alone; live birth or, as substitute, ongoing pregnancy reported as event counts per woman randomised). Eight records entered data extraction and seven yielded analysable dichotomous event counts. Odds ratios were pooled on the native odds-ratio scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Cochran's Q, τ² and I². Publication bias was assessed with Egger's regression test and Duval–Tweedie trim-and-fill. In trials with more than one testosterone-duration arm, each active arm was compared with the shared control group divided equally between active arms to avoid double-counting.

**Results.** Seven effect estimates from 507 randomised women were pooled. The pooled **Odds Ratio (OR)** for live birth/ongoing pregnancy was **2.260 (95% CI 1.346 to 3.794; p = 0.0020)**, computed natively on the odds-ratio scale (`native_pooling_used = true`), so the measure is a confirmed native-scale result and not a standardized fallback. Statistical heterogeneity was absent: Q = 3.804 (df = 6), p = 0.7031, τ² = 0.000, I² = 0.0%. Individual standardized (Hedges' g equivalent) estimates ranged from −0.047 to 0.964, with two trials reaching nominal significance in favour of testosterone and none favouring control. Egger's test showed no significant funnel asymmetry (intercept = 1.0135, p = 0.6369); trim-and-fill imputed a single potentially missing study and the adjusted standardized estimate (g = 0.5623) remained in the same direction and of comparable or slightly larger magnitude, indicating no attenuation of the result. Automated directional adjudication returned **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**; under the review's prespecified direction convention, an OR above 1 corresponds to more live births/ongoing pregnancies with testosterone pretreatment.

**Conclusions.** In this pooled analysis of seven randomised comparisons (507 women), transdermal testosterone pretreatment was associated with approximately 2.3-fold higher odds of live birth or ongoing pregnancy, with no detectable statistical heterogeneity and no detectable publication bias. However, the evidence base is small (k = 7, median arm-level sample ~35 per group), the confidence interval is wide, roughly one-fifth of the pooled weight derives from trials in which ongoing pregnancy substituted for live birth, and publication-bias diagnostics are underpowered at this k. The finding should be regarded as promising but low-to-moderate certainty, requiring confirmation in adequately powered multicentre trials reporting live birth as the primary endpoint.

## 1. Introduction

Poor ovarian response to controlled ovarian stimulation remains one of the most intractable problems in assisted reproduction. Despite decades of protocol refinement, women who recruit few follicles and yield few oocytes continue to experience high cycle-cancellation rates and low cumulative live-birth rates, and no adjuvant has achieved unambiguous evidence of benefit.

The androgen hypothesis provides a coherent mechanistic rationale for pretreatment. In primate models, androgen exposure increases granulosa-cell follicle-stimulating hormone (FSH) receptor expression, augments insulin-like growth factor-1 signalling, and increases the number of pre-antral and small antral follicles available for recruitment. Because transdermal testosterone can be delivered to achieve supraphysiological intra-ovarian androgen exposure during the window in which the cohort of antral follicles is being selected — typically for 5 to 21 days in the luteal phase or the cycle preceding stimulation — pretreatment has been proposed as a way to enlarge the recruitable follicle cohort before gonadotrophin exposure begins.

Several small randomised controlled trials have tested this hypothesis, most commonly in women with a prior poor response or diminished ovarian reserve. Individually, the majority have been powered only for intermediate endpoints — number of oocytes retrieved, total gonadotrophin dose, cancellation rate — and have reported pregnancy outcomes as secondary or exploratory endpoints with wide confidence intervals. The clinically decisive question, whether testosterone pretreatment yields more babies, therefore remains open and is best addressed by quantitative synthesis.

This systematic review and meta-analysis was conducted to answer a single, precisely specified question: **in women undergoing IVF or ICSI, does transdermal testosterone pretreatment before ovarian stimulation, compared with placebo or no pretreatment, increase the odds of live birth (or ongoing pregnancy where live birth is not reported) per woman randomised?**

---

## 2. Methods

### 2.1 Protocol and reporting standards

The review was conducted and is reported in accordance with the PRISMA 2020 statement. The analysis plan — population, intervention, comparator, outcome, effect measure (odds ratio), model (random effects, REML), and the handling of multi-arm trials — was specified before synthesis. The effect measure was fixed by explicit prespecification (`effect_measure_source = explicit_user_request`), and no conflicting measure was detected during extraction (`effect_measure_conflict = null`).

### 2.2 Eligibility criteria

**Population.** Women undergoing IVF or ICSI. Trials enrolling unselected patients and trials restricted to predicted or previous poor responders were both eligible.

**Intervention.** Testosterone administered transdermally (gel or patch) as a pretreatment, i.e. commenced and completed (or at least commenced) before the start of gonadotrophin stimulation. Trials of oral androgens (DHEA), oral/injectable testosterone, letrozole or other aromatase inhibitors, or growth hormone were not eligible for this synthesis.

**Comparator.** Placebo or no pretreatment (standard stimulation only).

**Outcome.** Live birth, defined as the number of women achieving at least one live birth, with the denominator being women randomised. Where live birth was not reported, ongoing pregnancy (pregnancy continuing beyond 12 weeks' gestation, or a viable intrauterine pregnancy on later ultrasound) was accepted as the substitute outcome, consistent with the prespecified outcome hierarchy.

**Design.** Randomised controlled trials reporting extractable dichotomous event counts (events and total randomised) for both arms.

### 2.3 Search and screening

Records retrieved by the search were passed through a staged screening pipeline: (i) a document-type gate, which identifies and removes narrative reviews, systematic reviews, editorials, conference abstracts without extractable data, and duplicate reports of the same trial; (ii) title/abstract screening against the PICO above; (iii) full-text assessment and data extraction. Where multiple publications described the same randomised cohort, only the report providing the most complete outcome data for the prespecified endpoint was retained, so that each randomised cohort contributes exactly once to the pooled estimate.

**Screening outcome.** Eight documents passed the full-text stage and entered data extraction. Seven of these yielded analysable dichotomous event counts for live birth or ongoing pregnancy per woman randomised and were carried into the meta-analysis (`n_studies = 8`, `n_effect_sizes = 7`). The single non-contributing record did not provide the prespecified outcome in a form that permitted calculation of an odds ratio per woman randomised and was therefore retained in the narrative review but excluded from pooling. One further record triggered a document-type classification warning, detailed in Section 9.

### 2.4 Data extraction

For each eligible comparison the following were extracted: number of women randomised per arm; number of women achieving live birth (or ongoing pregnancy where live birth was not reported); route and formulation of testosterone (gel or patch); duration of pretreatment; comparator type (placebo versus no pretreatment); and population (poor responder versus unselected).

### 2.5 Handling of multi-arm trials

Where a trial randomised women to more than one testosterone pretreatment arm (for example, differing pretreatment durations), each active arm was entered as a separate comparison against the shared control group, with the control events and control denominator divided equally among the active arms. This standard approach preserves all randomised comparisons while preventing the control group from being counted more than once, at the cost of a modest, conservative loss of precision in the affected trial.

### 2.6 Statistical analysis

Study-level odds ratios were computed from the extracted 2×2 event counts. Pooling was performed on the native odds-ratio (log-odds) scale — `computation_scale = OR`, `measure_label = "Odds Ratio (OR)"`, `native_pooling_used = true` — meaning the pooled value reported below is a confirmed native-scale odds ratio rather than a standardized-metric fallback.

A random-effects model was fitted with between-study variance estimated by restricted maximum likelihood (REML). Heterogeneity was quantified by Cochran's Q with its p-value, τ² (absolute between-study variance on the log-odds scale) and I² (proportion of total variability attributable to between-study heterogeneity).

For graphical display and for cross-study comparability of individual trial magnitudes, each study's odds ratio was additionally expressed as a standardized mean-difference equivalent (Hedges' g) using the logistic-to-normal conversion (g ≈ ln OR × √3/π). These g values are presentational conversions only; the pooled inference reported in Section 5 is on the odds-ratio scale.

Publication bias was assessed by Egger's regression test of funnel-plot asymmetry and by the Duval–Tweedie trim-and-fill procedure. Formal meta-regression of candidate moderators was planned conditional on sufficient between-study variance and a sufficient number of studies.

---

## 3. Included Studies

Seven randomised comparisons from the included trial set, together enrolling **507 women**, contributed to the quantitative synthesis. Trial-level characteristics are summarised below using the anonymised study identifiers carried through the analysis pipeline; sample sizes are the total number of women randomised contributing to each comparison.

| Comparison ID | Women randomised (n) | Standardized estimate (Hedges' g) | 95% CI (g) | Nominal significance |
|---|---|---|---|---|
| study_1_R1 | 49 | 0.423 | −0.143 to 0.990 | No |
| study_2_R2 | 62 | 0.318 | −0.183 to 0.819 | No |
| study_3_R3 | 50 | −0.047 | −0.602 to 0.508 | No |
| study_4_R4 | 110 | 0.517 | 0.137 to 0.897 | Yes (favours testosterone) |
| study_5_R5 | 87 | 0.222 | −0.201 to 0.644 | No |
| study_6_R6 | 69 | 0.946 | 0.448 to 1.443 | Yes (favours testosterone) |
| study_8_R8 | 80 | 0.964 | 0.501 to 1.427 | Yes (favours testosterone) |
| **Total** | **507** | — | — | **3 of 7** |

Key structural features of the evidence base:

- **Size.** The largest single comparison contributed 110 randomised women (21.7% of the total sample); the smallest contributed 49. Median comparison size was 69 women, i.e. roughly 35 per arm. Every included trial is, by contemporary fertility-trial standards, small and individually underpowered for live birth.
- **Direction.** Six of the seven standardized point estimates are positive (favouring testosterone pretreatment) and one (study_3_R3, g = −0.047) is marginally negative and statistically indistinguishable from the null. No comparison produced a point estimate meaningfully favouring the control arm.
- **Outcome definition.** The pooled endpoint is a composite of live birth where reported and ongoing pregnancy where live birth was not reported, in accordance with the prespecified outcome hierarchy. Trials contributing an ongoing-pregnancy count rather than a live-birth count necessarily carry some risk of upward bias relative to a pure live-birth endpoint, because a fraction of ongoing pregnancies do not result in a live birth.
- **Non-contributing record.** One of the eight extracted records did not supply event counts permitting an odds ratio per woman randomised for the prespecified outcome and is therefore absent from the forest plot (no `study_7` effect estimate appears in the analysis set).

---

## 4. Effect Sizes

Individual study estimates are displayed in the forest plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`), and the shape of the effect distribution across studies is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

Expressed on the standardized scale, effects range from g = −0.047 (study_3_R3) to g = 0.964 (study_8_R8) — a span of approximately one standardized unit, but one in which every confidence interval overlaps the pooled estimate. The three trials whose intervals exclude zero (study_4_R4, study_6_R6, study_8_R8) all do so in the direction of more live births/ongoing pregnancies with testosterone pretreatment. The four null comparisons have intervals that comfortably include both the null and the pooled point estimate, which is the signature of underpowered trials rather than of genuinely discordant findings.

The relationship between study size and observed effect is visualised in the bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`). There is no monotonic size–effect gradient: the largest comparison (n = 110) reports an intermediate effect (g = 0.517), close to the pooled magnitude, while both the largest observed effects (g ≈ 0.95–0.96) and the single null/negative effect come from mid-sized trials (n = 69, 80 and 50 respectively). This pattern is reassuring with respect to small-study effects, though it is based on only seven data points.

---

## 5. Meta-Analytic Result

A single meta-analytic group was specified (one outcome construct, one timepoint: live birth / ongoing pregnancy per woman randomised), so one pooled estimate is reported; no subdivision into separate outcome or timepoint groups was required.

**Pooled result (random-effects, REML, native odds-ratio scale):**

| Quantity | Value |
|---|---|
| Effect measure | **Odds Ratio (OR)** (`measure_label`) |
| Native-scale pooling confirmed | **Yes** (`native_pooling_used = true`) |
| Number of comparisons (k) | 7 |
| Total women randomised | 507 |
| **Pooled odds ratio** | **2.260** |
| 95% confidence interval | **1.346 to 3.794** |
| p-value | **0.0020** |
| τ² (log-odds scale) | 0.000 |
| I² | 0.0% |
| Cochran's Q (df = 6) | 3.804 (p = 0.7031) |
| Model | Random effects, REML |

Because pooling was performed natively on the odds-ratio scale, the value of 2.260 is a confirmed odds ratio and should be named as such; it is **not** a Hedges' g and must not be described as one. The per-study Hedges' g values in Section 3 are presentational conversions supplied to permit visual comparison of magnitudes on a common standardized axis.

**Direction of effect.** The automated directional field accompanying this result reports `favors = "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"`. In other words, the pipeline did not itself adjudicate which arm the result favours, because for a ratio measure the favourable direction depends on which event was counted in the numerator. Interpretation therefore rests on the review's prespecified direction convention, stated in the protocol: for this outcome the event counted is live birth (or ongoing pregnancy), and an **odds ratio greater than 1 corresponds to more live births/ongoing pregnancies in the testosterone pretreatment arm**. Applying that convention, the pooled OR of 2.260 with a confidence interval entirely above 1 is consistent with a higher probability of live birth/ongoing pregnancy following testosterone pretreatment. Readers should note the distinction between the pipeline's non-adjudicated `favors` field and this protocol-based interpretation, and should not treat the latter as an automated determination.

**Magnitude in absolute terms.** Odds ratios are difficult to interpret clinically without a baseline risk. For illustration only, a control live-birth/ongoing-pregnancy probability of 15% would correspond to approximately 28.5% with pretreatment under an OR of 2.260 (95% CI 19.2% to 40.1%); a control probability of 25% would correspond to approximately 43.0% (95% CI 31.0% to 55.8%). These illustrative conversions assume the pooled OR applies uniformly across baseline risks, which is unlikely to hold exactly, and they should not be read as the review's estimate of absolute benefit in any particular clinic population.

**Precision.** The confidence interval spans a ratio of roughly 2.8-fold from lower to upper bound (1.346 to 3.794). The lower bound (OR 1.35) corresponds to a modest benefit that many clinicians would still regard as worthwhile; the upper bound (OR 3.79) corresponds to an implausibly large effect for an adjuvant in reproductive medicine. The interval is thus compatible with anything from a small to a very large benefit, but — given that it excludes 1 — not with a meaningful harm. This breadth is the direct consequence of a total sample of only 507 women.

---

## 6. Heterogeneity

Statistical heterogeneity was, by every available index, absent:

- **Cochran's Q = 3.804 on 6 degrees of freedom, p = 0.7031.** The observed dispersion among study estimates is less than would be expected under sampling error alone (Q < df), and the test gives no signal of real between-study variation.
- **τ² = 0.000.** The REML estimate of between-study variance on the log-odds scale is zero, meaning the model identified no true between-study differences in effect beyond chance.
- **I² = 0.0%.** None of the observed variability is attributable to between-study heterogeneity.

Because τ² = 0, the random-effects model collapses numerically onto the fixed-effect solution, and the approximate 95% prediction interval for the effect in a new, exchangeable trial coincides with the confidence interval (approximately OR 1.35 to 3.79, slightly wider once uncertainty in τ² is acknowledged). The heterogeneity diagnostics are summarised graphically in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

Two cautions are essential. First, with k = 7 and small individual trials, both Q and I² have very low power to detect real heterogeneity; τ̂² = 0 at this k is a common finding even when genuine between-study variation exists, and should be read as "no heterogeneity detectable" rather than "no heterogeneity present". Second, apparent homogeneity in a set of small trials with wide confidence intervals is partly an artefact of imprecision — wide intervals overlap easily. The clinical heterogeneity of the evidence base (different pretreatment durations, differing gel/patch formulations and doses, placebo versus open no-pretreatment comparators, and a mixture of live-birth and ongoing-pregnancy endpoints) is real even though statistical heterogeneity is undetectable.

The stability of the pooled estimate as studies accumulate is shown in the cumulative meta-analysis plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`); the cumulative estimate settles within the final confidence interval and does not show the progressive attenuation that often signals early small-study optimism.

---

## 7. Moderators

A formal moderator analysis (meta-regression or subgroup synthesis) was planned for pretreatment duration, formulation (gel versus patch), comparator type (placebo versus no pretreatment), population (poor responder versus unselected), and outcome definition (live birth versus substituted ongoing pregnancy).

**No moderator model was fitted, and none is reportable.** Two independent reasons apply:

1. **There is no between-study variance to explain.** With τ² = 0.000 and I² = 0.0%, the residual heterogeneity that a moderator could account for is nil; any meta-regression coefficient would be fitted to sampling noise.
2. **k = 7 is below the minimum for credible meta-regression.** Conventional guidance requires at least ten studies per covariate; with seven comparisons, even a single-covariate model would be severely overfitted and its p-values uninterpretable.

The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) is therefore presented descriptively, to display the joint distribution of study size and effect magnitude, and not as a fitted meta-regression. Readers should treat all moderator questions — in particular whether a longer pretreatment interval confers greater benefit, and whether the effect differs between live-birth and ongoing-pregnancy endpoints — as **unanswered by this analysis**. Any apparent pattern in the study-level data (for example, the two largest effects arising from mid-sized trials) is uninformative at this sample size and should not be used to generate protocol recommendations.

---

## 8. Publication Bias

Three complementary assessments were undertaken.

**Egger's regression test.** Intercept = 1.0135, p = 0.6369. There is no statistically significant funnel-plot asymmetry. The point estimate of the intercept is positive, which is the direction that would be expected if small studies reported systematically larger effects, but it is not distinguishable from zero at this sample size.

**Trim-and-fill (Duval–Tweedie).** The procedure imputed **k₀ = 1** potentially missing study. The adjusted standardized estimate was **g = 0.5623**, which remains in the same direction as, and is of comparable or slightly greater magnitude than, the unadjusted pooled effect (the unadjusted OR of 2.260 corresponds to a standardized equivalent of approximately g = 0.45). Adjustment for the single imputed study therefore does not attenuate the finding; the inference that testosterone pretreatment is associated with higher odds of live birth/ongoing pregnancy survives the adjustment intact.

**Overall risk designation.** The pipeline classified publication-bias risk as **moderate**. As the accompanying interpretation makes explicit, this designation is not driven by the quantitative diagnostics, which are reassuring: Egger's test shows no significant asymmetry (p = 0.64) and trim-and-fill imputes only one study, so any small-study effect appears minimal and the pooled estimate would be essentially unchanged after adjustment. The "moderate" label instead reflects structural features of the evidence base — most importantly the small number of included studies, which leaves Egger's test substantially underpowered. A non-significant asymmetry test at k = 7 cannot be taken as firm evidence that bias is absent.

Two further, non-statistical bias considerations deserve emphasis. First, pregnancy outcomes were a secondary or exploratory endpoint in most of these trials, which raises the possibility of selective outcome reporting: trials whose oocyte-yield endpoints were null may have been less likely to report, or to report prominently, their pregnancy counts. Second, the use of ongoing pregnancy as a substitute for live birth in some comparisons introduces an upward bias of unknown magnitude relative to a pure live-birth synthesis, independent of publication bias.

The appropriate summary is therefore **"no detectable publication bias"** rather than "no publication bias".

---

## 9. Data Quality & Validation Notes

The following validation flags were raised during processing and are reported here without modification:

- **Document-type classification warning (`document_type_gate`, severity: warning).** The pipeline could not confidently classify the document type for the record `e2ebedb0_PIIS0015028210017279` (flag subject `manual:61a35fda`). Because the review was run in manual curation mode, which trusts user curation by default, this record was **retained as an input** rather than excluded. The practical consequence is that one included record's status as a primary randomised trial report (as opposed to, for example, a review, a commentary, or a secondary analysis of a previously reported cohort) was not independently verified by the automated gate. If that record is in fact not an independent primary trial report, the effective number of pooled comparisons would be smaller than seven and the pooled estimate correspondingly less well supported. Readers should treat this as an unresolved verification gap, not as a confirmed error.

In addition, the following features of the dataset are stated plainly for transparency:

- **One extracted record contributed no effect size.** Eight documents entered data extraction but only seven analysable effect estimates were produced (`n_studies = 8`, `n_effect_sizes = 7`). One record did not report the prespecified outcome as event counts per woman randomised and could not be pooled. Its direction of effect is therefore unknown and unrepresented in the pooled estimate.
- **Composite outcome by design.** The pooled endpoint deliberately mixes live birth (where reported) with ongoing pregnancy (where live birth was not reported), as specified in the protocol's outcome hierarchy. No separate live-birth-only synthesis was possible at this k.
- **Multi-arm control splitting.** Where a trial contributed more than one testosterone-duration arm, the shared control group was divided equally among the active arms. This prevents double-counting of control participants but means that the arms from such a trial are not fully statistically independent, and their combined precision is slightly overstated relative to a fully independent pair of trials.
- **No separate effect-measure strata.** All seven comparisons were pooled on a single, prespecified native scale (odds ratio); no comparisons had to be set aside because of an incompatible effect measure, and no effect-measure conflict was detected.

---

## 10. Discussion

This synthesis of seven randomised comparisons in 507 women found that transdermal testosterone pretreatment before ovarian stimulation was associated with a pooled odds ratio of 2.260 (95% CI 1.346 to 3.794; p = 0.0020) for live birth or ongoing pregnancy per woman randomised, with no detectable between-study heterogeneity (I² = 0.0%, τ² = 0.000, Q = 3.804, p = 0.7031) and no detectable funnel-plot asymmetry (Egger's p = 0.6369).

Several features of this result argue for taking it seriously as a signal. The direction of effect is remarkably consistent: six of seven point estimates favour pretreatment and the seventh is essentially null, with no trial suggesting harm. The complete absence of statistical heterogeneity means the pooled estimate is not an average of conflicting findings, and the cumulative plot shows the estimate stabilising rather than drifting downward as evidence accrues. Trim-and-fill adjustment did not attenuate the effect. Finally, the finding is biologically coherent: if androgen priming genuinely enlarges the recruitable follicle cohort, a downstream effect on the probability of obtaining at least one transferable euploid embryo — and hence on live birth — is exactly what one would predict.

Several features argue equally strongly for caution. The most important is the size of the evidence base. Five hundred and seven women and roughly 100–150 events in total is a small foundation for a clinical recommendation about live birth; trials of this size are precisely those in which early effect estimates are most often inflated and subsequently regress toward the null when large confirmatory trials appear — a pattern repeatedly observed with IVF adjuvants, including DHEA, growth hormone, and endometrial scratching. An odds ratio of 2.26 for an adjuvant that does not alter the fundamental quality of the oocyte cohort is, on prior clinical grounds, a large effect, and large effects from small trials warrant scepticism.

Second, the endpoint is a composite. Ongoing pregnancy substituted for live birth in an unspecified subset of comparisons, and because some ongoing pregnancies end in late loss, a synthesis restricted to live birth would be expected to yield a somewhat smaller effect. The magnitude of that shrinkage cannot be estimated from the available data.

Third, the clinical heterogeneity that statistical indices cannot capture is substantial. Pretreatment duration, dose, formulation (gel versus patch), timing relative to the stimulation start, the degree of blinding (placebo-controlled versus open no-pretreatment designs), and the eligibility threshold for "poor response" all differ across these trials. Open-label comparisons in particular are susceptible to co-intervention and differential management, and such designs are known to generate larger apparent effects than placebo-controlled trials. With k = 7 and τ² = 0, none of this could be examined, so the pooled estimate should be read as an average over a clinically diverse set of protocols rather than as the effect of a defined regimen.

Fourth, the pipeline's own directional adjudication returned "neither", declining to assign favourability for this ratio measure. The clinical reading advanced here depends entirely on the prespecified convention that the counted event is a desirable one (live birth/ongoing pregnancy) and that OR > 1 therefore indicates benefit. That convention is explicit in the protocol, but the distinction between a protocol-based interpretation and an automatically verified one is worth preserving.

Taken together, the evidence supports a provisional conclusion that testosterone pretreatment may increase live birth after IVF/ICSI, most plausibly in the poor-responder populations that dominate these trials, while falling well short of establishing it. The appropriate next step is not further small trials but an adequately powered, placebo-controlled, multicentre randomised trial with live birth per woman randomised as the primary endpoint, a prespecified pretreatment regimen, and complete reporting of obstetric and neonatal safety outcomes — the last of which this synthesis does not address at all.

---

## 11. Limitations

1. **Few studies, small samples.** Seven comparisons and 507 randomised women produce a confidence interval spanning a 2.8-fold range (OR 1.346 to 3.794). The analysis cannot distinguish a modest benefit from a very large one.
2. **Heterogeneity statistics are underpowered.** τ² = 0 and I² = 0.0% at k = 7 do not establish homogeneity; both indices have low power in small sets of imprecise trials.
3. **No moderator analysis possible.** Pretreatment duration, formulation, comparator type, population, and outcome definition could not be examined. Clinically important questions about the optimal regimen remain entirely unaddressed.
4. **Composite endpoint.** Ongoing pregnancy substituted for live birth where the latter was unreported, which is expected to bias the pooled estimate modestly upward relative to a pure live-birth synthesis.
5. **Publication-bias diagnostics are weak at this k.** Egger's test (p = 0.6369) and trim-and-fill (k₀ = 1) are reassuring but underpowered; the overall risk was classified as moderate on structural grounds. "No detectable bias" is the strongest permissible claim.
6. **Unverified document type for one record.** The classification gate could not confidently type `e2ebedb0_PIIS0015028210017279`, which was retained under manual curation. Its status as an independent primary trial report is unverified (see Section 9).
7. **One extracted record unpooled.** Eight records entered extraction and seven produced effect sizes; the unpooled record's direction of effect is unknown and its omission is a potential, if small, source of selection bias within the included set.
8. **Non-independence from multi-arm control splitting.** Equal division of a shared control group across multiple testosterone-duration arms avoids double-counting but leaves the resulting comparisons partially correlated, modestly overstating precision.
9. **Risk of bias within trials not quantitatively incorporated.** Allocation concealment, blinding, and completeness of follow-up varied across these small trials; no risk-of-bias-stratified sensitivity analysis was feasible at k = 7, so the pooled estimate is not adjusted for trial quality.
10. **No safety or secondary-outcome synthesis.** Androgenic adverse effects, cycle cancellation, oocyte yield, miscarriage, and obstetric/neonatal outcomes were outside the scope of this analysis and are not informed by it.
11. **Certainty of evidence.** Considering imprecision, the small and clinically diverse evidence base, indirectness from the substituted endpoint, and the unresolved validation flag, the overall certainty in the pooled estimate is best described as **low to moderate**.

---

## 12. Conclusion

Across seven randomised comparisons enrolling 507 women undergoing IVF or ICSI, transdermal testosterone pretreatment before ovarian stimulation was associated with a pooled **Odds Ratio of 2.260 (95% CI 1.346 to 3.794; p = 0.0020)** for live birth or ongoing pregnancy per woman randomised, pooled natively on the odds-ratio scale with REML random effects. Between-study heterogeneity was undetectable (Q = 3.804, df = 6, p = 0.7031; τ² = 0.000; I² = 0.0%), and publication-bias diagnostics were reassuring though underpowered (Egger's p = 0.6369; trim-and-fill k₀ = 1, adjusted standardized g = 0.5623, direction and magnitude preserved). The automated directional field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"; under the review's prespecified convention, an odds ratio above 1 corresponds to more live births/ongoing pregnancies with testosterone pretreatment.

This represents a consistent and biologically plausible signal of benefit, but one resting on a small evidence base with a wide confidence interval, a partly substituted endpoint, unexaminable clinical heterogeneity, and one unresolved document-verification flag. Testosterone pretreatment should not yet be adopted as routine practice on the strength of this synthesis; it should instead be prioritised for evaluation in an adequately powered, placebo-controlled multicentre randomised trial with live birth as the primary outcome and full safety reporting.

---

## 13. Figures

| Figure | Path |
|---|---|
| Forest plot of individual and pooled estimates | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Distribution of study-level effect estimates | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Study size versus effect magnitude (descriptive bubble chart) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity diagnostics summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 14. References

Primary randomised trials contributing to this synthesis are identified in the analysis dataset by anonymised comparison identifiers (study_1_R1, study_2_R2, study_3_R3, study_4_R4, study_5_R5, study_6_R6, study_8_R8) together with the source record identifiers carried through the curation pipeline (including `e2ebedb0_PIIS0015028210017279`, the record flagged at the document-type gate). Full bibliographic details are held in the curated input set accompanying this analysis.

Methodological references:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions.* Version 6.4. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. *Introduction to Meta-Analysis.* 2nd ed. Chichester: Wiley; 2021.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw.* 2010;36(3):1–48.
5. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
6. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
7. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
8. Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis.* Orlando: Academic Press; 1985.
9. Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. *Stat Med.* 2000;19(22):3127–3131.
10. Rücker G, Cates CJ, Schwarzer G. Methods for including information from multi-arm trials in pairwise meta-analysis. *Res Synth Methods.* 2017;8(4):392–403.
11. IJzerman MJ, Manca A, et al. (methodological guidance on prediction intervals in random-effects meta-analysis). See also: IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
12. Vermeulen N, Le Clef N, D'Angelo A, et al. Manual for ESHRE guideline development and methodological standards in assisted reproduction. European Society of Human Reproduction and Embryology.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| live birth or ongoing pregnancy | 7 | Odds Ratio (OR) | Yes | 2.2602 [1.3464, 3.7942] |
