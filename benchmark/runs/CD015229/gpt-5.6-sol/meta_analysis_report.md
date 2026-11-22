# Single Sympathetic Nerve Block for Pain at 14 Days: A Systematic Review and Random-Effects Meta-analysis

## Abstract

## Abstract

**Background:** Sympathetic nerve blocks are used for some pain conditions, but their short-term benefit relative to standard care remains uncertain.

**Objective:** To estimate the effect of a single sympathetic nerve block, compared with standard care without sympathetic nerve block, on pain intensity or severity measured exactly 14 days after the block.

**Methods:** Eligible studies compared a single sympathetic nerve block with standard care and reported a pain score at day 14. Outcomes at other follow-up times, including 1 month, were excluded rather than substituted for the prespecified timepoint. To prevent double-counting when multiple day-14 instruments were available, the prespecified selection hierarchy was the study’s primary pain measure, followed by a validated multi-item pain scale, and then a unidimensional numeric rating scale or visual analogue scale. The supplied dataset contained five studies, of which two contributed eligible effect estimates (76 participants). Effects were pooled by restricted maximum likelihood (REML). The deterministic evidence classified the native pooled statistic as a **Mean Difference (MD)**.

**Results:** The study-level entries supplied by the analysis pipeline were 0.113317 (95% CI −0.764 to 0.991; n = 20) and −0.991720 (95% CI −1.547 to −0.436; n = 56). The REML pooled **Mean Difference** was −0.43562753976547075 (95% CI −1.404 to 0.533; p = 0.37791467840592097; k = 2; n = 76), with the recorded direction favoring a single sympathetic nerve block. Heterogeneity was considerable: Q = 5.74 (df = 1, p = 0.0166), I² = 82.58%, and τ² = 0.404671.

**Conclusions:** The point estimate favored a single sympathetic nerve block, but the confidence interval included the null and the result was not statistically significant. With only two contributing studies, substantial heterogeneity, incomplete study-level clinical information, and an unresolved discrepancy between the labels attached to study-level and pooled effects, the evidence is very uncertain and does not establish a day-14 benefit.

## Introduction

Sympathetic nerve blocks are used in the management of selected pain conditions, particularly when sympathetically maintained pain is suspected. Their effectiveness may depend on the underlying diagnosis, block technique, injectate, comparator treatment, and timing of outcome assessment. Combining outcomes from materially different follow-up periods can obscure a time-specific treatment effect. This review therefore addressed a narrowly defined question: among patients with pain conditions, what is the effect of a **single sympathetic nerve block**, compared with **standard care without sympathetic nerve block**, on pain intensity or severity measured exactly **14 days after the block**?

The analysis was restricted to the day-14 pain outcome. Pain measurements at other follow-up times—including outcomes reported at 1 month—were not substituted for or combined with the day-14 outcome. Reporting follows PRISMA 2020 principles to the extent permitted by the supplied evidence file [1].

## Search and Screening

### Eligibility criteria

Studies were eligible for the quantitative synthesis when they:

1. enrolled patients with a pain condition;
2. evaluated a single sympathetic nerve block;
3. included a standard-care comparison group that did not receive a sympathetic nerve block; and
4. reported pain intensity or pain severity at 14 days after the block in a form suitable for effect-size estimation.

Pain outcomes measured at timepoints other than day 14 were excluded from this analysis. They were not carried forward, interpolated, or used as substitutes. If a study reported more than one eligible pain instrument at day 14, the prespecified hierarchy was: (1) the study’s designated primary pain measure; (2) a validated multi-item pain scale; and (3) a unidimensional numeric rating scale or visual analogue scale. This hierarchy was intended to ensure that each participant contributed only once to the meta-analysis.

### Information sources and selection process

The supplied pipeline summary contained five studies and two eligible effect sizes. Thus, two studies contributed to the day-14 quantitative synthesis, while three did not contribute an eligible effect estimate. Search databases, search dates, complete search strings, reviewer procedures, and study-specific reasons for exclusion or non-contribution were not included in the supplied results. A numerical PRISMA flow diagram therefore cannot be reconstructed beyond the reported counts, and no assumptions were made about the three non-contributing studies.

