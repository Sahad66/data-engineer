#Step 1 — Python script তৈরি করো
import csv
from pathlib import Path

# Project-এর data file-এর path
project_dir = Path(__file__).resolve().parent.parent
csv_file = project_dir / "data" / "sales.csv"

# CSV file পড়া
with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    sales = list(reader)

print("Total records:", len(sales))
print("First record:", sales[0])


#Step 2 — Python দিয়ে revenue হিসাব করো

total_revenue = 0

for sale in sales:
    quantity = int(sale["quantity"])
    unit_price = float(sale["unit_price"])

    revenue = quantity * unit_price
    total_revenue += revenue

print("Total revenue:", total_revenue)



#Step 3 — Data validation যোগ করো


invalid_rows = []

for sale in sales:
    if not sale["sale_id"] or not sale["product"]:
        invalid_rows.append(sale)
        continue

    if int(sale["quantity"]) <= 0:
        invalid_rows.append(sale)

print("Invalid records:", len(invalid_rows))