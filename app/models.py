"""Pydantic data models for the generic meta-analysis pipeline."""

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal, Dict, Union


class EffectMeasure(str, Enum):
    """Native effect-size family a given outcome group is pooled on.

    Deliberately a SEPARATE enum from cochrane_benchmark.models.EffectMeasure
    (same value vocabulary, no shared import) -- production code must not
    depend on the benchmark subpackage; see utils/effect_measures.py's
    module docstring for the full rationale. UNKNOWN is a first-class,
    expected outcome of resolution, not an error state -- see
    utils/effect_measures.py::resolve_group_effect_measure()."""

    SMD = "SMD"             # Standardized Mean Difference
    MD = "MD"                # (raw/unstandardized) Mean Difference
    OR = "OR"                 # Odds Ratio
    PETO_OR = "PETO_OR"       # Peto Odds Ratio
    RR = "RR"                 # Risk Ratio
    HR = "HR"                 # Hazard Ratio -- ratio measure, pooled on log scale exactly like
                               # OR/RR/PETO_OR (generic inverse-variance on log(HR), the standard
                               # convention). No counts-based reconstruction exists for HR (a 2x2
                               # table cannot recover a time-to-event hazard ratio) -- only an
                               # already-reported HR+CI can ever populate this scale. See
                               # utils/effect_measures.py::compute_native_row_effect().
    RD = "RD"                 # Risk Difference (p_treatment - p_control) -- LINEAR scale like MD,
                               # never log-transformed/back-transformed. Cochrane's standard
                               # alternative to RR/OR for rare-event or zero-cell-heavy dichotomous
                               # outcomes, where RD's variance formula stays well-behaved without a
                               # continuity correction. Computed from raw 2x2 counts via
                               # metafor::escalc(measure="RD") -- see
                               # statistics/metafor_engine.py::escalc_rd_from_counts().
    HEDGES_G = "HEDGES_G"     # explicit Hedges' g
    GENERIC = "GENERIC"       # generic inverse-variance, already-computed estimate
    UNKNOWN = "UNKNOWN"       # not resolved with sufficient confidence -- see resolve_group_effect_measure()


