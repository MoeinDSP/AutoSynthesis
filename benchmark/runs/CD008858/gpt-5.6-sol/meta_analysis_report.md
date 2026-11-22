# Short-term adverse events after live attenuated Oka/Merck herpes zoster vaccination in adults aged 50 years or older: a systematic review and random-effects meta-analysis

## Abstract

**Background:** This review evaluated whether live attenuated Oka/Merck herpes zoster vaccine (Zostavax), compared with placebo, changes the risk that adults aged 50 years or older experience one or more adverse events of any type during the comprehensive, trial-defined short-term post-vaccination safety interval.

**Methods:** Four eligible study comparisons (7,080 participants) contributed one effect size each. The outcome included participants with at least one injection-site or systemic adverse event, whether vaccine-related or not, during the short-term safety window. A random-effects model fitted by restricted maximum likelihood (REML) pooled risk ratios (RRs). Statistical heterogeneity was assessed with Cochran’s Q, I², and τ². Small-study effects were explored with Egger’s test and trim-and-fill.

**Results:** The pooled risk ratio was 1.7903190351158367 (95% CI 1.342–2.389; p = 7.556217252202103 × 10⁻⁵; k = 4; n = 7,080). Heterogeneity was substantial (I² = 72.75%; τ² = 0.051079), although Cochran’s Q was not conventionally significant (Q = 7.618, df = 3, p = 0.0546). Under the prespecified adverse-event coding, the point estimate corresponds to a higher probability of experiencing at least one adverse event after Zostavax than after placebo. Nevertheless, the supplied analysis metadata classified favorability as “neither (essentially a tie, or a ratio measure where favourability depends on which event was counted),” and that classification is retained rather than overridden. Egger’s intercept was 0.8221 (p = 0.3552), and trim-and-fill estimated no missing studies (k₀ = 0); these analyses have very low power with only four studies.

**Conclusions:** Zostavax was associated with a statistically significant increase in the short-term risk of experiencing one or more adverse events of any type relative to placebo. The magnitude varied across studies, and the evidence is limited by substantial heterogeneity, only four comparisons, absent trial-level event counts and bibliographic details in the supplied dataset, and insufficient information for risk-of-bias or moderator analyses.

## Introduction

Herpes zoster results from reactivation of latent varicella-zoster virus, with incidence and complications increasing with age. The live attenuated Oka/Merck herpes zoster vaccine (Zostavax) was developed to reduce herpes-zoster morbidity in older adults. Because the vaccine is live attenuated and commonly produces local reactions, its short-term tolerability is an important component of benefit–risk assessment.

This review addressed the following question: among adults aged 50 years or older, what is the effect of Zostavax, compared with placebo, on the risk of experiencing one or more adverse events of any type during the comprehensive short-term post-vaccination safety interval defined by each trial report?

The eligible outcome was binary and participant-based: at least one adverse event of any type, including injection-site or systemic events and events judged vaccine-related or unrelated. Restricted safety categories—such as vaccine-related events alone, injection-site events alone, systemic events alone, serious adverse events, hospitalisations, and deaths—were outside the target outcome. Longer-term safety, herpes-zoster efficacy, post-herpetic neuralgia, and immunogenicity were also outside scope.

## Search/Screening

The supplied results identify four included studies and four effect sizes. No database names, search dates, search strings, registry searches, deduplication counts, full-text exclusion counts, or reasons for exclusion were provided. Consequently, a numerical PRISMA flow diagram and independent assessment of search completeness cannot be reconstructed without inventing information.

Eligibility was defined by the review question as follows:

- **Population:** adults aged at least 50 years.
- **Intervention:** live attenuated Oka/Merck herpes zoster vaccine administered using a licensed or trial vaccine schedule.
- **Comparator:** placebo.
- **Outcome:** one or more adverse events of any type during the comprehensive, trial-defined short-term post-vaccination interval.
- **Design requirement:** a comparative trial yielding arm-level binary safety data or an estimable risk ratio.

