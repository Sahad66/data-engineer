import csv
from collections import Counter
from pathlib import Path

path = Path("data/orders.csv")

with path.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

counts = Counter(row["order_id"] for row in rows)

duplicate_ids = [
    order_id for order_id, count in counts.items()
    if count > 1
]

print("Total rows:", len(rows))
print("Duplicate order IDs:", duplicate_ids)
