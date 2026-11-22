-- New human-in-the-loop pause right after the search agent: the user can
-- decline found papers and add further PDFs before full-text retrieval.
-- The run status gains 'awaiting_paper_selection'; the CHECK from
-- 0001_initial.sql is unnamed, so Postgres auto-named it runs_status_check.
ALTER TABLE runs DROP CONSTRAINT IF EXISTS runs_status_check;
ALTER TABLE runs ADD CONSTRAINT runs_status_check
    CHECK (status IN ('queued','running','awaiting_paper_selection','awaiting_fulltext_upload',
                      'awaiting_review','completed','failed','cancelled'));
