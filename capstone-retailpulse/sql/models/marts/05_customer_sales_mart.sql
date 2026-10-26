-- RetailPulse Capstone
-- Phase 3 Part 5: Customer Sales Data Mart

CREATE TABLE IF NOT EXISTS marts.customer_sales_summary (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT,
    total_orders BIGINT NOT NULL,
    total_units_sold BIGINT NOT NULL,
    gross_sales NUMERIC(14, 2) NOT NULL
);

--Customer summary load

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
    COUNT(DISTINCT f.order_id) AS total_orders,
    COALESCE(SUM(f.quantity), 0) AS total_units_sold,
    COALESCE(SUM(f.gross_order_value), 0) AS gross_sales
FROM staging.customers AS c
LEFT JOIN marts.fact_sales AS f
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ON CONFLICT (customer_id) DO UPDATE
SET
    customer_name = EXCLUDED.customer_name,
    city = EXCLUDED.city,
    total_orders = EXCLUDED.total_orders,
    total_units_sold = EXCLUDED.total_units_sold,
    gross_sales = EXCLUDED.gross_sales;