For a safety substudy, the intended approach was to use substudy events and denominators when the target outcome was not measured in the full trial. The intended denominator hierarchy preferred the number randomised per arm when reported. Eligible vaccine batches or doses were to be combined, while ineligible vaccine or schedule arms were to be omitted. The supplied aggregate results do not include enough arm-level information to verify these decisions independently.

## Included Studies

Four study comparisons, identified only as `study_1_R1`, `study_2_R2`, `study_3_R3`, and `study_4_R4`, were included. Their total sample size was 7,080, distributed as follows:

| Study label | Total participants contributing to the comparison |
|---|---:|
| `study_1_R1` | 54 |
| `study_2_R2` | 201 |
| `study_3_R3` | 209 |
| `study_4_R4` | 6,616 |
| **Total** | **7,080** |

The fourth comparison contributed 6,616 participants (93.45% of the combined participant count), although its statistical weight in the REML analysis cannot be determined from the supplied summary alone. Study names, countries, recruitment settings, age distributions, vaccine potency or dosing details, safety-window durations, arm-specific sample sizes, and arm-specific event counts were not provided. Accordingly, these characteristics cannot be described or checked against the eligibility rules.

No study-level risk-of-bias judgments were supplied. In particular, there was insufficient information to evaluate randomisation, allocation concealment, masking, completeness of adverse-event ascertainment, selective reporting, or differences in safety surveillance between trial arms.

## Effect Sizes

The prespecified effect measure was the **Risk Ratio (RR)**. An RR greater than 1 denotes a higher risk of experiencing at least one adverse event in the Zostavax arm, whereas an RR less than 1 denotes a lower risk.

The study-level source field was named `hedges_g`, but the meta-analysis metadata explicitly identifies the computation scale as RR, the effect measure as RR, and native pooling as used. Moreover, the supplied study values and confidence limits are internally consistent with log risk ratios: exponentiating them yields the study RRs below. They are therefore presented as analysis-scale log RRs and corresponding RRs, rather than being mislabeled as a standardized mean difference.

| Study label | n | Reported analysis-scale estimate | Reported 95% CI on analysis scale | Corresponding RR | Approximate RR 95% CI* |
|---|---:|---:|---:|---:|---:|
| `study_1_R1` | 54 | -0.124338 | -0.658 to 0.410 | 0.883 | 0.518–1.507 |
| `study_2_R2` | 201 | 0.899454 | 0.609 to 1.190 | 2.458 | 1.839–3.287 |
| `study_3_R3` | 209 | 0.632697 | 0.355 to 0.911 | 1.883 | 1.426–2.487 |
| `study_4_R4` | 6,616 | 0.532438 | 0.483 to 0.581 | 1.703 | 1.621–1.788 |

\*RRs were obtained by exponentiating the supplied analysis-scale estimates and rounded confidence limits; they are therefore approximate. The first comparison was imprecise and compatible with either a reduction or increase in risk. The other three estimates were above 1, with confidence intervals excluding 1.

