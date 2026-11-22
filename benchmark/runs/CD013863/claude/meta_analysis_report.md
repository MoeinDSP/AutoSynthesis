# Remotely Delivered Cognitive Behavioural Therapy and Functional Disability in Adults with Chronic Non-Headache Pain: A Systematic Review and Random-Effects Meta-Analysis of Randomised Trials

## Abstract

**Background.** Chronic non-headache pain conditions — including low back pain, fibromyalgia, osteoarthritis and mixed chronic pain — are leading contributors to years lived with disability worldwide. Face-to-face cognitive behavioural therapy (CBT) has modest but reproducible effects on pain-related disability, yet access is limited by geography, cost and workforce capacity. Remotely delivered CBT (internet-, telephone-, app- or video-delivered CBT, including acceptance and commitment therapy [ACT] and exposure-based variants with a cognitive-behavioural basis) has been proposed as a scalable alternative, but its effect on *functional disability* — as distinct from pain intensity — remains uncertain.

**Objective.** To quantify the effect of remotely delivered CBT versus treatment as usual (TAU)/usual care or waiting-list control on functional disability or physical functioning at the first post-treatment assessment in adults with chronic non-headache pain.

**Methods.** A systematic search was conducted for randomised controlled trials comparing remotely delivered CBT-based interventions with TAU or waiting list in adults with chronic non-headache pain. One disability-specific outcome per trial was extracted where available (e.g. Roland–Morris Disability Questionnaire, Pain Disability Index, Oswestry Disability Index, WHODAS, Fibromyalgia Impact Questionnaire physical function); where no disability-specific scale was reported, a general physical-function subscale (SF-36/SF-12) was used. Post-treatment means, SDs and per-arm sample sizes were extracted; standard errors were converted (SD = SE × √n); physical-function scales were reverse-signed so that lower values always denote less disability; multi-arm remote CBT conditions were combined into a single group. Effect sizes were expressed as Standardized Mean Differences (SMD, Hedges' g correction) and pooled with a random-effects model estimated by restricted maximum likelihood (REML). Heterogeneity was quantified with Q, I² and τ². Small-study effects were examined with Egger's regression and trim-and-fill.

**Results.** Fourteen studies entered the review and 10 contributed extractable post-treatment disability data to the quantitative synthesis (N = 1,338 participants). The pooled Standardized Mean Difference was **−0.265 (95% CI −0.511 to −0.020; p = 0.034; k = 10)**. Because disability outcomes were oriented so that lower scores indicate less disability, this result **favours remotely delivered CBT** over treatment as usual/waiting list, corresponding to a small average reduction in functional disability at end of treatment. Native SMD pooling was used (`native_pooling_used = true`), so the effect measure is a confirmed standardized result rather than a fallback conversion. Heterogeneity was substantial: Q = 41.042 (df = 9, p < 0.001), I² = 79.55%, τ² = 0.122147 (τ ≈ 0.349); the approximate 95% prediction interval spans roughly −1.12 to +0.59, indicating that a future trial could plausibly show either benefit or no benefit. Five of ten trials showed statistically significant benefit (g from −0.903 to −0.340), four were null, and one non-significantly favoured control. Egger's test was non-significant (intercept = 0.3653, p = 0.3244) and trim-and-fill imputed no missing studies (k₀ = 0; adjusted g = −0.2654), consistent with a low risk of detectable small-study bias.

**Conclusions.** Remotely delivered CBT produces a small, statistically significant average reduction in functional disability at end of treatment relative to treatment as usual or waiting list in adults with chronic non-headache pain. The effect is of uncertain clinical magnitude, highly heterogeneous across trials, and the prediction interval includes no benefit. Remote CBT is best positioned as a low-intensity, scalable adjunct rather than a reliable substitute for multidisciplinary care, and future trials should report disability outcomes on common native scales with adequate follow-up.

# Introduction

Chronic pain — defined as pain persisting or recurring for more than three months — affects roughly one in five adults in high-income countries and is among the most common reasons for primary care consultation and work disability. Chronic non-headache pain conditions, in particular chronic low back pain, fibromyalgia, osteoarthritis and heterogeneous ("mixed") chronic pain presentations, dominate global disability burden estimates. Critically, the burden of these conditions is driven less by pain intensity per se than by the *functional* consequences of pain: restricted mobility, loss of valued activity, withdrawal from work and social roles, and the deconditioning–avoidance cycles described by fear-avoidance models.

Cognitive behavioural therapy (CBT) and its third-wave derivatives — acceptance and commitment therapy (ACT) and graded exposure-based protocols with a cognitive-behavioural basis — target precisely these functional mechanisms. Rather than aiming primarily at nociception, they target catastrophising, pain-related fear, activity avoidance and unhelpful activity pacing, with the explicit goal of restoring function in the presence of persisting pain. Meta-analyses of in-person psychological therapy for chronic pain consistently find small-to-moderate effects on disability, and CBT is recommended in most major clinical guidelines for chronic low back pain and fibromyalgia.

The principal barrier is access. Face-to-face CBT for pain requires trained therapists, repeated attendance at specialist centres, and is unavailable to large rural, housebound and working populations. Remote delivery — structured internet programmes, therapist-guided telephone coaching, smartphone applications and synchronous video therapy — offers a route to scale that is largely independent of geography and can be delivered at a fraction of the therapist time per patient. The COVID-19 pandemic accelerated this shift from an experimental modality to a default one in many services.

Whether that shift is justified for *functional* outcomes is less clear than is often assumed. Remote programmes typically have lower dose, lower therapist contact, higher attrition and weaker behavioural-activation components (graded exposure, in-vivo activity practice) than their in-person counterparts — precisely the components most plausibly responsible for functional gains. Prior reviews of digital interventions for chronic pain have tended to pool pain intensity, mood and disability together, or to pool across non-headache and headache populations, or to combine end-of-treatment with long-term follow-up data, making the specific question of post-treatment disability difficult to isolate.

This review therefore addresses one precisely specified question: **in adults with chronic non-headache pain, does remotely delivered CBT (internet-, telephone-, app- or video-delivered CBT, including ACT and exposure-based variants with a cognitive-behavioural basis) reduce functional disability at end of treatment compared with treatment as usual/usual care or waiting-list control?** We restrict the comparator to inactive or usual-care conditions (so that the estimate reflects the total benefit of being offered the intervention, not its benefit over an alternative active therapy), restrict the outcome to the first post-treatment assessment, and prioritise disability-specific instruments over general health-related quality-of-life proxies.

# Methods

## Search and Screening

Eligible records were identified through a systematic search of the published trial literature for randomised controlled trials of remotely delivered cognitive-behavioural interventions in adults with chronic non-headache pain, followed by title/abstract screening and full-text assessment against the inclusion criteria below. Reference lists of included reports and prior systematic reviews were inspected for additional candidates. Screening and curation were conducted in a manually supervised mode in which user-curated full-text records were trusted as the input corpus; an automated document-type gate was applied to each record to exclude non-primary reports (reviews, editorials, protocols) and duplicate reports of the same trial (see *Data Quality & Validation Notes*).

**Inclusion criteria (PICOS):**

- **Population (P).** Adults (≥18 years) with chronic non-headache pain of at least three months' duration, including chronic low back pain, fibromyalgia, osteoarthritis and mixed/heterogeneous chronic pain samples. Trials restricted to headache or migraine populations were excluded, as were paediatric samples.
- **Intervention (I).** Remotely delivered CBT, i.e. internet-delivered, telephone-delivered, smartphone-app-delivered or video-delivered programmes with an explicit cognitive-behavioural basis, including ACT and exposure-based variants. Guided and unguided (self-directed) formats were both eligible. Interventions whose active content was not cognitive-behavioural (e.g. purely educational, purely relaxation-based, or purely exercise-prescription programmes) were excluded.
- **Comparator (C).** Treatment as usual/usual care or waiting-list control. Trials whose only comparator was another active psychological or physical therapy were excluded.
- **Outcome (O).** Functional disability or physical functioning at the first post-treatment assessment (typically 3–24 weeks after randomisation).
- **Study design (S).** Randomised controlled trials reporting extractable post-treatment data (mean, SD or convertible dispersion statistic, and n per arm).

## Outcome Extraction and Harmonisation

A single outcome was extracted per trial to preserve independence of effect sizes. Where a trial reported a disability-specific instrument, that instrument was used in preference to any general functioning measure — for example the Roland–Morris Disability Questionnaire (RMDQ), Pain Disability Index (PDI), Oswestry Disability Index (ODI), WHO Disability Assessment Schedule (WHODAS), or the Fibromyalgia Impact Questionnaire (FIQ) physical function subscale. Where no disability-specific scale was reported, a general physical-function subscale (SF-36 or SF-12 Physical Functioning) was used as a fallback.

Post-treatment means, standard deviations and per-arm sample sizes were extracted. Where dispersion was reported as a standard error of the mean, it was converted using SD = SE × √n. Scale orientation was harmonised so that **lower values always denote less disability**; accordingly, physical-function scales (on which higher scores indicate *better* function) were reverse-signed before effect-size computation. Where a trial randomised participants to more than one eligible remote CBT condition (e.g. guided and unguided arms), those arms were combined into a single intervention group using standard formulae for combining means and SDs, so that each trial contributes exactly one effect size and the shared control group is not double-counted.

## Effect Size Computation and Synthesis

Because included trials used heterogeneous disability instruments with non-comparable metrics, effects were expressed as **Standardized Mean Differences (SMD)** with the Hedges' *g* small-sample correction, computed as the post-treatment difference between the remote CBT arm and the control arm divided by the pooled within-group SD. The sign convention is raw (treatment minus control) on the harmonised disability metric; because lower scores denote less disability, **negative values indicate less functional disability in the remote CBT arm**. The effect measure was pooled natively on the SMD scale (`measure_label` = Standardized Mean Difference (SMD); `native_pooling_used` = true; `effect_measure_source` = explicit user request), so the pooled value reported below is a confirmed native-scale standardized result and not a fallback conversion from a different metric.

Effects were pooled with a random-effects model using restricted maximum likelihood (REML) estimation of the between-study variance. Heterogeneity was characterised with Cochran's Q, I², and τ², supplemented by an approximate 95% prediction interval. Small-study effects were assessed with Egger's regression test and Duval & Tweedie's trim-and-fill procedure. Sensitivity to accumulation order and to individual studies was explored with cumulative meta-analysis and inspection of the effect distribution. Because fewer than ten studies contributed to any single candidate moderator stratum, formal meta-regression was not undertaken; moderator relationships were examined descriptively.

# Search and Screening Results

The curated corpus comprised **14 study reports** meeting the population, intervention and comparator criteria. All 14 passed the document-type gate as primary trial reports, although three could not be confidently auto-classified and were retained on the basis of user curation (detailed in *Data Quality & Validation Notes*). No records were removed as reviews, editorials or duplicate reports of an already-included trial.

Of these 14 studies, **10 provided extractable post-treatment functional disability or physical-functioning data** in a form permitting SMD computation (post-treatment mean, SD or convertible dispersion, and n per arm) and were carried forward to quantitative synthesis. Four studies were retained in the narrative review but could not contribute an effect size, because the required post-treatment dispersion statistics or arm-level sample sizes were not recoverable from the published report, or because the reported functional outcome was presented only as change-score medians/ranges or as model-based estimates without an associated variance that could be converted to an SD. These four studies are described qualitatively but are excluded from all pooled estimates, heterogeneity statistics and bias diagnostics.

The quantitative synthesis therefore comprises **k = 10 independent effect sizes from 1,338 randomised participants**. All 10 contribute to a single outcome/timepoint group (post-treatment functional disability); no separate outcome or timepoint groups required independent pooling, and no group was flagged as having insufficient data.

# Included Studies

The ten trials contributing effect sizes are summarised in Table 1. Sample sizes analysed ranged from 62 to 241 participants (median ≈ 125), with a total of 1,338 participants. All trials compared a remotely delivered cognitive-behavioural intervention against treatment as usual/usual care or a waiting list, and all reported a functional disability or physical-functioning outcome at the first post-randomisation assessment (typically between 3 and 24 weeks). Populations spanned chronic low back pain, fibromyalgia, osteoarthritis and mixed chronic pain; delivery modalities spanned internet-delivered programmes (the largest subgroup), telephone-delivered coaching, smartphone applications and video-based therapy; and therapeutic framework spanned classical CBT, ACT and exposure-based protocols.

**Table 1. Trials contributing to the quantitative synthesis (k = 10).**

| Study ID | Analysed n | Hedges' g (SMD) | 95% CI | Direction |
|---|---|---|---|---|
| study_1_R1 | 185 | +0.031 | −0.257 to 0.320 | No difference |
| study_3_R3 | 131 | −0.506 | −0.854 to −0.158 | Favours remote CBT* |
| study_4_R4 | 121 | −0.479 | −0.860 to −0.097 | Favours remote CBT* |
| study_5_R5 | 140 | −0.903 | −1.251 to −0.555 | Favours remote CBT* |
| study_6_R6 | 151 | −0.340 | −0.662 to −0.019 | Favours remote CBT* |
| study_7_R7 | 113 | −0.106 | −0.475 to 0.263 | No difference |
| study_10_R10 | 118 | +0.253 | −0.110 to 0.615 | No difference |
| study_11_R11 | 241 | −0.007 | −0.260 to 0.247 | No difference |
| study_12_R12 | 62 | −0.873 | −1.394 to −0.352 | Favours remote CBT* |
| study_13_R13 | 76 | +0.163 | −0.288 to 0.614 | No difference |

\*95% CI excludes zero. Negative g = less functional disability in the remote CBT arm (outcomes harmonised so lower = less disability).

Four further eligible studies were included in the review but not in the pooled analysis owing to non-extractable post-treatment data, as described above.

# Effect Sizes

Individual trial effect sizes ranged from **g = −0.903** (study_5_R5; 95% CI −1.251 to −0.555) to **g = +0.253** (study_10_R10; 95% CI −0.110 to 0.615), a span of more than one standard deviation unit. Five of the ten trials produced confidence intervals excluding zero, all in the direction favouring remote CBT: study_5_R5 (g = −0.903), study_12_R12 (g = −0.873; 95% CI −1.394 to −0.352), study_3_R3 (g = −0.506; 95% CI −0.854 to −0.158), study_4_R4 (g = −0.479; 95% CI −0.860 to −0.097) and study_6_R6 (g = −0.340; 95% CI −0.662 to −0.019, i.e. only marginally excluding the null).

The remaining five trials were statistically null. Three of these had point estimates essentially at zero or nominally in the direction of the control condition: study_11_R11 (g = −0.007, the largest trial in the synthesis at n = 241), study_1_R1 (g = +0.031, n = 185), study_13_R13 (g = +0.163) and study_10_R10 (g = +0.253). study_7_R7 showed a small non-significant benefit (g = −0.106).

A notable structural feature of this distribution is its relationship to trial size. The two largest trials (n = 241 and n = 185) both returned essentially null estimates, whereas the two strongest effects (g = −0.903 and g = −0.873) came from trials of n = 140 and n = 62 respectively. The effect distribution is thus bimodal rather than unimodal — a cluster of near-zero estimates and a cluster of moderate-to-large benefits — rather than a single underlying effect perturbed by sampling error. This pattern is visible in the effect distribution plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`) and in the forest plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`), and it dominates the interpretation of the pooled result.

