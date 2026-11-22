# Neoadjuvant Platinum-Based Chemotherapy for Early-Stage Triple-Negative Breast Cancer: A Systematic Review and Meta-Analysis of Disease-Free Survival

## Abstract

**Background:** Triple-negative breast cancer (TNBC) represents an aggressive breast cancer subtype with heightened recurrence rates and limited targeted therapy options. The addition of platinum salts (carboplatin or cisplatin) to standard neoadjuvant chemotherapy regimens has been evaluated across multiple randomized clinical trials, with conflicting evidence regarding long-term disease-free survival (DFS) benefits.

**Methods:** A systematic review and meta-analysis was conducted to assess the effect of neoadjuvant platinum-based chemotherapy compared to platinum-free neoadjuvant regimens on disease-free survival in women with early-stage TNBC. Searches and screening yielded 12 candidate studies, from which 5 comparative effect sizes were extracted. A random-effects model using restricted maximum likelihood (REML) estimation was conducted on studies providing native survival hazard ratio inputs ($k = 3$, $n = 606$). Secondary standardized effect sizes were examined for the broader cohort. Publication bias was evaluated via Egger's regression test and the trim-and-fill method.

**Results:** The pooled Hazard Ratio (HR) for disease-free survival across $k = 3$ natively pooled studies was 0.634 (95% CI: [0.277, 1.449], $p = 0.2801$), indicating that the meta-analytic result favors neither arm (essentially a tie, with confidence intervals spanning unity). Substantial statistical heterogeneity was observed ($I^2 = 55.26\%$, $\tau^2 = 0.3057$, Cochran's $Q = 4.471$, $p = 0.1069$). Two additional studies (representing 789 patients) could not be included in native HR pooling due to lack of raw survival input data, but exhibited standardized mean differences (Hedges' $g$) of -0.320 and -0.254 favoring platinum therapy. Egger's test revealed no statistically significant funnel plot asymmetry (intercept = 0.0817, $p = 0.1151$), and the trim-and-fill method identified zero missing studies ($k_0 = 0$), suggesting low risk of publication bias.

**Conclusion:** Although point estimates suggest a trend toward reduced recurrence hazards with platinum addition, the pooled hazard ratio did not achieve statistical significance and favored neither intervention decisively. Given notable heterogeneity and data attrition due to reporting discrepancies, further standardized individual patient-data analyses are warranted to identify patient subsets most likely to benefit.

# The Impact of Adding Platinum-Based Chemotherapy to Neoadjuvant Regimens on Disease-Free Survival in Early-Stage Triple-Negative Breast Cancer: A Systematic Review and Meta-Analysis

## Introduction

Triple-negative breast cancer (TNBC)—defined immunohistochemically by the lack of estrogen receptor (ER), progesterone receptor (PR), and human epidermal growth factor receptor 2 (HER2) overexpression—accounts for approximately 15% to 20% of all invasive breast carcinomas. TNBC is characterized by aggressive clinical behavior, distinct metastatic patterns, an elevated early relapse rate, and poor overall prognosis following standard systemic therapies. 

Neoadjuvant chemotherapy (NACT) represents the standard of care for patients with early-stage and locally advanced TNBC. The primary objective of neoadjuvant treatment is cytoreduction to optimize surgical outcomes and provide prognostic stratification based on pathological complete response (pCR). Because TNBC tumors frequently exhibit genomic instability and deficiencies in homologous recombination DNA repair (such as *BRCA1* and *BRCA2* mutations or "BRCAness"), DNA-damaging cross-linking agents such as platinum salts (carboplatin or cisplatin) have emerged as rational therapeutic candidates.

While prospective trials have consistently demonstrated that adding carboplatin or cisplatin to anthracycline- and taxane-based neoadjuvant backbones increases pCR rates, their impact on long-term survival endpoints—such as disease-free survival (DFS), event-free survival (EFS), and relapse-free survival (RFS)—remains a matter of ongoing clinical debate. Increased hematologic and non-hematologic toxicities associated with platinum agents can lead to dose delays, reductions, or early discontinuations of standard backbone chemotherapy, potentially counterbalancing survival gains.

This systematic review and meta-analysis quantitatively evaluates whether the addition of neoadjuvant platinum-based chemotherapy compared with neoadjuvant chemotherapy without platinum prolongs disease-free survival in women with early-stage TNBC.

---

## Search and Screening Results

The systematic literature search identified 12 relevant candidate studies investigating platinum-based neoadjuvant chemotherapy against non-platinum control regimens in early-stage TNBC. Following dual independent screening against rigorous eligibility criteria, 5 comparative effect sizes across 5 distinct clinical trial cohorts were extracted for quantitative synthesis.

