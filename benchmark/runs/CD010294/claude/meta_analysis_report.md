# Vasopressin V2 Receptor Antagonists and Serious Adverse Events in Autosomal Dominant Polycystic Kidney Disease: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Vasopressin type 2 receptor (V2R) antagonists such as tolvaptan and lixivaptan slow kidney volume growth and eGFR decline in autosomal dominant polycystic kidney disease (ADPKD), but their aquaretic, hepatic and metabolic effects raise questions about overall tolerability. Whether V2R antagonism increases, decreases or does not alter the risk of serious adverse events (SAEs) relative to placebo or standard therapy remains uncertain.

**Objective.** To quantify the effect of V2R antagonists versus placebo or standard therapy on the number of participants experiencing one or more investigator-reported SAEs in ADPKD.

**Methods.** A systematic search of randomised controlled trials in ADPKD populations reporting composite SAE counts (any SAE or treatment-emergent SAE) with the number randomised per arm as denominator was conducted and screened in duplicate. Dichotomous data were pooled on the native risk ratio (RR) scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was summarised with Cochran's Q, I² and τ². Small-study effects were assessed with Egger's regression test and the trim-and-fill procedure.

**Results.** Four trials met inclusion criteria; three contributed extractable arm-level SAE data and were pooled (k = 3; N = 1,632 randomised participants). The pooled risk ratio was 0.875 (95% CI 0.245 to 3.118; p = 0.8366), a result that favours **neither** arm — the confidence interval is compatible with both a substantial reduction and a roughly three-fold increase in the risk of experiencing at least one SAE. Between-study heterogeneity was moderate and statistically non-significant (Q = 4.452, df = 2, p = 0.1079; I² = 55.41%; τ² = 0.734936). With only three effect estimates, no moderator or subgroup analyses could be fitted. Egger's test showed no funnel asymmetry (intercept = 0.7114, p = 0.3324) and trim-and-fill imputed no missing studies (k₀ = 0); overall risk of publication bias was rated low, with the caveat of very low power.

**Conclusions.** Current randomised evidence does not demonstrate either an increase or a decrease in serious adverse events with V2R antagonists in ADPKD. The pooled estimate is extremely imprecise and heterogeneous, and should be read as an absence of conclusive evidence rather than as evidence of equivalence. Composite SAE counts also obscure the specific, clinically important hepatic and aquaretic harms that drive monitoring requirements for this drug class.

## 1. Introduction

Autosomal dominant polycystic kidney disease (ADPKD) is the most common monogenic kidney disorder and a leading inherited cause of kidney failure. Cyclic adenosine monophosphate (cAMP)-driven cystogenesis is mediated in substantial part through the vasopressin type 2 receptor (V2R) on the principal cells of the collecting duct, making V2R an attractive pharmacological target. Selective V2R antagonists — most prominently tolvaptan, with lixivaptan and satavaptan also having been evaluated in nephrology populations — reduce intracellular cAMP, attenuate total kidney volume growth, and slow the rate of estimated glomerular filtration rate (eGFR) decline in appropriately selected patients.

Efficacy, however, has never been the principal barrier to widespread use of this class. The therapeutic profile of V2R antagonists is dominated by tolerability considerations: profound aquaresis with polyuria, nocturia and thirst; the potential for hypernatraemia and volume depletion; and, critically, idiosyncratic hepatocellular injury that has required a risk-evaluation-and-mitigation framework with scheduled liver enzyme monitoring. The development programme for lixivaptan was itself discontinued following a hepatic safety signal. In this context, the composite endpoint "number of participants experiencing one or more serious adverse events" is a pragmatic, investigator-adjudicated, regulatory-relevant global index of harm, and is the outcome most consistently reported across randomised trials in this field.

This systematic review and meta-analysis addresses a single, focused question: **what is the effect of V2R antagonists, compared with placebo or standard therapy, on the proportion of randomised participants who experience at least one serious adverse event during an ADPKD trial?** By convention for this analysis, a risk ratio below 1 indicates *fewer* SAEs in the V2R antagonist arm — i.e. the drug appearing safer than control — whereas a risk ratio above 1 indicates a greater burden of serious harm with active treatment.

---

## 2. Methods: Search and Screening

### 2.1 Eligibility criteria

Studies were eligible if they met all of the following:

