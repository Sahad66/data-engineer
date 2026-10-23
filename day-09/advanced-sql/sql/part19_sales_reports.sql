--Report 1: Overall business KPI
SELECT
    COUNT(DISTINCT source_order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    COALESCE(SUM(sales_amount), 0) AS total_revenue,
    ROUND(
        COALESCE(SUM(sales_amount), 0)
        / NULLIF(COUNT(DISTINCT source_order_id), 0),
        2
    ) AS average_order_value
FROM ecommerce_dw.fact_sales;

--Report 2: Category-wise revenue
SELECT
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS revenue
FROM ecommerce_dw.fact_sales f
JOIN ecommerce_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;


--Report 3: Top-selling products
SELECT
    p.product_name,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS revenue
FROM ecommerce_dw.fact_sales f
JOIN ecommerce_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY units_sold DESC, revenue DESC
LIMIT 5;

--Report 4: Monthly sales trend
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.sales_amount) AS monthly_revenue,
    COUNT(DISTINCT f.source_order_id) AS total_orders
FROM ecommerce_dw.fact_sales f
JOIN ecommerce_dw.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


--Report 5: Customer-wise revenue
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(DISTINCT f.source_order_id) AS total_orders,
    SUM(f.sales_amount) AS total_spent
FROM ecommerce_dw.fact_sales f
JOIN ecommerce_dw.dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC;