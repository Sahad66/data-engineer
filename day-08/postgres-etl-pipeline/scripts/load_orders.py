
import csv
import getpass
import os
from decimal import Decimal
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_FILE = BASE_DIR / "data" / "clean_orders.csv"


def main():
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Missing file: {CLEAN_FILE}")

    with CLEAN_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    password = getpass.getpass("PostgreSQL password: ")

    inserted = 0

    with psycopg.connect(
        dbname=os.getenv("PGDATABASE", "day8_etl"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    ) as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(
                    """
                    INSERT INTO clean_orders
                        (order_id, customer_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                    """,
                    (
                        int(row["order_id"]),
                        row["customer_id"].strip(),
                        int(row["quantity"]),
                        Decimal(row["unit_price"]),
                    ),
                )
                inserted += cur.rowcount

    skipped = len(rows) - inserted

    print(f"Input rows: {len(rows)}")
    print(f"Inserted rows: {inserted}")
    print(f"Skipped existing/conflicting rows: {skipped}")


if __name__ == "__main__":
    main()
