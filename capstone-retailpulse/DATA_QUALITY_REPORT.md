# RetailPulse — Data Quality Validation Report

## Verified Results

| Check | Result | Status |
|---|---:|---|
| Raw orders | 10 | PASS |
| Staging orders | 10 | PASS |
| Fact sales rows | 10 | PASS |
| Duplicate order IDs | 0 | PASS |
| Invalid sales rows | 0 | PASS |
| Total gross sales | 9790.00 | PASS |
| Raw-to-staging order reconciliation | 0 mismatches | PASS |

## Notes

- Raw and staging order records matched for the checked fields.
- No duplicate order IDs were found in the sales fact table.
- No invalid quantity, unit price, or null gross sales values were found in the summary validation.
- Total gross sales matched the previously observed result of 9790.00.

## Verification Scope

These results reflect the reported PostgreSQL query outputs. Re-run the validation queries after modifying source data or warehouse models.
