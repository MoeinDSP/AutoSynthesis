# Rituximab versus Tacrolimus for Prevention of Relapse in Children with Steroid-Sensitive Nephrotic Syndrome: A Systematic Review and Random-Effects Meta-Analysis of Randomized Trials

## Abstract

**Background.** Steroid-sensitive nephrotic syndrome (SSNS) in children frequently follows a steroid-dependent (SDNS) or frequently relapsing (FRNS) course, exposing patients to cumulative corticosteroid toxicity. Both rituximab (an anti-CD20 monoclonal antibody) and tacrolimus (a calcineurin inhibitor) are used as steroid-sparing agents, but their comparative efficacy for relapse prevention is uncertain.

**Objective.** To determine whether rituximab, compared with tacrolimus, reduces the risk of nephrotic syndrome relapse within approximately 12 months of randomization in children with SSNS, including SDNS and FRNS phenotypes.

**Methods.** A systematic search and structured screening pipeline identified randomized trials comparing rituximab with tacrolimus in children with SSNS/SDNS/FRNS that reported the number of children experiencing one or more relapses (per ISKDC/KDIGO definitions) and the number randomized per arm at approximately 12 months. The pre-specified effect measure was the risk ratio (RR), pooled on its native scale using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was quantified with Cochran's Q, I², and τ². Small-study effects were examined with Egger's regression and trim-and-fill.

**Results.** Three randomized trials contributing three effect estimates and 194 randomized children met inclusion criteria. The pooled Risk Ratio (RR) for relapse by 12 months was 0.531 (95% CI 0.231 to 1.221; p = 0.136; k = 3; n = 194), estimated on the native RR scale (native pooling confirmed). Because the confidence interval comfortably includes the null and the p-value exceeds conventional thresholds, the pooled result favours **neither** arm — it is statistically consistent with a tie (or, for a ratio measure, with a direction that depends on which event was counted) and does not establish superiority of rituximab over tacrolimus. Heterogeneity was substantial and clinically important: Q = 5.669 (p = 0.0588), I² = 62.4%, τ² = 0.332552. The three per-study standardized estimates were markedly discordant in direction (0.000, 95% CI −0.620 to 0.620; 0.459, 95% CI −0.222 to 1.140; and −0.904, 95% CI −1.280 to −0.529), with the largest trial (n = 120) pointing away from the pooled summary. Egger's regression indicated strong funnel-plot asymmetry (intercept −2.4752, p = 0.0002) while trim-and-fill imputed no missing studies (k₀ = 0; adjusted estimate −0.1891); overall risk of small-study/publication bias was rated **high**.

**Conclusions.** In this small body of evidence, rituximab was not shown to reduce the risk of relapse by 12 months relative to tacrolimus in children with steroid-sensitive nephrotic syndrome. The pooled point estimate is numerically lower than the null but the interval is wide, heterogeneity is substantial, directions of individual trial effects conflict, and bias diagnostics are discordant and concerning. The evidence base (k = 3, n = 194) is too sparse and too heterogeneous to support a confident comparative recommendation; adequately powered head-to-head trials with harmonized 12-month relapse definitions are needed.

**Registration.** Not registered; this report documents a secondary analysis of a structured evidence-synthesis pipeline.

## 1. Introduction

Idiopathic nephrotic syndrome is the most common glomerular disease of childhood. Approximately 80–90% of affected children are steroid-sensitive (SSNS), achieving remission with corticosteroid therapy, but between 40% and 60% subsequently follow a frequently relapsing (FRNS) or steroid-dependent (SDNS) course. Repeated or continuous corticosteroid exposure in these children carries well-documented morbidity: growth impairment, obesity, hypertension, cataract, osteopenia, behavioural disturbance and adrenal suppression. The central therapeutic problem is therefore not the induction of remission but its durable maintenance with minimal steroid burden.

Two mechanistically distinct steroid-sparing strategies dominate contemporary practice. Calcineurin inhibitors — of which tacrolimus is now the most widely used in paediatric nephrology — suppress T-cell activation and have direct stabilizing effects on the podocyte actin cytoskeleton. They are effective but require continuous administration, therapeutic drug monitoring, and carry risks of nephrotoxicity, hypertension, glucose intolerance and cosmetic side effects; relapse on withdrawal ("calcineurin-inhibitor dependence") is common. Rituximab, a chimeric monoclonal antibody against CD20, depletes B lymphocytes and has produced striking remission durations in SDNS/FRNS in single-arm and placebo-controlled studies, with the practical advantage of intermittent intravenous dosing. Its risks include infusion reactions, hypogammaglobulinaemia, prolonged B-cell aplasia, neutropenia and rare severe infections.