class MetaAnalysisPlan(BaseModel):
    """
    Dynamically generated plan produced by the PlanningAgent.
    Every downstream agent reads from this to stay topic-agnostic.
    """
    research_question: str
    treatment_label: str        # e.g. "LLM-generated message", "mindfulness intervention"
    control_label: str          # e.g. "human-written message", "waitlist control"
    outcome_description: str    # e.g. "attitude change on a Likert scale"
    positive_direction: str     # e.g. "positive g = treatment more effective than control"
    higher_score_is_worse: bool = False
    # True when a HIGHER raw score on this plan's outcome measure means a WORSE result (e.g.
    # a symptom-severity/problem/pain scale like ECBI or PHQ-9). False when a HIGHER raw score
    # means a BETTER result (e.g. a function, quality-of-life, or skill scale). Decided once by
    # the planning agent from the outcome's own definition -- never inferred downstream from
    # the scale's name via keyword matching. utils/paper_results_converter.py::_convert_row()
    # uses this to flip the sign of cohens_d/hedges_g so a positive computed value always
    # matches positive_direction's stated convention, instead of the raw, unflipped
    # (mean_treatment - mean_control) sign. Root cause this fixes: without it, a
    # lower-is-better outcome where the treatment arm improved MORE than control produces a
    # NEGATIVE hedges_g even though the row's own effect_direction field says "positive" --
    # an internal contradiction that also flips the sign of the whole pooled result.
    search_queries: List[str]   # 1–3 queries for the arXiv/database API
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    moderators_to_extract: List[str]   # e.g. ["study design", "topic domain", "sample type"]
    search_start_year: int = 2020
    effect_size_note: Optional[str] = ""  # any special notes for effect-size computation

    # --- Native effect-measure resolution: tier 1 (explicit request) and the
    # separate, lower-priority tier-3 supporting signal -- see
    # utils/effect_measures.py::resolve_group_effect_measure(). Both are
    # plan-level defaults, applied to every outcome group unless a group's
    # own rows carry stronger evidence (tier 2, paper-reported). ---
    target_effect_measure: Optional[EffectMeasure] = None
    # tier 1 -- an explicit, deliberate user request (e.g. "pool this as an
    # odds ratio"), extracted by plan_node from the user's own prompt. When
    # set, this is an intentional override: it wins over what any individual
    # paper reports, but a disagreement is still recorded (never silent) --
    # see EffectSizeRecord/MetaAnalysisGroupResult's effect_measure_conflict.

    methodology_effect_measure_hint: Optional[EffectMeasure] = None
    # tier 3 (supporting signal only, NEVER an override) -- e.g. a Cochrane
    # review's own stated methodology ("we pooled dichotomous outcomes as
    # risk ratios"). Set only by cochrane_benchmark/pipeline.py from
    # ReviewContext.stated_effect_measure (methodology text, not a result --
    # never from GroundTruth). Production runs never set this field.

    split_by_timepoint: bool = False
    # Gate for utils/outcome_grouping.py::build_outcome_group_key() -- whether
    # follow_up_timepoint should fragment an outcome_family into separate
    # pooling groups. Defaults to False: an outcome is pooled as ONE number
    # (Cochrane's own convention -- "Mortality (all-cause)" is one comparison,
    # not "Mortality at 3mo"/"Mortality at 12mo", unless the review itself
    # analyzes it that way). Set True only when the user's own prompt, or (for
    # Cochrane runs) the review's stated methodology, explicitly calls for
    # separate timepoint analyses -- same supporting-signal provenance as
    # methodology_effect_measure_hint above, never inferred from paper text.
    # follow_up_timepoint is ALWAYS still recorded as metadata on every row
    # regardless of this flag -- only the GROUPING behavior changes.

    single_outcome_target: Optional[str] = None
    # Set ONLY when the user's OWN research question explicitly asks about
    # one specific, singular outcome/construct (e.g. "effect on mortality",
    # "effect on positive symptoms of psychosis") rather than several outcomes
    # or a broad clinical/functional battery -- extracted by plan_node from
    # the prompt, same provenance discipline as split_by_timepoint above
    # (never inferred from paper text, never review-specific). A short,
    # canonical name for that one construct, e.g. "positive symptoms of
    # psychosis" -- None (the default) means "let the two-pass outcome
    # taxonomy discover however many families the batch actually needs" (the
    # normal, multi-outcome path).
    #
    # When set, agents/cross_paper_outcome_mapper_agent.py's classification
    # pass is anchored to this ONE family instead of letting the taxonomy
    # step freely invent per-instrument sub-families (e.g. "PANSS positive
    # symptoms" vs "BPRS positive symptoms" vs "SAPS positive symptoms" all
    # measuring the SAME target construct) -- confirmed via a real test run
    # (CD015331, positive-symptoms-only prompt) that without this override,
    # a single declared target outcome still fragmented into 3 pooling
    # groups purely because of which rating scale each study used. This
    # mechanism is general: it activates for ANY plan whose prompt names one
    # outcome, not a hardcoded list for any specific review.

    @field_validator("effect_size_note", mode="before")
    @classmethod
    def _coerce_effect_size_note(cls, v):
        return v if v is not None else ""


