
/*
==========================================================
DAY 9 - MODULE 1: ADVANCED SQL
Parts 1-4 | Practice & Revision Notes
Database: day9_advanced_sql
==========================================================

PART 1: SQL REVISION
PART 2: CTE
PART 3: SUBQUERIES
PART 4: VIEWS & MATERIALIZED VIEWS
*/


-- ======================================================
-- PART 1: SQL REVISION
-- ======================================================

-- Query 1: Display all sales
SELECT *
FROM sales;


-- Query 2: Select specific columns
SELECT product, unit_price
FROM sales;


-- Query 3: Filter Electronics products
SELECT *
FROM sales
WHERE category = 'Electronics';


-- Query 4: Count records in each category
SELECT
    category,
    COUNT(*) AS total_records
FROM sales
GROUP BY category;


-- Query 5: Show categories with at least 2 records
SELECT
    category,
    COUNT(*) AS total_records
FROM sales
GROUP BY category
HAVING COUNT(*) >= 2;


-- Query 6: Calculate category-wise revenue
SELECT
    category,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;


-- ======================================================
-- PART 2: CTE (COMMON TABLE EXPRESSION)
-- ======================================================

-- Query 7: Calculate revenue using a CTE
WITH category_sales AS (
    SELECT
        category,
        SUM(quantity * unit_price) AS total_revenue
    FROM sales
    GROUP BY category
)
SELECT category, total_revenue
FROM category_sales
ORDER BY total_revenue DESC;


-- Query 8: Filter CTE results
WITH category_sales AS (
    SELECT
        category,
        SUM(quantity * unit_price) AS total_revenue
    FROM sales
    GROUP BY category
)
SELECT *
FROM category_sales
WHERE total_revenue > 20000;


-- ======================================================
-- PART 3: SUBQUERIES
-- ======================================================

-- Query 9: Find products above the overall average price
SELECT product, unit_price
FROM sales
WHERE unit_price > (
    SELECT AVG(unit_price)
    FROM sales
);


-- Query 10: Find products above their category average
-- This is a correlated subquery
SELECT
    s.product,
    s.category,
    s.unit_price
FROM sales AS s
WHERE s.unit_price > (
    SELECT AVG(s2.unit_price)
    FROM sales AS s2
    WHERE s2.category = s.category
);


-- Query 11: Find the most expensive product
SELECT product, unit_price
FROM sales
WHERE unit_price = (
    SELECT MAX(unit_price)
    FROM sales
);


-- ======================================================
-- PART 4: VIEWS
-- ======================================================

-- Query 12: Create a reusable sales summary view
CREATE OR REPLACE VIEW sales_summary AS
SELECT
    category,
    SUM(quantity) AS total_quantity,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY category;


-- Query 13: Read the view
SELECT *
FROM sales_summary
ORDER BY total_revenue DESC;


-- Query 14: Filter the view
SELECT *
FROM sales_summary
WHERE total_revenue > 5000;


-- ======================================================
-- PART 4: MATERIALIZED VIEWS
-- ======================================================

-- Query 15: Create a stored result snapshot
-- DROP is used here to make this practice section rerunnable.
DROP MATERIALIZED VIEW IF EXISTS category_sales_snapshot;

CREATE MATERIALIZED VIEW category_sales_snapshot AS
SELECT
    category,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY category;


-- Query 16: Read the materialized view
SELECT *
FROM category_sales_snapshot
ORDER BY total_revenue DESC;


-- Query 17: Add a new sale for the refresh demonstration
-- If sale_id 7 already exists, it will not be inserted again.
INSERT INTO sales
    (sale_id, product, category, quantity, unit_price)
VALUES
    (7, 'Monitor', 'Electronics', 1, 15000)
ON CONFLICT (sale_id) DO NOTHING;


-- Query 18: Refresh the stored snapshot
REFRESH MATERIALIZED VIEW category_sales_snapshot;


-- Query 19: Compare the current view and snapshot
SELECT *
FROM sales_summary
WHERE category = 'Electronics';

SELECT *
FROM category_sales_snapshot
WHERE category = 'Electronics';


-- ======================================================
-- END OF DAY 9 MODULE 1 NOTES
-- ======================================================