KDIGO guidance acknowledges both agents as reasonable options for SDNS/FRNS but does not establish a hierarchy between them, reflecting a genuine evidence gap: most randomized data compare each drug against steroids, placebo, or mycophenolate mofetil rather than against each other. Direct head-to-head randomized comparisons of rituximab with tacrolimus are few and small.

**Research question.** In children with steroid-sensitive nephrotic syndrome (including steroid-dependent and frequently relapsing forms), does rituximab compared with tacrolimus reduce the risk of relapse by 12 months?

**Pre-specified effect direction.** A positive effect size (an RR favouring treatment, i.e. an RR below the null on the relapse-event scale) indicates that rituximab produced fewer relapses than tacrolimus — that is, rituximab lowered the risk of relapse by 12 months. Interpretation of direction in this report is taken from the analysis engine's `favors` field rather than inferred from the arithmetic sign of the summary statistic, because ratio measures and event-counting conventions can invert the apparent meaning of a raw sign.

---

## 2. Methods

### 2.1 Protocol and reporting standards

This report follows the PRISMA 2020 reporting framework for systematic reviews and meta-analyses. No prospective protocol was registered; the analysis documents the output of a structured, automated evidence-synthesis pipeline comprising document retrieval, document-type gating, outcome classification, effect-size extraction, and random-effects pooling. This absence of prospective registration is recorded as a limitation (Section 10).

### 2.2 Eligibility criteria

Studies were eligible if they satisfied all of the following:

- **Population (P):** Children (broadly, <18 years) with steroid-sensitive idiopathic nephrotic syndrome, including explicitly steroid-dependent and frequently relapsing phenotypes. Trials restricted to steroid-resistant nephrotic syndrome were not eligible for this comparison.
- **Intervention (I):** Rituximab (anti-CD20 monoclonal antibody), any dosing schedule.
- **Comparator (C):** Tacrolimus, as the calcineurin-inhibitor comparator arm.
- **Outcome (O):** Occurrence of nephrotic syndrome relapse — recurrence of proteinuria defined per standard ISKDC/KDIGO criteria — within approximately 12 months of randomization, extracted as the number of children experiencing one or more relapses and the total number randomized in each arm.
- **Study design (S):** Randomized controlled trials with a concurrent tacrolimus comparator arm.

Exclusions comprised: secondary/syndromic nephrotic syndrome; non-randomized and single-arm designs; studies without a 12-month (or approximately 12-month) relapse endpoint recoverable as a dichotomous count; and documents that were themselves evidence syntheses rather than primary trial reports (see Section 2.3 and Section 9).

### 2.3 Information sources, search and screening

Candidate records were retrieved from the pipeline's indexed bibliographic corpus and supplemented by manually supplied documents. All retrieved records passed through an automated **document-type gate** designed to separate primary randomized trial reports from secondary literature (narrative reviews, systematic reviews, meta-analyses, guidelines, editorials, protocols) and from duplicate reports of the same trial. Records surviving this gate were then screened against the PICOS criteria above, and the relapse-by-12-months outcome was located and classified within each eligible report.

One manually supplied document (internal identifier `manual:11fa224a`) was **excluded at the document-type gate** because it was classified as a systematic review or meta-analysis rather than a primary study. The gate's rationale was explicit: the document contained a PRISMA-guided database search, a study-selection flow diagram, formal risk-of-bias assessment of its included trials, pooled risk ratios and mean differences with forest plots, and heterogeneity and publication-bias analyses across eight included studies. Including such a document alongside primary trials would double-count participant data and artificially inflate precision; its exclusion is therefore methodologically correct, but it is reported transparently here (Section 9) because that document plausibly indexes additional primary trials that the present synthesis did not capture.

### 2.4 Data extraction

For each included trial, the following were extracted: trial identifier, number randomized to rituximab and to tacrolimus, number of children in each arm experiencing one or more relapses within approximately 12 months, and the resulting effect estimate with its confidence interval. Where the pipeline reported a standardized per-study estimate alongside the dichotomous counts, both were retained; the dichotomous counts formed the basis of the native-scale pooled analysis.

### 2.5 Effect measure and synthesis

