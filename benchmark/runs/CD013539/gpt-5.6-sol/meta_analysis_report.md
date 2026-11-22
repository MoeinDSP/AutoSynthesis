# Progression-Free Survival With Bevacizumab Biosimilars Versus Originator Bevacizumab in Adults With Cancer: A Systematic Review and Meta-analysis

## Abstract

**Background:** Bevacizumab biosimilars are intended to have no clinically meaningful differences from originator bevacizumab. This review assessed progression-free survival (PFS) in adults with cancer.

**Methods:** Trial-level hazard ratios (HRs) from each study’s time-to-event analysis were eligible. HRs were not to be reconstructed from Kaplan–Meier curves, event counts, medians, P values, or other incomplete summaries. Four studies contributing 2,534 participants supplied an estimable PFS effect and were pooled using a random-effects restricted maximum-likelihood (REML) model. An HR below 1 favored the bevacizumab biosimilar.

**Results:** Although five studies were represented in the pipeline, four contributed to the quantitative synthesis. The pooled Hazard Ratio (HR) was 1.002301448687117 (95% CI 0.914–1.099; p = 0.9608538966971846), classified in the supplied results as favoring neither group—essentially a tie. Heterogeneity was absent in the observed dataset (Q = 2.264, df = 3, p = 0.5195; I² = 0.0%; τ² = 0.0). Egger’s intercept was −0.2937 (p = 0.5809), but this test had very low power with only four studies. Trim-and-fill estimated one potentially missing study; publication-bias risk was therefore classified as moderate.

**Conclusions:** Available trial-level evidence showed no detectable difference in PFS between bevacizumab biosimilars and originator bevacizumab. The confidence interval remains compatible with modest benefit or harm, and the small evidence base, incomplete study descriptors, and limited ability to assess reporting bias warrant cautious interpretation.

## Search/Screening

This report addresses the question: among adults with cancer, what is the effect of a bevacizumab biosimilar, compared with originator bevacizumab, on progression-free survival (PFS)? The prespecified effect measure was the hazard ratio (HR) from each trial’s own time-to-event survival analysis. For the reported HR, values below 1 favor the biosimilar because they represent a lower hazard of progression or death; HRs above 1 favor originator bevacizumab.

The supplied pipeline summary contained five studies and four estimable effect sizes. Thus, four studies entered the quantitative synthesis and one study did not contribute an effect estimate. The reason the fifth study could not be pooled was not supplied. No information was provided about searched databases, registries, search dates, search terms, language restrictions, duplicate removal, record-level screening, full-text exclusions, protocol registration, or reviewer procedures. A complete PRISMA flow diagram therefore cannot be reconstructed from the available results.

To protect the validity of the time-to-event analysis, eligible effects were restricted to HRs reported directly by the trials or derivable from a reported HR and its 95% confidence interval. HRs were not reconstructed or approximated from Kaplan–Meier curves, event counts, median PFS, P values alone, or other summary data.

## Included Studies

Five studies were represented in the evidence pipeline. Four studies—labeled `study_1_R1`, `study_2_R2`, `study_3_R3`, and `study_5_R5`—contributed PFS effect estimates and a combined sample of 2,534 participants. Their respective sample sizes were 548, 689, 535, and 762. No trial-level information was supplied for the fifth study, and it did not contribute to the meta-analysis.

Study names, publication years, countries, cancer types and stages, biosimilar products, treatment backbones, lines of therapy, follow-up durations, PFS definitions, analysis populations, and risk-of-bias judgments were not available. Consequently, clinical comparability and internal validity could not be examined beyond the statistical results supplied.

## Effect Sizes

The metadata explicitly identifies the effect measure as a native **Hazard Ratio (HR)** requested by the user. The four study-level numeric entries were stored under a generically named `hedges_g` field; given the explicit HR metadata and their relationship to the pooled HR, they were treated as log(HR) values rather than as standardized mean differences. This field-label inconsistency should be considered when auditing the extraction.

The individual estimates were:

