"""SQLAlchemy Core table definitions -- the Python-side description of the
schema in migrations/0001_initial.sql, used for query construction
(run_store.py) and the verify_schema() startup check.

Deliberately Core, not the full ORM: this is a second, complementary
representation used purely for building SQL, not a competing object model
against the Pydantic classes in models.py (which stay authoritative for
in-process data). Column names/types must stay in lockstep with the .sql
migration -- if you add a column here, add it there too, and vice versa.
"""

from __future__ import annotations

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Text, Integer, BigInteger, Boolean, Float, TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import JSONB

METADATA = MetaData()

runs = Table(
    "runs", METADATA,
    Column("run_id", Text, primary_key=True),
    Column("session_id", Text),
    Column("celery_task_id", Text),
    Column("status", Text, nullable=False, default="queued"),
    Column("mode", Text, nullable=False, default="manual"),
    Column("execution_backend", Text, nullable=False, default="thread"),
    Column("source", Text, nullable=False, default="dashboard"),
    Column("run_group_id", Text),
    Column("run_variant", Text),
    Column("external_ref", Text),
    Column("external_ref_kind", Text),
    Column("prompt", Text, nullable=False),
    Column("plan_json", JSONB),
    Column("model_name", Text),
    Column("vision_model_name", Text),
    Column("config_snapshot", JSONB),
    Column("output_dir", Text, nullable=False),
    Column("paper_files_json", JSONB),  # manual-mode server-side PDF paths, for /retry (0002)
    Column("created_at", TIMESTAMP(timezone=True)),
    Column("queued_at", TIMESTAMP(timezone=True)),
    Column("started_at", TIMESTAMP(timezone=True)),
    Column("finished_at", TIMESTAMP(timezone=True)),
    Column("current_stage", Text),
    Column("failure_stage", Text),
    Column("error_message", Text),
    Column("error_traceback", Text),
    Column("attempt", Integer, nullable=False, default=0),
    Column("worker_id", Text),
    Column("heartbeat_at", TIMESTAMP(timezone=True)),
    Column("n_search_retrieved", Integer),
    Column("n_screened_excluded", Integer),
    Column("n_eligibility_excluded", Integer),
    Column("n_papers_eligible", Integer),
    Column("n_studies", Integer),
    Column("n_effect_sizes", Integer),
    Column("pdf_cache_hits", Integer, nullable=False, default=0),
    Column("pdf_cache_misses", Integer, nullable=False, default=0),
    Column("stats_engine", JSONB),
    Column("results_json", JSONB),
    Column("pipeline_state_json", JSONB),
)

run_pause_states = Table(
    "run_pause_states", METADATA,
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), primary_key=True),
    Column("phase", Text, primary_key=True),
    Column("payload", JSONB, nullable=False),
    Column("created_at", TIMESTAMP(timezone=True)),
)

run_stage_events = Table(
    "run_stage_events", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("stage_id", Text, nullable=False),
    Column("stage_name", Text),
    Column("event", Text, nullable=False),
    Column("at", TIMESTAMP(timezone=True)),
    Column("detail", JSONB),
)

run_papers = Table(
    "run_papers", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("paper_id", Text, nullable=False),
    Column("title", Text),
    Column("authors", JSONB),
    Column("year", Integer),
    Column("doi", Text),
    Column("pmid", Text),
    Column("url", Text),
    Column("pdf_url", Text),
    Column("source", Text),
    Column("provenance", JSONB),
    Column("document_type", Text),
    Column("trial_registry_id", Text),
    Column("trial_cluster_id", Text),
    Column("is_uploaded", Boolean, nullable=False, default=False),
    Column("upload_filename", Text),
    Column("has_full_text", Boolean, nullable=False, default=False),
    Column("full_text_chars", Integer),
    Column("screening_decision", Text),
    Column("screening_reason", Text),
    Column("eligibility_decision", Text),
    Column("eligibility_reason", Text),
    Column("exclusion_criterion", Text),
    Column("fulltext_status", Text),
    Column("fulltext_failure_reason", Text),
)

run_studies = Table(
    "run_studies", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("study_id", Text, nullable=False),
    Column("paper_id", Text),
    Column("title", Text),
    Column("treatment_label", Text),
    Column("control_label", Text),
    Column("n_participants", Integer),
    Column("n_treatment", Integer),
    Column("n_control", Integer),
    Column("moderators", JSONB),
    Column("extraction_status", Text),
    Column("extraction_note", Text),
)

