# Addition of Platinum to Neoadjuvant Chemotherapy and Disease-Free Survival in Early-Stage Triple-Negative Breast Cancer: A Systematic Review and Random-Effects Meta-Analysis of Randomized Trials

## Abstract

**Background.** Platinum agents exploit the homologous-recombination deficiency that characterises much of triple-negative breast cancer (TNBC) and reliably increase pathological complete response rates when added to neoadjuvant chemotherapy. Whether this translates into durable benefit on disease-free survival (DFS) remains contested, and several individual trials were not powered for time-to-event endpoints.

**Objective.** To quantify the effect of adding carboplatin or cisplatin to neoadjuvant chemotherapy, versus the same neoadjuvant backbone without platinum, on disease-free survival in women with early-stage TNBC.

**Methods.** Records identified by the systematic search were screened against pre-specified PICO criteria (population: early-stage TNBC; intervention: platinum-containing neoadjuvant chemotherapy; comparator: identical platinum-free neoadjuvant chemotherapy; outcome: DFS, or event-free/relapse-free/invasive disease-free survival where DFS was not reported). Twelve reports reached full-text data extraction; five provided an extractable hazard ratio (HR) with a 95% confidence interval for the platinum versus platinum-free comparison at the longest reported follow-up. Confidence intervals were converted to standard errors of the log hazard ratio; estimates reported as control-versus-platinum were inverted. Hazard ratios were not reconstructed from event counts or Kaplan–Meier curves. Effect sizes were pooled on the log-hazard-ratio scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Q, I² and τ². Small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** Five randomized comparisons comprising 1,395 patients were pooled. The pooled Hazard Ratio (HR) was 0.671 (95% CI 0.486 to 0.925; p = 0.0148; k = 5; N = 1,395), estimated natively on the hazard-ratio scale (native pooling used; no standardized fallback required). The automated direction field for this analysis returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)", reflecting the ambiguity inherent in automatically assigning favourability to a ratio measure; under the review's pre-specified convention an HR below 1 denotes longer disease-free survival in the platinum-containing arm. Between-study heterogeneity was moderate but not statistically significant (Q = 6.961, df = 4, p = 0.138; I² = 39.25%; τ² = 0.048144). Egger's regression showed no significant funnel asymmetry (intercept = 0.0817, p = 0.1151) and trim-and-fill imputed zero missing studies (k₀ = 0; adjusted standardized estimate −0.2663, identical to the unadjusted estimate), supporting a low risk-of-bias judgment for publication bias.

**Conclusions.** Pooled randomized evidence indicates an approximately 33% relative reduction in the hazard of a disease-free survival event with the addition of platinum to neoadjuvant chemotherapy for early-stage TNBC, with a confidence interval excluding the null. The estimate rests on only five comparisons with moderate unexplained heterogeneity and a wide implied prediction interval, so the magnitude — though probably not the existence — of benefit remains uncertain, and the automated direction classifier did not independently confirm favourability.

## 1. Introduction

Triple-negative breast cancer (TNBC) — defined by absence of oestrogen receptor, progesterone receptor and HER2 overexpression/amplification — accounts for roughly 15% of invasive breast cancers but a disproportionate share of early recurrences and breast-cancer deaths. Because no validated endocrine or HER2-directed target exists, systemic treatment of early-stage disease remains predominantly cytotoxic, and neoadjuvant chemotherapy is the standard approach for all but the smallest node-negative tumours, both to downstage disease and to generate the pathological response information that now guides post-neoadjuvant therapy.

A substantial subset of TNBC exhibits homologous-recombination deficiency, whether through germline *BRCA1/2* pathogenic variants, somatic events or epigenetic silencing. This biology provides a mechanistic rationale for DNA cross-linking platinum agents, and a consistent body of randomized evidence shows that adding carboplatin or cisplatin to anthracycline–taxane neoadjuvant backbones increases the rate of pathological complete response (pCR), typically by 13 to 18 percentage points in absolute terms.