| Study label | n | Supplied log(HR) | Supplied 95% CI on log scale | HR (exponentiated) | Approximate 95% CI for HR |
|---|---:|---:|---:|---:|---:|
| `study_1_R1` | 548 | −0.005533 | −0.173 to 0.162 | 0.994482 | 0.841137–1.175860 |
| `study_2_R2` | 689 | −0.045920 | −0.195 to 0.103 | 0.955118 | 0.822835–1.108491 |
| `study_3_R3` | 535 | 0.058447 | −0.111 to 0.228 | 1.060188 | 0.894939–1.256085 |
| `study_5_R5` | 762 | −0.005536 | −0.148 to 0.136 | 0.994479 | 0.862431–1.145682 |

The exponentiated study estimates are shown to aid clinical interpretation; small differences in the last displayed digit may arise because the supplied study-level confidence limits were rounded to three decimals. Every study-level confidence interval crossed the null value of HR = 1. The estimates clustered closely around the null, with two point estimates slightly below 1, one slightly above 1, and one essentially at 1.

The trial estimates and pooled result are displayed in the forest plot at `outputs/HShuwD5_xJc0KHeDZGpcYg/forest_plot.png`. Their distribution is shown at `outputs/HShuwD5_xJc0KHeDZGpcYg/effect_distribution.png`.

## Meta-Analytic Result(s)

A random-effects model estimated by restricted maximum likelihood (REML) pooled four native PFS HRs from 2,534 participants. The pooled **Hazard Ratio (HR)** was **1.002301448687117** (95% CI **0.914–1.099**; p = **0.9608538966971846**).

According to the supplied favorability classification, this result favored **neither group and was essentially a tie**. Clinically, it indicates no detectable difference in the hazard of progression or death between bevacizumab biosimilars and originator bevacizumab. The confidence interval nevertheless remains compatible with a modest reduction or increase in hazard and therefore should not be interpreted as proving exact equality or formal equivalence.

A cumulative meta-analysis plot was generated at `outputs/HShuwD5_xJc0KHeDZGpcYg/cumulative_plot.png`. Because no numerical cumulative estimates or study ordering were provided, the temporal or sequential pattern should be interpreted from that figure rather than inferred from the final pooled result alone.

## Heterogeneity

There was no observed statistical heterogeneity:

- Cochran’s Q = **2.264** with 3 degrees of freedom;
- Q-test p = **0.5195**;
- I² = **0.0%**; and
- τ² = **0.0**.

These values indicate that the observed dispersion was no greater than expected from within-study sampling error. However, only four studies were pooled, so the Q test had limited power and the estimates of I² and τ² were imprecise. An I² of 0% does not establish that the trials were clinically identical or that the true between-study variance is exactly zero.

A graphical heterogeneity summary is available at `outputs/HShuwD5_xJc0KHeDZGpcYg/heterogeneity_summary.png`.

## Moderators

No moderator or subgroup results were supplied. Accordingly, there is no evidence from these analyses about whether relative PFS effects vary by cancer type, biosimilar product, geographic region, treatment backbone, line of therapy, disease stage, follow-up duration, or study-level risk of bias.

A bubble chart was generated at `outputs/HShuwD5_xJc0KHeDZGpcYg/bubble_chart.png`, but the underlying moderator, coefficient, confidence interval, and statistical test were not reported in the context data. It therefore cannot support a quantitative meta-regression conclusion in this report. In any event, a meta-regression with only four studies would be severely underpowered and at substantial risk of spurious findings.

## Publication Bias

Egger’s regression produced an intercept of **−0.2937** with p = **0.5809**, providing no statistical evidence of small-study effects or funnel-plot asymmetry. This non-significant result should not be interpreted as evidence that publication bias is absent: with k = 4, Egger’s test is substantially underpowered and is generally unsuitable for firm conclusions.

Trim-and-fill estimated **one** potentially missing study (k₀ = **1**). The output also reported a trim-and-fill value of **0.013** under the field `trim_fill_g`; its scale was not identified as a native HR, so it was not interpreted as an adjusted pooled HR. Taking the non-significant Egger test, the imputed study, and the very small number of studies together, the supplied analysis classified publication-bias risk as **moderate**. Publication bias therefore cannot be ruled out.

## Discussion

This meta-analysis found essentially identical PFS between bevacizumab biosimilars and originator bevacizumab. The pooled HR of 1.002301448687117 was extremely close to the null, and its p value of 0.9608538966971846 showed no evidence against the null hypothesis of equal hazards. The consistency of the four trial estimates and the absence of observed heterogeneity strengthen the descriptive conclusion that the available trials produced similar relative effects.