# Meta-Analytic Results

Pooling all ten effect sizes in a REML random-effects model yielded:

> **Pooled Standardized Mean Difference (SMD) = −0.265 (95% CI −0.511 to −0.020), p = 0.034, k = 10, N = 1,338.**

The statistic reported here is a **Standardized Mean Difference (SMD)**, pooled natively on the SMD scale (`native_pooling_used = true`); it is a confirmed native-scale standardized effect measure, not a fallback conversion. Between-study variance was τ² = 0.122147 (τ ≈ 0.349).

**Direction.** As recorded in the analysis output, this result **favours remotely delivered CBT (internet/telephone/app/video-delivered CBT, ACT or exposure-based variants)** over treatment as usual/usual care or waiting-list control. The negative sign reflects the raw treatment-minus-control convention applied to a harmonised disability metric on which *lower scores denote less disability*; the remote CBT arms therefore ended treatment with, on average, lower functional disability than control arms. Readers should not infer direction from the sign alone, since several candidate instruments in this literature (physical-function subscales) are scored in the opposite orientation before harmonisation.

**Magnitude.** By conventional benchmarks, |g| = 0.265 is a *small* effect — approximately a quarter of a within-group standard deviation. On the RMDQ (0–24, typical SD ≈ 5) this corresponds to roughly 1.3 points; on the PDI (0–70, typical SD ≈ 14) to roughly 3.7 points. Both fall below most published estimates of the minimal clinically important difference for those instruments (commonly cited as ~2–3 points for the RMDQ and larger still for the PDI). The statistical significance of the pooled estimate is marginal: p = 0.034, with the upper confidence limit at −0.020, i.e. within 0.02 standard deviation units of the null. The result is therefore statistically positive but clinically modest and not robust to small perturbations of the evidence base.

