
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_file = PROJECT_DIR / "data" / "orders.csv"

with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    print("Headers:", reader.fieldnames)

    rows = list(reader)
    print("Total Orders:", len(rows))

    for row in rows:
        print(row)
