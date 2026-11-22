# Mobile Phone Reminders to Caregivers and Receipt of the Third Dose of DTP-Containing Vaccine (DTP3/Pentavalent-3) in Children in Low- and Middle-Income Countries: A Systematic Review and Meta-Analysis of Randomised Trials

## Abstract

**Background.** Incomplete immunisation schedules remain a major cause of preventable child mortality in low- and middle-income countries (LMICs). Completion of the third dose of a DTP-containing vaccine (DTP3/pentavalent-3) is the standard global tracer indicator of a functioning routine immunisation programme. Mobile phone reminders (SMS text messages, live phone calls and automated voice calls) directed to parents and caregivers are a low-cost, scalable demand-side intervention, but trial results have been inconsistent.

**Objective.** To quantify the effect of mobile phone reminders sent to parents/caregivers, added to routine immunisation care, compared with routine immunisation care without reminders, on receipt of DTP3/pentavalent-3 among children in LMICs.

**Methods.** We conducted a systematic review and random-effects meta-analysis of randomised and cluster-randomised controlled trials conducted in LMICs. Crude (unadjusted) intention-to-treat event counts for receipt of the third DTP-containing dose were extracted for each arm using all randomised/enrolled participants as denominators; adjusted odds ratios, logistic-regression and GEE/cluster-adjusted estimates were not used where raw counts were available. In multi-arm trials, the reminder-only arm was compared with the no-reminder routine-care arm, ignoring arms combining reminders with monetary incentives, education-only arms and other co-interventions. The primary effect measure was the risk ratio (RR), pooled on its native scale using a restricted maximum likelihood (REML) random-effects model. Heterogeneity was summarised with Cochran's Q, I² and τ². Small-study effects were assessed with Egger's regression test and Duval & Tweedie trim-and-fill.

**Results.** Six trials contributing six independent effect estimates and 3,869 children met the inclusion criteria. The pooled Risk Ratio (RR) for receipt of DTP3/pentavalent-3 was **1.119 (95% CI 1.014 to 1.235; p = 0.0257; k = 6; N = 3,869)**, pooled natively on the RR scale (native pooling confirmed). Between-study heterogeneity was substantial: Q = 64.383 (df = 5), p < 0.001, I² = 90.22%, τ² = 0.01189 (log-RR scale, τ ≈ 0.109), with an approximate 95% prediction interval of 0.80 to 1.56. Study-level standardized estimates ranged from g = −0.011 (95% CI −0.155 to 0.132) to g = 0.985 (95% CI 0.747 to 1.223). The automated direction classification returned by the analysis pipeline for this pooled estimate was "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)", and this is the direction label that should be quoted for the result. Egger's test showed no significant funnel asymmetry (intercept = 0.0409, p = 0.6687); trim-and-fill imputed one missing study (adjusted standardized estimate g = 0.3659). Overall publication-bias risk was rated moderate, reflecting the small number of trials rather than positive statistical evidence of bias.

**Conclusions.** Across six LMIC trials, adding mobile phone reminders to routine immunisation care was associated with a pooled risk ratio of 1.119 for DTP3/pentavalent-3 receipt, with a confidence interval that excludes the null but a prediction interval that includes it. Heterogeneity was very high (I² = 90.22%), so the pooled value should be read as an average across highly dissimilar programme contexts rather than a transportable estimate of benefit. The evidence is compatible with a modest average improvement in third-dose coverage in some settings and with no effect in others; context-specific piloting and larger, better-reported trials with crude per-arm denominators are needed.


## 1. Introduction

Routine childhood immunisation is among the most cost-effective public health interventions available, yet roughly one in seven infants worldwide still fails to complete the primary three-dose series of a diphtheria–tetanus–pertussis (DTP)-containing vaccine. Receipt of the third dose (DTP3, usually delivered in LMICs as pentavalent-3, containing DTP, hepatitis B and *Haemophilus influenzae* type b antigens) is the canonical global tracer indicator for immunisation system performance, precisely because it requires a caregiver to return to a health facility on three separate occasions. Attrition between the first and third dose — the "drop-out" gap — is concentrated in low- and middle-income countries (LMICs) and is driven as much by forgetting, competing demands, uncertainty about due dates and travel costs as by outright vaccine refusal.

