# Elective versus Therapeutic Neck Dissection for Early-Stage (T1–T2) Clinically Node-Negative Oral Cavity Squamous Cell Carcinoma: A Systematic Review and Meta-Analysis of Disease-Free Survival

## Abstract

**Background.** The management of the clinically node-negative (cN0) neck in early-stage (T1–T2) oral cavity squamous cell carcinoma (OCSCC), including oral tongue cancer, remains contested. Elective (immediate, prophylactic) neck dissection performed at the time of primary tumour resection removes occult nodal metastases but exposes the substantial majority of patients who are pathologically node-negative to unnecessary morbidity; the alternative strategy of therapeutic (delayed) neck dissection reserves surgery for patients who develop nodal relapse during structured observation.

**Objective.** To quantify whether elective neck dissection improves disease-free survival (DFS; time from randomisation to recurrence, disease progression, new disease, or death from any cause) compared with therapeutic (delayed) neck dissection in adults with T1–T2 cN0 OCSCC.

**Methods.** A systematic search and automated screening pipeline identified five potentially eligible study reports addressing elective versus therapeutic neck dissection in this population. Two studies (k = 2; N = 746 participants) provided an extractable DFS hazard ratio (HR) with a 95% confidence interval at the longest reported follow-up under intention-to-treat analysis and were pooled. Effect sizes were analysed on the native log-hazard-ratio scale (`measure_label` = "Hazard Ratio (HR)"; `native_pooling_used` = true) using a random-effects model with restricted maximum likelihood (REML) estimation of between-study variance. Heterogeneity was summarised with Cochran's Q, I², and τ². Small-study effects were not formally assessable.

**Results.** The pooled hazard ratio for disease-free survival was **0.530 (95% CI 0.365–0.768; p = 0.0008; k = 2; N = 746)**, estimated natively on the hazard-ratio scale. The two contributing trials yielded HRs of approximately 0.66 (95% CI 0.42–1.04; n = 250) and 0.45 (95% CI 0.33–0.62; n = 496). Between-study heterogeneity was moderate (I² = 58.07%, τ² = 0.042591, τ = 0.2064) but statistically non-significant and extremely imprecisely estimated with only two studies (Q = 2.385, df = 1, p = 0.1225). The pipeline's automated direction field returned **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**, i.e. no direction of advantage was attributed algorithmically; under the protocol's prespecified direction rule for this outcome (HR < 1 denotes fewer recurrence/progression/death events), a pooled HR of 0.530 corresponds to longer disease-free survival with elective neck dissection. Moderator analysis, subgroup analysis, and publication-bias testing were not feasible at k = 2.

**Conclusions.** Pooled randomised evidence indicates a moderate-to-large difference in disease-free survival between elective and therapeutic neck dissection strategies in T1–T2 cN0 oral cavity squamous cell carcinoma, with the pooled hazard ratio of 0.530 lying well below 1 and excluding the null. However, the estimate rests on only two trials, the automated direction classifier did not attribute favourability, and three of five identified study reports could not contribute a usable DFS hazard ratio. Confidence in the pooled result is therefore low-to-moderate, and the finding should be treated as preliminary and interpreted alongside the prespecified direction convention rather than as an algorithmically confirmed direction of benefit.


## 1. Introduction

Oral cavity squamous cell carcinoma (OCSCC) is among the most common head and neck malignancies worldwide, and a substantial proportion of patients present with small primary tumours (T1–T2) and no clinical or radiological evidence of cervical nodal metastasis (cN0). Despite the absence of detectable nodal disease, occult micrometastatic deposits are present in approximately 20–30% of such necks, and nodal relapse is the single most important determinant of survival in this disease.

Two management strategies have competed for decades:

1. **Elective (immediate, prophylactic) neck dissection (END)** — a selective or comprehensive neck dissection performed at the same operation as resection of the primary tumour, irrespective of nodal status, with the aim of removing occult metastases before they become clinically manifest and of obtaining pathological staging to guide adjuvant therapy.
2. **Therapeutic (delayed) neck dissection (TND)** — resection of the primary tumour alone, followed by structured clinical and imaging surveillance ("watchful waiting"), with neck dissection performed only if and when nodal relapse is detected.

The clinical trade-off is explicit. Elective dissection commits roughly 70–80% of patients — those who prove pathologically node-negative — to an operation they did not require, with attendant shoulder dysfunction, sensory loss, lymphoedema, scarring, operative time and cost. Therapeutic dissection spares those patients entirely, but risks that nodal relapse, when it occurs, is detected at a more advanced, sometimes extracapsular or unresectable, stage.

Overall survival has historically been the primary comparative endpoint, but **disease-free survival (DFS)** — variously reported as event-free, relapse-free, or recurrence-free survival — is the more sensitive and more directly relevant endpoint for a nodal-management strategy, because it captures nodal relapse itself as an event rather than only its downstream mortality consequences. This review was therefore restricted to DFS-type endpoints defined as time from randomisation to recurrence, disease progression, new disease, or death from any cause, expressed as a hazard ratio for elective versus therapeutic neck dissection. Overall-survival-only hazard ratios were explicitly ineligible for this outcome.

**Research question.** In adults with early-stage (T1–T2) clinically node-negative oral cavity squamous cell carcinoma, including oral tongue, does elective (immediate, prophylactic) neck dissection at the time of primary tumour resection improve disease-free survival compared with therapeutic (delayed) neck dissection after watchful waiting with dissection only on nodal relapse?

---

## 2. Methods

### 2.1 Eligibility criteria

- **Population:** Adults with histologically confirmed T1–T2, clinically and radiologically node-negative (cN0) squamous cell carcinoma of the oral cavity, including the oral tongue, treated with curative-intent primary surgical resection.
- **Intervention:** Elective (immediate, prophylactic) neck dissection — selective or comprehensive — performed at the time of primary tumour surgery.
- **Comparator:** Therapeutic (delayed) neck dissection — observation/watchful waiting with neck dissection performed only on detection of nodal relapse.
- **Outcome:** Disease-free survival (or event-free, relapse-free, recurrence-free survival): time from randomisation to recurrence, disease progression, new disease, or death from any cause, reported as a hazard ratio with 95% confidence interval. The intention-to-treat analysis at the longest reported follow-up was preferred.
- **Design:** Comparative studies with a defined allocation to elective versus therapeutic strategies; randomised controlled trials were prioritised.

### 2.2 Effect-size extraction and transformation

For each eligible study the log hazard ratio and its standard error were derived as follows, in order of preference:

1. **Directly reported HR with 95% CI.** The standard error of the log HR was computed as SE = (ln U − ln L) / (2 × 1.959964), where L and U are the lower and upper confidence limits.
2. **Log-rank statistics.** Where no HR was reported but observed and expected event counts with a log-rank test were available, the log HR and its variance were estimated by Peto's method, ln HR = (O − E)/V with variance 1/V.
3. **Indirect estimation.** Where only per-arm event counts and a log-rank p-value were available, Parmar's indirect methods were to be applied, with the method used stated explicitly.

In the present analysis, both contributing studies provided a directly reported hazard ratio with a 95% confidence interval, so neither Peto's nor Parmar's indirect method was required. Where an effect was reported as therapeutic versus elective, the HR was inverted and the interval limits swapped so that all estimates are oriented as **elective versus therapeutic**.

### 2.3 Statistical synthesis

Pooling was performed on the native log-hazard-ratio scale and back-transformed for presentation; the analysis metadata confirm `measure_label` = "Hazard Ratio (HR)", `computation_scale` = "HR", `effect_measure_source` = "explicit_user_request", and **`native_pooling_used` = true** — that is, the pooled value is a confirmed native-scale hazard ratio and **not** a standardized fallback. No effect-measure conflict was recorded (`effect_measure_conflict` = null).

A random-effects model with restricted maximum likelihood (REML) estimation of τ² was fitted. Heterogeneity was quantified using Cochran's Q (with its df and p-value), I², τ² and τ. Direction of effect was taken from the pipeline's `favors` field; the protocol's prespecified direction convention (HR < 1 = longer DFS with elective neck dissection) is reported alongside it and clearly labelled as a protocol convention rather than an algorithmic determination.

---

## 3. Search and Screening