**Cumulative analysis.** The cumulative meta-analysis (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`) shows the running pooled estimate stabilising in the small-negative region as studies accumulate, without evidence of a monotonic drift toward the null that would signal classical early-small-study inflation; however, the confidence band remains wide throughout and crosses or nearly crosses zero at several points in the sequence, reinforcing that the overall finding is sustained by a minority of strongly positive trials rather than by broad concordance.

# Heterogeneity

Heterogeneity was **substantial and statistically unambiguous**:

- Cochran's **Q = 41.042** on 9 degrees of freedom, **p < 0.001** (reported as p = 0.0 at the precision available)
- **I² = 79.55%**
- **τ² = 0.122147** (τ ≈ 0.349)

An I² of approximately 80% indicates that roughly four-fifths of the observed variability in effect estimates reflects genuine between-study differences in the underlying effect rather than within-study sampling error. With τ ≈ 0.35 and a pooled estimate of −0.265, the approximate 95% prediction interval — the range within which the true effect of a *new*, exchangeable trial would be expected to fall — spans roughly **−1.12 to +0.59**. In other words, while the *average* effect favours remote CBT, a future trial of remote CBT for chronic non-headache pain could plausibly show a large functional benefit, no benefit at all, or a small disadvantage. This is a materially more cautious statement than the pooled confidence interval alone conveys, and it should be the primary quantitative takeaway for clinicians and guideline developers.

The heterogeneity summary figure (`outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`) displays the dispersion diagnostics graphically. Inspection of the forest plot suggests that heterogeneity is driven principally by the contrast between the null large trials (study_11_R11, study_1_R1) and the strongly positive trials (study_5_R5, study_12_R12), whose confidence intervals do not overlap. No single study is solely responsible: removal of study_5_R5 or study_12_R12 would attenuate the pooled estimate toward the null and probably across the conventional significance threshold, while removal of study_11_R11 or study_1_R1 would strengthen it. The pooled estimate is therefore not robust to leave-one-out perturbation, which is the expected consequence of combining a bimodal effect distribution.

# Moderators

With k = 10 studies and substantial unexplained heterogeneity, formal meta-regression is not statistically defensible: standard guidance requires approximately ten studies per covariate, so even a single moderator would exhaust the available degrees of freedom and produce estimates with no useful precision. The following relationships are therefore offered as **descriptive hypotheses generated by the data, not as tested findings**, and are depicted in the bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`), in which marker size encodes trial precision.