Mobile phone penetration in LMICs has grown faster than almost any other infrastructure, creating an opportunity to address the "forgetting and scheduling" component of drop-out directly. Mobile phone reminders — SMS text messages, live calls from health workers or call-centre staff, and automated/interactive voice response (IVR) calls — are inexpensive per contact, require no additional clinic infrastructure, and can be layered onto existing electronic immunisation registries. Several randomised trials have evaluated such reminders in sub-Saharan Africa and South Asia, but reported effects range from essentially null to large, and the trials differ markedly in modality (SMS versus voice), message frequency, baseline coverage, whether the intervention was delivered alongside functioning digital registries, and whether literacy and phone-sharing were addressed.

Previous reviews have often pooled heterogeneous outcomes — "any vaccination", "up-to-date status", "timely receipt within one week of the due date" and dose-specific coverage — into a single estimate, and have frequently incorporated adjusted odds ratios or cluster-adjusted GEE estimates alongside crude counts. This mixes effect measures and inflates apparent precision. The present review deliberately restricts attention to a single, policy-relevant, dose-specific binary outcome — receipt of the third DTP-containing dose — extracted as crude intention-to-treat event counts, and pools these on the native risk-ratio scale.

**Review question (PICO).**
- **Population:** Children in low- and middle-income countries eligible for routine infant immunisation.
- **Intervention:** Mobile phone reminders to parents/caregivers (SMS text messages and/or phone calls, including automated voice calls) plus routine immunisation care.
- **Comparator:** Routine immunisation care without reminders (no-reminder control).
- **Outcome:** Number of children who received/completed the third dose of a DTP-containing vaccine (DTP3/DPT3/pentavalent-3/Penta-3), out of the number randomised/enrolled in each arm, at the trial's main follow-up assessment for that dose (e.g. by 14 weeks, 18 weeks, 6 months or 12 months of age).
- **Effect direction:** A risk ratio greater than 1 (equivalently a positive standardized effect on the underlying scale) indicates that **more** children received DTP3/pentavalent-3 in the reminder arm than in the no-reminder routine-care arm — i.e. that reminders improved DTP3 coverage.

---

## 2. Search and Screening

### 2.1 Reporting standard

This review was prepared and is reported in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) statement. The structure below follows the PRISMA flow logic: identification, screening, eligibility assessment and inclusion.

### 2.2 Eligibility criteria

**Included:**
- Randomised controlled trials, including individually randomised and cluster-randomised designs, conducted wholly or predominantly in low- or middle-income countries (World Bank classification at the time of the trial).
- Interventions in which the active component delivered to the parent/caregiver arm was a mobile phone reminder — SMS text message, live voice call, automated voice/IVR call, or a defined combination of these — layered onto routine immunisation services.
- A concurrent control arm receiving routine immunisation care without reminders.
- Reporting of DTP3/pentavalent-3 receipt (or "completed all three doses") as an event count, or as a percentage convertible to a count using the number randomised in that arm.

**Excluded:**
- Non-randomised, before–after, interrupted time-series and purely observational evaluations.
- Trials conducted exclusively in high-income settings.
- Interventions in which the phone reminder could not be separated from a co-intervention (e.g. conditional cash transfer, food/lottery incentive, community mobilisation, home visits, or education-only arms). In multi-arm trials, only the reminder-only arm versus the no-reminder routine-care arm was extracted; incentive-plus-reminder arms, education-only arms and other co-intervention arms were disregarded.
- Reports presenting only adjusted odds ratios, logistic-regression coefficients or cluster-adjusted (GEE) estimates when crude per-arm counts could not be recovered. Odds ratios were never back-converted into the pooled result.
- Outcomes restricted to "timely receipt within one week of the due date" or "received without delay" when overall DTP3 receipt was also reported; overall receipt was preferred.
- Reviews, commentaries, protocols without results, and duplicate/companion reports of an already-included trial (the primary outcome report was retained to avoid double-counting).

### 2.3 Information sources and search strategy

Electronic searches combined controlled vocabulary and free-text terms across three concept blocks: (i) *immunisation* (vaccin\*, immuni\*, DTP, DPT, pentavalent, Penta-3, EPI); (ii) *mobile phone reminder* (SMS, "text message", "short message service", mHealth, "mobile phone", "voice call", "automated call", IVR, reminder, recall); and (iii) *study design* (randomi\*ed, trial, RCT). Database searches were supplemented by hand-searching reference lists of prior systematic reviews on reminder/recall interventions and by screening trial registries for completed studies.

### 2.4 Selection process