The **pre-specified effect measure was the risk ratio (RR)** for relapse by 12 months (`measure_label`: "Risk Ratio (RR)"; `effect_measure_source`: explicit user request; no measure conflict detected). Critically, **native pooling was used and confirmed** (`native_pooling_used = true`): the pooled estimate reported below is a genuine RR computed on the risk-ratio scale, not a back-transformed standardized mean difference or other fallback approximation. No standardized-fallback caveat applies to the pooled summary.

Pooling used a **random-effects model with restricted maximum likelihood (REML)** estimation of the between-study variance τ², which was considered obligatory a priori given anticipated clinical and methodological diversity in rituximab dosing, tacrolimus target trough levels, concomitant steroid tapering protocols, and baseline relapse frequency.

Heterogeneity was quantified using Cochran's Q with its p-value, the I² statistic (proportion of total variability attributable to between-study heterogeneity rather than sampling error), and τ² (absolute between-study variance on the analysis scale). Prediction intervals were considered but are not reported as a primary quantity given k = 3, where such intervals are extremely unstable.

### 2.6 Small-study effects and publication bias

Funnel-plot asymmetry was assessed with **Egger's regression test** and with the **Duval and Tweedie trim-and-fill** procedure. Both diagnostics are acknowledged to be severely underpowered and potentially misleading with fewer than ten studies; results are presented and interpreted with that caveat made explicit rather than as definitive evidence.

### 2.7 Moderator analysis

Moderator (meta-regression and subgroup) analyses were planned for rituximab dose/schedule, tacrolimus trough target, proportion of SDNS versus FRNS participants, prior immunosuppressant exposure, and risk-of-bias domain ratings. Feasibility was conditional on study count.

---

## 3. Search and Screening Results

The screening cascade yielded the following:

| Stage | Records |
|---|---|
| Records entering document-type gate | All retrieved + manually supplied records |
| Excluded at document-type gate as systematic review / meta-analysis | 1 (`manual:11fa224a`) |
| Primary randomized trial reports meeting full PICOS criteria | **3** |
| Trials contributing extractable relapse-by-12-months data | **3** |
| Effect estimates entering quantitative synthesis | **3** |
| Total randomized children in the synthesis | **194** |

No records were excluded as duplicate reports of an already-included trial, and no eligible outcome failed classification. The single documented exclusion is the secondary-literature record described in Section 2.3.

The final evidence base is therefore **k = 3 randomized trials, n = 194 children** — a sparse base by the standards of comparative-effectiveness meta-analysis, and one that constrains every downstream inference in this report.

---

## 4. Included Studies

Three randomized trials comparing rituximab with tacrolimus for relapse prevention in paediatric SSNS/SDNS/FRNS contributed to the synthesis. Their sizes were markedly unequal, which has direct consequences for weighting and for the interpretation of heterogeneity.

| Study (pipeline label) | Randomized (n) | Standardized per-study estimate | 95% CI | Relative size |
|---|---|---|---|---|
| study_1 (R1) | 40 | 0.000 | [−0.620, 0.620] | Small |
| study_2 (R2) | 34 | 0.459 | [−0.222, 1.140] | Small |
| study_3 (R3) | 120 | −0.904 | [−1.280, −0.529] | Large (62% of total n) |
| **Total** | **194** | — | — | — |

The structural feature that dominates this dataset is immediately visible: one trial (study_3) enrolled 120 of the 194 children — nearly two-thirds of all participants — and its estimate lies in the **opposite direction** from the other two and from the pooled summary, with a confidence interval that excludes the null in that opposite direction. The two smaller trials (combined n = 74) produced estimates of exactly null (study_1) and modestly positive (study_2), neither individually statistically significant.

Precise descriptions of rituximab dosing (single versus multiple 375 mg/m² infusions, fixed versus weight-based dosing, retreatment on B-cell reconstitution), tacrolimus target troughs, concomitant prednisolone tapering, and relapse ascertainment frequency were not available at the level of granularity required for formal comparative tabulation in this secondary analysis. Their likely variation is treated as a source of clinical heterogeneity in Sections 6 and 10.

---

## 5. Effect Sizes

### 5.1 Per-study estimates

The three per-study estimates recorded by the pipeline, with 95% confidence intervals, were:

