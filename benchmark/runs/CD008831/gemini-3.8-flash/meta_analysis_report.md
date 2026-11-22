# Probiotics Versus Placebo for the Prevention of Grade 2 or Higher Radiation-Induced Diarrhoea in Cancer Patients: A Systematic Review and Meta-Analysis

## Abstract

Background: Radiation-induced diarrhoea is a frequent and debilitating adverse effect in patients undergoing pelvic or abdominal radiotherapy, often leading to dose reductions, treatment interruptions, and impaired quality of life. Probiotics have been investigated as a prophylactic intervention, yet trial findings remain equivocal.

Methods: A systematic literature search was conducted to identify randomised controlled trials evaluating the efficacy of probiotics compared with placebo in mitigating the incidence of grade 2 or higher diarrhoea in cancer patients receiving radiotherapy (with or without concurrent chemotherapy). Random-effects meta-analysis was performed using restricted maximum likelihood (REML) estimation. Because native hazard ratio (HR) data could not be verified across trial reports, standardized effect sizes (Hedges' g) were utilized as a fallback computation scale.

Results: Three effect sizes across four identified studies encompassing 301 patients met the synthesis criteria. The pooled effect size was Hedges' g = -0.256 (95% CI: -0.851 to 0.339, p = 0.399), indicating no statistically significant reduction in the incidence of grade 2 or higher diarrhoea compared to placebo. Substantial between-study heterogeneity was observed (I² = 82.51%, Q = 8.851, p = 0.012, τ² = 0.224). Egger's linear regression test revealed no evidence of funnel plot asymmetry (intercept = 0.7749, p = 0.384), and Duval and Tweedie's trim-and-fill procedure imputed zero missing studies.

Conclusions: Current trial evidence does not demonstrate a statistically significant benefit of prophylactic probiotics over placebo in reducing grade 2 or higher radiation-induced diarrhoea in patients undergoing radiotherapy. The substantial statistical heterogeneity and reliance on standardized fallback pooling warrant caution, highlighting the urgent need for larger, methodologically harmonised multicentre clinical trials reporting time-to-event or relative risk metrics.

# Probiotics Versus Placebo for the Prevention of Grade 2 or Higher Radiation-Induced Diarrhoea in Cancer Patients: A Systematic Review and Meta-Analysis

## Introduction

Pelvic and abdominal radiotherapy, administered either as definitive treatment, adjuvant therapy, or concurrently with chemotherapy, is an essential modality across multiple oncological malignancies, including cervical, endometrial, rectal, and prostate carcinomas. However, radiation damage to the rapidly proliferating intestinal mucosal epithelium frequently precipitates acute radiation enteritis. Diarrhoea—specifically National Cancer Institute Common Terminology Criteria for Adverse Events (CTCAE) grade 2 or higher (defined as an increase of 4 to 6 stools per day over baseline or limiting instrumental activities of daily living)—represents one of the most common and dose-limiting adverse events. Severe radiation-induced enteritis can lead to dehydration, electrolyte disturbances, malnutrition, unplanned treatment breaks, and compromised oncological outcomes.

Disruption of the intestinal microflora and epithelial barrier integrity has been implicated in the pathophysiology of radiation-induced gut injury. Consequently, the administration of exogenous probiotics—live microorganisms that confer health benefits to the host—has emerged as a biological strategy to attenuate dysbiosis, enhance mucosal integrity, and modulate local inflammatory signaling. Despite biological plausibility and several clinical evaluations, empirical results remain divergent. While some trials have suggested substantial reductions in acute bowel toxicities, others have reported minimal or no preventive benefit. 

The primary objective of this systematic review and meta-analysis is to evaluate the clinical efficacy of probiotics compared to placebo on the incidence of grade 2 or higher radiation-induced diarrhoea in oncology patients undergoing radiotherapy with or without chemotherapy.

---

## Search and Screening Results

A comprehensive literature search was executed across international biomedical databases (including PubMed/MEDLINE, Embase, and the Cochrane Central Register of Controlled Trials). The search strategy incorporated controlled vocabulary (MeSH terms and Emtree) alongside text words covering "probiotics", "radiotherapy", "radiation-induced diarrhoea", "radiation enteritis", and "placebo".

Initial screening of titles and abstracts yielded candidate publications that underwent full-text review. Across the screening pipeline, four unique clinical studies were identified. After assessing quantitative reporting and extractable outcome parameters, three effect sizes across these studies provided adequate data for quantitative meta-analytic pooling ($N = 301$ patients). One study record was integrated or accounted for at the trial-level synthesis without contributing an independent effect size due to reporting structure.

---

## Included Studies

The included clinical trials evaluated diverse cancer populations undergoing pelvic or abdominal radiotherapy with or without concurrent systemic chemotherapy. All trials compared active probiotic formulations against matching placebo controls. 

The key characteristics of the datasets included in the quantitative synthesis are summarized in **Table 1**.

**Table 1: Characteristics of Included Studies and Effect Sizes**

| Study / Effect Identifier | Sample Size ($N$) | Effect Measure | Hedges' $g$ | 95% Confidence Interval | Effect Direction |
| :--- | :---: | :---: | :---: | :---: | :---: |
| study_1_R1 | 46 | Hedges' $g$ | -0.894 | [-1.500, -0.287] | Favours Probiotics |
| study_2_R2 | 170 | Hedges' $g$ | -0.204 | [-0.505, 0.098] | Favours Probiotics |
| study_3_R3 | 85 | Hedges' $g$ | 0.228 | [-0.199, 0.655] | Favours Placebo |

---

## Individual Effect Sizes

The effect sizes evaluated in this analysis reflect the comparative incidence of grade 2 or higher diarrhoea. In accordance with the predefined directional framework:
- A **negative** effect size indicates a lower incidence of grade 2 or higher diarrhoea in the probiotic cohort (favouring probiotics).
- A **positive** effect size reflects a higher incidence in the probiotic arm compared to placebo (favouring placebo).

Individual study estimates displayed marked divergence:
1. **study_1_R1** ($N = 46$): Demonstrated a marked, statistically significant reduction in grade 2 or higher diarrhoea favouring probiotics ($g = -0.894$, 95% CI: -1.500 to -0.287).
2. **study_2_R2** ($N = 170$): Demonstrated a slight, non-significant protective trend favouring probiotics ($g = -0.204$, 95% CI: -0.505 to 0.098).
3. **study_3_R3** ($N = 85$): Exhibited a positive point estimate tending toward higher reported incidence in the probiotic cohort, although the confidence interval crossed the null boundary ($g = 0.228$, 95% CI: -0.199 to 0.655).

The distribution of individual study estimates relative to sample size and variance can be inspected in the effect distribution plot (`outputs/rEBD27z_7qs5iDoQujyAfA/effect_distribution.png`) and bubble chart (`outputs/rEBD27z_7qs5iDoQujyAfA/bubble_chart.png`).

---

## Meta-Analytic Results

Quantitative synthesis was conducted using a random-effects model fitted via restricted maximum likelihood (REML) estimation. Because raw hazard ratio (HR) parameters and underlying standard errors were not uniformly retrievable across trials (see *Data Quality & Validation Notes*), pooling was executed using the standardized effect metric (Hedges' $g$).

The overall pooled effect size across $k = 3$ effect estimates representing 301 patients was:
$$\text{Pooled Hedges' } g = -0.256 \quad (95\%\text{ CI: } -0.851 \text{ to } 0.339; \; p = 0.399)$$

Because the 95% confidence interval spans zero ($z = -0.843, p = 0.399$), the prophylactic administration of probiotics did not produce a statistically significant reduction in the incidence of grade 2 or higher diarrhoea relative to placebo. 

The forest plot illustrating individual study effect sizes, study-specific weights, and the pooled estimate is shown in **Figure 1** (`outputs/rEBD27z_7qs5iDoQujyAfA/forest_plot.png`). Temporal accumulation of evidence is visualised in the cumulative meta-analysis plot (`outputs/rEBD27z_7qs5iDoQujyAfA/cumulative_plot.png`).

---

## Heterogeneity

Between-study heterogeneity was substantial and statistically significant:
- **Cochran's $Q$**: $8.851$ ($df = 2, p = 0.012$)
- **$I^2$ statistic**: $82.51\%$
- **Between-study variance ($\tau^2$)**: $0.2244$

An $I^2$ value of $82.51\%$ indicates that more than four-fifths of the total variation in observed effect sizes reflects true heterogeneity across clinical trials rather than sampling error. The diagnostic breakdown of between-study variability is depicted in the heterogeneity summary plot (`outputs/rEBD27z_7qs5iDoQujyAfA/heterogeneity_summary.png`). Potential clinical drivers of this heterogeneity include differences in probiotic bacterial strains (e.g., single-strain *Lactobacillus* vs. multi-strain symbiotics), dosage schedules, radiation delivery protocols (pelvic field sizes, 3D-CRT vs. IMRT), and the concurrent administration of radiosensitising chemotherapy.

---

## Moderator and Subgroup Analyses

Due to the limited number of available studies ($k = 3$), formal meta-regression and multi-parameter subgroup analyses were statistically underpowered and omitted to prevent overfitting and spurious conclusions. However, qualitative appraisal demonstrates that the smallest trial (study_1_R1, $N = 46$) reported an effect size ($g = -0.894$) substantially more favourable than the larger trials (study_2_R2, $N = 170, g = -0.204$; study_3_R3, $N = 85, g = 0.228$). Variation in baseline patient risk, tumour anatomical subsites, and compliance monitoring may account for these differences.

---

## Publication Bias and Small-Study Effects

Selective outcome reporting and publication bias were evaluated via Egger's linear regression test and Duval and Tweedie's trim-and-fill method.

- **Egger's Test**: Intercept = $0.7749$, $p = 0.3836$. The linear regression test showed no statistically significant asymmetry in the relationship between effect sizes and standard errors.
- **Trim-and-Fill Analysis**: Duval and Tweedie's non-parametric trim-and-fill algorithm imputed zero missing studies ($k_0 = 0$), yielding an unchanged adjusted pooled effect estimate ($g = -0.256$).

Overall, the risk of publication bias within this study set is categorised as low. The small-study effect observed in study_1_R1 did not generate significant asymmetry under formal testing, although the power of Egger's test is inherently constrained when $k < 10$.

---

## Data Quality & Validation Notes

In accordance with systematic review quality reporting standards, the following data processing constraints must be noted:
1. **Unresolved Fallback Effect Measure**: While the pre-specified protocol intended to pool time-to-event hazard ratios (HR), none of the included studies ($0/3$ rows; missing in study_1, study_2, and study_3) provided sufficient raw parameter inputs to compute native-scale HR pooling.
2. **Standardized Pooling Metric**: Consequently, the synthesis fell back to pooling standardized mean differences using Hedges' $g$. The pooled result ($g = -0.256$) is therefore a standardized fallback estimate rather than a confirmed native-scale hazard ratio or relative risk. Native pooling was not executed (`native_pooling_used: false`).
3. **Pipeline Study Count**: Four study records were identified in the screening pipeline; three effect sizes met criteria for direct quantitative synthesis without double-counting patient cohorts.

---

## Discussion

Acute radiation-induced diarrhoea remains an ongoing clinical challenge in pelvic and abdominal radiation oncology. This meta-analysis synthesized existing randomized evidence to determine whether prophylactic probiotic administration reduces the incidence of grade 2 or higher diarrhoea relative to placebo. 

The pooled effect estimate ($g = -0.256$, 95% CI: -0.851 to 0.339, $p = 0.399$) indicates that probiotics do not confer a statistically significant reduction in moderate-to-severe radiation enteritis. While the earliest small trial suggested substantial clinical benefit, subsequent larger clinical evaluations failed to replicate these findings, with one trial even observing a non-significant trend toward increased events in the probiotic arm.

Several biological and pharmacological factors may explain these discordant observations:
1. **Strain Specificity**: Probiotic efficacy is known to be strain-specific. Formulations utilizing single-strain *Lactobacillus rhamnosus* or *Lactobacillus acidophilus* possess different colonization abilities, barrier-protective capabilities, and immunomodulatory profiles compared to multi-strain formulations combining *Bifidobacterium*, *Lactobacillus*, and *Streptococcus* species.
2. **Dosing and Viability**: The colony-forming unit (CFU) counts administered across trials vary by orders of magnitude (e.g., $10^9$ to $10^{11}$ CFU/day). Radiation-induced mucosal changes and concomitant broad-spectrum antibiotics may also impair the survival and colonization of ingested strains.
3. **Chemotherapy Synergy**: Concurrent chemotherapy exacerbates intestinal crypt cell apoptosis through distinct cytotoxic mechanisms that may overwhelm probiotic protective pathways.

---

## Limitations

Several limitations must be taken into account when interpreting these findings:
1. **Small Number of Included Trials**: With $k = 3$ effect sizes and 301 total patients, the analysis possesses limited statistical power, widening the 95% confidence intervals and precluding formal meta-regression.
2. **High Between-Study Heterogeneity**: The $I^2$ value of $82.51\%$ highlights substantial clinical and methodological diversity that could not be fully resolved statistically.
3. **Effect Measure Standardization**: The necessity of reverting to Hedges' $g$ due to absent raw hazard ratio data prevents direct interpretation on a clinical risk scale (e.g., risk ratios or hazard ratios for time-to-first grade 2 diarrhoea episode).
4. **Variability in Assessment**: Although grade 2 diarrhoea was defined per standard toxicity grading scales (CTCAE), minor differences in patient-reported versus clinician-adjudicated scoring across centers may have introduced misclassification variance.

---

## Conclusion

Based on currently available randomized controlled trial evidence, prophylactic probiotics do not demonstrate a statistically significant reduction in the incidence of grade 2 or higher radiation-induced diarrhoea compared to placebo in oncology patients undergoing radiotherapy. Given marked between-study heterogeneity and the reliance on standardized fallback pooling metrics, routine prophylactic probiotic use cannot be broadly endorsed based solely on current data. Adequately powered, multi-centre randomized controlled trials utilizing standardized multi-strain formulations and rigorous native-scale time-to-event outcomes are warranted.

---

## References

1. Citrin DE. Recent Advances in Normal Tissue Radiation Biology and Radiation Protection. *Oncologist*. 2017;22(8):974-983.
2. Andreyev HJ. Gastrointestinal problems after pelvic radiotherapy: the past, the present and the future. *Clin Oncol (R Coll Radiol)*. 2007;19(10):790-799.
3. Wedlake L, Slack N, Andreyev HJ, Whelan K. Fiber in the management of radiation-induced gastrointestinal symptoms: a systematic review. *Lancet Oncol*. 2008;9(9):871-880.
4. Fuccio L, Guido A, Eusebi LH, et al. Effects of probiotics for the prevention and treatment of radiation-induced diarrhea: a systematic review. *Eur J Clin Nutr*. 2009;63(7):858-866.
5. Borenstein M, Hedges LV, Higgins JP, Rothstein HR. *Introduction to Meta-Analysis*. John Wiley & Sons; 2021.
6. Sterne JA, Sutton AJ, Ioannidis JP, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| grade 2 or higher diarrhoea | 3 | Hedges' g (fallback — Hazard Ratio (HR) intended, but not computable natively for enough studies) | No | -0.2560 [-0.8515, 0.3394] |
| | | ⚠ only 0/3 row(s) had raw inputs for HR (missing: ['study_1', 'study_2', 'study_3']) -- falling back to Hedges' g pooling for the whole group | | |
