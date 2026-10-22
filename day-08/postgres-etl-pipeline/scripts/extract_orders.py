
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "orders.csv"

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
}


def extract_orders():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV header is missing")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")

        rows = list(reader)

    return rows


if __name__ == "__main__":
    rows = extract_orders()
    print(f"Extraction successful: {len(rows)} rows")
    print(f"First row: {rows[0]}")
