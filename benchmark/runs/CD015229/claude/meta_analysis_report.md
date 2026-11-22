# Effect of a Single Sympathetic Nerve Block versus Standard Care on Pain Intensity at 14 Days Post-Intervention: A Systematic Review and Meta-Analysis

## Abstract

**Background.** Sympathetic nerve blocks (stellate ganglion, lumbar sympathetic, celiac plexus and paravertebral sympathetic blocks) are widely used as single-shot interventions for sympathetically maintained and visceral pain states. Whether a *single* block produces a clinically meaningful analgesic benefit that persists into the sub-acute window (~2 weeks) relative to standard care remains uncertain.

**Objective.** To quantify the effect of a single sympathetic nerve block, compared with standard care (usual pharmacological/conservative management, sham block, or placebo injection), on patient-reported pain intensity measured at approximately 14 days post-intervention.

**Methods.** A systematic search and structured screening pipeline identified 5 eligible study reports, of which 3 contributed extractable, non-overlapping effect estimates for the 14-day pain-intensity outcome (N = 114 participants). Effects were pooled using a random-effects model fitted by restricted maximum likelihood (REML). The pre-specified effect measure was the **Mean Difference (MD)**, and native-scale pooling was confirmed (`native_pooling_used = true`). Heterogeneity was quantified with Q, I² and τ². Small-study effects were assessed with Egger's regression and trim-and-fill.

**Results.** The pooled **Mean Difference (MD)** at ~14 days was **−0.2613 (95% CI −1.095 to 0.573; p = 0.5393; k = 3; N = 114)**. Per the pre-specified direction field, this point estimate **favours the single sympathetic nerve block arm**, but the confidence interval crosses the line of no effect and the result is not statistically significant. Between-study heterogeneity was substantial: **Q = 7.584 (p = 0.0226), I² = 72.03%, τ² = 0.363231**. Study-level estimates were discordant in direction, ranging from −0.99172 (95% CI −1.547 to −0.436) to +0.20835 (95% CI −0.430 to 0.847). Egger's regression showed no significant funnel asymmetry (intercept −2.1015, p = 0.3948) and trim-and-fill imputed no missing studies (k₀ = 0; adjusted estimate −0.2578), indicating a low *detected* risk of publication bias.

**Conclusions.** Current pooled evidence does not demonstrate a statistically significant effect of a single sympathetic nerve block on pain intensity at 14 days. The point estimate favours the block, but the interval is wide, heterogeneity is substantial and directionally inconsistent, and the evidence base is very small (k = 3). These findings should be regarded as hypothesis-generating; adequately powered, blocked-and-sham-controlled trials reporting a standardised 14-day pain assessment are required.

## 1. Introduction

Interruption of sympathetic efferent and afferent traffic by local-anaesthetic blockade has been a cornerstone of interventional pain management for nearly a century. Stellate ganglion blocks are used for complex regional pain syndrome (CRPS) of the upper limb, post-traumatic facial and head pain, and, more recently, for post-traumatic stress and vasomotor symptoms; lumbar sympathetic blocks are applied to lower-limb CRPS and ischaemic pain; celiac plexus blocks are a standard of care for pancreatic and upper-abdominal visceral cancer pain; and paravertebral sympathetic blockade is used across thoracic and abdominal pain syndromes.

The mechanistic rationale — abolishing sympathetically maintained nociceptive signalling, improving perfusion, and interrupting central sensitisation loops — predicts an analgesic effect that may outlast the pharmacokinetic duration of the injected local anaesthetic. Clinically, this "carry-over" assumption underpins the common practice of offering a *single* diagnostic-therapeutic block before committing a patient to a series of blocks, neurolysis, or neuromodulation. The empirical basis for that assumption at the two-week mark is, however, thin: most randomised studies report either very early endpoints (minutes to 24 hours), when the direct pharmacological effect dominates, or late endpoints (1–6 months), by which time co-interventions and natural history confound attribution.

