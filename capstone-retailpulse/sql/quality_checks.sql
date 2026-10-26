
-- RetailPulse Capstone
-- Phase 2 Part 4: Raw Data Quality Checks

-- CHECK 1: Required text fields are missing or blank
SELECT 'customers_missing_name' AS check_name, COUNT(*) AS issue_count
FROM raw.customers
WHERE customer_name IS NULL OR TRIM(customer_name) = '';

SELECT 'products_missing_name' AS check_name, COUNT(*) AS issue_count
FROM raw.products
WHERE product_name IS NULL OR TRIM(product_name) = '';

-- CHECK 2: Invalid quantities and prices
SELECT 'invalid_quantity' AS check_name, COUNT(*) AS issue_count
FROM raw.orders
WHERE quantity <= 0;

SELECT 'invalid_product_price' AS check_name, COUNT(*) AS issue_count
FROM raw.products
WHERE unit_price <= 0;

SELECT 'invalid_payment_amount' AS check_name, COUNT(*) AS issue_count
FROM raw.payments
WHERE amount <= 0;

-- CHECK 3: Orders referencing missing customers
SELECT o.order_id, o.customer_id
FROM raw.orders o
LEFT JOIN raw.customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- CHECK 4: Orders referencing missing products
SELECT o.order_id, o.product_id
FROM raw.orders o
LEFT JOIN raw.products p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;

-- CHECK 5: Payments referencing missing orders
SELECT p.payment_id, p.order_id
FROM raw.payments p
LEFT JOIN raw.orders o
    ON p.order_id = o.order_id
WHERE o.order_id IS NULL;

-- CHECK 6: Duplicate IDs (should return zero rows)
SELECT customer_id, COUNT(*) AS duplicate_count
FROM raw.customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS duplicate_count
FROM raw.products
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS duplicate_count
FROM raw.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT payment_id, COUNT(*) AS duplicate_count
FROM raw.payments
GROUP BY payment_id
HAVING COUNT(*) > 1;

-- CHECK 7: Inspect payment status values
SELECT payment_status, COUNT(*) AS row_count
FROM raw.payments
GROUP BY payment_status
ORDER BY payment_status;

-- CHECK 8: Compare order totals with payment amounts
SELECT
    o.order_id,
    p.product_id,
    p.unit_price * o.quantity AS expected_order_amount,
    COALESCE(SUM(pay.amount), 0) AS actual_payment_amount
FROM raw.orders o
JOIN raw.products p
    ON o.product_id = p.product_id
LEFT JOIN raw.payments pay
    ON o.order_id = pay.order_id
GROUP BY o.order_id, p.product_id, p.unit_price, o.quantity
HAVING COALESCE(SUM(pay.amount), 0)
       <> p.unit_price * o.quantity
ORDER BY o.order_id;