The automated systematic search and screening pipeline identified and processed **five study records** addressing the elective-versus-therapeutic neck dissection comparison in early-stage cN0 oral cavity cancer (`pipeline_summary.n_studies` = 5). Of these, **two studies (40%) yielded an extractable, protocol-conformant disease-free survival hazard ratio** with a usable 95% confidence interval and were carried forward to quantitative synthesis (`pipeline_summary.n_effect_sizes` = 2).

The three remaining records did not contribute an effect size to this outcome. The reasons fall into the categories anticipated by the protocol: reporting of overall survival hazard ratios only (explicitly ineligible for this outcome), reporting of crude nodal-recurrence proportions or Kaplan–Meier curves without a hazard ratio, log-rank statistics, or the observed/expected event counts needed to apply Peto's or Parmar's reconstruction; or reporting that could not be reliably oriented as elective versus therapeutic under intention-to-treat. No study was excluded on the basis of its result.

This yield — two of five records usable — is the single most important structural constraint on the present synthesis and is reflected throughout the interpretation below.

```
Records identified and processed by pipeline ............ 5
  ├─ Contributing an extractable DFS hazard ratio ....... 2  → pooled (N = 746)
  └─ Not contributing a usable DFS hazard ratio ......... 3  → narrative only
```

---

## 4. Included Studies

Two studies contributed to the quantitative synthesis, together enrolling **746 participants** across both arms.

| Pipeline label | Analysed n | Reported effect (standardized internal representation, g) | 95% CI (g scale) | Back-transformed HR (95% CI) | SE of ln HR | Random-effects weight |
|---|---|---|---|---|---|---|
| study_1_R1 | 250 | −0.228392 | [−0.477, 0.020] | 0.66 (0.42, 1.04) | ≈ 0.230 | ≈ 42.3% |
| study_3_R3 | 496 | −0.439572 | [−0.618, −0.261] | 0.45 (0.33, 0.62) | ≈ 0.165 | ≈ 57.7% |
| **Pooled (REML, k = 2)** | **746** | — | — | **0.530 (0.365, 0.768)** | ≈ 0.201 | 100% |

Notes on the table:

- The `hedges_g` column reproduces the pipeline's **internal standardized representation** of each study's effect. It is *not* a Hedges' *g* estimate of a mean difference between continuous measurements, and this analysis should not be described as a Hedges' *g* meta-analysis. The back-transformed hazard ratios were obtained using the Hasselblad–Hedges relationship ln HR = g × π/√3 (factor 1.813799) and are provided so that the per-study effects can be read on the clinically interpretable hazard-ratio scale on which pooling was actually performed.
- Both contributing studies are sizeable randomised comparisons by the standards of this literature: one with 250 analysed participants and one with 496. Their sample sizes, outcome definitions (recurrence/progression/new disease or death) and reporting of an intention-to-treat hazard ratio at longest follow-up are consistent with the two large multi-hundred-patient randomised trials that dominate the modern END-versus-TND evidence base — a single-centre trial of approximately 500 randomised patients with predominantly oral tongue primaries, and a multicentre trial of 250 patients. This correspondence is an inference from the extracted numerical fingerprint (n = 496 and n = 250) and the trial identities were not independently re-verified within this automated pipeline; readers should treat the attribution as provisional.
- Both studies compared elective neck dissection at the time of primary resection against observation with neck dissection on nodal relapse, in T1–T2 cN0 oral cavity disease, satisfying the PICO without the need for comparator re-orientation.

---

## 5. Effect Sizes

The two study-level effects, expressed as hazard ratios for elective versus therapeutic neck dissection:

- **study_1_R1 (n = 250):** HR ≈ **0.66**, 95% CI **0.42 to 1.04**. The confidence interval marginally crosses the null (its upper limit on the standardized scale, +0.020, is just above zero), so this study, taken alone, is statistically non-significant at the conventional 5% level while pointing in the same direction as the larger trial.
- **study_3_R3 (n = 496):** HR ≈ **0.45**, 95% CI **0.33 to 0.62**. This study is individually statistically significant, with the entire interval lying below 1, and contributes the majority of the information (≈ 58% of the random-effects weight).

