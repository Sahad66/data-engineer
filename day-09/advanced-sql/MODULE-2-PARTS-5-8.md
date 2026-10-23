# Day 9 — Module 2: SQL Window Functions (Parts 5–8)

**Database:** `day9_advanced_sql`  
**Tool:** PostgreSQL / VS Code  
**Purpose:** Practice, revision, interview ও exam preparation

> এই notes Day 8-এর ETL project থেকে আলাদা।

---

# Part 5 — ROW_NUMBER(), RANK(), DENSE_RANK()

## 5.1 Table তৈরি

```sql
-- Product sales practice table তৈরি
CREATE TABLE IF NOT EXISTS product_sales (
    sale_id INTEGER PRIMARY KEY,   -- প্রতিটি sale-এর unique ID
    product VARCHAR(50),           -- Product name
    category VARCHAR(50),          -- Product category
    revenue NUMERIC(10, 2)         -- Sales revenue
);
```

**ব্যাখ্যা:** `CREATE TABLE IF NOT EXISTS` table না থাকলে তৈরি করে। `PRIMARY KEY` duplicate `sale_id` আটকায়।

## 5.2 Sample data insert

```sql
-- Sample product data যোগ করা
INSERT INTO product_sales (sale_id, product, category, revenue)
VALUES
    (1, 'Laptop', 'Electronics', 5000),
    (2, 'Mouse', 'Electronics', 3000),
    (3, 'Keyboard', 'Electronics', 3000),
    (4, 'Chair', 'Furniture', 2000),
    (5, 'Desk', 'Furniture', 1000)
ON CONFLICT (sale_id) DO NOTHING; -- একই ID থাকলে পুনরায় insert নয়
```

## 5.3 ROW_NUMBER()

```sql
-- Revenue বেশি থেকে কম অনুযায়ী প্রতিটি row-কে আলাদা নম্বর
SELECT
    product,
    revenue,
    ROW_NUMBER() OVER (
        ORDER BY revenue DESC, sale_id
    ) AS row_num
FROM product_sales;
```

**Logic:** `ROW_NUMBER()` প্রত্যেক row-কে আলাদা serial number দেয়। Revenue সমান হলেও row number আলাদা হবে।

## 5.4 RANK() ও DENSE_RANK()

```sql
-- তিন ধরনের ranking একসঙ্গে তুলনা
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
```

**Expected output:**

| Product | Revenue | ROW_NUMBER | RANK | DENSE_RANK |
|---|---:|---:|---:|---:|
| Laptop | 5000 | 1 | 1 | 1 |
| Mouse | 3000 | 2 | 2 | 2 |
| Keyboard | 3000 | 3 | 2 | 2 |
| Chair | 2000 | 4 | 4 | 3 |
| Desk | 1000 | 5 | 5 | 4 |

**মনে রাখো:**
- `ROW_NUMBER()` = প্রত্যেক row-এর আলাদা number।
- `RANK()` = tie হলে একই rank; পরের rank-এ gap থাকে।
- `DENSE_RANK()` = tie হলে একই rank; gap থাকে না।

## 5.5 PARTITION BY

```sql
-- প্রতিটি category-এর ভিতরে আলাদা ranking
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
```

**Logic:** `PARTITION BY category` প্রতিটি category-এর জন্য আলাদা ranking group তৈরি করে। Original rows একত্র করে ফেলে না।

---

# Part 6 — LAG(), LEAD() ও Revenue Growth

## 6.1 Monthly sales table

```sql
-- মাসভিত্তিক revenue table তৈরি
CREATE TABLE IF NOT EXISTS monthly_sales (
    month_start DATE PRIMARY KEY,   -- মাসের প্রথম দিন
    revenue NUMERIC(12, 2) NOT NULL -- মাসের revenue
);
```

## 6.2 Sample monthly data

```sql
-- ছয় মাসের sample revenue insert অথবা update
INSERT INTO monthly_sales (month_start, revenue)
VALUES
    ('2026-01-01', 10000),
    ('2026-02-01', 12000),
    ('2026-03-01', 9000),
    ('2026-04-01', 15000),
    ('2026-05-01', 18000),
    ('2026-06-01', 16000)
ON CONFLICT (month_start) DO UPDATE
SET revenue = EXCLUDED.revenue;
```

**Logic:** একই মাস আগে থেকে থাকলে `EXCLUDED.revenue` ব্যবহার করে নতুন revenue দিয়ে update করে।

## 6.3 LAG() — Previous row

```sql
-- আগের মাসের revenue দেখা
SELECT
    month_start,
    revenue,
    LAG(revenue) OVER (
        ORDER BY month_start
    ) AS previous_revenue
FROM monthly_sales
ORDER BY month_start;
```

**Logic:** `LAG()` আগের row-এর value দেয়। প্রথম row-এর আগের row না থাকায় `NULL` আসে।

## 6.4 LEAD() — Next row

```sql
-- পরের মাসের revenue দেখা
SELECT
    month_start,
    revenue,
    LEAD(revenue) OVER (
        ORDER BY month_start
    ) AS next_revenue
FROM monthly_sales
ORDER BY month_start;
```

**Logic:** `LEAD()` পরের row-এর value দেয়। শেষ row-এর পরের row না থাকায় `NULL` আসে।

## 6.5 Revenue change

```sql
-- আগের মাসের তুলনায় revenue কত পরিবর্তন হয়েছে
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
```

**Formula:** `Revenue Change = Current Revenue - Previous Revenue`

## 6.6 Percentage growth

