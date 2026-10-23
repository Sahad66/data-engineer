--Check 1: Duplicate business keys
SELECT source_order_id, product_key, COUNT(*) AS duplicate_count
FROM ecommerce_dw.fact_sales
GROUP BY source_order_id, product_key
HAVING COUNT(*) > 1;

--Check 2: Invalid quantity or amount
SELECT *
FROM ecommerce_dw.fact_sales
WHERE quantity <= 0
OR unit_price < 0
OR sales_amount < 0;



--Check 3: Foreign-key relationship validation
SELECT f.*
FROM ecommerce_dw.fact_sales f
LEFT JOIN ecommerce_dw.dim_product p
    ON f.product_key = p.product_key
LEFT JOIN ecommerce_dw.dim_customer c
    ON f.customer_key = c.customer_key
LEFT JOIN ecommerce_dw.dim_date d
    ON f.date_key = d.date_key
WHERE p.product_key IS NULL
   OR c.customer_key IS NULL
   OR d.date_key IS NULL;


--Check 4: Revenue reconciliation
SELECT
    SUM(sales_amount) AS stored_revenue,
    SUM(quantity * unit_price) AS calculated_revenue,
    SUM(sales_amount) - SUM(quantity * unit_price) AS difference
FROM ecommerce_dw.fact_sales;



--Check 5: Raw versus warehouse counts
SELECT
    (SELECT COUNT(*) FROM ecommerce_dw.raw_orders) AS raw_rows,
    (SELECT COUNT(*) FROM ecommerce_dw.fact_sales) AS warehouse_rows,
    (SELECT COUNT(DISTINCT source_order_id)
     FROM ecommerce_dw.fact_sales) AS unique_orders;


--