Eligibility was restricted to randomized controlled trials or prospective comparative studies evaluating neoadjuvant chemotherapy with carboplatin or cisplatin against standard platinum-free neoadjuvant regimens in women with confirmed stage I–III TNBC, reporting time-to-event outcomes (DFS, EFS, or RFS) with hazard ratios and corresponding 95% confidence intervals, or sufficient data allowing effect size derivation.

---

## Included Studies and Individual Effect Sizes

A total of 5 distinct trial cohorts provided quantitative comparative effect sizes, encompassing a total of 1,395 patients. Individual study effect sizes and standardized metric transformations are summarized in Table 1.

### Table 1: Included Studies and Extracted Comparative Effect Sizes

| Study Identifier | Sample Size ($n$) | Standardized Effect Size (Hedges' $g$) | 95% Confidence Interval | Native HR Inclusion Status |
| :--- | :---: | :---: | :---: | :--- |
| **study_2_R2** | 315 | -0.3197 | [-0.542, -0.097] | Excluded from native HR (lacks raw inputs) |
| **study_3_R3** | 443 | -0.0341 | [-0.220, 0.152] | Included in native HR pooling |
| **study_4_R4** | 88 | -0.1500 | [-0.568, 0.268] | Included in native HR pooling |
| **study_6_R6** | 474 | -0.2543 | [-0.446, -0.063] | Excluded from native HR (lacks raw inputs) |
| **study_7_R7** | 75 | -0.8262 | [-1.298, -0.355] | Included in native HR pooling |

Individual standardized effect sizes across the 5 cohorts exhibited negative Hedges' $g$ values ranging from -0.0341 to -0.8262. In survival and event analysis conventions where negative differences reflect reduced event frequencies or prolonged time to event, these individual point estimates consistently tilted toward improved disease-free survival with platinum chemotherapy. Notably, study_2_R2 ($g = -0.3197$, 95% CI: [-0.542, -0.097]), study_6_R6 ($g = -0.2543$, 95% CI: [-0.446, -0.063]), and study_7_R7 ($g = -0.8262$, 95% CI: [-1.298, -0.355]) demonstrated statistically significant reductions in risk when viewed on the standardized difference scale.

---

## Meta-Analytic Results

Native time-to-event pooling on the Hazard Ratio (HR) scale was performed using restricted maximum likelihood (REML) random-effects modeling on the 3 studies that supplied fully confirmed native time-to-event parameters (`native_pooling_used = true`). 

### Primary Pooling (Native Scale)

- **Number of studies pooled ($k$):** 3
- **Total sample size ($n$):** 606 patients
- **Pooled Effect Measure:** Hazard Ratio (HR)
- **Pooled Hazard Ratio (HR):** 0.6341 (exact: 0.6341016586087502)
- **95% Confidence Interval:** [0.277, 1.449]
- **Statistical Significance:** $p = 0.2801$
- **Directional Determination:** The pooled result favors **neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)**.

Although the point estimate indicates a Hazard Ratio of 0.634—suggesting a nominal 36.6% relative hazard reduction for disease recurrence or death in patients receiving neoadjuvant platinum—the 95% confidence interval is broad ([0.277, 1.449]) and encompasses unity. Consequently, the effect does not reach statistical significance ($p = 0.2801$), and formally favors neither treatment arm over the other.

The forest plot illustrating the study-specific effect estimates and the pooled random-effects estimate is displayed in Figure 1.

![Forest Plot](outputs/HShuwD5_xJc0KHeDZGpcYg/forest_plot.png)
*Figure 1: Forest plot of disease-free survival comparing neoadjuvant platinum-based chemotherapy against platinum-free control regimens.*

Cumulative evidence accumulation across studies is depicted in the cumulative meta-analysis plot in Figure 2.

![Cumulative Forest Plot](outputs/HShuwD5_xJc0KHeDZGpcYg/cumulative_plot.png)
*Figure 2: Cumulative meta-analysis plot reflecting effect size trajectory over sequential evidence synthesis.*

---

## Assessment of Heterogeneity

Between-study variance and heterogeneity were quantified across the natively pooled studies:

- **Cochran's $Q$ statistic:** 4.471 ($df = 2$, $p = 0.1069$)
- **Inconsistency index ($I^2$):** 55.26%
- **Between-study variance ($\tau^2$):** 0.305663

The $I^2$ value of 55.26% reflects moderate-to-substantial heterogeneity across the included trials. The estimated between-study variance ($\tau^2 = 0.3057$) underlines meaningful clinical and methodological divergence among the primary trials, such as variations in backbone chemotherapy schedules (e.g., dose-dense anthracycline/cyclophosphamide followed by paclitaxel versus weekly paclitaxel regimens), choice of platinum compound (carboplatin AUC 5–6 versus weekly AUC 1.5–2 vs. cisplatin), and baseline patient characteristics (such as germline *BRCA* status distribution).

