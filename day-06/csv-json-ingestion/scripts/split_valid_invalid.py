
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / "data" / "orders_messy.csv"
VALID = BASE / "data" / "orders_valid.csv"
REJECTED = BASE / "data" / "orders_rejected.csv"

def validate(row):
    issues = []

    if not (row.get("customer_id") or "").strip():
        issues.append("missing_customer_id")

    try:
        if int(row["order_id"]) <= 0:
            issues.append("invalid_order_id")

        if int(row["quantity"]) <= 0:
            issues.append("invalid_quantity")

        price = Decimal(row["unit_price"])
        if not price.is_finite() or price < 0:
            issues.append("invalid_unit_price")

    except (ValueError, TypeError, KeyError, InvalidOperation):
        issues.append("invalid_numeric_value")

    return issues

with open(SOURCE, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    fields = (reader.fieldnames or []) + ["quality_issues"]

    if not reader.fieldnames:
        raise ValueError("Source CSV has no header")

    valid_rows = []
    rejected_rows = []

    for row in reader:
        issues = validate(row)

        if issues:
            rejected_rows.append({
                **row,
                "quality_issues": ";".join(issues)
            })
        else:
            valid_rows.append({
                **row,
                "quality_issues": ""
            })

for path, rows in [(VALID, valid_rows), (REJECTED, rejected_rows)]:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

print("Valid rows:", len(valid_rows))
print("Rejected rows:", len(rejected_rows))
print("Valid file:", VALID.name)
print("Rejected file:", REJECTED.name)