- **Population:** adults with a clinical or genetic diagnosis of ADPKD.
- **Intervention:** a vasopressin V2 receptor antagonist (tolvaptan, lixivaptan, satavaptan, or a pharmacologically equivalent agent), at any dose or titration schedule.
- **Comparator:** placebo or standard/usual therapy without V2R antagonism.
- **Outcome:** the number of participants experiencing one or more serious adverse events during the trial, as reported by the investigators, with the number randomised in each arm as the denominator. Trial-reported composite SAE counts (labelled "any SAE", "serious treatment-emergent adverse events", or equivalent) were accepted.
- **Design:** randomised controlled trial (parallel-group or randomised withdrawal/extension with a concurrent control).

Narrative reviews, editorials, non-randomised cohorts, single-arm extension phases without a concurrent comparator, and secondary reports that duplicated an already-included randomised population were not eligible as independent data sources.

### 2.2 Information sources and screening

Records were identified through a structured search of the trial and bibliographic literature and processed through an automated-assisted screening pipeline with human verification. Titles and abstracts were screened against the eligibility criteria, and potentially eligible full texts were retrieved and assessed. Where multiple publications described the same randomised cohort, the report providing the most complete arm-level SAE numerator and denominator was retained, and the remainder treated as companion reports so that no participant contributed twice to the pooled estimate.

### 2.3 Data extraction and effect size derivation

For each included trial we extracted the number of participants with ≥1 SAE and the number randomised, separately for the V2R antagonist and control arms. The pre-specified effect measure for this review was the **risk ratio (RR)** on its native binary scale; this was an explicit analytic specification rather than an inference made post hoc from the extracted data (`effect_measure_source: explicit_user_request`), and **native-scale pooling was successfully applied** (`native_pooling_used: true`). The reported pooled statistic is therefore a genuine risk ratio, not a standardised-mean-difference surrogate back-transformed into ratio units, and no measure conflict was recorded during extraction.

For descriptive and diagnostic plotting purposes the pipeline additionally expressed each study's result in a common standardised metric; those per-study standardised values are tabulated in Section 4 but are **not** the basis of the pooled inference, and the pooled result must not be described as a Hedges' *g*.

### 2.4 Synthesis methods

Effect estimates were combined using a random-effects model with between-study variance estimated by **restricted maximum likelihood (REML)**, chosen a priori because variation in dose, trial duration, baseline CKD stage and SAE ascertainment practices makes a common-effect assumption implausible. Heterogeneity was quantified using Cochran's Q with its associated p-value, the I² statistic, and the absolute between-study variance τ². Small-study effects and potential publication bias were examined with Egger's regression test of funnel-plot asymmetry and the Duval–Tweedie trim-and-fill procedure. Moderator analyses were planned conditional on a sufficient number of contributing estimates.

---

## 3. Included Studies

The screening process yielded **four studies** that satisfied the population, intervention and comparator criteria. Of these, **three contributed arm-level serious adverse event data in a form that could be converted into a risk ratio with a randomised denominator**, and these three constitute the analytic sample for the quantitative synthesis (k = 3). The fourth eligible study did not yield an extractable, non-duplicative SAE numerator/denominator pair and therefore contributes to the narrative review but not to the pooled estimate. This discrepancy between the number of included studies (4) and the number of pooled effect estimates (3) is stated here explicitly so that the denominator of the synthesis is not overstated.

The three pooled trials together randomised **1,632 participants**. The analytic set is markedly unbalanced in size: one trial accounts for 1,366 randomised participants (83.7% of the total sample), while the two remaining trials contributed 175 and 91 participants respectively. Precision in the pooled analysis is therefore concentrated overwhelmingly in a single large trial, with the smaller trials contributing comparatively little information but, under the random-effects weighting scheme, disproportionate influence on the estimate of between-study variance.

---

## 4. Effect Sizes

Table 1 presents the study-level estimates as returned by the analysis pipeline, expressed in the standardised diagnostic metric used for plotting. These are reported for transparency and to show the direction and relative precision of each contributing trial; the confirmed pooled inference is on the risk ratio scale (Section 5).

**Table 1. Study-level effect estimates (standardised diagnostic metric) and sample sizes**

| Study label | Standardised estimate | 95% CI | N randomised |
|---|---|---|---|
| study_1_R1 | −1.11028 | [−1.552, −0.668] | 91 |
| study_2_R2 | 0.258537 | [−0.089, 0.607] | 175 |
| study_4_R4 | 0.218106 | [0.112, 0.324] | 1,366 |

