-- =====================================================
-- DAY 09 | MODULE 02 | WINDOW FUNCTIONS
-- Parts 5-8: Ranking, LAG/LEAD, Running Total, Analytics
-- Database: day9_advanced_sql
-- =====================================================


-- =====================================================
-- PART 5: ROW_NUMBER(), RANK(), DENSE_RANK()
-- =====================================================

CREATE TABLE IF NOT EXISTS product_sales (
    sale_id INTEGER PRIMARY KEY,
    product VARCHAR(50),
    category VARCHAR(50),
    revenue NUMERIC(10, 2)
);

INSERT INTO product_sales (sale_id, product, category, revenue)
VALUES
    (1, 'Laptop', 'Electronics', 5000),
    (2, 'Mouse', 'Electronics', 3000),
    (3, 'Keyboard', 'Electronics', 3000),
    (4, 'Chair', 'Furniture', 2000),
    (5, 'Desk', 'Furniture', 1000)
ON CONFLICT (sale_id) DO NOTHING;


-- ROW_NUMBER: prottek row-er unique number
-- RANK: tie hole same rank, porer rank skip hoy
-- DENSE_RANK: tie hole same rank, rank skip hoy na

SELECT
    product,
    revenue,
    ROW_NUMBER() OVER (
        ORDER BY revenue DESC, sale_id
    ) AS row_num,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS sales_rank,
    DENSE_RANK() OVER (
        ORDER BY revenue DESC
    ) AS dense_rank
FROM product_sales
ORDER BY revenue DESC, sale_id;


-- Category onujayi ranking

SELECT
    product,
    category,
    revenue,
    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS category_rank
FROM product_sales
ORDER BY category, category_rank, product;


-- =====================================================
-- PART 6: LAG(), LEAD(), MONTHLY GROWTH
-- =====================================================

CREATE TABLE IF NOT EXISTS monthly_sales (
    month_start DATE PRIMARY KEY,
    revenue NUMERIC(12, 2) NOT NULL
);

INSERT INTO monthly_sales (month_start, revenue)
VALUES
    ('2026-01-01', 10000),
    ('2026-02-01', 12000),
    ('2026-03-01', 9000),
    ('2026-04-01', 15000),
    ('2026-05-01', 18000),
    ('2026-06-01', 16000)
ON CONFLICT (month_start)
DO UPDATE SET revenue = EXCLUDED.revenue;


-- LAG: previous row-er value

SELECT
    month_start,
    revenue,
    LAG(revenue) OVER (
        ORDER BY month_start
    ) AS previous_revenue
FROM monthly_sales
ORDER BY month_start;


-- LEAD: next row-er value

SELECT
    month_start,
    revenue,
    LEAD(revenue) OVER (
        ORDER BY month_start
    ) AS next_revenue
FROM monthly_sales
ORDER BY month_start;


-- Monthly revenue change

SELECT
    month_start,
    revenue,
    LAG(revenue) OVER (
        ORDER BY month_start
    ) AS previous_revenue,
    revenue - LAG(revenue) OVER (
        ORDER BY month_start
    ) AS revenue_change
FROM monthly_sales
ORDER BY month_start;


-- Monthly growth percentage

WITH monthly_comparison AS (
    SELECT
        month_start,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month_start
        ) AS previous_revenue
    FROM monthly_sales
)
SELECT
    month_start,
    revenue,
    previous_revenue,
    ROUND(
        100.0 * (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0),
        2
    ) AS growth_percent
FROM monthly_comparison
ORDER BY month_start;


-- =====================================================
-- PART 7: RUNNING TOTAL AND MOVING AVERAGE
-- =====================================================

-- Running total: current month porjonto total revenue

SELECT
    month_start,
    revenue,
    SUM(revenue) OVER (
        ORDER BY month_start
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS running_total
FROM monthly_sales
ORDER BY month_start;


-- Moving average: current month + ager 2 month

SELECT
    month_start,
    revenue,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY month_start
            ROWS BETWEEN 2 PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3_months
FROM monthly_sales
ORDER BY month_start;


-- Multiple window functions in one query

SELECT
    month_start,
    revenue,
    LAG(revenue) OVER w AS previous_revenue,
    SUM(revenue) OVER (
        ORDER BY month_start
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS running_total,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY month_start
            ROWS BETWEEN 2 PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3_months
FROM monthly_sales
WINDOW w AS (ORDER BY month_start)
ORDER BY month_start;


-- =====================================================
-- PART 8: SALES ANALYTICS PRACTICAL PROJECT
-- =====================================================

-- Product ranking + category total revenue

SELECT
    product,
    category,
    revenue,
    RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS category_rank,
    SUM(revenue) OVER (
        PARTITION BY category
    ) AS category_total
FROM product_sales
ORDER BY category, category_rank, product;


-- Monthly analytics report

WITH monthly_report AS (
    SELECT
        month_start,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month_start
        ) AS previous_revenue,
        SUM(revenue) OVER (
            ORDER BY month_start
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS running_total,
        AVG(revenue) OVER (
            ORDER BY month_start
            ROWS BETWEEN 2 PRECEDING
            AND CURRENT ROW
        ) AS moving_average
    FROM monthly_sales
)
SELECT
    month_start,
    revenue,
    previous_revenue,
    revenue - previous_revenue AS revenue_change,
    running_total,
    ROUND(moving_average, 2) AS moving_average
FROM monthly_report
ORDER BY month_start;


-- =====================================================
-- DATA VALIDATION
-- =====================================================

-- Total number of months: expected 6

SELECT COUNT(*) AS total_months
FROM monthly_sales;


-- Expected total revenue: 80000
-- Expected lowest monthly revenue: 9000
-- Expected highest monthly revenue: 18000

SELECT
    SUM(revenue) AS total_revenue,
    MIN(revenue) AS lowest_monthly_revenue,
    MAX(revenue) AS highest_monthly_revenue
FROM monthly_sales;


-- =====================================================
-- QUICK REVISION
-- ROW_NUMBER() = unique row number
-- RANK() = ties share rank; gaps can appear
-- DENSE_RANK() = ties share rank; no gaps
-- LAG() = previous row value
-- LEAD() = next row value
-- PARTITION BY = separate groups
-- Running total = cumulative SUM
-- Moving average = average over a row window
-- NULLIF(x, 0) = prevents division by zero
-- =====================================================