This report addresses the specific, pre-specified question:

> **What is the effect of a single sympathetic nerve block, compared with standard care, on patient-reported pain intensity score at approximately 14 days post-intervention?**

**Effect direction convention.** Throughout this review, a *positive* effect size denotes **lower pain** (i.e. benefit) in the sympathetic block arm. Note, however, that the pooled statistic reported by the analysis engine retains the raw statistical sign convention (treatment minus control), so a *negative* Mean Difference on a pain scale corresponds to lower pain in the block arm. To avoid any ambiguity, the arm favoured by the pooled result is reported exclusively from the pre-specified `favors` field of the analysis output and is never inferred from the sign of the estimate in the text below.

Only the ~14-day assessment window (±a few days) is analysed here. Other timepoints (24 hours, 1 month, 3 months) are the subject of separate, parallel analyses within this review programme and are not merged into the estimates reported below.

---

## 2. Search and Screening

### 2.1 Information sources and strategy

A systematic search of the indexed literature was conducted through the review pipeline, targeting controlled studies of single-session sympathetic blockade with a comparator arm receiving standard care, sham block, or placebo injection, and reporting a continuous patient-reported pain-intensity outcome. Search concepts combined:

- **Intervention terms:** *sympathetic block*, *stellate ganglion block*, *cervicothoracic ganglion*, *lumbar sympathetic block*, *celiac/coeliac plexus block*, *splanchnic block*, *paravertebral sympathetic block*, *sympathetic blockade*.
- **Comparator terms:** *standard care*, *usual care*, *conservative management*, *sham*, *placebo*, *saline injection*, *control*.
- **Outcome terms:** *pain*, *visual analogue scale*, *VAS*, *numeric(al) rating scale*, *NRS*, *pain intensity*, *pain score*, *brief pain inventory*.
- **Design filters:** randomised controlled trial, controlled clinical trial, comparative study.

### 2.2 Screening and selection

Records were screened in two stages (title/abstract, then full text) against the following criteria.

**Inclusion criteria**
1. Human participants with a pain condition of any aetiology.
2. Intervention consisting of a **single** sympathetic nerve block (stellate ganglion, lumbar sympathetic, celiac plexus, or paravertebral sympathetic).
3. A concurrent comparator receiving standard care, sham block, or placebo injection.
4. A continuous, patient-reported pain-intensity outcome assessed at approximately **14 days** post-intervention (VAS 0–100, NRS 0–10, or a pain subscale of a validated composite instrument).
5. Sufficient data to compute an effect estimate and its variance (group means with SD/SE/CI and group sizes, or a reported between-group contrast with dispersion).

**Exclusion criteria**
1. Series of repeated or continuous blocks without an isolable single-block arm.
2. Neurolytic/radiofrequency ablation as the index intervention where no local-anaesthetic single-block arm existed.
3. No contemporaneous control arm (single-arm, before–after, or historical-control designs).
4. No pain assessment within the 14-day window.
5. Reviews, editorials, protocols, conference abstracts without extractable data, and duplicate reports of the same trial population.

### 2.3 Study flow

The screening and extraction pipeline retained **5 study reports** meeting eligibility criteria for this review question. Of these, **3 reports supplied an extractable, non-overlapping effect estimate for the 14-day pain-intensity endpoint** and entered the quantitative synthesis (`n_studies = 5`, `n_effect_sizes = 3`). The remaining 2 eligible reports could not be pooled for this specific endpoint — for example because the 14-day pain outcome was reported without usable dispersion statistics, or was reported only in a form (e.g. responder proportions, median with range, graphical-only presentation) that could not be converted to the pre-specified Mean Difference scale without unverifiable assumptions. These reports are retained in the narrative review but contribute no weight to the pooled estimate. This 5-to-3 attrition is an explicit, acknowledged limitation (see §9 and §10).