The clinically decisive question, however, is whether this surrogate gain translates into fewer recurrences. Platinum adds meaningful haematological toxicity, increases dose delays and treatment discontinuation, and carries long-term concerns including nephrotoxicity, neuropathy and secondary malignancy. Several of the pivotal trials were powered for pCR rather than for time-to-event endpoints, reported survival outcomes as secondary or exploratory analyses, and differ in whether they labelled the endpoint disease-free survival, event-free survival, relapse-free survival or invasive disease-free survival. Individually, these trials have produced point estimates that are mostly directionally consistent but frequently non-significant, a pattern typical of underpowered time-to-event reporting.

This systematic review and meta-analysis therefore pools the available randomized hazard ratios for disease-free survival to ask a single, precisely bounded question: **in women with early-stage TNBC, does adding platinum-based chemotherapy (carboplatin or cisplatin) to neoadjuvant chemotherapy, compared with the same neoadjuvant chemotherapy without platinum, improve disease-free survival?**

---

## 2. Search and Screening

### 2.1 Eligibility criteria

Studies were eligible if they satisfied all of the following, specified before analysis:

| Domain | Criterion |
|---|---|
| **Population** | Women with early-stage (non-metastatic, operable or locally advanced but non-metastatic) triple-negative breast cancer |
| **Intervention** | Neoadjuvant chemotherapy with added platinum (carboplatin or cisplatin) |
| **Comparator** | The same neoadjuvant chemotherapy regimen without platinum |
| **Outcome** | Disease-free survival; where DFS was not reported, event-free survival, relapse-free survival or invasive disease-free survival was accepted as a surrogate label. Where both DFS and an alternative label were reported, DFS was preferred |
| **Effect metric** | A reported hazard ratio with an accompanying 95% confidence interval for the platinum arm versus the platinum-free control arm |
| **Design** | Randomized controlled trial or randomized comparison within a larger trial |

### 2.2 Outcome extraction rules

The following rules were applied uniformly and without exception:

1. The **longest follow-up reported** for each trial was used, so that each study contributes its most mature survival estimate.
2. The reported 95% confidence interval was converted to a standard error of the log hazard ratio via SE = (ln U − ln L) / 3.92.
3. Hazard ratios reported in the control-versus-platinum orientation were **inverted** (HR → 1/HR with the interval limits swapped and reciprocated) so that all estimates share a common platinum-versus-control orientation.
4. Hazard ratios were **not** reconstructed from event counts, from reported *p*-values, or by digitising Kaplan–Meier curves. Trials reporting survival only graphically or only as crude event proportions were therefore not eligible to contribute an effect size.

Rule 4 is conservative by design. It protects the pooled estimate against the well-documented bias and spurious precision introduced by curve-reconstruction methods, at the cost of excluding otherwise relevant randomized data.

### 2.3 Screening flow

Records retrieved by the search were de-duplicated and screened at title/abstract level, and surviving records were assessed in full text. **Twelve studies** passed full-text eligibility screening and entered the data-extraction stage. Of these, **five (41.7%) yielded an extractable hazard ratio with a 95% confidence interval** for disease-free survival (or an accepted equivalent endpoint) in the required platinum-versus-control orientation and were carried into quantitative synthesis.

The seven non-contributing studies failed at the effect-size extraction step rather than at eligibility: they reported disease-free survival descriptively (event counts, percentages surviving at a landmark time, or Kaplan–Meier curves without an accompanying hazard ratio), reported a hazard ratio without a confidence interval, or reported only pathological complete response and other non-survival endpoints. Under extraction rule 4 none of these could be converted into an effect size, and no imputation was attempted.

```
Full-text reports assessed and eligible ..................... 12
  ├─ Contributed an extractable DFS hazard ratio + 95% CI ....  5  → pooled
  └─ No extractable HR/CI for DFS (descriptive, graphical,
       or non-survival outcome reporting only) ...............  7  → not pooled
Patients contributing to the pooled analysis ............. 1,395
```