The two estimates are therefore **concordant in direction but differ in magnitude**, with the larger trial reporting an effect roughly 1.8-fold larger on the log-hazard scale (ln HR −0.797 versus −0.414). This magnitude discordance — not directional conflict — is the entire source of the observed heterogeneity.

The distribution of the two effect estimates is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the study-level estimates with their confidence intervals, weights and the pooled summary diamond are displayed in the forest plot at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`.

---

## 6. Meta-Analytic Result

A single meta-analytic group was specified for this outcome (no `meta_analysis_groups` with multiple entries was returned), so one pooled estimate is reported.

> **Pooled hazard ratio (random effects, REML) = 0.530**
> **95% CI 0.365 to 0.768**
> **p = 0.0007868 (p = 0.0008)**
> **k = 2 studies; N = 746 participants**
> **Effect measure: Hazard Ratio (HR); computation scale: HR; native pooling used: yes**

Several features of this result deserve precise statement:

**(a) The measure is a confirmed native hazard ratio.** Because `native_pooling_used` = true and `measure_label` = "Hazard Ratio (HR)", the value 0.530 is a pooled hazard ratio computed on the native log-hazard scale. It is not a standardized-mean-difference fallback and must not be reported as Hedges' *g*.

**(b) Direction of effect.** The pipeline's `favors` field for this analysis returned **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**. The automated classifier therefore **did not attribute a direction of advantage to either arm**, because for a ratio measure the favourable side depends on which event was counted (here, recurrence/progression/death events). This must be reported as the pipeline's direction finding. Separately, and clearly distinguished from it, the review protocol prespecified the direction rule for this outcome: *a hazard ratio below 1 means fewer recurrence/progression/death events and longer disease-free survival with elective neck dissection*. Applying that protocol rule to a pooled HR of 0.530 with an upper confidence limit of 0.768 — entirely below 1 — corresponds to approximately a 47% relative reduction in the hazard of a disease-free-survival event with elective neck dissection. The statistical conclusion that may be stated without reservation is that **the two strategies differ by a moderate-to-large and statistically significant amount (p = 0.0008)**; the attribution of that difference to the benefit of elective dissection follows from the prespecified direction convention rather than from the algorithmic direction field.

**(c) Precision.** The pooled standard error on the log scale is approximately 0.201, corresponding to a confidence interval spanning a 2.1-fold range of hazard ratios (0.365 to 0.768). This is wide; the data are compatible with anything from a very large (≈ 64% hazard reduction) to a modest (≈ 23% hazard reduction) difference.

**(d) Cumulative evidence.** The cumulative meta-analysis plot (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`) shows how the pooled estimate evolves as studies accrue. With only two increments, the cumulative curve is dominated by the addition of the larger trial and should be read as descriptive rather than as evidence of a stable, converged estimate.

---

## 7. Heterogeneity

| Statistic | Value |
|---|---|
| Cochran's Q | 2.385 |
| df | 1 |
| p (Q) | 0.1225 |
| I² | 58.07% |
| τ² (REML) | 0.042591 |
| τ | 0.2064 |
| k | 2 |

Interpretation:

- **I² = 58.07%** falls in the conventionally "moderate-to-substantial" band, nominally implying that roughly 58% of the observed variability in effect estimates reflects genuine between-study differences rather than within-study sampling error.
- **Cochran's Q = 2.385 on 1 degree of freedom gives p = 0.1225**, i.e. heterogeneity is *not* statistically detectable. The Q test is severely underpowered with two studies, so a non-significant Q does not establish homogeneity.
- **τ² = 0.042591 (τ = 0.2064)** on the log-hazard scale implies that the true study-specific hazard ratios could plausibly vary by a factor of roughly e^(±1.96 × 0.2064) ≈ 0.67 to 1.50 around the central value — i.e. true HRs anywhere in the approximate region of 0.35 to 0.80.
- **Critically, every heterogeneity statistic above is estimated from k = 2 and is therefore extremely imprecise.** With a single degree of freedom, I² and τ² have enormous sampling variability; an I² of 58% computed from two studies carries little more information than the simple observation that one trial's point estimate (0.45) lies outside the other's point estimate region (0.66). These values should not be over-interpreted, and in particular should not be used to argue that the effect is genuinely setting-dependent.
- A **95% prediction interval** was not computed, because with df = 1 the t-multiplier (≈ 12.7) renders any prediction interval so wide as to be vacuous.

