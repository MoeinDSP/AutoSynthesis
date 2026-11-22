-- Phase 4: POST /api/runs/{run_id}/retry needs to re-dispatch a manual-
-- upload run with its original server-side PDF paths -- these were never
-- persisted anywhere before (only the in-memory `paper_files` argument
-- passed to threading.Thread), so a "queued" row alone wasn't enough to
-- reconstruct a retry. search/downstream-mode runs pass NULL here (they
-- don't need it -- search re-discovers papers, downstream re-reads
-- meta_ready_results.json from output_dir).
ALTER TABLE runs ADD COLUMN IF NOT EXISTS paper_files_json JSONB;
