-- RetailPulse Capstone
-- Phase 2 Part 5: Create staging tables

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id   TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city          TEXT
);

CREATE TABLE IF NOT EXISTS staging.products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT,
    unit_price   NUMERIC(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.orders (
    order_id    TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_date  DATE NOT NULL,
    product_id  TEXT NOT NULL,
    quantity    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.payments (
    payment_id     TEXT PRIMARY KEY,
    order_id       TEXT NOT NULL,
    payment_method TEXT,
    payment_status TEXT NOT NULL,
    amount         NUMERIC(12, 2) NOT NULL
);