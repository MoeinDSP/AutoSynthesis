# Neoadjuvant Platinum Chemotherapy and Disease-Free Survival in Early-Stage Triple-Negative Breast Cancer: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background:** The survival effect of adding platinum to neoadjuvant chemotherapy for early-stage triple-negative breast cancer remains clinically important. This review evaluated disease-free survival and closely corresponding time-to-event outcomes for neoadjuvant chemotherapy with carboplatin or cisplatin versus the otherwise identical regimen without platinum.

**Methods:** Eligible comparisons were required to isolate the addition of platinum and report a hazard ratio (HR) for disease-free survival or a closely corresponding outcome. The supplied evidence set contained 12 study records and four effect-size entries; four independent comparisons (total N = 1,307) contributed to the quantitative synthesis. HRs were pooled using a restricted maximum-likelihood random-effects model. Heterogeneity was assessed using Cochran’s Q, I², and τ². Small-study effects were assessed using Egger’s test and trim-and-fill, with the important qualification that only four comparisons were available.

**Results:** The pooled Hazard Ratio (HR) was 0.6584065408916374 (95% CI 0.462–0.938; p = 0.020636156044091938; k = 4; N = 1,307). The supplied favorability classification was “neither (essentially a tie, or a ratio measure where favourability depends on which event was counted),” and this classification is retained rather than independently reassigned. Heterogeneity was moderate (I² = 51.27%; τ² = 0.062121); Cochran’s Q was 6.951 (p = 0.0735). Egger’s intercept was 0.3003 (p = 0.0083), indicating funnel-plot asymmetry, while trim-and-fill estimated no missing comparisons (k₀ = 0). The supplied assessment rated publication-bias risk as high.

**Conclusions:** The random-effects synthesis produced an HR below 1 with a confidence interval excluding 1, but the supplied direction field classified the result as favoring neither arm. Interpretation is limited by moderate heterogeneity, only four pooled comparisons, high assessed publication-bias risk, unavailable study-level bibliographic and outcome-definition details, and an inconsistency between the standardized labels attached to individual entries and the confirmed native HR used in the meta-analysis.

## Introduction

Triple-negative breast cancer lacks expression of estrogen receptor, progesterone receptor, and HER2 and is associated with a substantial risk of early recurrence. Platinum compounds produce DNA cross-links and may be particularly active in tumors with homologous-recombination deficiency. Although platinum-containing neoadjuvant regimens can affect short-term response, the clinically decisive question addressed here is whether adding carboplatin or cisplatin improves disease-free survival or a closely corresponding time-to-event outcome.

The objective was to estimate the effect on disease-free survival among women with early-stage triple-negative breast cancer of adding neoadjuvant carboplatin or cisplatin to an otherwise identical chemotherapy regimen, compared with that regimen without platinum. Pathological complete response, overall survival, toxicity, and other outcomes were outside the scope of this analysis.

## Search/Screening

The intended eligibility framework was as follows:

- **Population:** women with early-stage triple-negative breast cancer;
- **Intervention:** neoadjuvant chemotherapy plus carboplatin or cisplatin;
- **Comparator:** the same neoadjuvant chemotherapy regimen without platinum;
- **Outcome:** disease-free survival or a closely corresponding time-to-event outcome, including event-free, relapse-free, or invasive disease-free survival;
- **Effect estimate:** HR with a 95% confidence interval for platinum versus control, preferably from the longest reported follow-up; and
- **Design requirement:** a comparative study in which platinum addition was isolated from other regimen differences.

When multiple reports represented the same trial, the prespecified approach was to prioritize the later long-term survival analysis over an earlier pathological-complete-response report. Disease-free survival was to be preferred when both disease-free survival and an event-free survival definition incorporating preoperative progression were available.

The supplied context reports 12 studies or study records in the evidence pipeline and four effect-size entries. However, it provides no database names, search strings, search dates, registry sources, duplicate counts, full-text exclusion reasons, or record-level disposition for the remaining eight records. Consequently, a numerical PRISMA flow diagram and a reproducible search strategy cannot be reconstructed without inventing information. The quantitative synthesis was restricted to the four supplied independent effect-size entries.

## Included Studies

Four comparisons, identified only as R1 through R4, contributed to the meta-analysis:

- **R1:** N = 315;
- **R2:** N = 443;
- **R3:** N = 474; and
- **R4:** N = 75.

The combined analyzed sample was N = 1,307. R3 was the largest comparison and R4 the smallest.

