-- RetailPulse Phase 4 - Part 2
-- First Incremental Load with Watermark
-- Safe to rerun: target uses order_id as primary key.

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

BEGIN;

-- 1. Load only rows newer than the saved watermark.
INSERT INTO audit.incremental_demo_target (
    order_id,
    customer_id,
    amount,
    updated_at
)
SELECT
    s.order_id,
    s.customer_id,
    s.amount,
    s.updated_at
FROM audit.incremental_demo_source AS s
CROSS JOIN audit.incremental_demo_watermark AS w
WHERE w.pipeline_name = 'retailpulse_incremental_demo'
  AND s.updated_at > w.last_updated_at - INTERVAL '1 day'
ON CONFLICT (order_id) DO UPDATE
SET
    customer_id = EXCLUDED.customer_id,
    amount = EXCLUDED.amount,
    updated_at = EXCLUDED.updated_at
WHERE audit.incremental_demo_target.updated_at
      < EXCLUDED.updated_at;

-- 2. Advance the watermark only after processing succeeds.
UPDATE audit.incremental_demo_watermark
SET last_updated_at = COALESCE(
    (
        SELECT MAX(updated_at)
        FROM audit.incremental_demo_source
    ),
    last_updated_at
)
WHERE pipeline_name = 'retailpulse_incremental_demo';


-- Record a successful pipeline run
INSERT INTO audit.incremental_demo_runs (
    pipeline_name,
    completed_at,
    source_rows,
    target_rows,
    status
)
SELECT
    'retailpulse_incremental_demo',
    CURRENT_TIMESTAMP,
    (SELECT COUNT(*) FROM audit.incremental_demo_source),
    (SELECT COUNT(*) FROM audit.incremental_demo_target),
    'SUCCESS';

COMMIT;

COMMIT;



--Password123