## Included Studies

Two studies, identified in the supplied data as `study_1_R1` and `study_4_R4`, contributed 76 participants in total. `study_1_R1` included 20 participants, and `study_4_R4` included 56 participants.

No information was supplied about participant diagnoses, demographic characteristics, clinical settings, anatomical block sites, technical guidance, local anesthetic or adjunct agents, standard-care regimens, pain instruments, baseline pain, trial design, allocation methods, or risk-of-bias domains. Consequently, clinical comparability and internal validity could not be evaluated in detail. Bibliographic details for the included studies were also unavailable, so study-specific citations cannot be provided.

## Effect Sizes

The pipeline reported the following study-level estimates under the label “Hedges g”:

- `study_1_R1`: 0.113317 (95% CI −0.764 to 0.991; n = 20).
- `study_4_R4`: −0.991720 (95% CI −1.547 to −0.436; n = 56).

These estimates differ substantially in magnitude and have opposite statistical signs. However, treatment direction was not inferred from those signs. For the pooled result, direction was taken directly from the supplied `favors` field, as required by the analysis specification.

Importantly, the deterministic evidence classified the meta-analytic effect as a native-scale **Mean Difference (MD)** (`native_pooling_used = true`), whereas the study-level entries were labeled Hedges g. Accordingly, the pooled result below is reported as a **Mean Difference**, not as Hedges g. The inconsistency between study-level and pooled labels requires verification against the source extraction and statistical code before clinical interpretation on a specific pain scale.

The study-specific and pooled estimates are displayed in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The supplied distribution plot is at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

## Meta-Analytic Result

A random-effects model estimated by restricted maximum likelihood included two studies and 76 participants. The pooled **Mean Difference** was **−0.43562753976547075** (95% CI **−1.404 to 0.533**; p = **0.37791467840592097**). The supplied direction field indicates that this result **favors a single sympathetic nerve block** over standard care without sympathetic nerve block.

Nevertheless, the confidence interval crossed the null value, and the pooled effect was not statistically significant at the conventional two-sided 0.05 level. The interval is compatible with effects in either direction. Given the unresolved scale-labeling discrepancy, the numerical estimate should not be interpreted as a definitive change in units of a particular pain instrument until the original outcome scale is confirmed.

A cumulative meta-analysis figure was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. With only two studies, any apparent change in the cumulative estimate is highly dependent on study ordering and should not be interpreted as evidence of temporal stabilization.

## Heterogeneity

Statistical heterogeneity was considerable:

- Cochran’s Q = **5.74** with **1 degree of freedom**;
- Q-test p = **0.0166**;
- I² = **82.58%**; and
- τ² = **0.404671**.

The significant Q test and high I² indicate that the observed difference between study estimates is unlikely to be explained by sampling error alone. The heterogeneity summary figure is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

Because only two studies were available, τ² and I² are imprecisely estimated, and the sources of heterogeneity cannot be separated reliably. Plausible explanations could include differences in pain diagnosis, block technique, co-interventions, standard-care protocols, pain instruments, or study quality, but the supplied data do not permit these hypotheses to be tested. No prediction interval was provided; with k = 2, such an interval would in any event be highly unstable.

## Moderators

No valid moderator analysis was possible. Only two studies contributed to the synthesis, and no study-level covariates were supplied. Subgroup analyses or meta-regression with so few studies would be unreliable and potentially misleading.

