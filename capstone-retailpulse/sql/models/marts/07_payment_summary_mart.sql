-- RetailPulse Capstone
-- Phase 3 Part 7: Payment Summary Data Mart

CREATE TABLE IF NOT EXISTS marts.payment_summary (
    payment_method TEXT PRIMARY KEY,
    total_payments BIGINT NOT NULL,
    paid_payments BIGINT NOT NULL,
    pending_payments BIGINT NOT NULL,
    paid_amount NUMERIC(14, 2) NOT NULL,
    pending_amount NUMERIC(14, 2) NOT NULL
);

INSERT INTO marts.payment_summary (
    payment_method,
    total_payments,
    paid_payments,
    pending_payments,
    paid_amount,
    pending_amount
)
SELECT
    COALESCE(payment_method, 'unknown') AS payment_method,
    COUNT(*) AS total_payments,
    COUNT(*) FILTER (
        WHERE LOWER(payment_status) = 'paid'
    ) AS paid_payments,
    COUNT(*) FILTER (
        WHERE LOWER(payment_status) = 'pending'
    ) AS pending_payments,
    COALESCE(
        SUM(amount) FILTER (
            WHERE LOWER(payment_status) = 'paid'
        ), 0
    ) AS paid_amount,
    COALESCE(
        SUM(amount) FILTER (
            WHERE LOWER(payment_status) = 'pending'
        ), 0
    ) AS pending_amount
FROM staging.payments
GROUP BY COALESCE(payment_method, 'unknown')
ON CONFLICT (payment_method) DO UPDATE
SET
    total_payments = EXCLUDED.total_payments,
    paid_payments = EXCLUDED.paid_payments,
    pending_payments = EXCLUDED.pending_payments,
    paid_amount = EXCLUDED.paid_amount,
    pending_amount = EXCLUDED.pending_amount;