**PRISMA flow (quantitative synthesis path):** records identified → screened → full texts assessed → **5 studies included in the systematic review** → **3 studies (N = 114 participants) included in the meta-analysis of pain at ~14 days**.

---

## 3. Included Studies

Three studies contributed to the pooled 14-day estimate, with a combined sample of **114 participants**. Sample sizes were small throughout (range 20–56), and all three contributed an independent, single effect estimate (one effect per study; no multiplicity correction or multi-level nesting was required).

**Table 1. Studies contributing to the 14-day pain-intensity synthesis**

| Study (effect ID) | N | Study-level effect estimate | 95% CI | Precision (CI width) | Relative contribution |
|---|---|---|---|---|---|
| `study_1_R1` | 20 | 0.113317 | −0.764 to 0.991 | 1.755 | Lowest (smallest N) |
| `study_3_R3` | 38 | 0.208350 | −0.430 to 0.847 | 1.277 | Intermediate |
| `study_5_R5` | 56 | −0.991720 | −1.547 to −0.436 | 1.111 | Highest (largest N) |
| **Total** | **114** | — | — | — | — |

Two further eligible reports (`study_2`, `study_4` in the review register) were identified but did not yield a poolable 14-day estimate and are therefore absent from Table 1.

**Characteristics and clinical heterogeneity.** The three pooled studies differ in ways that are material to interpretation. The analysis set spans more than one anatomical block target and, by the eligibility criteria, more than one underlying pain aetiology (sympathetically maintained limb pain versus visceral/abdominal pain are mechanistically distinct entities with different expected natural histories over a two-week window). Comparators also differ in rigour across the eligible pool, encompassing both *active* sham/placebo injections (which preserve blinding and control for needling and expectancy effects) and *open* standard-care arms (which do not). Pain instruments differed across the original reports (VAS and NRS variants, and composite-instrument pain subscales), and the exact day of the "14-day" assessment varied within the permitted ±few-day window. These sources of clinical and methodological diversity provide a plausible substantive explanation for the statistical heterogeneity documented in §6 and are the primary reason the pooled estimate should not be read as a single transportable parameter.

**Risk of bias considerations.** With samples of 20–56, none of the included studies is powered to detect a small-to-moderate analgesic difference at 14 days; all are therefore vulnerable to both random error and, where blinding was incomplete, to performance and detection bias in a subjective, self-reported outcome. Attrition over a two-week follow-up and the availability of rescue analgesia as a co-intervention are further threats that typically attenuate or distort between-arm contrasts at this timepoint.

---

## 4. Effect Sizes

### 4.1 Effect measure

The effect measure for this synthesis was pre-specified by explicit user request as the **Mean Difference (MD)** (`effect_measure = "MD"`, `effect_measure_source = "explicit_user_request"`, no measure conflict recorded). **Native-scale pooling was used and confirmed (`native_pooling_used = true`)**: the pooled value reported below is a Mean Difference computed and combined on its native scale, not a standardized fallback. Accordingly, the pooled statistic is named throughout as the **pooled Mean Difference (MD)**, and it must **not** be described or cited as Hedges' *g*, Cohen's *d*, or any other standardized metric. The deterministic Effect Measure Summary table appended to this report is authoritative on this point and is consistent with the text here.

### 4.2 Study-level estimates

Study-level estimates as entered into the pooling model were:

- `study_1_R1`: **0.113317** (95% CI −0.764 to 0.991), N = 20
- `study_3_R3`: **0.208350** (95% CI −0.430 to 0.847), N = 38
- `study_5_R5`: **−0.991720** (95% CI −1.547 to −0.436), N = 56

Two features dominate this set. First, **every individual confidence interval is wide** — the narrowest spans 1.11 units — reflecting the uniformly small samples; two of the three intervals include the null. Second, and more importantly, **the estimates are directionally discordant**: `study_1_R1` and `study_3_R3` sit on one side of the null while `study_5_R5` sits firmly on the other, with the largest and most precise study being the one whose interval excludes the null. The intervals of `study_5_R5` and `study_3_R3` do not overlap, which is the visual signature of genuine between-study inconsistency rather than mere imprecision.

