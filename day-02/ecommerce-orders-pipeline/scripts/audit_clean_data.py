
import subprocess
import logging
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "data_quality_audit.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

SQL_QUERY = """
SELECT
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
           OR TRIM(customer_id) = ''
    ),
    COUNT(*) FILTER (
        WHERE quantity <= 0
    ),
    (
        SELECT COUNT(*)
        FROM (
            SELECT order_id
            FROM ecommerce_orders_clean
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) AS duplicates
    )
FROM ecommerce_orders_clean;
"""

logging.info("Data quality audit started")

result = subprocess.run(
    [
        "psql", "-U", "postgres",
        "-d", "day-2", "-t", "-A",
        "-c", SQL_QUERY
    ],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    logging.error("SQL execution failed: %s", result.stderr.strip())
    print("AUDIT FAILED: SQL execution error")
    print(result.stderr)
else:
    values = result.stdout.strip().split("|")

    if len(values) != 3:
        logging.error("Unexpected query output: %s", result.stdout.strip())
        print("AUDIT FAILED: Unexpected query output")
    else:
        missing_id, invalid_qty, duplicate_ids = map(int, values)

        status = (
            "PASS"
            if missing_id == 0
            and invalid_qty == 0
            and duplicate_ids == 0
            else "FAIL"
        )

        print("=== CLEAN DATA QUALITY AUDIT ===")
        print(f"Missing Customer ID: {missing_id}")
        print(f"Invalid Quantity: {invalid_qty}")
        print(f"Duplicate Order IDs: {duplicate_ids}")
        print(f"AUDIT STATUS: {status}")

        logging.info(
            "Missing ID=%s | Invalid Quantity=%s | Duplicate IDs=%s | STATUS=%s",
            missing_id, invalid_qty, duplicate_ids, status
        )

logging.info("Data quality audit finished")
print(f"Audit log saved to: {LOG_FILE}")
