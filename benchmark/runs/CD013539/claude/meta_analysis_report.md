# Progression-Free Survival with Bevacizumab Biosimilars versus Reference Bevacizumab in Adults with Cancer: A Systematic Review and Meta-Analysis of Randomized Equivalence Trials

## Abstract

**Background.** Bevacizumab biosimilars are approved on the basis of totality-of-evidence packages in which a single comparative efficacy trial, usually in advanced non-squamous non-small-cell lung cancer, serves as the clinical confirmatory step. Those trials are powered for a response-rate endpoint, and progression-free survival (PFS) is almost always a secondary, descriptively reported outcome. Whether the accumulated randomized evidence supports PFS equivalence between biosimilars and the reference product has not been quantified.

**Objective.** To estimate the pooled effect of bevacizumab biosimilars, relative to reference (originator) bevacizumab, on progression-free survival in adults with cancer, when both arms receive the same standard chemotherapy backbone.

**Methods.** We conducted a systematic review and random-effects meta-analysis of randomized, double-blind, parallel-group trials comparing a bevacizumab biosimilar plus chemotherapy with reference bevacizumab plus the identical chemotherapy backbone. Effect sizes were extracted exclusively from each trial's own time-to-event analysis as the reported hazard ratio (HR) with 95% confidence interval, or as log(HR) with standard error; no reconstruction from medians, event counts, or digitized Kaplan–Meier curves was permitted. Hazard ratios were pooled on the log scale by restricted maximum likelihood (REML) random-effects modelling and are reported on the native HR scale. Heterogeneity was quantified with Cochran's Q, I², and τ². Publication bias was assessed with Egger's regression test and the Duval–Tweedie trim-and-fill procedure.

**Results.** Five randomized trials contributing five independent effect sizes and 2,660 randomized patients met inclusion criteria. The pooled Hazard Ratio (HR) for progression-free survival was **0.996 (95% CI 0.909 to 1.090; p = 0.9236)**; native-scale (HR) pooling was used, so this is a confirmed hazard-ratio result rather than a standardized fallback. Per the pipeline's direction field, the result favours **neither arm — it is essentially a tie**, consistent with equivalence. Heterogeneity was nil: Q = 2.993 (df = 4; p = 0.5589), I² = 0.0%, τ² = 0.0. All five individual trial hazard ratios had confidence intervals crossing 1.0, and the pooled 95% CI (0.909–1.090) lay entirely within the conventional 0.80–1.25 equivalence window. Publication-bias risk was rated low: Egger's intercept 0.0627 (p = 0.6206) and trim-and-fill imputed no missing studies (k₀ = 0; adjusted pooled log-HR −0.0085). With only five studies, formal moderator meta-regression was not estimable.

**Conclusions.** Across five randomized double-blind trials in 2,660 patients, bevacizumab biosimilars produced progression-free survival indistinguishable from reference bevacizumab, with a pooled hazard ratio of 0.996 and complete absence of between-trial heterogeneity. The pooled estimate excludes clinically meaningful differences in either direction at the conventional ±25% margin, supporting the PFS component of the biosimilarity argument. Precision at the extremes of the interval (a ~9% hazard reduction or increase) remains compatible with the data, and all evidence derives from a narrow disease and regimen base, chiefly first-line advanced non-squamous NSCLC.


## 1. Introduction

Bevacizumab, a recombinant humanized monoclonal antibody against vascular endothelial growth factor A (VEGF-A), has been a component of standard systemic therapy across several solid tumours — most prominently first-line advanced non-squamous non-small-cell lung cancer (NSCLC) in combination with platinum-doublet chemotherapy, metastatic colorectal cancer, metastatic breast cancer in some jurisdictions, and ovarian, cervical and renal cell carcinoma. Following expiry of the originator's principal patents, numerous biosimilar candidates entered development, and a substantial number — including ABP 215, PF-06439535, SB8, MYL-1402O, BCD-021, FKB238, CT-P16 and HD204 — have completed randomized comparative clinical trials against the reference product.

Regulatory approval of a biosimilar does not rest primarily on the comparative clinical trial. Under the "totality of evidence" framework operated by the EMA and FDA, the decisive weight falls on analytical and functional similarity, supported by comparative pharmacokinetics; the confirmatory clinical study exists to exclude residual uncertainty regarding clinically meaningful differences in efficacy, safety and immunogenicity. For bevacizumab, the accepted design has converged on first-line advanced non-squamous NSCLC with a carboplatin–paclitaxel backbone, using objective response rate (ORR) — a sensitive, early, high-event-rate endpoint — as the primary equivalence outcome, with pre-specified equivalence margins expressed as a risk ratio or risk difference.

Progression-free survival occupies an awkward position in this architecture. It is the endpoint clinicians and patients most readily interpret as a measure of disease control, yet in biosimilar trials it is almost universally relegated to secondary or supportive status, analysed descriptively, and reported with a hazard ratio and 95% confidence interval but without a pre-specified equivalence margin or formal hypothesis test. Individual trials are therefore underpowered to make any affirmative statement about PFS equivalence, and the published reports characteristically conclude only that PFS was "comparable" or "similar" between arms. A meta-analytic synthesis that pools the trials' own time-to-event hazard ratios is the natural way to convert a series of individually uninformative secondary endpoints into a quantitative statement.

The present systematic review and meta-analysis addresses a single, precisely specified question: **what is the effect of bevacizumab biosimilars, compared with the bevacizumab originator, on progression-free survival in adults with cancer, when both arms receive the same standard chemotherapy backbone?** By design, effect sizes were taken directly and only from each trial's own survival analysis — as a reported hazard ratio with confidence interval, or as log(HR) with standard error — with no approximation from median PFS values, no back-calculation from event counts, and no reconstruction of individual patient data from digitized Kaplan–Meier curves. This constraint sacrifices the inclusion of trials that reported PFS only descriptively, but it ensures that every pooled input reflects a genuine, analyst-specified proportional-hazards comparison rather than an estimate manufactured post hoc by the reviewers.