class PaperRecord(BaseModel):
    id: str
    title: str
    abstract: str
    authors: List[str] = []
    year: int
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    source: str
    doi: Optional[str] = None
    full_text: Optional[str] = None

    # --- Additive retrieval-provenance fields (database_search.py's
    # extended source registry -- see utils/manual_import.py,
    # search_clinicaltrials_gov, search_wos). All optional; a record from
    # any pre-existing source that doesn't set these behaves exactly as
    # before. ---
    pmid: Optional[str] = None                       # PubMed/PMC ID, when the source provides one directly
                                                        # (previously only resolved downstream during full-text fetch)
    trial_registry_id: Optional[str] = None            # e.g. an NCT ID, when the record came from a trial registry
                                                        # (ClinicalTrials.gov, WHO ICTRP) rather than a paper database,
                                                        # OR backfilled by utils/trial_matching.py from a registry ID
                                                        # found in the paper's own full text (generic NCT/ISRCTN/
                                                        # EudraCT-style regex -- never disease/study-name-specific)
    provenance: List[str] = Field(default_factory=list)  # every source that contributed to this record after
                                                            # dedup-merge, e.g. ["pubmed", "clinicaltrials_gov"] --
                                                            # `source` stays the FIRST source that found it (unchanged
                                                            # field, unchanged meaning); provenance is the full list

    # --- Document-provenance fields (see agents/document_type_agent.py) ---
    document_type: Optional[str] = None
    # One of "primary_study" | "systematic_review_or_meta_analysis" |
    # "protocol_or_registration" | "guideline_or_consensus_statement" |
    # "narrative_review_or_commentary" | "unclear" | None (not yet classified,
    # e.g. search-mode papers that already passed eligibility_node's own
    # equivalent check). Set by document_type_node for manual-mode uploads --
    # a closed vocabulary, never a per-review label.
    trial_cluster_id: Optional[str] = None
    # Stable id (hash of the sorted paper ids in the cluster -- never derived
    # from a study/author name) shared by two-or-more PaperRecords that
    # utils/trial_matching.py::match_same_trial() determined describe the
    # SAME underlying trial. None when no companion publication was found.
    # Used by agents/meta_analysis_agent.py to avoid double-counting one
    # trial's data twice within a single pooling group.


class ScreeningDecision(BaseModel):
    paper_id: str
    decision: Literal["include", "exclude"]
    reason: str


class EligibilityDecision(BaseModel):
    paper_id: str
    decision: Literal["include", "exclude"]
    reason: str
    exclusion_criterion: Optional[Literal["insufficient_design", "missing_data"]] = None


class StudyData(BaseModel):
    """
    Generic study record — works for any meta-analysis topic.
    Statistical fields use treatment/control instead of domain-specific labels.
    Moderator variables are stored as a free-form dict keyed by moderator name.
    """
    study_id: str
    report_id: str
    title: str = ""
    paper_id: str = ""
    treatment_label: str = ""   # specific label for this study's treatment arm
    control_label: str = ""     # specific label for this study's control arm
    # Core statistics
    n_participants: Optional[int] = None
    n_treatment: Optional[int] = None
    n_control: Optional[int] = None
    mean_treatment: Optional[float] = None
    mean_control: Optional[float] = None
    sd_treatment: Optional[float] = None
    sd_control: Optional[float] = None
    t_value: Optional[float] = None
    f_value: Optional[float] = None
    p_value: Optional[float] = None
    prop_treatment: Optional[float] = None   # binary outcomes
    prop_control: Optional[float] = None
    publication_year: Optional[int] = None
    is_peer_reviewed: bool = True
    moderators: dict = {}   # {moderator_name: value} — flexible per plan

    @model_validator(mode="after")
    def _fill_derived_fields(self) -> "StudyData":
        # Compute n_participants from group sizes if missing
        if self.n_participants is None:
            if self.n_treatment is not None and self.n_control is not None:
                self.n_participants = self.n_treatment + self.n_control
            elif self.n_treatment is not None:
                self.n_participants = self.n_treatment
            elif self.n_control is not None:
                self.n_participants = self.n_control
        # Fall back to year from paper metadata stored in moderators, or use 0
        if self.publication_year is None:
            self.publication_year = int(self.moderators.get("year", 0)) or None
        return self

