-- RetailPulse Capstone
-- Phase 3 Part 2: Sales Fact Model

CREATE TABLE IF NOT EXISTS marts.fact_sales (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price > 0),
    gross_order_value NUMERIC(14, 2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED
);