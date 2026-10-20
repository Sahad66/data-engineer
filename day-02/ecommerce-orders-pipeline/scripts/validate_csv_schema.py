
import csv
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
csv_file = project_dir / "data" / "ecommerce_orders.csv"

required_columns = [
    "order_id",
    "customer_id",
    "quantity",
]

try:
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV is empty or has no header.")

        missing_columns = [
            column
            for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        rows = list(reader)

        print("CSV schema validation: PASS")
        print("Total rows:", len(rows))
        print("Required columns:", required_columns)

except FileNotFoundError:
    print(f"ERROR: File not found: {csv_file}")
    raise SystemExit(1)

except PermissionError:
    print("ERROR: Permission denied while reading CSV.")
    raise SystemExit(1)

except ValueError as error:
    print(f"CSV VALIDATION FAILED: {error}")
    raise SystemExit(1)
