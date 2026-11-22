-- AutoSynthesis persistence layer -- initial schema.
--
-- General-purpose (no Cochrane-specific vocabulary anywhere): "runs" is any
-- pipeline execution -- manual upload, auto-search, downstream-only re-run,
-- or a Cochrane benchmark review. Column names mirror models.py's Pydantic
-- classes field-for-field where a table corresponds to one; see
-- persistence/schema.py's comments for the exact mapping.
--
-- File contents on disk (outputs/<run_id>/... or
-- cochrane_benchmark/runs/<review>/<mode>/...) remain the primary artifact
-- store -- see run_artifacts below, which INDEXES those files rather than
-- duplicating their contents (with three deliberate exceptions: plan_json,
-- results_json, pipeline_state_json on `runs`, kept as JSONB backups so
-- /api/runs/{id}/results works even if the output directory is later moved
-- or pruned).

CREATE TABLE IF NOT EXISTS schema_migrations (
    version     text PRIMARY KEY,
    applied_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runs (
    run_id              text PRIMARY KEY,
    session_id          text NULL,
    celery_task_id      text NULL,
    status              text NOT NULL DEFAULT 'queued'
                        CHECK (status IN ('queued','running','awaiting_fulltext_upload',
                                          'awaiting_review','completed','failed','cancelled')),
    mode                text NOT NULL DEFAULT 'manual'
                        CHECK (mode IN ('manual','search','downstream')),
    execution_backend   text NOT NULL DEFAULT 'thread'
                        CHECK (execution_backend IN ('thread','celery')),
    source              text NOT NULL DEFAULT 'dashboard'
                        CHECK (source IN ('dashboard','api','benchmark','cli')),
    -- Generic sibling/external-identifier linking -- e.g. two evaluation
    -- variants of one review, or a caller-supplied benchmark/review id.
    -- Deliberately free-text, never a Cochrane-specific column.
    run_group_id        text NULL,
    run_variant         text NULL,
    external_ref        text NULL,
    external_ref_kind   text NULL,

    prompt              text NOT NULL,
    plan_json           jsonb NULL,
    model_name          text NULL,
    vision_model_name   text NULL,
    config_snapshot     jsonb NULL,

    output_dir          text NOT NULL,

    created_at          timestamptz NOT NULL DEFAULT now(),
    queued_at           timestamptz NULL,
    started_at          timestamptz NULL,
    finished_at         timestamptz NULL,

    current_stage       text NULL,
    failure_stage       text NULL,
    error_message       text NULL,
    error_traceback     text NULL,
    attempt             int NOT NULL DEFAULT 0,

    worker_id           text NULL,
    heartbeat_at        timestamptz NULL,

    -- Taken from the raw GraphState dict, NOT PipelineState -- several
    -- PipelineState counters are dead (always 0) post-conversion; see
    -- orchestrator.py::_to_pipeline_state(). Deliberately richer than
    -- /results here.
    n_search_retrieved      int NULL,
    n_screened_excluded     int NULL,
    n_eligibility_excluded  int NULL,
    n_papers_eligible       int NULL,
    n_studies               int NULL,
    n_effect_sizes          int NULL,

    pdf_cache_hits      int NOT NULL DEFAULT 0,
    pdf_cache_misses    int NOT NULL DEFAULT 0,

    stats_engine        jsonb NULL,
    results_json         jsonb NULL,
    pipeline_state_json  jsonb NULL
);
CREATE INDEX IF NOT EXISTS ix_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS ix_runs_created_at ON runs(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_runs_session_created ON runs(session_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_runs_external_ref ON runs(external_ref);
CREATE INDEX IF NOT EXISTS ix_runs_run_group_id ON runs(run_group_id);

-- Durable replacement for dashboard.py's in-memory pipeline["pending_graph_state"].
-- phase identifies WHICH pause this is (today's two auto-search-mode pauses).
CREATE TABLE IF NOT EXISTS run_pause_states (
    run_id      text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    phase       text NOT NULL CHECK (phase IN ('after_fulltext','after_eligibility')),
    payload     jsonb NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, phase)
);

-- Durable progress trail -- survives Redis eviction/restart; what
-- run_stage_events-derived progress reporting reads instead of (or as a
-- fallback for) the live log stream.
CREATE TABLE IF NOT EXISTS run_stage_events (
    id          bigserial PRIMARY KEY,
    run_id      text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    stage_id    text NOT NULL,
    stage_name  text NULL,
    event       text NOT NULL CHECK (event IN ('start','end','error')),
    at          timestamptz NOT NULL DEFAULT now(),
    detail      jsonb NULL
);
CREATE INDEX IF NOT EXISTS ix_run_stage_events_run_id ON run_stage_events(run_id, at);

-- Mirrors models.PaperRecord / ScreeningDecision / EligibilityDecision.
CREATE TABLE IF NOT EXISTS run_papers (
    id                      bigserial PRIMARY KEY,
    run_id                  text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    paper_id                text NOT NULL,
    title                   text NULL,
    authors                 jsonb NULL,
    year                    int NULL,
    doi                     text NULL,
    pmid                    text NULL,
    url                     text NULL,
    pdf_url                 text NULL,
    source                  text NULL,
    provenance              jsonb NULL,
    document_type           text NULL,
    trial_registry_id       text NULL,
    trial_cluster_id        text NULL,
    is_uploaded             boolean NOT NULL DEFAULT false,
    upload_filename         text NULL,
    has_full_text           boolean NOT NULL DEFAULT false,
    full_text_chars         int NULL,
    screening_decision      text NULL,
    screening_reason        text NULL,
    eligibility_decision    text NULL,
    eligibility_reason      text NULL,
    exclusion_criterion     text NULL,
    fulltext_status         text NULL,
    fulltext_failure_reason text NULL,
    UNIQUE (run_id, paper_id)
);
CREATE INDEX IF NOT EXISTS ix_run_papers_run_id ON run_papers(run_id);

-- Mirrors models.StudyData.
CREATE TABLE IF NOT EXISTS run_studies (
    id                  bigserial PRIMARY KEY,
    run_id              text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    study_id            text NOT NULL,
    paper_id            text NULL,
    title               text NULL,
    treatment_label     text NULL,
    control_label       text NULL,
    n_participants      int NULL,
    n_treatment         int NULL,
    n_control           int NULL,
    moderators          jsonb NULL,
    extraction_status   text NULL,
    extraction_note     text NULL,
    UNIQUE (run_id, study_id)
);
CREATE INDEX IF NOT EXISTS ix_run_studies_run_id ON run_studies(run_id);

-- Mirrors models.EffectSizeRecord field-for-field.
CREATE TABLE IF NOT EXISTS run_effect_sizes (
    id                      bigserial PRIMARY KEY,
    run_id                  text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    study_id                text NULL,
    report_id               text NULL,
    paper_id                text NULL,
    outcome_group_key       text NULL,
    outcome_name            text NULL,
    outcome_family          text NULL,
    comparison_family       text NULL,
    follow_up_timepoint     text NULL,
    unit_of_analysis        text NULL,
    trial_cluster_id        text NULL,
    effect_measure          text NULL,
    computation_scale       text NULL,
    reported_effect_measure text NULL,
    outcome_units           text NULL,
    cohens_d                double precision NULL,
    hedges_g                double precision NULL,
    native_value            double precision NULL,
    native_variance         double precision NULL,
    variance                double precision NULL,
    se                      double precision NULL,
    ci_lower                double precision NULL,
    ci_upper                double precision NULL,
    weight                  double precision NULL,
    n_total                 int NULL,
    computation_method      text NULL,
    conversion_method       text NULL,
    effect_direction        text NULL,
    raw                     jsonb NULL
);
CREATE INDEX IF NOT EXISTS ix_run_effect_sizes_run_id ON run_effect_sizes(run_id);
CREATE INDEX IF NOT EXISTS ix_run_effect_sizes_group ON run_effect_sizes(run_id, outcome_group_key);

-- Mirrors models.MetaAnalysisGroupResult.
CREATE TABLE IF NOT EXISTS run_outcome_groups (
    id                          bigserial PRIMARY KEY,
    run_id                      text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    outcome_group_key           text NOT NULL,
    label                       text NULL,
    outcome_family              text NULL,
    comparison_family           text NULL,
    follow_up_timepoint         text NULL,
    k                           int NULL,
    n_total                     int NULL,
    insufficient_data           boolean NOT NULL DEFAULT false,
    single_effect_g             double precision NULL,
    split_reason                text NULL,
    study_ids                   jsonb NULL,
    effect_measure              text NULL,
    computation_scale           text NULL,
    effect_measure_source       text NULL,
    effect_measure_conflict     text NULL,
    is_primary                  boolean NOT NULL DEFAULT false,
    UNIQUE (run_id, outcome_group_key)
);
CREATE INDEX IF NOT EXISTS ix_run_outcome_groups_run_id ON run_outcome_groups(run_id);

-- Mirrors models.MetaAnalysisResult. is_primary=true is the row surfaced as
-- today's top-level /results.pooled_g/ci_lower/ci_upper/etc.
CREATE TABLE IF NOT EXISTS run_pooled_results (
    run_id                      text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    outcome_group_key           text NOT NULL,
    pooled_effect               double precision NULL,
    pooled_g                    double precision NULL,
    pooled_se                   double precision NULL,
    ci_lower                    double precision NULL,
    ci_upper                    double precision NULL,
    z_value                     double precision NULL,
    p_value                     double precision NULL,
    tau_squared                 double precision NULL,
    tau                         double precision NULL,
    i_squared                   double precision NULL,
    h_squared                   double precision NULL,
    q_statistic                 double precision NULL,
    q_df                        int NULL,
    q_p_value                   double precision NULL,
    k                           int NULL,
    n_total                     int NULL,
    method                      text NULL,
    effect_measure              text NULL,
    computation_scale           text NULL,
    effect_measure_source       text NULL,
    effect_measure_conflict     text NULL,
    is_primary                  boolean NOT NULL DEFAULT false,
    PRIMARY KEY (run_id, outcome_group_key)
);

-- Mirrors models.ModeratorResult.
CREATE TABLE IF NOT EXISTS run_moderator_results (
    id                  bigserial PRIMARY KEY,
    run_id              text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    outcome_group_key   text NULL,
    moderator_name      text NULL,
    qm_statistic        double precision NULL,
    qm_df               int NULL,
    qm_p_value          double precision NULL,
    reference_category  text NULL,
    subgroups           jsonb NULL,
    coefficients        jsonb NULL
);
CREATE INDEX IF NOT EXISTS ix_run_moderator_results_run_id ON run_moderator_results(run_id);

-- Mirrors models.BiasResult.
CREATE TABLE IF NOT EXISTS run_bias_results (
    id                      bigserial PRIMARY KEY,
    run_id                  text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    outcome_group_key       text NULL,
    eggers_intercept        double precision NULL,
    eggers_se               double precision NULL,
    eggers_t_value          double precision NULL,
    eggers_p_value          double precision NULL,
    trim_fill_k0            int NULL,
    trim_fill_side          text NULL,
    trim_fill_g             double precision NULL,
    trim_fill_ci_lower      double precision NULL,
    trim_fill_ci_upper      double precision NULL,
    bias_risk               text NULL
);
CREATE INDEX IF NOT EXISTS ix_run_bias_results_run_id ON run_bias_results(run_id);

-- Mirrors models.RiskOfBiasAssessment (+ nested RoBDomainJudgment as jsonb).
CREATE TABLE IF NOT EXISTS run_rob_assessments (
    id                      bigserial PRIMARY KEY,
    run_id                  text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    paper_id                text NULL,
    paper_title             text NULL,
    design_classification   text NULL,
    design_rationale        text NULL,
    tool_used               text NULL,
    overall_risk             text NULL,
    overall_summary          text NULL,
    domain_judgments        jsonb NULL
);
CREATE INDEX IF NOT EXISTS ix_run_rob_assessments_run_id ON run_rob_assessments(run_id);

-- Mirrors models.ValidationFlag.
CREATE TABLE IF NOT EXISTS run_validation_flags (
    id          bigserial PRIMARY KEY,
    run_id      text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    stage       text NULL,
    severity    text NULL,
    subject_id  text NULL,
    message     text NULL,
    auto_action text NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_run_validation_flags_run_id ON run_validation_flags(run_id);

-- Structured index of the ~15 files agents/pipeline_audit_agent.py (and
-- others) already write under output_dir -- bridges "keep existing output
-- files" with "Postgres becomes the structured source for run history"
-- WITHOUT duplicating file contents.
CREATE TABLE IF NOT EXISTS run_artifacts (
    id              bigserial PRIMARY KEY,
    run_id          text NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    kind            text NULL,
    name            text NOT NULL,
    relative_path   text NOT NULL,
    size_bytes      bigint NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    UNIQUE (run_id, relative_path)
);
CREATE INDEX IF NOT EXISTS ix_run_artifacts_run_id ON run_artifacts(run_id);

-- Source of the measured PDF-cache speedup number (Redis cache, Phase 2).
-- run_id is nullable because a PDF can be parsed outside any tracked run
-- (e.g. an ad-hoc script) -- the cache doesn't require a run to function.
CREATE TABLE IF NOT EXISTS pdf_extraction_events (
    id              bigserial PRIMARY KEY,
    run_id          text NULL REFERENCES runs(run_id) ON DELETE SET NULL,
    content_sha256  text NOT NULL,
    cache_key       text NOT NULL,
    cache_hit       boolean NOT NULL,
    extractor       text NULL,
    text_chars      int NULL,
    elapsed_ms      int NULL,
    created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_pdf_extraction_events_created_at ON pdf_extraction_events(created_at);
CREATE INDEX IF NOT EXISTS ix_pdf_extraction_events_sha256 ON pdf_extraction_events(content_sha256);
CREATE INDEX IF NOT EXISTS ix_pdf_extraction_events_run_id ON pdf_extraction_events(run_id);
