# Effects of Probiotics on End-of-Treatment Serum Creatinine in Chronic Kidney Disease: A Systematic Review and Meta-Analysis

## Abstract

### Background
Probiotics have been proposed as an adjunctive intervention for chronic kidney disease (CKD), but their effect on serum creatinine remains uncertain.

### Objective
To evaluate the effect of single-strain or multi-strain probiotic supplements or probiotic-containing foods, compared with placebo or no treatment, on serum creatinine measured at the end of approximately 8–24 weeks of treatment among people with CKD, including diabetic nephropathy and dialysis populations.

### Methods
Five study comparisons involving 253 participants were synthesized. The confirmed native-scale effect measure was the mean difference (MD) in serum creatinine (probiotic minus control), expressed in mg/dL. A random-effects model using restricted maximum likelihood (REML) was applied. Negative MDs indicate lower serum creatinine with probiotics. Heterogeneity was assessed using Cochran’s Q, I², and τ². Small-study effects were examined using Egger’s test and trim-and-fill.

### Results
The pooled mean difference was −0.1530330923822796 mg/dL (95% CI −0.237 to −0.069; p=0.00038377072271947467; k=5; n=253), favoring probiotics. No observed between-study heterogeneity was detected (Q=1.404, p=0.8435; I²=0.0%; τ²=0.0). Egger’s intercept was 1.2704 (p=0.1444), and trim-and-fill estimated no missing studies (k₀=0). The supplied assessment therefore classified publication-bias risk as low, although tests for funnel-plot asymmetry have limited power with only five studies.

### Conclusions
Across five comparisons, probiotics were associated with a statistically significant mean reduction of approximately 0.15 mg/dL in end-of-treatment serum creatinine. Interpretation should remain cautious because the dataset was small and did not provide study-level clinical characteristics, risk-of-bias judgments, or sufficient information for moderator analyses.

## Search/Screening

The review question was defined using the following eligibility framework:

- **Population:** People with chronic kidney disease (CKD) of any stage, including diabetic nephropathy and dialysis populations.
- **Intervention:** Single-strain or multi-strain probiotic supplements or probiotic-containing foods, including probiotic yoghurt, soy milk, or honey.
- **Comparator:** Placebo or no treatment.
- **Outcome:** Serum creatinine in mg/dL at the end of treatment, using the last assessment within approximately 8–24 weeks.
- **Eligible data:** Arm-level mean, standard deviation, and analyzed participant count. End-of-treatment values were preferred; change scores were eligible only when available for both arms and defined as end minus baseline.

The supplied dataset contained five eligible studies, five effect sizes, and 253 participants. A full database search strategy, search dates, deduplication counts, title/abstract screening counts, full-text exclusion reasons, and PRISMA flow counts were not supplied. Consequently, the reproducibility and completeness of the search and screening process cannot be independently evaluated from the available information.

The prespecified data-handling rules required conversion of serum creatinine reported in µmol/L to mg/dL by division by 88.4, conversion of SE/SEM to SD using `SD = SE × √n`, assignment of treatment arms from their definitions rather than column order, and standard combination of eligible probiotic arms in multi-arm studies. No study-specific extraction records were provided to determine whether any of these procedures were required in the included studies. Likewise, the available results did not identify any study as having been analyzed with change scores.

## Included Studies

Five study comparisons were included:

| Study label | Analyzed participants | Study estimate (mg/dL) | 95% CI (mg/dL) |
|---|---:|---:|---:|
| study_1_R1 | 40 | −1.108332 | −1.774 to −0.443 |
| study_2_R2 | 60 | −0.197401 | −0.705 to 0.310 |
| study_3_R3 | 33 | −0.127087 | −0.810 to 0.556 |
| study_4_R4 | 60 | −0.179189 | −0.686 to 0.328 |
| study_5_R5 | 60 | 0.000000 | −0.506 to 0.506 |
| **Total** | **253** | — | — |

The analysis metadata explicitly identifies the native effect measure as the **Mean Difference (MD)** and confirms that native-scale pooling was used. Accordingly, the study estimates above are presented as treatment-minus-control MDs in mg/dL. Negative values represent lower serum creatinine in the probiotic arm. Although the source payload names the study-level numerical field `hedges_g`, that field name is inconsistent with the confirmed native MD metadata and should not be interpreted as evidence that the primary synthesis used standardized effects.

