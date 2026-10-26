
-- RetailPulse: Incremental Pipeline Monitoring

-- 1. Recent pipeline runs
SELECT
    run_id,
    pipeline_name,
    started_at,
    completed_at,
    source_rows,
    target_rows,
    status,
    error_message
FROM audit.incremental_demo_runs
ORDER BY run_id DESC
LIMIT 10;


-- 2. Run summary by status
SELECT
    status,
    COUNT(*) AS total_runs
FROM audit.incremental_demo_runs
GROUP BY status
ORDER BY status;


-- 3. Latest failed runs
SELECT
    run_id,
    started_at,
    completed_at,
    error_message
FROM audit.incremental_demo_runs
WHERE status = 'FAILED'
ORDER BY run_id DESC
LIMIT 5;


-- 4. Most recent successful run
SELECT
    run_id,
    started_at,
    completed_at,
    source_rows,
    target_rows
FROM audit.incremental_demo_runs
WHERE status = 'SUCCESS'
ORDER BY run_id DESC
LIMIT 1;