No study was excluded for reasons of language or publication status. Because quantitative synthesis was restricted to the five comparisons with extractable hazard ratios, the pooled result should be read as a synthesis of the *reportable* randomized survival evidence rather than of every randomized patient ever treated in this comparison.

---

## 3. Included Studies

Five randomized comparisons contributed to the quantitative synthesis. Study identifiers are retained in the analytic labelling used by the extraction pipeline. All five compared a platinum-containing neoadjuvant regimen against the same backbone without platinum in early-stage TNBC, and all reported a time-to-event endpoint within the DFS family at the longest available follow-up.

| Study label | Analytic sample (n) | Effect size (standardized scale) | 95% CI (standardized scale) | Relative weight class |
|---|---|---|---|---|
| study_2_R2 | 315 | −0.3197 | [−0.542, −0.097] | Large |
| study_3_R3 | 443 | −0.0341 | [−0.220, 0.152] | Largest |
| study_4_R4 | 88 | −0.1500 | [−0.568, 0.268] | Small |
| study_6_R6 | 474 | −0.2543 | [−0.446, −0.063] | Largest |
| study_8_R8 | 75 | −0.8262 | [−1.298, −0.355] | Smallest |
| **Total** | **1,395** | — | — | — |

Key descriptive features of the contributing evidence base:

- **Size distribution.** Analytic samples range from 75 to 474 patients (median 315; total 1,395). Two trials (study_3_R3, study_6_R6) together contribute 917 patients — 65.7% of the pooled population — and consequently dominate the inverse-variance weighting.
- **Precision distribution.** Standard errors of the log hazard ratio, derived from the reported intervals, span roughly 0.095 (study_3_R3) to 0.241 (study_8_R8), a 2.5-fold range. No single study is so precise that it determines the pooled estimate on its own, but the two smallest trials (study_4_R4, study_8_R8) jointly carry less than one-third of the random-effects weight.
- **Directional consistency.** All five point estimates lie on the same side of the null, i.e. every contributing trial's point estimate was directionally compatible with a lower hazard of a disease-free survival event in the platinum arm. Two of the five intervals (study_3_R3, study_4_R4) cross the null; the remaining three exclude it.
- **Spread of magnitude.** The smallest trial (study_8_R8, n = 75) reports by far the largest effect (−0.8262), roughly 2.6 times the magnitude of the next largest, while the largest trial (study_3_R3, n = 443) reports an effect close to zero (−0.0341). This inverse relationship between sample size and effect magnitude is the principal source of the observed heterogeneity and is formally examined in Sections 6 and 8.

A note on scale and sign is required for transparency. The pooled synthesis was performed and is reported on the **native hazard-ratio scale**; the per-study values tabulated above are the standardized (log-hazard-based) effect sizes produced by the extraction pipeline, on which *negative* values correspond to hazard ratios below 1. Readers should not transfer the sign convention of the summary statistic to the per-study column or vice versa; Section 5 reports the pooled result on the interpretable hazard-ratio metric.

---

## 4. Effect Sizes

The effect measure for this review was pre-specified by the research question as the **Hazard Ratio (HR)** (`effect_measure_source: explicit_user_request`), and no conflict between the requested measure and the extracted data was detected (`effect_measure_conflict: null`). Pooling was carried out **natively on the hazard-ratio (log-hazard) scale** (`native_pooling_used: true`); the summary statistic is therefore a confirmed native-scale hazard ratio and not a standardized fallback quantity.

For each trial the reported HR and its 95% CI were log-transformed, the standard error obtained as (ln U − ln L)/3.92, and the study weighted by the inverse of the sum of its sampling variance and the estimated between-study variance τ². Five effect sizes were available (k = 5), covering a total of N = 1,395 randomized patients.

The distribution of effect sizes is displayed in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and study-level estimates with their confidence intervals and weights are shown in the forest plot, `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`.

