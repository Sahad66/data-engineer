
BEGIN;

DROP TABLE IF EXISTS ecommerce_orders_clean;

CREATE TABLE ecommerce_orders_clean AS
WITH ranked_orders AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY order_date, customer_id
        ) AS row_num
    FROM ecommerce_orders_raw_backup
)
SELECT
    order_id,
    customer_id,
    order_date,
    product,
    quantity,
    unit_price,
    status
FROM ranked_orders
WHERE row_num = 1
  AND customer_id IS NOT NULL
  AND TRIM(customer_id) <> ''
  AND quantity > 0;

COMMIT;


