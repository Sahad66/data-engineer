
import csv
from pathlib import Path
from collections import Counter

# Project folder automatically identify
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "ecommerce_orders.csv"

with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

print(f"Total rows: {len(rows)}")

# Check duplicate order IDs
order_ids = [row["order_id"] for row in rows]
counts = Counter(order_ids)

duplicates = [
    order_id
    for order_id, count in counts.items()
    if count > 1
]

print("Duplicate order IDs:", duplicates)

# Check missing customer IDs
missing_customers = [
    row["order_id"]
    for row in rows
    if not row["customer_id"].strip()
]

print("Orders with missing customer ID:", missing_customers)

# Check invalid quantities
invalid_quantities = []

for row in rows:
    try:
        quantity = int(row["quantity"])
        if quantity <= 0:
            invalid_quantities.append(row["order_id"])
    except ValueError:
        invalid_quantities.append(row["order_id"])

print("Orders with invalid quantity:", invalid_quantities)