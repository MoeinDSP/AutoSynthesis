# Bupropion for Smoking Abstinence Among Hospitalised Adults Who Smoke: A Systematic Review and Random-Effects Meta-analysis

## Abstract

**Background:** Hospitalisation provides an opportunity to initiate smoking-cessation treatment. This review evaluated whether bupropion improves longer-term smoking abstinence among hospitalised adults who smoke.

**Methods:** Eligible studies were randomised controlled trials comparing bupropion with placebo or no bupropion/usual care, without an unequal pharmacological co-intervention. The target outcome was the strictest available smoking-abstinence measure at each trial’s single longest follow-up of at least six months, with all randomised participants retained in the denominator and losses to follow-up classified as smoking. Arm-level risks were to be pooled as a random-effects risk ratio using restricted maximum likelihood (REML). The supplied dataset contained four studies, but only three effect sizes were included in the meta-analysis; participant-level extraction details and the reason the fourth study was not pooled were not provided.

**Results:** Three studies comprising 484 randomised participants contributed to the quantitative synthesis. The pooled Risk Ratio (RR) was **1.0509027314129569** (95% CI **0.721 to 1.532**; p = **0.7962966580070138**). The supplied favourability classification was **neither arm**, indicating an essentially null result. Heterogeneity was low to modest (Q = **2.424**, p = **0.2976**; I² = **15.92%**; τ² = **0.018879**). Egger’s intercept was **0.9522** (p = **0.0364**), and trim-and-fill estimated two potentially missing studies; the supplied assessment therefore classified publication-bias risk as high. These diagnostics are highly unstable with only three studies.

**Conclusions:** The available meta-analysis did not show evidence that bupropion increased long-term smoking abstinence among hospitalised adults compared with placebo or no bupropion/usual care. The confidence interval remained compatible with both clinically meaningful benefit and harm. Interpretation is limited by the small evidence base, possible small-study effects, and the absence of study-level arm counts, abstinence definitions, validation methods, follow-up times, and screening details in the supplied results.

## Search/Screening

The review question was defined using the following eligibility framework:

- **Population:** adults who smoked and were hospitalised at enrolment or treatment initiation.
- **Intervention:** bupropion; counselling or another nonpharmacological co-intervention was permissible only when delivered comparably in both groups.
- **Comparator:** placebo or no bupropion/usual care, without nicotine replacement therapy, varenicline, or another smoking-cessation medication given unequally between groups.
- **Design:** randomised controlled trials.
- **Outcome:** smoking abstinence at the single longest reported follow-up occurring at least six months after randomisation. Outcomes at three months or earlier were ineligible.
- **Outcome hierarchy:** sustained or continuous abstinence was preferred to point-prevalence abstinence, and biochemical validation was preferred when available. Reduced smoking was not considered abstinence.
- **Analysis population:** all randomised participants were to remain in their assigned-arm denominator, with participants lost to follow-up classified as smoking.

The supplied pipeline summary identified **4 studies**, of which **3 supplied effect sizes** for meta-analysis. Thus, the quantitative synthesis included three studies and excluded or otherwise did not pool one identified study. No study-level exclusion reason was supplied, so it is not possible to determine whether the fourth study lacked an eligible follow-up, had an ineligible comparator, duplicated another report, or had insufficient outcome data.

Database names, search strings, coverage dates, date of the final search, language restrictions, deduplication counts, numbers screened at title/abstract and full-text stages, reviewer procedures, protocol registration, and a PRISMA flow diagram were not included in the context data. These items therefore cannot be reconstructed without risking fabrication. The report should consequently be regarded as a synthesis of the provided analytic results rather than a fully auditable de novo systematic search.

## Included Studies

Three randomised comparisons, with **484 participants in total**, contributed to the pooled analysis. A fourth study appeared in the pipeline summary but did not contribute an effect size.

The supplied study labels and statistical records were:

| Study label | Participants | Supplied effect-scale estimate | Supplied 95% CI |
|---|---:|---:|---:|
| study_1_R1 | 151 | -0.056391 | -0.375 to 0.263 |
| study_2_R2 | 248 | 0.244420 | -0.005 to 0.494 |
| study_4_R4 | 85 | -0.252746 | -0.680 to 0.174 |

The individual-study field was labelled `hedges_g` in the source data, although the meta-analysis was explicitly configured and reported as a native **Risk Ratio (RR)** analysis. Because individual arm-level event counts were not supplied, these study-specific records cannot be independently verified or safely relabelled as either RRs or log RRs. Accordingly, they are reproduced above only as supplied effect-scale estimates and are not interpreted as Hedges’ g.

No trial names, publication years, hospital settings, clinical admission categories, bupropion doses or durations, counselling protocols, exact follow-up times, arm-level randomised totals, numbers abstinent, abstinence definitions, or biochemical-validation methods were provided. Consequently, adherence to the intended outcome hierarchy and intention-to-treat smoking-trial rule could not be independently checked at study level.

