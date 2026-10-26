-- RetailPulse Phase 4 - Part 5
-- Audit log table for incremental pipeline

CREATE TABLE IF NOT EXISTS audit.incremental_demo_runs (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    source_rows INTEGER NOT NULL DEFAULT 0,
    target_rows INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL
        CHECK (status IN ('SUCCESS', 'FAILED')),
    error_message TEXT
);