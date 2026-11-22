# Prophylactic Anticoagulant and Antiplatelet Therapy and the Risk of Adverse Events in Non-Hospitalised Adults with COVID-19: A Systematic Review and Random-Effects Meta-Analysis

## Abstract

**Background.** Thromboinflammation is a central feature of COVID-19, and prophylactic anticoagulant or antiplatelet therapy was widely trialled in non-hospitalised patients — both in the ambulatory (outpatient) setting and after discharge from hospital. Because these populations are at comparatively low absolute thrombotic risk, the safety profile of prophylaxis (principally bleeding, but also any treatment-emergent adverse event) is decisive for the risk–benefit balance. We therefore synthesised randomised evidence on the *proportion of participants experiencing at least one adverse event*.

**Methods.** We conducted a systematic review and random-effects meta-analysis of randomised controlled trials comparing prophylactic anticoagulant/antithrombotic therapy (low-molecular-weight heparin, rivaroxaban, apixaban, aspirin or similar) with placebo or no anticoagulant (standard care) in non-hospitalised adults with COVID-19. The outcome was the number of participants with at least one adverse event out of the number randomised in each arm, extracted according to a pre-specified preference hierarchy (any adverse event of any type → serious adverse events → bleeding events), with the definition recorded for each trial. Participants, not episodes, were counted; trials reporting only episode counts were excluded. Multi-arm trials were handled by combining all active anticoagulant arms into a single treatment group. Risk ratios (RR) were pooled on the native binary scale using restricted maximum likelihood (REML) with a random-effects model. Heterogeneity was quantified with Q, I² and τ²; small-study effects were examined with Egger's regression and trim-and-fill.

**Results.** Six studies met the inclusion criteria; five contributed a poolable participant-level adverse-event comparison (k = 5; N = 2,016 randomised participants). The pooled risk ratio was **RR = 1.196 (95% CI 0.887 to 1.612; p = 0.2399)**. By the pre-specified direction convention (RR < 1 favours anticoagulation), this point estimate lies on the harm side of unity but the confidence interval comfortably crosses 1; the result is classified as favouring **neither arm** — essentially a statistical tie, with the caveat that for a ratio measure the practical favourability depends on which adverse-event category each trial counted. Between-study heterogeneity was absent (Q = 3.506, df = 4, p = 0.477; I² = 0.0%; τ² = 0.0). Egger's regression showed no funnel asymmetry (intercept = −0.126, p = 0.7356) and trim-and-fill imputed a single potentially missing study (adjusted standardized estimate 0.2554); overall publication-bias risk was nonetheless graded **moderate**, driven by the small number of trials rather than by positive evidence of bias.

**Conclusions.** In non-hospitalised adults with COVID-19, prophylactic anticoagulant or antiplatelet therapy was not associated with a statistically significant change in the proportion of participants experiencing at least one adverse event. The pooled estimate is compatible with anything from an ~11% relative reduction to an ~61% relative increase in the risk of having at least one adverse event, so a clinically meaningful excess of adverse events — most plausibly bleeding — cannot be excluded. Given the low absolute event rates reported in these outpatient and post-discharge populations and the modest total sample size, the evidence is best described as imprecise rather than reassuring.

**Registration.** Not registered; this synthesis was conducted as a secondary analysis of a pre-specified extraction protocol.

## 1. Introduction

Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) infection provokes a well-characterised prothrombotic state. Endothelial injury, complement activation, neutrophil extracellular trap formation and marked elevations in D-dimer and fibrinogen combine to produce a coagulopathy that, in hospitalised patients, translates into high rates of venous and arterial thromboembolism. This observation drove rapid adoption of pharmacological thromboprophylaxis for inpatients, where several large randomised trials subsequently demonstrated benefit for therapeutic-intensity heparin in moderately ill, ward-level patients.

The non-hospitalised population is a different problem. Two distinct groups fall under this heading: (i) **ambulatory outpatients** with symptomatic but non-severe COVID-19 managed at home, and (ii) **post-discharge patients** in the weeks following an index hospitalisation, when thrombotic risk is thought to persist but is no longer counterbalanced by inpatient monitoring. In both groups the absolute incidence of thromboembolism is substantially lower than in ward or ICU populations — frequently well under 2% over 30–45 days. When absolute benefit is small, the numerator of harm becomes decisive: even a modest absolute excess of bleeding, or of nuisance adverse effects sufficient to cause treatment discontinuation, can erase any net advantage.

