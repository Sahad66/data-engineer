-- RetailPulse Capstone
-- Phase 2 Part 5: Load normalized data into staging

-- Clear previous staging data before reloading
TRUNCATE TABLE
    staging.payments,
    staging.orders,
    staging.products,
    staging.customers;

INSERT INTO staging.customers
    (customer_id, customer_name, city)
SELECT
    TRIM(customer_id),
    TRIM(customer_name),
    NULLIF(TRIM(city), '')
FROM raw.customers;

INSERT INTO staging.products
    (product_id, product_name, category, unit_price)
SELECT
    TRIM(product_id),
    TRIM(product_name),
    NULLIF(TRIM(category), ''),
    unit_price
FROM raw.products;

INSERT INTO staging.orders
    (order_id, customer_id, order_date, product_id, quantity)
SELECT
    TRIM(order_id),
    TRIM(customer_id),
    order_date,
    TRIM(product_id),
    quantity
FROM raw.orders;

INSERT INTO staging.payments
    (payment_id, order_id, payment_method, payment_status, amount)
SELECT
    TRIM(payment_id),
    TRIM(order_id),
    LOWER(NULLIF(TRIM(payment_method), '')),
    LOWER(TRIM(payment_status)),
    amount
FROM raw.payments;