
import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "orders.json"

with open(path, "r", encoding="utf-8") as file:
    orders = json.load(file)

first_order = orders[0]

for key, value in first_order.items():
    print(key, "=", value, "| type =", type(value).__name__)
