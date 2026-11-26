# Semaglutide Versus Placebo for Medium-Term Percentage Change in Body Weight in Adults With Obesity: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

### Background
Semaglutide is used for chronic weight management, but its medium-term placebo-controlled effect in adults recruited primarily because of obesity requires quantitative synthesis.

### Objective
To estimate the effect of semaglutide, administered subcutaneously or orally at any dose for at least 6 months, versus placebo on percentage change in body weight from baseline at an on-treatment assessment between 6 and 24 months.

### Methods
The supplied dataset contained 11 effect-size records and reported a random-effects meta-analysis fitted by restricted maximum likelihood (REML). The prespecified effect was the semaglutide-minus-placebo mean difference (MD) in percentage points; negative values indicate greater weight reduction with semaglutide. The synthesis included 5,626 participants. Statistical heterogeneity and small-study effects were assessed using Cochran’s Q, I², τ², Egger’s test, Begg’s test, trim-and-fill, and PET–PEESE analyses.

### Results
Across 11 records, the pooled mean difference was −10.413085512407049 percentage points (95% CI −11.984 to −8.842; p=1.4303561864942757×10⁻³⁸), favoring semaglutide. Heterogeneity was considerable (Q=183.844, I²=95.53%, τ²=6.434948; reported Q-test p=0.0). Egger’s test (intercept −7.0688; p=0.2604) and Begg’s test (Kendall’s τ=−0.2569; p=0.2743) were not statistically significant. Trim-and-fill imputed two studies and produced an adjusted MD of −9.6293. PET–PEESE selected PET, yielding a corrected estimate of −5.6406 (p=0.1736). The supplied assessment classified publication-bias risk as moderate.

### Conclusions
The supplied analysis indicates substantially greater medium-term percentage body-weight reduction with semaglutide than with placebo. Confidence in the numerical magnitude is limited by extreme heterogeneity, mixed publication-bias diagnostics, absent study-level bibliographic and design information, and material internal inconsistencies in the supplied dataset—most notably a pipeline count of zero studies despite 11 pooled records and individual estimates labeled as “hedges_g” although the synthesis is designated a native-scale MD. The pooled estimate should therefore be considered provisional pending verification against original trial reports.

## Introduction

Obesity is a chronic, relapsing disease associated with cardiometabolic morbidity, impaired quality of life, and premature mortality. Semaglutide, a glucagon-like peptide-1 receptor agonist, has been evaluated in multiple placebo-controlled weight-management trials using subcutaneous and oral formulations and differing dose regimens. Percentage change in body weight is a clinically interpretable outcome that accommodates differences in baseline body mass and is commonly used in obesity trials.

This review addressed the following question: **In adults whose primary trial eligibility was obesity, what was the effect of semaglutide (any dose; subcutaneous or oral; administered for at least 6 months), compared with placebo, on percentage change in body weight from baseline at medium-term follow-up (6–24 months)?** The target contrast was the semaglutide-minus-placebo mean difference in percentage points at the assessment closest to the end of the eligible window while randomized treatment remained ongoing. Under this sign convention, a negative MD denotes greater weight loss with semaglutide.

## Search/Screening

The supplied results did not include bibliographic databases, search dates, full search strategies, deduplication procedures, reviewer methods, or counts for records identified, screened, excluded, and included. Consequently, a reproducible search strategy and PRISMA flow diagram cannot be reported from the available information.

The intended eligibility criteria were:

- adults enrolled primarily on the basis of obesity;
- randomized comparison of semaglutide with placebo;
- semaglutide administered orally or subcutaneously, at any dose, for at least 6 months;
- percentage change in body weight from baseline assessed during ongoing randomized treatment between 6 and 24 months; and
- use of the assessment closest to the end of the eligible window.