## Effect Sizes

The prespecified effect measure was the **Risk Ratio (RR)** based on arm-level abstinence risks. An RR greater than 1 would ordinarily indicate more abstinence with bupropion, whereas an RR less than 1 would indicate more abstinence with control. For the pooled output, however, the supplied `favors` field classified the result as **“neither (essentially a tie, or a ratio measure where favourability depends on which event was counted).”** In accordance with that supplied classification, the pooled estimate is described as favouring neither arm rather than assigning benefit from its numerical sign alone.

The analysis used native RR pooling (`native_pooling_used = true`), so the summary is a confirmed ratio-scale result rather than a standardised fallback. The source also recorded a measure conflict: the user-specified RR was retained even though the underlying paper or papers reportedly presented odds ratios. Without events and randomised denominators, the requested RRs cannot be independently reconstructed, and odds ratios should not be treated as interchangeable with RRs when outcomes are not rare.

A forest plot is available at:

- `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`

The supplied additional visualisations are:

- Cumulative plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
- Effect distribution: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
- Bubble chart: `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`
- Heterogeneity summary: `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

## Meta-Analytic Result(s)

A random-effects model estimated by **restricted maximum likelihood (REML)** pooled **3 studies** and **484 participants**. The pooled **Risk Ratio (RR)** was:

> **RR = 1.0509027314129569 (95% CI 0.721 to 1.532; p = 0.7962966580070138).**

The confidence interval included the null value of 1, and the test of the pooled effect was not statistically significant. Based on the supplied favourability field, the result favoured **neither arm** and was essentially a tie. The interval was wide enough to remain compatible with appreciably lower or higher abstinence under bupropion, so the result should not be interpreted as demonstrating equivalence or absence of any clinically important effect.

Only the eligible long-term abstinence outcome was pooled. No short-term cessation, smoking reduction, adverse-event, cardiovascular-event, withdrawal-symptom, or other clinical outcome was combined with this analysis.

## Heterogeneity

Observed between-study heterogeneity was low to modest:

- **Cochran’s Q = 2.424** with **p = 0.2976**;
- **I² = 15.92%**;
- **τ² = 0.018879**.

The Q test did not provide evidence against homogeneity, although it has very low power with only three studies. The I² estimate suggests that a relatively small proportion of observed variability was attributable to between-study heterogeneity rather than sampling error. Nevertheless, both I² and τ² are imprecisely estimated in such a small meta-analysis. The random-effects model was appropriate given plausible clinical variation in hospital populations, admission diagnoses, behavioural support, treatment implementation, abstinence definitions, and follow-up timing.

A graphical summary of heterogeneity is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

## Moderators

No subgroup analysis or meta-regression result was supplied. Potential moderators—including admission diagnosis, baseline nicotine dependence, bupropion dose and duration, counselling intensity, placebo versus usual-care control, abstinence definition, biochemical validation, and length of follow-up—could not be examined.

With only three pooled studies, formal moderator analyses would in any event be underpowered and prone to false-positive or unstable estimates. The bubble chart at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` should therefore be considered descriptive rather than evidence of a moderator effect.

## Publication Bias

The supplied publication-bias diagnostics were:

- **Egger’s intercept = 0.9522**;
- **Egger’s test p = 0.0364**;
- **Trim-and-fill estimated missing studies (k₀) = 2**;
- **Trim-and-fill output = 0.2444** on the source’s internal effect scale;
- **Overall supplied risk classification: high**.

The statistically significant Egger test suggests funnel-plot asymmetry or small-study effects, and the trim-and-fill procedure estimated two potentially missing studies. However, publication-bias tests are not reliable with only three observed studies. Funnel asymmetry may reflect chance, clinical heterogeneity, selective outcome reporting, or other small-study effects rather than publication bias alone. Likewise, trim-and-fill is highly unstable with so few studies. The value **0.2444** was labelled `trim_fill_g` rather than confirmed as a Risk Ratio; it therefore should not be interpreted as an adjusted RR or as a definitive bias-corrected treatment effect.

On balance, the supplied high-risk classification should be reported, but the numerical diagnostics should be treated as exploratory. The pooled estimate warrants caution rather than a mechanical publication-bias adjustment.

## Discussion

This random-effects synthesis of three randomised trials found no statistically detectable improvement in long-term smoking abstinence with bupropion among hospitalised adults who smoke. The point estimate was close to the null, and the supplied output classified it as favouring neither intervention. The 95% confidence interval was broad, extending from **0.721 to 1.532**, and therefore did not exclude either a potentially important reduction or a potentially important increase in abstinence.