Most published syntheses of outpatient and post-discharge antithrombotic prophylaxis have concentrated on efficacy endpoints — death, hospitalisation, venous thromboembolism (VTE) — and have treated safety as a secondary, narratively summarised consideration. Where safety has been pooled, it has usually been restricted to *major bleeding*, an outcome so rare in these trials that the resulting confidence intervals are uninformative. A broader question has been comparatively neglected: **what proportion of participants experience at least one adverse event of any kind?** This is the quantity that most closely corresponds to the patient-facing burden of taking a prophylactic antithrombotic in the community, and it is the quantity synthesised here.

### 1.1 Objective

To estimate, in non-hospitalised adults with COVID-19, the effect of prophylactic anticoagulant or antiplatelet therapy compared with placebo or no anticoagulant (standard care) on the proportion of randomised participants experiencing at least one adverse event during follow-up.

### 1.2 Direction-of-effect convention

Throughout this report, **a risk ratio below 1 indicates that fewer participants experienced adverse events in the anticoagulant arm** (i.e. the result favours prophylaxis), and **a risk ratio above 1 indicates that more participants experienced adverse events in the anticoagulant arm** (i.e. harm). This convention is stated explicitly because, for ratio measures applied to heterogeneously defined adverse-event categories, the sign of the estimate alone does not unambiguously identify the favoured arm.

---

## 2. Methods

### 2.1 Eligibility criteria

**Population.** Non-hospitalised adults (≥18 years) with confirmed or clinically diagnosed COVID-19, comprising ambulatory outpatients and patients randomised at or after discharge from an index COVID-19 hospitalisation.

**Intervention.** Prophylactic-intensity anticoagulant or antiplatelet therapy, including low-molecular-weight heparin (e.g. enoxaparin), direct oral anticoagulants (rivaroxaban, apixaban), and antiplatelet agents (aspirin) or comparable agents.

**Comparator.** Placebo or no anticoagulant (standard care without antithrombotic prophylaxis).

**Outcome.** The number of participants with at least one adverse event, out of the number randomised in each arm, during the trial's defined follow-up period.

**Design.** Randomised controlled trials. Non-randomised studies, single-arm cohorts, modelling studies, narrative and systematic reviews, editorials and protocols without results were excluded.

### 2.2 Outcome extraction rules

Adverse-event reporting in COVID-19 trials is notoriously inconsistent, so a strict and pre-specified extraction hierarchy was applied:

1. **Any adverse event of any type** (the preferred definition);
2. if unavailable, **serious adverse events (SAEs)**;
3. if unavailable, **bleeding events** (major bleeding, clinically relevant non-major bleeding, or any bleeding).

The definition actually used was recorded for every trial so that the composition of the pooled estimate remains transparent. Additional rules:

- Where a trial reported several **non-overlapping** adverse-event categories and no broad total, only categories the paper *explicitly* defined as non-overlapping were summed. Categories of uncertain overlap were not summed, to avoid double-counting participants.
- **Participants were counted, not episodes.** Trials reporting only event (episode) counts were excluded from the pooled analysis, because a participant-level risk ratio cannot be recovered from episode counts.
- The **denominator was the number randomised (intention-to-treat)**. The safety population was used only when the randomised number was not reported, and such instances were flagged.
- **Efficacy outcomes were never repurposed as adverse-event counts.** Deaths, hospitalisations, venous thromboembolic events, symptom resolution and quality-of-life measures were excluded from the adverse-event numerator even when a trial tabulated them alongside safety data.
- In **multi-arm trials**, multiple anticoagulant doses or agents were combined into a single treatment group (summing both events and participants) and compared against the shared placebo/no-treatment arm, thereby avoiding unit-of-analysis error from reusing the control group.

### 2.3 Search and screening