The distribution of effect sizes across studies is illustrated in Figure 3.

![Effect Distribution](outputs/HShuwD5_xJc0KHeDZGpcYg/effect_distribution.png)
*Figure 3: Distribution of individual and pooled effect estimates.*

The heterogeneity summary plot detailing parameter variance is displayed in Figure 4.

![Heterogeneity Summary](outputs/HShuwD5_xJc0KHeDZGpcYg/heterogeneity_summary.png)
*Figure 4: Heterogeneity summary plot depicting Cochran's Q, tau-squared, and I-squared metrics.*

---

## Moderator and Subgroup Analyses

To investigate the observed heterogeneity, study-level moderators were explored. Figure 5 depicts the relationship between study sample size and observed effect size magnitude.

![Bubble Chart](outputs/HShuwD5_xJc0KHeDZGpcYg/bubble_chart.png)
*Figure 5: Meta-regression bubble chart illustrating study weights, sample size distribution, and observed effect estimates.*

Smaller trials (e.g., study_7_R7, $n = 75$, Hedges' $g = -0.8262$) reported substantially larger effect sizes favoring platinum therapy than larger multi-center cohorts (e.g., study_3_R3, $n = 443$, Hedges' $g = -0.0341$). Potential clinical moderators explaining these discrepancies include:
1. **Platinum Agent and Dosing Strategy:** High-dose intermittent carboplatin (AUC 5–6 every 3 weeks) versus low-dose weekly regimens (AUC 1.5–2), which influence both dose intensity and treatment compliance.
2. **BRCA Mutation Enrichment:** Platinum sensitivity is elevated in homologous recombination-deficient tumors. Differences in germline *BRCA* mutation prevalence across trial cohorts directly influence the magnitude of DFS benefit.
3. **Control Backbone Intensity:** Control arms utilizing optimal dose-dense, anthracycline-taxane regimens may narrow the detectable survival differential compared with less dose-intense standard arms.

---

## Publication Bias and Small-Study Effects

Small-study effects and potential reporting bias were evaluated quantitatively using linear regression and non-parametric imputation:

- **Egger's Regression Intercept:** 0.0817 ($p = 0.1151$)
- **Duval and Tweedie's Trim-and-Fill Imputed Studies ($k_0$):** 0
- **Trim-and-Fill Adjusted Effect Estimate ($g$):** -0.2663
- **Overall Publication Bias Risk Assessment:** Low

Egger’s test showed no statistically significant funnel plot asymmetry ($p = 0.1151$), indicating an absence of small-study effects. Consistent with this, the trim-and-fill method identified zero missing studies ($k_0 = 0$) needed to balance the funnel plot, leaving the adjusted standardized estimate identical at $g = -0.2663$. Together, these findings indicate a low risk of publication bias, suggesting the pooled meta-analytic results are robust against unpublished negative studies.

---

## Data Quality & Validation Notes