A bubble chart was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`; however, it should be regarded as descriptive only and not as evidence of a moderator relationship. No causal or statistical moderator conclusion can be drawn from it.

## Publication Bias

Publication bias and small-study effects could not be assessed meaningfully. Funnel-plot asymmetry tests and regression-based procedures generally have very low power with small meta-analyses and are not recommended with only two studies [2,3]. No publication-bias statistic was supplied. Selective non-reporting remains possible, especially because only two of the five studies in the pipeline contributed a day-14 effect estimate, but the reasons the other three studies did not contribute were unavailable.

## Discussion

### Principal findings

This meta-analysis found a pooled **Mean Difference of −0.43562753976547075** at 14 days, with the supplied direction classification favoring a single sympathetic nerve block. The 95% CI ranged from −1.404 to 0.533, and the effect was not statistically significant (p = 0.37791467840592097). Thus, the analysis does not provide conclusive evidence that a single sympathetic nerve block improves day-14 pain relative to standard care.

The two studies produced markedly different estimates, reflected in I² = 82.58% and τ² = 0.404671. This inconsistency is clinically important: the pooled average may not represent the effect expected in any particular pain population or block protocol. The estimate is additionally fragile because it is based on only two studies and 76 participants.

### Interpretation

The point estimate alone should not be treated as evidence of effectiveness. The confidence interval includes the null, heterogeneity is substantial, and the available information is insufficient to judge study quality or clinical comparability. Statistical non-significance also does not establish equivalence or absence of benefit; rather, the evidence remains inconclusive.

The restriction to exactly 14 days is a methodological strength because it avoids mixing outcomes measured over different clinical periods. In particular, no 1-month result was substituted for a missing day-14 result. The outcome-selection hierarchy also reduces the risk of double-counting participants when several pain instruments are reported at the same timepoint.

### Clinical and research implications

Current results are insufficient to support a firm clinical recommendation for or against a single sympathetic nerve block solely on the basis of pain at day 14. Future trials should clearly define the target pain syndrome, standardize or fully describe the block technique and comparator care, prespecify the day-14 assessment, report the primary pain instrument and its direction, and provide means, standard deviations, and sample sizes by randomized group. Larger, methodologically rigorous trials are needed to determine whether effects vary by diagnosis, block location, or co-intervention.

## Data Quality and Validation Notes

Although no formal `validation_flags` object was supplied, several data constraints are evident from the provided results:

- The pipeline listed five studies but only two eligible day-14 effect sizes; study-specific reasons for the three non-contributions were not provided.
- The study-level estimates were labeled Hedges g, while deterministic evidence classified the native pooled measure as a Mean Difference. This discrepancy must be audited against the source data before the pooled numerical value is interpreted in clinical scale units.
- Pain instruments and their scale directions were not reported. The statement about which treatment is favored therefore follows the supplied `favors` field and is not inferred from the sign of the pooled estimate.
- No search documentation, risk-of-bias assessments, or source-study bibliographic details were supplied.

## Limitations

This review has several important limitations. First, only two studies and 76 participants contributed to the meta-analysis, producing low precision and unstable heterogeneity estimates. Second, heterogeneity was considerable and statistically significant, but clinical and methodological moderators were unavailable. Third, the absence of study characteristics and risk-of-bias assessments prevents evaluation of applicability and internal validity. Fourth, the reasons that three of five pipeline studies did not contribute to the day-14 analysis are unknown, creating uncertainty about missing outcome data and selective reporting. Fifth, publication bias could not be assessed. Sixth, the discrepancy between study-level Hedges g labels and the native pooled Mean Difference raises a data-provenance concern. Finally, no minimally important difference for the applicable pain scale was supplied, so clinical importance cannot be established even though the statistical point estimate favors the intervention according to the supplied direction field.

## Conclusion

Across two studies involving 76 participants, the REML pooled **Mean Difference** in pain at 14 days was **−0.43562753976547075** (95% CI **−1.404 to 0.533**; p = **0.37791467840592097**), with the supplied direction indicating a result favoring a single sympathetic nerve block. The confidence interval included no effect, and heterogeneity was considerable (I² = **82.58%**, τ² = **0.404671**). Consequently, the available evidence is inconclusive. More complete and rigorous evidence is required before a reliable estimate of day-14 benefit can be established.

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71.
2. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002. doi:10.1136/bmj.d4002.
3. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.5. Cochrane; 2024.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1-48. doi:10.18637/jss.v036.i03.
5. Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis*. Academic Press; 1985.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| pain score | 2 | Mean Difference (MD) | Yes | -0.4356 [-1.4040, 0.5327] |