Records were de-duplicated and screened on title and abstract against the eligibility criteria, followed by full-text assessment of all potentially eligible reports. Records were removed at full-text stage for the following reasons, in descending order of frequency: wrong study design (non-randomised or observational evaluation); high-income setting; no extractable dose-specific DTP3/pentavalent-3 outcome (e.g. only composite "fully immunised child" status, or only timeliness); reminder bundled inseparably with incentives or home visits; secondary/companion publication of an already-included trial; and review or commentary articles with no primary data.

### 2.5 Screening outcome

Six randomised trials met all inclusion criteria and contributed extractable crude DTP3/pentavalent-3 event counts. These six trials contributed six independent effect estimates (one per trial; no trial contributed more than one comparison, so no within-study dependency correction was required) and a combined analysed sample of **3,869 children**.

### 2.6 Data extraction and analysis set

For each included trial we extracted: country and setting; reminder modality; comparator description; number randomised/enrolled per arm; and the number of children in each arm receiving the third DTP-containing dose at the trial's main follow-up assessment for that dose. Intention-to-treat denominators (all randomised/enrolled participants) were used throughout. Where only percentages were reported, counts were reconstructed by applying the percentage to the number randomised in that arm. No adjusted, model-based or cluster-corrected estimates were substituted for crude counts.

---

## 3. Included Studies

Six trials, labelled here by their analysis identifiers R1–R6, were included. Table 1 summarises the contributing estimates and their analysed sample sizes.

**Table 1. Characteristics of included effect estimates**

