# Fluoropyrimidine-Based Combination Chemotherapy Versus Gemcitabine Plus Nab-Paclitaxel for Overall Survival in Advanced Pancreatic Cancer: A Systematic Review and Meta-Analysis

## Abstract

**Background:** The comparative overall-survival effect of fluoropyrimidine-based combination chemotherapy versus gemcitabine plus nab-paclitaxel in adults with advanced pancreatic cancer remains clinically important.

**Methods:** Eligible comparisons evaluated a fluoropyrimidine-based combination regimen—including combinations involving S-1, capecitabine, or 5-fluorouracil/leucovorin—against gemcitabine plus nab-paclitaxel and reported an overall-survival hazard ratio (HR) from a Cox proportional-hazards or equivalent survival model. Overall survival was the sole outcome. Reported HRs and 95% confidence intervals were analyzed on the log-HR scale and pooled using a random-effects restricted maximum-likelihood (REML) model. Six studies were represented in the review pipeline, but only four contributed usable effect estimates (total N = 1,088).

**Results:** Across four comparisons, the pooled Hazard Ratio (HR) was 0.7767061387528923 (95% CI 0.658 to 0.917; p = 0.0028443049495806122). The supplied direction field classified this result as favoring neither arm—an essentially tied or directionally indeterminate result for which favorability depends on the event coding—so no arm-level superiority is assigned here despite the numerical HR being below 1. Between-study heterogeneity was low: I² = 13.34%, τ² = 0.004597, and Q = 3.729 (p = 0.2923). Egger’s intercept was −0.0436 (p = 0.4759), but trim-and-fill estimated one potentially missing study; the supplied overall publication-bias risk was moderate.

**Conclusions:** The four-study REML synthesis produced a statistically significant pooled overall-survival HR with low observed heterogeneity. Nevertheless, interpretation of which treatment is favored is constrained by the supplied direction classification, incomplete study-level bibliographic and HR data, exclusion of two represented studies from quantitative synthesis, and the very small number of studies available for publication-bias assessment.

## Introduction

Advanced pancreatic cancer has a poor prognosis, and systemic chemotherapy is central to treatment. Gemcitabine plus nab-paclitaxel is an established multidrug regimen, while several fluoropyrimidine-based combinations—including regimens involving S-1, capecitabine, or 5-fluorouracil (5-FU) with leucovorin—are used or investigated as alternatives. Direct comparative evidence is therefore important when selecting treatment.

This systematic review and meta-analysis addressed the following question: among adults with advanced pancreatic cancer, what is the effect on overall survival of fluoropyrimidine-based combination chemotherapy compared directly with gemcitabine plus nab-paclitaxel? Overall survival was treated exclusively as a time-to-event outcome. Eligible quantitative estimates were hazard ratios reported by the source papers from Cox proportional-hazards or equivalent survival models; progression-free survival, response rates, adverse-event counts, comparisons of median survival, and reconstructed or approximated hazard ratios were not acceptable substitutes.

## Search and Screening

The supplied review pipeline contained six studies. Four studies provided usable overall-survival effect estimates and entered the quantitative synthesis; two did not contribute to the meta-analysis. The aggregate sample size across the four quantitatively synthesized studies was 1,088 participants.

The supplied context did not include bibliographic-database names, search dates, complete search strings, deduplication counts, title/abstract screening counts, full-text exclusion reasons, protocol-registration information, or a PRISMA flow diagram. Consequently, those details cannot be reconstructed without inventing information. In particular, it cannot be determined from the supplied results whether the two noncontributing studies lacked a usable overall-survival HR, were duplicate reports, or were excluded for another reason. They are therefore described only as not contributing a usable quantitative estimate.

Eligibility for the outcome synthesis required:

- adults with advanced pancreatic cancer;
- a direct comparison between fluoropyrimidine-based combination chemotherapy and gemcitabine plus nab-paclitaxel;
- overall survival analyzed as a time-to-event outcome; and
- an HR and uncertainty estimate from a Cox proportional-hazards or equivalent reported survival model, sufficient to obtain log(HR) and its standard error.

Studies without a usable overall-survival HR were ineligible for quantitative synthesis of this outcome. No substitute endpoint or reconstructed HR was used.

## Included Studies

The four contributing records were identified in the supplied dataset as `study_3_R3`, `study_4_R4`, `study_5_R5`, and `study_6_R6`. Their reported sample sizes were 122, 770, 113, and 83, respectively, summing to 1,088.

| Study identifier | Sample size | Included in OS synthesis |
|---|---:|---|
| `study_3_R3` | 122 | Yes |
| `study_4_R4` | 770 | Yes |
| `study_5_R5` | 113 | Yes |
| `study_6_R6` | 83 | Yes |
| Two additional represented studies | Not supplied | No usable quantitative contribution documented |

