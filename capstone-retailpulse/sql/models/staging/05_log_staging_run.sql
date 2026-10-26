
-- RetailPulse Capstone
-- Record a successful staging reload

WITH row_counts AS (
    SELECT
        (SELECT COUNT(*) FROM raw.customers)
      + (SELECT COUNT(*) FROM raw.products)
      + (SELECT COUNT(*) FROM raw.orders)
      + (SELECT COUNT(*) FROM raw.payments) AS source_rows,

        (SELECT COUNT(*) FROM staging.customers)
      + (SELECT COUNT(*) FROM staging.products)
      + (SELECT COUNT(*) FROM staging.orders)
      + (SELECT COUNT(*) FROM staging.payments) AS target_rows
),
run_time AS (
    SELECT clock_timestamp() AS recorded_at
)
INSERT INTO audit.pipeline_runs (
    pipeline_name,
    started_at,
    finished_at,
    status,
    source_rows,
    target_rows,
    details
)
SELECT
    'retailpulse_staging_reload',
    recorded_at,
    recorded_at,
    'SUCCESS',
    source_rows,
    target_rows,
    'Staging reload completed; source and staging counts recorded.'
FROM row_counts
CROSS JOIN run_time
WHERE source_rows = target_rows
RETURNING *;
