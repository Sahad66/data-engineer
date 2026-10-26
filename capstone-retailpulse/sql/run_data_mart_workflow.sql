-- RetailPulse Capstone
-- Phase 3 Part 11: Integrated Data Mart Workflow

\set ON_ERROR_STOP on

BEGIN;

-- 1. Refresh customer sales summary
INSERT INTO marts.customer_sales_summary (
    customer_id,
    customer_name,
    city,
    total_orders,
    total_units_sold,
    gross_sales
)
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT f.order_id),
    COALESCE(SUM(f.quantity), 0),
    COALESCE(SUM(f.gross_order_value), 0)
FROM staging.customers c
LEFT JOIN marts.fact_sales f
    ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ON CONFLICT (customer_id) DO UPDATE
SET
    customer_name = EXCLUDED.customer_name,
    city = EXCLUDED.city,
    total_orders = EXCLUDED.total_orders,
    total_units_sold = EXCLUDED.total_units_sold,
    gross_sales = EXCLUDED.gross_sales;

-- 2. Refresh product sales summary
INSERT INTO marts.product_sales_summary (
    product_id,
    product_name,
    category,
    unit_price,
    total_orders,
    total_units_sold,
    gross_sales
)
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    COUNT(DISTINCT f.order_id),
    COALESCE(SUM(f.quantity), 0),
    COALESCE(SUM(f.gross_order_value), 0)
FROM staging.products p
LEFT JOIN marts.fact_sales f
    ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.unit_price
ON CONFLICT (product_id) DO UPDATE
SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    unit_price = EXCLUDED.unit_price,
    total_orders = EXCLUDED.total_orders,
    total_units_sold = EXCLUDED.total_units_sold,
    gross_sales = EXCLUDED.gross_sales;

-- 3. Refresh payment summary
INSERT INTO marts.payment_summary (
    payment_method,
    total_payments,
    paid_payments,
    pending_payments,
    paid_amount,
    pending_amount
)
SELECT
    COALESCE(payment_method, 'unknown'),
    COUNT(*),
    COUNT(*) FILTER (
        WHERE LOWER(payment_status) = 'paid'
    ),
    COUNT(*) FILTER (
        WHERE LOWER(payment_status) = 'pending'
    ),
    COALESCE(SUM(amount) FILTER (
        WHERE LOWER(payment_status) = 'paid'
    ), 0),
    COALESCE(SUM(amount) FILTER (
        WHERE LOWER(payment_status) = 'pending'
    ), 0)
FROM staging.payments
GROUP BY COALESCE(payment_method, 'unknown')
ON CONFLICT (payment_method) DO UPDATE
SET
    total_payments = EXCLUDED.total_payments,
    paid_payments = EXCLUDED.paid_payments,
    pending_payments = EXCLUDED.pending_payments,
    paid_amount = EXCLUDED.paid_amount,
    pending_amount = EXCLUDED.pending_amount;

-- 4. Validate source-to-mart customer coverage
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM staging.customers)
       <> (SELECT COUNT(*) FROM marts.customer_sales_summary)
    THEN
        RAISE EXCEPTION 'Customer mart row count mismatch';
    END IF;

    IF (SELECT COUNT(*) FROM staging.products)
       <> (SELECT COUNT(*) FROM marts.product_sales_summary)
    THEN
        RAISE EXCEPTION 'Product mart row count mismatch';
    END IF;

    IF (SELECT COUNT(*) FROM staging.payments)
       <> (SELECT COALESCE(SUM(total_payments), 0)
           FROM marts.payment_summary)
    THEN
        RAISE EXCEPTION 'Payment mart count mismatch';
    END IF;

    RAISE NOTICE 'PASS: Customer, product and payment marts validated';
END $$;

-- 5. Validate sales totals across fact and summary marts
DO $$
BEGIN
    IF (SELECT COALESCE(SUM(gross_order_value), 0)
        FROM marts.fact_sales)
       <> (SELECT COALESCE(SUM(gross_sales), 0)
           FROM marts.customer_sales_summary)
    THEN
        RAISE EXCEPTION 'Customer mart sales total mismatch';
    END IF;

    IF (SELECT COALESCE(SUM(gross_order_value), 0)
        FROM marts.fact_sales)
       <> (SELECT COALESCE(SUM(gross_sales), 0)
           FROM marts.product_sales_summary)
    THEN
        RAISE EXCEPTION 'Product mart sales total mismatch';
    END IF;

    RAISE NOTICE 'PASS: Sales totals reconciled';
END $$;

COMMIT;