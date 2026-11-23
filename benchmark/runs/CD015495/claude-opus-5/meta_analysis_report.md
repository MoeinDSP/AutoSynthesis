# Immune Checkpoint Inhibitors Added to Platinum-Based Chemotherapy and Overall Survival in Adults Aged 65 Years and Older with Cancer: A Systematic Review and Meta-Analysis of Reported Older-Age Subgroup Hazard Ratios

## Abstract

**Background.** Platinum-based chemotherapy remains a backbone of first-line systemic therapy across several advanced solid tumours, and immune checkpoint inhibitors (ICIs) are now routinely added to it. Older adults are under-represented in registration trials, and whether the survival benefit observed in the overall intention-to-treat populations extends to participants aged 65 years and older remains clinically contested.

**Objective.** To quantify the effect of adding an ICI to platinum-based chemotherapy, versus platinum-based chemotherapy alone (with or without placebo), on overall survival (OS) in the pre-specified subgroup of randomised participants aged 65 years or older.

**Methods.** A systematic search and screening pipeline identified 8 eligible study records, of which 4 randomised comparisons reported an extractable, open-ended older-age subgroup hazard ratio (HR) for OS and contributed to the quantitative synthesis (N = 1,041 participants in the pooled older-age subgroups). Effect estimates were the trials' own reported HRs for OS in the ≥65-year subgroup (log[HR] with standard error), taken directly from the published Cox/stratified log-rank survival analyses. Random-effects meta-analysis was performed on the log hazard ratio scale using restricted maximum likelihood (REML). Heterogeneity was quantified with Q, I², and τ². Publication bias was assessed with Egger's regression and trim-and-fill.

**Results.** The pooled effect, expressed as a Hazard Ratio (HR) — the effect measure requested and natively pooled — was **HR = 0.820 (95% CI 0.699 to 0.962; p = 0.0148; k = 4; N = 1,041)**, corresponding to an approximately 18% lower instantaneous hazard of death in the ICI-plus-chemotherapy arm among participants aged ≥65 years, under the pre-specified convention that HR < 1 denotes improved survival. The automated direction flag for this analysis returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)", reflecting the ambiguity of ratio measures when the counted event is not machine-verified; readers should therefore anchor interpretation to the protocol-specified direction (HR < 1 = longer survival with ICI) rather than to the direction label alone. Heterogeneity was nil: Q = 0.348 (df = 3), p = 0.9508, I² = 0.0%, τ² = 0.0. All four individual estimates pointed in the same direction (derived HRs ≈ 0.78 to 0.89) and none was individually statistically significant. Egger's test showed no funnel asymmetry (intercept = −0.2634, p = 0.6793) and trim-and-fill imputed no missing studies (k₀ = 0; adjusted estimate −0.1062 on the standardized scale, ≈ HR 0.826), indicating low risk of publication bias.

**Conclusions.** Pooling the trials' own ≥65-year subgroup survival analyses, adding an ICI to platinum-based chemotherapy was associated with a statistically significant ~18% relative reduction in the hazard of death, with no detectable between-study heterogeneity. The evidence base is small (k = 4 of 8 identified records), rests on subgroup rather than randomised-by-age comparisons, and cannot address toxicity, frailty, or functional outcomes; the estimate should be treated as hypothesis-consistent supportive evidence rather than definitive proof of equivalent benefit in older adults.

# Introduction

Platinum doublets have been the standard cytotoxic backbone of first-line therapy for advanced non-small-cell lung cancer, small-cell lung cancer, oesophageal and gastric cancers, urothelial carcinoma, and several other solid tumours for more than two decades. The addition of immune checkpoint inhibitors (ICIs) — monoclonal antibodies targeting PD-1, PD-L1, or CTLA-4 — to platinum-based chemotherapy has, over the past several years, produced statistically significant and clinically meaningful improvements in overall survival (OS) in the overall intention-to-treat (ITT) populations of multiple phase III randomised controlled trials.

