
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_file = PROJECT_DIR / "data" / "orders.csv"

EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
]

with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    actual_columns = reader.fieldnames

    if actual_columns is None:
        raise ValueError("CSV is empty or has no header")

    missing = set(EXPECTED_COLUMNS) - set(actual_columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    print("Schema validation: PASS")
    print("Columns:", actual_columns)