Hospitalisation can create a “teachable moment,” provide temporary smoking restriction, and facilitate initiation of behavioural and pharmacological treatment. At the same time, hospital populations are clinically heterogeneous, and post-discharge adherence to medication and counselling may be difficult. These considerations may contribute to differences across trials even though the statistical estimate of heterogeneity was modest.

The principal strength of the intended review method is its clinically focused outcome definition: one long-term abstinence endpoint per trial, prioritising sustained or continuous abstinence and biochemical validation, with all randomised participants retained and losses treated as smoking. Restricting eligible contrasts to groups that differed only in bupropion was also designed to isolate the medication’s incremental effect. However, the supplied aggregate results did not include enough study-level information to verify that these rules were applied consistently.

The discrepancy between the explicitly requested RR and reports said to present odds ratios is important. An RR is directly interpretable as a ratio of abstinence probabilities, while an odds ratio may appear farther from the null when abstinence is common. The native pooled output was identified as an RR, but the absence of arm-level events and randomised totals prevents independent reproduction. Publication-bias signals further reduce confidence, although those signals themselves are unreliable in a three-study meta-analysis.

Overall, the evidence is best characterised as **inconclusive rather than evidence of no effect**. A well-powered, transparently reported trial could materially change the estimate.

## Data Quality & Validation Notes

Although no formal `validation_flags` object was supplied, several data-quality issues are evident in the provided results:

1. The pipeline identified **4 studies**, but only **3 effect sizes** were pooled; no reason was supplied for omission of the fourth study.
2. Arm-level abstinence events and randomised denominators were absent, preventing verification of the RR calculations and the intention-to-treat assumption that losses were smokers.
3. Exact abstinence definitions, biochemical-validation methods, and follow-up times were not supplied, preventing confirmation that the strictest outcome at the longest eligible follow-up was used.
4. Individual effects were stored under a field labelled `hedges_g`, while the meta-analysis was specified as a native Risk Ratio analysis. Those study-level values should not be described as Hedges’ g without further clarification.
5. The analysis record notes that source paper(s) explicitly reported odds ratios, whereas the requested and pooled measure was RR. Reconstruction from raw arm counts is needed to validate this conversion.
6. The trim-and-fill result was not clearly labelled on the RR scale and therefore cannot be presented as a bias-adjusted RR.

## Limitations

The review has several important limitations:

- Only three studies and 484 participants contributed to the pooled result, limiting precision and robustness.
- Study identities and bibliographic details were unavailable, so trial characteristics and possible overlapping populations could not be checked.
- Search and screening methods were not provided, precluding assessment of search completeness and full PRISMA flow reporting.
- The reason that one of four identified studies did not enter the synthesis was not documented.
- Arm-level event counts were unavailable, so ITT denominators, conversion of percentages to counts, treatment-arm assignment, and the pooled RR could not be independently reproduced.
- Outcome definitions, validation procedures, and eligible follow-up durations were unavailable; outcome-selection rules could not be audited.
- No trial-level risk-of-bias assessment was supplied.
- Statistical heterogeneity estimates and publication-bias diagnostics are unstable when based on only three studies.
- No moderator analysis was feasible, leaving potentially important clinical variation unexplained.
- The measure discrepancy between source-reported odds ratios and the requested RRs creates an additional validation concern.

## Conclusion

In three randomised trials including 484 participants, bupropion did not produce a statistically significant improvement in smoking abstinence at the longest follow-up of at least six months compared with placebo or no bupropion/usual care. The REML random-effects pooled **Risk Ratio was 1.0509027314129569 (95% CI 0.721 to 1.532; p = 0.7962966580070138)**, with low-to-modest estimated heterogeneity (**I² = 15.92%**). The supplied classification indicated that the result favoured neither arm.

Because the confidence interval was wide, the evidence does not establish equivalence and cannot exclude clinically meaningful benefit or harm. The very small evidence base, high supplied publication-bias risk, missing study-level extraction details, and unresolved effect-measure discrepancy substantially limit confidence. Additional adequately powered randomised trials with transparent reporting of randomised denominators, abstinence events, sustained and biochemically validated outcomes, and long-term follow-up are needed.

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71.
2. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1-48. doi:10.18637/jss.v036.i03.
3. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine*. 2002;21(11):1539-1558. doi:10.1002/sim.1186.
4. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629-634. doi:10.1136/bmj.315.7109.629.
5. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455-463. doi:10.1111/j.0006-341X.2000.00455.x.

*Bibliographic details for the four identified smoking-cessation studies were not included in the supplied context and therefore could not be listed without fabrication.*

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| smoking abstinence | 3 | Risk Ratio (RR) | Yes | 1.0509 [0.7209, 1.5321] |
| | | ⚠ user requested RR, but the paper(s) explicitly report OR -- user request kept as authoritative | | |