The result should be interpreted as an estimate of comparative PFS, not as proof of pharmaceutical equivalence in every respect. Failure to detect a difference in a conventional superiority-style meta-analysis is not itself a formal demonstration of equivalence or non-inferiority. Such conclusions require prespecified clinical margins and appropriate confidence-interval comparisons. The pooled 95% CI of 0.914–1.099 excludes very large relative differences but remains compatible with modest effects in either direction.

The findings are clinically reassuring insofar as PFS is a direct time-to-event efficacy outcome and the analysis used trial-derived HRs rather than approximations from medians or Kaplan–Meier graphics. Native HR pooling also preserves both event timing and censoring information embodied in each trial’s survival analysis. Nevertheless, applicability cannot be assessed fully because the cancer populations, biosimilar agents, treatment regimens, and follow-up schedules were not described in the supplied data.

The forest, cumulative, distribution, bubble, and heterogeneity plots should be considered supporting visualizations rather than substitutes for the numerical results. In particular, the cumulative and bubble plots cannot be interpreted definitively without their study-ordering and moderator metadata.

## Data Quality & Validation Notes

Although no formal `validation_flags` object was supplied, several data-provenance issues are evident from the provided results:

1. The pipeline listed five studies but only four effect sizes; no reason was provided for the fifth study’s non-contribution.
2. Trial-level values were stored in a field named `hedges_g`, while the meta-analysis metadata explicitly specified native HR pooling. They were interpreted as log(HR) values because the configured effect measure was HR and exponentiation was consistent with the pooled result; this should be checked against the original extraction file.
3. The trim-and-fill estimate was also labeled `trim_fill_g`, and its native scale was not confirmed. It was therefore not presented as an adjusted HR.
4. Bibliographic citations and core clinical characteristics of the included trials were absent, preventing source verification, assessment of overlapping reports, and trial-level risk-of-bias appraisal.

## Limitations

First, only four studies and 2,534 participants contributed to the pooled result. This limited the precision of heterogeneity estimates, precluded credible moderator analyses, and made statistical tests of publication bias unreliable.

Second, the available summary did not provide a reproducible search strategy or PRISMA screening counts. It is therefore not possible to assess search completeness, selection procedures, or reasons for exclusion.

Third, study-level clinical characteristics were unavailable. Potential differences in malignancy, disease stage, concomitant chemotherapy, treatment line, PFS assessment schedule, stratification factors, and analysis population could not be investigated.

Fourth, trial-level risk of bias could not be assessed. Randomization methods, allocation concealment, blinding, outcome adjudication, attrition, protocol deviations, and selective reporting were not described.

Fifth, the generic `hedges_g` field names create a data-labeling ambiguity even though the analysis metadata identifies native HR pooling. Verification against the original trial reports and extraction sheets is advisable before publication.

Finally, the analysis evaluates relative PFS only. It does not establish comparability for overall survival, objective response, toxicity, immunogenicity, quality of life, or cost, and it does not by itself constitute a formal biosimilarity, equivalence, or non-inferiority assessment.

## Conclusion

Across four studies involving 2,534 adults with cancer, bevacizumab biosimilars and originator bevacizumab produced essentially indistinguishable PFS. The REML random-effects pooled Hazard Ratio (HR) was **1.002301448687117** (95% CI **0.914–1.099**; p = **0.9608538966971846**), with no observed heterogeneity (I² = **0.0%**, τ² = **0.0**). The supplied result therefore favored neither group and was essentially a tie.

These findings support similar PFS efficacy in the available trials, but formal equivalence cannot be claimed. Confidence is constrained by the small number of studies, incomplete reporting of search and study characteristics, inability to assess trial-level bias, unresolved extraction-field labels, and limited power to detect publication bias.

## References

Bibliographic details for the five study reports were not included in the supplied data and therefore cannot be cited without risking fabrication. The final manuscript should add the original trial reports after verification against the extraction dataset.

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71.
2. Higgins JPT, Thomas J, Chandler J, et al., editors. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.5. Cochrane; 2024.
3. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634. doi:10.1136/bmj.315.7109.629.
4. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463. doi:10.1111/j.0006-341X.2000.00455.x.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| progression-free survival | 4 | Hazard Ratio (HR) | Yes | 1.0023 [0.9144, 1.0987] |