The supplied material does not identify trial names, investigators, countries, recruitment periods, exact chemotherapy backbones, platinum agent and schedule, follow-up duration, outcome terminology, outcome definitions, randomization status, or risk-of-bias judgments. It therefore cannot establish from the available fields whether all four comparisons used disease-free survival specifically, rather than one of the permitted closely corresponding outcomes, or whether each estimate came from the longest available follow-up. These deficiencies limit clinical characterization and assessment of transitivity.

## Effect Sizes

The four individual entries were supplied under fields named `hedges_g` and `ci`, even though the meta-analysis record confirms native pooling on the HR scale (`effect_measure = HR`, `computation_scale = HR`, and `native_pooling_used = true`). The individual values should therefore not be presented as published native HRs without clarification. As supplied, they were:

- **R1:** −0.319671 (95% CI −0.542 to −0.097; N = 315);
- **R2:** −0.034056 (95% CI −0.220 to 0.152; N = 443);
- **R3:** −0.254329 (95% CI −0.446 to −0.063; N = 474); and
- **R4:** −0.826176 (95% CI −1.298 to −0.355; N = 75).

These individual values appear numerically compatible with log-HR-scale inputs, but their scale cannot be definitively relabeled from the supplied fields alone. They are therefore reported exactly as provided and are not described as published study-level HRs. The pooled estimate, in contrast, is explicitly confirmed as a native-scale Hazard Ratio (HR).

The study-level and pooled estimates are displayed in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The effect-size distribution is shown at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

## Meta-Analytic Result(s)

A restricted maximum-likelihood random-effects model was used. Across four comparisons and 1,307 participants, the pooled **Hazard Ratio (HR)** was **0.6584065408916374** (95% CI **0.462–0.938**; p = **0.020636156044091938**).

The supplied `favors` field classifies this result as **“neither (essentially a tie, or a ratio measure where favourability depends on which event was counted).”** In accordance with the provided analysis specification, that classification is reported directly and is not replaced by a direction inferred from the numerical HR. This classification should be reconciled against the prespecified coding of the event and treatment contrast before clinical conclusions about which arm is favored are drawn.

A cumulative meta-analysis plot is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. Because the ordering variable used in that plot was not supplied, it should not automatically be interpreted as chronological accumulation.

## Heterogeneity

Between-comparison heterogeneity was moderate:

- **I²:** 51.27%;
- **τ²:** 0.062121;
- **Cochran’s Q:** 6.951; and
- **Q-test p value:** 0.0735.

The Q test did not cross the conventional 0.05 threshold, but with only four comparisons it has limited power. The I² estimate indicates that approximately half of the observed variance was attributed by the model to between-comparison heterogeneity rather than sampling error. The nonzero τ² supports use of a random-effects model. The supplied results do not include a prediction interval, and one should not be fabricated.

A graphical heterogeneity summary is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

## Moderators

No study-level moderator data were supplied. Prespecified or clinically plausible moderators would include platinum agent (carboplatin versus cisplatin), platinum dose and schedule, anthracycline/taxane backbone, use of additional systemic agents, germline BRCA status, homologous-recombination deficiency, stage distribution, outcome definition, follow-up duration, and risk of bias. None could be analyzed.