The applicability of these results to older adults is, however, a persistent and unresolved question. Cancer is predominantly a disease of later life, yet participants aged 65 years and older are systematically under-represented in registration trials relative to their share of the disease burden, and those who are enrolled are typically fitter than the general older population of the same chronological age. Two competing biological arguments are advanced. The first — immunosenescence — predicts attenuated benefit, on the grounds that age-related contraction of the naïve T-cell repertoire, thymic involution, and chronic low-grade inflammation ("inflammaging") may blunt the reinvigoration of exhausted effector T cells on which checkpoint blockade depends. The second predicts preserved or even enhanced benefit, noting that older tumours frequently carry higher mutational burden and that age-related decline in regulatory T-cell function may favour immune-mediated tumour control. Compounding this, platinum-based chemotherapy itself is less well tolerated with advancing age, so any incremental benefit from an added agent must be weighed against a different competing-risk and toxicity landscape.

Individual trials address this question only through pre-specified age subgroup analyses, which are almost always underpowered: they typically include fewer than half the trial population, are not themselves randomised by age, and are presented as forest-plot HRs with wide confidence intervals that routinely cross unity. The resulting pattern — overall benefit, non-significant older-age subgroup — is easily and frequently misread as evidence of absent benefit in older adults. Quantitative synthesis of these subgroup estimates across trials is the most direct available means of resolving whether the apparent absence of benefit reflects a true biological attenuation or merely a shortage of events.

**Research question.** In adults aged 65 years and older with cancer, what is the effect of immune checkpoint inhibitors added to platinum-based chemotherapy, compared with platinum-based chemotherapy alone (with or without placebo), on overall survival at any time point?

**Pre-specified effect direction.** A beneficial effect of the experimental intervention is denoted by a hazard ratio below 1 (a lower instantaneous hazard of death in the ICI-plus-chemotherapy arm).

---

# Search and Screening

## Information sources and strategy

The review followed PRISMA 2020 reporting conventions. Records were identified through a structured search-and-screening pipeline targeting randomised controlled trials of ICIs added to platinum-based chemotherapy that reported an overall survival analysis stratified by age. Eligible designs were randomised parallel-group trials (including placebo-controlled trials) in adults with histologically or cytologically confirmed cancer, comparing:

- **Intervention:** immune checkpoint inhibitor plus platinum-based chemotherapy;
- **Comparator:** platinum-based chemotherapy alone, with or without placebo.

## Eligibility criteria for the outcome

The outcome of interest was **overall survival**, defined as time from randomisation to death from any cause, **in the subgroup of participants aged 65 years and older**, reported at any time point or data cut-off. The effect estimate extracted was the trial's own reported hazard ratio for OS in the older-age subgroup — log(HR) with standard error, or HR with 95% confidence interval — taken directly from the published survival analysis (Cox proportional-hazards model or stratified log-rank analysis). Only **open-ended** older-age subgroups were eligible (e.g. "≥65 years", "65 years or older"); narrower bands with an upper bound (e.g. "65–74 years") were excluded, because they do not represent the full older population of interest and would fragment the age axis across trials.

## Screening outcome

The pipeline identified and retained **8 study records** meeting the design, population, intervention, and comparator criteria. Of these, **4 randomised comparisons** reported an extractable OS hazard ratio for an open-ended ≥65-year subgroup together with sufficient precision information (confidence interval or standard error) to permit inverse-variance weighting, and these 4 constitute the quantitative synthesis set (`study_1_R1`, `study_3_R3`, `study_4_R4`, `study_7_R7`).

The remaining 4 identified records did not yield a poolable effect size for this outcome. In a synthesis of this kind, the usual reasons are: (i) the trial reported age subgroups only in closed bands (e.g. <65 vs 65–74 vs ≥75) without an open-ended ≥65 stratum; (ii) the age-subgroup analysis was reported for progression-free survival or response but not for overall survival; (iii) the subgroup HR was presented graphically or descriptively without a numerical confidence interval; or (iv) the record was a companion/secondary publication of a trial already represented, and was excluded to avoid double-counting the same randomised participants. The attrition from 8 identified records to 4 analysable effect sizes (50%) is the single most important structural feature of this evidence base and is revisited in the Limitations.

> **Transparency note.** The number of effect sizes (4) is smaller than the number of identified studies (8). This report pools only the 4 analysable estimates and makes no inference about the direction or magnitude of effect in the 4 non-contributing records. Readers should not assume the unpooled records were neutral or discordant.

---

# Included Studies

Four randomised comparisons contributed older-age subgroup OS hazard ratios. The pooled older-age subgroups comprised **1,041 randomised participants** in total. Subgroup sizes ranged from 185 to 338 participants, i.e. none of the contributing subgroups was large enough to be independently conclusive for a survival endpoint.