The intended exclusions were off-treatment or post-discontinuation extension assessments and outcomes expressed only as body weight in kilograms, BMI, waist circumference, or categorical weight-loss response. For multi-dose studies, the intended hierarchy was a reported combined semaglutide group, followed by 2.4 mg weekly, or the highest available dose if 2.4 mg was absent. For randomized-withdrawal designs, the intended contrast was change from withdrawal randomization to the end of randomized continuation versus placebo.

The dataset contained 11 effect-size records. However, the pipeline summary reported `n_studies=0` while simultaneously reporting `n_effect_sizes=11`. Because no exclusion log or trial identifiers were supplied, neither the number of unique trials nor the independence of all 11 records could be independently verified.

## Included Studies

The meta-analysis included 11 anonymized records with a reported total sample size of 5,626 participants. Record-level sample sizes ranged from 207 to 807. No author names, publication years, trial acronyms, recruitment settings, participant characteristics, semaglutide formulations, doses, follow-up times, estimands, analysis populations, or risk-of-bias assessments were provided.

The anonymized records and supplied estimates were as follows:

| Record | Supplied estimate | 95% CI | n |
|---|---:|---:|---:|
| study_1_R1 | −1.327911 | −1.496 to −1.160 | 667 |
| study_2_R2 | −1.735059 | −1.905 to −1.566 | 803 |
| study_3_R3 | −1.017460 | −1.195 to −0.840 | 611 |
| study_4_R4 | −1.014395 | −1.253 to −0.776 | 304 |
| study_5_R5 | −16.692810 | −18.327 to −15.059 | 207 |
| study_7_R7 | −1.456868 | −1.649 to −1.265 | 529 |
| study_8_R8 | −0.841342 | −1.006 to −0.677 | 616 |
| study_10_R10 | −1.069257 | −1.297 to −0.842 | 375 |
| study_11_R11 | −0.773399 | −0.916 to −0.630 | 807 |
| study_12_R12 | −1.451502 | −1.718 to −1.185 | 300 |
| study_13_R13 | −1.166840 | −1.388 to −0.946 | 407 |

The record identifiers are not consecutive; records 6 and 9 were not present. This may reflect screening or removal, but no explanation was supplied.

## Effect Sizes

The prespecified native effect measure was the **Mean Difference (MD)** in percentage change in body weight, calculated as semaglutide minus placebo. Therefore, negative values favor semaglutide because a more negative percentage change represents greater weight loss. The meta-analysis metadata designate the computation scale as MD, identify the source as the explicit user request, and state that native pooling was used.

The requested extraction hierarchy was: (1) directly reported adjusted treatment difference with its 95% CI; (2) arm-level model-based means with uncertainty; and (3) arm-level raw means with SDs. The supplied data did not identify which source was used for any record, nor did they provide arm-level statistics or analyzed denominators by treatment group. It was therefore not possible to verify adherence to the extraction hierarchy or independently reproduce the effect estimates.

Importantly, the individual-effect field in the supplied machine-readable data was named `hedges_g`, although the meta-analysis was explicitly designated as native-scale MD. Most individual values were approximately −0.77 to −1.74, whereas one was −16.692810. This pattern raises a serious possibility that standardized and native-scale estimates were mislabeled or mixed. The pooled statistic is reported below exactly as supplied and using its required label, **Mean Difference (MD)**, but the scale discrepancy requires source-data verification.

## Meta-Analytic Result(s)

A random-effects model fitted using restricted maximum likelihood included 11 records and 5,626 participants. The **pooled mean difference** was **−10.413085512407049 percentage points** (95% CI **−11.984 to −8.842**; p=**1.4303561864942757×10⁻³⁸**). According to the supplied `favors` field, the result favored **semaglutide (any dose; subcutaneous or oral; at least 6 months)**.

Clinically, if the native percentage-point scale is correct, the estimate corresponds to an average reduction in body weight approximately 10.41 percentage points greater with semaglutide than with placebo at medium-term follow-up. The confidence interval excludes no difference by a wide margin. Nevertheless, the estimate should not be treated as definitive because the individual records and pooled result show unresolved scale and numerical inconsistencies.