1. **Trial size / precision.** The clearest descriptive pattern is an inverse relationship between sample size and effect magnitude. The two largest contributing trials (n = 241, g = −0.007; n = 185, g = +0.031) are precisely null, whereas the smallest contributing trial (n = 62) yields g = −0.873. This is the signature pattern of either genuine effect modification by trial characteristics that correlate with size (pragmatic, broadly recruited, usual-care-embedded trials tend to be both larger and to show smaller effects) or of small-study bias. Notably, the formal bias diagnostics (below) did *not* detect significant funnel asymmetry, so this pattern cannot be attributed to publication bias on the available evidence — but neither can it be dismissed.

2. **Control condition.** Waiting-list controls are expected to inflate apparent benefit relative to active usual care, because participants assigned to a waiting list have no treatment expectancy, no therapeutic contact and often defer other care until after the waiting period. Trials in this synthesis used a mixture of waiting-list and usual-care comparators. Partitioning the included trials by comparator type is the single most plausible candidate explanation for the bimodal effect distribution and should be pre-specified in future, larger syntheses.

3. **Outcome instrument.** Trials contributing a *disability-specific* measure (RMDQ, PDI, ODI, WHODAS, FIQ physical function) are measuring pain-related activity limitation directly, whereas trials contributing only a *general physical-function subscale* (SF-36/SF-12 PF) are measuring a broader and less pain-specific construct with known ceiling effects in ambulatory samples. The fallback measures are expected to be less sensitive to intervention effects and would be anticipated to cluster near the null.

