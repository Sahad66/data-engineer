-- Day 9 Module 5 Part 18
-- Source -> Staging -> Warehouse

CREATE TABLE IF NOT EXISTS ecommerce_dw.raw_orders (
    order_id INTEGER,
    customer_id VARCHAR(30),
    customer_name VARCHAR(100),
    city VARCHAR(100),
    product_id VARCHAR(30),
    product_name VARCHAR(100),
    category VARCHAR(50),
    order_date DATE,
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
-- Duplicate order 5001 is intentionally included.
-- Invalid quantity 0 is intentionally included.

INSERT INTO ecommerce_dw.raw_orders
    (order_id, customer_id, customer_name, city,
     product_id, product_name, category,
     order_date, quantity, unit_price)
VALUES
    (5001, 'C101', 'Rahim', 'Dhaka',
     'P101', 'Keyboard', 'Electronics',
     '2026-10-01', 2, 1500.00),

    (5002, 'C102', 'Karim', 'Chattogram',
     'P102', 'Mouse', 'Electronics',
     '2026-10-02', 3, 500.00),

    (5003, 'C103', 'Nila', 'Rajshahi',
     'P103', 'Notebook', 'Stationery',
     '2026-10-03', 5, 100.00),

    (5004, 'C101', 'Rahim', 'Dhaka',
     'P104', 'Monitor', 'Electronics',
     '2026-10-04', 1, 12000.00),

    (5001, 'C101', 'Rahim', 'Dhaka',
     'P101', 'Keyboard', 'Electronics',
     '2026-10-01', 2, 1500.00),

    (5005, 'C104', 'Sadia', 'Khulna',
     'P105', 'USB Cable', 'Accessories',
     '2026-10-05', 0, 250.00);


-- Product dimension
INSERT INTO ecommerce_dw.dim_product
    (product_id, product_name, category)
SELECT DISTINCT
    product_id, product_name, category
FROM ecommerce_dw.raw_orders
WHERE NULLIF(TRIM(product_id), '') IS NOT NULL
  AND NULLIF(TRIM(product_name), '') IS NOT NULL
  AND NULLIF(TRIM(category), '') IS NOT NULL
ON CONFLICT (product_id)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category;

-- Customer dimension
INSERT INTO ecommerce_dw.dim_customer
    (customer_id, customer_name, city)
SELECT DISTINCT
    customer_id, customer_name, city
FROM ecommerce_dw.raw_orders
WHERE NULLIF(TRIM(customer_id), '') IS NOT NULL
  AND NULLIF(TRIM(customer_name), '') IS NOT NULL
ON CONFLICT (customer_id)
DO UPDATE SET
    customer_name = EXCLUDED.customer_name,
    city = EXCLUDED.city;

-- Date dimension
INSERT INTO ecommerce_dw.dim_date
    (date_key, full_date, year, month, month_name)
SELECT DISTINCT
    TO_CHAR(order_date, 'YYYYMMDD')::INTEGER,
    order_date,
    EXTRACT(YEAR FROM order_date)::INTEGER,
    EXTRACT(MONTH FROM order_date)::INTEGER,
    TO_CHAR(order_date, 'FMMonth')
FROM ecommerce_dw.raw_orders
WHERE order_date IS NOT NULL
ON CONFLICT (date_key)
DO NOTHING;


WITH deduplicated AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY order_id, product_id
               ORDER BY loaded_at
           ) AS row_num
    FROM ecommerce_dw.raw_orders
    WHERE order_id IS NOT NULL
      AND NULLIF(TRIM(customer_id), '') IS NOT NULL
      AND NULLIF(TRIM(product_id), '') IS NOT NULL
      AND order_date IS NOT NULL
      AND quantity > 0
      AND unit_price >= 0
)
INSERT INTO ecommerce_dw.fact_sales
    (source_order_id, product_key, customer_key,
     date_key, quantity, unit_price, sales_amount)
SELECT
    r.order_id,
    p.product_key,
    c.customer_key,
    d.date_key,
    r.quantity,
    r.unit_price,
    (r.quantity * r.unit_price)::NUMERIC(14,2)
FROM deduplicated r
JOIN ecommerce_dw.dim_product p
    ON p.product_id = r.product_id
JOIN ecommerce_dw.dim_customer c
    ON c.customer_id = r.customer_id
JOIN ecommerce_dw.dim_date d
    ON d.full_date = r.order_date
WHERE r.row_num = 1
ON CONFLICT (source_order_id, product_key)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    date_key = EXCLUDED.date_key,
    quantity = EXCLUDED.quantity,
    unit_price = EXCLUDED.unit_price,
    sales_amount = EXCLUDED.sales_amount;


SELECT
    source_order_id,
    quantity,
    unit_price,
    sales_amount
FROM ecommerce_dw.fact_sales
ORDER BY source_order_id;

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


SELECT
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS revenue
FROM ecommerce_dw.fact_sales f
JOIN ecommerce_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;


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