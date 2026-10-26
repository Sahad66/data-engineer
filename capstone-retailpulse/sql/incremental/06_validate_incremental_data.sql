-- RetailPulse Phase 4 - Part 9
-- Incremental Data Quality and Reconciliation

-- Check 1: Compare source and target row counts
SELECT
    (SELECT COUNT(*)
     FROM audit.incremental_demo_source) AS source_rows,

    (SELECT COUNT(*)
     FROM audit.incremental_demo_target) AS target_rows;

-- Check 2: Find source orders missing from target
SELECT s.order_id
FROM audit.incremental_demo_source AS s
LEFT JOIN audit.incremental_demo_target AS t
    ON t.order_id = s.order_id
WHERE t.order_id IS NULL;

-- Check 3: Find amount or timestamp mismatches
SELECT
    s.order_id,
    s.amount AS source_amount,
    t.amount AS target_amount,
    s.updated_at AS source_updated_at,
    t.updated_at AS target_updated_at
FROM audit.incremental_demo_source AS s
JOIN audit.incremental_demo_target AS t
    ON t.order_id = s.order_id
WHERE s.amount IS DISTINCT FROM t.amount
   OR s.updated_at IS DISTINCT FROM t.updated_at;

-- Check 4: Detect duplicate order IDs in target
SELECT order_id, COUNT(*) AS row_count
FROM audit.incremental_demo_target
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Check 5: Find invalid amounts
SELECT *
FROM audit.incremental_demo_target
WHERE amount <= 0;