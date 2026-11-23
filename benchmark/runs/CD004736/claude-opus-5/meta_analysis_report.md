# Antenatal Iron-Containing Supplementation and Maternal Iron-Deficiency Anaemia at Term: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Iron-deficiency anaemia is the single most common nutritional disorder of pregnancy and is associated with adverse maternal and perinatal outcomes. Although antenatal iron supplementation is recommended by the World Health Organization, the magnitude of its effect on *laboratory-confirmed* iron-deficiency anaemia at term — as distinct from anaemia defined by haemoglobin alone — is less frequently quantified.

**Objective.** To determine whether antenatal supplementation with any iron-containing supplement (iron alone, iron + folic acid, or multiple micronutrients with iron), compared with the same supplement without iron or with placebo/no treatment, reduces the risk of maternal iron-deficiency anaemia at term, defined as haemoglobin <110 g/L together with at least one additional laboratory indicator of iron deficiency, measured at ≥37 weeks' gestation.

**Methods.** A systematic search of randomised and quasi-randomised trials of antenatal iron-containing supplementation was undertaken and screened against the above population, intervention, comparator and outcome criteria. Trials reporting zero events in both arms were pre-specified as not estimable and were excluded from pooling. Effect sizes were pooled on the risk-ratio scale using a restricted maximum likelihood (REML) random-effects model. Heterogeneity was quantified with Cochran's Q, I² and τ². Small-study effects were assessed with Egger's regression test and the Duval–Tweedie trim-and-fill procedure.

**Results.** Six studies met the inclusion criteria; four contributed estimable effect sizes (k = 4; N = 2,209 participants). The pooled risk ratio was **0.289 (95% CI 0.126 to 0.661; p = 0.0033)**, corresponding to an approximately 71% lower relative risk of term iron-deficiency anaemia in the iron-supplemented arms. The automated direction field for this analysis returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)", reflecting the fact that the favourability of a ratio measure depends on which event was coded as the numerator; this ambiguity is reported transparently rather than resolved by inference. Heterogeneity was moderate and not statistically significant (Q = 6.237, df = 3, p = 0.1006; I² = 54.23%; τ² = 0.329123). Egger's regression indicated marked funnel-plot asymmetry (intercept = −0.0274, p < 0.001) and overall publication-bias risk was rated **high**; trim-and-fill imputed no missing studies (k₀ = 0), leaving the adjusted estimate unchanged.

**Conclusions.** Antenatal iron-containing supplementation was associated with a large and statistically significant reduction in the risk of laboratory-confirmed maternal iron-deficiency anaemia at term. However, the evidence base is small (k = 4), moderately heterogeneous, and shows strong statistical signals of small-study effects; the confidence interval is wide and the point estimate is likely to be an upper bound on the true benefit. The direction-of-benefit label returned by the analysis pipeline was indeterminate and the result should be read alongside the deterministic Effect Measure Summary table appended to this report.

**Registration.** Not registered; this report follows PRISMA 2020 reporting guidance.


## 1. Introduction

Anaemia in pregnancy affects an estimated one third to one half of pregnant women worldwide, with the highest burden in low- and middle-income settings. Iron deficiency is the dominant attributable cause, arising from the roughly 1,000 mg of additional iron required across gestation to support expansion of maternal red cell mass, placental and fetal growth, and to offset peripartum blood loss. Maternal iron-deficiency anaemia (IDA) has been linked to increased risks of preterm birth, low birth weight, impaired thermoregulation and immune function, peripartum transfusion, and — in severe cases — maternal mortality. On this basis the World Health Organization recommends daily oral elemental iron (30–60 mg) with folic acid (400 µg) throughout pregnancy in populations where anaemia prevalence is high, with intermittent regimens as an alternative where prevalence is low.

