
-- RetailPulse Capstone
-- Phase 2 - Part 2
-- Create raw data tables

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city          TEXT
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT,
    unit_price   NUMERIC(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date  DATE NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.payments (
    payment_id     INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    payment_method TEXT,
    payment_status TEXT NOT NULL,
    amount         NUMERIC(12, 2) NOT NULL
);
