from decimal import Decimal, InvalidOperation


def transform_order(row):
    return {
        "order_id": int(row["order_id"]),
        "customer_id": row["customer_id"].strip(),
        "quantity": int(row["quantity"]),
        "unit_price": Decimal(row["unit_price"]),
    }


sample = {
    "order_id": "1001",
    "customer_id": " C101 ",
    "quantity": "2",
    "unit_price": "150.50",
}

order = transform_order(sample)

print(order)
print("Order ID type:", type(order["order_id"]).__name__)
print("Quantity type:", type(order["quantity"]).__name__)
print("Price type:", type(order["unit_price"]).__name__)
print("Total:", order["quantity"] * order["unit_price"])