class MetaReadyResult(BaseModel):
    """
    Normalized result row produced from paper_results.json.

    This is the bridge between general statistical extraction and
    meta-analysis effect-size computation.
    """
    paper_id: str
    paper_title: str = ""
    study_label: str = ""
    outcome_name: str = ""
    comparison_label: str = ""

    treatment_label: str = ""
    control_label: str = ""

    n_treatment: Optional[int] = None
    n_control: Optional[int] = None

    mean_treatment: Optional[float] = None
    mean_control: Optional[float] = None
    sd_treatment: Optional[float] = None
    sd_control: Optional[float] = None

    t_value: Optional[float] = None
    f_value: Optional[float] = None
    coefficient: Optional[float] = None
    p_value: Optional[float] = None

    statistic_type: str = ""
    effect_size_ready: bool = False
    exclusion_reason: Optional[str] = None

    cohens_d: Optional[float] = None
    hedges_g: Optional[float] = None
    conversion_method: Optional[str] = None

    evidence_quote: Optional[str] = None

class EffectSizeRecord(BaseModel):
    study_id: str
    report_id: str
    cohens_d: float
    hedges_g: float
    variance: float
    se: float
    ci_lower: float
    ci_upper: float
    weight: Optional[float] = None
    n_total: int
    computation_method: str   # "means_sds" | "t_value" | "f_value" | "proportions"

    # --- Outcome grouping (added so cross_paper_outcome_mapper_agent's
    # construct classification survives into pooling -- previously computed
    # correctly at the mapping stage but silently dropped before reaching
    # effect_size_node/meta_analysis_node, which pooled every row from every
    # paper into one undifferentiated model regardless of what construct it
    # measured. See agents/meta_analysis_agent.py and
    # utils/outcome_grouping.py::build_outcome_group_key(). ---
    outcome_name: Optional[str] = None            # display label, e.g. "PROMIS Cognitive Abilities"
    outcome_family: Optional[str] = None           # normalised construct, from cross_paper_outcome_mapper_agent's
                                                    # run-specific closed taxonomy (see record_outcome_taxonomy)
    comparison_family: Optional[str] = None        # normalised comparison/intervention construct, same mapper --
                                                    # e.g. "drug_a_vs_placebo" vs "drug_b_vs_placebo". Included in
                                                    # outcome_group_key so different comparisons on the same outcome
                                                    # are never pooled together (see utils/outcome_grouping.py)
    effect_direction: Optional[str] = None         # free text from the mapper describing which arm this row's
                                                    # positive value favors -- VALIDATION-ONLY (see
                                                    # agents/meta_analysis_agent.py's direction check); never used
                                                    # to auto-flip a sign, only to flag disagreement within a group
    favors_treatment: Optional[bool] = None        # True/False/None (tie or unknown) -- computed by
                                                    # agents/effect_size_agent.py from this row's RAW hedges_g sign
                                                    # (treatment - control, never flipped -- see
                                                    # utils/effect_measures.py::determine_favors_treatment()) plus
                                                    # plan.higher_score_is_worse. This is the ONLY place
                                                    # higher_score_is_worse affects anything -- hedges_g/cohens_d
                                                    # themselves always keep the raw statistical sign convention,
                                                    # matching how Cochrane/RevMan itself reports these measures, so
                                                    # numbers are directly comparable to a published forest plot.
                                                    # "Which side is favourable" is answered by this field instead.
    unit_of_analysis: Optional[str] = None         # e.g. "per participant" / "per event" / "per limb" -- only
                                                    # populated when the paper states one explicitly; VALIDATION-ONLY,
                                                    # flags disagreement within a pooling group, never auto-corrects
    trial_cluster_id: Optional[str] = None         # shared by two-or-more rows whose underlying PaperRecords
                                                    # utils/trial_matching.py determined describe the SAME
                                                    # trial (see PaperRecord.trial_cluster_id) -- used by
                                                    # agents/meta_analysis_agent.py to avoid double-counting
                                                    # one trial's data twice within a single pooling group
    conversion_method: Optional[str] = None        # how this row's hedges_g/native_value was derived, e.g.
                                                    # "means_sds" | "reported_or" | "reported_rr" | "hr_to_d_approx"
                                                    # | "median_iqr_wan2014_approx" -- lets downstream code/reports
                                                    # tell an exact conversion from a tagged approximation
    follow_up_timepoint: Optional[str] = None      # normalised follow-up window, e.g. "intermediate (1-6 months)" --
                                                    # ALWAYS recorded as metadata when the paper states one, regardless
                                                    # of whether it is used to split pooling groups (see split_by_timepoint
                                                    # on MetaAnalysisPlan and build_outcome_group_key())
    outcome_group_key: str = "default"             # declarative key built from the fields above;
                                                    # "default" when no construct info is available at all
                                                    # (legacy/degenerate case -- keeps single-outcome runs
                                                    # behaving exactly as before: one group, one pooled result)

    # --- Native effect-measure inputs (row-level evidence -- see
    # utils/effect_measures.py::resolve_group_effect_measure() and
    # compute_native_row_effect()). All optional and additive: a row with
    # none of this populated behaves exactly as before (pooled on hedges_g
    # only). ---
    reported_effect_measure: Optional[str] = None  # free text, as stated BY THE PAPER itself
                                                    # (e.g. "risk ratio") -- tier-2 evidence; never
                                                    # inferred/computed, only set when the paper's own
                                                    # results section names its measure
    outcome_units: Optional[str] = None            # e.g. "mmHg", "days" -- tier-3 MD-vs-SMD evidence
    raw_measure_inputs: Dict[str, Union[float, str]] = Field(default_factory=dict)
                                                    # whichever of events_treatment/n_treatment/
                                                    # events_control/n_control (dichotomous) or
                                                    # mean_treatment/sd_treatment/mean_control/sd_control
                                                    # (continuous) or reported_ratio/reported_ratio_ci_lower/
                                                    # reported_ratio_ci_upper (already-reported RR/OR) is
                                                    # available for THIS row -- the raw ingredients
                                                    # compute_native_row_effect() needs to (re)compute a
                                                    # reported_ratio_measure (str: "RR"/"OR"/"HR") tags
                                                    # WHICH field actually supplied reported_ratio, so
                                                    # compute_native_row_effect() can refuse to let an HR
                                                    # silently satisfy an RR/OR request (or vice versa) --
                                                    # the one non-numeric value this dict carries.
                                                    # native-scale value via metafor_engine, distinct from
                                                    # the hedges_g/cohens_d columns above.

    effect_measure: EffectMeasure = EffectMeasure.UNKNOWN   # resolved for this row's group -- see
                                                              # MetaAnalysisGroupResult.effect_measure_source
    computation_scale: EffectMeasure = EffectMeasure.HEDGES_G  # the scale native_value/native_variance
                                                                 # are actually expressed on -- always
                                                                 # concrete (falls back to HEDGES_G when
                                                                 # effect_measure is UNKNOWN), so pooling
                                                                 # always has a usable number
    native_value: Optional[float] = None            # point estimate on computation_scale (log scale for
                                                     # OR/RR/PETO_OR, matching metafor's own yi convention;
                                                     # linear scale for MD/SMD/HEDGES_G)
    native_variance: Optional[float] = None          # sampling variance of native_value


