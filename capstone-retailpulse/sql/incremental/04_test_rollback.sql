-- RetailPulse Phase 4 - Part 8
-- Test transaction rollback safely

BEGIN;

-- This insert is valid, but must roll back.
INSERT INTO audit.incremental_demo_txn_test (
    order_id,
    amount
)
VALUES (
    'TXN_TEST_001',
    100.00
);

-- This insert violates CHECK (amount > 0).
INSERT INTO audit.incremental_demo_txn_test (
    order_id,
    amount
)
VALUES (
    'TXN_TEST_002',
    -50.00
);

COMMIT;