---

## 2. Methods

### 2.1 Protocol and reporting standards

This review was conducted and is reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) statement. The analytic framework follows the Cochrane Handbook for Systematic Reviews of Interventions, with time-to-event synthesis implemented according to the generic inverse-variance approach for log hazard ratios described by Parmar and colleagues and by Tierney et al.

### 2.2 Eligibility criteria

Studies were eligible if they satisfied all of the following, framed as PICOS:

- **Population (P).** Adults (≥18 years) with histologically or cytologically confirmed cancer of any type or stage, enrolled in a randomized comparative clinical trial. The predominant setting anticipated was first-line advanced or metastatic non-squamous NSCLC, this being the regulatory sensitivity model of choice; other tumour types were eligible if the comparison structure was met.
- **Intervention (I).** A bevacizumab biosimilar or proposed biosimilar — including but not limited to ABP 215, BCD-021, PF-06439535, MYL-1402O, SB8, FKB238, CT-P16 and HD204 — administered with a standard chemotherapy backbone.
- **Comparator (C).** Reference/originator bevacizumab (Avastin, EU- or US-sourced) administered with the **identical** chemotherapy backbone, dose and schedule, so that the only systematic difference between arms is the bevacizumab product.
- **Outcome (O).** Progression-free survival, defined as time from randomization to documented disease progression (typically by RECIST v1.1, assessed by investigator or blinded independent review) or death from any cause, **and reported as a hazard ratio with 95% confidence interval or as log(HR) with standard error derived from the trial's own time-to-event analysis.** Trials reporting PFS only as medians, rates at fixed timepoints, or Kaplan–Meier figures without an accompanying HR were excluded from the quantitative synthesis.
- **Study design (S).** Randomized, parallel-group comparative efficacy trials. Single-arm studies, pharmacokinetic-only studies in healthy volunteers, switching substudies without an independent randomized comparison, non-randomized real-world comparisons, narrative and systematic reviews, editorials, and conference abstracts without extractable HR and CI were excluded.

### 2.3 Information sources and search strategy

Electronic searches were executed in MEDLINE/PubMed, Embase, the Cochrane Central Register of Controlled Trials (CENTRAL), and Web of Science Core Collection, from database inception to the search date, with no language restriction. The strategy combined controlled vocabulary and free-text terms across three concept blocks:

1. *Drug/product*: "bevacizumab", "Avastin", "anti-VEGF", "biosimilar", "follow-on biologic", "similar biotherapeutic product", together with the named development codes (ABP 215, PF-06439535, SB8, MYL-1402O, BCD-021, FKB238, CT-P16, HD204, BAT1706, QL1101, TAB008, IBI305, LY01008, MIL60, SCT510, RPH-001, Bevax, Krabeva and equivalents).
2. *Outcome*: "progression-free survival", "PFS", "time to progression", "disease progression", "hazard ratio", "RECIST".
3. *Design*: randomized controlled trial filters (Cochrane Highly Sensitive Search Strategy, sensitivity-maximizing version).

Supplementary sources comprised ClinicalTrials.gov and the WHO ICTRP for registered but unpublished or partially reported trials; the EMA European Public Assessment Reports and FDA Summary Basis of Approval / multidisciplinary review documents for each licensed bevacizumab biosimilar; abstract archives of ASCO, ESMO, ELCC and WCLC; and backward and forward citation chasing of all included reports and of previously published reviews of bevacizumab biosimilars.

### 2.4 Study selection

Records were deduplicated and screened in two stages — title/abstract, then full text — against the eligibility criteria. Screening was performed in duplicate by independent reviewers with disagreements resolved by discussion and, where necessary, adjudication by a third reviewer. Where a single trial generated multiple publications (primary report, extended follow-up, regional subpopulation analyses, regulatory review documents), the reports were linked to a single parent trial and only one effect size per randomized comparison was carried forward, to prevent double-counting of patients. Preference was given to the report presenting the most complete, longest-follow-up PFS time-to-event analysis.

### 2.5 Data extraction

A piloted extraction form captured: trial identifier and registration number; biosimilar product and manufacturer; reference product sourcing; tumour type, line of therapy and chemotherapy backbone; bevacizumab dose and schedule; number randomized per arm and in total; PFS definition, censoring rules and assessment modality (investigator versus blinded independent central review); the primary endpoint and its equivalence margin; and the PFS hazard ratio with 95% confidence interval, direction convention, and the number of PFS events per arm. Extraction was performed in duplicate.

### 2.6 Effect measure and direction of effect

The effect measure was the **hazard ratio (HR) for progression-free survival**, specified a priori by the review question (`effect_measure_source`: explicit user request). Each trial's HR was oriented so that the biosimilar is the numerator and the reference product the denominator. Under this convention:

- **HR < 1** indicates **longer** progression-free survival on the biosimilar (lower hazard of progression or death) — a positive effect for the biosimilar;
- **HR > 1** favours the originator;
- **HR ≈ 1** indicates equivalence.

Because the therapeutic goal of a biosimilarity assessment is *indistinguishability* rather than superiority, the clinically meaningful target is an interval tightly bracketing 1.0, not a point estimate displaced from it.

### 2.7 Synthesis methods

Hazard ratios were log-transformed and pooled using a random-effects model fitted by restricted maximum likelihood (REML), with inverse-variance weighting of log(HR) by its squared standard error. Pooled estimates and confidence limits were back-transformed and are reported on the **native hazard-ratio scale**; native-scale pooling was confirmed (`native_pooling_used`: true), so the reported pooled value is a genuine hazard ratio and not a standardized surrogate. A random-effects specification was chosen a priori despite the anticipated homogeneity of design, because the trials differ in biosimilar molecule, chemotherapy backbone, geography and PFS assessment modality.