Because the largest study also carries the most extreme estimate, the random-effects weighting — which, under substantial τ², deliberately flattens weights toward equality — pulls the pooled value markedly toward the null relative to what a precision-weighted fixed-effect model would produce. This is the appropriate behaviour given the detected heterogeneity, but it means the pooled point estimate is an average over genuinely conflicting findings rather than a summary of a common effect.

**Figures.** Study-level estimates and their intervals are displayed in the forest plot: `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. The dispersion and shape of the effect distribution are shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

---

## 5. Meta-Analytic Result

A single synthesis group was analysed; the context data contain no `meta_analysis_groups` entries, so all included effects pertain to one outcome/timepoint (pain intensity at ~14 days) and a single pooled figure is reported.

**Table 2. Random-effects pooled result, pain intensity at ~14 days**

| Quantity | Value |
|---|---|
| Effect measure | **Mean Difference (MD)** (native pooling confirmed) |
| Pooled estimate | **−0.2613** |
| 95% confidence interval | **−1.095 to 0.573** |
| p-value | **0.5393** |
| Studies (k) | **3** |
| Participants (N) | **114** |
| Model | Random effects, REML |
| Q (df = 2) | 7.584 (p = 0.0226) |
| I² | 72.03% |
| τ² | 0.363231 |
| Favours (pre-specified field) | **Single sympathetic nerve block** |

The pooled **Mean Difference (MD)** at approximately 14 days post-intervention is **−0.2613 (95% CI −1.095 to 0.573)**, with **p = 0.5393**. In accordance with the pre-specified `favors` field, the direction of this point estimate **favours the single sympathetic nerve block arm** over standard care. However, the result is **not statistically significant at the conventional 5% level**: the 95% confidence interval comfortably includes the null and extends appreciably in both directions, spanning values that would represent a worthwhile reduction in pain (lower bound −1.095) through to values consistent with slightly *worse* pain in the block arm (upper bound +0.573).

Interpreted plainly: **the available data are compatible with a modest analgesic benefit of a single sympathetic block at two weeks, with no benefit at all, and with a small harm.** The study cannot distinguish between these possibilities. The width of the interval — roughly 1.67 units, or more than six times the magnitude of the point estimate — is driven jointly by the very small number of studies (k = 3), the small samples within them (N = 114 in total), and the substantial between-study variance component (τ² = 0.363231) that the random-effects model must propagate into the standard error of the summary estimate.

A cumulative meta-analysis, ordering studies and re-estimating the pooled value sequentially, is provided in `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. With only three studies this plot is primarily descriptive; it illustrates how unstable the running estimate remains and shows that no asymptotic convergence toward a stable value has been achieved — the pooled estimate has not "settled", and a single additional trial of moderate size could plausibly move it across the null in either direction.

---

## 6. Heterogeneity

Between-study heterogeneity was **substantial and statistically significant**:

- **Cochran's Q = 7.584 on 2 degrees of freedom, p = 0.0226** — the null hypothesis of a common underlying effect is rejected at the 5% level.
- **I² = 72.03%** — approximately 72% of the observed variability in effect estimates is attributable to real between-study differences rather than within-study sampling error. By conventional benchmarks this falls in the "substantial" band (50–90%).
- **τ² = 0.363231** — the estimated between-study variance of true effects, corresponding to a between-study standard deviation of approximately **0.603** on the Mean Difference scale. This is more than twice the magnitude of the pooled point estimate itself, meaning the dispersion of true effects across settings dwarfs their average.

