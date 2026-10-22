import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "orders.csv"
CLEAN_FILE = BASE_DIR / "data" / "clean_orders.csv"
REJECTED_FILE = BASE_DIR / "data" / "rejected_orders.csv"


def validate_order(row):
    errors = []

    order_id = row.get("order_id", "").strip()
    customer_id = row.get("customer_id", "").strip()
    quantity = row.get("quantity", "").strip()
    unit_price = row.get("unit_price", "").strip()

    try:
        int(order_id)
    except ValueError:
        errors.append("Invalid order_id")

    if not customer_id:
        errors.append("Missing customer_id")

    try:
        if int(quantity) <= 0:
            errors.append("Invalid quantity")
    except ValueError:
        errors.append("Invalid quantity")

    try:
        price = Decimal(unit_price)
        if not price.is_finite() or price < 0:
            errors.append("Invalid unit_price")
    except InvalidOperation:
        errors.append("Invalid unit_price")

    return errors


def main():
    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        required = {
            "order_id", "customer_id", "quantity", "unit_price"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Required CSV columns are missing")

        rows = list(reader)

    clean_rows = []
    rejected_rows = []

    for row in rows:
        errors = validate_order(row)

        if errors:
            rejected_rows.append({
                **row,
                "rejection_reason": "; ".join(errors)
            })
        else:
            clean_rows.append(row)

    with CLEAN_FILE.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["order_id", "customer_id", "quantity", "unit_price"]
        )
        writer.writeheader()
        writer.writerows(clean_rows)

    with REJECTED_FILE.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id", "customer_id", "quantity",
                "unit_price", "rejection_reason"
            ]
        )
        writer.writeheader()
        writer.writerows(rejected_rows)

    print("Input rows:", len(rows))
    print("Clean rows:", len(clean_rows))
    print("Rejected rows:", len(rejected_rows))
    print("Reconciliation:", len(rows) == len(clean_rows) + len(rejected_rows))


if __name__ == "__main__":
    main()