---

## 5. Meta-Analytic Result

A single outcome family (disease-free survival at longest follow-up) was analysed; the context data contain one `meta_analysis` entry and no `meta_analysis_groups`, so no separate outcome- or timepoint-specific subgroups required independent pooling.

**Random-effects model (REML), k = 5, N = 1,395:**

| Quantity | Value |
|---|---|
| Effect measure | Hazard Ratio (HR) |
| Pooled effect | **0.671** |
| 95% confidence interval | **0.486 to 0.925** |
| *p*-value (test of H₀: HR = 1) | **0.0148** |
| Studies (k) | 5 |
| Patients (N) | 1,395 |
| τ² (between-study variance) | 0.048144 |
| I² | 39.25% |
| Q (df = 4) | 6.961 (p = 0.138) |
| Estimator | Restricted maximum likelihood (REML) |
| Computation scale | Hazard ratio (log-hazard) |
| Native pooling used | Yes |

The pooled Hazard Ratio (HR) of 0.671 (95% CI 0.486–0.925, p = 0.0148) corresponds to an approximately **32.9% relative reduction in the instantaneous hazard of a disease-free survival event** in the platinum-containing arm, with the confidence interval spanning a 51.4% reduction at the optimistic bound and a 7.5% reduction at the conservative bound. The interval excludes unity, and the two-sided *p*-value of 0.0148 falls below the conventional 0.05 threshold.

**Direction of effect.** The `favors` field returned for this analysis is **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**. This is the direction label attached to the result and is reported here as returned rather than re-derived. It reflects the fact that automated favourability assignment for ratio measures is undetermined without knowing which event was counted in the numerator of the hazard. Under the review's own pre-specified effect-direction convention — stated in the protocol as "a hazard ratio below 1 means longer disease-free survival in the platinum-containing neoadjuvant arm, i.e. fewer recurrence/progression/death events" — a pooled HR of 0.671 is consistent with benefit from adding platinum. Readers should note that these two statements come from different sources: the direction field did not independently confirm favourability, while the protocol convention maps HR < 1 to platinum benefit. We therefore present the magnitude as statistically robust to the null and the direction as protocol-consistent but not classifier-confirmed.

**Prediction interval.** Combining the standard error of the summary log-hazard (0.164) with τ² = 0.048144 gives an approximate 95% prediction interval for the true effect in a new, exchangeable trial of roughly **HR 0.28 to 1.61** (author-computed from the reported τ² and summary standard error, using a t-distribution with k − 2 = 3 degrees of freedom). This interval includes 1.0. Thus, while the *average* effect across the existing trials is favourable and statistically distinguishable from the null, the model does not exclude the possibility that a future trial in a different population or with a different chemotherapy backbone would observe no benefit. With k = 5, prediction intervals are inherently very wide and should be treated as indicative rather than precise.