A systematic search of the published randomised literature on antithrombotic prophylaxis in non-hospitalised COVID-19 was conducted, covering bibliographic databases and trial registries, supplemented by backward and forward citation chasing of eligible reports and of prior systematic reviews on the topic. Records were screened in two stages — title/abstract, then full text — against the criteria in §2.1. Reviews, duplicate publications and secondary reports of already-included trials were removed at the full-text stage; where a trial had generated more than one publication, a single primary report was designated as the data source to prevent double-counting of participants.

### 2.4 Effect size computation and synthesis

For each trial, the number of participants with at least one adverse event and the number randomised were extracted for both arms, and a **risk ratio (RR)** was computed on the native binary scale. Pooling was performed with a **random-effects model estimated by restricted maximum likelihood (REML)** on the log-RR scale, with back-transformation for reporting. The random-effects specification was chosen a priori because trials differed in agent, dose, duration, population (outpatient vs post-discharge) and, critically, in the adverse-event definition available.

For graphical display and for the small-study-effect diagnostics, study-level estimates were additionally expressed on a standardized (Hedges' *g*) metric; these standardized values are presented in §4 for comparability across the forest display, while **the pooled inferential result reported in §5 is a native risk-ratio pooling** (`native_pooling_used = true`; effect measure specified by explicit a priori request).

### 2.5 Heterogeneity, moderators and bias

Between-study heterogeneity was quantified using Cochran's Q, the I² statistic and the between-study variance τ². Pre-specified candidate moderators were drug class (heparin vs direct oral anticoagulant vs antiplatelet), setting (outpatient vs post-discharge), follow-up duration and adverse-event definition (any AE vs SAE vs bleeding). Small-study effects were assessed with Egger's regression test and Duval and Tweedie's trim-and-fill procedure. Cumulative meta-analysis ordered by sample size was used to inspect the stability of the pooled estimate as evidence accrued.

---

## 3. Search and Screening Results

Screening identified **six studies** meeting the population, intervention, comparator and design criteria. Of these, **five contributed a poolable participant-level adverse-event comparison** and were carried forward to quantitative synthesis (k = 5). One study met the clinical eligibility criteria but did not yield an extractable participant-level adverse-event numerator and denominator conforming to the rules in §2.2 — for example, reporting adverse events only as episode counts, or reporting only efficacy endpoints that the protocol forbids repurposing as adverse-event counts — and was therefore retained in the systematic review but excluded from the meta-analysis. This 6-versus-5 discrepancy is stated plainly here because it means the pooled estimate does not incorporate every eligible randomised trial identified.

The five pooled trials contributed a combined **2,016 randomised participants**.

---

## 4. Included Studies and Effect Sizes

Table 1 presents the five contributing comparisons with their standardized study-level estimates and 95% confidence intervals. Study identifiers correspond to the extraction records (`study_1_R1` … `study_5_R5`).

**Table 1. Study-level effect estimates (standardized metric, for display and diagnostics)**

| Record | Standardized estimate (Hedges' *g*) | 95% CI | N (randomised, both arms) |
|---|---|---|---|
| study_1_R1 | 0.2159 | −0.050 to 0.482 | 219 |
| study_2_R2 | 0.0136 | −0.171 to 0.199 | 449 |
| study_3_R3 | 0.6318 | 0.435 to 0.829 | 558 |
| study_4_R4 | −0.0576 | −0.238 to 0.123 | 472 |
| study_5_R5 | 0.1569 | −0.063 to 0.377 | 318 |
| **Total** | — | — | **2,016** |

Four of the five standardized estimates are positive (i.e. directionally consistent with more participants reporting at least one adverse event under prophylaxis), and one (`study_4_R4`) is marginally negative. Only one comparison, `study_3_R3` (g = 0.6318, 95% CI 0.435 to 0.829, N = 558), excludes the null in its own right; the remaining four individual confidence intervals all span zero. `study_3_R3` is also the largest contributing trial, so it carries substantial weight in the pooled result.

It should be emphasised that these standardized values are the display metric. The inferential synthesis reported below was conducted on the **native risk-ratio scale**, as pre-specified; the two metrics are monotonically related but not numerically interchangeable, and the standardized column should not be read as a risk ratio.

The distribution of study-level estimates is shown in `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`, and the relationship between estimate magnitude and study size (precision) in `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`.

---

## 5. Meta-Analytic Result

**Primary analysis (k = 5; N = 2,016 randomised participants).**

| Quantity | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** |
| Pooled effect | **1.196** |
| 95% confidence interval | **0.887 to 1.612** |
| p-value | **0.2399** |
| Model | Random effects, REML |
| Computation scale | RR (native) |
| Native pooling confirmed | Yes |
| Favours | **Neither arm** (essentially a tie; for a ratio measure, favourability also depends on which adverse-event category was counted) |

The **pooled risk ratio was 1.196 (95% CI 0.887 to 1.612, p = 0.2399)**. Under the direction convention of §1.2, the point estimate sits on the harm side of unity — corresponding to approximately a 20% relative increase in the probability that a given participant experiences at least one adverse event under prophylaxis — but the interval is wide and includes the null comfortably. Formally, the data are compatible with anything between an approximately **11.3% relative reduction** and an approximately **61.2% relative increase** in the proportion of participants with at least one adverse event. The direction field for this analysis is **"neither"**, and we report it as such: this is a null result, not a demonstration of harm and not a demonstration of safety.

The forest plot is provided at `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`. A cumulative meta-analysis (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`) shows the running pooled estimate as studies are added; the estimate does not exhibit the characteristic drift from a large early effect toward the null that would signal a first-published-exaggeration pattern, but with only five accumulation steps this inspection is qualitative rather than diagnostic.

Only a single meta-analytic group was defined for this question (one outcome construct, one timepoint stratum), so no separate subgroup pooling by outcome or timepoint was required; all five comparisons belong to the same synthesis.

---

## 6. Heterogeneity

Between-study heterogeneity was **absent**:

| Statistic | Value |
|---|---|
| Cochran's Q | **3.506** (df = 4) |
| p (Q) | **0.477** |
| I² | **0.0%** |
| τ² | **0.0** |

The Q statistic (3.506 on 4 degrees of freedom) is smaller than its degrees of freedom, so the I² estimate is truncated at **0.0%** and the REML estimate of between-study variance is **τ² = 0.0**. In practical terms, the observed dispersion of study-level estimates is entirely consistent with within-study sampling error alone; the random-effects model has therefore collapsed to a fixed-effect weighting, and the confidence interval reported in §5 reflects sampling variability rather than any additional between-study variance component.

This finding warrants two cautions. First, with k = 5, both Q and I² have low power to detect genuine moderate heterogeneity, and I² = 0% should not be over-interpreted as evidence of true clinical homogeneity. Second, and more substantively, the trials pooled here were *not* clinically homogeneous — they differ in agent class, in setting (outpatient vs post-discharge), and, most importantly, in which tier of the adverse-event hierarchy (§2.2) was available. Statistical homogeneity in the presence of definitional heterogeneity is better read as a sign that the available adverse-event counts were uniformly imprecise than as a sign that the underlying treatment effects are identical. A graphical summary of the heterogeneity diagnostics is available at `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`.

One notable tension deserves explicit mention: `study_3_R3` is the only comparison whose individual interval excludes the null, and its estimate (g = 0.6318) lies well above the others, yet the Q test does not flag significant inconsistency. With five studies and moderate within-study precision, Q simply lacks the power to resolve a single outlying estimate. Readers should treat the possibility that `study_3_R3` reflects a different underlying adverse-event definition or ascertainment intensity — rather than a different drug effect — as a live hypothesis that this dataset cannot adjudicate.

---

## 7. Moderators

Formal moderator analysis was **not performed**, and this is a deliberate decision rather than an omission. Two considerations preclude it:

1. **τ² = 0.0.** With no residual between-study variance to explain, meta-regression has no variance component on which to operate; any apparent moderator association would be fitted to sampling noise.
2. **k = 5.** Conventional guidance requires roughly ten studies per covariate for meta-regression. With five comparisons, even a single-covariate model would be severely overfitted and its coefficient uninterpretable.

The pre-specified candidate moderators — drug class (LMWH vs DOAC vs antiplatelet), clinical setting (ambulatory outpatient vs post-discharge), follow-up duration, and the tier of adverse-event definition used — therefore remain unexamined quantitatively. Of these, the **adverse-event definition** is the most consequential unexplored source of variation, since a trial reporting "any adverse event of any type" will generate a far higher event rate, and a correspondingly different risk ratio, than a trial reporting only major bleeding. The bubble chart (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) displays effect magnitude against study size and can be inspected informally, but it should not be read as a fitted meta-regression.

We state plainly: **no moderator effect is established or excluded by this analysis.**

---

## 8. Publication Bias

| Diagnostic | Value |
|---|---|
| Egger's regression intercept | **−0.126** |
| Egger's test p-value | **0.7356** |
| Trim-and-fill: studies imputed (k₀) | **1** |
| Trim-and-fill adjusted estimate (standardized scale) | **0.2554** |
| Overall risk rating | **Moderate** |

Egger's regression showed **no statistically significant funnel-plot asymmetry** (intercept = −0.126, p = 0.7356). The intercept is small and negative, the opposite sign to what classic small-study publication bias in favour of the intervention would produce. Trim-and-fill imputed only **one** potentially missing study, yielding an adjusted standardized estimate of 0.2554 — a minor perturbation that does not change the qualitative conclusion.

Taken together, these statistics provide **no positive evidence of publication bias**, and it is unlikely that small-study effects have materially distorted the pooled risk ratio. The overall risk was nonetheless graded **moderate**, and that rating should be understood as reflecting factors beyond the two test statistics: principally the **small number of included studies (k = 5), which leaves Egger's test substantially underpowered**, together with residual uncertainty about coverage of unregistered or unpublished trials and of the grey literature. Egger's test with five studies has very low power; a non-significant result is weak evidence of symmetry, not a clearance.

A further, field-specific consideration applies to adverse-event outcomes: publication and reporting bias in safety data typically operates not through suppression of whole trials but through **selective non-reporting of safety tables within published trials**. The exclusion of one otherwise-eligible study for lack of an extractable participant-level adverse-event count (§3) is a concrete instance of exactly this mechanism, and it is not detectable by funnel-plot methods. The pooled result should accordingly be read with appropriate caution.

---

## 9. Discussion

This synthesis of five randomised comparisons in 2,016 non-hospitalised adults with COVID-19 found **no statistically significant difference** in the proportion of participants experiencing at least one adverse event between prophylactic anticoagulant/antiplatelet therapy and placebo or standard care (RR = 1.196, 95% CI 0.887 to 1.612, p = 0.2399), with no detectable between-study heterogeneity (I² = 0.0%, τ² = 0.0, Q = 3.506, p = 0.477).

Three features of this result deserve emphasis.

**First, the result is null, not reassuring.** The confidence interval extends to 1.612. An upper bound of that magnitude means a 60% relative increase in the proportion of participants with at least one adverse event remains entirely consistent with the data. In a population where the absolute efficacy benefit of prophylaxis is itself small — outpatient trials have generally reported low and often statistically indistinguishable rates of thromboembolism, hospitalisation and death — a harm of that size would be decision-relevant. Describing this finding as "no safety signal" would overstate what an interval of 0.887–1.612 can support. The correct characterisation is **imprecision**.

**Second, the point estimate's direction is consistently, if weakly, towards more adverse events with prophylaxis.** Four of five standardized study-level estimates are positive, and the pooled RR of 1.196 sits above unity. Mechanistically this is unsurprising: anticoagulants and antiplatelet agents predictably increase bleeding, including the clinically relevant non-major and minor bleeding that dominates adverse-event tallies in ambulatory populations, and injectable LMWH additionally generates local injection-site reactions. The direction field for the pooled analysis is nonetheless **"neither"**, because the interval straddles the null and because, for a ratio of heterogeneously defined adverse-event categories, the arm that is "favoured" cannot be read off the sign alone. We report it that way rather than inflating a non-significant trend into a harm signal.

**Third, the composite nature of the outcome cuts both ways.** Pooling "at least one adverse event" across trials that operationalised it as any-AE, as SAEs, or as bleeding-only produces a measure of mixed clinical gravity. A trial counting any adverse event will capture nuisance events with high frequency and low severity; a trial counting only major bleeding will capture rare, severe events. Aggregating these tiers improves statistical power at the cost of interpretive clarity, and the pooled RR of 1.196 should be understood as an average across these definitions rather than as a risk ratio for any one of them. The pre-specified hierarchy (§2.2) makes this composition auditable, but it does not dissolve the problem.

**Relation to existing evidence.** The pattern observed here — a point estimate modestly favouring the control arm on safety, with wide intervals and no heterogeneity — is consistent with the broad picture emerging from the outpatient and post-discharge COVID-19 antithrombotic literature, in which efficacy benefits have been difficult to demonstrate against a low baseline event rate while bleeding has increased in a dose- and agent-dependent fashion. Our contribution is to apply a transparent, participant-counted, ITT-denominator extraction rule to the *adverse-event* endpoint specifically, rather than to major bleeding alone, and to report the resulting estimate on its native ratio scale.

**Clinical implications.** These data do not support routine prophylactic anticoagulation or antiplatelet therapy for unselected non-hospitalised adults with COVID-19 on safety grounds, and they do not exclude a clinically important excess of adverse events. Decisions in individual patients at elevated thrombotic risk — for example, recently discharged patients with additional VTE risk factors — should continue to rest on individualised risk assessment, informed by the fact that the safety evidence base in this setting is small and imprecise.

---

## 10. Data Quality and Validation Notes

No automated validation flags were raised for this dataset. However, three data-quality matters established in the course of the analysis should be recorded explicitly rather than left to inference:

- **One of six eligible studies was excluded from the quantitative synthesis.** Six studies met the clinical eligibility criteria but only five yielded a participant-level adverse-event numerator and ITT denominator conforming to the extraction rules; the pooled estimate (k = 5) therefore rests on five of six eligible trials.
- **Reviews, duplicate publications and secondary reports were removed at full text**, and where a trial generated multiple publications a single primary report was designated as the data source. This step prevents double-counting of participants but means that supplementary safety data published in companion papers may not be reflected.
- **The display metric and the inferential metric differ.** Study-level estimates in Table 1 are standardized (Hedges' *g*) values used for the forest display, the distribution plot and the small-study-effect diagnostics (including the trim-and-fill adjusted value of 0.2554). The pooled inferential result in §5 is a **native risk-ratio pooling** on the RR scale, with native pooling confirmed. The two should not be compared numerically.

No instances required substitution of a safety population for the randomised denominator in the pooled comparisons; had any occurred, they would have been flagged here.

---

## 11. Limitations

1. **Very small evidence base.** Five pooled comparisons and 2,016 participants provide limited power for a binary outcome with low event rates. The width of the confidence interval (0.887–1.612) is the dominant limitation of this review.
2. **One eligible trial could not be pooled**, because its adverse-event reporting did not permit participant-level extraction. Its exclusion is itself a form of outcome-reporting bias that the funnel-based diagnostics cannot detect.
3. **Heterogeneous outcome definitions.** The pre-specified hierarchy (any AE → SAE → bleeding) means the pooled estimate aggregates adverse-event categories of differing frequency and severity. The statistical homogeneity observed (I² = 0.0%) does not imply definitional homogeneity.
4. **Heterogeneity statistics are underpowered.** With k = 5, Q and I² have low sensitivity; I² = 0.0% should not be taken as confirmation that true effects are identical, and the apparently outlying `study_3_R3` cannot be formally adjudicated.
5. **No moderator analysis was possible.** With τ² = 0.0 and k = 5, meta-regression on drug class, setting, follow-up duration or adverse-event definition was not defensible. Consequently the review cannot say whether safety differs between LMWH, DOACs and aspirin, or between outpatient and post-discharge populations — questions of direct clinical importance.
6. **Publication-bias assessment is weak.** Egger's test (p = 0.7356) is non-significant but underpowered at k = 5; trim-and-fill imputed one study. The overall risk rating remains **moderate**, reflecting these limitations rather than positive evidence of bias.
7. **Risk-of-bias at study level was not formally pooled or incorporated as a covariate.** Trials in this literature differ materially in blinding (several open-label, standard-care-controlled designs), which plausibly affects adverse-event ascertainment: unblinded participants and investigators may report nuisance events differentially. This is a credible source of bias in the direction of the observed point estimate.
8. **Multi-arm pooling.** Combining multiple anticoagulant doses/agents into a single treatment arm avoids unit-of-analysis error but assumes a common safety effect across doses, which is biologically implausible for anticoagulants and may dilute dose-dependent bleeding signals.
9. **No absolute risk estimates.** Because baseline adverse-event rates varied with the definition applied, no pooled absolute risk difference or number-needed-to-harm is reported; the relative measure alone cannot convey absolute burden.

---

## 12. Conclusion

Across five randomised comparisons in 2,016 non-hospitalised adults with COVID-19, prophylactic anticoagulant or antiplatelet therapy was **not** associated with a statistically significant change in the proportion of participants experiencing at least one adverse event compared with placebo or standard care: **pooled Risk Ratio 1.196 (95% CI 0.887 to 1.612; p = 0.2399; REML random-effects; I² = 0.0%, τ² = 0.0, Q = 3.506, p = 0.477)**. The result favours **neither arm**. Egger's test showed no funnel asymmetry (p = 0.7356) and trim-and-fill imputed a single study, but with only five trials the publication-bias assessment remains underpowered and overall bias risk is graded moderate.

The honest reading is that the point estimate drifts modestly towards more adverse events with prophylaxis — consistent with the expected bleeding liability of these agents — while the interval remains too wide to establish or exclude a clinically important excess. Combined with the low absolute thrombotic event rates characteristic of ambulatory and post-discharge COVID-19 populations, this imprecision argues against routine prophylaxis for unselected non-hospitalised patients and in favour of individualised risk assessment. Future trials and, crucially, future trial *reports* should publish participant-level counts for a standardised, clearly defined adverse-event endpoint — including minor and clinically relevant non-major bleeding — so that the safety side of the risk–benefit equation can be quantified with the same rigour routinely applied to efficacy.

---

## 13. Figures

| Figure | Path |
|---|---|
| Forest plot (study-level and pooled estimates) | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Cumulative meta-analysis | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Distribution of effect estimates | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Bubble chart (effect vs. study size) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Heterogeneity diagnostics summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 14. References

Methodological references underpinning the synthesis:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023. (Chapters 10 and 19, on meta-analysis and adverse effects.)
3. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1–48.
4. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Controlled Clinical Trials*. 1986;7(3):177–188.
5. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
6. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
7. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
8. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002.
9. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.
10. Zorzela L, Loke YK, Ioannidis JP, et al. PRISMA harms checklist: improving harms reporting in systematic reviews. *BMJ*. 2016;352:i157.

Clinical and contextual references on COVID-19 thromboprophylaxis:

11. Connors JM, Levy JH. COVID-19 and its implications for thrombosis and anticoagulation. *Blood*. 2020;135(23):2033–2040.
12. Klok FA, Kruip MJHA, van der Meer NJM, et al. Incidence of thrombotic complications in critically ill ICU patients with COVID-19. *Thrombosis Research*. 2020;191:145–147.
13. Cuker A, Tseng EK, Nieuwlaat R, et al. American Society of Hematology living guidelines on the use of anticoagulation for thromboprophylaxis in patients with COVID-19. *Blood Advances*. 2021/2022 (living update series).
14. Barnes GD, Burnett A, Allen A, et al. Thromboembolism and anticoagulant therapy during the COVID-19 pandemic: interim clinical guidance from the Anticoagulation Forum. *Journal of Thrombosis and Thrombolysis*. 2020;50(1):72–81.
15. Spyropoulos AC, Levy JH, Ageno W, et al. Scientific and Standardization Committee communication: clinical guidance on the diagnosis, prevention, and treatment of venous thromboembolism in hospitalized patients with COVID-19. *Journal of Thrombosis and Haemostasis*. 2020;18(8):1859–1865.

*Note on study-level citations:* the five pooled comparisons are identified in this report by their extraction record identifiers (`study_1_R1`–`study_5_R5`) in accordance with the de-identified analytic dataset supplied for synthesis; bibliographic details for each contributing trial are held in the accompanying extraction table.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| adverse events | 5 | Risk Ratio (RR) | Yes | 1.1959 [0.8874, 1.6115] |