The supplied results did not report study design, recruitment period, country, disease-stage distribution, line of therapy, performance status, precise experimental regimen, dosing schedule, adjusted versus unadjusted model status, or risk-of-bias judgments. These characteristics therefore could not be summarized or used to assess clinical comparability.

## Effect Sizes

The prespecified and confirmed native effect measure was the **Hazard Ratio (HR)** for overall survival. The meta-analysis used native HR pooling, with computation on the time-to-event scale and REML estimation. Conventionally, HRs are analyzed after logarithmic transformation and then exponentiated for presentation.

The supplied study-level effect-size table was labeled `hedges_g` and contained the following standardized values:

| Study identifier | Supplied standardized value | 95% CI | N |
|---|---:|---:|---:|
| `study_3_R3` | −0.045683 | −0.401 to 0.309 | 122 |
| `study_4_R4` | −0.102629 | −0.244 to 0.039 | 770 |
| `study_5_R5` | −0.270674 | −0.660 to 0.119 | 113 |
| `study_6_R6` | −0.279017 | −0.711 to 0.153 | 83 |

These standardized entries are not presented as study-level HRs because the dataset did not supply their corresponding native HR labels or a documented conversion. They must not be interpreted as mortality HRs or used as substitutes for reported survival-model estimates. The authoritative pooled result supplied by the analysis pipeline was explicitly labeled **Hazard Ratio (HR)**, with native pooling confirmed.

The forest plot is available at `outputs/HShuwD5_xJc0KHeDZGpcYg/forest_plot.png`. The effect-size distribution is shown at `outputs/HShuwD5_xJc0KHeDZGpcYg/effect_distribution.png`, and the cumulative-analysis plot is at `outputs/HShuwD5_xJc0KHeDZGpcYg/cumulative_plot.png`.

## Meta-Analytic Result

A random-effects REML model synthesized four overall-survival comparisons comprising 1,088 participants. The pooled **Hazard Ratio (HR)** was **0.7767061387528923** (95% CI **0.658 to 0.917**; p = **0.0028443049495806122**).

The supplied `favors` field classified the pooled estimate as **“neither (essentially a tie, or a ratio measure where favourability depends on which event was counted).”** In accordance with that predefined classification, the result is not assigned as favoring either treatment arm in this report. This restraint is important because the event coding and HR contrast orientation needed to translate the numerical ratio into an arm-level clinical direction were not independently documented in the study-level data supplied for reporting.

The pooled confidence interval excluded the null HR of 1, and the model-level test was statistically significant. Statistical significance should not, however, be conflated with a confirmed treatment-direction interpretation.

## Heterogeneity

Observed statistical heterogeneity was low:

- **I² = 13.34%**;
- **τ² = 0.004597**;
- **Cochran’s Q = 3.729**; and
- **Q-test p = 0.2923**.

The Q test did not reject homogeneity at conventional significance thresholds. Nevertheless, with only four studies, both Q and I² are imprecise, and absence of statistically detectable heterogeneity does not establish clinical equivalence among regimens or populations. The heterogeneity summary figure is available at `outputs/HShuwD5_xJc0KHeDZGpcYg/heterogeneity_summary.png`.

## Moderators

No study-level moderator results were supplied, and no subgroup analysis or meta-regression could be interpreted. Potentially relevant moderators would include the specific fluoropyrimidine regimen, treatment line, metastatic versus locally advanced disease, performance status, geographic setting, study design, and whether the reported HR was adjusted. None could be evaluated from the available data.

A bubble chart was generated at `outputs/HShuwD5_xJc0KHeDZGpcYg/bubble_chart.png`; however, the supplied context did not identify a moderator variable, regression coefficient, confidence interval, or p value associated with that figure. It therefore does not support a formal moderator conclusion.

## Publication Bias

Egger’s regression produced an intercept of **−0.0436** with **p = 0.4759**. This test was not statistically significant and supplied no strong evidence of funnel-plot asymmetry or small-study effects. Trim-and-fill estimated **one** potentially missing study (`k0 = 1`) and returned an adjusted standardized value of **−0.1128**.

The trim-and-fill value was not supplied as a native HR and therefore cannot be interpreted as an adjusted overall-survival HR. Moreover, publication-bias procedures are unstable with only four studies; Egger’s test has low power, and trim-and-fill depends on assumptions that may not hold under clinical heterogeneity. Consistent with the supplied interpretation, publication bias cannot be ruled out, and the overall publication-bias risk is considered **moderate**.

## Discussion

This quantitative synthesis included four direct comparisons with 1,088 participants. The random-effects REML model yielded a pooled HR of 0.7767061387528923, with a 95% CI from 0.658 to 0.917 and p = 0.0028443049495806122. Statistical heterogeneity was limited (I² = 13.34%), and the Q test was not significant. These findings indicate a comparatively consistent time-to-event association across the four included estimates on the scale used by the analysis.