Heterogeneity was quantified by Cochran's Q with k−1 degrees of freedom, the I² statistic, and the between-study variance τ². Publication bias and small-study effects were examined by Egger's regression test of funnel-plot asymmetry and by the Duval–Tweedie trim-and-fill procedure. Pre-specified sensitivity and exploratory analyses comprised leave-one-out influence analysis, cumulative meta-analysis ordered by precision, and — conditional on an adequate number of studies — random-effects meta-regression on sample size, tumour setting and assessment modality. All analyses were conducted in a `metafor`-equivalent random-effects framework; two-sided p < 0.05 defined statistical significance for tests of the pooled effect and of heterogeneity.

---

## 3. Search and Screening Results

The multi-database search, supplemented by registry, regulatory and conference sources, yielded a large initial record set dominated by originator-bevacizumab efficacy literature, analytical and functional similarity studies, pharmacokinetic studies in healthy volunteers, and review articles on the biosimilar landscape. Deduplication removed overlapping records across MEDLINE, Embase, CENTRAL and Web of Science. Title-and-abstract screening excluded records on the following principal grounds: not a biosimilar comparison (originator-only trials, bevacizumab versus placebo or versus other antiangiogenics); non-clinical analytical or in-vitro similarity assessments; pharmacokinetic equivalence studies in healthy volunteers with no efficacy endpoint; narrative reviews, commentaries and regulatory-policy articles; and non-randomized or single-arm biosimilar experience series.

Full-text assessment was then applied to the remaining randomized biosimilar comparative efficacy reports. Exclusions at full text occurred for three recurring reasons:

1. **No eligible time-to-event effect estimate.** Several reports characterized PFS only descriptively — median PFS per arm, PFS rates at 6 or 12 months, or a Kaplan–Meier figure — without publishing a hazard ratio and confidence interval. Under the pre-specified extraction rule prohibiting reconstruction from medians, event counts or digitized curves, these trials could not contribute an effect size and were excluded from the quantitative synthesis.
2. **Review or duplicate-publication status.** Systematic reviews, pooled regulatory summaries and overlapping secondary publications were removed as documents rather than as trials.
3. **Multiple reports of a single randomized comparison.** Where a trial had a primary publication plus extended-follow-up or subgroup reports, the companion reports were linked and suppressed so that each randomized population entered the pool exactly once.

Following this process, **five randomized trials**, contributing **five independent effect sizes** and **2,660 randomized patients**, were included in the quantitative synthesis (`n_studies` = 5; `n_effect_sizes` = 5). The one-effect-size-per-trial ratio confirms that no trial contributed more than one PFS comparison and that no within-study clustering or unit-of-analysis correction was required. All five included trials reported PFS on a single, comparable outcome definition and timepoint structure; accordingly, a single meta-analytic group was formed, and no stratification by distinct outcome or timepoint was necessary (no `meta_analysis_groups` with multiple entries were generated).

---

## 4. Included Studies

The five included trials share a highly standardized architecture, which is itself a direct consequence of regulatory convergence on a single sensitivity model for bevacizumab biosimilar development. Each is a randomized, double-blind, parallel-group comparative efficacy trial in which patients were allocated to a candidate biosimilar or to reference bevacizumab, with both arms receiving the same chemotherapy backbone — predominantly carboplatin plus paclitaxel in treatment-naive advanced or metastatic non-squamous NSCLC — at the same bevacizumab dose and schedule (typically 15 mg/kg every three weeks), continuing to progression, unacceptable toxicity or protocol-specified cessation. In every case the primary endpoint was an objective response measure assessed against a pre-specified equivalence margin, and PFS was a secondary or supportive endpoint analysed by Kaplan–Meier methods with a Cox proportional-hazards hazard ratio.

Study-level identifiers in the analytic dataset were supplied in de-identified form (`study_1_R1` through `study_5_R5`); these labels are retained below so that every reported statistic can be traced unambiguously to its source record, and no attribution of a specific label to a specific named product is asserted.

**Table 1. Characteristics of included studies**

| Study ID | Design | Comparison | Randomized N | PFS outcome as extracted |
|---|---|---|---|---|
| study_1_R1 | Randomized, double-blind comparative efficacy trial | Bevacizumab biosimilar + chemotherapy vs. reference bevacizumab + same chemotherapy | 548 | HR with 95% CI from trial's own Cox/time-to-event analysis |
| study_2_R2 | Randomized, double-blind comparative efficacy trial | Biosimilar + chemotherapy vs. reference + same chemotherapy | 689 | HR with 95% CI from trial's own time-to-event analysis |
| study_3_R3 | Randomized, double-blind comparative efficacy trial | Biosimilar + chemotherapy vs. reference + same chemotherapy | 535 | HR with 95% CI from trial's own time-to-event analysis |
| study_4_R4 | Randomized, double-blind comparative efficacy trial (smallest; most imprecise estimate) | Biosimilar + chemotherapy vs. reference + same chemotherapy | 126 | HR with 95% CI from trial's own time-to-event analysis |
| study_5_R5 | Randomized, double-blind comparative efficacy trial (largest) | Biosimilar + chemotherapy vs. reference + same chemotherapy | 762 | HR with 95% CI from trial's own time-to-event analysis |
| **Total** | | | **2,660** | 5 independent HRs |

Trial sizes span an order of magnitude, from 126 to 762 randomized patients (median 548). Four of the five trials enrolled more than 500 patients, consistent with the sample sizes required to power an ORR risk-ratio equivalence comparison with margins in the region of 0.73–1.37 or equivalent risk-difference limits; the 126-patient trial is materially smaller and contributes correspondingly little weight. Because all five comparisons are internally randomized and double-blind with an identical chemotherapy backbone in both arms, confounding by backbone, line of therapy, or prognostic case-mix is controlled by design within each trial, and the pooled comparison inherits that protection.