The forest plot is available at `forest.png`. A cumulative meta-analysis plot is available at `cumulative.png`, and the distribution plot is available at `distribution.png`. These figures should be interpreted with the same scale-validation caveat.

## Heterogeneity

Between-record heterogeneity was considerable:

- Cochran’s Q: **183.844**;
- reported Q-test p value: **0.0**;
- I²: **95.53%**; and
- τ²: **6.434948** on the reported MD scale.

Thus, most observed variation was attributed to between-record differences rather than sampling error. The Q-test p value of 0.0 is reproduced exactly as supplied and should be understood as a rounded or machine-reported value rather than a literal probability of zero.

The high I² indicates that the pooled MD is an average across substantially differing effects. Potential sources could include dose, route, treatment duration, follow-up time, participant characteristics, co-interventions, estimand, handling of treatment discontinuation, and randomized-withdrawal versus conventional parallel-group design. These explanations could not be tested because corresponding study-level data were absent. A heterogeneity summary is provided at `heterogeneity_summary.png`.

## Moderators

No moderator variables or meta-regression coefficients were supplied. Accordingly, no valid subgroup analysis or moderator inference could be performed for dose, route of administration, duration, follow-up time, trial design, baseline BMI, diabetes status, or analytic estimand.

A bubble plot was generated at `bubble.png`; however, in the absence of a specified moderator, coefficient, uncertainty estimate, and model description, it cannot support a quantitative moderator conclusion. Any visual pattern in that plot should be regarded as exploratory only.

## Publication Bias

The supplied publication-bias assessment classified overall risk as **moderate**. Tests were conducted on the reported Mean Difference (MD) scale.

- Egger’s intercept was **−7.0688** (p=**0.2604**).
- Begg’s rank-correlation statistic was **τ=−0.2569** (p=**0.2743**).
- Trim-and-fill estimated **2** potentially missing studies and gave an adjusted MD of **−9.6293**.
- PET estimated an MD of **−5.6406** (p=**0.1736**).
- PEESE estimated an MD of **−8.2664**.
- The PET–PEESE procedure selected PET, giving a corrected estimate of **−5.6406**.

Egger’s and Begg’s tests did not provide statistically significant evidence of funnel-plot asymmetry. Their power is limited with only 11 records, particularly in the presence of extreme heterogeneity. Conversely, trim-and-fill suggested two potentially missing studies, and PET–PEESE produced a materially attenuated estimate. These mixed findings support the supplied moderate-risk classification and warrant caution. Moreover, asymmetry methods may be unreliable if the underlying estimates do not share a valid common scale.

## Discussion

### Principal findings

The supplied REML synthesis found a pooled mean difference of −10.413085512407049 percentage points, favoring semaglutide over placebo for medium-term percentage change in body weight. If confirmed on the native scale, this would represent a large treatment effect. Every supplied individual estimate was negative, directionally favoring semaglutide under the prespecified semaglutide-minus-placebo convention.

The apparent consistency of effect direction did not translate into consistency of magnitude. Heterogeneity was extreme (I²=95.53%), and one estimate, −16.692810, differed sharply from the remaining estimates, which ranged from −0.773399 to −1.735059. This could represent a genuinely larger treatment effect, but it could also indicate incompatible effect metrics or a data-processing error. The pooled estimate is also not readily reconcilable with the displayed set of individual values, reinforcing the need for computational audit.

### Clinical interpretation

Assuming the effect measure is correctly expressed in percentage points, semaglutide produced greater weight reduction than placebo during 6–24 months of randomized treatment. However, the pooled average should not be assumed to apply uniformly across formulations, doses, populations, trial designs, or follow-up times. The absence of study-level details prevents assessment of clinical comparability and makes it impossible to determine whether the large heterogeneity arose from clinically meaningful effect modification or data incompatibility.

