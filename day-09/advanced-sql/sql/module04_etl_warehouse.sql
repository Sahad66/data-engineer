# Day 9 — Module 4: ETL & Data Warehouse Integration
## Parts 13–16 | Complete SQL Practice Notes

```sql
/*
==========================================================
DAY 9 - MODULE 4: ETL & DATA WAREHOUSE INTEGRATION
PART 13: Raw, Staging and Warehouse Layers
PART 14: Data Types and Schema Design
PART 15: Incremental Loading and Watermark
PART 16: Data Quality Checks
Database: day9_advanced_sql
==========================================================
*/

-- ========================================================
-- PART 13: RAW, STAGING AND WAREHOUSE LAYERS
-- Raw = original source data
-- Staging = validated and typed data
-- Warehouse = clean data for reporting
-- ========================================================

-- Practice schema তৈরি করো।
CREATE SCHEMA IF NOT EXISTS etl_practice;

-- Raw table: source data TEXT হিসেবে রাখবে।
-- এতে invalid date বা amount-ও audit করা যায়।
CREATE TABLE IF NOT EXISTS etl_practice.raw_orders (
    source_order_id TEXT,
    customer_id TEXT,
    order_date TEXT,
    amount TEXT,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- চারটি sample record যোগ করো।
-- 1003-এ customer ID missing।
-- 1004-এ order date invalid।
INSERT INTO etl_practice.raw_orders
    (source_order_id, customer_id, order_date, amount)
SELECT v.source_order_id, v.customer_id, v.order_date, v.amount
FROM (VALUES
    ('1001', '1', '2026-10-01', '2500.00'),
    ('1002', '2', '2026-10-02', '4000.00'),
    ('1003', '',  '2026-10-03', '1500.00'),
    ('1004', '4', 'invalid-date', '900.00')
) AS v(source_order_id, customer_id, order_date, amount)
WHERE NOT EXISTS (
    SELECT 1
    FROM etl_practice.raw_orders r
    WHERE r.source_order_id = v.source_order_id
);

-- Raw data দেখো।
SELECT *
FROM etl_practice.raw_orders
ORDER BY source_order_id;


-- Staging table: সঠিক data type ও constraints।
CREATE TABLE IF NOT EXISTS etl_practice.stg_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- শুধু valid data Raw থেকে Staging-এ load করো।
-- pg_input_is_valid() type conversion সম্ভব কি না যাচাই করে।
-- Missing customer, invalid date, invalid amount বাদ পড়ে।
INSERT INTO etl_practice.stg_orders
    (order_id, customer_id, order_date, amount)
SELECT
    source_order_id::INTEGER,
    NULLIF(TRIM(customer_id), '')::INTEGER,
    order_date::DATE,
    amount::NUMERIC(12,2)
FROM etl_practice.raw_orders
WHERE pg_input_is_valid(source_order_id, 'integer')
  AND NULLIF(TRIM(customer_id), '') IS NOT NULL
  AND pg_input_is_valid(NULLIF(TRIM(customer_id), ''), 'integer')
  AND pg_input_is_valid(order_date, 'date')
  AND pg_input_is_valid(amount, 'numeric')
  AND amount::NUMERIC >= 0
ON CONFLICT (order_id) DO NOTHING;

-- Expected: 2 valid rows।
SELECT *
FROM etl_practice.stg_orders
ORDER BY order_id;


-- Warehouse fact table তৈরি করো।
CREATE TABLE IF NOT EXISTS etl_practice.fact_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Staging থেকে Warehouse-এ load করো।
-- একই order ID থাকলে existing values update হবে।
INSERT INTO etl_practice.fact_orders
    (order_id, customer_id, order_date, amount)
SELECT order_id, customer_id, order_date, amount
FROM etl_practice.stg_orders
ON CONFLICT (order_id) DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    order_date = EXCLUDED.order_date,
    amount = EXCLUDED.amount,
    loaded_at = CURRENT_TIMESTAMP;

-- Expected: 2 orders এবং total amount 6500.00।
SELECT
    COUNT(*) AS total_orders,
    COALESCE(SUM(amount), 0) AS total_amount
FROM etl_practice.fact_orders;


-- ========================================================
-- PART 14: DATA TYPES AND SCHEMA DESIGN
-- INTEGER = ID
-- DATE = date
-- NUMERIC = exact monetary value
-- TIMESTAMPTZ = timezone-aware timestamp
-- ========================================================

CREATE TABLE IF NOT EXISTS etl_practice.order_schema_demo (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sample data insert করো।
-- Duplicate primary key থাকলে row skip হবে।
INSERT INTO etl_practice.order_schema_demo
    (order_id, customer_id, order_date, amount, status)
VALUES
    (2001, 101, DATE '2026-10-01', 2500.00, 'completed'),
    (2002, 102, DATE '2026-10-02', 4500.50, 'pending'),
    (2003, 103, DATE '2026-10-03', 1200.00, 'cancelled')
ON CONFLICT (order_id) DO NOTHING;

-- Data verify করো।
SELECT *
FROM etl_practice.order_schema_demo
ORDER BY order_id;

-- Table-এর actual column types দেখো।
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'etl_practice'
  AND table_name = 'order_schema_demo'
ORDER BY ordinal_position;


-- ========================================================
-- PART 15: INCREMENTAL LOADING AND WATERMARK
-- Incremental loading = নতুন/পরিবর্তিত data load করা।
-- Watermark = শেষ processed timestamp।
-- ========================================================

-- Source table।
CREATE TABLE IF NOT EXISTS etl_practice.incremental_source (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Target table।
CREATE TABLE IF NOT EXISTS etl_practice.incremental_target (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    updated_at TIMESTAMPTZ NOT NULL
);

-- Watermark table।
CREATE TABLE IF NOT EXISTS etl_practice.etl_watermark (
    pipeline_name TEXT PRIMARY KEY,
    last_loaded_at TIMESTAMPTZ NOT NULL
);

-- প্রথমবারের জন্য পুরোনো watermark সেট করো।
-- আগে থেকে থাকলে existing watermark reset হবে না।
INSERT INTO etl_practice.etl_watermark
    (pipeline_name, last_loaded_at)
VALUES
    ('orders_pipeline', TIMESTAMPTZ '2000-01-01 00:00:00+00')
ON CONFLICT (pipeline_name) DO NOTHING;

-- Demo source records।
INSERT INTO etl_practice.incremental_source
    (order_id, customer_id, order_date, amount, updated_at)
VALUES
    (3001, 201, DATE '2026-10-10', 3500.00,
     TIMESTAMPTZ '2026-10-10 10:00:00+00'),
    (3002, 202, DATE '2026-10-11', 5200.00,
     TIMESTAMPTZ '2026-10-11 10:00:00+00')
ON CONFLICT (order_id) DO NOTHING;

-- Incremental load transaction:
-- 1. Current watermark পড়বে।
-- 2. Watermark-এর পরের records খুঁজবে।
-- 3. Target table-এ upsert করবে।
-- 4. Successful load-এর timestamp দিয়ে watermark update করবে।
BEGIN;

WITH current_watermark AS (
    SELECT last_loaded_at
    FROM etl_practice.etl_watermark
    WHERE pipeline_name = 'orders_pipeline'
),
new_rows AS (
    SELECT s.*
    FROM etl_practice.incremental_source s
    CROSS JOIN current_watermark w
    WHERE s.updated_at > w.last_loaded_at
),
loaded_rows AS (
    INSERT INTO etl_practice.incremental_target
        (order_id, customer_id, order_date, amount, updated_at)
    SELECT
        order_id, customer_id, order_date, amount, updated_at
    FROM new_rows
    ON CONFLICT (order_id) DO UPDATE SET
        customer_id = EXCLUDED.customer_id,
        order_date = EXCLUDED.order_date,
        amount = EXCLUDED.amount,
        updated_at = EXCLUDED.updated_at
    RETURNING updated_at
)
UPDATE etl_practice.etl_watermark
SET last_loaded_at = GREATEST(
    last_loaded_at,
    COALESCE(
        (SELECT MAX(updated_at) FROM loaded_rows),
        last_loaded_at
    )
)
WHERE pipeline_name = 'orders_pipeline';

COMMIT;

-- Target-এর records দেখো।
SELECT *
FROM etl_practice.incremental_target
ORDER BY order_id;

-- Watermark check করো।
SELECT *
FROM etl_practice.etl_watermark
WHERE pipeline_name = 'orders_pipeline';


-- ========================================================
-- PART 16: SQL DATA QUALITY CHECKS
-- Missing values, invalid types, duplicates, negative values,
-- row counts, totals এবং dimension keys validate করো।
-- ========================================================

-- 16.1 Raw data quality issues শনাক্ত করো।
SELECT
    source_order_id,
    customer_id,
    order_date,
    amount,
    CASE
        WHEN NULLIF(TRIM(source_order_id), '') IS NULL
            THEN 'Missing Order ID'
        WHEN NOT pg_input_is_valid(source_order_id, 'integer')
            THEN 'Invalid Order ID'
        WHEN NULLIF(TRIM(customer_id), '') IS NULL
            THEN 'Missing Customer ID'
        WHEN NOT pg_input_is_valid(
            NULLIF(TRIM(customer_id), ''), 'integer'
        )
            THEN 'Invalid Customer ID'
        WHEN NOT pg_input_is_valid(order_date, 'date')
            THEN 'Invalid Order Date'
        WHEN NOT pg_input_is_valid(amount, 'numeric')
            THEN 'Invalid Amount'
        WHEN amount::NUMERIC < 0
            THEN 'Negative Amount'
        ELSE 'No Issue'
    END AS quality_issue
FROM etl_practice.raw_orders
ORDER BY source_order_id;


-- 16.2 Duplicate order IDs খুঁজে বের করো।
-- 0 rows = duplicate পাওয়া যায়নি।
SELECT
    source_order_id,
    COUNT(*) AS duplicate_count
FROM etl_practice.raw_orders
GROUP BY source_order_id
HAVING COUNT(*) > 1;


-- 16.3 Staging table-এ NULL বা negative amount check করো।
-- 0 rows = এই checks pass করেছে।
SELECT *
FROM etl_practice.stg_orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR order_date IS NULL
   OR amount IS NULL
   OR amount < 0;


-- 16.4 Warehouse table-এ NULL বা negative amount check করো।
SELECT *
FROM etl_practice.fact_orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR order_date IS NULL
   OR amount IS NULL
   OR amount < 0;


-- 16.5 Staging বনাম Warehouse row count compare করো।
SELECT
    (SELECT COUNT(*) FROM etl_practice.stg_orders) AS staging_rows,
    (SELECT COUNT(*) FROM etl_practice.fact_orders) AS warehouse_rows;


-- 16.6 Staging বনাম Warehouse total amount compare করো।
-- একই records load হলে row count ও total amount মিলবে।
SELECT
    'staging' AS layer,
    COUNT(*) AS total_orders,
    COALESCE(SUM(amount), 0) AS total_amount
FROM etl_practice.stg_orders

UNION ALL

SELECT
    'warehouse' AS layer,
    COUNT(*) AS total_orders,
    COALESCE(SUM(amount), 0) AS total_amount
FROM etl_practice.fact_orders;


-- 16.7 Day 9 Module 3 Warehouse dimension-key check।
-- fact_sales ও dimension tables public schema-তে আছে।
-- 0 rows = unmatched dimension keys পাওয়া যায়নি।
SELECT f.*
FROM public.fact_sales f
LEFT JOIN public.dim_product p
    ON f.product_key = p.product_key
LEFT JOIN public.dim_customer c
    ON f.customer_key = c.customer_key
LEFT JOIN public.dim_date d
    ON f.date_key = d.date_key
WHERE p.product_key IS NULL
   OR c.customer_key IS NULL
   OR d.date_key IS NULL;


-- 16.8 Final audit summary: প্রতিটি table-এর row count।
SELECT 'raw_orders' AS table_name, COUNT(*) AS total_rows
FROM etl_practice.raw_orders

UNION ALL

SELECT 'stg_orders', COUNT(*)
FROM etl_practice.stg_orders

UNION ALL

SELECT 'fact_orders', COUNT(*)
FROM etl_practice.fact_orders

UNION ALL

SELECT 'incremental_target', COUNT(*)
FROM etl_practice.incremental_target
ORDER BY table_name;


/*
==========================================================
QUICK REVISION
Raw       = original source data
Staging   = validated and typed data
Warehouse = analytics-ready data
Incremental load = new/changed data load
Watermark = last processed timestamp
Data quality = null/type/duplicate/range/count/total checks
==========================================================
END OF DAY 9 MODULE 4 (PARTS 13-16)
*/
```