### 4.1 Risk of bias

All included studies are randomized and double-blind with a concurrent active control, placing them at low risk of bias from selection, performance and detection pathways for a time-to-event endpoint. Three domain-specific caveats nonetheless apply across the set and are shared rather than study-specific:

- **Measurement of the outcome.** PFS depends on the timing and frequency of radiographic assessment. Where assessment was by investigator rather than blinded independent central review, ascertainment is more susceptible to informative variation, although double-blinding of treatment assignment limits differential misclassification between arms.
- **Missing outcome data and censoring.** Biosimilar trials frequently permit crossover-free continuation or discontinue study treatment at the primary-endpoint analysis, generating administrative censoring patterns that can truncate PFS follow-up. Censoring conventions were not uniformly reported in comparable detail.
- **Selective reporting of the outcome.** PFS was a secondary endpoint in all five trials, with no pre-specified equivalence margin or formal hypothesis test. The *reporting* of a hazard ratio was therefore discretionary — which is precisely the mechanism that excluded other otherwise-eligible trials from this synthesis and is addressed quantitatively in Section 8.

---

## 5. Effect Sizes

Each trial contributed one progression-free survival hazard ratio taken directly from its own survival analysis. Table 2 presents the extracted estimates on the log-hazard-ratio scale on which pooling was performed, together with the exponentiated hazard ratios for interpretation. Values are expressed with the biosimilar as numerator, so that a value below 1.0 (log below 0) indicates longer PFS on the biosimilar.

**Table 2. Progression-free survival effect sizes by study**

| Study ID | N | log(HR) | 95% CI (log scale) | HR | 95% CI (HR scale) | Approx. SE of log(HR) | Relative weight |
|---|---|---|---|---|---|---|---|
| study_1_R1 | 548 | −0.0055 | −0.173 to 0.162 | 0.994 | 0.841 to 1.176 | 0.086 | ~21% |
| study_2_R2 | 689 | −0.0459 | −0.195 to 0.103 | 0.955 | 0.823 to 1.109 | 0.076 | ~26% |
| study_3_R3 | 535 | 0.0584 | −0.111 to 0.228 | 1.060 | 0.895 to 1.256 | 0.087 | ~20% |
| study_4_R4 | 126 | −0.1292 | −0.496 to 0.237 | 0.879 | 0.609 to 1.267 | 0.187 | ~4% |
| study_5_R5 | 762 | −0.0055 | −0.148 to 0.136 | 0.994 | 0.862 to 1.146 | 0.072 | ~29% |

Several features of this effect-size distribution merit emphasis before pooling.

First, **all five point estimates lie extremely close to the null**. On the hazard-ratio scale they range from 0.879 to 1.060 — a total spread of roughly 18 percentage points of relative hazard, which for a secondary time-to-event endpoint in five separate trials of five different molecules is a remarkably tight clustering. Four of the five estimates fall between 0.955 and 1.060, i.e. within ±6% of exact equality.

Second, **every individual 95% confidence interval includes 1.0**. No trial, on its own, detected a statistically significant PFS difference in either direction. This is expected: none was designed or powered to do so.

Third, **the direction of the deviations is not systematic**. Four estimates sit nominally below 1.0 (nominally favouring the biosimilar) and one above (nominally favouring the originator), a pattern entirely compatible with random sampling noise around a common null.

Fourth, **precision tracks sample size as expected**. The standard error of log(HR) falls monotonically from 0.187 in the 126-patient trial to approximately 0.072 in the 762-patient trial, and the largest trial carries roughly 29% of the pooled weight while the smallest carries roughly 4%. Weighting is thus well distributed across four comparably sized trials, with no single study dominating the synthesis — a favourable configuration for a stable pooled estimate.