- **study_1_R1:** 0.000 (95% CI −0.620 to 0.620), n = 40. Exactly null; the confidence interval is symmetric about zero and wide, spanning what would conventionally be read as moderate benefit through moderate harm.
- **study_2_R2:** 0.459 (95% CI −0.222 to 1.140), n = 34. A moderate estimate in the direction of the rituximab arm on the standardized scale, but the interval crosses zero; this trial, the smallest in the set, is individually uninformative.
- **study_3_R3:** −0.904 (95% CI −1.280 to 0.529 → correctly, −1.280 to −0.529), n = 120. A large estimate in the direction opposite to study_2, with a confidence interval that **excludes** zero. This is the only individually "significant" trial in the set, and it points away from the pooled conclusion.

These per-study values are reported on the standardized scale used by the extraction layer for display and for the bias diagnostics. The pooled synthesis in Section 6, by contrast, was computed on the **native risk-ratio scale** from the underlying relapse counts, with native pooling confirmed. Readers should not attempt to reconcile the arithmetic of the three standardized per-study numbers directly with the native-scale pooled RR; the two live on different metrics, and the deterministic Effect Measure Summary table appended to this report is authoritative on measure labelling.

### 5.2 Qualitative pattern

The salient qualitative feature is **directional conflict**. One trial is exactly null, one leans one way, and the largest trial — carrying the greatest weight and the only non-null interval — leans decisively the other. This is not the pattern of a consistent treatment effect measured with noise; it is the pattern of either genuine effect modification across trial contexts or of differences in design, population, or outcome ascertainment that render the three estimates non-exchangeable. Either reading undercuts confidence in a single pooled summary as a faithful description of "the" rituximab-versus-tacrolimus effect.

---

## 6. Meta-Analytic Result

### 6.1 Primary pooled estimate

Random-effects (REML) pooling of the three trials on the native risk-ratio scale produced:

| Quantity | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** — native pooling confirmed |
| Studies (k) | 3 |
| Participants (n) | 194 |
| **Pooled Risk Ratio (RR)** | **0.531** |
| 95% confidence interval | **0.231 to 1.221** |
| p-value | **0.136** |
| τ² (between-study variance) | 0.332552 |
| I² | 62.4% |
| Cochran's Q | 5.669 (p = 0.0588) |
| Estimation method | REML random-effects |

### 6.2 Direction and interpretation

Per the analysis engine's `favors` field, the pooled result **favours neither arm** — it is "essentially a tie, or a ratio measure where favourability depends on which event was counted." This designation is used here in preference to any inference drawn from the numerical position of 0.531 relative to 1.0, consistent with the pre-specified rule that raw signs and ratio magnitudes retain a treatment-minus-control convention that can invert the apparent direction of benefit depending on the event counted.

Concretely, the inference supported by these data is as follows. The point estimate of the pooled Risk Ratio is 0.531, but its 95% confidence interval runs from 0.231 to 1.221 and therefore **includes the null value of 1.0**. The associated p-value of 0.136 does not reach conventional statistical significance at α = 0.05. The data are thus compatible with a substantial reduction in relapse risk (an RR as low as 0.231, i.e. a roughly 77% relative reduction), with no difference whatsoever, and with a modest increase in relapse risk in the rituximab arm (an RR as high as 1.221, i.e. a roughly 22% relative increase). **The hypothesis that rituximab reduces the risk of relapse by 12 months relative to tacrolimus is not confirmed by this synthesis.** The absence of statistical significance here should be read as genuine uncertainty arising from a very small evidence base with conflicting internal signals, not as demonstrated equivalence — the interval is far too wide to exclude clinically important differences in either direction.

### 6.3 Figures

- **Forest plot:** `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` — displays the three per-study estimates with confidence intervals and the random-effects summary diamond, making visually apparent both the directional conflict among trials and the summary interval's overlap of the null.
- **Cumulative meta-analysis:** `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` — shows how the running pooled estimate moves as trials accumulate; with k = 3 this is descriptive only and is highly sensitive to ordering.
- **Effect distribution:** `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` — illustrates the dispersion of the three estimates and the degree to which they fail to cluster.
- **Bubble chart:** `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` — plots effect magnitude against study size, visualizing the inverse relationship between precision and effect direction in this dataset.
- **Heterogeneity summary:** `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` — graphical summary of Q, I² and τ².

### 6.4 Outcome groups

The context data contained a single `meta_analysis` entry and no `meta_analysis_groups` with multiple members; all three trials contributed to the same outcome and timepoint (relapse within approximately 12 months of randomization). No separate outcome or timepoint strata therefore require independent reporting, and no group was flagged as having insufficient data for pooling.

---

## 7. Heterogeneity

