
import csv
import getpass
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def read_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    input_rows = read_csv("orders.csv")
    clean_rows = read_csv("clean_orders.csv")
    rejected_rows = read_csv("rejected_orders.csv")

    assert len(input_rows) == len(clean_rows) + len(rejected_rows), (
        "Reconciliation failed"
    )

    for row in clean_rows:
        assert row["customer_id"].strip(), "Missing clean customer_id"
        assert int(row["quantity"]) > 0, "Invalid clean quantity"

        price = Decimal(row["unit_price"])
        assert price.is_finite() and price >= 0, "Invalid clean price"

    for row in rejected_rows:
        assert row["rejection_reason"].strip(), "Missing rejection reason"

    password = getpass.getpass("PostgreSQL password: ")

    with psycopg.connect(
        dbname=os.getenv("PGDATABASE", "day8_etl"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*), COUNT(DISTINCT order_id),
                       COUNT(*) FILTER (
                           WHERE customer_id IS NULL OR BTRIM(customer_id) = ''
                       ),
                       COUNT(*) FILTER (WHERE quantity <= 0),
                       COUNT(*) FILTER (WHERE unit_price < 0)
                FROM clean_orders
                """
            )
            total, unique_ids, missing_customers, bad_qty, bad_price = (
                cur.fetchone()
            )

            cur.execute(
                """
                SELECT status, input_rows, clean_rows, rejected_rows
                FROM etl_audit
                ORDER BY run_id DESC
                LIMIT 1
                """
            )
            audit = cur.fetchone()

    assert total == unique_ids, "Duplicate order IDs found"
    assert missing_customers == 0, "Missing customers found"
    assert bad_qty == 0, "Invalid quantities found"
    assert bad_price == 0, "Invalid prices found"
    assert audit is not None, "No audit record found"
    assert audit[0] == "SUCCESS", "Latest audit status is not SUCCESS"
    assert audit[1:4] == (
        len(input_rows), len(clean_rows), len(rejected_rows)
    ), "Audit row counts do not match current files"

    print("File reconciliation: PASS")
    print("Clean data validation: PASS")
    print("Database quality: PASS")
    print("Latest audit: PASS")
    print(f"Database rows: {total}")
    print("VERIFICATION: PASS")


if __name__ == "__main__":
    main()
