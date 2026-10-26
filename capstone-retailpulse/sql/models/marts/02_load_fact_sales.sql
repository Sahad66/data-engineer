-- Load sales facts from staging tables
-- Current source grain: one row per order

BEGIN;

INSERT INTO marts.fact_sales (
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price
)
SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.quantity,
    p.unit_price
FROM staging.orders AS o
JOIN staging.products AS p
    ON p.product_id = o.product_id
ON CONFLICT (order_id) DO UPDATE
SET
    customer_id = EXCLUDED.customer_id,
    product_id = EXCLUDED.product_id,
    order_date = EXCLUDED.order_date,
    quantity = EXCLUDED.quantity,
    unit_price = EXCLUDED.unit_price;

COMMIT;