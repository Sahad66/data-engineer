
-- RetailPulse Capstone
-- Phase 2 Part 6: Staging Data Quality Checks

-- CHECK 1: Missing or blank required text fields
SELECT 'customer_name_missing' AS check_name, COUNT(*) AS issue_count
FROM staging.customers
WHERE customer_name IS NULL OR TRIM(customer_name) = ''

UNION ALL

SELECT 'product_name_missing', COUNT(*)
FROM staging.products
WHERE product_name IS NULL OR TRIM(product_name) = ''

UNION ALL

SELECT 'order_id_missing', COUNT(*)
FROM staging.orders
WHERE order_id IS NULL OR TRIM(order_id) = ''

UNION ALL

SELECT 'payment_status_missing', COUNT(*)
FROM staging.payments
WHERE payment_status IS NULL OR TRIM(payment_status) = '';

-- CHECK 2: Invalid numeric values
SELECT 'invalid_quantity' AS check_name, COUNT(*) AS issue_count
FROM staging.orders
WHERE quantity <= 0

UNION ALL

SELECT 'invalid_product_price', COUNT(*)
FROM staging.products
WHERE unit_price <= 0

UNION ALL

SELECT 'invalid_payment_amount', COUNT(*)
FROM staging.payments
WHERE amount <= 0;

-- CHECK 3: Orders with missing customer references
SELECT o.order_id, o.customer_id
FROM staging.orders o
LEFT JOIN staging.customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- CHECK 4: Orders with missing product references
SELECT o.order_id, o.product_id
FROM staging.orders o
LEFT JOIN staging.products p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;

-- CHECK 5: Payments with missing order references
SELECT pay.payment_id, pay.order_id
FROM staging.payments pay
LEFT JOIN staging.orders o
    ON pay.order_id = o.order_id
WHERE o.order_id IS NULL;

-- CHECK 6: Inspect duplicate IDs
-- Primary keys should prevent duplicates.
SELECT customer_id, COUNT(*) AS duplicate_count
FROM staging.customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS duplicate_count
FROM staging.products
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS duplicate_count
FROM staging.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT payment_id, COUNT(*) AS duplicate_count
FROM staging.payments
GROUP BY payment_id
HAVING COUNT(*) > 1;

-- CHECK 7: Inspect payment statuses
SELECT payment_status, COUNT(*) AS row_count
FROM staging.payments
GROUP BY payment_status
ORDER BY payment_status;

-- CHECK 8: Compare order totals against summed payment amounts
SELECT
    o.order_id,
    p.unit_price * o.quantity AS expected_amount,
    COALESCE(SUM(pay.amount), 0) AS actual_payment_amount
FROM staging.orders o
JOIN staging.products p
    ON o.product_id = p.product_id
LEFT JOIN staging.payments pay
    ON pay.order_id = o.order_id
GROUP BY o.order_id, p.unit_price, o.quantity
HAVING COALESCE(SUM(pay.amount), 0)
       <> p.unit_price * o.quantity
ORDER BY o.order_id;
