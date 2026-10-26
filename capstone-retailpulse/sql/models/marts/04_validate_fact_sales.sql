-- Check 1: Staging vs fact row counts
SELECT
    (SELECT COUNT(*) FROM staging.orders) AS staging_orders,
    (SELECT COUNT(*) FROM marts.fact_sales) AS fact_sales_rows;


-- Check 2: Missing customer/product references
SELECT
    f.order_id,
    f.customer_id,
    f.product_id
FROM marts.fact_sales AS f
LEFT JOIN staging.customers AS c
    ON c.customer_id = f.customer_id
LEFT JOIN staging.products AS p
    ON p.product_id = f.product_id
WHERE c.customer_id IS NULL
   OR p.product_id IS NULL;


-- Check 3: Gross sales reconciliation

SELECT
    SUM(o.quantity * p.unit_price) AS expected_gross_sales,
    (SELECT SUM(gross_order_value)
     FROM marts.fact_sales) AS actual_gross_sales
FROM staging.orders AS o
JOIN staging.products AS p
    ON p.product_id = o.product_id;

-- Check 4: Invalid sales values

SELECT *
FROM marts.fact_sales
WHERE quantity <= 0
   OR unit_price <= 0
   OR gross_order_value <= 0
   OR order_id IS NULL
   OR customer_id IS NULL
   OR product_id IS NULL;