The supplied materials did not report authors, publication years, countries, CKD stages, dialysis status, diabetic nephropathy status, probiotic strains or doses, food vehicles, treatment duration by study, comparator details, baseline creatinine, follow-up completeness, or risk-of-bias judgments. These characteristics therefore cannot be summarized without speculation.

## Effect Sizes

Four of the five point estimates were below zero, while one was exactly zero. Only `study_1_R1` had a 95% confidence interval excluding zero (MD −1.108332 mg/dL, 95% CI −1.774 to −0.443). The other four comparisons were individually imprecise and compatible with both benefit and harm:

- `study_2_R2`: MD −0.197401 mg/dL (95% CI −0.705 to 0.310).
- `study_3_R3`: MD −0.127087 mg/dL (95% CI −0.810 to 0.556).
- `study_4_R4`: MD −0.179189 mg/dL (95% CI −0.686 to 0.328).
- `study_5_R5`: MD 0.000000 mg/dL (95% CI −0.506 to 0.506).

The forest plot is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The supplied effect-distribution plot is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

## Meta-Analytic Result(s)

Using a random-effects REML model, the **pooled mean difference** was **−0.1530330923822796 mg/dL** (95% CI **−0.237 to −0.069**; **p=0.00038377072271947467**; k=5; n=253). As specified for this outcome and confirmed by the supplied `favors` field, the result favors **probiotics**. On average, probiotic treatment was associated with end-of-treatment serum creatinine approximately 0.153 mg/dL lower than placebo or no treatment.

The confidence interval excludes the null value of 0 mg/dL, indicating statistical significance at the conventional two-sided 0.05 level. Clinical importance cannot be established from the pooled MD alone because baseline kidney function, CKD stage, dialysis status, assay context, and minimal clinically important difference were not supplied.

A cumulative meta-analysis plot was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. Numerical cumulative estimates and the study ordering used in that plot were not included in the supplied results; therefore, no claims are made about when statistical significance emerged or how the pooled estimate evolved as studies accumulated.

## Heterogeneity

Observed statistical heterogeneity was absent:

- **Cochran’s Q:** 1.404 with 4 degrees of freedom
- **Q-test p value:** 0.8435
- **I²:** 0.0%
- **τ²:** 0.0

These statistics indicate that the observed dispersion was no greater than expected from within-study sampling error. The heterogeneity summary figure is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

An I² of 0.0% should not be interpreted as proof that the studies were clinically identical or that the true effect is necessarily constant. With only five studies, heterogeneity estimates and the Q test have limited ability to identify genuine between-study variation. Moreover, potentially important differences in CKD population, probiotic formulation, treatment duration, and comparator were not available for evaluation.

## Moderators

No subgroup estimates, meta-regression coefficients, moderator definitions, or study-level covariate data were supplied. Accordingly, it was not possible to assess whether effects varied according to:

- CKD stage or dialysis status;
- diabetic versus non-diabetic kidney disease;
- single-strain versus multi-strain probiotics;
- probiotic supplements versus probiotic-containing foods;
- probiotic species, dose, or treatment duration;
- placebo versus no-treatment controls; or
- use of end values versus change scores.