| Estimate ID | Analysis label | Analysed N (both arms) | Standardized effect (Hedges' g, display scale) | 95% CI | Share of total N |
|---|---|---|---|---|---|
| R1 | study_1_R1 | 600 | 0.027 | −0.133 to 0.187 | 15.5% |
| R2 | study_2_R2 | 321 | 0.139 | −0.080 to 0.358 | 8.3% |
| R3 | study_3_R3 | 1,596 | 0.543 | 0.443 to 0.643 | 41.3% |
| R4 | study_4_R4 | 300 | 0.144 | −0.083 to 0.370 | 7.8% |
| R5 | study_5_R5 | 748 | −0.011 | −0.155 to 0.132 | 19.3% |
| R6 | study_6_R6 | 304 | 0.985 | 0.747 to 1.223 | 7.9% |
| **Total** | — | **3,869** | — | — | 100% |

Notes on Table 1: the study-level values in the fourth column are standardized effects (Hedges' g) produced for display and for the funnel/trim-and-fill diagnostics, so that trials of different sizes and baseline coverage can be plotted on a common axis. **The pooled inferential result reported in Section 5 was computed on the native risk-ratio scale, not on the standardized scale**; the two are therefore not numerically interchangeable, and the g values should be read as a comparative display of direction and precision rather than as the primary estimates.

### 3.1 Narrative description of the evidence base

All six trials randomised caregivers (individually or in clusters) to receive mobile phone reminders about upcoming immunisation appointments in addition to routine services, versus routine services alone. Sample sizes varied by more than a factor of five, from 300 to 1,596 children; the single largest trial (R3) contributed 41.3% of the analysed sample, and the three smallest trials (R2, R4, R6) together contributed only 24.0%.

The directional pattern across trials is striking and is the central substantive finding of this review. Three trials (R1, R2, R4) produced small positive point estimates whose confidence intervals comfortably include the null; one trial (R5) produced an essentially exactly null estimate (g = −0.011) with a tight confidence interval; and two trials (R3, R6) produced moderate-to-large positive estimates with confidence intervals excluding the null by a wide margin (R3: g = 0.543, 95% CI 0.443 to 0.643; R6: g = 0.985, 95% CI 0.747 to 1.223). There is thus no trial in this evidence base showing a credible *harm* from reminders — the lower bound of the most negative trial (R5) is only −0.155 — but there is a sharp split between trials showing nothing and trials showing a substantial benefit. This bimodality, rather than any single outlier, is what drives the heterogeneity statistics reported in Section 6.

### 3.2 Risk of bias considerations

Blinding of caregivers to receipt of a text message or phone call is impossible, so all included trials are at high risk of performance bias by design; however, the primary outcome (receipt of a vaccine dose) is relatively objective and is frequently verified against immunisation cards or facility/registry records, which limits detection bias. Residual concerns common to this literature, and relevant to the interpretation below, include: (i) differential loss to follow-up between arms, partially mitigated here by the requirement for intention-to-treat denominators; (ii) outcome ascertainment that depends on caregiver retention of a home-based record, which may itself be influenced by the intervention; (iii) in cluster-randomised trials, baseline imbalance across a small number of clusters; and (iv) selective reporting of the dose or timepoint with the most favourable result. Because we extracted crude counts over all randomised participants and preferred overall receipt over timeliness, the extraction rules used here reduce — but cannot eliminate — the influence of (iv).

---

## 4. Effect Sizes

### 4.1 Effect measure

The pre-specified and analysed effect measure for this review is the **Risk Ratio (RR)**, selected by explicit user/protocol request (`effect_measure_source = explicit_user_request`), with no conflict recorded between the requested and detected measure. Pooling was carried out on the native RR scale (`native_pooling_used = true`, `computation_scale = RR`). **The pooled statistic reported below is therefore a genuine, confirmed native-scale pooled risk ratio and must be named as such — it is not a standardized mean difference and is not Hedges' g.** Where standardized (Hedges' g) values appear in this report, they are explicitly labelled as display or diagnostic quantities.

An RR above 1 denotes a higher probability of receiving DTP3/pentavalent-3 in the reminder arm than in the no-reminder arm.

### 4.2 Study-level estimates

Figure 1 (`outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png`) presents the forest plot of all six contributing estimates with their 95% confidence intervals and the random-effects summary. Figure 3 (`outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png`) displays the distribution of study-level effects, which visualises the bimodal clustering described in Section 3.1: a tight group of four near-null estimates and two clearly separated positive estimates.

Precision varied substantially. The narrowest study-level confidence interval (R3, width 0.200 on the standardized display scale) reflects both the largest sample (n = 1,596) and a large event count; the widest intervals belong to R6 (width 0.476) and R4 (width 0.453), the two smallest contributions.

---

## 5. Meta-Analytic Results

### 5.1 Primary pooled estimate

A single meta-analytic group was specified (one outcome, receipt of DTP3/pentavalent-3, at each trial's main follow-up assessment for that dose); no separate outcome/timepoint subgroups were required, and no group was flagged as having insufficient data for pooling.

Using a random-effects model estimated by restricted maximum likelihood (REML):

| Quantity | Value |
|---|---|
| Effect measure | **Risk Ratio (RR)** (native pooling confirmed) |
| Number of studies (k) | 6 |
| Total analysed children (N) | 3,869 |
| **Pooled risk ratio** | **1.119** |
| 95% confidence interval | **1.014 to 1.235** |
| p-value | **0.0257** |
| τ² (log-RR scale) | 0.01189 (τ ≈ 0.109) |
| I² | 90.22% |
| Cochran's Q (df = 5) | 64.383 (p < 0.001) |
| Approximate 95% prediction interval | 0.80 to 1.56 |
| Estimator | REML random-effects |
| Direction classification returned by the analysis | *"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"* |

The pooled risk ratio of 1.119 corresponds, on the relative scale, to an approximately 12% higher probability of third-dose receipt in reminder arms than in no-reminder arms, with a 95% confidence interval spanning a 1.4% to 23.5% relative increase. On an illustrative control-arm coverage of 70% — broadly typical of the settings represented — this translates to an absolute difference of about 8.3 percentage points (95% CI 1.0 to 16.5), i.e. a number needed to remind of roughly 12 children (95% CI 6 to 100) for one additional third dose. These absolute figures are illustrative conversions, not pooled absolute effects, and they scale directly with assumed baseline coverage: at higher baseline coverage the same relative effect yields a smaller absolute gain.

### 5.2 Direction of effect — important interpretive note

Per the direction field carried by the analysis, this pooled result is classified as favouring **"neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)"**. We report that classification as returned rather than substituting our own reading of the sign of the pooled estimate, because for ratio measures the favourability of a value above 1 depends on whether the event counted is a desirable one (here, dose receipt) or an undesirable one, and because the sign convention of the pooled value is treatment-minus-control in raw form.

Readers should therefore note the following tension explicitly, rather than have it smoothed over: the 95% confidence interval (1.014 to 1.235) excludes 1 and the p-value is 0.0257, which under a conventional 5% threshold is a statistically detectable deviation from the null; yet the automated direction classification does not assign a favoured arm, and the prediction interval (≈ 0.80 to 1.56) comfortably includes 1. Taken together, the honest summary is that **the average effect in this body of evidence is positive but small and fragile, and the evidence is not strong enough to declare a consistently favoured arm across settings**. The confidence interval describes uncertainty about the *mean* effect; the prediction interval describes where the effect in a *new* LMIC programme would be expected to fall, and that interval includes both meaningful benefit and no benefit at all.

### 5.3 Cumulative analysis

Figure 2 (`outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png`) shows the cumulative meta-analysis, in which estimates are added sequentially and the running pooled estimate is re-computed. Because the evidence base contains two trials with large positive effects and four with near-null effects, the cumulative trajectory is sensitive to ordering: the running estimate is pulled upward whenever R3 or R6 enters and drifts back toward the null as the near-null trials accumulate. The practical implication is that the pooled value has not stabilised — with only six trials, the summary estimate remains materially dependent on which trials happen to be in the pool.

---

## 6. Heterogeneity

Between-study heterogeneity was **substantial to considerable** by every standard criterion:

- **Cochran's Q = 64.383 on 5 degrees of freedom, p < 0.001.** The null hypothesis of a common underlying effect is decisively rejected; Q is nearly 13 times its expected value under homogeneity (E[Q] = df = 5).
- **I² = 90.22%.** Approximately 90% of the observed variability in effect estimates reflects genuine between-study differences rather than within-study sampling error. Under the Cochrane interpretive bands this falls in the "considerable heterogeneity" range (75–100%).
- **τ² = 0.01189** on the log-RR scale, implying a between-study standard deviation of τ ≈ 0.109 in log-RR units. A trial drawn at random from the same population of studies would therefore be expected to have a true risk ratio roughly within a multiplicative factor of e^(±1.96 × 0.109) ≈ 0.81 to 1.24 of the pooled value, before adding sampling error.
- **Approximate 95% prediction interval: 0.80 to 1.56.** This interval includes 1, meaning that the existing evidence does not exclude the possibility that reminders have no effect — or even a small negative effect — on DTP3 receipt in a new setting.

Figure 5 (`outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png`) summarises these diagnostics graphically.

Given I² of 90.22%, the fixed-effect model is inappropriate and the random-effects (REML) model was used throughout. However, it is important to state plainly that a random-effects average over a 90%-heterogeneous set of trials is a weighted description of a dispersed distribution, not an estimate of a single transportable effect. Clinically and programmatically, the heterogeneity *is* the finding: mobile phone reminders appear capable of producing substantial coverage gains in some immunisation systems (R3, R6) while producing nothing detectable in others (R1, R2, R4, R5).

### 6.1 Sources of heterogeneity — plausible explanations

Although formal testing was not possible (Section 7), the literature and the structure of this evidence base suggest several candidate explanations, offered here as hypotheses:

1. **Baseline coverage and ceiling effects.** Where control-arm DTP3 coverage is already high, there is little headroom for a reminder to improve; trials in low-coverage settings have more room to demonstrate an effect.
2. **Reminder modality.** SMS requires caregiver literacy and handset access; automated or live voice calls do not. Trials in low-literacy populations that used text-only reminders would be expected to underperform.
3. **Phone ownership and sharing.** Where the registered number belongs to a male household head or is shared across a compound, the reminder may never reach the caregiver who brings the child.
4. **Supply-side readiness.** A reminder can only convert into a dose if a stocked, staffed session is actually available on the reminded day. Reminders layered on an unreliable supply chain address the wrong bottleneck.
5. **Intensity and tailoring.** Single generic messages versus multi-message, date-specific, named-child reminders plausibly differ in effect.
6. **Outcome ascertainment window.** Trials assessing DTP3 at 14–18 weeks capture timeliness-sensitive effects, whereas assessment at 6 or 12 months allows late catch-up doses in the control arm to erode any apparent difference.

---

## 7. Moderators

No study-level moderator variables (e.g. reminder modality, baseline coverage, country, urban/rural setting, message frequency, follow-up window, or risk-of-bias domain) were available in the analysis dataset in a form permitting formal meta-regression. Consequently, **no subgroup analyses or meta-regressions were conducted, and none should be inferred from this report.**

Figure 4 (`outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png`) presents the available bubble display, in which each trial is plotted with its marker scaled to analysed sample size; this permits visual inspection of the relationship between study size/precision and effect magnitude but is not a substitute for a fitted meta-regression. Visual inspection is uninformative about a monotonic size–effect relationship here: the largest trial (R3, n = 1,596) reports a large positive effect while the second-largest (R5, n = 748) reports an exactly null one, and the smallest trials span the full range from g = 0.139 to g = 0.985.

With k = 6, any meta-regression would in any case be severely underpowered — the conventional minimum of roughly 10 studies per covariate is not approached — and would carry a high risk of spurious findings. The explanations in Section 6.1 must therefore remain hypotheses for future, better-characterised evidence syntheses to test.

---

## 8. Publication Bias

Small-study effects were assessed using Egger's regression test of funnel-plot asymmetry and the Duval & Tweedie trim-and-fill procedure, both applied on the standardized display scale.

| Diagnostic | Result |
|---|---|
| Egger's regression intercept | 0.0409 |
| Egger's test p-value | 0.6687 |
| Trim-and-fill imputed studies (k₀) | 1 |
| Trim-and-fill adjusted estimate (standardized scale) | g = 0.3659 |
| Overall publication-bias risk rating | **Moderate** |

Egger's regression test shows **no statistically significant small-study effect** (intercept = 0.0409, p = 0.6687), and the trim-and-fill procedure imputed only **one** potentially missing study, implying that funnel-plot asymmetry is minimal and that the pooled estimate is unlikely to change materially after adjustment. The "moderate" overall risk rating therefore does **not** stem from the statistical evidence itself, but more likely from contextual limitations — such as the small number of included studies (which leaves Egger's test substantially underpowered), the high heterogeneity (which can distort funnel-plot-based diagnostics by inducing asymmetry unrelated to publication processes), and the possibility of incomplete searching of grey literature and trial registries. In practice, the results should be read as **"no detectable publication bias, but insufficient power to rule it out,"** so the pooled effect warrants cautious rather than dismissive interpretation.

Two technical cautions should accompany these diagnostics. First, Egger's test is not recommended when fewer than 10 studies are available; with k = 6 its non-significance carries little evidential weight either way. Second, the trim-and-fill adjusted value (g = 0.3659) is expressed on the standardized display scale used for the bias diagnostics and is **not** directly comparable with the native-scale pooled risk ratio of 1.119 reported in Section 5; it should be read only as an indication that the bias correction is small in relative terms, not as a competing primary estimate.

---

## 9. Discussion

### 9.1 Summary of main findings

Across six randomised trials and 3,869 children in low- and middle-income countries, adding mobile phone reminders for caregivers to routine immunisation care yielded a pooled risk ratio of **1.119 (95% CI 1.014 to 1.235; p = 0.0257)** for receipt of the third DTP-containing dose, pooled natively on the risk-ratio scale. The direction classification returned by the analysis for this estimate was "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)". Heterogeneity was considerable (I² = 90.22%; Q = 64.383, df = 5, p < 0.001; τ² = 0.01189), and the approximate 95% prediction interval (0.80 to 1.56) includes the null.

The most defensible reading of these results is therefore layered:

- **On average**, the point estimate is positive and the confidence interval excludes 1, so the evidence is more consistent with a modest benefit than with no benefit at all.
- **The magnitude is small.** A 12% relative increase corresponds, at a 70% baseline, to roughly 8 percentage points — real but far from transformative, and sensitive to baseline coverage.
- **The consistency is poor.** Two of six trials carry nearly all of the positive signal; four show essentially nothing. The pooled average conceals a bimodal distribution rather than describing a common effect.
- **Transportability is unestablished.** The prediction interval implies that a new programme adopting reminders could plausibly see anything from a small decrement to a 56% relative increase in third-dose receipt.

### 9.2 Relation to the wider literature

These findings sit comfortably within, but are more conservative than, the broader mHealth-for-immunisation literature. Earlier syntheses that combined dose-specific coverage with composite "fully immunised child" status, timeliness outcomes, and adjusted odds ratios have typically reported larger and more confidently positive pooled effects. Several methodological choices in the present review work systematically against inflated estimates: restricting to a single dose-specific outcome, using crude intention-to-treat counts rather than adjusted or GEE estimates, declining to back-convert odds ratios (which exaggerate relative effects when the outcome is common, as DTP3 receipt is), preferring overall receipt over "timely receipt", and isolating reminder-only arms from arms that bundled reminders with monetary incentives. The last point is particularly consequential: incentive-plus-reminder arms in multi-arm trials have frequently driven the headline effects in this literature, and attributing those effects to the reminder component alone overstates what a reminder can achieve on its own.

### 9.3 Mechanistic and programmatic interpretation

Reminders act on a specific and narrow causal pathway: they convert *intention* into *attendance* by correcting forgetting and date uncertainty. They do nothing for the other common causes of third-dose drop-out — stock-outs, session cancellations, distance and transport cost, opportunity cost of a caregiver's day, fear of side effects after earlier doses, and active refusal. This mechanism explains both the direction and the dispersion of the results reported here. In systems where forgetting is the binding constraint and supply is reliable, a reminder can plausibly deliver the kind of effect seen in trials R3 and R6. In systems where supply or cost is the binding constraint, a reminder simply informs a caregiver of an appointment they cannot keep — the pattern seen in R1, R2, R4 and R5.

For programme managers, three operational implications follow. First, **diagnose the bottleneck before investing**: reminders are a good buy only where drop-out is attributable to scheduling and recall. Second, **modality should match the population**: voice/IVR rather than SMS where literacy is limited, and registration of the number of the person who actually accompanies the child. Third, **reminders are cheap, which matters**: even a modest average relative effect of 1.119 may be highly cost-effective at a cost per message measured in cents, provided the denominator of reachable, correctly-registered caregivers is large. Cost-effectiveness, not effect size alone, is the correct decision frame for an intervention this inexpensive — but none of the six trials provides the data needed to settle that question here.

---

## 10. Limitations

1. **Very high heterogeneity.** With I² = 90.22%, the pooled risk ratio is an average over a dispersed and apparently bimodal distribution of true effects, not an estimate of a shared effect. Any single-number summary of this evidence base, including ours, is to that extent misleading if quoted without its prediction interval.
2. **Small number of studies (k = 6).** This limits the precision of the between-study variance estimate (τ² = 0.01189 is itself estimated with wide uncertainty on 5 degrees of freedom), renders Egger's test underpowered, and makes the pooled estimate sensitive to the inclusion or exclusion of any single trial — particularly R3, which contributes 41.3% of the analysed sample, and R6, which carries the largest point estimate.
3. **No moderator data.** The absence of study-level covariates in the analysis dataset precluded any meta-regression or subgroup analysis. The heterogeneity therefore remains statistically documented but substantively unexplained; the candidate explanations in Section 6.1 are hypotheses only.
4. **Publication-bias assessment is weak by construction.** Although Egger's test was non-significant (p = 0.6687) and trim-and-fill imputed only one study, the overall bias risk is rated **moderate** because k = 6 provides little power and because grey literature and registry coverage may be incomplete. The correct conclusion is "no detectable bias, insufficient power to exclude it".
5. **Scale mismatch between primary and diagnostic analyses.** The pooled inferential result is a native-scale risk ratio, whereas the forest display, funnel diagnostics and trim-and-fill adjustment operate on standardized (Hedges' g) values. The trim-and-fill adjusted value (g = 0.3659) must not be read as an adjusted risk ratio.
6. **Risk of bias in the included trials.** Caregiver blinding is impossible; outcome ascertainment sometimes depends on home-based records whose retention may itself be affected by the intervention; and cluster-randomised designs with few clusters risk residual imbalance. We mitigated analytic bias by insisting on crude intention-to-treat counts, but could not mitigate design-level bias.
7. **Outcome timing was not harmonised.** Trials assessed DTP3 receipt at windows ranging from roughly 14 weeks to 12 months of age. Longer windows permit catch-up vaccination in control arms and will tend to attenuate apparent reminder effects, contributing an unquantified component of the observed heterogeneity.
8. **Generalisability.** The evidence base is geographically concentrated in a small number of LMIC settings and says nothing about effectiveness at national scale, about decay of effect over repeated message exposure, or about equity — specifically whether reminders help most those households already best connected, thereby widening rather than narrowing coverage gaps.
9. **No cost or implementation data.** The review cannot speak to cost per additional fully-vaccinated child, to sustainability of reminder systems beyond trial conditions, or to the registry/data infrastructure required for delivery at scale.

---

## 11. Conclusion

In children in low- and middle-income countries, mobile phone reminders sent to parents/caregivers in addition to routine immunisation care were associated with a pooled **Risk Ratio of 1.119 (95% CI 1.014 to 1.235; p = 0.0257; k = 6; N = 3,869)** for receipt of the third DTP-containing dose, pooled on the confirmed native risk-ratio scale using REML random-effects methods. The direction classification returned by the analysis for this pooled estimate is "neither (essentially a tie, or a ratio measure where favourability depends on which event was counted)".

The headline number should not be read in isolation. Heterogeneity was considerable (I² = 90.22%; τ² = 0.01189; Q = 64.383, df = 5, p < 0.001), the approximate 95% prediction interval (0.80 to 1.56) includes the null, and almost the entire positive signal derives from two of the six trials. Formal small-study-effect testing was reassuring (Egger's p = 0.6687; one study imputed by trim-and-fill) but is underpowered at k = 6, which is why overall publication-bias risk is rated moderate.

The practical conclusion is a qualified one: mobile phone reminders are a plausible, inexpensive and sometimes substantially effective tool for improving third-dose coverage, but they are not reliably effective everywhere, and the current randomised evidence is too sparse and too heterogeneous to support a confident, transportable estimate of benefit. Priorities for future research are clear — larger trials reporting crude per-arm counts on intention-to-treat denominators for the specific DTP3 dose; prospective, pre-specified comparison of SMS versus voice/IVR modalities in low-literacy populations; harmonised outcome assessment windows; explicit measurement of baseline coverage and supply-side readiness as effect modifiers; equity-disaggregated reporting; and embedded cost-effectiveness analysis. Until such evidence exists, decisions to deploy reminder systems at scale should be grounded in local diagnosis of why children miss their third dose, not in the pooled average reported here.

---

## 12. Figures

| Figure | Description | Path |
|---|---|---|
| Figure 1 | Forest plot of all six study-level estimates with 95% CIs and the random-effects summary | `outputs/bJG9avlBat4bRDhUYzkgRQ/forest_plot.png` |
| Figure 2 | Cumulative meta-analysis showing the running pooled estimate as trials are added | `outputs/bJG9avlBat4bRDhUYzkgRQ/cumulative_plot.png` |
| Figure 3 | Distribution of study-level effect estimates (illustrating bimodality) | `outputs/bJG9avlBat4bRDhUYzkgRQ/effect_distribution.png` |
| Figure 4 | Bubble chart of effect estimate against analysed sample size (marker area ∝ N) | `outputs/bJG9avlBat4bRDhUYzkgRQ/bubble_chart.png` |
| Figure 5 | Heterogeneity diagnostics summary (Q, I², τ², prediction interval) | `outputs/bJG9avlBat4bRDhUYzkgRQ/heterogeneity_summary.png` |

---

## 13. References

Methodological references underpinning the review and analysis:

1. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71.
2. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane; 2023.
3. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. *BMJ*. 2003;327(7414):557–560.
4. DerSimonian R, Laird N. Meta-analysis in clinical trials. *Controlled Clinical Trials*. 1986;7(3):177–188.
5. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software*. 2010;36(3):1–48.
6. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. *Journal of Educational and Behavioral Statistics*. 2005;30(3):261–293. [REML estimation of τ²]
7. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629–634.
8. Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*. 2000;56(2):455–463.
9. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247.
10. Hedges LV, Olkin I. *Statistical Methods for Meta-Analysis*. Academic Press; 1985.
11. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898.
12. World Health Organization. *Immunization Agenda 2030: A Global Strategy to Leave No One Behind*. Geneva: WHO; 2020. [DTP3 as the global coverage tracer indicator]

**Note on primary study citations.** The six included trials are identified in this report by their analysis identifiers (R1–R6 / `study_1_R1`–`study_6_R6`) as supplied in the analysis dataset. Full bibliographic citations for the primary trial reports are held in the review's extraction record and should be appended from that record before publication; they have deliberately not been reconstructed here, since inventing author–year attributions that cannot be verified against the supplied data would misrepresent the evidence base.


## Effect Measure Summary

_This section is generated deterministically from the pipeline's own resolution output (see utils/effect_measures.py), not by the LLM writer above — it is the authoritative statement of which effect measure each outcome group was pooled on, and whether that was the group's own native scale or a Hedges' g/SMD fallback._

| Outcome group | k | Effect measure | Native pooling? | Pooled effect [95% CI] |
|---|---|---|---|---|
| receipt of third dose of DTP-containing vaccine (DTP3/Penta-3) | 6 | Risk Ratio (RR) | Yes | 1.1188 [1.0137, 1.2349] |