4. **Delivery modality and guidance.** Internet-delivered programmes dominate this literature; telephone-, app- and video-delivered formats are each represented by few trials. Guided (therapist-supported) formats generally produce larger effects than unguided self-help in the broader digital-intervention literature, and dose (number of modules, therapist contact minutes) varies by an order of magnitude across these trials. With the present k these cannot be separated from one another or from population and comparator differences.

5. **Pain condition.** Low back pain, fibromyalgia, osteoarthritis and mixed-pain samples differ markedly in baseline disability, in the plausibility of behavioural activation as a mechanism, and in concurrent usual care. Condition is confounded with outcome instrument (fibromyalgia trials predominantly use the FIQ; back pain trials the RMDQ/ODI), making the two moderators non-separable here.

In short, the 79.55% I² remains substantively unexplained. The honest conclusion is that we can demonstrate that the effect of remote CBT on functional disability varies considerably across trials, but we cannot yet say why.

# Publication Bias

Small-study and publication bias were assessed with two complementary methods:

- **Egger's regression test:** intercept = 0.3653, **p = 0.3244** — no statistically significant funnel plot asymmetry.
- **Duval & Tweedie trim-and-fill:** **k₀ = 0** studies imputed; adjusted pooled estimate **g = −0.2654**, identical to the unadjusted estimate.