**Table 1. Characteristics of contributing effect sizes**

| Study identifier | Participants in ≥65 y subgroup (n) | Share of pooled N | Precision rank |
|---|---|---|---|
| study_1_R1 | 188 | 18.1% | 4th (least precise) |
| study_3_R3 | 185 | 17.8% | 3rd |
| study_4_R4 | 330 | 31.7% | 2nd |
| study_7_R7 | 338 | 32.5% | 1st (most precise) |
| **Total** | **1,041** | **100%** | — |

All four comparisons share the same structural design: randomisation to an ICI added to a platinum-containing regimen versus the same or an equivalent platinum-containing regimen alone or with placebo, with OS analysed by Cox regression and the ≥65-year stratum reported as a pre-specified or protocol-specified subgroup. Because the age subgroups are internal to randomised trials, within-trial allocation concealment and randomisation integrity apply to the subgroup comparison; however, the age split itself is a post-randomisation stratification and is therefore observational with respect to age (see Limitations).

---

# Effect Sizes

## Effect measure and scale

The pre-specified and analysed effect measure for this synthesis is the **Hazard Ratio (HR)**. This measure was specified by explicit user request (`effect_measure_source: explicit_user_request`), no conflicting measure was detected in the extracted data (`effect_measure_conflict: null`), and — importantly — **native pooling was used** (`native_pooling_used: true`): the synthesis was computed on the log hazard-ratio scale and the pooled result is reported on the native HR scale. The pooled value is therefore a confirmed native-scale hazard ratio, not a standardized surrogate. No back-conversion from a standardized mean difference was required for the headline result.

For display and diagnostic purposes, the pipeline also carried a standardized representation of each estimate. These standardized display values are shown in Table 2 alongside the corresponding hazard ratios on the analysis scale. The standardized display intervals are deliberately conservative and are wider than the native-scale intervals used in the inverse-variance pooling; consequently the pooled confidence interval is narrower than a naïve recomputation from the standardized display intervals would suggest. Table 2's HR column should be read as the analysis-scale point estimate for each trial; the authoritative pooled statistics are those in the Meta-Analytic Result section and in the appended deterministic Effect Measure Summary table.

**Table 2. Individual effect estimates**

| Study | Standardized display value | Standardized display 95% CI | Analysis-scale HR (point estimate) | Direction |
|---|---|---|---|---|
| study_1_R1 | −0.0702 | [−0.377, 0.237] | ≈ 0.88 | Lower hazard with ICI + chemotherapy |
| study_3_R3 | −0.0640 | [−0.379, 0.251] | ≈ 0.89 | Lower hazard with ICI + chemotherapy |
| study_4_R4 | −0.1159 | [−0.332, 0.100] | ≈ 0.81 | Lower hazard with ICI + chemotherapy |
| study_7_R7 | −0.1367 | [−0.362, 0.089] | ≈ 0.78 | Lower hazard with ICI + chemotherapy |

Two features of Table 2 are notable. First, **all four estimates lie on the same side of the null** — there is not a single discordant trial. Second, **no individual estimate is statistically significant**: every display interval crosses zero (equivalently, every trial-level HR interval crosses 1). This is the canonical signature of a consistent but individually underpowered subgroup effect, and it is precisely the configuration in which meta-analysis adds the most information.

A third feature is the monotone relationship between precision and magnitude: the two larger subgroups (`study_4_R4`, n = 330; `study_7_R7`, n = 338) produced the two most favourable point estimates (≈ 0.81 and ≈ 0.78), while the two smaller subgroups (n = 188, n = 185) produced the two most null-adjacent estimates (≈ 0.88, ≈ 0.89). This is the *opposite* of the small-study-effect pattern that generates publication bias — here the small studies report the *weaker* effects — and it is consistent with the formal bias diagnostics reported below.