It is worth emphasising that a significant Q test with only k = 3 is notable, because Q has low power when the number of studies is small. Detecting significant heterogeneity in such a sparse dataset indicates that the inconsistency is pronounced, not marginal. The source of the signal is evident from §4.2: the directional conflict between `study_5_R5` on one side of the null and `study_1_R1`/`study_3_R3` on the other, with non-overlapping confidence intervals between the two largest studies.

Two caveats on precision apply. First, I² is itself estimated with great imprecision at k = 3; its own confidence interval would be extremely wide and would likely encompass values from negligible to near-total heterogeneity. Second, τ² estimated by REML from three studies is a low-information quantity. Neither statistic should be reported as a precise characterisation of the heterogeneity; they are best read as a qualitative signal that these three studies are not estimating the same thing.

A formal prediction interval — the interval within which the true effect of a *new*, exchangeable study would be expected to fall — is not reported here because it cannot be estimated with any usable precision from k = 3 and τ² of this magnitude; any such interval would be so wide as to be uninformative. Qualitatively, however, the combination of a wide confidence interval and τ² = 0.363231 implies that the predicted effect in a future setting is highly uncertain and could lie on either side of the null.

Given k = 3, **no subgroup analysis or sensitivity analysis by design feature was performed**, as such analyses would be driven entirely by single studies.

A graphical summary of the heterogeneity statistics is provided in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 7. Moderators

**No meta-regression or formal moderator analysis was conducted, and none can be legitimately conducted on this dataset.** With k = 3 studies and a single covariate, a meta-regression would have 1 residual degree of freedom; the resulting coefficients would be essentially unidentified, highly unstable, and at severe risk of over-fitting. Published guidance (and the widely used rule of thumb of ≥10 studies per covariate) places this analysis well outside the range in which moderator inference is defensible.

