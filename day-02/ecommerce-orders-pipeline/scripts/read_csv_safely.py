
import csv
from pathlib import Path

# Project folder-এর অবস্থান বের করা
project_dir = Path(__file__).resolve().parent.parent

# CSV file-এর path
csv_file = project_dir / "data" / "ecommerce_orders.csv"

try:
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    print("CSV loaded successfully!")
    print("Total rows:", len(rows))

except FileNotFoundError:
    print("ERROR: CSV file was not found.")
    raise

except PermissionError:
    print("ERROR: Permission denied while reading CSV.")
    raise
