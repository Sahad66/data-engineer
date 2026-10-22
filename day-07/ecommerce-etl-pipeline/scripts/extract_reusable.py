import csv
import json
from pathlib import Path


def extract_csv(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames

    return rows, columns


def extract_json(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8-sig") as file:
        rows = json.load(file)

    if not isinstance(rows, list):
        raise ValueError("JSON must contain a list of records")

    columns = list(rows[0].keys()) if rows else []
    return rows, columns


if __name__ == "__main__":
    csv_rows, csv_columns = extract_csv("data/orders.csv")
    json_rows, json_columns = extract_json("data/orders.json")

    print("CSV rows:", len(csv_rows))
    print("CSV columns:", csv_columns)
    print("JSON rows:", len(json_rows))
    print("JSON columns:", json_columns)





from pathlib import Path

path = Path("data/orders.csv")

if not path.exists():
    raise FileNotFoundError(f"File not found: {path}")
required_columns = {
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
}
missing_columns = required_columns - set(csv_columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

print("Schema validation: PASS")