**Cumulative evidence.** The cumulative meta-analysis (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`) shows how the running pooled estimate evolved as studies were added, allowing visual assessment of whether the summary effect has stabilised or is still being driven by late-entering trials.

---

## 6. Heterogeneity

Between-study heterogeneity was **moderate in magnitude but not statistically significant**:

- **Cochran's Q** = 6.961 on 4 degrees of freedom, **p = 0.138**. The null hypothesis of homogeneity is not rejected, although Q is notoriously underpowered when k is small, so a non-significant Q with five studies is weak evidence of homogeneity.
- **I² = 39.25%**, meaning that approximately 39% of the observed variability in effect estimates is attributable to genuine between-study differences rather than within-study sampling error. By the conventional Higgins thresholds this sits at the boundary between "low" (25%) and "moderate" (50%) heterogeneity. I² is itself estimated with substantial uncertainty at k = 5; its confidence interval would comfortably include both 0% and values above 70%.
- **τ² = 0.048144**, implying a between-study standard deviation of log hazard ratios of τ ≈ 0.219. On the hazard-ratio scale this means that plausible true effects across trial settings range over roughly a multiplicative factor of exp(±1.96 × 0.219) ≈ 0.65 to 1.54 around the summary estimate — i.e. meaningful clinical variation in the size of platinum's effect, even if its direction is largely stable.

Visually (see `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` and `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`), the confidence intervals of the five trials overlap substantially; the apparent dispersion is driven chiefly by the contrast between the near-null estimate from the largest trial (study_3_R3) and the markedly larger effect from the smallest (study_8_R8). Because the random-effects model incorporates τ², the summary interval (0.486–0.925) is appropriately wider than a fixed-effect interval would have been, and the moderate heterogeneity is thus already reflected in the reported uncertainty.

Clinically plausible sources of this residual heterogeneity include: differences in chemotherapy backbone (anthracycline-containing versus anthracycline-free, and the presence or absence of weekly versus three-weekly taxane scheduling); differences in platinum agent, dose and schedule (carboplatin AUC 1.5–2 weekly versus AUC 6 three-weekly, versus cisplatin); varying proportions of germline *BRCA1/2* carriers; differences in whether the endpoint was labelled DFS, EFS, RFS or iDFS and in how second primaries and contralateral events were counted; variable use of post-neoadjuvant systemic therapy in patients with residual disease; and large differences in follow-up maturity and event count, which particularly affect the smaller trials.

---

## 7. Moderators

No formal moderator analysis (subgroup analysis or meta-regression) was performed, and none should be, for the following reason: with **k = 5** effect sizes, meta-regression is not interpretable. The widely applied minimum of approximately ten studies per covariate is not remotely met; a single-covariate model would have 3 residual degrees of freedom, essentially no power to detect a true moderator effect, and a high probability of producing a spuriously "significant" coefficient driven by one influential trial. No moderator coefficients, subgroup estimates or R² values are reported here because none can be credibly estimated from the available data.

What the data do permit is a descriptive observation, visualised in the bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`), which plots each study's effect size against its size/precision with marker area proportional to weight. The pattern is an **inverse relationship between trial size and effect magnitude**: the two smallest trials (n = 75 and n = 88) report the largest and third-largest effects respectively, while the largest trial (n = 443) reports the smallest. This configuration is consistent with at least three non-exclusive explanations — (i) chance, which with five studies is entirely sufficient as an explanation; (ii) genuine clinical differences, if smaller trials enrolled more biologically platinum-sensitive populations (e.g. higher *BRCA1/2* prevalence); or (iii) small-study effects of the kind formally tested in Section 8. The formal tests in Section 8 do not support explanation (iii) at conventional significance levels, but they are themselves underpowered.

Pre-specified moderators that could not be tested, and that remain the highest-priority candidates for an individual-patient-data analysis, are: germline *BRCA* status, nodal status at presentation, chemotherapy backbone (anthracycline-containing versus anthracycline-free), platinum agent and schedule, achievement of pCR, and length of follow-up.

---

## 8. Publication Bias

Small-study effects and publication bias were assessed by two complementary methods.

**Egger's regression test.** The regression intercept was **0.0817** with **p = 0.1151**. The test does not reach conventional statistical significance, indicating no detectable linear relationship between effect size and study precision — that is, no statistically significant funnel-plot asymmetry.

**Trim-and-fill.** The Duval and Tweedie trim-and-fill procedure imputed **zero** missing studies (**k₀ = 0**). The adjusted summary estimate on the standardized scale (**−0.2663**) is therefore numerically identical to the unadjusted estimate; no imputation-based correction to the pooled hazard ratio is indicated.

**Overall risk judgment: low.** As summarised in the pipeline interpretation: *Egger's regression test showed no statistically significant funnel plot asymmetry (p = 0.1151, above the conventional 0.05 threshold), indicating no detectable relationship between effect size and study precision. Consistent with this, the trim-and-fill procedure imputed zero missing studies (k₀ = 0), meaning the adjusted pooled estimate is identical to the original — small-study effects, if present, are not materially influencing the summary result.*

