
import csv
from decimal import Decimal
from pathlib import Path

from validate_orders import validate_order

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "orders.csv"
CLEAN_FILE = BASE_DIR / "data" / "clean_orders.csv"
REJECTED_FILE = BASE_DIR / "data" / "rejected_orders.csv"

COLUMNS = ["order_id", "customer_id", "quantity", "unit_price"]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    clean_rows = []
    rejected_rows = []

    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV header is missing")

        missing = set(COLUMNS) - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")

        for row in reader:
            converted, reasons = validate_order(row)

            if reasons:
                rejected = {
                    column: row.get(column, "")
                    for column in COLUMNS
                }
                rejected["rejection_reason"] = "; ".join(reasons)
                rejected_rows.append(rejected)
            else:
                clean_rows.append({
                    "order_id": converted["order_id"],
                    "customer_id": converted["customer_id"],
                    "quantity": converted["quantity"],
                    "unit_price": format(
                        converted["unit_price"], "f"
                    ),
                })

    with CLEAN_FILE.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(clean_rows)

    rejected_columns = COLUMNS + ["rejection_reason"]
    with REJECTED_FILE.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=rejected_columns
        )
        writer.writeheader()
        writer.writerows(rejected_rows)

    input_count = len(clean_rows) + len(rejected_rows)
    reconciled = input_count == len(clean_rows) + len(rejected_rows)

    print(f"Input rows: {input_count}")
    print(f"Clean rows: {len(clean_rows)}")
    print(f"Rejected rows: {len(rejected_rows)}")
    print(f"Reconciliation: {'PASS' if reconciled else 'FAIL'}")
    print(f"Clean file: {CLEAN_FILE}")
    print(f"Rejected file: {REJECTED_FILE}")


if __name__ == "__main__":
    main()
