
-- RetailPulse Capstone
-- Phase 2 Part 8: Audit logging table

CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.pipeline_runs (
    run_id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_name   TEXT NOT NULL,
    started_at      TIMESTAMPTZ NOT NULL,
    finished_at     TIMESTAMPTZ NOT NULL,
    status          TEXT NOT NULL
                    CHECK (status IN ('SUCCESS', 'FAILED')),
    source_rows     INTEGER NOT NULL DEFAULT 0,
    target_rows     INTEGER NOT NULL DEFAULT 0,
    details         TEXT,
    CONSTRAINT valid_run_times CHECK (finished_at >= started_at),
    CONSTRAINT nonnegative_row_counts CHECK (
        source_rows >= 0 AND target_rows >= 0
    )
);
