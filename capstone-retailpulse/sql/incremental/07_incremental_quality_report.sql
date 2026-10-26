SELECT
    'Row count reconciliation' AS check_name,
    CASE
        WHEN (SELECT COUNT(*) FROM audit.incremental_demo_source)
           = (SELECT COUNT(*) FROM audit.incremental_demo_target)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS result

UNION ALL

SELECT
    'Missing source orders',
    CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM audit.incremental_demo_source s
            LEFT JOIN audit.incremental_demo_target t
                ON t.order_id = s.order_id
            WHERE t.order_id IS NULL
        )
        THEN 'PASS'
        ELSE 'FAIL'
    END

UNION ALL

SELECT
    'Source-target value consistency',
    CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM audit.incremental_demo_source s
            JOIN audit.incremental_demo_target t
                ON t.order_id = s.order_id
            WHERE s.amount IS DISTINCT FROM t.amount
               OR s.updated_at IS DISTINCT FROM t.updated_at
        )
        THEN 'PASS'
        ELSE 'FAIL'
    END

UNION ALL

SELECT
    'Duplicate order IDs',
    CASE
        WHEN NOT EXISTS (
            SELECT order_id
            FROM audit.incremental_demo_target
            GROUP BY order_id
            HAVING COUNT(*) > 1
        )
        THEN 'PASS'
        ELSE 'FAIL'
    END

UNION ALL

SELECT
    'Invalid amounts',
    CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM audit.incremental_demo_target
            WHERE amount <= 0
        )
        THEN 'PASS'
        ELSE 'FAIL'
    END;