Three features of this pattern are analytically important.

1. **The estimates are directionally discordant.** One trial (study_1_R1, the smallest, N = 91) produced a large estimate in the opposite direction from the other two, with a confidence interval that excludes the null. The two larger trials (N = 175 and N = 1,366) both produced small positive estimates, and in the largest trial that estimate also excludes the null.
2. **The confidence intervals of the outlying small trial and the large trial do not overlap**, which is the proximate source of the heterogeneity quantified in Section 6.
3. **Precision is highly asymmetric.** The largest trial has a standardised interval width of approximately 0.21 units, roughly four times narrower than either smaller trial, reflecting its eight- to fifteen-fold larger sample.

The distribution of study-level estimates is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the study-by-study estimates with their confidence intervals and pooled summary are shown in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`.

---

## 5. Meta-Analytic Result

**Table 2. Random-effects pooled result (native risk ratio scale, REML)**

| Quantity | Value |
|---|---|
| Effect measure | Risk Ratio (RR) |
| Native-scale pooling confirmed | Yes |
| Number of pooled estimates (k) | 3 |
| Total randomised participants | 1,632 |
| Pooled risk ratio | **0.875** |
| 95% confidence interval | **0.245 to 3.118** |
| p-value | **0.8366** |
| Between-study variance τ² | 0.734936 |
| I² | 55.41% |
| Cochran's Q (df = 2) | 4.452 (p = 0.1079) |
| Estimation method | REML |
| Favours | **Neither arm** — essentially a tie on a ratio measure |

The pooled risk ratio for experiencing one or more serious adverse events with a V2R antagonist versus placebo or standard therapy was **RR = 0.875 (95% CI 0.245 to 3.118; p = 0.8366)**. Following the `favors` determination carried by the analysis, this result **favours neither arm**: it is statistically indistinguishable from the null on a ratio scale, and the direction of any favourability on a composite harm count additionally depends on which specific events were captured in each trial's SAE definition.

The point estimate, taken at face value, would correspond to a 12.5% relative reduction in the probability of at least one SAE with active treatment. That reading would be an over-interpretation. The confidence interval spans from a 75.5% relative *reduction* in SAE risk to a 3.12-fold relative *increase* — a range that encompasses substantial benefit, exact equivalence, and substantial harm. The width of this interval (a ratio of upper to lower bound of approximately 12.7) is the single most informative feature of the analysis: with three heterogeneous trials and a sizeable between-study variance component, the data simply do not localise the true effect to any clinically actionable region.

The p-value of 0.8366 should be interpreted as reflecting an absence of evidence against the null hypothesis of no difference, and emphatically not as evidence that the two arms are equivalent. A non-significant result derived from k = 3 with τ² = 0.735 carries very little power to exclude even a moderate increase in serious harm.

A cumulative meta-analysis, ordered to show the evolution of the pooled estimate as studies accrue, is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. It illustrates the dominance of the single large trial in stabilising the summary estimate and the sensitivity of the early pooled value to the small discordant trial.

---

## 6. Heterogeneity

Between-study heterogeneity was **moderate by the I² benchmark but not statistically significant by the Q test**:

- **Cochran's Q = 4.452** on 2 degrees of freedom, **p = 0.1079**
- **I² = 55.41%**, indicating that approximately 55% of the observed variability in effect estimates is attributable to genuine between-study differences rather than within-study sampling error
- **τ² = 0.734936**, the estimated variance of the true log-scale effects across studies

These three statistics tell a coherent but uncomfortable story. The Q test does not reach conventional significance, but with only two degrees of freedom Q is notoriously underpowered, so p = 0.1079 provides no reassurance of homogeneity. The I² value of 55.41% falls in the conventionally "moderate" band, and crucially I² is itself estimated with very wide uncertainty when k = 3 — its confidence interval in such a configuration typically extends from near zero to well above 80%. The most informative of the three is **τ² = 0.734936**, which on a log-ratio scale is large: it implies a standard deviation of true effects of roughly 0.86 log units, meaning plausible true risk ratios in individual future trials could easily range over an order of magnitude. This substantial τ² is the direct arithmetic cause of the very wide pooled confidence interval, since random-effects weighting inflates the variance of the summary estimate in proportion to it.

Because of this τ², a 95% prediction interval for the effect in a new trial would be so wide as to be uninformative and is not reported as a meaningful quantity here; with k = 3 the t-multiplier on one degree of freedom alone renders such an interval uninterpretable.

The identifiable source of the heterogeneity is clear from Section 4: the smallest trial (N = 91) produced an estimate in the opposite direction from, and non-overlapping with, the largest trial (N = 1,366). Clinically plausible explanations include differences in trial duration and hence cumulative exposure, differences in baseline kidney function and comorbidity (which drive background SAE rates independent of treatment), differences in dose and titration aggressiveness, and — perhaps most importantly — differences in how investigators operationalised "serious" in adverse event reporting. A composite that is dominated in one trial by hospitalisations for kidney-related events and in another by hepatic enzyme elevations is not measuring the same construct, even when both are labelled "any SAE".

Graphical summaries of the heterogeneity diagnostics are provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 7. Moderator Analyses

No moderator, subgroup or meta-regression analyses were performed. **With k = 3 contributing effect estimates, the data cannot support the estimation of any covariate effect.** A meta-regression with a single moderator would leave one residual degree of freedom; any resulting coefficient would be essentially unidentified, and conventional guidance (a minimum of roughly ten studies per covariate) is violated by a factor of more than three. Stratification by agent (tolvaptan versus lixivaptan versus satavaptan), by dose, by trial duration, by baseline CKD stage, or by comparator type (placebo versus standard therapy) would in each case reduce strata to one or two studies, producing within-stratum "pooled" values that are simply the individual study results relabelled.

A bubble chart exploring the relationship between study size and effect magnitude is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. It should be read descriptively only: it illustrates that the single discordant estimate is also the smallest trial, which is consistent both with a small-study effect and with ordinary sampling variability, and three points cannot distinguish between these possibilities.

Consequently, the observed I² of 55.41% and τ² of 0.734936 remain **unexplained** heterogeneity. This is an important limitation for clinical application: we cannot identify which patients, doses or exposure durations are associated with a higher or lower burden of serious adverse events.

---

## 8. Publication Bias and Small-Study Effects

Two complementary assessments were undertaken.

**Egger's regression test.** The regression intercept was **0.7114** with **p = 0.3324**. This provides no statistically significant evidence of funnel-plot asymmetry, falling well above both the conventional 0.05 threshold and the more liberal 0.10 threshold often recommended for small-study-effect testing. There is thus no detectable systematic relationship between effect size and study precision in this dataset.

**Trim-and-fill.** The Duval–Tweedie procedure imputed **zero missing studies (k₀ = 0)**, indicating that the observed funnel configuration was not judged asymmetric enough to require augmentation; the pooled estimate consequently required no adjustment for potentially suppressed results. The procedure's reported adjusted estimate on the standardised diagnostic scale was −0.1944, consistent with no material shift.

**Overall risk of publication bias: low.**

**Essential caveat.** Both procedures have very limited statistical power when fewer than approximately ten studies are available and when between-study heterogeneity is substantial — and this analysis violates both conditions simultaneously (k = 3, I² = 55.41%). With three data points, Egger's regression is fitted on one residual degree of freedom and could only detect extreme asymmetry. The appropriate reading is therefore **"no evidence of publication bias"**, not positive evidence that bias is absent. This caveat is especially pertinent for a safety outcome, where selective non-reporting of harm data — including incomplete SAE tabulation in trial publications and the cessation of development programmes for safety reasons — is a well-documented and directional phenomenon that funnel-based methods are poorly equipped to detect.

---

## 9. Discussion

This meta-analysis of three randomised comparisons encompassing 1,632 randomised participants found **no statistically detectable difference in the risk of experiencing one or more serious adverse events between V2R antagonist and placebo/standard-therapy arms in ADPKD** (pooled risk ratio 0.875, 95% CI 0.245 to 3.118, p = 0.8366, favouring neither arm).

The clinical message of this result lies almost entirely in its imprecision. An interval running from RR 0.245 to RR 3.118 cannot exclude a tripling of the probability of serious harm, nor can it exclude a substantial protective effect. For a drug class whose benefit is a slowing of structural and functional kidney disease progression over years, and whose principal clinical constraint is a mandated hepatic monitoring programme, a safety estimate of this width does not materially change the benefit–harm calculation in either direction. Prescribers and guideline developers should continue to rely on the specific, mechanistically coherent harm signals that motivated the current risk-management framework — transaminase elevation and hepatocellular injury, aquaresis-driven polyuria and nocturia, thirst, hypernatraemia and volume depletion — rather than on an aggregate SAE count that is statistically silent.

A second substantive point concerns the construct validity of the composite endpoint itself. "Any serious adverse event" aggregates events that differ profoundly in their attributability to treatment. In ADPKD trials, a substantial share of SAEs comprises hospitalisations for cyst haemorrhage, cyst infection, nephrolithiasis, flank pain and hypertensive complications — events driven by the underlying disease rather than by V2R blockade, and events that an agent slowing cyst growth might plausibly *reduce*. Those disease-related SAEs are pooled in the same numerator as drug-attributable hepatic events, which V2R antagonism plausibly *increases*. Opposing mechanistic effects on different components of a composite are a classic recipe for a null aggregate, and the point estimate of 0.875 sitting just below unity is entirely consistent with such a cancellation. A composite SAE count should therefore be regarded as a screening instrument for gross safety imbalance, not as an adequate characterisation of this class's harm profile.

Third, the heterogeneity deserves weight in interpretation. τ² = 0.734936 is not a nuisance parameter here; it is a substantive finding that the true SAE risk ratio plausibly differs across trial contexts by a large margin. Until the sources of that variation are identified — dose, duration, baseline eGFR, and above all SAE adjudication practice — a single pooled number is a poor summary of what is known.

Finally, the direction of the single discordant trial merits comment without over-reading. The smallest trial (N = 91) produced an estimate opposite in sign to the two larger trials and with a confidence interval excluding the null. Small trials with extreme, significant results are exactly the configuration most susceptible to chance, selective analysis and outcome-reporting effects, and its influence on τ² — and hence on the width of the pooled interval — is disproportionate to its information content.

---

## 10. Data Quality and Completeness Notes

No formal validation flags were returned by the analysis pipeline for this dataset. Nonetheless, several data-handling facts should be stated plainly rather than left implicit:

- **Four studies were included; only three contributed pooled effect estimates.** One eligible study did not provide an extractable, non-duplicative count of participants with ≥1 SAE against a randomised denominator and is therefore described narratively but excluded from the quantitative synthesis. Readers should not interpret "four included studies" as "four pooled trials".
- **Companion and secondary reports of the same randomised cohorts were not entered separately**, in order to avoid double-counting participants; where multiple publications described one trial population, the most complete arm-level safety report was used.
- **Reviews, editorials and non-randomised reports identified during screening were excluded** and do not contribute data.
- **The effect measure was specified a priori as the risk ratio and was pooled natively on that scale** (`native_pooling_used: true`). The per-study values in Table 1 are standardised diagnostic conversions used for plotting; they are not the basis of the pooled inference and the pooled result is not a Hedges' *g*.
- **Sample-size imbalance is extreme.** A single trial supplies 1,366 of 1,632 randomised participants (83.7%). The pooled estimate is, in practical terms, that trial's result widened by the between-study variance contributed by two much smaller trials.

---

## 11. Limitations

1. **Very small number of pooled studies (k = 3).** This is the dominant limitation. It renders τ² poorly estimated, I² highly uncertain, moderator analysis impossible, and publication-bias testing nearly powerless.
2. **Extremely wide confidence interval.** The pooled RR of 0.875 with a 95% CI of 0.245 to 3.118 cannot exclude clinically important harm or benefit; the analysis is not an equivalence demonstration.
3. **Unexplained moderate heterogeneity** (I² = 55.41%, τ² = 0.734936), with one trial directionally discordant and non-overlapping with the largest trial, and no capacity to investigate why.
4. **Composite outcome heterogeneity of definition.** "Serious adverse event" was taken as investigator-reported, and definitions, ascertainment intensity and adjudication practice almost certainly varied across trials; disease-related and drug-related events are aggregated in a single numerator.
5. **Dominance of one trial.** With 83.7% of participants from a single study, the synthesis has limited capacity to represent variation across the evidence base.
6. **No component-level analysis.** Hepatic, aquaretic, electrolyte and disease-related SAE components were not analysed separately, although these are the clinically decision-relevant quantities for this drug class.
7. **Agent-level inference not possible.** The review scope spans tolvaptan, lixivaptan and satavaptan, but with k = 3 the pooled estimate cannot be attributed to, or disaggregated by, any individual molecule, dose or titration strategy.
8. **Duration and exposure.** Trials differed in follow-up length; cumulative SAE probability is duration-dependent, and no exposure-adjusted (incidence-rate) analysis was feasible with arm-level participant counts alone.
9. **Publication and reporting bias cannot be excluded.** The low risk rating reflects the absence of detectable asymmetry in an underpowered test, not demonstrated absence of bias, and safety outcomes are particularly prone to selective reporting.
10. **Formal risk-of-bias and GRADE certainty assessments** were not quantitatively incorporated into the synthesis; on the basis of imprecision and unexplained inconsistency alone, the certainty of evidence for this outcome would be expected to be low.

---

## 12. Conclusion

Pooling three randomised comparisons in 1,632 participants with ADPKD, V2R antagonists were associated with a risk ratio of **0.875 (95% CI 0.245 to 3.118; p = 0.8366)** for experiencing one or more serious adverse events relative to placebo or standard therapy — a result that **favours neither arm**. Between-study heterogeneity was moderate and unexplained (I² = 55.41%, τ² = 0.734936; Q = 4.452, df = 2, p = 0.1079), and there was no detectable publication-bias asymmetry (Egger's p = 0.3324; trim-and-fill k₀ = 0), though both bias tests were severely underpowered.

The appropriate conclusion is one of **unresolved uncertainty rather than demonstrated safety**. The existing randomised evidence is too sparse, too heterogeneous and too imprecise to establish whether V2R antagonism raises, lowers or leaves unchanged the overall burden of serious harm in ADPKD. Composite SAE counts are, in any case, a blunt instrument for a class whose harms (hepatic injury, aquaresis) and potential benefits (reduced cyst-related complications) may act in opposite directions on the same aggregate endpoint. Future trials and syntheses should report and pool **component-specific serious adverse events** — hepatic, electrolyte/volume, and disease-related — with exposure-adjusted denominators, and should make full arm-level safety tables available so that the determinants of between-trial variation can be identified rather than merely quantified.

**Figures referenced.** Forest plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. Cumulative meta-analysis: `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. Distribution of effect estimates: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`. Bubble chart (descriptive): `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. Heterogeneity summary: `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Torres VE, Chapman AB, Devuyst O, et al. Tolvaptan in patients with autosomal dominant polycystic kidney disease. *N Engl J Med*. 2012;367(25):2407–2418.
3. Torres VE, Chapman AB, Devuyst O, et al. Tolvaptan in later-stage autosomal dominant polycystic kidney disease. *N Engl J Med*. 2017;377(20):1930–1942.
4. Higashihara E, Torres VE, Chapman AB, et al. Tolvaptan in autosomal dominant polycystic kidney disease: three years' experience. *Clin J Am Soc Nephrol*. 2011;6(10):2499–2507.
5. Gansevoort RT, Arici M, Benzing T, et al. Recommendations for the use of tolvaptan in autosomal dominant polycystic kidney disease: a position statement on behalf of the ERA-EDTA Working Groups on Inherited Kidney Disorders and European Renal Best Practice. *Nephrol Dial Transplant*. 2016;31(3):337–348.
6. Watkins PB, Lewis JH, Kaplowitz N, et al. Clinical pattern of tolvaptan-associated liver injury in subjects with autosomal dominant polycystic kidney disease: analysis of clinical trials database. *Drug Saf*. 2015;38(11):1103–1113.
7. Chebib FT, Perrone RD, Chapman AB, et al. A practical guide for treatment of rapidly progressive ADPKD with tolvaptan. *J Am Soc Nephrol*. 2018;29(10):2458–2470.
8. Bolignano D, Palmer SC, Ruospo M, Zoccali C, Craig JC, Strippoli GFM. Interventions for preventing the progression of autosomal dominant polycystic kidney disease. *Cochrane Database Syst Rev*. 2015;(7):CD010294.
9. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
10. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
11. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
12. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
13. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
14. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
15. Zarzuelo Romero MJ, et al. Lixivaptan safety and discontinuation in autosomal dominant polycystic kidney disease: a review of the clinical development programme. *Expert Opin Drug Saf*. 2023 (and associated programme communications).


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| serious adverse events | 3 | Risk Ratio (RR) | Yes | 0.8748 [0.2455, 3.1176] |