Moreover, with k = 4, meta-regression or extensive subgroup analysis would be statistically unstable and at high risk of spurious findings even if covariate data were available. The bubble plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` may illustrate an association encoded by the pipeline, but the moderator variable and regression specification were not provided; it cannot support a substantive moderator conclusion.

## Publication Bias

Egger’s test produced an intercept of **0.3003** with **p = 0.0083**, indicating statistically detectable funnel-plot asymmetry in the supplied analysis. Trim-and-fill estimated **k₀ = 0** missing comparisons and supplied an adjusted value of **−0.3004**. Because that adjusted value was not explicitly labeled as a native-scale HR, it is not interpreted as an adjusted pooled HR.

The supplied publication-bias assessment was **high risk**. The significant Egger result warrants caution, and the finding of no imputed comparisons under trim-and-fill does not rule out selective publication or other small-study effects. At the same time, both Egger’s regression and trim-and-fill are unreliable with only four comparisons: asymmetry can arise from genuine heterogeneity, methodological differences, chance, or selective reporting, and absence of trim-and-fill imputation has low evidential value in such a small set.

## Discussion

This random-effects meta-analysis synthesized four comparisons involving 1,307 participants. The pooled Hazard Ratio (HR) was 0.6584065408916374 (95% CI 0.462–0.938; p = 0.020636156044091938). The confidence interval excluded the null HR of 1, but the supplied favorability field classified the result as favoring neither arm. This unresolved direction-label issue is material: it prevents an unqualified statement about which treatment is favored, notwithstanding the numerical estimate.

The results also showed moderate heterogeneity (I² = 51.27%; τ² = 0.062121). Differences in platinum compound, dose intensity, chemotherapy backbone, patient selection, survival endpoint definitions, and follow-up could plausibly contribute, but the supplied data do not permit these explanations to be tested. In particular, combining disease-free survival with closely corresponding outcomes can be reasonable when event definitions are sufficiently aligned, but differences such as inclusion of preoperative progression may alter the estimand.

The evidence should not be interpreted solely through statistical significance. The pooled estimate depends on four comparisons, one of which was small (N = 75), and Egger’s test indicated asymmetry. The publication-bias signal, moderate heterogeneity, and absent study-level methodological details reduce confidence in the precision and transportability of the summary estimate.

The forest plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`), cumulative plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`), effect distribution (`outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`), bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`), and heterogeneity summary (`outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`) should be reviewed alongside the numerical results.

## Limitations

1. **Incomplete search documentation:** Databases, dates, search terms, language restrictions, and supplementary search methods were not supplied, preventing assessment of search completeness and reproducibility.
2. **Incomplete screening accounting:** The pipeline reports 12 studies but only four effect sizes. The disposition of the other eight records and reasons for their non-inclusion in the quantitative synthesis were not provided.
3. **Missing bibliographic information:** Trial names, authors, publication years, and complete citations were unavailable.
4. **Unverified endpoint definitions:** The exact survival endpoint and event definition for each comparison were not supplied, so alignment of disease-free, event-free, relapse-free, and invasive disease-free survival could not be checked.
5. **Unverified report selection:** The available data do not demonstrate that the longest follow-up report was selected for every trial or that multiple reports of the same population were excluded without double-counting.
6. **Individual-effect labeling inconsistency:** Individual entries were labeled `hedges_g`, whereas the synthesis was explicitly designated as native HR pooling. Although the values may represent log HRs, this cannot be confirmed from the supplied fields.
7. **Direction-classification inconsistency:** The pooled HR is below 1, but the supplied `favors` field classifies the result as favoring neither arm. Event coding and contrast direction require source-level verification.
8. **Limited number of comparisons:** With k = 4, estimates of heterogeneity and small-study effects are imprecise, moderator analysis is not defensible, and publication-bias procedures are unstable.
9. **No risk-of-bias assessment:** Domain-level judgments for randomization, deviations from intervention, missing data, outcome measurement, and selective reporting were not available.
10. **No certainty assessment:** The supplied evidence was insufficient for a formal GRADE rating.
11. **No prediction interval:** The analysis did not supply a random-effects prediction interval, limiting assessment of the likely range of effects in a new setting.

## Conclusion

In four comparisons totaling 1,307 participants, addition of neoadjuvant platinum was associated with a pooled Hazard Ratio (HR) of 0.6584065408916374 (95% CI 0.462–0.938; p = 0.020636156044091938) under a REML random-effects model. Heterogeneity was moderate (I² = 51.27%; τ² = 0.062121), and publication-bias risk was rated high following a significant Egger test (intercept 0.3003; p = 0.0083), despite trim-and-fill estimating no missing comparisons. The supplied direction field classified the pooled result as favoring neither arm; therefore, the treatment-favorability conclusion should remain unresolved until event coding and contrast direction are verified against the source reports. Clinical confidence is further limited by the small evidence base, incomplete reporting of search and study characteristics, unavailable risk-of-bias assessments, and inconsistent labeling of individual effect estimates.

## References

Complete bibliographic details were not included in the supplied context and therefore cannot be reconstructed reliably. The four quantitative comparisons are retained under their supplied identifiers:

1. Study report R1 (`study_1_R1`), N = 315. Full citation not provided.
2. Study report R2 (`study_2_R2`), N = 443. Full citation not provided.
3. Study report R3 (`study_3_R3`), N = 474. Full citation not provided.
4. Study report R4 (`study_4_R4`), N = 75. Full citation not provided.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| disease-free survival | 4 | Hazard Ratio (HR) | Yes | 0.6584 [0.4622, 0.9380] |