The study estimates and pooled result are displayed in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The effect-size distribution is shown at `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

## Meta-Analytic Result(s)

A random-effects model fitted by restricted maximum likelihood included all four comparisons. The **pooled Risk Ratio (RR) was 1.7903190351158367** (95% CI 1.342–2.389; p = 7.556217252202103 × 10⁻⁵; k = 4; n = 7,080).

Thus, the pooled point estimate indicates that the probability of experiencing at least one adverse event during the short-term safety window was approximately 1.79 times as high after Zostavax as after placebo. The confidence interval excluded the null value of 1, and the supplied p value indicated strong statistical evidence against the null hypothesis of equal risks.

The supplied `favors` field classifies this result as **“neither (essentially a tie, or a ratio measure where favourability depends on which event was counted).”** This classification is reported exactly as provided. Separately, under the review’s explicitly defined adverse-event direction, an RR above 1 means more participants experienced adverse events in the Zostavax group; it should not be interpreted as evidence of better vaccine safety.

A cumulative meta-analysis plot was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. Because the ordering variable used for that plot was not provided, it should be regarded as descriptive rather than as evidence about chronological stability.

## Heterogeneity

Between-study heterogeneity was substantial:

- **Cochran’s Q:** 7.618 with 3 degrees of freedom
- **Q-test p value:** 0.0546
- **I²:** 72.75%
- **τ²:** 0.051079

The I² estimate indicates that a substantial proportion of the observed dispersion was attributed to between-study heterogeneity rather than sampling error. The Q test narrowly exceeded the conventional 0.05 threshold, but this should not be taken as evidence of homogeneity: with only four comparisons, Q has limited power, and both I² and τ² indicate meaningful dispersion. The estimated between-study standard deviation is approximately 0.226 on the log-RR scale (√0.051079).

Potential clinical or methodological explanations could include differences in age, vaccine potency, adverse-event definitions, active versus passive surveillance, safety-window duration, denominator choice, and whether data came from a full trial or a safety substudy. These explanations remain hypotheses because the corresponding study characteristics were not supplied.

A graphical summary of heterogeneity is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

## Moderators

No moderator coefficients, subgroup analyses, or meta-regression results were supplied. Therefore, no evidence-based conclusion can be drawn about whether effects differed by age group, sex, vaccine lot or potency, dosing schedule, follow-up duration, study size, or safety-ascertainment method.

A bubble chart was generated at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`, but the plotted moderator, coefficient, uncertainty, and model specification were not reported. The chart cannot support a formal moderator conclusion without those details. Given k = 4, any meta-regression would in any event be severely underpowered and at high risk of overfitting.

## Publication Bias

Egger’s regression produced an intercept of **0.8221** with **p = 0.3552**. Trim-and-fill estimated **k₀ = 0** missing studies. The supplied interpretation classified publication-bias risk as low and reported no evidence of funnel-plot asymmetry or small-study effects.

These findings require substantial caution. With only four studies, Egger’s test has very low power, funnel-plot asymmetry is difficult to distinguish from chance or genuine heterogeneity, and trim-and-fill is unstable. A non-significant Egger test therefore does not establish the absence of reporting bias. The trim-and-fill output also contained an adjusted working-scale value of **0.5347**, but its field labeling and relationship to the RR model were not sufficiently documented for substantive interpretation; because k₀ was zero, no imputed studies were added.

## Discussion

### Principal findings

Across four comparisons involving 7,080 participants, Zostavax was associated with a higher short-term risk of experiencing one or more adverse events of any type than placebo. The pooled RR was 1.7903190351158367, and its 95% CI of 1.342–2.389 excluded 1. Three study estimates indicated increased risk, while the smallest study was inconclusive. The combined evidence was heterogeneous (I² = 72.75%), indicating that the magnitude of the association varied beyond what would ordinarily be expected from sampling error alone.

### Clinical interpretation

The outcome was deliberately broad. It captured whether a participant had at least one event of any type during a short safety interval, regardless of whether the event was local or systemic and regardless of whether investigators considered it vaccine-related. Such a composite is useful for describing overall short-term reactogenicity and tolerability, but it does not indicate event severity, duration, preventability, or clinical importance. An increase in this endpoint may be driven mainly by transient injection-site reactions rather than serious systemic harm; the supplied data cannot distinguish those possibilities.

The result must not be extrapolated to serious adverse events, hospitalisation, mortality, longer-term safety, vaccine efficacy, prevention of post-herpetic neuralgia, or immunogenicity. Those outcomes were outside the review question.

### Consistency and robustness

The large fourth study produced a comparatively precise estimate, while the smallest study was imprecise. Nevertheless, the random-effects model appropriately allowed true effects to vary across studies. The substantial I² and non-zero τ² mean that the pooled RR should be interpreted as an average across potentially different trial settings rather than as a universal effect applicable to every population or safety-surveillance system.