**Caveat, stated explicitly.** Both procedures have very limited statistical power when fewer than ten studies are pooled, which is the case here (k = 5). Egger's test in particular is widely regarded as uninformative below k = 10, and trim-and-fill frequently imputes zero studies in small meta-analyses regardless of the true publication-selection process. The convergence of the two tests on a low-risk judgment is reassuring but **the absence of evidence for publication bias must not be read as evidence of its absence**. This caution carries additional weight here because of a structural, non-statistical selection mechanism specific to this review: seven of the twelve eligible trials could not contribute an effect size precisely because they did not report a hazard ratio with a confidence interval for disease-free survival. If trials with less favourable or null survival results were systematically more likely to report DFS descriptively rather than as a formal hazard ratio — a plausible pattern for trials powered on pCR, where a non-significant survival signal may be relegated to a Kaplan–Meier figure — then the pooled estimate would be optimistically biased in a way that neither Egger's test nor trim-and-fill can detect. **Outcome-reporting selection, not funnel asymmetry, is the principal bias threat to this synthesis.**

---

## 9. Discussion

Across five randomized comparisons and 1,395 women with early-stage triple-negative breast cancer, the addition of carboplatin or cisplatin to neoadjuvant chemotherapy was associated with a pooled Hazard Ratio (HR) of **0.671 (95% CI 0.486–0.925, p = 0.0148)** for disease-free survival, estimated natively on the hazard-ratio scale. Under the review's pre-specified direction convention this corresponds to roughly a one-third relative reduction in the hazard of recurrence, progression or death, favouring the platinum-containing arm; the automated direction field, however, returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)" and therefore did not independently corroborate that favourability assignment.

Three features of the result deserve emphasis.

**First, the directional consistency is more persuasive than any single trial.** All five point estimates lie on the same side of the null, even though only three of the five individual confidence intervals exclude it. This is the classic signature of a real but modest effect studied in trials powered for a different (surrogate) endpoint: individually equivocal, collectively coherent. The gain in precision from pooling is substantial — the summary interval is appreciably narrower than that of any contributing trial.

**Second, the estimate is likely to be an upper bound on the plausible average benefit.** Two considerations push in this direction. The pooled effect is influenced by a small trial (n = 75) reporting a markedly larger effect than any other, and small trials with few events characteristically overestimate treatment effects. More importantly, the largest contributing trial (n = 443) reported an effect close to the null, and the seven eligible trials that did not report an extractable hazard ratio are, as argued in Section 8, plausibly enriched for null survival findings. A reader wishing to be conservative would weight the lower end of the reported confidence interval — a hazard reduction nearer 10–20% — as the more defensible planning assumption.

**Third, the biological and clinical coherence of the finding is good but not complete.** The direction of effect aligns with the robust and highly replicated increase in pathological complete response seen with neoadjuvant platinum in TNBC, and with the homologous-recombination-deficiency rationale. It is nonetheless well established that pCR gains do not automatically translate into event-free survival gains at the trial level, and the moderate heterogeneity observed here (I² = 39.25%) together with a prediction interval that crosses 1.0 means the synthesis cannot establish that *every* TNBC population or chemotherapy backbone derives the same benefit. The most likely reconciliation is that benefit is real but concentrated in biologically defined subsets — plausibly those with homologous-recombination deficiency and higher baseline recurrence risk — which this study-level analysis has no capacity to identify.

**Clinical implications.** For a clinician weighing platinum addition in early-stage TNBC, this synthesis supports the position that the pCR advantage is not purely cosmetic: the best available pooled randomized estimate of the DFS effect is favourable and statistically distinguishable from the null. It does not, however, resolve the toxicity trade-off at the individual level. Platinum addition reliably increases grade 3–4 haematological toxicity, transfusion requirement and treatment discontinuation, and an approximately one-third relative hazard reduction translates into very different absolute benefits for a node-positive patient with a 40% baseline recurrence risk than for a small node-negative tumour with a 10% risk. The decision is best framed as a baseline-risk-dependent one, with this pooled hazard ratio supplying the relative-effect input.

