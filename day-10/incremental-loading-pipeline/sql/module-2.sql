# Day 10 — Module 2 SQL Notes
## Topic: Incremental Data, UPSERT, ON CONFLICT & Duplicate Prevention

### Part 5 — Target Table তৈরি

```sql
CREATE TABLE day10_incremental.orders_target (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(20),
    amount NUMERIC(10,2),
    updated_at TIMESTAMPTZ
);
```

### Query 2: Source ও Target দেখা

```sql
SELECT *
FROM day10_incremental.orders_source
ORDER BY order_id;

SELECT *
FROM day10_incremental.orders_target
ORDER BY order_id;
```

### Query 3: Target-এ নেই এমন নতুন Record খোঁজা

```sql
SELECT s.*
FROM day10_incremental.orders_source AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM day10_incremental.orders_target AS t
    WHERE t.order_id = s.order_id
)
ORDER BY s.order_id;
```

**ব্যাখ্যা:** `NOT EXISTS` source-এর এমন record খুঁজে বের করে, যার `order_id` target-এ নেই।

### Part 6 — নতুন Record Load করা

```sql
INSERT INTO day10_incremental.orders_target
    (order_id, customer_id, amount, updated_at)
SELECT
    s.order_id,
    s.customer_id,
    s.amount,
    s.updated_at
FROM day10_incremental.orders_source AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM day10_incremental.orders_target AS t
    WHERE t.order_id = s.order_id
);
```

### Query 5: Target যাচাই

```sql
SELECT *
FROM day10_incremental.orders_target
ORDER BY order_id;
```

### Query 6: Source-এর Existing Order Update করা

```sql
UPDATE day10_incremental.orders_source
SET amount = 800.00,
    updated_at = CURRENT_TIMESTAMP
WHERE order_id = 2;
```

**ব্যাখ্যা:** order 2-এর amount পরিবর্তন করে এবং তার update timestamp বর্তমান সময়ে সেট করে।

### Part 7 — UPSERT with ON CONFLICT

```sql
INSERT INTO day10_incremental.orders_target
    (order_id, customer_id, amount, updated_at)
SELECT
    order_id,
    customer_id,
    amount,
    updated_at
FROM day10_incremental.orders_source
ON CONFLICT (order_id)
DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    amount = EXCLUDED.amount,
    updated_at = EXCLUDED.updated_at
WHERE EXCLUDED.updated_at >
      day10_incremental.orders_target.updated_at;
```

**গুরুত্বপূর্ণ শব্দ:**

- `INSERT`: নতুন record যোগ করে।
- `ON CONFLICT (order_id)`: একই order ID থাকলে conflict শনাক্ত করে।
- `DO UPDATE`: existing record update করে।
- `EXCLUDED`: নতুন করে insert করার চেষ্টা করা row।
- `WHERE`: incoming record-এর timestamp target-এর timestamp-এর চেয়ে নতুন হলেই update করে।

### Query 8: Updated Target যাচাই

```sql
SELECT
    order_id,
    customer_id,
    amount,
    updated_at
FROM day10_incremental.orders_target
ORDER BY order_id;
```

Expected: order 2-এর amount `800.00` হবে।

### Part 8 — Duplicate Prevention

### Query 9: Duplicate Order ID খোঁজা

```sql
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM day10_incremental.orders_target
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected: `0 rows`।

### Query 10: Total, Unique ও Duplicate Count

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_rows
FROM day10_incremental.orders_target;
```

Expected:

| total_rows | unique_order_ids | duplicate_rows |
|---:|---:|---:|
| 4 | 4 | 0 |

### Query 11: Primary Key Conflict Test

**সতর্কতা:** এই query ইচ্ছাকৃতভাবে duplicate key error তৈরি করবে।

```sql
INSERT INTO day10_incremental.orders_target
    (order_id, customer_id, amount, updated_at)
VALUES
    (1, 'C101', 500.00, CURRENT_TIMESTAMP);
```

Expected: duplicate key violation error, কারণ `order_id = 1` আগে থেকেই আছে।

### Query 12: Pipeline Rerun Test

Part 7-এর UPSERT query আবার চালিয়ে যাচাই করো:

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders
FROM day10_incremental.orders_target;
```

Expected: `total_rows = 4`, `unique_orders = 4`।

## Quick Revision

| Concept | কাজ |
|---|---|
```
| `NOT EXISTS` | Target-এ নেই এমন record খোঁজে |
| `INSERT` | নতুন record যোগ করে |
| `UPDATE` | Existing record পরিবর্তন করে |
| `UPSERT` | Insert অথবা Update করে |
| `ON CONFLICT` | Unique/primary-key conflict সামলায় |
| `PRIMARY KEY` | একই key-সহ একাধিক row হতে দেয় না |
| `GROUP BY` + `HAVING` | Duplicate key শনাক্ত করে |
| `COUNT(DISTINCT ...)` | Unique value গণনা করে |

**মনে রাখবে:** Duplicate prevention-এর জন্য Primary Key/Unique Constraint এবং UPSERT গুরুত্বপূর্ণ। আর পরিবর্তিত data শনাক্ত করতে `updated_at`, watermark বা অন্য নির্ভরযোগ্য change-tracking logic প্রয়োজন।

**Day 10 — Module 2, Parts 5–8 সম্পন্ন।**

```