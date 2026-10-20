
import csv
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "sales.csv"

required_columns = {
    "sale_id",
    "sale_date",
    "product",
    "category",
    "quantity",
    "unit_price",
    "city",
}

errors = []
seen_ids = set()
checked_rows = 0

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    if not reader.fieldnames or not required_columns.issubset(
        reader.fieldnames
    ):
        raise ValueError("CSV is missing required columns")

    for row_number, row in enumerate(reader, start=2):
        checked_rows += 1

        try:
            sale_id = int(row["sale_id"])
            if sale_id <= 0:
                raise ValueError("sale_id must be positive")

            if sale_id in seen_ids:
                raise ValueError(f"Duplicate sale_id: {sale_id}")
            seen_ids.add(sale_id)

            date.fromisoformat(row["sale_date"])

            if not row["product"].strip():
                raise ValueError("Product is empty")

            quantity = int(row["quantity"])
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            price = Decimal(row["unit_price"])
            if not price.is_finite() or price < 0:
                raise ValueError("Unit price must be finite and non-negative")

            if not row["category"].strip():
                raise ValueError("Category is empty")

            if not row["city"].strip():
                raise ValueError("City is empty")

        except (ValueError, InvalidOperation, TypeError) as error:
            errors.append(
                f"Row {row_number}: {error}"
            )

print(f"Rows checked: {checked_rows}")
print(f"Errors found: {len(errors)}")

for error in errors:
    print(error)

if errors:
    print("Data quality result: FAILED")
else:
    print("Data quality result: PASSED")