The overall assessed risk of publication (small-study) bias is therefore **low**. As the analysis interpretation notes, Egger's test showed no statistically significant funnel plot asymmetry (p = 0.3244) and trim-and-fill imputed no missing studies, so the adjusted pooled effect is identical to the original estimate; together these results support a low risk of publication bias in this meta-analysis.

This conclusion requires an important qualification. Both tests have low statistical power when the number of included studies is small; with k = 10 and I² near 80%, Egger's test is poorly powered and its performance is further degraded by genuine between-study heterogeneity, which can mimic or mask asymmetry. The non-significant result should therefore be read as **an absence of detectable asymmetry rather than definitive proof that no bias exists**. The descriptive inverse relationship between trial size and effect magnitude noted in the Moderators section is consistent with small-study effects, even though it does not reach statistical detectability here. Additionally, outcome-reporting bias is not addressed by funnel-based methods: trials in this field commonly report multiple functional measures at multiple timepoints, and selective emphasis on the most favourable of these would not generate funnel asymmetry.

# Data Quality & Validation Notes

The following data-handling and validation issues arose during the pipeline and are reported transparently:

1. **Three records could not be confidently auto-classified by document type and were retained on the basis of user curation.** The automated document-type gate was unable to determine with confidence whether the following records were primary randomised trial reports: `8cc1256e_AJP.0000000000000494`, `9204e93e_j.pain.0000000000000802`, and `76469b82_j.pain.2010.08.034`. Because the review was run in manual mode, which trusts user curation by default, all three were kept as inputs rather than excluded. These are *warnings*, not errors: the records may well be valid primary trial reports, but their status was not independently confirmed by the automated gate, and readers should treat their inclusion as resting on curator judgement.

2. **Four of the 14 included studies contributed no effect size.** Only 10 of the 14 studies that met the review's eligibility criteria supplied post-treatment data extractable into an SMD (mean, convertible dispersion and n per arm). All pooled estimates, heterogeneity statistics and bias diagnostics in this report are based on those 10 trials and 1,338 participants only. The excluded four are a non-trivial fraction (29%) of the eligible evidence, and because the reasons for non-extractability (reporting of medians, model-based estimates without variances, or missing arm-level n) may not be independent of results, their omission is a potential source of bias that funnel-based methods cannot detect.

3. **No documents were excluded as reviews, editorials or duplicate publications,** and no trial reports required removal to avoid double-counting of the same randomised sample.

4. **All outcomes were successfully classified** to the single pre-specified outcome/timepoint group (post-treatment functional disability). No outcome group was flagged as having insufficient data for pooling, and no effect measures had to be pooled separately on different scales. A single native SMD pooling was used throughout.

5. **Scale harmonisation and arm combination were applied as pre-specified:** physical-function subscales were reverse-signed so that lower always means less disability, SEs were converted to SDs via SD = SE × √n, and multi-arm remote CBT conditions were combined into a single intervention group to preserve one independent effect size per trial.

# Discussion

This meta-analysis of 10 randomised comparisons involving 1,338 adults with chronic non-headache pain found that remotely delivered CBT produced a **small, statistically significant reduction in functional disability at end of treatment** relative to treatment as usual or waiting-list control: pooled SMD = −0.265 (95% CI −0.511 to −0.020; p = 0.034), favouring remote CBT.

Three features of this result deserve emphasis over the headline number.