```sql
-- CTE-তে আগের মাসের revenue বের করা
WITH monthly_comparison AS (
    SELECT
        month_start,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month_start
        ) AS previous_revenue
    FROM monthly_sales
)
-- Percentage growth হিসাব করা
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
```

**Formula:**

`Growth % = (Current - Previous) / Previous × 100`

- `WITH` = CTE তৈরি করে।
- `NULLIF(value, 0)` = value শূন্য হলে `NULL` দেয়, division-by-zero এড়াতে সাহায্য করে।
- `ROUND(value, 2)` = দশমিকের পর ২ ঘর রাখে।

---

# Part 7 — Running Total ও Moving Average

## 7.1 Running Total

```sql
-- প্রথম মাস থেকে বর্তমান মাস পর্যন্ত মোট revenue
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
```

**Expected output:**

| Month | Revenue | Running Total |
|---|---:|---:|
| Jan | 10000 | 10000 |
| Feb | 12000 | 22000 |
| Mar | 9000 | 31000 |
| Apr | 15000 | 46000 |
| May | 18000 | 64000 |
| Jun | 16000 | 80000 |

**Logic:**
- `SUM() OVER()` = Window-এর মধ্যে sum হিসাব করে।
- `UNBOUNDED PRECEDING` = Window-এর প্রথম row থেকে।
- `CURRENT ROW` = বর্তমান row পর্যন্ত।

## 7.2 Three-row Moving Average

```sql
-- বর্তমান ও আগের সর্বোচ্চ দুইটি row-এর average
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
```

**Expected output:**

| Month | Revenue | Moving Average |
|---|---:|---:|
| Jan | 10000 | 10000.00 |
| Feb | 12000 | 11000.00 |
| Mar | 9000 | 10333.33 |
| Apr | 15000 | 12000.00 |
| May | 18000 | 14000.00 |
| Jun | 16000 | 16333.33 |

**Logic:** `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` বর্তমান row ও তার আগের সর্বোচ্চ দুইটি row নেয়। শুরুতে তিনটি row না থাকলে উপলব্ধ row-গুলোর average হিসাব হয়।

## 7.3 Multiple Window Functions

```sql
-- Previous revenue, running total ও moving average একসঙ্গে
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
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3_months
FROM monthly_sales
WINDOW w AS (ORDER BY month_start)
ORDER BY month_start;
```

**Logic:** `WINDOW w AS (...)` একটি named window তৈরি করে, যাতে একই window definition পুনরায় ব্যবহার করা যায়।

---

# Part 8 — Sales Analytics Practical Project

## 8.1 Product Ranking ও Category Total

```sql
-- প্রতিটি product-এর rank এবং category-এর total revenue
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
```

**ব্যবহার:** কোন category-এর কোন product সবচেয়ে বেশি revenue করছে এবং পুরো category-এর total কত, তা বোঝা যায়।

## 8.2 Monthly Sales Analytics Report

```sql
-- CTE-তে monthly analytics তৈরি
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
-- Business report output
SELECT
    month_start,
    revenue,
    previous_revenue,
    revenue - previous_revenue AS revenue_change,
    running_total,
    ROUND(moving_average, 2) AS moving_average
FROM monthly_report
ORDER BY month_start;
```

**Report থেকে জানা যায়:**
- বর্তমান মাসের revenue
- আগের মাসের revenue
- Revenue change
- Cumulative revenue
- Three-row moving average

## 8.3 Final Validation

```sql
-- মোট কয়টি মাসের record আছে
SELECT COUNT(*) AS total_months
FROM monthly_sales;

-- মোট, সর্বনিম্ন ও সর্বোচ্চ monthly revenue
SELECT
    SUM(revenue) AS total_revenue,
    MIN(revenue) AS lowest_monthly_revenue,
    MAX(revenue) AS highest_monthly_revenue
FROM monthly_sales;
```

**Expected values:**
- `total_months` = 6
- `total_revenue` = 80000
- `lowest_monthly_revenue` = 9000
- `highest_monthly_revenue` = 18000

---

# Exam Revision — Quick Notes

| Function / Keyword | মনে রাখার উপায় |
|---|---|
| `OVER()` | Window Function চালানোর window |
| `PARTITION BY` | Group অনুযায়ী আলাদা হিসাব |
| `ORDER BY` | Row-এর ক্রম নির্ধারণ |
| `ROW_NUMBER()` | প্রত্যেক row-এর আলাদা number |
| `RANK()` | Tie-এর পর rank gap |
| `DENSE_RANK()` | Tie-এর পর gap নেই |
| `LAG()` | Previous row |
| `LEAD()` | Next row |
| `SUM() OVER()` | Running total |
| `AVG() OVER()` | Moving average |
| `ROWS BETWEEN` | Window frame-এর row range |
| `UNBOUNDED PRECEDING` | Window-এর শুরু থেকে |
| `CURRENT ROW` | বর্তমান row পর্যন্ত |
| `NULLIF()` | Zero division এড়াতে সাহায্য করে |
| `WITH` | CTE তৈরি করে |

## Practice Checklist

- [ ] `product_sales` table তৈরি ও sample data insert
- [ ] `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` তুলনা
- [ ] `PARTITION BY category` দিয়ে ranking
- [ ] `LAG()` ও `LEAD()` চালানো
- [ ] Revenue change ও growth percentage হিসাব
- [ ] Running total ও moving average যাচাই
- [ ] Sales analytics report চালানো
- [ ] Final validation: 6 months, total revenue 80000