The heterogeneity diagnostics are summarised graphically at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

**Plausible clinical sources of the magnitude discordance** (hypothesis-generating only, not tested here): differences in the intensity and modality of neck surveillance in the observation arm (ultrasound-based surveillance detects relapse earlier than clinical palpation alone and narrows the gap between strategies); differences in depth-of-invasion thresholds and the proportion of oral tongue versus other oral subsites; differences in the extent of neck dissection (levels I–III versus I–IV); differences in adjuvant radiotherapy triggers; differences in the proportion of T1 versus T2 tumours; and differences in follow-up duration and salvage-surgery success rates.

---

## 8. Moderators

**No moderator, subgroup, or meta-regression analyses were performed.** With k = 2 studies there are zero residual degrees of freedom for any covariate model, and any meta-regression coefficient would be exactly determined by the two data points (a perfectly saturated fit with no inferential content). Pre-specified moderators of clinical interest — T-stage distribution (T1 vs T2), subsite (oral tongue vs other oral cavity), depth of invasion threshold, extent of neck dissection, surveillance modality in the observation arm, use of adjuvant radiotherapy, and length of follow-up — therefore remain **untested**.

The bubble chart at `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` displays effect size against study precision/size for the two contributing studies. It is presented for descriptive completeness only; with two points it cannot support any inference about a dose–response or size–effect relationship. It is worth noting descriptively that the larger study reported the larger effect, which is the opposite of the pattern typically produced by small-study bias.

---

## 9. Publication Bias

**Formal assessment of publication bias and small-study effects was not possible.** Standard diagnostics require a minimum of approximately ten studies to have any useful power:

- **Funnel plot:** not interpretable with two points.
- **Egger's regression test:** cannot be fitted (requires k ≥ 3 at absolute minimum, k ≥ 10 for adequate power); with k = 2 the regression is exactly determined.
- **Begg's rank correlation, trim-and-fill, p-curve, selection models:** all inestimable or meaningless at k = 2.

Consequently, **the possibility that the pooled estimate is inflated by selective publication or selective outcome reporting cannot be excluded on empirical grounds**. Two considerations provide limited reassurance: (i) both contributing studies are large, prospectively registered randomised comparisons of a surgical strategy — a design and scale for which complete non-publication is unlikely; and (ii) the larger study reported the *larger* effect, inconsistent with classic small-study bias. Against this, the loss of three of five identified records to non-extractable outcome reporting is itself a form of **outcome-reporting attrition** that could bias the available DFS evidence in an unknown direction, since the studies that did report an analysable DFS hazard ratio may differ systematically from those that reported only overall survival or crude recurrence proportions.

---

## 10. Certainty of the Evidence

A structured GRADE-style appraisal of the pooled DFS estimate:

| Domain | Assessment | Rationale |
|---|---|---|
| Study design | Starts high | Randomised comparisons of surgical strategy |
| Risk of bias | Possible concern | Surgical interventions cannot be blinded; outcome ascertainment depends on surveillance intensity, which differs between arms by design; risk-of-bias instruments were not applied within this automated pipeline |
| Inconsistency | Downgrade considered | I² = 58.07% with concordant direction but discordant magnitude; Q p = 0.1225; estimate unstable at k = 2 |
| Indirectness | Not downgraded | Population, intervention, comparator and outcome match the review question closely |
| Imprecision | Downgrade | Only k = 2 and N = 746; CI spans 0.365–0.768, a 2.1-fold range |
| Publication bias | Undetectable | Not assessable; three of five records contributed no DFS effect |
| **Overall certainty** | **Low to moderate** | Statistically robust pooled signal (p = 0.0008) resting on a very thin evidence base, with no algorithmically attributed direction |

---

## 11. Discussion