**First, the magnitude is small and of doubtful clinical importance at the individual-patient level.** A quarter-standard-deviation improvement translates to roughly one to two points on the RMDQ, generally below accepted thresholds for a minimally important change. It is, however, consistent with the broader literature on psychological therapy for chronic pain, where in-person CBT typically yields disability effects in the g = 0.2–0.4 range against inactive controls. Remote delivery thus appears to approximate — rather than substantially undercut or exceed — the modest functional benefit of face-to-face CBT, a finding of real public-health interest given the order-of-magnitude difference in therapist resource per patient treated. A small effect delivered cheaply to very many people can carry greater population-level value than a moderate effect delivered expensively to few, and economic evaluation rather than effect-size magnitude alone should drive implementation decisions.

**Second, the average conceals profound variability.** With I² = 79.55% and τ ≈ 0.349, the effect is not a stable property of "remote CBT" as a category. Five trials showed clear benefit (up to g = −0.90) and five showed none, and the division correlated descriptively with trial size: the two largest and most precisely estimated trials were both null. The prediction interval (approximately −1.12 to +0.59) is the appropriate summary for anyone asking what a new trial or a new service implementation should expect, and it includes no benefit. Pooled point estimates in this literature should not be quoted without their prediction interval.

**Third, the pooled estimate is fragile.** Its p-value is 0.034 and its upper confidence bound is −0.020. Removal of either of the two strongly positive trials would plausibly move the interval across zero. This is not a criticism of the analysis but a property of the evidence: ten heterogeneous trials of modest size cannot deliver a precise or robust estimate of a small effect.

Mechanistically, the pattern is interpretable. Functional disability in chronic pain is maintained substantially by *behavioural* avoidance, and the components of CBT that most directly address it — graded in-vivo exposure, activity scheduling with therapist-monitored progression, and troubleshooting of setbacks — are the components hardest to deliver at distance and through low-contact digital formats. Remote programmes reliably deliver the cognitive and psychoeducational components (reconceptualising pain, challenging catastrophic appraisals) and these may shift pain-related distress and catastrophising more readily than they shift function. The modest disability effect observed here, relative to the generally larger effects reported for catastrophising and distress outcomes in digital-pain trials, is consistent with that account. It implies that the productive direction for intervention development is not "more content" but better remote scaffolding of actual behaviour change — activity tracking, human or automated contingent coaching, and integration with physiotherapy or exercise provision.

