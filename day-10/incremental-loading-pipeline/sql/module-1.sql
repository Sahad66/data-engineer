# Day 10 — Module 1 SQL Notes
## Topic: Incremental Loading, Full Load, Watermark & High-Water Mark (HWM)

### Part 1: Schema ও Source Table তৈরি

```sql
CREATE SCHEMA IF NOT EXISTS day10_incremental;

CREATE TABLE day10_incremental.orders_source (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(20),
    amount NUMERIC(10,2),
    updated_at TIMESTAMPTZ
);
```

### Part 2: Source Table-এ Sample Data Insert

```sql
INSERT INTO day10_incremental.orders_source
    (order_id, customer_id, amount, updated_at)
VALUES
    (1, 'C101', 500.00, '2026-10-20 09:00:00+06'),
    (2, 'C102', 750.00, '2026-10-20 10:00:00+06'),
    (3, 'C103', 300.00, '2026-10-20 11:00:00+06');
```

### Part 3: Source Table-এর সব Data দেখা

```sql
SELECT *
FROM day10_incremental.orders_source
ORDER BY order_id;
```

### Part 4: নতুন Order Insert

```sql
INSERT INTO day10_incremental.orders_source
    (order_id, customer_id, amount, updated_at)
VALUES
    (4, 'C104', 900.00, '2026-10-20 12:00:00+06');
```

### Part 5: নির্দিষ্ট ID-এর পরের নতুন Order খোঁজা

```sql
SELECT *
FROM day10_incremental.orders_source
WHERE order_id > 3
ORDER BY order_id;
```

Expected: শুধু `order_id = 4`।

### Part 6: Full Load ও Incremental Load-এর জন্য সব Order দেখা

```sql
SELECT order_id, amount
FROM day10_incremental.orders_source
ORDER BY order_id;
```

### Part 7: Watermark Table তৈরি

```sql
CREATE TABLE day10_incremental.etl_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_loaded_at TIMESTAMPTZ NOT NULL
);
```

### Part 8: Watermark-এ Checkpoint Insert

```sql
INSERT INTO day10_incremental.etl_watermark
    (pipeline_name, last_loaded_at)
VALUES
    ('orders_pipeline', '2026-10-20 10:00:00+06');
```

### Part 9: Watermark দেখা

```sql
SELECT *
FROM day10_incremental.etl_watermark;
```

### Part 10: Watermark ব্যবহার করে নতুন/পরিবর্তিত Data খোঁজা

```sql
SELECT s.*
FROM day10_incremental.orders_source AS s
CROSS JOIN day10_incremental.etl_watermark AS w
WHERE w.pipeline_name = 'orders_pipeline'
  AND s.updated_at > w.last_loaded_at
ORDER BY s.updated_at;
```

Expected: বর্তমান sample data অনুযায়ী order 3 ও order 4 আসবে।

### Part 11: High-Water Mark (HWM) দিয়ে নতুন ID খোঁজা

ধরা হয়েছে, সর্বশেষ processed `order_id = 3`।

```sql
SELECT *
FROM day10_incremental.orders_source
WHERE order_id > 3
ORDER BY order_id;
```

Expected: শুধু order 4।

### Part 12: Source-এর সর্বোচ্চ Order ID বের করা

```sql
SELECT MAX(order_id) AS high_water_mark
FROM day10_incremental.orders_source;
```

Expected:

| high_water_mark |
|---:|
| 4 |

### Part 13: সব Order ID ও Amount যাচাই

```sql
SELECT order_id, customer_id, amount, updated_at
FROM day10_incremental.orders_source
ORDER BY order_id;
```

```
### গুরুত্বপূর্ণ Notes

- **Full Load:** সব প্রয়োজনীয় data load করা।
- **Incremental Load:** শুধু নতুন বা পরিবর্তিত data load করা।
- **Watermark:** শেষ processing checkpoint, যেমন `updated_at`।
- **High-Water Mark (HWM):** সর্বোচ্চ processed value, যেমন `order_id`।
- `order_id > HWM` দিয়ে পুরোনো order-এর update শনাক্ত করা যায় না।
- `updated_at > watermark` দিয়ে update শনাক্ত করতে হলে source-এর update-এর সময় `updated_at` সঠিকভাবে পরিবর্তন হতে হবে।
- Target-এ data সফলভাবে load ও validate করার আগে watermark update করা উচিত নয়।
- বাস্তব pipeline-এ duplicate প্রতিরোধের জন্য unique key এবং UPSERT ব্যবহার করা হয়।

**Day 10 Module 1-এর SQL Notes শেষ।**
```