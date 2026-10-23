-- =====================================================
-- DAY 09 | MODULE 3 | DATA WAREHOUSE FUNDAMENTALS
-- Parts 9-12: E-commerce Data Warehouse
-- Schema: Star Schema
-- =====================================================

-- Run this file in database: day9_advanced_sql


-- =====================================================
-- STEP 1: CREATE DIMENSION TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_product (
    product_key INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    month_name VARCHAR(20),
    year_number INTEGER
);


-- =====================================================
-- STEP 2: CREATE FACT TABLE
-- Grain: one row per order and product
-- =====================================================

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    product_key INTEGER NOT NULL REFERENCES dim_product(product_key),
    customer_key INTEGER NOT NULL REFERENCES dim_customer(customer_key),
    order_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    sales_amount NUMERIC(12, 2) NOT NULL CHECK (sales_amount >= 0),
    UNIQUE (order_id, product_key)
);


-- =====================================================
-- STEP 3: INSERT PRODUCT DIMENSION DATA
-- =====================================================

INSERT INTO dim_product
    (product_key, product_name, category)
VALUES
    (101, 'Laptop', 'Electronics'),
    (102, 'Mouse', 'Accessories'),
    (103, 'Keyboard', 'Accessories'),
    (104, 'Office Chair', 'Furniture')
ON CONFLICT (product_key) DO UPDATE
SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category;


-- =====================================================
-- STEP 4: INSERT CUSTOMER DIMENSION DATA
-- =====================================================

INSERT INTO dim_customer
    (customer_key, customer_name, city)
VALUES
    (1, 'Rahim', 'Dhaka'),
    (2, 'Karim', 'Rajshahi'),
    (3, 'Nadia', 'Chattogram')
ON CONFLICT (customer_key) DO UPDATE
SET
    customer_name = EXCLUDED.customer_name,
    city = EXCLUDED.city;


-- =====================================================
-- STEP 5: INSERT DATE DIMENSION DATA
-- =====================================================

INSERT INTO dim_date
    (date_key, full_date, month_name, year_number)
VALUES
    (20261001, '2026-10-01', 'October', 2026),
    (20261002, '2026-10-02', 'October', 2026),
    (20261003, '2026-10-03', 'October', 2026),
    (20261101, '2026-11-01', 'November', 2026)
ON CONFLICT (date_key) DO UPDATE
SET
    full_date = EXCLUDED.full_date,
    month_name = EXCLUDED.month_name,
    year_number = EXCLUDED.year_number;


-- =====================================================
-- STEP 6: INSERT FACT SALES DATA
-- sales_amount = quantity * unit selling price
-- =====================================================

INSERT INTO fact_sales
    (date_key, product_key, customer_key,
     order_id, quantity, sales_amount)
VALUES
    (20261001, 101, 1, 1001, 1, 50000),
    (20261001, 102, 1, 1001, 2, 1000),
    (20261002, 103, 2, 1002, 1, 2500),
    (20261002, 104, 3, 1003, 2, 12000),
    (20261003, 101, 2, 1004, 1, 50000),
    (20261101, 102, 3, 1005, 3, 1500)
ON CONFLICT (order_id, product_key) DO UPDATE
SET
    date_key = EXCLUDED.date_key,
    customer_key = EXCLUDED.customer_key,
    quantity = EXCLUDED.quantity,
    sales_amount = EXCLUDED.sales_amount;


-- =====================================================
-- STEP 7: BUSINESS ANALYTICS QUERIES
-- =====================================================

-- Q1: Total sales, total quantity and fact rows

SELECT
    COUNT(*) AS total_order_lines,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM fact_sales;


-- Q2: Revenue by product

SELECT
    p.product_name,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales AS f
JOIN dim_product AS p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_revenue DESC;


-- Q3: Revenue by category

SELECT
    p.category,
    SUM(f.sales_amount) AS category_revenue
FROM fact_sales AS f
JOIN dim_product AS p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY category_revenue DESC;


-- Q4: Revenue by customer

SELECT
    c.customer_name,
    c.city,
    SUM(f.sales_amount) AS total_spent
FROM fact_sales AS f
JOIN dim_customer AS c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_key, c.customer_name, c.city
ORDER BY total_spent DESC;


-- Q5: Monthly sales trend

SELECT
    d.year_number,
    d.month_name,
    SUM(f.sales_amount) AS monthly_revenue
FROM fact_sales AS f
JOIN dim_date AS d
    ON f.date_key = d.date_key
GROUP BY d.year_number, d.month_name
ORDER BY d.year_number, MIN(d.full_date);


-- =====================================================
-- STEP 8: DATA QUALITY VALIDATION
-- =====================================================

-- Fact row count: expected 6

SELECT COUNT(*) AS fact_rows
FROM fact_sales;


-- Expected total sales: 117000

SELECT
    SUM(sales_amount) AS total_revenue,
    SUM(quantity) AS total_quantity
FROM fact_sales;


-- Check whether any dimension reference is missing.
-- Expected: 0 rows

SELECT f.*
FROM fact_sales AS f
LEFT JOIN dim_product AS p
    ON f.product_key = p.product_key
LEFT JOIN dim_customer AS c
    ON f.customer_key = c.customer_key
LEFT JOIN dim_date AS d
    ON f.date_key = d.date_key
WHERE p.product_key IS NULL
   OR c.customer_key IS NULL
   OR d.date_key IS NULL;


-- =====================================================
-- QUICK REVISION
-- OLTP = operational transactions
-- OLAP = analytical queries
-- Fact = business measurements
-- Dimension = descriptive business context
-- Star Schema = fact surrounded by dimensions
-- Grain = what one fact row represents
-- =====================================================