Heterogeneity in this synthesis is **substantial and consequential**.

- **I² = 62.4%** indicates that approximately 62% of the observed variability across trial estimates reflects real between-study differences in effect rather than within-study sampling error. By the Cochrane Handbook's descriptive bands, this falls squarely in the "substantial heterogeneity" range (50–90%).
- **τ² = 0.332552** quantifies the absolute between-study variance on the analysis scale. This is a large value relative to the magnitude of the pooled effect itself and is the proximate reason the random-effects confidence interval is so wide: the REML model correctly inflates uncertainty to accommodate the dispersion it detects, and in doing so moves the interval across the null.
- **Cochran's Q = 5.669 on 2 degrees of freedom, p = 0.0588.** This is marginal by the conventional 0.05 threshold but, critically, Q is notoriously underpowered when k is small. With only three studies, a p-value of 0.0588 should be read as *supportive* of real heterogeneity, not as evidence of homogeneity. Taken alongside I² = 62.4% and the large τ², the coherent reading is that these three trials are estimating genuinely different quantities.

It must also be stated that with k = 3, **I² and τ² are themselves estimated with very poor precision**. The confidence interval around I² = 62.4% would be extremely wide, plausibly spanning from near-zero to over 90%. The point estimates are the best available description of this dataset, but they are fragile.

The qualitative evidence for heterogeneity is arguably stronger than the quantitative. The three per-study estimates are not merely dispersed in magnitude — they **conflict in direction**, with the largest and most precise trial (n = 120) producing a non-null estimate opposite to the direction of the smaller trials. When heterogeneity takes this form, the pooled mean is a poor summary of any individual trial's result and functions more as an arithmetic average of discordant findings than as an estimate of a common underlying effect. Plausible clinical sources include differences in rituximab dosing intensity and retreatment policy, tacrolimus trough targets and adherence, the mix of steroid-dependent versus frequently relapsing participants, prior immunosuppressive exposure, background steroid tapering schedules, the intensity and frequency of proteinuria monitoring, and the precise operationalization of "relapse" (consecutive-day dipstick thresholds versus protein:creatinine ratio cut-offs).

---

## 8. Moderator Analyses

**No moderator analyses were performed, and none were statistically feasible.**

With k = 3 studies, formal meta-regression is not interpretable: a single covariate model would leave one residual degree of freedom, and any resulting coefficient would be determined almost entirely by which trial happened to sit at the extreme of the covariate distribution. Guidance conventionally recommends a minimum of roughly ten studies per covariate; this dataset falls an order of magnitude short. Subgroup analysis is equally unavailable, since any split would produce strata of one or two trials.

The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) is provided as a **descriptive** visualization of the effect-size-by-study-size relationship. It should not be read as a fitted moderator model. Its visual content — larger trial, opposite-direction effect — is a restatement of the directional conflict described in Section 7, not an independent statistical finding.

Consequently, the substantial heterogeneity detected in Section 7 **remains entirely unexplained**. The pre-specified moderators (rituximab dose and retreatment schedule, tacrolimus trough target, SDNS versus FRNS proportion, prior immunosuppressant exposure, risk-of-bias domains) could not be examined. This is a material limitation: it means we can neither identify a subgroup in which rituximab might genuinely outperform tacrolimus nor exclude the possibility that the pooled null conceals real, clinically relevant effect modification.

---

## 9. Publication Bias and Small-Study Effects

Formal bias diagnostics returned a **discordant and concerning** picture, and the pipeline's overall small-study/publication-bias risk rating for this synthesis is **high**.

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | −2.4752 |
| Egger's test p-value | **0.0002** |
| Trim-and-fill imputed studies (k₀) | **0** |
| Trim-and-fill adjusted estimate | −0.1891 |
| Overall bias risk rating | **High** |

**Interpretation.** Egger's test provides strong statistical evidence of funnel-plot asymmetry (p = 0.0002), consistent with small-study effects. Yet trim-and-fill imputed no missing studies (k₀ = 0), meaning the pooled estimate is unchanged by that particular adjustment. This discordance indicates that the asymmetry is not a simple one-sided "gap" in the funnel of the kind trim-and-fill is designed to detect and fill. Instead, it may reflect genuine small-study effects, between-study heterogeneity, or systematic differences in study quality rather than straightforward suppression of null results. The high risk-of-bias rating is therefore justified, and **the null trim-and-fill result should not be read as reassurance**. Sensitivity analyses using contour-enhanced funnel plots, PET-PEESE, or formal selection models are warranted before drawing firm conclusions.

Two further cautions are essential. First, **both diagnostics are invalid at k = 3**. Egger's regression with three points fits a line through a near-saturated design; its p-value of 0.0002 is driven by the geometry of three widely dispersed points — in particular by the large, precise, opposite-direction trial — far more than by any reliable inference about selective publication. A p-value of this apparent strength from three studies should be treated as a signal that *something structural is wrong with the dataset's shape*, not as a quantified probability of publication bias. Second, the trim-and-fill adjusted value of −0.1891 is reported on the standardized display scale and, with k₀ = 0, represents no actual adjustment to the primary native-scale pooled RR of 0.531; it should not be substituted for the primary estimate.

The honest synthesis of Section 7 and Section 9 together is that heterogeneity and apparent asymmetry are two views of the same underlying problem: three trials that do not agree, dominated by one large trial pulling against the others, in an evidence base too small for any bias-correction method to operate reliably.

---

## 10. Data Quality and Validation Notes

The pipeline raised one validation flag, reported here in full and without mitigation:

- **Document-type gate exclusion (severity: warning).** One manually supplied document (`manual:11fa224a`) was excluded from the primary-study set because it was classified as a **systematic review or meta-analysis**, not a primary trial report. The classifier's stated basis was that the document is an explicit meta-analysis of randomized controlled trials, containing a PRISMA-guided database search, a study selection and inclusion flow chart, risk-of-bias assessment of its included trials, pooled risk ratios and mean differences with forest plots, and heterogeneity and publication-bias analyses across **eight** included studies.

**Plain-language implications.** This exclusion is methodologically correct — incorporating a meta-analysis as if it were a primary study would double-count participants and spuriously narrow confidence intervals. However, it carries a substantive warning for the present report: that excluded synthesis drew on **eight** included studies, whereas the current analysis located only **three** eligible primary trials. Some of that discrepancy will reflect differing eligibility criteria (the excluded review may have pooled comparators other than tacrolimus, or outcomes other than 12-month relapse), but the gap is large enough that **incomplete retrieval of eligible primary trials cannot be excluded**. The present pooled estimate may therefore rest on a subset of the available randomized evidence, and its point estimate could shift materially if additional trials were recovered and incorporated.

Additional data-quality observations:

- No outcomes failed classification; the relapse-by-12-months endpoint was identified in all three included trials.
- No effect measures required separate pooling; a single measure (RR) and a single outcome/timepoint group applied throughout.
- No trial reports were excluded for double-counting (no duplicate publications of the same trial were detected).
- Native pooling on the RR scale was confirmed (`native_pooling_used = true`), so the pooled summary is a genuine risk ratio and not a standardized fallback.
- Granular trial-level characteristics (dosing, trough targets, steroid tapers, relapse definitions, risk-of-bias domain judgements) were not available at the resolution needed for comparative tabulation or moderator modelling.

---

## 11. Discussion

This meta-analysis assembled three randomized trials (n = 194 children) comparing rituximab with tacrolimus for prevention of relapse in paediatric steroid-sensitive nephrotic syndrome. The pooled Risk Ratio for relapse within approximately 12 months was 0.531 (95% CI 0.231–1.221; p = 0.136), computed on the native risk-ratio scale. Per the analysis engine's direction field, this result **favours neither arm**. The research question — whether rituximab reduces the 12-month relapse risk relative to tacrolimus — is therefore answered in the negative *with respect to statistical demonstration*: the hypothesis is not supported by the available randomized evidence.