A substantial trial literature addresses antenatal iron supplementation, but much of it defines the primary outcome as *anaemia* on the basis of haemoglobin concentration alone. Haemoglobin is a late, non-specific marker: it is affected by plasma-volume expansion, inflammation, haemoglobinopathies, and deficiencies of folate and vitamin B12. Consequently, "anaemia" endpoints conflate true iron-deficient erythropoiesis with physiological haemodilution and with anaemias of non-iron aetiology. A more specific endpoint — haemoglobin below 110 g/L *together with* at least one corroborating laboratory indicator of depleted or functionally unavailable iron (low serum ferritin, low transferrin saturation, raised soluble transferrin receptor, or low mean cell volume) — isolates the pathology the intervention is designed to prevent, and is therefore the construct of greatest mechanistic and clinical interest.

This review addresses a single, narrowly specified question: in pregnant women, does antenatal supplementation with any iron-containing supplement (iron alone, iron plus folic acid, or multiple micronutrients containing iron), compared with the same supplement without iron or with placebo/no treatment, reduce the risk of maternal iron-deficiency anaemia at term (haemoglobin <110 g/L plus at least one additional laboratory indicator of iron deficiency, assessed at ≥37 weeks' gestation)?

A positive (beneficial) effect is defined a priori as a risk ratio below 1 — that is, fewer women with laboratory-confirmed IDA at term in the iron-containing arm.

---

## 2. Methods

### 2.1 Eligibility criteria

**Population.** Pregnant women of any age, parity, gestational age at enrolment, and baseline haematological status, in any setting.

**Intervention.** Any iron-containing antenatal supplement, administered orally or parenterally, given alone or in combination with folic acid or with a multiple-micronutrient preparation. Any dose, salt, formulation or dosing frequency (daily or intermittent) was eligible.

**Comparator.** The *same* supplement without the iron component (i.e. folic acid alone, or micronutrients without iron), placebo, or no treatment. This comparator structure isolates the contribution of iron itself rather than of co-administered micronutrients.

**Outcome.** The number or proportion of women with haemoglobin <110 g/L *and* at least one additional laboratory indicator of iron deficiency (low serum ferritin, low transferrin saturation, raised soluble transferrin receptor, low mean cell volume, or an equivalent indicator as defined by trialists), assessed at 37 completed weeks' gestation or later. Outcomes based on haemoglobin alone, or assessed earlier than 37 weeks, did not qualify for this analysis.

**Design.** Randomised and quasi-randomised controlled trials.

**Pre-specified estimability rule.** Trials reporting zero events in both arms were treated as *not estimable* for a ratio measure and were excluded from pooling, rather than being retained via a continuity correction. This rule was applied without exception.

### 2.2 Information sources and search

A systematic search of the trial literature on antenatal iron and micronutrient supplementation was executed and supplemented by reference-list screening of prior systematic reviews on the same intervention. Records were de-duplicated, then screened at title/abstract level and at full text against the criteria in §2.1. Non-trial document types (narrative and systematic reviews, commentaries, protocols) and duplicate reports of the same randomised cohort were removed so that each randomised population contributed only once to the pooled estimate.

### 2.3 Data extraction and effect-size computation

For each eligible trial, the number of women with term IDA and the number assessed were extracted by arm. Effect sizes were computed and are reported here in the form supplied by the analysis pipeline. The **pooled** analysis was performed natively on the risk-ratio scale (`measure_label` = "Risk Ratio (RR)"; `effect_measure_source` = explicit user request; `native_pooling_used` = **true**), meaning the pooled statistic reported in §5 is a confirmed native-scale risk ratio and *not* a standardized fallback. Per-study values in the effect-size listing (§4) are expressed on a standardized (g-type) scale used by the pipeline for display and diagnostic purposes; readers should not treat these per-study standardized values as the native risk ratios of the individual trials, and the two scales should not be compared numerically.

### 2.4 Synthesis methods

Pooling used a random-effects model with between-study variance estimated by restricted maximum likelihood (REML), which is appropriate when clinical and methodological diversity across trials (dose, formulation, baseline iron status, comparator type, assay thresholds) makes a common true effect implausible. Heterogeneity was characterised by Cochran's Q with its p-value, the I² statistic (proportion of observed variance attributable to between-study differences rather than sampling error), and τ² (the absolute between-study variance on the analysis scale). Small-study effects and potential publication bias were examined using Egger's regression of effect size on its standard error and the Duval–Tweedie trim-and-fill procedure. Figures generated for this synthesis are referenced by path in the relevant sections.

---

## 3. Search and Screening

The screening process identified **six studies** meeting the population, intervention, comparator, outcome and design criteria set out in §2.1. Of these, **four** supplied data that were estimable on the risk-ratio scale for the term IDA outcome and were carried forward into the quantitative synthesis (k = 4). The remaining two included studies did not contribute an estimable effect size — consistent with the pre-specified rule under which trials reporting zero events in both arms are treated as not estimable and excluded from pooling, and with the exclusion of records that could not supply arm-level event counts for the composite laboratory-confirmed endpoint at ≥37 weeks. These two studies are therefore described narratively as part of the included evidence base but contribute no weight to the pooled estimate.

Document-type filtering removed review articles and duplicate reports of the same randomised cohorts prior to synthesis, so that no randomised population is represented more than once in the pooled result.

The resulting evidence base for pooling comprises **2,209 randomised participants across four trials**.

---

## 4. Included Studies

Table 1 summarises the four trials contributing estimable effect sizes. Sample sizes span a 18-fold range, from 90 to 1,616 participants, and the analysis is dominated by a single large trial (study_4_R4) contributing 1,616 of the 2,209 participants (73.2% of the analysed sample).

**Table 1. Studies contributing estimable effect sizes to the pooled analysis (k = 4).**

| Study label | N analysed | Standardized effect size (g-scale, as supplied) | 95% CI | Share of total N |
|---|---|---|---|---|
| study_1_R1 | 90 | −1.682258 | [−2.188, −1.176] | 4.1% |
| study_3_R3 | 383 | −0.700440 | [−0.907, −0.494] | 17.3% |
| study_4_R4 | 1,616 | −0.393108 | [−0.492, −0.295] | 73.2% |
| study_5_R5 | 120 | −1.826879 | [−2.253, −1.401] | 5.4% |
| **Total** | **2,209** | — | — | 100% |

Two additional studies met the review's eligibility criteria but did not yield an estimable risk ratio for term IDA (see §3) and are excluded from all quantitative results below.

Across the contributing trials, the intervention was an iron-containing antenatal supplement and the comparator the same supplement without iron, placebo, or no treatment; the outcome in every contributing trial was the composite of haemoglobin <110 g/L plus at least one corroborating laboratory indicator of iron deficiency measured at ≥37 weeks' gestation. Detailed descriptors of dose, iron salt, dosing frequency, baseline anaemia prevalence, geographical setting and risk-of-bias domain judgements were not available in the structured data underlying this synthesis; their absence is recorded as a limitation (§11) and precluded the pre-specified subgroup analyses described in §7.

---

## 5. Effect Sizes

Every one of the four contributing trials produced an effect size in the same direction on the standardized display scale (all four standardized values negative, all four confidence intervals excluding zero; Table 1). There is thus **complete directional consistency** across the contributing evidence: no trial pointed towards harm or towards a null effect on the term IDA endpoint.

The magnitude of the standardized per-study values, however, varies markedly — from −0.393 in the largest trial to −1.827 in the smallest-but-one. This ordering is instructive: the two smallest trials (N = 90 and N = 120) produced the two largest effect magnitudes (−1.682 and −1.827), the mid-sized trial (N = 383) an intermediate magnitude (−0.700), and the largest trial (N = 1,616) the smallest magnitude (−0.393). This monotonic inverse relationship between sample size and effect magnitude is the classic signature of small-study effects, and it anticipates the funnel-asymmetry finding reported in §8.

The distribution of effect sizes is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between study size and effect magnitude is visualised in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

---

## 6. Meta-Analytic Result

A single outcome/timepoint group was analysed; the context data contained no `meta_analysis_groups` with multiple entries, so there is one pooled result to report and no separate per-group figures are required.

**Primary result.** Random-effects (REML) pooling of the four estimable trials yielded a **pooled Risk Ratio (RR) of 0.289 (95% CI 0.126 to 0.661), p = 0.0033**, based on k = 4 trials and N = 2,209 participants.

Key features of this estimate:

- **Effect measure.** The statistic is a **Risk Ratio (RR)**, pooled natively on the risk-ratio scale (`native_pooling_used` = true, `computation_scale` = RR). It is a confirmed native-scale result, not a standardized fallback. It must **not** be described as Hedges' *g*, notwithstanding the g-scale per-study values listed in Table 1.
- **Magnitude.** A risk ratio of 0.289 corresponds to a 71.1% relative reduction in the event counted; the 95% confidence interval spans relative reductions from 87.4% (RR = 0.126) to 33.9% (RR = 0.661). The interval excludes 1.0 across its whole range, and the association is statistically significant at conventional thresholds (p = 0.0033).
- **Direction.** The `favors` field returned for this analysis is **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**. In accordance with the reporting rules for this synthesis, the direction of benefit is reported using this field rather than inferred from the sign or position of the point estimate. Practically, this means the pipeline could not confirm which arm the ratio favours, because for a ratio measure the favourable direction depends on which event (IDA present vs. IDA absent) was coded as the numerator. Under the review's a priori convention — in which the counted event is *maternal iron-deficiency anaemia at term* and an RR below 1 denotes benefit — an RR of 0.289 would denote a reduction in term IDA with iron-containing supplementation; readers should treat this as the review's interpretive convention rather than as a pipeline-confirmed direction, and should consult the deterministic Effect Measure Summary table appended below, which takes precedence over narrative interpretation.
- **Precision.** The confidence interval is wide (a 5.2-fold ratio between its upper and lower bounds), reflecting both the small number of contributing trials and the substantial between-study variance (§7).

The forest plot, showing individual study estimates, weights and the pooled summary, is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. A cumulative meta-analysis, illustrating how the pooled estimate evolves as studies are added, is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`; inspection of this plot is particularly informative here, since the inverse size–effect gradient noted in §5 implies that the cumulative estimate attenuates as larger trials enter the synthesis.

---

## 7. Heterogeneity

Heterogeneity statistics for the single pooled group were:

| Statistic | Value | Interpretation |
|---|---|---|
| Cochran's Q | 6.237 (df = 3) | Observed dispersion modestly exceeds that expected from sampling error alone |
| Q p-value | 0.1006 | Not statistically significant at α = 0.05 |
| I² | 54.23% | Moderate: just over half the observed variance is attributable to real between-study differences rather than chance |
| τ² | 0.329123 | Substantial absolute between-study variance on the analysis scale |
| Model | REML random effects | Between-study variance explicitly estimated and incorporated |

These statistics should be read together rather than individually. The non-significant Q p-value (p = 0.1006) **does not** license an assumption of homogeneity: with only four studies, Cochran's Q has very low power, and a p-value above 0.05 in this setting is weak evidence of anything. The I² value of 54.23% falls in the conventional "moderate" band (30–60%) and, importantly, I² itself is estimated imprecisely when k is small — its own confidence interval would be extremely wide and would almost certainly extend from near zero to well above 75%.

The most informative quantity is τ² = 0.329123, which is not negligible. On the log-risk-ratio scale this implies a between-study standard deviation of approximately 0.574, i.e. substantial dispersion of true effects across trials. An approximate prediction interval derived from the reported τ² and the pooled estimate's standard error spans roughly RR 0.013 to RR 6.2 — an interval so wide that it includes both near-total prevention and apparent harm. This derived figure is approximate (it is reconstructed from the reported summary statistics rather than taken directly from the pipeline output, and the t-based multiplier on 2 degrees of freedom is extremely conservative), but it correctly conveys that the pooled point estimate should not be read as a reliable prediction of the effect in a new population.

Substantively, the observed heterogeneity is entirely plausible on clinical grounds. Trials of antenatal iron differ in iron dose and chemical form, dosing frequency (daily vs. intermittent), duration and gestational timing of supplementation, adherence, comparator (true placebo vs. no treatment vs. iron-free micronutrient supplement), background anaemia and infection prevalence, malaria and helminth burden, dietary iron bioavailability, and — critically for this endpoint — the specific laboratory indicator and cut-off used to corroborate iron deficiency. Any of these could shift the absolute and relative risk of the composite outcome. Importantly, the heterogeneity here concerns *magnitude*, not *direction*: all four contributing trials pointed the same way (§5).

A graphical summary of heterogeneity diagnostics is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 8. Moderator Analyses

No moderator or subgroup analyses were performed, and none can be legitimately performed on this dataset.

With k = 4 contributing trials, any meta-regression would have at most two residual degrees of freedom after fitting a single covariate, which is far below the widely cited minimum of roughly ten studies per covariate. Subgroup analyses that had been of interest a priori — iron dose (low vs. standard vs. high), route (oral vs. parenteral), regimen (daily vs. intermittent), supplement composition (iron alone vs. iron + folic acid vs. multiple micronutrients with iron), comparator type (placebo/no treatment vs. iron-free supplement), baseline population anaemia prevalence, and the specific corroborating iron indicator used — could not be undertaken because the necessary study-level descriptors were not available in the structured data supporting this synthesis.

The one pattern that is visible, and that functions as an informal moderator, is **study size**. As set out in §5, effect magnitude declines monotonically with increasing sample size across the four trials. This gradient is rendered visually in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. A formal meta-regression of effect size on its standard error is effectively what Egger's test performs, and its result is reported in §9. No subgroup or moderator value is reported here because none was estimated; any apparent explanation of the heterogeneity in §7 would be speculative.

---

## 9. Publication Bias and Small-Study Effects

Two complementary assessments were conducted, with discordant results that nonetheless point to the same overall conclusion.

**Egger's regression test.** The regression intercept was **−0.0274 with p < 0.001** (reported as p = 0.0 to the precision available). This indicates **strong funnel-plot asymmetry** — a statistically pronounced relationship between effect size and its precision, such that smaller, less precise studies report systematically larger effects than larger, more precise ones. This is directly corroborated by the descriptive pattern in Table 1, where the two smallest trials yield the two largest standardized effects and the largest trial the smallest.

**Trim-and-fill (Duval–Tweedie).** The algorithm imputed **k₀ = 0** missing studies, so the adjusted estimate is identical to the unadjusted one (reported adjusted value −1.121 on the pipeline's standardized display scale; note this adjusted figure is expressed on the g-type display scale rather than the native RR scale of the primary result, and the two are not directly comparable).

**Overall publication-bias risk: HIGH.**

The discordance between these two procedures should not be read as reassuring. Trim-and-fill has low statistical power, particularly when k is small, and it detects only a specific rank-based pattern of asymmetry — it is known to fail when asymmetry arises from genuine between-study heterogeneity, from a non-monotonic missingness pattern, or when there are too few studies for its trimming step to operate meaningfully. With four studies, k₀ = 0 is close to an uninformative result. The Egger finding, by contrast, is both statistically strong and descriptively corroborated by the raw size–effect gradient, and it is the finding that drives the high-risk rating.

Two important caveats cut in the opposite direction, however. First, Egger's test is itself unreliable with fewer than ten studies and is prone to false positives when effect sizes are large and sample sizes very unequal — both of which hold here. Second, asymmetry has causes other than selective publication: genuine small-study effects (e.g. small trials conducted in more severely iron-deficient populations with higher baseline event rates and therefore larger achievable relative reductions), differential methodological quality, or artefactual correlation between the log risk ratio and its standard error when event rates differ between arms.

The defensible conclusion is therefore that **the pooled risk ratio of 0.289 is likely to overstate the true average effect**, and that the true effect — while plausibly still beneficial, given the directional unanimity of all four trials — is probably closer to the attenuated estimate seen in the largest and most precise trial. Sensitivity analyses that would sharpen this inference (leave-one-out removal of the two smallest trials, meta-regression on standard error, limit meta-analysis, or a formal selection model) could not be executed on the available data and are recommended for any update of this review.

---

## 10. Discussion

### 10.1 Summary of findings

Across four randomised trials comprising 2,209 pregnant women, antenatal supplementation with an iron-containing preparation was associated with a pooled risk ratio of 0.289 (95% CI 0.126 to 0.661; p = 0.0033) for laboratory-confirmed maternal iron-deficiency anaemia at term. On the review's a priori convention — in which the counted event is term IDA and an RR below 1 indicates benefit — this represents a large relative reduction. The result was statistically significant, directionally consistent across every contributing trial, and derived from a native risk-ratio pooling rather than a standardized approximation. It is, however, accompanied by moderate between-study heterogeneity (I² = 54.23%, τ² = 0.329123), a wide confidence interval, and strong statistical evidence of small-study effects. The automated direction field returned an indeterminate label ("neither"), which is reported here as received rather than overridden.

### 10.2 Relation to existing evidence

The direction and approximate magnitude of this result are consistent with the broader literature on antenatal iron supplementation, which has repeatedly shown large relative reductions in maternal anaemia and iron deficiency at term and underpins current WHO recommendations for routine daily iron and folic acid in pregnancy. What this analysis adds is specificity of outcome: by requiring a corroborating laboratory indicator of iron deficiency alongside a haemoglobin below 110 g/L, it addresses the aetiologically relevant endpoint rather than the haemoglobin-defined composite that mixes iron-deficient erythropoiesis with haemodilution and non-iron anaemias. That a large effect persists under this stricter definition is biologically coherent: if iron supply is the limiting factor, supplementation should act most strongly on precisely the subgroup in which both haemoglobin and iron stores are depleted.

### 10.3 Interpretation and clinical implications

Three interpretive points deserve emphasis.

First, **the point estimate should be treated as an upper bound, not a best estimate.** The combination of high publication-bias risk, a pronounced inverse size–effect gradient, and the dominance of a single large trial with the smallest effect all suggest attenuation under any bias-adjusted analysis. Clinicians and guideline developers should weight the large-trial evidence more heavily than the unadjusted pooled figure.

Second, **the absolute benefit depends entirely on baseline risk**, which this analysis does not report. A relative reduction of ~70% translates into a very different number-needed-to-treat in a population with 40% baseline term IDA than in one with 4%. Because the structured data did not include baseline event rates or setting descriptors, no absolute risk difference or NNT is reported here. This is a material gap for clinical translation, and is the single most useful extension for any update.

Third, **this review addresses efficacy on a haematological endpoint only.** It says nothing about clinically harder outcomes (preterm birth, birth weight, transfusion, maternal mortality), nor about harms — gastrointestinal intolerance and poor adherence with oral iron, the specific risks of parenteral iron, and the debated question of iron supplementation in iron-replete women or in high-malaria-transmission settings. A favourable haematological result is a necessary but not sufficient basis for a supplementation policy.

---

## 11. Data Quality and Validation Notes

The following data-handling and quality issues materially affect how this report should be read, and are stated plainly:

1. **Six studies included, four pooled.** Of the six studies meeting eligibility criteria, only four contributed estimable effect sizes to the quantitative synthesis. Two contributed no weight. This is consistent with the pre-specified rule treating trials with zero events in both arms as not estimable for a ratio measure, and with the exclusion of records lacking extractable arm-level event counts for the composite ≥37-week endpoint. The pooled result therefore rests on two thirds of the included evidence base.
2. **Document-type and duplicate filtering.** Review articles and duplicate reports of the same randomised cohort were removed before synthesis so that no randomised population is counted twice. Readers comparing the study count in this report with raw search yields should expect a discrepancy for this reason.
3. **Two effect-size scales appear in this report.** Per-study values in Table 1 are on the pipeline's standardized (g-type) display scale; the pooled result in §6 is a native-scale Risk Ratio. The trim-and-fill adjusted value (−1.121) is likewise on the standardized display scale. These scales are not numerically comparable and should not be converted into one another by the reader. The pooled effect measure itself was explicitly specified as RR and native pooling was confirmed (`native_pooling_used` = true), so the primary result is a genuine risk ratio.
4. **Direction label indeterminate.** The pipeline's `favors` field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)". This review reports that label as received and interprets the estimate only under its explicitly stated a priori convention. The deterministic Effect Measure Summary table appended to this report is authoritative.
5. **Missing study-level descriptors.** Iron dose, route, formulation, regimen, comparator type, setting, baseline anaemia prevalence, the specific corroborating iron indicator and cut-off, and formal risk-of-bias domain judgements were not available in the structured data. Consequently, no risk-of-bias assessment, no GRADE certainty rating, no subgroup analysis and no absolute-risk calculation are reported. Their absence should be read as unavailability, not as a judgement that they were adequate.

No additional `validation_flags` were supplied with the context data for this synthesis.

---

## 12. Limitations

- **Very small number of trials (k = 4).** This is the binding constraint on the entire analysis. It renders Cochran's Q underpowered, I² imprecise, τ² unstable, Egger's test unreliable, trim-and-fill near-uninformative, and meta-regression impossible. Every inferential statistic in this report inherits this fragility.
- **High publication-bias risk.** Egger's test showed strong asymmetry (p < 0.001), corroborated by the raw inverse relationship between sample size and effect magnitude. The pooled estimate is therefore likely inflated by small-study effects.
- **Dominance of a single trial.** One trial contributes 73.2% of participants and reports the smallest effect; the pooled estimate's position between this trial and the much larger small-trial effects is sensitive to model choice and weighting.
- **Wide confidence and prediction intervals.** The 95% CI spans a 5.2-fold range of risk ratios, and the approximate prediction interval derived from τ² includes values compatible with both near-total prevention and apparent harm. The average effect is better established than the effect in any given new setting.
- **Unexplained moderate heterogeneity.** I² = 54.23% with τ² = 0.329123, with no moderator analysis possible to explain it.
- **Outcome-definition variability.** The composite endpoint permits *any* of several corroborating iron indicators at trialist-defined thresholds. Ferritin is an acute-phase reactant and performs differently in inflammatory settings than transferrin saturation, soluble transferrin receptor or mean cell volume. Pooling across indicator choices introduces construct heterogeneity that is invisible in the summary statistics.
- **No risk-of-bias or certainty assessment.** Domain-level risk-of-bias judgements and a GRADE rating could not be produced from the available data; blinding, allocation concealment and attrition — all of which plausibly affect a laboratory endpoint assessed at term — remain unassessed.
- **Excluded non-estimable trials.** Two eligible studies were excluded from pooling. Where exclusion was driven by zero events in both arms, this removes trials conducted in low-risk populations, which may bias the pooled relative effect upward relative to the full eligible evidence base.
- **No absolute effects, harms, or clinical endpoints.** No baseline risks, risk differences, numbers-needed-to-treat, adverse-event data, or downstream maternal/neonatal clinical outcomes are reported.
- **No prospective registration.** The review was not registered, so protocol-level pre-specification beyond the stated estimability rule cannot be independently verified.

---

## 13. Conclusion

In pregnant women, antenatal supplementation with an iron-containing supplement — iron alone, iron plus folic acid, or multiple micronutrients with iron — compared with the same supplement without iron or with placebo/no treatment, was associated with a **pooled Risk Ratio of 0.289 (95% CI 0.126 to 0.661; p = 0.0033; k = 4; N = 2,209)** for laboratory-confirmed maternal iron-deficiency anaemia at term. All four contributing trials pointed in the same direction, and under the review's a priori convention (term IDA as the counted event, RR < 1 = benefit) this corresponds to a substantial reduction in risk; the pipeline's own direction field, however, returned an indeterminate label and is reported as such.

This conclusion must be heavily qualified. The evidence base comprises only four estimable trials out of six included studies, shows moderate unexplained heterogeneity (I² = 54.23%, τ² = 0.329123; Q = 6.237, df = 3, p = 0.1006), and carries a **high** risk of publication bias driven by strong funnel asymmetry (Egger's p < 0.001) that trim-and-fill (k₀ = 0) is too underpowered to adjudicate. The true average benefit is most likely smaller than 0.289 and closer to the attenuated estimate observed in the largest and most precise trial.

The existing recommendation for routine antenatal iron supplementation in anaemia-prevalent populations is not contradicted by these data — indeed it is directionally supported on a stringently defined, laboratory-confirmed endpoint. But the *magnitude* reported here should not be quoted as a precise estimate of benefit. Priorities for future work are: (i) additional adequately powered trials reporting the composite haemoglobin-plus-iron-indicator endpoint at ≥37 weeks with standardised indicators and thresholds; (ii) reporting of baseline event rates so that absolute benefits and NNTs can be derived; (iii) individual-participant-data synthesis to permit dose, regimen, formulation and baseline-iron-status moderator analyses that k = 4 cannot support; and (iv) bias-adjusted sensitivity analyses (leave-one-out, SE meta-regression, selection models) to quantify how much of the observed effect survives correction for small-study effects.

---

## 14. Figures

| Figure | Path |
|---|---|
| Forest plot (study estimates, weights, pooled summary) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect size vs. study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity diagnostics summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 15. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Peña-Rosas JP, De-Regil LM, Garcia-Casal MN, Dowswell T. Daily oral iron supplementation during pregnancy. *Cochrane Database of Systematic Reviews.* 2015;(7):CD004736.
4. Peña-Rosas JP, De-Regil LM, Gomez Malave H, Flores-Urrutia MC, Dowswell T. Intermittent oral iron supplementation during pregnancy. *Cochrane Database of Systematic Reviews.* 2015;(10):CD009997.
5. World Health Organization. *WHO Recommendations on Antenatal Care for a Positive Pregnancy Experience.* Geneva: WHO; 2016.
6. World Health Organization. *Guideline: Daily Iron and Folic Acid Supplementation in Pregnant Women.* Geneva: WHO; 2012.
7. World Health Organization. *Haemoglobin Concentrations for the Diagnosis of Anaemia and Assessment of Severity.* Geneva: WHO; 2011 (WHO/NMH/NHD/MNM/11.1).
8. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software.* 2010;36(3):1–48.
9. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics.* 2005;30(3):261–293.
10. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
11. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
12. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
13. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ.* 2011;343:d4002.
14. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
15. Pavord S, Daru J, Prasannan N, Robinson S, Stanworth S, Girling J; BSH Committee. UK guidelines on the management of iron deficiency in pregnancy. *British Journal of Haematology.* 2020;188(6):819–830.
16. Daru J, Allotey J, Peña-Rosas JP, Khan KS. Serum ferritin thresholds for the diagnosis of iron deficiency in pregnancy: a systematic review. *Transfusion Medicine.* 2017;27(3):167–174.
17. Keats EC, Haider BA, Tam E, Bhutta ZA. Multiple-micronutrient supplementation for women during pregnancy. *Cochrane Database of Systematic Reviews.* 2019;(3):CD004905.
18. Deeks JJ, Higgins JPT, Altman DG. Analysing data and undertaking meta-analyses. In: *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| maternal iron-deficiency anaemia at term | 4 | Risk Ratio (RR) | Yes | 0.2886 [0.1260, 0.6610] |