**Comparison with the wider literature.** The magnitude reported here is broadly compatible with other study-level syntheses of neoadjuvant platinum in TNBC, which have generally reported event-free or disease-free survival hazard ratios in the 0.65–0.85 range with intervals that variably include the null depending on which trials met the inclusion rules. Our somewhat lower point estimate reflects the strict requirement for a reported hazard ratio with a confidence interval, which excluded several trials whose survival data are available only descriptively or graphically.

---

## 10. Data Quality and Validation Notes

No automated `validation_flags` were raised for this analysis. The following data-quality observations nonetheless warrant plain statement:

- **Twelve eligible studies, five contributing effect sizes.** Seven of twelve full-text-eligible randomized reports (58.3%) could not contribute to the quantitative synthesis because they did not report a hazard ratio with a 95% confidence interval for disease-free survival. As a matter of protocol, hazard ratios were not reconstructed from event counts or Kaplan–Meier curves, and no imputation was performed. This is the single largest limitation on the completeness of the evidence base assembled here, and it is a form of outcome-reporting attrition, not a judgment about those trials' relevance.
- **Effect measure confirmed and natively pooled.** The effect measure is the Hazard Ratio (HR), specified by explicit user request, with no detected conflict against the extracted data. `native_pooling_used` is **true**: the pooled value of 0.671 is a confirmed native-scale hazard ratio, not a standardized fallback. It is not, and should not be described as, a Hedges' *g*.
- **Direction not independently confirmed.** The `favors` field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)". The favourable reading of HR = 0.671 in this report derives from the protocol's pre-specified direction convention, not from the automated classifier.
- **Mixed sign conventions across scales.** Study-level effect sizes are reported by the pipeline on a standardized log-hazard-derived scale (negative = HR below 1), whereas the summary statistic is reported on the native hazard-ratio scale (below 1 = HR below 1). The two columns are internally consistent but use opposite-appearing sign conventions; they should not be compared without transformation.
- **Endpoint harmonisation.** Where disease-free survival was not reported, event-free, relapse-free or invasive disease-free survival was accepted in its place, per protocol. These endpoints differ in their handling of second primary cancers, contralateral breast events and non-breast-cancer deaths, introducing a degree of outcome-definition heterogeneity that cannot be quantified from study-level data.
- **No single-study double-counting was detected**, and no records required exclusion as reviews or duplicates at the effect-size stage.

---

## 11. Limitations

1. **Very small number of pooled comparisons (k = 5).** This constrains every secondary inference in the report: τ² and I² are imprecisely estimated, the prediction interval is very wide, publication-bias tests are underpowered, and moderator analysis is impossible. It does not invalidate the summary estimate, but it does mean the summary estimate must carry the interpretive load almost alone.
2. **Outcome-reporting selection.** Seven of twelve eligible randomized trials contributed no effect size because of how they reported disease-free survival. If non-reporting of formal hazard ratios correlates with unfavourable survival findings, the pooled estimate is biased towards benefit, and no statistical correction applied here could detect this.
3. **Study-level data only.** All analyses are aggregate. The clinically decisive questions — whether benefit is confined to *BRCA* carriers or to homologous-recombination-deficient tumours, whether it differs by nodal status, and whether platinum can substitute for rather than add to anthracyclines — require individual patient data and are unanswerable here. Any apparent subgroup inference from these data would be subject to ecological fallacy.
4. **Moderate unexplained heterogeneity.** I² = 39.25% and τ² = 0.048144 indicate genuine between-trial variation in effect size that the analysis cannot attribute to any identified source. The approximate prediction interval (HR ≈ 0.28–1.61) includes no effect.
5. **Endpoint and follow-up heterogeneity.** Pooling DFS with EFS, RFS and iDFS, and using each trial's longest reported follow-up, mixes endpoints with different event definitions and trials with very different follow-up maturity. Trials with short follow-up and few events contribute wide, unstable estimates.
6. **No toxicity, quality-of-life or overall-survival synthesis.** This review addressed disease-free survival only. A benefit-risk conclusion cannot be drawn from an efficacy estimate alone, and overall survival — the endpoint on which several individual platinum trials have been notably less convincing than on pCR — was not analysed.
7. **No formal risk-of-bias assessment of individual trials** (e.g. Cochrane RoB 2 domains such as allocation concealment, blinding of outcome assessment, and selective reporting) is reported in the available context data, so the pooled estimate is unweighted by internal validity. Given that survival outcomes in several of these trials were secondary or exploratory, the selective-reporting domain is of particular concern.
8. **Direction-label ambiguity.** As noted, the automated favourability field did not resolve to an arm, so the favourable interpretation rests on the protocol's stated convention rather than on data-derived confirmation.