A **bubble chart** relating study-level effect estimates to study precision/size is nevertheless provided for descriptive purposes: `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. It should be read as a visual aid only; no coefficient, slope, or p-value is reported from it, and any apparent trend across three points carries no inferential weight.

Descriptively, the clinically plausible moderators that *would* be the priority candidates in a larger evidence base are:

1. **Anatomical block target** (stellate ganglion vs lumbar sympathetic vs celiac plexus vs paravertebral), which maps onto fundamentally different pain mechanisms and expected durations of effect.
2. **Underlying pain aetiology** (sympathetically maintained/neuropathic limb pain vs visceral cancer pain), which governs the natural-history trajectory over the 14-day window.
3. **Comparator type** (active sham/placebo injection vs open standard care), which determines the magnitude of expectancy and performance effects embedded in the contrast — a particularly important moderator for a subjective outcome at a timepoint when direct pharmacological effect has largely dissipated.
4. **Pain instrument and exact assessment day** within the permitted window.
5. **Permitted co-interventions / rescue analgesia**, which can mask a genuine analgesic effect by equalising reported pain scores across arms.

The possibility that one or more of these factors accounts for the 72.03% of variance attributed to between-study differences is entirely consistent with the data, but it cannot be tested here. Establishing which of these explains the directional conflict observed in §4.2 is the single highest-value next step for this literature.

---

## 8. Publication Bias

Small-study effects were assessed using Egger's regression test and the Duval–Tweedie trim-and-fill procedure.

**Table 3. Small-study effect diagnostics**

| Test | Result |
|---|---|
| Egger's regression intercept | **−2.1015** |
| Egger's test p-value | **0.3948** |
| Trim-and-fill imputed studies (k₀) | **0** |
| Trim-and-fill adjusted estimate | **−0.2578** |
| Overall assessed risk | **Low** |

Egger's regression showed **no statistically significant funnel-plot asymmetry (intercept = −2.1015, p = 0.3948)**. The trim-and-fill procedure **imputed no missing studies (k₀ = 0)**, so the adjusted estimate (**−0.2578**) is essentially identical to the unadjusted pooled Mean Difference (−0.2613) — a shift of 0.0035 units, which is immaterial. Taken together, these diagnostics support a **low risk of publication bias (small-study effects)** as assessed by the available tests.

This conclusion must be heavily qualified. **Both Egger's test and trim-and-fill have very low statistical power when k is small — and with k = 3 they are, for practical purposes, uninformative.** Egger's test is generally not recommended below k = 10, and substantial heterogeneity (here, I² = 72.03%) further degrades its performance by inflating the standard error of the regression slope and by inducing asymmetry that is unrelated to selective publication. The magnitude of the Egger intercept (−2.1015) is in fact not small; it is the standard error, not the point estimate, that renders it non-significant. The correct reading is therefore: **no evidence of publication bias was detected, but the analysis had essentially no capacity to detect it.** Absence of detected asymmetry here must not be presented as evidence of absence of bias.

A further, non-statistical consideration reinforces caution: an interventional literature of this kind, dominated by small single-centre studies, is structurally susceptible to selective reporting of favourable timepoints. The fact that only 3 of 5 otherwise-eligible reports provided an extractable 14-day estimate (§2.3) is itself a form of outcome-reporting attrition that funnel-based methods cannot capture.

---

## 9. Data Quality & Validation Notes

No formal `validation_flags` were returned by the analysis pipeline for this synthesis. The following data-handling facts are nevertheless reported plainly so that readers can judge the evidence on its actual footing:

- **Study-to-effect attrition.** The pipeline retained **5 eligible study reports** but only **3 extractable effect sizes** for the 14-day pain outcome. Two eligible reports therefore contribute nothing to the pooled estimate. The pooled result describes 3 studies and 114 participants, not 5 studies.
- **Effect measure.** The effect measure was set by **explicit user request** to the **Mean Difference (MD)**, with no recorded measure conflict, and **native-scale pooling was confirmed**. The pooled value is a genuine Mean Difference and is not a standardized fallback. It must not be relabelled as Hedges' *g*.
- **Single synthesis group.** The context data contain no `meta_analysis_groups` entries, i.e. all pooled effects belong to one outcome/timepoint. No separate per-group estimates were required or produced, and no results from other timepoints (24 h, 1 month, 3 months) have been merged into the figures above.
- **Sign convention.** The pooled estimate carries the raw treatment-minus-control sign convention. The arm favoured has been taken exclusively from the pipeline's `favors` field (single sympathetic nerve block) and not inferred from the sign.
- **Analyses not performed.** No subgroup analyses, meta-regression, or leave-one-out sensitivity analyses were run, because k = 3 renders them uninterpretable. The bubble chart is descriptive only.
- **Diagnostic power.** Publication-bias diagnostics were computed and are reported, but at k = 3 they are underpowered to the point of being near-uninformative; they are presented for completeness and transparency, not as reassurance.

---

## 10. Discussion

This meta-analysis pooled three controlled studies (N = 114) addressing a narrowly defined and clinically important question: does a *single* sympathetic nerve block reduce patient-reported pain intensity at approximately two weeks, relative to standard care? The pooled **Mean Difference (MD) of −0.2613 (95% CI −1.095 to 0.573; p = 0.5393)** **favours the single sympathetic nerve block arm** by the pre-specified direction field, but is far from statistical significance and is surrounded by an interval wide enough to accommodate clinically meaningful benefit, exact equivalence, and modest harm.

**What this does and does not tell clinicians.** The honest summary is one of *uncertainty*, not of demonstrated ineffectiveness. A non-significant pooled estimate in a dataset of three small trials is weak evidence about anything; it is emphatically not evidence that single sympathetic blocks lack a two-week analgesic effect. Equally, it provides no empirical support for the common clinical assumption that a single block delivers a reliable carry-over benefit at two weeks that justifies the procedure on therapeutic (as opposed to diagnostic) grounds. The practical implication is that the two-week carry-over effect should currently be regarded as unproven in either direction, and that decisions to proceed from a single diagnostic block to a therapeutic series should be grounded in individual response and in the longer-timepoint analyses of this review programme rather than in an assumed population-level 14-day benefit.

**The heterogeneity is the headline finding.** Arguably the most informative result here is not the pooled estimate but the inconsistency underlying it: **I² = 72.03%, τ² = 0.363231, Q = 7.584 (p = 0.0226)**, with the largest study pointing firmly in one direction and the two smaller studies pointing the other way, and with non-overlapping confidence intervals between the two largest contributors. When true effects are this dispersed, an average effect is a poor summary; the clinically relevant question shifts from "does it work?" to "in whom, with which target, against which comparator, does it work?" The candidate explanations enumerated in §7 — block target, pain aetiology, comparator rigour, instrument, and permitted co-interventions — are each plausible and each untestable with three studies. Notably, comparator rigour deserves particular attention: at 14 days, when the local anaesthetic is long gone, much of any apparent difference against an *open* standard-care arm could reflect expectancy and the ritual of a procedure rather than neurophysiological blockade, whereas a sham-controlled contrast would strip that component out. A literature that mixes the two comparator types will, by construction, generate exactly the kind of directional discordance observed here.

**Relation to the wider evidence.** The pattern seen here — plausible mechanism, enthusiastic clinical adoption, and a small, heterogeneous, underpowered randomised evidence base — is characteristic of much of the interventional pain literature, and is consistent with prior systematic reviews of sympathetic blockade that have repeatedly concluded that trial quality and sample size, rather than effect magnitude, are the limiting factors. The present analysis adds a specific, quantified estimate for the 14-day endpoint, with explicit documentation of its fragility, rather than a definitive answer.

**Robustness.** Within the limits of the available diagnostics, the pooled estimate appears robust to small-study effects: trim-and-fill imputed no studies and shifted the estimate by only 0.0035 units (−0.2613 → −0.2578), and Egger's test was non-significant (p = 0.3948). This offers mild reassurance about funnel asymmetry but, as set out in §8, carries little weight at k = 3. Conversely, the cumulative analysis (`cumulative_plot.png`) makes clear that the estimate is *not* robust to the addition of new data: it has not stabilised, and remains highly sensitive to each additional study.

---

## 11. Limitations

1. **Very small number of studies (k = 3).** This is the dominant limitation. It constrains the precision of the pooled estimate, renders heterogeneity statistics imprecise, makes publication-bias diagnostics near-uninformative, and precludes subgroup analysis, meta-regression, and meaningful leave-one-out sensitivity analysis.
2. **Small total sample (N = 114; range 20–56 per study).** No contributing study was powered for the 14-day endpoint; all are vulnerable to random error and to the inflated effect estimates typical of small trials.
3. **Substantial, directionally discordant heterogeneity (I² = 72.03%, τ² = 0.363231, Q p = 0.0226).** The pooled Mean Difference averages over studies that disagree about the *direction* of effect, limiting its interpretability as a single transportable parameter.
4. **Incomplete outcome extraction.** Only 3 of 5 eligible reports supplied a poolable 14-day estimate; the 2 excluded reports may differ systematically from those included, introducing potential outcome-reporting bias that no funnel-based method can detect.
5. **Clinical and methodological diversity.** Pooled studies span different anatomical block targets, different underlying pain aetiologies, different pain instruments (VAS/NRS/composite subscales), different exact assessment days within the ±few-day window, and — critically — different comparator types (active sham/placebo versus open standard care), the last of which differentially embeds expectancy effects.
6. **Risk of bias within studies not formally incorporated.** Blinding status, attrition over the two-week follow-up, and rescue-analgesia co-interventions could not be modelled or used to weight the synthesis; for a subjective self-reported outcome these are first-order threats.
7. **No prediction interval reported.** At k = 3 with this τ², a prediction interval cannot be estimated with usable precision and would be uninformative; readers are therefore given no quantified expectation for a future study's effect.
8. **Underpowered bias diagnostics.** Egger's test and trim-and-fill are not recommended below approximately 10 studies and are further degraded by high heterogeneity; the "low risk" designation reflects *non-detection*, not demonstrated absence, of bias.
9. **Single-timepoint scope.** By design, only the ~14-day assessment is analysed. Conclusions here do not generalise to earlier or later timepoints, which are reported separately within this review programme, and the trajectory of effect over time cannot be inferred from this analysis alone.

---

## 12. Conclusion

Pooling three small controlled studies (N = 114), a single sympathetic nerve block produced a pooled **Mean Difference (MD) of −0.2613 (95% CI −1.095 to 0.573; p = 0.5393)** for patient-reported pain intensity at approximately 14 days compared with standard care. The point estimate **favours the single sympathetic nerve block arm**, but the result is **not statistically significant** and the confidence interval spans both meaningful benefit and modest harm. Between-study heterogeneity was substantial and statistically significant (**I² = 72.03%, τ² = 0.363231, Q = 7.584, p = 0.0226**), with the included studies disagreeing about the direction of effect. Publication-bias diagnostics were unremarkable (Egger's p = 0.3948; trim-and-fill k₀ = 0; adjusted estimate −0.2578), but are underpowered at k = 3 and should not be read as reassurance.

**Bottom line.** The present evidence neither establishes nor refutes a two-week analgesic benefit of a single sympathetic nerve block. The findings are **hypothesis-generating** and should not be used to justify or to abandon the practice. Priority next steps are: (i) adequately powered, **sham-controlled**, double-blind randomised trials with a pre-specified 14-day pain endpoint; (ii) **standardisation** of the pain instrument, the assessment day, and the handling of rescue analgesia; (iii) **stratification or pre-planned subgrouping by block target and pain aetiology**, so that the substantial heterogeneity identified here can be explained rather than merely averaged away; and (iv) individual-participant-data synthesis, which would allow moderator effects to be examined without the degrees-of-freedom constraints that make study-level meta-regression impossible in an evidence base of this size.

---

## Figures

| Figure | Path |
|---|---|
| Forest plot — study-level and pooled Mean Difference, pain at ~14 days | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis — stability of the running pooled estimate | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart — effect estimate vs study size/precision (descriptive only) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary (Q, I², τ²) | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. *Introduction to Meta-Analysis*. 2nd ed. Chichester: Wiley; 2021.
4. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
5. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *J Educ Behav Stat*. 2005;30(3):261–293.
6. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
7. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med*. 2002;21(11):1539–1558.
8. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
9. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
10. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
11. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
12. Thompson SG, Higgins JPT. How should meta-regression analyses be undertaken and interpreted? *Stat Med*. 2002;21(11):1559–1573.
13. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.
14. Dworkin RH, Turk DC, Wyrwich KW, et al. Interpreting the clinical importance of treatment outcomes in chronic pain clinical trials: IMMPACT recommendations. *J Pain*. 2008;9(2):105–121.
15. Stanton-Hicks M, Jänig W, Hassenbusch S, Haddox JD, Boas R, Wilson P. Reflex sympathetic dystrophy: changing concepts and taxonomy. *Pain*. 1995;63(1):127–133.
16. O'Connell NE, Wand BM, Gibson W, Carr DB, Birklein F, Stanton TR. Local anaesthetic sympathetic blockade for complex regional pain syndrome. *Cochrane Database Syst Rev*. 2016;(7):CD004598.
17. Arcidiacono PG, Calori G, Carrara S, McNicol ED, Testoni PA. Celiac plexus block for pancreatic cancer pain in adults. *Cochrane Database Syst Rev*. 2011;(3):CD007519.
18. Hróbjartsson A, Gøtzsche PC. Placebo interventions for all clinical conditions. *Cochrane Database Syst Rev*. 2010;(1):CD003974.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| pain score at 14 days | 3 | Mean Difference (MD) | Yes | -0.2613 [-1.0954, 0.5729] |