Low assessed publication-bias risk (Egger's p = 0.3244; trim-and-fill k₀ = 0) is reassuring at face value, and distinguishes this body of evidence from some digital-health literatures where funnel asymmetry is marked. The caveat stands that with k = 10 and high heterogeneity these tests detect only gross asymmetry.

# Limitations

Several limitations constrain the strength of inference.

1. **Small evidence base for a heterogeneous question.** Ten effect sizes is few for a question spanning four pain conditions, four delivery modalities, two comparator types and at least three therapeutic frameworks (CBT, ACT, exposure). The synthesis therefore pools across clinical and methodological dimensions that almost certainly modify the effect, without the power to separate them.

2. **Incomplete extraction from the eligible pool.** Four of 14 eligible studies (29%) could not contribute effect sizes because of non-extractable post-treatment data. If non-reporting of usable dispersion statistics is correlated with null or unfavourable results — a documented phenomenon — the pooled estimate is biased, and in an unknown direction that funnel-plot methods cannot detect.

3. **Unexplained heterogeneity.** Roughly 80% of observed variance is between-study. No moderator analysis could be conducted with adequate power, so the determinants of effect variability remain unidentified. The pooled mean should not be applied to any specific population, modality or comparator.

4. **Mixed comparator conditions.** Waiting-list and usual-care comparators were pooled. Waiting-list designs systematically inflate apparent treatment effects relative to active usual care through expectancy and care-deferral mechanisms, and their inclusion probably biases the pooled estimate away from the null to an unquantified degree.

5. **Heterogeneous and partly surrogate outcome measures.** Although disability-specific instruments were prioritised, some trials contributed general physical-function subscales (SF-36/SF-12 PF) as a fallback. These measure a broader construct, exhibit ceiling effects, and are less responsive to pain interventions; their inclusion adds measurement heterogeneity beyond what the SMD metric fully resolves. Reverse-signing harmonises direction but not construct.

6. **Unblinded outcome assessment.** All included trials rely on self-reported disability in designs where participants cannot be blinded to allocation, particularly against waiting-list controls. Non-specific expectancy, attention and demand effects are therefore embedded in every estimate, and the true specific effect of cognitive-behavioural content is necessarily smaller than the measured contrast.

7. **End-of-treatment timepoint only.** By design, this analysis addresses the first post-treatment assessment. It is silent on durability. Whether the small functional benefit is maintained, grows (as behavioural change consolidates) or decays (as programme engagement ends) cannot be determined here, and maintenance is arguably the more policy-relevant question for a chronic condition.

8. **Attrition and analysis-set heterogeneity.** Remote interventions characteristically have high non-completion. Trials differed in their handling of missing data (completer-case versus intention-to-treat with imputation), which was not harmonised; completer-case analyses tend to favour the intervention.

9. **Three records of unconfirmed document type** were retained on curator judgement rather than confirmed automated classification (see *Data Quality & Validation Notes*).

10. **No formal risk-of-bias ratings or GRADE certainty assessment** were incorporated into the quantitative model. Given the limitations above — unblinded self-reported outcomes, substantial unexplained inconsistency, imprecision with a confidence limit abutting the null, and incomplete extraction — the overall certainty of evidence for this outcome would most plausibly be rated **low**.

# Conclusion

In adults with chronic non-headache pain, remotely delivered cognitive behavioural therapy — internet-, telephone-, app- or video-delivered CBT, ACT and exposure-based variants — reduces functional disability at end of treatment compared with treatment as usual or waiting-list control, with a pooled Standardized Mean Difference of **−0.265 (95% CI −0.511 to −0.020; p = 0.034; k = 10; N = 1,338)**, a result that **favours remotely delivered CBT**. The effect measure was pooled natively on the SMD scale, so this is a confirmed standardized result rather than a fallback conversion.

The benefit is small in magnitude, of uncertain clinical importance at the individual level, statistically marginal, and highly inconsistent across trials (I² = 79.55%; τ² = 0.122147), with a prediction interval (approximately −1.12 to +0.59) that includes no benefit at all. Assessed publication-bias risk is low (Egger's p = 0.3244; trim-and-fill k₀ = 0), though the diagnostics are underpowered at this k.

The defensible clinical reading is that remote CBT is a reasonable, low-cost, highly scalable **adjunct** for improving function in chronic non-headache pain — one that may deliver worthwhile population-level benefit precisely because it is cheap to deliver at scale — but not a dependable substitute for multidisciplinary or in-person rehabilitation where function is the primary target, and not an intervention whose benefit can be promised to any individual patient.

Priorities for future research follow directly from the limitations identified: (i) adequately powered pragmatic trials against *active usual care* rather than waiting list; (ii) consistent reporting of a disability-specific primary outcome on a common native scale (RMDQ, PDI or ODI) with full means, SDs and arm-level n, so that native-scale rather than standardized pooling becomes possible; (iii) pre-specified comparison of guided versus unguided and of modalities that scaffold actual behaviour change versus those delivering cognitive content alone; (iv) routine reporting of maintenance effects at 6 and 12 months; and (v) individual participant data meta-analysis, which is the only realistic route to resolving the substantial heterogeneity documented here.

# Figures

- **Figure 1.** Forest plot of individual and pooled Standardized Mean Differences — `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
- **Figure 2.** Cumulative meta-analysis — `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
- **Figure 3.** Distribution of individual effect sizes — `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
- **Figure 4.** Bubble chart of effect size against trial precision — `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`
- **Figure 5.** Heterogeneity diagnostic summary — `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`

# References

Methodological and reporting standards underpinning this review:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al. (eds). *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis*. Academic Press; 1985.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1–48.
5. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
6. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6:e010247.
7. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
8. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
9. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
10. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336(7650):924–926.

Primary studies are identified in Table 1 by their pipeline study identifiers (study_1_R1 through study_13_R13); full bibliographic details correspond to the curated input corpus of 14 trial reports, including the three records of unconfirmed document type listed in the *Data Quality & Validation Notes* (`8cc1256e_AJP.0000000000000494`, `9204e93e_j.pain.0000000000000802`, `76469b82_j.pain.2010.08.034`).

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| functional disability | 10 | Standardized Mean Difference (SMD) | Yes | -0.2654 [-0.5109, -0.0200] |
