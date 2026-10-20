
import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "data" / "nested_order.json"

with open(path, "r", encoding="utf-8") as file:
    order = json.load(file)

print("Order ID:", order["order_id"])
print("Customer:", order["customer"]["customer_id"])
print("City:", order["customer"]["city"])

for item in order["items"]:
    print(item["product"], "quantity:", item["quantity"])