run_effect_sizes = Table(
    "run_effect_sizes", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("study_id", Text),
    Column("report_id", Text),
    Column("paper_id", Text),
    Column("outcome_group_key", Text),
    Column("outcome_name", Text),
    Column("outcome_family", Text),
    Column("comparison_family", Text),
    Column("follow_up_timepoint", Text),
    Column("unit_of_analysis", Text),
    Column("trial_cluster_id", Text),
    Column("effect_measure", Text),
    Column("computation_scale", Text),
    Column("reported_effect_measure", Text),
    Column("outcome_units", Text),
    Column("cohens_d", Float),
    Column("hedges_g", Float),
    Column("native_value", Float),
    Column("native_variance", Float),
    Column("variance", Float),
    Column("se", Float),
    Column("ci_lower", Float),
    Column("ci_upper", Float),
    Column("weight", Float),
    Column("n_total", Integer),
    Column("computation_method", Text),
    Column("conversion_method", Text),
    Column("effect_direction", Text),
    Column("raw", JSONB),
)

run_outcome_groups = Table(
    "run_outcome_groups", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("outcome_group_key", Text, nullable=False),
    Column("label", Text),
    Column("outcome_family", Text),
    Column("comparison_family", Text),
    Column("follow_up_timepoint", Text),
    Column("k", Integer),
    Column("n_total", Integer),
    Column("insufficient_data", Boolean, nullable=False, default=False),
    Column("single_effect_g", Float),
    Column("split_reason", Text),
    Column("study_ids", JSONB),
    Column("effect_measure", Text),
    Column("computation_scale", Text),
    Column("effect_measure_source", Text),
    Column("effect_measure_conflict", Text),
    Column("is_primary", Boolean, nullable=False, default=False),
)

run_pooled_results = Table(
    "run_pooled_results", METADATA,
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), primary_key=True),
    Column("outcome_group_key", Text, primary_key=True),
    Column("pooled_effect", Float),
    Column("pooled_g", Float),
    Column("pooled_se", Float),
    Column("ci_lower", Float),
    Column("ci_upper", Float),
    Column("z_value", Float),
    Column("p_value", Float),
    Column("tau_squared", Float),
    Column("tau", Float),
    Column("i_squared", Float),
    Column("h_squared", Float),
    Column("q_statistic", Float),
    Column("q_df", Integer),
    Column("q_p_value", Float),
    Column("k", Integer),
    Column("n_total", Integer),
    Column("method", Text),
    Column("effect_measure", Text),
    Column("computation_scale", Text),
    Column("effect_measure_source", Text),
    Column("effect_measure_conflict", Text),
    Column("is_primary", Boolean, nullable=False, default=False),
)

run_moderator_results = Table(
    "run_moderator_results", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("outcome_group_key", Text),
    Column("moderator_name", Text),
    Column("qm_statistic", Float),
    Column("qm_df", Integer),
    Column("qm_p_value", Float),
    Column("reference_category", Text),
    Column("subgroups", JSONB),
    Column("coefficients", JSONB),
)

run_bias_results = Table(
    "run_bias_results", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("outcome_group_key", Text),
    Column("eggers_intercept", Float),
    Column("eggers_se", Float),
    Column("eggers_t_value", Float),
    Column("eggers_p_value", Float),
    Column("trim_fill_k0", Integer),
    Column("trim_fill_side", Text),
    Column("trim_fill_g", Float),
    Column("trim_fill_ci_lower", Float),
    Column("trim_fill_ci_upper", Float),
    Column("bias_risk", Text),
)

run_rob_assessments = Table(
    "run_rob_assessments", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("paper_id", Text),
    Column("paper_title", Text),
    Column("design_classification", Text),
    Column("design_rationale", Text),
    Column("tool_used", Text),
    Column("overall_risk", Text),
    Column("overall_summary", Text),
    Column("domain_judgments", JSONB),
)

run_validation_flags = Table(
    "run_validation_flags", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("stage", Text),
    Column("severity", Text),
    Column("subject_id", Text),
    Column("message", Text),
    Column("auto_action", Text),
    Column("created_at", TIMESTAMP(timezone=True)),
)

run_artifacts = Table(
    "run_artifacts", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="CASCADE"), nullable=False),
    Column("kind", Text),
    Column("name", Text, nullable=False),
    Column("relative_path", Text, nullable=False),
    Column("size_bytes", BigInteger),
    Column("created_at", TIMESTAMP(timezone=True)),
)

pdf_extraction_events = Table(
    "pdf_extraction_events", METADATA,
    Column("id", BigInteger, primary_key=True),
    Column("run_id", Text, ForeignKey("runs.run_id", ondelete="SET NULL")),
    Column("content_sha256", Text, nullable=False),
    Column("cache_key", Text, nullable=False),
    Column("cache_hit", Boolean, nullable=False),
    Column("extractor", Text),
    Column("text_chars", Integer),
    Column("elapsed_ms", Integer),
    Column("created_at", TIMESTAMP(timezone=True)),
)

schema_migrations = Table(
    "schema_migrations", METADATA,
    Column("version", Text, primary_key=True),
    Column("applied_at", TIMESTAMP(timezone=True)),
)