Formal publication-bias tests did not identify asymmetry, but this does not materially strengthen confidence because only four studies were available. Robustness also cannot be evaluated through influence analyses, leave-one-out analyses, alternative τ² estimators, Hartung–Knapp adjustment, or prediction intervals because these outputs were not provided.

## Data Quality & Validation Notes

Several validation issues in the supplied dataset affect interpretation:

1. The study-level numerical field was labeled `hedges_g`, whereas the meta-analysis metadata states that the native effect measure and computation scale were RR. The study values appear internally consistent with log RRs, but the field-name mismatch should be corrected in the source dataset.
2. The supplied `favors` field classifies the pooled result as favoring neither arm because event direction was considered ambiguous. This conflicts with the review question’s explicit definition of the event as an adverse outcome, under which RR > 1 means more adverse events with Zostavax. The formal supplied favorability classification has been retained, while the adverse-event direction has been explained separately.
3. Arm-level event counts and denominators were unavailable, preventing verification of the RRs, denominator hierarchy, handling of complete-case safety populations, and aggregation of eligible vaccine batches or doses.
4. Study citations and descriptive characteristics were unavailable, preventing checks for duplicate reports, overlapping populations, safety substudies, ineligible schedules, or multiple publications from the same trial.
5. The trim-and-fill output reported k₀ = 0 but also supplied a working-scale estimate of 0.5347 that does not transparently map to the reported pooled RR. It was therefore not treated as a confirmed adjusted RR.
6. No documents excluded as reviews or duplicates, unclassifiable outcomes, or reports excluded to avoid double-counting were identified in the supplied context. This reflects missing screening documentation rather than confirmation that none existed.

## Limitations

This synthesis has several important limitations:

- Only four comparisons were available, limiting precision in heterogeneity, publication-bias, and moderator assessments.
- Statistical heterogeneity was substantial (I² = 72.75%).
- The fourth study accounted for most participants, potentially making the evidence base highly dependent on one trial, although random-effects weights were not supplied.
- No arm-specific event counts or denominators were provided, so absolute risks, risk differences, numbers needed to harm, and direct recalculation of study RRs were impossible.
- Trial names, citations, settings, participant characteristics, vaccine schedules, and safety-window definitions were absent.
- No risk-of-bias assessment was available.
- The broad composite endpoint combines adverse events with potentially very different clinical significance.
- The safety intervals were trial-defined and may not have been identical across studies.
- Egger’s test and trim-and-fill are unreliable with k = 4.
- No prediction interval was supplied, so the expected range of effects in a new setting cannot be quantified.
- The analysis does not address serious or long-term harms and should not be used as a complete vaccine benefit–risk evaluation.

## Conclusion

In four placebo-controlled comparisons including 7,080 adults aged 50 years or older, live attenuated Oka/Merck herpes zoster vaccine was associated with a statistically significant increase in the short-term risk of experiencing one or more adverse events of any type. The pooled Risk Ratio was **1.7903190351158367** (95% CI **1.342–2.389**; p = **7.556217252202103 × 10⁻⁵**). The effect varied substantially across studies (**I² = 72.75%; τ² = 0.051079**). Although formal analyses did not detect publication bias, they were underpowered. Interpretation should therefore emphasize that this is a broad, short-term tolerability outcome and that the available summary data do not identify event severity, absolute excess risk, or longer-term safety.

## References

Complete bibliographic details were not included in the supplied results and therefore cannot be reconstructed reliably. The evidence base comprised four anonymized reports:

1. `study_1_R1` (n = 54).
2. `study_2_R2` (n = 201).
3. `study_3_R3` (n = 209).
4. `study_4_R4` (n = 6,616).

No external references have been invented or added.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| one or more adverse events | 4 | Risk Ratio (RR) | Yes | 1.7903 [1.3418, 2.3888] |
