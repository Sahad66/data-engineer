
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
json_file = PROJECT_DIR / "data" / "orders.json"

with open(json_file, "r", encoding="utf-8") as file:
    orders = json.load(file)

print("Total Orders:", len(orders))

for order in orders:
    print(order)