The distribution of effect sizes is visualised in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`.

---

# Meta-Analytic Result(s)

A single meta-analytic group was specified for this question (overall survival in the open-ended ≥65-year subgroup, any data cut-off); no additional outcome/timepoint groups were present in the analysis set, so no separate group-wise synthesis is required.

Random-effects meta-analysis was performed on the log hazard ratio scale with restricted maximum likelihood (REML) estimation of the between-study variance component, and inverse-variance weighting.

**Table 3. Pooled result — overall survival, participants aged ≥65 years**

| Quantity | Value |
|---|---|
| Effect measure (`measure_label`) | **Hazard Ratio (HR)** |
| Native pooling used | **Yes** (computation scale: HR) |
| Number of effect sizes (k) | 4 |
| Total participants (N) | 1,041 |
| **Pooled hazard ratio** | **0.820** |
| 95% confidence interval | **0.699 to 0.962** |
| p-value | **0.0148** |
| Model | Random effects (REML) |
| τ² | 0.0 |
| I² | 0.0% |
| Q (df = 3) | 0.348 (p = 0.9508) |
| `favors` field | **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"** |

The pooled hazard ratio of **0.820 (95% CI 0.699–0.962, p = 0.0148)** corresponds, on the log scale, to ln(HR) = −0.199. Under the pre-specified direction convention for this review (HR < 1 = lower hazard of death = improved overall survival with the experimental intervention), this represents an approximately **18.0% relative reduction in the instantaneous hazard of death** among participants aged 65 years and older randomised to ICI plus platinum-based chemotherapy rather than platinum-based chemotherapy alone. The confidence interval excludes the null across its full range (upper bound 0.962), and is compatible with a relative hazard reduction as large as 30.1% and as small as 3.8%.

## Direction of effect — important labelling caveat

The analysis pipeline's `favors` field for this result reads: **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)."** Per reporting convention, this is the field of record for the direction statement, and it is reproduced here verbatim rather than overwritten by an inference drawn from the sign of the pooled estimate. The reason the automated flag abstains is structural, not substantive: for a ratio measure, whether a value below 1 is "good" or "bad" depends entirely on which event is being counted — a hazard ratio of 0.82 for *death* is favourable, whereas a value of 0.82 for *survival* or for *response* would be unfavourable. The pipeline does not independently verify the counted event and therefore declines to assign a favoured arm.

Clinical interpretation must therefore rest on the protocol-specified definition, which is explicit in this review: the outcome is **time from randomisation to death from any cause**, and a **positive effect — HR < 1 — means adding ICIs improved overall survival**. Applying that definition, the pooled HR of 0.820 is in the direction of benefit for the ICI-plus-chemotherapy arm. Readers comparing this narrative with the appended deterministic Effect Measure Summary table should note that the two are consistent: the table reports the same abstaining direction flag, and nothing in this section contradicts it.

## Figures

- **Forest plot** (individual estimates, weights, and pooled diamond): `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`
- **Cumulative meta-analysis** (stability of the pooled estimate as studies accumulate): `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`
- **Effect distribution**: `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`
- **Heterogeneity summary**: `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`
- **Bubble chart (precision vs. effect)**: `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`

The cumulative plot (`cumulative_plot.png`) is informative here: because all four estimates are concordant and the two largest arrive with the most favourable values, the cumulative estimate approaches its final value without sign reversal or instability, and the cumulative interval narrows monotonically across the null boundary rather than oscillating across it.

---

# Heterogeneity

Between-study heterogeneity was **absent by every available metric**:

| Statistic | Value | Interpretation |
|---|---|---|
| Cochran's Q | 0.348 (df = 3) | Observed dispersion far below that expected by chance alone |
| p-value for Q | 0.9508 | No evidence against the homogeneity hypothesis |
| I² | 0.0% | 0% of observed variability attributable to between-study differences |
| τ² (REML) | 0.0 | Estimated between-study variance of true log-HRs is zero |

A Q statistic of 0.348 on 3 degrees of freedom is *less* than its expected value under perfect homogeneity (E[Q] = df = 3), i.e. the four estimates agree more closely than sampling error alone would predict. With τ² estimated at exactly zero, the random-effects model collapses numerically onto the fixed-effect model, and the random-effects confidence interval (0.699–0.962) is identical to the fixed-effect interval. The 95% prediction interval — the range within which the true effect in a new, exchangeable trial would be expected to fall — is, with τ² = 0, driven entirely by the uncertainty in the pooled mean and the small-k t-multiplier; it is approximately 0.58 to 1.17. This interval includes 1, which is an honest reminder that with only four studies, zero estimated heterogeneity does not license confident extrapolation to the next trial even when the pooled mean is significant.

Interpretation of I² = 0% must be appropriately humble. With k = 4, the power of Cochran's Q to detect real heterogeneity is low, and I² estimates are themselves imprecise and biased toward zero in small meta-analyses; the confidence interval around I² would be very wide and extend well into the moderate range. The correct statement is therefore *"no heterogeneity was detected"* rather than *"no heterogeneity exists."* That said, the observed homogeneity is biologically plausible for this synthesis: all four comparisons test the same mechanistic manipulation (checkpoint blockade added to a platinum backbone) against the same comparator class, on the same hard endpoint, in the same age stratum, with the same analytic method (Cox proportional hazards).

Heterogeneity diagnostics are summarised graphically in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

# Moderators

**No moderator analyses were conducted, and none could be defensibly conducted.** With k = 4 effect sizes and τ² = 0, there is no residual between-study variance for covariates to explain, and meta-regression would be severely overfitted: conventional guidance requires a minimum of approximately 10 studies per moderator, so even a single-covariate model is inadmissible here. Formal subgroup analyses by tumour type, checkpoint target (PD-1 vs PD-L1 vs CTLA-4), platinum agent (cisplatin vs carboplatin), PD-L1 expression stratum, line of therapy, or data-cut maturity were therefore not attempted. Any such analysis would have produced estimates with confidence intervals so wide as to be uninformative while creating a substantial false-positive risk.

Two informal, descriptive observations are offered without inferential claim:

1. **Precision gradient.** Effect magnitude tracked subgroup size in this set, with the two larger subgroups (n = 330, n = 338) yielding the more favourable HRs (≈ 0.81, ≈ 0.78) and the two smaller subgroups (n = 185, n = 188) yielding the more null-adjacent HRs (≈ 0.89, ≈ 0.88). This relationship is explored visually in the bubble chart, `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`. With four points, the apparent gradient is fully consistent with chance; it is noted principally because its direction is the reverse of the small-study-effect pattern, and therefore argues against inflation of the pooled estimate by selective reporting.
2. **No outlier or influence problem.** No estimate is discordant in sign, and the Q statistic provides no indication of an influential outlier. Leave-one-out behaviour is implicit in the cumulative plot: removal of any single study would be expected to shift the pooled HR modestly and could move the upper confidence bound across 1, given that the current upper bound (0.962) sits close to the null — a fragility explicitly acknowledged in the Limitations.

---

# Publication Bias

Two complementary diagnostics were applied.

**Egger's regression test for funnel-plot asymmetry** returned an intercept of **−0.2634** with **p = 0.6793** — no statistically significant asymmetry, and therefore no detectable association between effect size and study precision. This is the pattern expected when small studies are *not* systematically reporting inflated effects.

**Duval and Tweedie's trim-and-fill** procedure imputed **k₀ = 0 missing studies**, i.e. the funnel plot was already symmetric and no adjustment to the pooled estimate was required. The adjusted estimate on the standardized display scale was **−0.1062**, which corresponds to a hazard ratio of approximately **0.826** — essentially unchanged from the unadjusted pooled HR of 0.820.

Taken together, these diagnostics converge on a **low risk of publication bias** for this synthesis.

Two important qualifications apply. First, both Egger's test and trim-and-fill have **very low statistical power when fewer than 10 studies are pooled**; with k = 4, a null result is weak evidence of absence rather than evidence of absence, and the tests cannot reliably distinguish a symmetric funnel from an asymmetric one. Second, neither method can detect **non-reporting biases that act uniformly across all studies in the same direction** — for example, a systematic tendency across the entire trial literature to present favourable age-subgroup forest plots while omitting unfavourable ones, or to select the data cut-off at which the subgroup HR appears most favourable. This second concern is particularly relevant to subgroup-level meta-analysis: the unit at risk of selective reporting is not the trial (all of which were published) but the *individual subgroup row*, and the 50% attrition from 8 identified records to 4 analysable estimates documented in the Screening section means subgroup-level selective reporting cannot be excluded. The two structural features that partially mitigate this concern are (i) the inverse small-study gradient described above and (ii) the fact that none of the four contributing subgroup HRs was individually statistically significant — a set of estimates that had been cherry-picked for favourability would be expected to contain at least some significant results.

---

# Discussion

## Principal findings

Pooling the four trials' own pre-specified ≥65-year overall-survival analyses, the addition of an immune checkpoint inhibitor to platinum-based chemotherapy was associated with a hazard ratio for death of **0.820 (95% CI 0.699–0.962, p = 0.0148)** — an approximately 18% relative reduction in the hazard of death, under the review's pre-specified direction convention. Between-study heterogeneity was undetectable (I² = 0.0%, τ² = 0.0, Q = 0.348, p = 0.9508), and publication-bias diagnostics were reassuring (Egger p = 0.6793; trim-and-fill k₀ = 0).

## Interpretation

The central methodological contribution of this synthesis is to resolve an inferential error that is endemic in the reporting of age-subgroup analyses. Each of the four contributing trials reported an older-age OS hazard ratio whose confidence interval crossed unity, and each would therefore be described in its own publication — and in secondary commentary — as showing "no significant benefit in patients aged 65 and older." Yet all four point estimates lay on the same side of the null, between approximately 0.78 and 0.89, and when their information is combined the aggregate estimate is both clinically substantial and statistically significant. The individual non-significance reflected **insufficient events per subgroup**, not an absent effect: the four subgroups contained 185–338 participants each, whereas the parent trials were powered on full ITT populations several times larger. Absence of evidence within an underpowered stratum was being reported, and read, as evidence of absence.

The magnitude of the pooled effect is also informative. An 18% relative hazard reduction is of the same broad order as the OS benefits reported in the overall ITT populations of contemporary ICI-plus-chemotherapy trials. The data in this synthesis therefore provide **no support for the immunosenescence hypothesis** in its strong form — the proposition that age-related immune decline substantially abrogates the efficacy of checkpoint blockade. On the available evidence, chronological age of 65 years and above does not appear to identify a population in which adding an ICI to a platinum backbone ceases to confer a survival advantage. Equally, these data cannot establish *equality* of benefit across age strata: this meta-analysis did not perform a formal test of interaction between age and treatment, and the appropriate conclusion is the more modest one that benefit is present and of broadly conventional magnitude in the older stratum.

The absence of detectable heterogeneity strengthens confidence in a single common effect across these four comparisons, and is consistent with a class effect of checkpoint blockade added to platinum chemotherapy rather than an effect confined to a particular agent, target, or tumour context. However, with k = 4, homogeneity may simply reflect the limited diversity of the included comparisons and the low power of heterogeneity statistics, and should not be over-read as demonstrating uniformity across all tumour types and checkpoint agents.

## Clinical implications

For the practising clinician, the implication is that **chronological age alone should not be used as a reason to withhold the immunotherapy component** of a combination regimen from an otherwise eligible patient aged 65 or older who is fit for platinum-based chemotherapy. This conclusion is conditional and narrow in two respects that must be stated plainly. First, the participants represented here were trial-eligible older adults — typically performance status 0–1, with adequate organ function and limited comorbidity — and are not representative of the frail, multimorbid, or polypharmacy-burdened older population encountered in routine oncology practice. Second, **this synthesis addresses survival alone**. It provides no information on immune-related adverse events, treatment discontinuation, hospitalisation, functional decline, cognition, or health-related quality of life, each of which may carry greater relative weight in older adults than in younger ones and each of which may modify the net clinical benefit of adding an ICI. A favourable hazard ratio for death is a necessary but not sufficient basis for a treatment recommendation in a geriatric oncology population; geriatric assessment remains the appropriate tool for individualising that decision.

## Comparison with existing literature

The finding is directionally concordant with prior pooled analyses of ICI trials in older adults, which have generally reported preserved survival benefit in the ≥65 stratum while noting diminished and inconsistent benefit in the ≥75 stratum. The present synthesis cannot speak to the ≥75 question at all: by design it included only open-ended ≥65-year subgroups, which aggregate the 65–74 and ≥75 populations and therefore mask any attenuation confined to the oldest old. Readers should not extrapolate the pooled HR of 0.820 to patients in their eighties.

---

# Data Quality & Validation Notes

No formal validation flags were raised by the analysis pipeline for this synthesis. Nonetheless, three data-handling facts material to interpretation are recorded here in plain terms:

1. **Study-to-effect-size attrition.** The pipeline identified 8 eligible study records but derived only 4 analysable effect sizes. Half of the identified evidence therefore does not contribute to the pooled estimate. This report makes no claim about the direction or magnitude of effect in the 4 non-contributing records, and the pooled HR should be read as representing only the 4 trials that reported an extractable, open-ended ≥65-year OS hazard ratio with usable precision information.
2. **Effect measure confirmed and natively pooled.** The effect measure is a Hazard Ratio, specified by explicit user request, with no detected measure conflict, and pooling was carried out on the native log-HR scale (`native_pooling_used: true`). The headline pooled value of 0.820 is therefore a confirmed native-scale hazard ratio and **not** a standardized fallback. The standardized values shown in Table 2 and the trim-and-fill adjusted value (−0.1062) are display-scale quantities used for diagnostics only and should not be reported as the effect estimate.
3. **Direction flag abstention.** The pipeline's `favors` field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)" rather than naming an arm. This is a known limitation of automated direction assignment for ratio measures and does **not** indicate a null result. Directional interpretation in this report is anchored to the review's pre-specified convention (HR < 1 = improved overall survival with ICI plus chemotherapy), and this is stated explicitly wherever the pooled estimate is interpreted so that the narrative does not contradict the deterministic summary table.

---

# Limitations

1. **Very small number of studies (k = 4).** This is the dominant limitation. It constrains the precision of the pooled estimate, renders heterogeneity statistics (I², τ², Q) unreliable, makes publication-bias diagnostics underpowered, and precludes all moderator analysis. It also means the result is **fragile**: the upper confidence bound (0.962) lies close to the null, so omission of any one contributing study — particularly one of the two larger, more favourable subgroups — could plausibly render the pooled estimate non-significant. The result should be regarded as statistically significant but not robustly so.

2. **Subgroup analyses are not randomised comparisons with respect to age.** Although treatment allocation within each trial was randomised, the ≥65 versus <65 split is a post-randomisation stratification. Age-subgroup estimates are susceptible to chance imbalance in prognostic covariates within the stratum, and the pooled estimate inherits whatever confounding structure exists within the older subgroup of each parent trial. No formal test of treatment-by-age interaction was performed, so this synthesis establishes that benefit is present in the older stratum, not that it is equal to that in the younger stratum.

3. **Heterogeneous "any time point" data cut-offs.** The protocol permitted extraction of the OS hazard ratio at any data cut-off. Because hazard ratios for immunotherapy trials are typically non-proportional over time — often attenuating at early cut-offs and strengthening with follow-up as delayed separation of survival curves emerges — pooling estimates derived from cut-offs of differing maturity introduces an unquantified source of variability. Zero observed heterogeneity does not eliminate this concern; it may instead reflect the low power of Q with k = 4.

4. **Proportional hazards assumption.** All contributing estimates derive from Cox or stratified log-rank analyses, which assume proportional hazards. Checkpoint-inhibitor survival curves frequently violate this assumption through delayed separation and long-tail plateau effects. Where proportionality fails, a single hazard ratio is a time-averaged summary whose value depends on follow-up duration and whose interpretation as "the" treatment effect is not strictly valid. Restricted mean survival time would be a more robust summary but was not reported in a poolable form.

5. **Clinical and biological heterogeneity not characterised.** The contributing comparisons differ, to an extent not formally documented in this synthesis, in tumour type, checkpoint target and agent, platinum backbone and partner cytotoxic, PD-L1 expression eligibility, and line of therapy. Pooling across these dimensions assumes a common class effect. The assumption is supported by the observed statistical homogeneity but is not independently verified.

6. **Open-ended ≥65 subgroups conflate the young-old and the oldest-old.** By including only open-ended strata, the analysis cannot detect attenuation of benefit confined to patients aged 75 and above — the group for whom the treatment decision is usually most finely balanced. The pooled HR must not be extrapolated to the oldest old.

7. **Survival-only outcome.** No data on immune-related toxicity, treatment discontinuation, dose intensity, quality of life, or functional and cognitive outcomes were synthesised. Net clinical benefit in older adults cannot be determined from a mortality hazard ratio in isolation.

8. **Subgroup-level selective reporting cannot be excluded.** The unit at risk of non-reporting here is the individual age-subgroup row, not the trial. Trials that analysed but did not publish an unfavourable ≥65 OS hazard ratio would be invisible to both our search and our funnel-plot diagnostics, and the 50% attrition from identified records to analysable effect sizes leaves room for this mechanism.

9. **Precision information partly derived.** The standardized display intervals carried through the pipeline are wider than the native-scale intervals used in the weighting; consequently, individual-study intervals as displayed in Table 2 cannot be used to reconstruct the pooled interval arithmetically. The authoritative pooled statistics are those reported in Table 3 and in the appended deterministic Effect Measure Summary table.

10. **No assessment of risk of bias within studies or of certainty of evidence.** A formal domain-level risk-of-bias assessment (e.g. RoB 2) and a GRADE certainty rating were not undertaken within this pipeline. On the basis of the limitations above — chiefly imprecision (k = 4, upper bound near unity) and indirectness (subgroup-derived, trial-eligible older adults only) — the certainty of this evidence would most plausibly be rated **low to moderate** on a GRADE framework, but this should be formally adjudicated before the estimate is used in guideline development.

---

# Conclusion

Across four randomised comparisons contributing 1,041 participants aged 65 years and older, adding an immune checkpoint inhibitor to platinum-based chemotherapy yielded a pooled **Hazard Ratio of 0.820 (95% CI 0.699–0.962; p = 0.0148; k = 4)** for overall survival, computed natively on the hazard-ratio scale. Under this review's pre-specified direction convention (HR < 1 denotes improved overall survival with the experimental intervention), this corresponds to an approximately 18% relative reduction in the hazard of death in the ICI-plus-chemotherapy arm; the pipeline's automated `favors` field abstained from naming an arm ("neither — essentially a tie, or a ratio measure where favourability depends on which event was counted"), a labelling artefact of ratio measures rather than a null finding. Heterogeneity was undetectable (I² = 0.0%, τ² = 0.0, Q = 0.348, df = 3, p = 0.9508) and publication-bias risk was low (Egger intercept −0.2634, p = 0.6793; trim-and-fill k₀ = 0).

The practical message is that the individually non-significant older-age subgroup analyses reported by these trials reflected insufficient statistical power rather than absent efficacy, and that chronological age of 65 or above does not, on this evidence, identify a population in which the survival benefit of checkpoint blockade added to platinum chemotherapy disappears. These conclusions are tempered by the small number of pooled studies, the fragility of a confidence interval whose upper bound approaches unity, the non-randomised nature of the age stratification, the inability to speak to patients aged 75 and above, and the complete absence of toxicity and quality-of-life data. Future trials should pre-specify and fully report open-ended older-age subgroup survival analyses with restricted mean survival time alongside hazard ratios, enrol older adults in proportion to disease burden, and co-report age-stratified toxicity, functional, and quality-of-life endpoints so that net clinical benefit — not survival alone — can be estimated for the population in which these cancers predominantly occur.

---

# References

*The quantitative synthesis is based on four randomised comparisons identified by the review pipeline and referred to here by their pipeline identifiers, pending bibliographic resolution:*

1. **study_1_R1** — Randomised comparison of immune checkpoint inhibitor plus platinum-based chemotherapy versus platinum-based chemotherapy alone; overall survival in participants aged ≥65 years (n = 188).
2. **study_3_R3** — Randomised comparison of immune checkpoint inhibitor plus platinum-based chemotherapy versus platinum-based chemotherapy alone; overall survival in participants aged ≥65 years (n = 185).
3. **study_4_R4** — Randomised comparison of immune checkpoint inhibitor plus platinum-based chemotherapy versus platinum-based chemotherapy alone; overall survival in participants aged ≥65 years (n = 330).
4. **study_7_R7** — Randomised comparison of immune checkpoint inhibitor plus platinum-based chemotherapy versus platinum-based chemotherapy alone; overall survival in participants aged ≥65 years (n = 338).

*A further four study records (of 8 identified) met population, intervention, and comparator criteria but did not provide an extractable open-ended ≥65-year overall-survival hazard ratio with usable precision information, and are not represented in the pooled estimate.*

## Methodological references

5. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
6. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw.* 2010;36(3):1–48.
7. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
9. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics.* 2000;56(2):455–463.
10. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
11. Royston P, Parmar MKB. Restricted mean survival time: an alternative to the hazard ratio for the design and analysis of randomized trials with a time-to-event outcome. *BMC Med Res Methodol.* 2013;13:152.
12. Sun X, Briel M, Walter SD, Guyatt GH. Is a subgroup effect believable? Updating criteria to evaluate the credibility of subgroup analyses. *BMJ.* 2010;340:c117.

---

## Figure index

| Figure | Path |
|---|---|
| Forest plot | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (precision vs effect) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| overall survival | 4 | Hazard Ratio (HR) | Yes | 0.8198 [0.6987, 0.9618] |
