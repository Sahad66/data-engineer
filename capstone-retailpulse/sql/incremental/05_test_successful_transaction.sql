BEGIN;

INSERT INTO audit.incremental_demo_txn_test (
    order_id,
    amount
)
VALUES (
    'TXN_TEST_001',
    100.00
);

COMMIT;