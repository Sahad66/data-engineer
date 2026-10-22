import csv
from pathlib import Path

file_path = Path("data/orders.csv")

with file_path.open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("Total rows:", len(rows))
print("Columns:", reader.fieldnames)
print("First row:", rows[0])