A bubble chart was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`; however, in the absence of a reported moderator variable, coefficient, confidence interval, and p value, it cannot support an inferential moderator conclusion.

## Publication Bias

Egger’s test produced an intercept of **1.2704** with **p=0.1444**. This was not statistically significant and provides no clear evidence of funnel-plot asymmetry or small-study effects. The trim-and-fill procedure estimated **k₀=0** missing studies, and the supplied assessment classified publication-bias risk as **low**.

The trim-and-fill module also returned an estimate of **−0.2886**. Because no studies were imputed and the supplied materials do not explain the estimator underlying that value, it should not replace the prespecified REML pooled MD of −0.1530330923822796 mg/dL. More broadly, publication-bias tests are unreliable with very few studies: with k=5, Egger’s test has low power, and trim-and-fill may fail to detect selective publication. Thus, “low risk” here means that the supplied statistical diagnostics did not identify asymmetry, not that publication bias has been excluded.

## Discussion

This meta-analysis found that probiotics were associated with lower end-of-treatment serum creatinine in people with CKD. Across five comparisons and 253 participants, the pooled MD was −0.1530330923822796 mg/dL, with a 95% CI from −0.237 to −0.069. The direction favors probiotics, and the result was statistically significant. Statistical heterogeneity was not observed, with I² and τ² both equal to zero.

The pooled finding was based on a pattern in which four studies had point estimates below zero and one showed no difference. Nevertheless, most individual studies were imprecise: four of five confidence intervals included zero. The pooled precision therefore reflects aggregation across studies rather than consistently conclusive results within each trial. The first comparison had a substantially larger absolute point estimate than the remaining comparisons, but the heterogeneity test did not indicate excess dispersion.

The result directly addresses serum creatinine at approximately 8–24 weeks; it should not be generalized to other renal outcomes or longer-term disease progression. Serum creatinine is influenced by kidney filtration as well as muscle mass, dietary intake, volume status, dialysis timing, and laboratory methods. Without accompanying clinical information, the observed mean reduction cannot establish whether probiotics improve long-term kidney function, reduce dialysis requirements, or improve patient-important outcomes.

No data were synthesized for eGFR/GFR, albuminuria or proteinuria, inflammatory markers, lipid measures, glucose, microbiota outcomes, or adverse events, in accordance with the scope of the review. The analysis therefore does not establish efficacy for those outcomes or characterize probiotic safety.

## Data Quality & Validation Notes

The analysis metadata confirms native pooling as a Mean Difference in mg/dL. However, the study-level source field is labeled `hedges_g`, creating a nomenclature inconsistency. The confirmed meta-analysis measure and computation scale were both MD, so standardized-effect terminology was not used for the primary result.

No arm-level means, SDs, analyzed counts by arm, original measurement units, table footnotes, or extraction annotations were supplied. It was therefore not possible to independently verify unit conversions, distinguish SD from SE/SEM, verify arm assignment, identify inferred column headings, confirm multi-arm pooling, or determine whether any study used change scores. No formal `validation_flags` were supplied, and no duplicate reports, reviews, or otherwise excluded documents were identified in the provided results.

## Limitations

1. **Small evidence base:** Only five studies and 253 participants were included, limiting precision, robustness, and the reliability of heterogeneity and publication-bias analyses.
2. **Incomplete search documentation:** Search sources, strategies, dates, language restrictions, and PRISMA screening counts were unavailable, precluding assessment of search completeness.
3. **Missing study characteristics:** Clinical and intervention details were not supplied, preventing assessment of applicability and clinical heterogeneity.
4. **Unavailable risk-of-bias assessment:** No domain-level or overall study risk-of-bias judgments were provided. The certainty of the pooled estimate could therefore not be formally graded.
5. **Extraction could not be audited:** Arm-level means, SDs, participant counts, original units, and conversion records were absent.
6. **Unresolved source-field nomenclature:** The study-level field name suggests standardized effects, whereas the confirmed synthesis metadata specifies native MD pooling. The report follows the latter but cannot reconstruct the upstream data transformation.
7. **Limited assessment of effect modification:** No subgroup or meta-regression results were available, despite potentially important differences among CKD populations and probiotic interventions.
8. **Short-term surrogate outcome:** Serum creatinine after approximately 8–24 weeks does not by itself establish durable renal benefit or improvement in patient-important outcomes.
9. **Publication-bias tests were underpowered:** Non-significant Egger’s testing and k₀=0 from trim-and-fill do not rule out selective publication with only five studies.

## Conclusion

In five studies involving 253 participants with CKD, probiotic supplementation or probiotic-containing foods produced a statistically significant reduction in end-of-treatment serum creatinine compared with placebo or no treatment. The REML pooled mean difference was −0.1530330923822796 mg/dL (95% CI −0.237 to −0.069; p=0.00038377072271947467), favoring probiotics, with no observed statistical heterogeneity (I²=0.0%; τ²=0.0).

The finding suggests a modest short-term reduction in serum creatinine, but confidence in its clinical interpretation is constrained by the small number of studies, absent risk-of-bias information, limited reporting of participant and intervention characteristics, and inability to audit the arm-level extraction. Larger, rigorously reported trials should evaluate standardized probiotic formulations, prespecified CKD subgroups, longer follow-up, safety, and patient-important renal outcomes.

## References

No bibliographic citations for the five included studies or external methodological references were supplied in the source materials. The included evidence is therefore identified in this report by the provided study labels (`study_1_R1` through `study_5_R5`).

### Generated figures

1. Forest plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
2. Cumulative meta-analysis plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
3. Effect-distribution plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
4. Bubble chart: `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`
5. Heterogeneity summary: `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| serum creatinine | 5 | Mean Difference (MD) | Yes | -0.1530 [-0.2375, -0.0686] |