The analysis concerns percentage change in body weight only. It does not establish effects on absolute weight in kilograms, BMI, waist circumference, categorical weight-loss response, adverse events, treatment discontinuation, quality of life, or long-term cardiovascular outcomes.

### Certainty and applicability

A formal certainty-of-evidence assessment could not be completed because study-level risk of bias, inconsistency explanations, indirectness, and outcome-extraction details were unavailable. Imprecision around the supplied pooled mean was low, but statistical precision does not resolve concerns about heterogeneity, selective reporting, duplicate inclusion, or scale validity. Applicability is restricted to adults recruited primarily because of obesity and to assessments made during ongoing randomized therapy between 6 and 24 months.

## Data Quality & Validation Notes

Although no explicit `validation_flags` object was supplied, the dataset contains several issues requiring plain acknowledgment:

1. **Study-count contradiction:** the pipeline summary reports zero studies, whereas 11 effect-size records were pooled.
2. **Effect-measure labeling conflict:** individual estimates are stored under a field named `hedges_g`, but the synthesis is designated as native-scale Mean Difference (MD). The pooled result has therefore been labeled MD as required by the meta-analysis metadata, but its scale is not independently verified.
3. **Numerical incompatibility:** ten estimates cluster between approximately −0.77 and −1.74, while one equals −16.692810; the reported pooled MD of −10.413085512407049 is not readily explained by the displayed record-level pattern.
4. **Unverifiable independence:** anonymized record labels and absent citations prevent confirmation that each record represents a unique eligible trial or independent comparison.
5. **Missing extraction provenance:** the dataset does not state whether each estimate came from an adjusted treatment contrast, model-based arm means, or raw arm means.
6. **Missing design and timepoint information:** eligibility with respect to obesity as the primary enrollment criterion, treatment duration, ongoing randomized treatment, and the 6–24-month window cannot be independently confirmed.
7. **No risk-of-bias information:** study-level internal validity could not be evaluated.

These issues do not justify replacing the supplied numerical result with an invented alternative, but they substantially limit confidence in the pooled magnitude.

## Limitations

This report is limited by the information supplied. First, no reproducible search, PRISMA flow counts, exclusion reasons, protocol registration, or bibliographic references were available. Second, trial characteristics and risk-of-bias judgments were absent. Third, arm-level means, variances, sample sizes, and adjusted-effect derivations were not available for verification. Fourth, the discrepancy between the individual-effect field name and the designated pooled metric raises concern about mixed scales. Fifth, extreme heterogeneity reduces the interpretability of a single pooled average, and no prediction interval was supplied. Sixth, publication-bias tests had limited power with 11 records and may be distorted by heterogeneity. Seventh, no moderator analysis could explain between-record variation. Finally, duplicate populations, overlapping reports, and non-independent comparisons could not be ruled out.

## Conclusion

The supplied random-effects analysis of 11 records and 5,626 participants reported a pooled semaglutide-minus-placebo Mean Difference of **−10.413085512407049 percentage points** (95% CI **−11.984 to −8.842**; p=**1.4303561864942757×10⁻³⁸**), favoring semaglutide for medium-term percentage change in body weight. Heterogeneity was extreme (I²=**95.53%**), and publication-bias diagnostics were mixed, with an overall moderate-risk classification.

The direction of benefit favors semaglutide, but the precise pooled magnitude must be considered provisional. Verification against original reports and re-extraction on a confirmed common percentage-point scale are essential before this estimate is used for clinical guidance, guideline development, or decision modeling.

## References

No complete bibliographic citations were included in the supplied context. The available evidence records were identified only as `study_1_R1`, `study_2_R2`, `study_3_R3`, `study_4_R4`, `study_5_R5`, `study_7_R7`, `study_8_R8`, `study_10_R10`, `study_11_R11`, `study_12_R12`, and `study_13_R13`. Full trial reports and any associated protocols or statistical analysis plans should be added before publication.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| percentage change in body weight from baseline | 11 | Mean Difference (MD) | Yes | -10.4131 [-11.9845, -8.8417] |
