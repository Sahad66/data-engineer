
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation

PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_file = PROJECT_DIR / "data" / "orders_messy.csv"

passed = 0
failed = 0

with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    required = {"order_id", "customer_id", "quantity", "unit_price"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ValueError("Required CSV columns are missing")

    for line_number, row in enumerate(reader, start=2):
        issues = []

        if not (row.get("customer_id") or "").strip():
            issues.append("Missing customer_id")

        try:
            order_id = int(row["order_id"])
            quantity = int(row["quantity"])
            price = Decimal(row["unit_price"])

            if order_id <= 0:
                issues.append("Invalid order_id")
            if quantity <= 0:
                issues.append("Invalid quantity")
            if not price.is_finite() or price < 0:
                issues.append("Invalid unit_price")

        except (ValueError, TypeError, InvalidOperation):
            issues.append("Invalid numeric value")

        if issues:
            failed += 1
            print(f"Row {line_number}: FAIL - {', '.join(issues)}")
        else:
            passed += 1
            print(f"Row {line_number}: PASS")

print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("Overall:", "PASS" if failed == 0 else "FAIL")