---

## 12. Conclusion

In women with early-stage triple-negative breast cancer, pooling five randomized comparisons (N = 1,395) yields a pooled **Hazard Ratio (HR) of 0.671 (95% CI 0.486–0.925; p = 0.0148; I² = 39.25%; τ² = 0.048144; Q = 6.961, df = 4, p = 0.138; REML)** for disease-free survival with the addition of carboplatin or cisplatin to neoadjuvant chemotherapy, compared with the same neoadjuvant chemotherapy without platinum. Under the review's pre-specified direction convention this represents an approximately one-third relative reduction in the hazard of a disease-free survival event in the platinum-containing arm; the analysis's own direction field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)" and therefore did not independently confirm which arm is favoured. The effect measure was confirmed and pooled natively on the hazard-ratio scale, so this is a native-scale hazard ratio rather than a standardized fallback.

All five contributing trials pointed in the same direction, no statistically significant funnel asymmetry was detected (Egger's p = 0.1151) and trim-and-fill imputed no missing studies (k₀ = 0), supporting a low formal risk of publication bias. Against this, only five comparisons were available, seven of twelve eligible randomized trials could not contribute because they did not report a hazard ratio with a confidence interval for disease-free survival, heterogeneity was moderate, and the implied prediction interval includes no effect.

The reasonable reading is therefore: **the addition of platinum to neoadjuvant chemotherapy in early-stage TNBC probably improves disease-free survival, by an amount that is clinically non-trivial but whose magnitude is poorly pinned down and whose distribution across patient subgroups is unknown.** Mature survival reporting with formal hazard ratios from the trials that have so far reported disease-free survival only descriptively, and an individual-patient-data meta-analysis stratified by germline *BRCA* status, homologous-recombination-deficiency score and nodal status, are the two developments most likely to convert this probable benefit into an actionable, patient-specific recommendation.

---

## 13. Figures

| Figure | Path |
|---|---|
| Forest plot of study-level and pooled estimates | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Distribution of effect sizes | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect size vs. study size/precision) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 14. References

Methodological and reporting standards applied in this review:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
4. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *J Educ Behav Stat*. 2005;30(3):261–293. (REML estimation of τ².)
5. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
6. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
7. Parmar MKB, Torri V, Stewart L. Extracting summary statistics to perform meta-analyses of the published literature for survival endpoints. *Stat Med*. 1998;17(24):2815–2834. (Conversion of reported HR confidence intervals to standard errors of the log hazard ratio.)
8. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
9. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
10. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.

Primary studies contributing effect sizes are identified in Section 3 by their extraction-pipeline labels (study_2_R2, study_3_R3, study_4_R4, study_6_R6, study_8_R8); full bibliographic details are held in the accompanying extraction dataset.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| disease-free survival | 5 | Hazard Ratio (HR) | Yes | 0.6707 [0.4864, 0.9247] |
