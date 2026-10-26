-- RetailPulse Capstone
-- Phase 3 Part 10: Automated SQL Data Quality Tests

\set ON_ERROR_STOP on

-- Test 1: Fact table and reporting view row counts must match
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM marts.fact_sales)
       <> (SELECT COUNT(*) FROM marts.vw_sales_reporting)
    THEN
        RAISE EXCEPTION
            'FAIL: Fact table and reporting view row counts differ';
    END IF;

    RAISE NOTICE 'PASS: Fact/view row counts match';
END $$;


-- Test 2: Gross sales totals must match
DO $$
BEGIN
    IF (SELECT COALESCE(SUM(gross_order_value), 0)
        FROM marts.fact_sales)
       <> (SELECT COALESCE(SUM(gross_order_value), 0)
           FROM marts.vw_sales_reporting)
    THEN
        RAISE EXCEPTION
            'FAIL: Fact/view gross sales totals differ';
    END IF;

    RAISE NOTICE 'PASS: Fact/view gross sales totals match';
END $$;


-- Test 3: No invalid sales values
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM marts.fact_sales
        WHERE quantity <= 0
           OR unit_price <= 0
           OR gross_order_value <= 0
    )
    THEN
        RAISE EXCEPTION
            'FAIL: Invalid sales values found';
    END IF;

    RAISE NOTICE 'PASS: Sales values are valid';
END $$;


-- Test 4: Every fact row must match a customer and product
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM marts.fact_sales f
        LEFT JOIN staging.customers c
            ON c.customer_id = f.customer_id
        LEFT JOIN staging.products p
            ON p.product_id = f.product_id
        WHERE c.customer_id IS NULL
           OR p.product_id IS NULL
    )
    THEN
        RAISE EXCEPTION
            'FAIL: Unmatched customer or product found';
    END IF;

    RAISE NOTICE 'PASS: Customer/product references are valid';
END $$;