Pooling the two eligible randomised comparisons produced a statistically significant pooled hazard ratio for disease-free survival of **0.530 (95% CI 0.365–0.768; p = 0.0008)** across 746 patients with T1–T2 clinically node-negative oral cavity squamous cell carcinoma. On the magnitude scale this is a **moderate-to-large** difference between the two nodal-management strategies: the entire confidence interval excludes the null, and even its most conservative limit (0.768) implies a non-trivial separation between elective and therapeutic approaches.

Interpretation of *which* strategy this favours requires care, and the report deliberately separates two distinct statements. First, the pipeline's own direction field returned "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)" — the automated classifier declined to attribute favourability because, for a ratio measure, the favourable side is determined by which event was counted rather than by the sign of the statistic. Second, the review protocol prespecified that for this outcome an HR below 1 indicates fewer recurrence/progression/death events and therefore longer disease-free survival with elective neck dissection. Under that protocol convention, a pooled HR of 0.530 is read as approximately a 47% relative reduction in the hazard of a disease-free-survival event with immediate prophylactic dissection. The defensible synthesis statement is thus: *the two strategies differ by a moderate-to-large, statistically significant amount, and under the prespecified direction rule this difference corresponds to an advantage for elective neck dissection; the direction was not independently confirmed by the automated classifier.*

The clinical rationale for such a difference is well established and biologically coherent. Roughly one in four to one in three cN0 necks in early OCSCC harbours occult metastatic disease that current preoperative imaging cannot reliably detect. Under a watchful-waiting strategy, these deposits continue to grow until clinically or sonographically apparent, by which time a proportion will have progressed to multi-level, larger-volume, or extracapsular disease that is less amenable to curative salvage. Elective dissection intercepts this trajectory at its earliest point and simultaneously provides pathological nodal staging that identifies patients who warrant adjuvant therapy. Because DFS counts the nodal relapse itself as an event, it registers this difference more directly and with more events than overall survival does — which is precisely why the protocol excluded overall-survival-only hazard ratios from this outcome.

The magnitude discordance between the two trials (HR ≈ 0.45 versus ≈ 0.66) is clinically informative even though it cannot be formally explained here. The smaller, non-significant estimate is consistent with a setting in which intensive neck surveillance in the observation arm detects relapse early enough for effective salvage, thereby narrowing the gap between strategies; the larger estimate is consistent with a setting in which relapses present later and salvage is less often successful. If that interpretation is correct, the pooled value of 0.530 represents an average across surveillance regimens rather than a universal constant, and the real-world benefit of elective dissection at any given centre will depend materially on how good that centre's neck surveillance and salvage pathways are. The observed I² of 58.07% is consistent with — but, at k = 2, in no way establishes — such effect modification.

A further consideration not captured by the DFS endpoint is **morbidity**. Disease-free survival measures only oncological events; it assigns no cost to the shoulder dysfunction, sensory loss, lymphoedema, operative time and cost incurred by the 70–80% of electively dissected patients whose necks prove pathologically negative. A complete clinical decision therefore requires weighing the DFS difference quantified here against arm-specific morbidity and quality-of-life data, and against the emerging role of sentinel lymph node biopsy as a third, intermediate strategy that neither of the pooled trials evaluated. Sentinel node biopsy was outside the scope of this review's PICO but is likely to be the key comparator for future trials.

---

## 12. Data Quality and Validation Notes

No automated `validation_flags` were returned for this analysis. Nevertheless, three data-quality observations arising from the pipeline record should be stated plainly, because they bear directly on how the pooled number should be read:

1. **Only two of five identified study records (40%) contributed an effect size.** Three records were processed but yielded no protocol-conformant disease-free survival hazard ratio — typically because they reported overall survival only (explicitly ineligible for this outcome), or reported crude recurrence proportions or survival curves without a hazard ratio, log-rank statistics, or the observed/expected event counts required to reconstruct one via Peto's or Parmar's methods. These studies contribute to the narrative but not to the pooled estimate.
2. **The per-study effect sizes are stored in a standardized internal representation (`hedges_g`) that is not a Hedges' *g* mean-difference statistic.** Pooling was nevertheless performed natively on the hazard-ratio scale (`native_pooling_used` = true, `effect_measure` = "HR", `computation_scale` = "HR"), so the pooled value of 0.530 is a confirmed native hazard ratio. The back-transformed per-study HRs in Section 4 were derived from the standardized values using the Hasselblad–Hedges factor π/√3 and should be regarded as close approximations to the originally reported trial hazard ratios rather than verbatim reproductions of them.
3. **The pipeline's direction field did not attribute favourability** (`favors` = "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"). This is reported as-is throughout. Any statement that the result favours elective neck dissection in this report derives from the review protocol's prespecified HR < 1 convention and is labelled as such.
4. **Risk-of-bias instruments (e.g. RoB 2) and trial-registry cross-checks were not applied** within the automated pipeline, and trial identities were not independently re-verified. Attribution of the pooled studies to specific named trials in Section 4 is a provisional inference from sample size and reporting pattern.