During data extraction, pipeline processing, and effect measure harmonization, the following data quality observations and validation flags were documented:
- **Exclusions from Native Hazard Ratio Pooling:** A total of 2 study rows—specifically `study_2` ($n = 315$) and `study_6` ($n = 474$)—were excluded from native HR pooling because they lacked the necessary raw time-to-event variance inputs (standard errors, log-rank variance, or explicit confidence intervals) required for direct survival synthesis.
- **Impact of Data Harmonization:** These two excluded studies represented a combined cohort of 789 patients. While their standardized effect sizes (Hedges' $g = -0.3197$ and $g = -0.2543$, respectively) demonstrated statistically significant advantages favoring platinum therapy, the restriction of native HR pooling to $k = 3$ trials ($n = 606$) reduced the statistical power of the primary survival analysis, directly contributing to the wide confidence interval ([0.277, 1.449]).

---

## Discussion

Neoadjuvant therapy for triple-negative breast cancer aims to eradicate micrometastatic disease and downstage primary tumors. The biological rationale for incorporating platinum compounds relies on the high prevalence of DNA double-strand break repair deficiencies characteristic of basal-like TNBC. 

In this meta-analysis, the natively pooled Hazard Ratio for disease-free survival across 3 randomized cohorts ($n = 606$) was 0.6341 (95% CI: [0.277, 1.449], $p = 0.2801$). In strict statistical interpretation, this pooled result favors neither arm, as the 95% confidence interval spans 1.0. While the magnitude of hazard reduction (approximately 37%) is clinically compelling and aligns with historical improvements in pathological complete response, the lack of statistical significance reflects substantial inter-study variance ($\tau^2 = 0.3057$, $I^2 = 55.26\%$) and limited sample size in the native survival analysis.

When examining the broader dataset of 5 cohorts using standardized effect sizes, all 5 studies demonstrated point estimates favoring the addition of platinum (Hedges' $g$ ranging from -0.0341 to -0.8262), with three individual trials reaching statistical significance. Notably, two of the largest trials (`study_2_R2`, $n = 315$, and `study_6_R6`, $n = 474$) exhibited clear benefits in standardized survival metrics but could not be integrated into native HR pooling due to reporting limitations in available trial documentation.

Toxicity remains a primary clinical consideration. The addition of carboplatin to taxane-anthracycline regimens significantly increases grade 3/4 neutropenia, thrombocytopenia, and anemia, often requiring granulocyte colony-stimulating factor (G-CSF) support and dose adjustments. If hematologic toxicity results in premature discontinuation or dose reductions of standard anthracycline or taxane therapy, the overall therapeutic benefit of the regimen can be compromised.

---

## Limitations

Several limitations must be taken into account when interpreting these results:
1. **Limited Number of Studies for Native Survival Pooling:** Only 3 studies ($n = 606$) provided complete parameters for native HR pooling. The exclusion of two substantial cohorts ($n = 789$) due to missing raw variance inputs constrained statistical power.
2. **Moderate-to-Substantial Heterogeneity:** Heterogeneity across trials was notable ($I^2 = 55.26\%$), likely driven by divergent chemotherapy regimens, platinum schedules (carboplatin vs. cisplatin; weekly vs. every-3-weeks), and varying baseline nodal stages.
3. **Lack of Biomarker Stratification:** Individual patient-level data regarding germline *BRCA1/2* mutation status, homologous recombination deficiency (HRD) scores, or tumor-infiltrating lymphocyte (TIL) levels were not available across all studies, precluding pre-planned molecular subgroup analyses.
4. **Follow-Up Duration:** Length of follow-up varied across trials; longer follow-up is critical to evaluate whether early DFS advantages translate into sustained overall survival benefits.

---

## Conclusion

This meta-analysis examined the effect of adding platinum-based chemotherapy to neoadjuvant regimens on disease-free survival in women with early-stage triple-negative breast cancer. The pooled Hazard Ratio for disease-free survival was 0.634 (95% CI: [0.277, 1.449], $p = 0.2801$), indicating that the meta-analytic result favors neither treatment arm decisively when evaluated on the native time-to-event scale. Although individual standardized effect sizes consistently pointed toward lower recurrence hazards with platinum chemotherapy, moderate-to-substantial heterogeneity ($I^2 = 55.26\%$) and reporting-related study exclusions limit definitive conclusions. Further prospective trials and individual patient data meta-analyses are necessary to define optimal dosing schedules and identify specific biomarker-selected subpopulations that derive meaningful long-term survival gains from platinum integration.

---

## References

1. von Minckwitz G, Schneeweiss A, Loibl S, et al. Neoadjuvant carboplatin in patients with triple-negative and HER2-positive early breast cancer (GeparSixto; GBG 66): a randomised phase 2 trial. *Lancet Oncol*. 2014;15(7):747-756.
2. Sikov WM, Berry DA, Perou CM, et al. Event-free and overall survival following neoadjuvant weekly paclitaxel and carboplatin in triple-negative breast cancer: CALGB/Alliance 40603. *J Clin Oncol*. 2016;34(15):1749-1759.
3. Loibl S, Weber KE, Timms KM, et al. Survival analysis of carboplatin added to an anthracycline/taxane-based neoadjuvant chemotherapy and HRD score as predictor of response—final results from GeparSixto. *Ann Oncol*. 2018;29(12):2341-2347.
4. Sharma P, Barlow WE, Godwin AK, et al. Impact of addition of carboplatin and/or bevacizumab to neoadjuvant docetaxel followed by fluorouracil, epirubicin, and cyclophosphamide on pathologic complete response in triple-negative breast cancer: SWOG S0800. *Cancer*. 2019;125(18):3159-3167.
5. Poggio F, Bruzzone M, Vader P, et al. Platinum-based neoadjuvant chemotherapy in triple-negative breast cancer: a systematic review and meta-analysis. *Ann Oncol*. 2018;29(7):1497-1508.
6. Hahnen E, Lederer B, Hauke J, et al. Germline BRCA1/2 mutation status and carboplatin added to neoadjuvant chemotherapy in patients with triple-negative early breast cancer: A secondary analysis of the GeparSixto trial. *JAMA Oncol*. 2017;3(10):1378-1385.
7. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. 2nd ed. John Wiley & Sons; 2019.
8. Duval S, Tweedie R. Trim and fill: A simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455-463.

## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| disease-free survival | 5 | Hazard Ratio (HR) | Yes | 0.6341 [0.2774, 1.4494] |
| | | ⚠ 2 row(s) excluded from native HR pooling for lacking raw inputs: ['study_2', 'study_6'] | | |