class MetaAnalysisResult(BaseModel):
    pooled_g: float          # BACKWARD-COMPAT NAME ONLY -- kept because existing callers
                              # (dashboard.py, plots, older reports) read it by this name;
                              # always numerically identical to pooled_effect below. New
                              # measure-aware code should read pooled_effect instead, since
                              # "pooled_g" implies Hedges' g even when computation_scale is
                              # RR/OR/MD (see effect_measure/computation_scale below).
    pooled_effect: Optional[float] = None   # measure-neutral name -- auto-filled from
                                              # pooled_g when omitted (see validator below);
                                              # the value is on computation_scale's units
                                              # (already back-transformed to the natural
                                              # ratio scale for RR/OR/PETO_OR, not log-scale).
    pooled_se: float
    ci_lower: float
    ci_upper: float
    z_value: float
    p_value: float
    tau_squared: float
    tau: float
    i_squared: float
    h_squared: float
    q_statistic: float
    q_df: int
    q_p_value: float
    k: int
    n_total: int
    method: str = "REML"

    # --- Measure/scale of THIS pooled result -- added so anything reading
    # meta_result directly (the "primary" alias -- e.g. report_agent.py,
    # dashboard.py) can determine the measure/scale without needing the
    # wrapping MetaAnalysisGroupResult. Same fields/semantics as
    # MetaAnalysisGroupResult's own copies (see utils/effect_measures.py);
    # kept on BOTH because MetaAnalysisGroupResult.result is None for
    # insufficient_data groups, where the wrapper-level fields are the only
    # ones available. Defaults preserve pre-existing (Hedges' g-only)
    # behaviour for any caller that doesn't set them (e.g.
    # regenerate_run_plots.py, which pools hedges_g directly and doesn't
    # run measure resolution at all). ---
    effect_measure: EffectMeasure = EffectMeasure.HEDGES_G
    computation_scale: EffectMeasure = EffectMeasure.HEDGES_G
    effect_measure_source: Literal[
        "explicit_user_request", "explicit_paper_reported",
        "methodology_and_deterministic_agree", "methodology_prior", "deterministic_evidence",
        "unresolved_fallback",
    ] = "unresolved_fallback"
    effect_measure_conflict: Optional[str] = None

    favors_treatment: Optional[bool] = None   # same semantics as EffectSizeRecord.favors_treatment, computed
                                               # from pooled_g's RAW sign + plan.higher_score_is_worse (see
                                               # agents/meta_analysis_agent.py). pooled_g/pooled_effect above are
                                               # never flipped -- this field alone answers "which side won."

    @model_validator(mode="after")
    def _fill_pooled_effect(self) -> "MetaAnalysisResult":
        if self.pooled_effect is None:
            self.pooled_effect = self.pooled_g
        return self