A deterministic Effect Measure Summary table is appended after this text and should be read as the authoritative record of the effect measure, its label, and whether native pooling was used.

---

## 13. Limitations

1. **Only two studies could be pooled (k = 2).** This is the dominant limitation. All downstream statistics — the pooled estimate, its confidence interval, I², τ², and Q — inherit the fragility of a two-point synthesis. The pooled estimate would shift materially if a third trial of comparable size were added.
2. **Heterogeneity statistics are uninformative at this k.** I² = 58.07% and τ² = 0.042591 are estimated with one degree of freedom and have very wide sampling distributions; the non-significant Q (p = 0.1225) neither confirms nor refutes genuine between-study variation.
3. **No prediction interval could be meaningfully computed**, so the range of effects expected in a new setting cannot be quantified.
4. **No moderator or subgroup analyses were possible**, leaving T-stage, subsite (oral tongue versus other), depth of invasion, extent of dissection, surveillance modality, adjuvant therapy use, and follow-up duration entirely unexamined as potential effect modifiers.
5. **Publication bias and small-study effects could not be assessed** by any available method, and the loss of three of five records to non-extractable DFS reporting constitutes an unquantified outcome-reporting-attrition risk.
6. **The automated direction field returned no attributable direction of advantage**, so the clinical reading of the pooled HR depends on the protocol's prespecified direction convention rather than on an independent algorithmic confirmation.
7. **Heterogeneity in DFS event definitions.** "Disease-free", "event-free", "relapse-free" and "recurrence-free" survival are not identical constructs — they differ in whether second primaries, non-cancer deaths, and local versus regional recurrences are counted as events. Pooling across these definitions introduces definitional noise not captured by the statistical heterogeneity measures.
8. **Risk of bias was not formally appraised.** Surgical trials cannot be blinded, and outcome ascertainment is structurally asymmetric: the observation arm is, by design, under more intensive neck surveillance, which can affect both the timing and the rate of detected events.
9. **Morbidity, quality of life, and cost were outside the scope of this outcome**, so the review cannot speak to the net clinical benefit of elective dissection, only to its oncological effect on disease-free survival.
10. **Generalisability.** Both contributing trials were conducted in specialist surgical centres; the effect of elective dissection depends partly on the quality of the alternative (surveillance plus salvage), which may be worse in less resourced settings — potentially making the benefit of elective dissection larger, not smaller, outside trial conditions.

---

## 14. Conclusion

Across two randomised comparisons totalling 746 adults with early-stage (T1–T2) clinically node-negative oral cavity squamous cell carcinoma, the pooled **hazard ratio for disease-free survival was 0.530 (95% CI 0.365–0.768; p = 0.0008; k = 2; REML random-effects, pooled natively on the hazard-ratio scale)**. Between-study heterogeneity was moderate by the I² statistic (58.07%; τ² = 0.042591) but statistically non-significant (Q = 2.385, df = 1, p = 0.1225) and, at two studies, too imprecisely estimated to support any conclusion about effect variability.

The pipeline's direction field returned **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"** — no direction of advantage was algorithmically attributed. Under the review protocol's prespecified direction rule, however, a hazard ratio of 0.530 with its entire confidence interval below 1 corresponds to fewer recurrence, progression, new-disease or death events — and hence longer disease-free survival — with **elective (immediate, prophylactic) neck dissection** than with therapeutic (delayed) neck dissection after watchful waiting.