The arm-level clinical direction requires caution. Although the pooled numerical HR was below 1, the analysis output explicitly classified favorability as neither arm or directionally dependent on event coding. Because treatment-reference coding was not supplied at the individual-study level, this report follows that classification rather than inferring treatment superiority from the sign or magnitude alone. Confirmation of the coding used in every original Cox model would be necessary before translating the pooled ratio into a definitive claim that one regimen reduces mortality relative to the other.

The low I² suggests that most observed dispersion could be compatible with sampling error, but the evidence base was too small to exclude clinically important heterogeneity. Fluoropyrimidine-based chemotherapy is not a single intervention: S-1-, capecitabine-, and 5-FU/leucovorin-containing combinations can differ in partner drugs, schedules, pharmacology, toxicity, and applicable patient populations. Pooling may therefore estimate an average association across clinically nonidentical regimens.

The largest contributing study contained 770 of the 1,088 participants (70.77%), whereas the other studies contained 122, 113, and 83 participants. Although inverse-variance random-effects weights were not supplied and cannot be inferred from sample sizes alone, the evidence base may be materially influenced by the largest comparison. A leave-one-out sensitivity analysis was not reported, so robustness to removal of that study is unknown.

Publication-bias findings were mixed but weakly informative: Egger’s test was nonsignificant, while trim-and-fill imputed one potentially missing study. Given k = 4, neither approach can reliably establish or exclude selective publication. The moderate supplied risk classification is therefore appropriate.

## Data Quality and Validation Notes

- Six studies were represented in the pipeline, but only four supplied effect estimates usable in the quantitative synthesis; the exact exclusion reasons for the remaining two were not provided.
- The native pooled measure was explicitly confirmed as an overall-survival **Hazard Ratio (HR)**, and native pooling was used.
- The study-level table was separately labeled `hedges_g`. Because those entries were not documented as native HRs, they were not relabeled or interpreted as study-level mortality HRs.
- The trim-and-fill adjusted value was also supplied on a standardized scale rather than as an HR; it was not treated as an adjusted pooled survival HR.
- Event coding and treatment-reference orientation were not documented at the study level. The supplied direction classification was therefore retained exactly, and no independent arm-favorability claim was inferred.
- No bibliographic metadata, formal risk-of-bias assessments, search audit trail, or study-level regimen characteristics were supplied.

## Limitations

First, only four studies contributed to the meta-analysis, limiting precision in estimates of between-study variance and making publication-bias tests unreliable. Second, two of the six studies represented in the pipeline did not contribute usable quantitative data, but the reasons were unavailable; selective availability of HRs cannot be excluded.

Third, study-level native HRs, log(HR) values, standard errors, and model-adjustment details were not included in the reporting dataset. This prevented independent verification of effect extraction, contrast orientation, proportional-hazards assumptions, and weighting. Fourth, the mismatch between standardized study-level fields and the confirmed native pooled HR precluded a transparent study-by-study display of the native survival estimates.

Fifth, no risk-of-bias assessment was supplied. Confounding may be especially consequential if any included evidence was observational. Sixth, clinical and methodological characteristics were unavailable, preventing assessment of transitivity and exploration of heterogeneity by regimen, disease extent, treatment line, or performance status. Seventh, no influence analysis, leave-one-out analysis, prediction interval, or alternative variance estimator was reported.

Finally, this report is necessarily limited to aggregate results supplied in the context. The absence of complete search, screening, extraction, and bibliography records prevents full independent replication and complete PRISMA reporting.

## Conclusion

In four studies totaling 1,088 participants, fluoropyrimidine-based combination chemotherapy versus gemcitabine plus nab-paclitaxel produced a pooled overall-survival **Hazard Ratio (HR) of 0.7767061387528923** (95% CI 0.658 to 0.917; p = 0.0028443049495806122) under a random-effects REML model. Heterogeneity was low (I² = 13.34%; τ² = 0.004597), although uncertainty remains because only four studies were available.

The supplied direction field did not assign the result to either treatment arm, so this report does not claim superiority of one regimen without confirmation of event and reference-group coding. Publication bias was not demonstrated by Egger’s test, but it could not be excluded and was classified as moderate. Definitive interpretation requires verification against the original reports, complete native HR extraction, transparent risk-of-bias assessment, and additional direct comparative evidence.

## References

Complete bibliographic references were not supplied in the context and therefore cannot be reproduced without fabrication. The quantitatively included records were identified only as `study_3_R3`, `study_4_R4`, `study_5_R5`, and `study_6_R6`. Original citations should be inserted from the review’s study-extraction database before journal submission.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| overall survival | 4 | Hazard Ratio (HR) | Yes | 0.7767 [0.6579, 0.9169] |