class MetaAnalysisGroupResult(BaseModel):
    """One pooled meta-analysis for ONE outcome_group_key -- the unit that
    replaces "the one pooled MetaAnalysisResult" now that meta_analysis_node
    can produce several, one per distinct outcome construct/timepoint found
    among the included rows. See agents/meta_analysis_agent.py."""

    outcome_group_key: str
    outcome_family: Optional[str] = None
    comparison_family: Optional[str] = None        # which comparison/intervention this group is about, when the
                                                    # review has more than one (see utils/outcome_grouping.py) --
                                                    # None when every row in the review shares one comparison
    follow_up_timepoint: Optional[str] = None
    label: str                                    # human-readable, e.g. "subjective_cognitive_function (intermediate (1-6 months))"
    k: int
    n_total: int
    study_ids: List[str] = Field(default_factory=list)
    insufficient_data: bool = False                # True when k < MIN_K_FOR_POOLING -- reported, never silently merged
    single_effect_g: Optional[float] = None        # populated only when insufficient_data and k==1, for transparency
    result: Optional[MetaAnalysisResult] = None    # None when insufficient_data

    # --- Native effect-measure resolution outcome for this group -- see
    # utils/effect_measures.py::resolve_group_effect_measure(). result.pooled_g
    # (above) is ALWAYS the pooled number on computation_scale; these fields
    # say what that scale actually is and how confidently it was chosen. ---
    effect_measure: EffectMeasure = EffectMeasure.UNKNOWN
    computation_scale: EffectMeasure = EffectMeasure.HEDGES_G
    effect_measure_source: Literal[
        "explicit_user_request", "explicit_paper_reported",
        "methodology_and_deterministic_agree", "methodology_prior", "deterministic_evidence",
        "unresolved_fallback",
    ] = "unresolved_fallback"
    effect_measure_conflict: Optional[str] = None  # human-readable note when two signals disagreed --
                                                     # populated, never silently dropped, per explicit
                                                     # instruction (see resolve_group_effect_measure())
    split_reason: Optional[str] = None              # populated when this group was carved out of a larger
                                                     # outcome_group_key because its rows reported an incompatible
                                                     # effect measure (e.g. HR vs OR) -- see
                                                     # agents/meta_analysis_agent.py's measure-compatibility
                                                     # partition pass. None for groups that weren't split.