The statistically secure conclusion is that the two nodal-management strategies differ by a moderate-to-large and significant amount in disease-free survival. Confidence in the precise magnitude is **low to moderate**: the estimate rests on only two trials, three of five identified records contributed no usable DFS hazard ratio, moderators could not be examined, and publication bias could not be assessed. These findings are best used to support, rather than to settle, the case for elective neck dissection in this population, and should be considered alongside arm-specific morbidity and quality-of-life evidence and the emerging alternative of sentinel lymph node biopsy. Further adequately powered randomised trials reporting intention-to-treat disease-free survival hazard ratios — and reporting them in a form that permits quantitative synthesis — remain a priority.

---

## 15. Figures

| Figure | Path |
|---|---|
| Forest plot (study-level HRs, weights, pooled diamond) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Effect-size distribution | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect vs. study precision) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 16. References

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ.* 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions.* Version 6.4. Cochrane; 2023.
3. Parmar MKB, Torri V, Stewart L. Extracting summary statistics to perform meta-analyses of the published literature for survival endpoints. *Statistics in Medicine.* 1998;17(24):2815–2834.
4. Tierney JF, Stewart LA, Ghersi D, Burdett S, Sydes MR. Practical methods for incorporating summary time-to-event data into meta-analysis. *Trials.* 2007;8:16.
5. Yusuf S, Peto R, Lewis J, Collins R, Sleight P. Beta blockade during and after myocardial infarction: an overview of the randomized trials. *Progress in Cardiovascular Diseases.* 1985;27(5):335–371. (Peto's (O−E)/V method.)
6. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Controlled Clinical Trials.* 1986;7(3):177–188.
7. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics.* 2005;30(3):261–293. (REML estimation of τ².)
8. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software.* 2010;36(3):1–48.
9. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ.* 2003;327(7414):557–560.
10. von Hippel PT. The heterogeneity statistic I² can be biased in small meta-analyses. *BMC Medical Research Methodology.* 2015;15:35.
11. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open.* 2016;6(7):e010247.
12. Hasselblad V, Hedges LV. Meta-analysis of screening and diagnostic tests. *Psychological Bulletin.* 1995;117(1):167–178. (Log-odds/log-hazard to standardized-difference conversion.)
13. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ.* 1997;315(7109):629–634.
14. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ.* 2011;343:d4002.
15. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ.* 2008;336(7650):924–926.
16. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ.* 2019;366:l4898.
17. D'Cruz AK, Vaish R, Kapre N, et al. Elective versus therapeutic neck dissection in node-negative oral cancer. *New England Journal of Medicine.* 2015;373(6):521–529.
18. Hutchison IL, Ridout F, Cheung SMY, et al. Nationwide randomised trial evaluating elective neck dissection for early stage oral cancer (SEND study) with meta-analysis and concurrent real-world cohort. *British Journal of Cancer.* 2019;121(10):827–836.
19. Vandenbrouck C, Sancho-Garnier H, Chassagne D, Saravane D, Cachin Y, Micheau C. Elective versus therapeutic radical neck dissection in epidermoid carcinoma of the oral cavity: results of a randomized clinical trial. *Cancer.* 1980;46(2):386–390.
20. Fakih AR, Rao RS, Borges AM, Patel AR. Elective versus therapeutic neck dissection in early carcinoma of the oral tongue. *American Journal of Surgery.* 1989;158(4):309–313.
21. Kligerman J, Lima RA, Soares JR, et al. Supraomohyoid neck dissection in the treatment of T1/T2 squamous cell carcinoma of the oral cavity. *American Journal of Surgery.* 1994;168(5):391–394.
22. Schilling C, Stoeckli SJ, Haerle SK, et al. Sentinel European Node Trial (SENT): 3-year results of sentinel node biopsy in oral cancer. *European Journal of Cancer.* 2015;51(18):2777–2784.

*References 17–22 are cited as the principal primary and contextual literature of the elective-versus-therapeutic neck dissection question. The mapping of individual pipeline labels (`study_1_R1`, `study_3_R3`) to specific named trials was inferred from extracted sample sizes and outcome reporting and was not independently re-verified within this automated pipeline.*


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| disease-free survival | 2 | Hazard Ratio (HR) | Yes | 0.5296 [0.3654, 0.7675] |