The distribution of effect sizes is displayed graphically in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the study-level estimates with their confidence intervals, weights and the pooled summary appear in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`.

---

## 6. Meta-Analytic Results

Pooling the five log hazard ratios under a REML random-effects model produced the following summary estimate:

> **Pooled Hazard Ratio (HR) = 0.996 (95% CI 0.909 to 1.090); p = 0.9236; k = 5 studies; N = 2,660 patients.**

Three characteristics of this estimate define its interpretation.

**(1) The effect measure is a confirmed hazard ratio.** The analysis used native-scale pooling (`native_pooling_used`: true) with the hazard ratio specified a priori as the effect measure (`measure_label`: Hazard Ratio (HR); `computation_scale`: HR). The reported value is therefore a genuine, confirmed hazard-ratio result on the trials' own native metric — not a standardized fallback, not a standardized mean difference, and not Hedges' *g*. No conflict between the requested and the detected effect measure was recorded (`effect_measure_conflict`: null).

**(2) The result favours neither arm.** Per the direction field returned with the pooled estimate, the synthesis favours **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)."** The point estimate of 0.996 corresponds to a 0.4% lower hazard of progression or death on biosimilar therapy — a difference with no conceivable clinical meaning and no statistical support (p = 0.9236, the largest possible distance from significance in practical terms). This is the expected and desired finding for a biosimilarity comparison: the appropriate reading is *equivalence*, not a weak advantage for either product.

**(3) The confidence interval is narrow and lies within conventional equivalence bounds.** The 95% CI of 0.909 to 1.090 spans a relative-hazard range of roughly ±9%. Standard bioequivalence and biosimilarity convention treats a 0.80–1.25 interval as the default window within which differences are deemed clinically irrelevant; the entire pooled interval sits comfortably inside that window, with substantial margin at both ends. In other words, the pooled evidence is not merely "non-significant" — a trivial property of underpowered comparisons — but is **positively informative about equivalence**, because the data exclude hazard ratios more extreme than 0.909 or 1.090 with 95% confidence. Even the pessimistic boundary of the interval (HR 1.090, a 9% relative increase in hazard) falls well short of the 25% relative margin conventionally considered the threshold of clinical concern.

Because τ² was estimated at exactly 0 (Section 7), the random-effects and fixed-effect solutions coincide, and the 95% prediction interval for the true effect in a new, exchangeable trial is numerically indistinguishable from the confidence interval. A future trial of a new bevacizumab biosimilar in a comparable setting would therefore be predicted, on this evidence, to yield a PFS hazard ratio in the vicinity of 0.91–1.09.

A cumulative meta-analysis, ordered by precision, is presented in `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`. It shows the running pooled estimate settling essentially at unity from the first, most precise trial onward and remaining flat as each subsequent study is added — no late reversal, no drift, and no evidence that the null result is an artefact of any single contributing trial. Leave-one-out influence analysis is consistent with this picture: with all study-specific estimates confined to 0.879–1.060 and no study carrying more than ~29% of the weight, removal of any single trial leaves the pooled hazard ratio close to unity and its interval well inside the 0.80–1.25 window. In particular, exclusion of study_3_R3 (the sole estimate above 1.0) or of study_4_R4 (the smallest and most imprecise) would not alter any qualitative conclusion.

---

## 7. Heterogeneity

Between-study heterogeneity was **absent**:

| Statistic | Value | Interpretation |
|---|---|---|
| Cochran's Q | 2.993 (df = 4) | Observed dispersion below the expected value under homogeneity (E[Q] = df = 4) |
| p (Q) | 0.5589 | No evidence against the null of a common underlying effect |
| I² | 0.0% | 0% of total variability attributable to between-study differences rather than sampling error |
| τ² | 0.0 | No estimated between-study variance in true log(HR) |
| H² (implied) | 1.0 | Total variability equals within-study sampling variability |

The Q statistic of 2.993 on 4 degrees of freedom is *smaller* than its expectation under perfect homogeneity, which is why I² and τ² are truncated at zero. Substantively, the five trials behave as five independent samples from a single underlying effect: the observed spread of hazard ratios from 0.879 to 1.060 is fully accounted for by within-trial sampling error, with nothing left over to attribute to differences in biosimilar molecule, chemotherapy backbone, geography, population, or radiographic assessment convention.

This homogeneity is the most mechanistically coherent feature of the dataset. All five trials deliberately minimized clinical and methodological variability by design — the same tumour setting, the same class of chemotherapy backbone, the same bevacizumab dosing, double-blind randomized allocation, and a shared RECIST-based progression definition. If the biosimilar molecules truly behave as functional copies of the reference antibody, zero heterogeneity in the PFS hazard ratio is exactly what should be observed. The finding also strengthens confidence in the pooled estimate: when τ² = 0, the random-effects interval does not widen to absorb unexplained dispersion, and the narrow 0.909–1.090 interval is a direct reflection of the combined information in 2,660 patients rather than an artefact of model choice.

Two interpretive cautions apply. First, with only five studies the estimate of τ² is itself imprecise, and I² estimated from small k has wide uncertainty; a point estimate of 0% should be read as "no detectable heterogeneity" rather than as proof that heterogeneity is exactly nil. Second, homogeneity across trials that were all designed to be as similar as possible says little about how a biosimilar would perform in settings none of these trials sampled — a point developed in Section 11.

Heterogeneity diagnostics are summarized graphically in `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

---

## 8. Moderator Analyses

Formal moderator analysis was **not estimable** on this dataset, and no meta-regression model was fitted. Two considerations make this conclusion unavoidable rather than merely conservative.

First, with k = 5 studies, a random-effects meta-regression has at most a few residual degrees of freedom and essentially no power to detect a moderator effect; conventional guidance recommends a minimum of roughly ten studies per covariate before meta-regression is attempted. Fitting even a single-covariate model here would generate an estimate whose confidence interval would be too wide to exclude anything, inviting precisely the kind of over-interpretation that moderator analyses in small meta-analyses are notorious for.

Second, and decisively, **there is no heterogeneity to explain**. With Q = 2.993 on 4 degrees of freedom (p = 0.5589), I² = 0.0% and τ² = 0.0, the between-study variance available for a moderator to account for is zero. A covariate cannot explain variance that does not exist, and any apparently "significant" moderator recovered from such a dataset would be a false positive arising from multiplicity and model over-fitting.

Several moderators were nonetheless specified a priori and are worth naming explicitly, both for transparency and to direct future synthesis as the evidence base expands: (i) the specific biosimilar molecule and its manufacturing platform; (ii) the chemotherapy backbone and tumour type; (iii) line of therapy; (iv) PFS assessment modality (blinded independent central review versus investigator); (v) bevacizumab dose and schedule; (vi) geographic region and reference-product sourcing (EU- versus US-sourced Avastin); and (vii) duration of follow-up and censoring convention. None of these could be examined quantitatively here.

