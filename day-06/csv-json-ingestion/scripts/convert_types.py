
import csv
from decimal import Decimal
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_file = PROJECT_DIR / "data" / "orders.csv"

with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = int(row["order_id"])
        quantity = int(row["quantity"])
        unit_price = Decimal(row["unit_price"])

        total = quantity * unit_price

        print(
            f"Order {order_id}: "
            f"quantity={quantity}, "
            f"unit_price={unit_price}, "
            f"total={total:.2f}"
        )
