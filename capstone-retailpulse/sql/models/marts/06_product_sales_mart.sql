-- RetailPulse Capstone
-- Phase 3 Part 6: Product Performance Data Mart

CREATE TABLE IF NOT EXISTS marts.product_sales_summary (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    unit_price NUMERIC(12, 2) NOT NULL,
    total_orders BIGINT NOT NULL,
    total_units_sold BIGINT NOT NULL,
    gross_sales NUMERIC(14, 2) NOT NULL
);

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
    COUNT(DISTINCT f.order_id) AS total_orders,
    COALESCE(SUM(f.quantity), 0) AS total_units_sold,
    COALESCE(SUM(f.gross_order_value), 0) AS gross_sales
FROM staging.products AS p
LEFT JOIN marts.fact_sales AS f
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price
ON CONFLICT (product_id) DO UPDATE
SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    unit_price = EXCLUDED.unit_price,
    total_orders = EXCLUDED.total_orders,
    total_units_sold = EXCLUDED.total_units_sold,
    gross_sales = EXCLUDED.gross_sales;