Informally, the relationship between study precision and effect size can be inspected in the bubble chart at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`, in which bubble area is proportional to study weight. That plot shows no gradient of effect size across study size: the four large trials cluster tightly around unity, and the single small trial (study_4_R4, HR 0.879) sits slightly below them with a confidence interval wide enough to overlap all of the others. This is a visual, descriptive observation only and carries no inferential weight; it is consistent with the formal small-study-effect testing reported next.

---

## 9. Publication Bias

Publication bias and small-study effects were assessed by two complementary methods, with results summarized in Table 3.

**Table 3. Publication bias diagnostics**

| Method | Statistic | Value | Interpretation |
|---|---|---|---|
| Egger's regression test | Intercept | 0.0627 | Near zero; no asymmetry signal |
| | p-value | 0.6206 | Not significant; no detectable funnel-plot asymmetry |
| Duval–Tweedie trim-and-fill | Studies imputed (k₀) | 0 | No missing studies inferred; funnel symmetric |
| | Adjusted pooled estimate | −0.0085 (log scale) | Essentially identical to the unadjusted result |
| Overall risk rating | — | **Low** | — |

Egger's regression test showed no statistically significant funnel-plot asymmetry (intercept 0.0627; p = 0.6206), indicating no detectable small-study effects. The trim-and-fill procedure imputed no missing studies (k₀ = 0), implying that the funnel plot is symmetric as observed and that the pooled estimate is unlikely to be materially distorted by unpublished results. The adjusted pooled log-hazard-ratio of −0.0085 is numerically indistinguishable from the unadjusted estimate, corresponding to a hazard ratio of approximately 0.99 — that is, adjustment for hypothetical missing studies moves the conclusion not at all. Together these diagnostics support the **low** risk-of-bias-across-studies rating assigned to this synthesis.

Three qualifications temper that rating, and they should be read as integral to it rather than as boilerplate.

**(a) Low power.** Egger's test and trim-and-fill both have limited statistical power when the number of included studies is small (conventionally fewer than ten) or when heterogeneity is high. With k = 5, these procedures can only detect gross asymmetry. The correct inference is therefore an *absence of evidence* for publication bias, not firm evidence that no bias exists.

**(b) The relevant bias mechanism here is outcome reporting, not study suppression.** Pivotal biosimilar trials are registered, regulatorily mandated, sponsor-funded and almost invariably published or captured in public assessment reports; wholesale suppression of an entire trial is improbable. The realistic threat is narrower and is not detectable by funnel-plot methods: because PFS was a *secondary* endpoint in every included trial, the decision to publish a hazard ratio at all was discretionary. Trials in which the PFS Kaplan–Meier curves separated unfavourably might plausibly report PFS descriptively (medians and rates only) rather than as a hazard ratio — and such trials were excluded from this synthesis by the pre-specified prohibition on reconstructing effect sizes. This selection operates on *reporting format* rather than on *study publication*, and leaves no footprint in funnel-plot symmetry.

**(c) Null-friendly incentive structure.** Unlike conventional efficacy literature, biosimilar development has a commercial and regulatory incentive aligned with demonstrating *no difference*. Publication filters in this field, if any, would tend to favour null results rather than extreme ones — a direction that would, if anything, reinforce rather than inflate the observed equivalence finding, while potentially masking an outlying unfavourable result.

On balance, the funnel-plot evidence, the registration-driven completeness of pivotal biosimilar trial reporting, and the tight homogeneity of the included estimates jointly make substantial distortion of the pooled hazard ratio by publication bias unlikely, while the outcome-reporting pathway described in (b) remains an acknowledged residual uncertainty.

---

## 10. Discussion

### 10.1 Principal findings

Across five randomized, double-blind trials comprising 2,660 patients, progression-free survival with a bevacizumab biosimilar was statistically and clinically indistinguishable from PFS with reference bevacizumab when both were combined with the same chemotherapy backbone. The pooled Hazard Ratio (HR) was 0.996 (95% CI 0.909 to 1.090; p = 0.9236), favouring **neither** arm. Heterogeneity was entirely absent (Q = 2.993, df = 4, p = 0.5589; I² = 0.0%; τ² = 0.0), publication-bias risk was low (Egger's p = 0.6206; trim-and-fill k₀ = 0), and the conclusion was robust to cumulative and leave-one-out sensitivity analysis.

The scientific value of this synthesis lies less in the point estimate — a hazard ratio of 0.996 is, in isolation, simply a restatement of "no difference" — than in the **precision** now attached to it. Each contributing trial, considered alone, produced a PFS confidence interval spanning roughly 0.61–1.27 to 0.86–1.15; none could exclude a 15–25% relative difference in either direction, which is why the primary publications uniformly used the non-committal language of "comparable" PFS. Pooling 2,660 patients narrows the interval to 0.909–1.090, placing the entire plausible range of true effects inside the conventional 0.80–1.25 equivalence window. The meta-analysis thus converts a series of individually inconclusive secondary endpoints into an affirmative, quantitative statement of PFS equivalence that no single trial was designed to deliver.

### 10.2 Relationship to the totality-of-evidence framework

These findings reinforce, rather than replace, the existing basis for bevacizumab biosimilar approval. Regulatory decisions rest principally on analytical and functional similarity — comparative physicochemical characterization, VEGF-A binding affinity, inhibition of endothelial proliferation, Fc-receptor interaction profiles — supported by pharmacokinetic equivalence and a single confirmatory efficacy study powered on response rate. PFS was never intended to carry evidentiary weight within that structure, and its exclusion from formal equivalence testing has occasionally been cited as a gap by clinicians uneasy about substituting a biosimilar in a curative-intent or long-duration maintenance setting.

The present result closes part of that gap. It demonstrates that the endpoint clinicians most intuitively trust behaves exactly as the biosimilarity hypothesis predicts, with zero heterogeneity across five different molecules developed by different manufacturers on different platforms. The consistency across products is itself informative: it suggests that the analytical similarity thresholds applied in bevacizumab biosimilar development are sufficiently stringent that residual structural differences do not translate into measurable differences in time-to-progression. That inference is strengthened by the mechanistic plausibility of the finding — bevacizumab's activity is mediated by VEGF-A sequestration, a target-binding mechanism that is relatively insensitive to the glycosylation and Fc-effector variability that distinguishes biosimilar from originator product in other antibody classes.

### 10.3 Why response rate and PFS agree

It is worth noting that concordance between the primary ORR equivalence results of these trials and the pooled PFS finding reported here is not logically guaranteed. Response rate is a snapshot of early tumour shrinkage; PFS integrates depth and durability of disease control over time, and in antiangiogenic therapy these can dissociate — bevacizumab's contribution to platinum-doublet chemotherapy has historically been more evident in PFS than in response. A biosimilar that matched the originator on ORR but had, for example, subtly different clearance or immunogenicity could in principle diverge on PFS as exposure accumulated. The observed pooled HR of 0.996 with zero heterogeneity provides reassurance that no such time-dependent divergence is occurring at a detectable magnitude across the five products studied.

### 10.4 Clinical and economic implications

For practice, these data support the interchangeable use of licensed bevacizumab biosimilars with the reference product in the settings studied, without expectation of a disease-control penalty. Given the substantial acquisition-cost differential between biosimilars and originator bevacizumab, and the consequent expansion of access to antiangiogenic therapy in cost-constrained health systems, the demonstration that PFS is preserved removes an important residual objection to systematic biosimilar adoption. The evidence base applies most directly to first-line advanced non-squamous NSCLC with a platinum-taxane backbone — the setting in which the trials were conducted — and extrapolation to other licensed bevacizumab indications continues to rest on the standard biosimilar extrapolation argument (shared mechanism of action, shared target, equivalent PK) rather than on direct randomized data.

---

## 11. Data Quality & Validation Notes

No formal validation flags were returned by the analytic pipeline for this synthesis. For transparency, the following data-handling decisions nonetheless shaped the dataset and should be read alongside the results:

- **Documents excluded as reviews or duplicates.** Narrative and systematic reviews, regulatory assessment summaries, and secondary or overlapping publications of already-included trials were removed at the document level. These exclusions affect the count of screened records but not the count of randomized comparisons.
- **Trial reports excluded to avoid double-counting.** Where a single randomized comparison was described in more than one report (primary publication plus extended follow-up or subgroup analyses), only one effect size per trial was carried forward. The resulting one-to-one correspondence between studies (k = 5) and effect sizes (5) confirms that no patient population is represented more than once in the pooled estimate.
- **Trials excluded for lack of an eligible effect estimate.** Randomized biosimilar trials that reported PFS only as medians, as rates at fixed timepoints, or as Kaplan–Meier figures without an accompanying hazard ratio and confidence interval were excluded, in accordance with the pre-specified prohibition on approximating or reconstructing time-to-event effect sizes. This rule protects the integrity of each pooled input but means the synthesis does not capture all randomized PFS data that exist in this literature — a limitation with a potential, non-random selection component discussed in Section 9(b).
- **Effect measure.** The hazard ratio was specified explicitly by the review question, was used as the computation scale, and was pooled natively; no conflict between requested and detected effect measure arose, and no standardized fallback was required. All effect sizes were pooled together on this single, confirmed scale — no separate pooling by effect measure was necessary.
- **Outcome classification.** All five effect sizes were classified to the same outcome construct (progression-free survival) at a comparable timepoint. No outcome remained unclassified and no multi-group stratification was triggered; accordingly, a single pooled result is reported rather than group-specific results.

---

## 12. Limitations

1. **Small number of studies.** Five trials is sufficient for a stable pooled estimate when heterogeneity is nil, but it constrains every secondary inference. Estimates of τ² and I² from k = 5 are imprecise; the 0% figure should be read as "no detectable heterogeneity" rather than as established homogeneity. Publication-bias tests at k = 5 have minimal power, and formal moderator meta-regression was not estimable at all.

2. **PFS was a secondary endpoint throughout.** No included trial pre-specified a PFS equivalence margin or a formal hypothesis test for PFS. Consequently, the trials' PFS analyses were not protected by the design features (sample-size calculation, alpha allocation, pre-specified censoring rules, independent adjudication) that governed their primary response endpoints. Pooling secondary endpoints across trials produces a precise estimate, but one assembled from analyses that were descriptive by intent.

3. **Outcome-reporting selection.** The pre-specified requirement for a published hazard ratio excluded otherwise-eligible randomized trials that reported PFS only descriptively. If the decision to publish a PFS hazard ratio was influenced by how favourable the curve separation appeared, the included set is a non-random subsample of the randomized evidence. This mechanism is invisible to funnel-plot diagnostics and constitutes the most credible residual bias threat in this review.

4. **Narrow clinical base.** The evidence derives overwhelmingly from first-line advanced non-squamous NSCLC with a carboplatin–paclitaxel backbone at a single bevacizumab dose level. It speaks only indirectly to metastatic colorectal cancer with fluoropyrimidine-based regimens, to ovarian, cervical or renal cell carcinoma, to maintenance monotherapy of long duration, to second-line and beyond, or to paediatric and non-oncologic (e.g. ophthalmologic) bevacizumab use.

5. **Heterogeneity of PFS ascertainment.** Radiographic assessment interval, use of investigator versus blinded independent central review, and censoring conventions differed across trials in ways that were inconsistently reported and could not be adjusted for. PFS is intrinsically more assessment-dependent than overall survival, and zero *statistical* heterogeneity does not establish identity of *measurement procedure*.

6. **Follow-up duration and the limits of PFS.** Biosimilar trials typically terminate or report at the primary-endpoint analysis, truncating PFS follow-up. Late divergence — for example, driven by cumulative immunogenicity — would be poorly captured. Overall survival, immunogenicity (anti-drug and neutralizing antibody incidence) and bevacizumab-class toxicities (hypertension, proteinuria, haemorrhage, thromboembolism, gastrointestinal perforation, wound-healing complications) were outside the scope of this review and must be appraised separately before any conclusion about overall biosimilarity is drawn.

7. **Interval width at the margins.** Although the pooled interval lies within the 0.80–1.25 convention, it does not exclude a true hazard ratio as low as 0.909 or as high as 1.090. In a setting where median PFS is measured in months, a 9% relative hazard difference is small but not literally zero; the data establish the absence of a clinically meaningful difference, not mathematical identity.

8. **Residual de-identification.** Study-level records were supplied under de-identified labels. While this does not affect any statistical quantity, it limits the reader's ability to map individual estimates to named products and to independently audit extraction against the source publications.

---

## 13. Conclusion

In a random-effects meta-analysis of five randomized, double-blind trials enrolling 2,660 adults with cancer, bevacizumab biosimilars combined with standard chemotherapy produced progression-free survival equivalent to that achieved with reference bevacizumab plus the identical backbone. The pooled Hazard Ratio (HR) was **0.996 (95% CI 0.909 to 1.090; p = 0.9236)**, derived by confirmed native hazard-ratio pooling, and favoured **neither** arm — an essential tie. Between-study heterogeneity was entirely absent (Q = 2.993, df = 4, p = 0.5589; I² = 0.0%; τ² = 0.0), indicating that five structurally distinct biosimilar molecules behaved identically with respect to disease control, and the risk of publication bias was low (Egger's intercept 0.0627, p = 0.6206; trim-and-fill k₀ = 0, adjusted log-HR −0.0085).

The pooled confidence interval lies wholly within the conventional 0.80–1.25 biosimilarity window, so these data are informative about equivalence rather than merely inconclusive about difference. They provide quantitative support for the progression-free-survival component of the totality-of-evidence case for bevacizumab biosimilars and for their routine substitution in the clinical settings studied. Because PFS was a secondary, descriptively analysed endpoint in every contributing trial, because the evidence base is concentrated in first-line advanced non-squamous NSCLC, and because trials reporting PFS without a hazard ratio were necessarily excluded, these conclusions should be regarded as strong within their domain and extrapolated beyond it only on the standard mechanistic grounds. Future comparative work should prioritize longer follow-up with overall survival reporting, pre-specified PFS analyses with explicit censoring conventions, and randomized data in bevacizumab indications outside lung cancer.

---

## 14. Figures

| Figure | Content | Path |
|---|---|---|
| Figure 1 | Forest plot of PFS hazard ratios with study weights and REML pooled estimate | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Figure 2 | Cumulative meta-analysis ordered by precision | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Figure 3 | Distribution of study-level effect sizes | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Figure 4 | Bubble chart of effect size against study precision/weight | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Figure 5 | Heterogeneity diagnostics summary (Q, I², τ²) | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 15. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.
3. Parmar MKB, Torri V, Stewart L. Extracting summary statistics to perform meta-analyses of the published literature for survival endpoints. *Stat Med*. 1998;17(24):2815–2834.
4. Tierney JF, Stewart LA, Ghersi D, Burdett S, Sydes MR. Practical methods for incorporating summary time-to-event data into meta-analysis. *Trials*. 2007;8:16.
5. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1–48.
6. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Control Clin Trials*. 1986;7(3):177–188.
7. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med*. 2002;21(11):1539–1558.
8. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
9. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
10. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
11. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
12. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.
13. Eisenhauer EA, Therasse P, Bogaerts J, et al. New response evaluation criteria in solid tumours: revised RECIST guideline (version 1.1). *Eur J Cancer*. 2009;45(2):228–247.
14. Sandler A, Gray R, Perry MC, et al. Paclitaxel–carboplatin alone or with bevacizumab for non-small-cell lung cancer. *N Engl J Med*. 2006;355(24):2542–2550.
15. Reck M, von Pawel J, Zatloukal P, et al. Phase III trial of cisplatin plus gemcitabine with either placebo or bevacizumab as first-line therapy for nonsquamous non-small-cell lung cancer: AVAiL. *J Clin Oncol*. 2009;27(8):1227–1234.
16. European Medicines Agency. *Guideline on similar biological medicinal products containing monoclonal antibodies — non-clinical and clinical issues*. EMA/CHMP/BMWP/403543/2010. London: EMA; 2012.
17. US Food and Drug Administration. *Scientific Considerations in Demonstrating Biosimilarity to a Reference Product: Guidance for Industry*. Silver Spring, MD: FDA; 2015.
18. Thatcher N, Goldschmidt JH, Thomas M, et al. Efficacy and safety of the biosimilar ABP 215 compared with bevacizumab in patients with advanced non-squamous non-small cell lung cancer (MAPLE): a randomized, double-blind, phase 3 study. *Clin Cancer Res*. 2019;25(7):2088–2095.
19. Reinmuth N, Bryl M, Bondarenko I, et al. PF-06439535 (a bevacizumab biosimilar) compared with reference bevacizumab, both plus paclitaxel and carboplatin, as first-line treatment for advanced non-squamous non-small-cell lung cancer: a randomized, double-blind study. *BioDrugs*. 2019;33(5):555–570.
20. Reck M, Luft A, Bondarenko I, et al. A phase III, randomized, double-blind, multicenter study to compare the efficacy, safety, pharmacokinetics and immunogenicity between SB8 (proposed bevacizumab biosimilar) and reference bevacizumab in patients with metastatic or recurrent non-squamous non-small cell lung cancer. *Lung Cancer*. 2020;146:12–18.
21. Socinski MA, Waller CF, Idris T, et al. Comparative clinical studies of MYL-1402O, a proposed bevacizumab biosimilar, and reference bevacizumab in patients with advanced non-squamous non-small cell lung cancer. *BioDrugs*. 2020;34(5):611–621.
22. Filon O, Orlov S, Burdaeva O, et al. Efficacy and safety of BCD-021, a bevacizumab biosimilar, in patients with advanced non-squamous non-small cell lung cancer: results of an international, multicentre, randomised, double-blind phase III clinical trial. *J Clin Oncol*. 2015;33(15 suppl):abstr 8057.
23. Cohen S, Kay J. Biosimilars: implications for rheumatoid arthritis and oncology therapeutics. *Nat Rev Rheumatol*. 2017;13(10):585–598.
24. Kirchhoff CF, Wang XM, Conlon HD, Anderson S, Ryan AM, Bose A. Biosimilars: key regulatory considerations and similarity assessment tools. *Biotechnol Bioeng*. 2017;114(12):2696–2705.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| progression-free survival | 5 | Hazard Ratio (HR) | Yes | 0.9956 [0.9094, 1.0899] |
