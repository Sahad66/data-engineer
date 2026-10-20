
import subprocess
import sys

query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
           OR TRIM(customer_id) = ''
    ) AS missing_customer_ids,
    COUNT(*) FILTER (
        WHERE quantity <= 0
    ) AS invalid_quantities,
    COUNT(*) - COUNT(DISTINCT order_id)
        AS duplicate_rows
FROM ecommerce_orders_clean;
"""

result = subprocess.run(
    [
        "psql",
        "-U", "postgres",
        "-d", "day-2",
        "-t", "-A",
        "-c", query,
    ],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print("TEST FAILED: Could not query database.")
    print(result.stderr)
    sys.exit(1)

values = result.stdout.strip().split("|")

if len(values) != 4:
    print("TEST FAILED: Unexpected query output.")
    sys.exit(1)

total_rows, missing_ids, invalid_qty, duplicate_rows = map(
    int, values
)

print("Clean Data Validation Test")
print("---------------------------")
print("Total rows:", total_rows)
print("Missing customer IDs:", missing_ids)
print("Invalid quantities:", invalid_qty)
print("Duplicate rows:", duplicate_rows)

if (
    total_rows == 5
    and missing_ids == 0
    and invalid_qty == 0
    and duplicate_rows == 0
):
    print("TEST STATUS: PASS")
else:
    print("TEST STATUS: FAIL")
    sys.exit(1)
