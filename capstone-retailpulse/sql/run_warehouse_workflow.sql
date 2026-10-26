
-- RetailPulse Capstone
-- Phase 2 Part 9: Integrated Warehouse Workflow

\set ON_ERROR_STOP on

BEGIN;

-- 1. Reload staging tables
TRUNCATE TABLE
    staging.payments,
    staging.orders,
    staging.products,
    staging.customers;

INSERT INTO staging.customers
    (customer_id, customer_name, city)
SELECT
    TRIM(customer_id),
    TRIM(customer_name),
    NULLIF(TRIM(city), '')
FROM raw.customers;

INSERT INTO staging.products
    (product_id, product_name, category, unit_price)
SELECT
    TRIM(product_id),
    TRIM(product_name),
    NULLIF(TRIM(category), ''),
    unit_price
FROM raw.products;

INSERT INTO staging.orders
    (order_id, customer_id, order_date, product_id, quantity)
SELECT
    TRIM(order_id),
    TRIM(customer_id),
    order_date,
    TRIM(product_id),
    quantity
FROM raw.orders;

INSERT INTO staging.payments
    (payment_id, order_id, payment_method, payment_status, amount)
SELECT
    TRIM(payment_id),
    TRIM(order_id),
    LOWER(NULLIF(TRIM(payment_method), '')),
    LOWER(TRIM(payment_status)),
    amount
FROM raw.payments;

-- 2. Validate data before recording success
DO $$
BEGIN
    -- Source and target counts must match
    IF (SELECT COUNT(*) FROM raw.customers)
       <> (SELECT COUNT(*) FROM staging.customers)
    OR (SELECT COUNT(*) FROM raw.products)
       <> (SELECT COUNT(*) FROM staging.products)
    OR (SELECT COUNT(*) FROM raw.orders)
       <> (SELECT COUNT(*) FROM staging.orders)
    OR (SELECT COUNT(*) FROM raw.payments)
       <> (SELECT COUNT(*) FROM staging.payments)
    THEN
        RAISE EXCEPTION 'Source/staging row count mismatch';
    END IF;

    -- Required text fields
    IF EXISTS (
        SELECT 1 FROM staging.customers
        WHERE customer_name IS NULL OR TRIM(customer_name) = ''
    ) OR EXISTS (
        SELECT 1 FROM staging.products
        WHERE product_name IS NULL OR TRIM(product_name) = ''
    ) OR EXISTS (
        SELECT 1 FROM staging.payments
        WHERE payment_status IS NULL OR TRIM(payment_status) = ''
    ) THEN
        RAISE EXCEPTION 'Required field validation failed';
    END IF;

    -- Numeric quality
    IF EXISTS (
        SELECT 1 FROM staging.orders WHERE quantity <= 0
    ) OR EXISTS (
        SELECT 1 FROM staging.products WHERE unit_price <= 0
    ) OR EXISTS (
        SELECT 1 FROM staging.payments WHERE amount <= 0
    ) THEN
        RAISE EXCEPTION 'Invalid numeric values found';
    END IF;

    -- Referential integrity
    IF EXISTS (
        SELECT 1
        FROM staging.orders o
        LEFT JOIN staging.customers c
            ON c.customer_id = o.customer_id
        WHERE c.customer_id IS NULL
    ) OR EXISTS (
        SELECT 1
        FROM staging.orders o
        LEFT JOIN staging.products p
            ON p.product_id = o.product_id
        WHERE p.product_id IS NULL
    ) OR EXISTS (
        SELECT 1
        FROM staging.payments pay
        LEFT JOIN staging.orders o
            ON o.order_id = pay.order_id
        WHERE o.order_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Referential integrity validation failed';
    END IF;
END $$;

-- 3. Record successful workflow in audit table
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
    'retailpulse_warehouse_workflow',
    statement_timestamp(),
    clock_timestamp(),
    'SUCCESS',
    source_rows,
    target_rows,
    'Staging reload and configured quality checks passed.'
FROM row_counts;

COMMIT;
