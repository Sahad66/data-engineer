-- RetailPulse Capstone
-- Phase 3 Part 9: Reusable Sales Reporting View

CREATE OR REPLACE VIEW marts.vw_sales_reporting AS
SELECT
    f.order_id,
    f.order_date,
    f.customer_id,
    c.customer_name,
    c.city,
    f.product_id,
    p.product_name,
    p.category,
    f.quantity,
    f.unit_price,
    f.gross_order_value
FROM marts.fact_sales AS f
JOIN staging.customers AS c
    ON c.customer_id = f.customer_id
JOIN staging.products AS p
    ON p.product_id = f.product_id;