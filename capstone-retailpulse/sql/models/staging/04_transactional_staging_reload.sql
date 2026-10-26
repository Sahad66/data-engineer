
-- RetailPulse Capstone
-- Phase 2 Part 7: Transaction-safe staging reload

BEGIN;

-- Remove old staging rows inside the transaction.
TRUNCATE TABLE
    staging.payments,
    staging.orders,
    staging.products,
    staging.customers;

-- Reload customers first.
INSERT INTO staging.customers
    (customer_id, customer_name, city)
SELECT
    TRIM(customer_id),
    TRIM(customer_name),
    NULLIF(TRIM(city), '')
FROM raw.customers;

-- Reload products.
INSERT INTO staging.products
    (product_id, product_name, category, unit_price)
SELECT
    TRIM(product_id),
    TRIM(product_name),
    NULLIF(TRIM(category), ''),
    unit_price
FROM raw.products;

-- Reload orders.
INSERT INTO staging.orders
    (order_id, customer_id, order_date, product_id, quantity)
SELECT
    TRIM(order_id),
    TRIM(customer_id),
    order_date,
    TRIM(product_id),
    quantity
FROM raw.orders;

-- Reload payments.
INSERT INTO staging.payments
    (payment_id, order_id, payment_method, payment_status, amount)
SELECT
    TRIM(payment_id),
    TRIM(order_id),
    LOWER(NULLIF(TRIM(payment_method), '')),
    LOWER(TRIM(payment_status)),
    amount
FROM raw.payments;

-- Verify source and staging row counts before commit.
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM raw.customers)
       <> (SELECT COUNT(*) FROM staging.customers) THEN
        RAISE EXCEPTION 'Customer row count mismatch';
    END IF;

    IF (SELECT COUNT(*) FROM raw.products)
       <> (SELECT COUNT(*) FROM staging.products) THEN
        RAISE EXCEPTION 'Product row count mismatch';
    END IF;

    IF (SELECT COUNT(*) FROM raw.orders)
       <> (SELECT COUNT(*) FROM staging.orders) THEN
        RAISE EXCEPTION 'Order row count mismatch';
    END IF;

    IF (SELECT COUNT(*) FROM raw.payments)
       <> (SELECT COUNT(*) FROM staging.payments) THEN
        RAISE EXCEPTION 'Payment row count mismatch';
    END IF;
END $$;

COMMIT;