class ValidationFlag(BaseModel):
    """One structured, auditable note about data that was missing, incompatible,
    ambiguous, or misclassified somewhere in the pipeline -- the outcome-level
    counterpart to agents/pipeline_audit_agent.py's paper-level loss_stage/
    loss_reason tracking. Every mechanism that used to only log a warning or
    silently fall back now also appends one of these; never a substitute for
    fixing the underlying issue, just a record that it happened and why."""

    stage: Literal[
        "extraction", "outcome_classification", "effect_measure_resolution",
        "comparison_split", "direction_check", "unit_of_analysis_check",
        "trial_dedup", "document_type_gate", "insufficient_data",
    ]
    severity: Literal["info", "warning", "error"]
    subject_id: str      # paper_id / study_id / outcome_group_key, whichever this flag is about
    message: str
    auto_action: Optional[str] = None   # e.g. "split_group" | "excluded_row" | "excluded_paper" | None


class SubgroupResult(BaseModel):
    category: str
    k: int
    pooled_g: float
    ci_lower: float
    ci_upper: float
    tau_squared: float
    i_squared: float


class ModeratorResult(BaseModel):
    moderator_name: str
    qm_statistic: float
    qm_df: int
    qm_p_value: float
    subgroups: List[SubgroupResult]
    reference_category: str
    coefficients: List[dict]   # [{term, estimate, se, ci_lower, ci_upper, p_value}]


class BiasResult(BaseModel):
    eggers_intercept: float
    eggers_se: float
    eggers_t_value: float
    eggers_p_value: float
    trim_fill_k0: int
    trim_fill_side: str
    trim_fill_g: float
    trim_fill_ci_lower: float
    trim_fill_ci_upper: float
    bias_risk: Literal["low", "moderate", "high"]


class RoBDomainJudgment(BaseModel):
    """One domain judgment within a RoB 2 (randomized) or ROBINS-I (non-randomized)
    assessment. `domain_name` and the valid `judgment` values depend on `tool_used`
    on the parent RiskOfBiasAssessment:
      RoB 2:    judgment in {"low", "some_concerns", "high"}
      ROBINS-I: judgment in {"low", "moderate", "serious", "critical", "no_information"}
    """
    domain_number: int
    domain_name: str
    judgment: str
    rationale: str
    evidence_quote: Optional[str] = None


class RiskOfBiasAssessment(BaseModel):
    """Per-study risk-of-bias assessment, one per included paper."""
    paper_id: str
    paper_title: str
    design_classification: Literal["randomized", "non_randomized"]
    design_rationale: str = ""
    tool_used: Literal["RoB2", "ROBINS-I"]
    domain_judgments: List[RoBDomainJudgment] = []
    overall_risk: str  # RoB2: low|some_concerns|high ; ROBINS-I: low|moderate|serious|critical|no_information
    overall_summary: str = ""


class PipelineState(BaseModel):
    plan: Optional[MetaAnalysisPlan] = None
    search_n_retrieved: int = 0
    search_n_after_dedup: int = 0
    screening_n_included: int = 0
    screening_n_excluded: int = 0
    eligibility_n_included: int = 0
    eligibility_n_excluded_design: int = 0
    eligibility_n_excluded_data: int = 0
    included_studies: List[StudyData] = []
    effect_sizes: List[EffectSizeRecord] = []
    meta_analysis: Optional[MetaAnalysisResult] = None       # alias for the primary outcome group -- see meta_analysis_groups
    meta_analysis_groups: List[MetaAnalysisGroupResult] = []  # one per distinct outcome_group_key
    moderator_results: List[ModeratorResult] = []
    bias_result: Optional[BiasResult] = None
    rob_assessments: List[RiskOfBiasAssessment] = []
    report_path: Optional[str] = None
    stats_engine_info: Optional[Dict[str, str]] = None
    validation_flags: List[ValidationFlag] = []