It is worth being careful about what that negative answer does and does not mean. The point estimate of 0.531 sits numerically below the null, and taken in isolation would correspond to a large relative reduction. Some readers will be tempted to treat the result as "promising but underpowered." Three features of this dataset argue against that reading being adopted uncritically. First, the confidence interval extends to 1.221, admitting the possibility that rituximab performs *worse* than tacrolimus. Second, and more importantly, the point estimate is not a consistent signal diluted by noise — it is an average over trials that **disagree in direction**, in which the single largest and most precise trial (n = 120, 62% of all participants) produced a non-null estimate pointing the other way. A pooled mean constructed from such components is a weak basis for clinical extrapolation. Third, the bias diagnostics flagged strong funnel asymmetry (Egger's p = 0.0002) with a high overall bias-risk rating, and the null trim-and-fill result provides no reassurance against it.

How does this sit against the wider literature? Rituximab has an unusually strong track record in SDNS/FRNS when compared with placebo or with steroid continuation, where randomized trials have shown meaningful prolongation of relapse-free survival and reduction in steroid burden. The present analysis does not contradict that: it addresses a different and harder question, namely whether rituximab is *superior to an active, effective comparator*. Tacrolimus is itself an efficacious steroid-sparing agent in this population, and demonstrating superiority over an effective active control requires both a larger effect and a larger sample than demonstrating superiority over placebo. A pooled estimate that cannot distinguish the two agents at 12 months is entirely consistent with both drugs being genuinely effective and broadly comparable over this horizon. It is also consistent with the two agents differing in ways that a binary 12-month relapse endpoint cannot capture — for example in time to first relapse, in cumulative steroid dose, in the trajectory of relapse risk after drug withdrawal, or in the tolerability and adherence burden that matters so much to families.

The absence of feasible moderator analysis is a particular loss here. Clinically plausible effect modifiers abound — rituximab dose intensity and whether retreatment is given on B-cell reconstitution; tacrolimus trough targets and adherence; the proportion of steroid-dependent versus frequently relapsing children; prior exposure to cyclophosphamide, mycophenolate or calcineurin inhibitors; and the stringency of relapse ascertainment. Any of these could generate the directional conflict observed. With k = 3 none could be tested, and so the heterogeneity (I² = 62.4%, τ² = 0.333) stands unexplained.

For clinical practice, the responsible conclusion is that this synthesis provides **no basis for preferring rituximab over tacrolimus**, nor tacrolimus over rituximab, for relapse prevention at 12 months in children with SSNS. Choice between the agents should continue to be individualized on the basis of adverse-effect profiles, adherence and monitoring feasibility, prior treatment history, venous access and infusion logistics, family preference, and cost — all of which this analysis leaves untouched.

For research, the priorities are clear: adequately powered head-to-head randomized trials with harmonized, pre-registered definitions of relapse; reporting of both binary relapse-by-12-months and time-to-relapse outcomes; longer follow-up extending beyond drug withdrawal; systematic reporting of cumulative steroid exposure and harms; and individual-participant-data pooling, which would allow the effect modification that aggregate meta-regression cannot address at this k to be examined directly.

---

## 12. Limitations

1. **Very small number of studies (k = 3).** This is the dominant limitation. It renders moderator analysis impossible, makes heterogeneity statistics (I², τ², Q) highly imprecise, and invalidates the standard publication-bias diagnostics. Random-effects estimation with three studies yields an unstable τ² and consequently an unstable confidence interval.
2. **Small total sample (n = 194).** The synthesis is underpowered to detect clinically modest differences between two active agents; a wide interval was essentially guaranteed by the sample size alone.
3. **Directional conflict among trials.** The largest trial (n = 120) produced the only individually non-null estimate, in the direction *opposite* to the pooled summary. The pooled mean may therefore not represent any real underlying common effect.
4. **Substantial unexplained heterogeneity.** I² = 62.4% and τ² = 0.333 with Q p = 0.0588; no source could be identified or adjusted for.
5. **High risk of small-study/publication bias with discordant diagnostics.** Egger's p = 0.0002 indicates strong asymmetry, but trim-and-fill imputed nothing (k₀ = 0). Neither test is valid at k = 3; the discordance itself is uninterpretable in a conventional sense and should be treated as a red flag rather than resolved in either direction.
6. **Possible incomplete retrieval.** A correctly excluded secondary synthesis in the corpus drew on eight included studies; the present analysis found three eligible primary trials. Incomplete capture of eligible randomized evidence cannot be excluded (Section 10).
7. **No formal risk-of-bias assessment at trial level.** Domain-level judgements (randomization, allocation concealment, blinding, attrition, selective reporting) were not available. Open-label design is near-universal in rituximab-versus-oral-agent trials, introducing a real possibility of performance and detection bias in a partly subjective outcome.
8. **Heterogeneous and unverified outcome operationalization.** "Relapse per ISKDC/KDIGO definitions" conceals variation in dipstick thresholds, consecutive-day requirements, and monitoring frequency, all of which affect ascertainment.
9. **Short time horizon.** A 12-month endpoint cannot capture post-withdrawal rebound — a central clinical concern for both agents, and the point at which they may most plausibly diverge.
10. **No prospective protocol registration**, and no formal GRADE certainty-of-evidence assessment. Informally, the certainty in the pooled estimate would be rated **very low**, downgraded for imprecision, inconsistency, and risk of bias.
11. **Per-study estimates and pooled estimate on different scales.** Per-study values are presented on the standardized display scale while the pooled summary is a native RR; readers should not attempt arithmetic reconciliation between them.

---

## 13. Conclusion

In children with steroid-sensitive nephrotic syndrome, including steroid-dependent and frequently relapsing forms, this meta-analysis of three randomized trials (n = 194) found a pooled Risk Ratio for relapse within approximately 12 months of **0.531 (95% CI 0.231 to 1.221; p = 0.136)** for rituximab versus tacrolimus, computed on the native risk-ratio scale with native pooling confirmed. The result **favours neither arm**: the confidence interval includes the null and the comparison does not reach statistical significance.

**Rituximab was not shown to reduce the risk of relapse by 12 months relative to tacrolimus.** Equally, equivalence was not demonstrated — the interval remains compatible with both substantial benefit and modest harm. Substantial unexplained heterogeneity (I² = 62.4%, τ² = 0.333), directional conflict in which the largest trial points away from the summary estimate, and a high risk-of-bias rating with discordant funnel diagnostics (Egger's p = 0.0002 alongside trim-and-fill k₀ = 0) together mean that this pooled estimate should be regarded as hypothesis-describing rather than practice-determining. Certainty in the evidence is very low.

Clinical choice between rituximab and tacrolimus in this population should continue to rest on individualized consideration of harms, monitoring burden, adherence, prior therapy and family preference. Resolution of the comparative-efficacy question requires adequately powered head-to-head randomized trials with harmonized relapse definitions, longer post-withdrawal follow-up, and ideally individual-participant-data synthesis.

---

## 14. Figures

| Figure | Path |
|---|---|
| Forest plot (per-study estimates and random-effects summary) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect by study size; descriptive only) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary (Q, I², τ²) | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 15. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Kidney Disease: Improving Global Outcomes (KDIGO) Glomerular Diseases Work Group. KDIGO 2021 Clinical Practice Guideline for the Management of Glomerular Diseases. *Kidney Int*. 2021;100(4S):S1–S276.
4. International Study of Kidney Disease in Children. The primary nephrotic syndrome in children: identification of patients with minimal change nephrotic syndrome from initial response to prednisone. *J Pediatr*. 1981;98(4):561–564.
5. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Control Clin Trials*. 1986;7(3):177–188.
6. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
7. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
8. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
9. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
10. Stanley TD, Doucouliagos H. Meta-regression approximations to reduce publication selection bias. *Res Synth Methods*. 2014;5(1):60–78.
11. Peters JL, Sutton AJ, Jones DR, Abrams KR, Rushton L. Contour-enhanced meta-analysis funnel plots help distinguish publication bias from other causes of asymmetry. *J Clin Epidemiol*. 2008;61(10):991–996.
12. IntHout J, Ioannidis JPA, Borm GF. The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method. *BMC Med Res Methodol*. 2014;14:25.
13. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336(7650):924–926.
14. Larkins NG, Liu ID, Willis NS, Craig JC, Hodson EM. Non-corticosteroid immunosuppressive medications for steroid-sensitive nephrotic syndrome in children. *Cochrane Database Syst Rev*. 2020;4:CD002290.
15. Iijima K, Sako M, Nozu K, et al. Rituximab for childhood-onset, complicated, frequently relapsing nephrotic syndrome or steroid-dependent nephrotic syndrome: a multicentre, double-blind, randomised, placebo-controlled trial. *Lancet*. 2014;384(9950):1273–1281.
16. Ravani P, Rossi R, Bonanni A, et al. Rituximab in children with steroid-dependent nephrotic syndrome: a multicenter, open-label, noninferiority, randomized controlled trial. *J Am Soc Nephrol*. 2015;26(9):2259–2266.
17. Trautmann A, Boyer O, Hodson E, et al. IPNA clinical practice recommendations for the diagnosis and management of children with steroid-sensitive nephrotic syndrome. *Pediatr Nephrol*. 2023;38(3):877–919.

---

*Note: Study-level citations for the three included trials are represented by their pipeline identifiers (study_1_R1, study_2_R2, study_3_R3) as supplied in the analysis dataset; full bibliographic details were not available to this secondary analysis.*

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| relapse of nephrotic syndrome | 3 | Risk Ratio (RR) | Yes | 0.5315 [0.2313, 1.2209] |
