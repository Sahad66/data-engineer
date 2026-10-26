
-- RetailPulse Capstone
-- Phase 4: Incremental Loading Demo Setup

BEGIN;

-- 1. Incremental source table
CREATE TABLE IF NOT EXISTS audit.incremental_demo_source (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    updated_at TIMESTAMP NOT NULL
);

-- 2. Incremental target table
CREATE TABLE IF NOT EXISTS audit.incremental_demo_target (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    updated_at TIMESTAMP NOT NULL
);

-- 3. Watermark table
CREATE TABLE IF NOT EXISTS audit.incremental_demo_watermark (
    pipeline_name TEXT PRIMARY KEY,
    last_updated_at TIMESTAMP NOT NULL
);

-- 4. Initial watermark
INSERT INTO audit.incremental_demo_watermark (
    pipeline_name,
    last_updated_at
)
VALUES (
    'retailpulse_incremental_demo',
    TIMESTAMP '1900-01-01 00:00:00'
)
ON CONFLICT (pipeline_name) DO NOTHING;

-- 5. Initial sample source rows
INSERT INTO audit.incremental_demo_source (
    order_id,
    customer_id,
    amount,
    updated_at
)
VALUES
    ('O2001', 'C001', 1500.00, TIMESTAMP '2026-10-20 09:00:00'),
    ('O2002', 'C002', 2200.00, TIMESTAMP '2026-10-20 10:00:00'),
    ('O2003', 'C003', 1800.00, TIMESTAMP '2026-10-20 11:00:00')
ON CONFLICT (order_id) DO NOTHING;

COMMIT;
