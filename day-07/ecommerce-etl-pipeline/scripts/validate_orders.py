from decimal import Decimal, InvalidOperation


def validate_order(row):
    errors = []

    order_id = row.get("order_id", "").strip()
    customer_id = row.get("customer_id", "").strip()
    quantity = row.get("quantity", "").strip()
    unit_price = row.get("unit_price", "").strip()

    if not order_id:
        errors.append("Missing order_id")
    else:
        try:
            int(order_id)
        except ValueError:
            errors.append("Invalid order_id")

    if not customer_id:
        errors.append("Missing customer_id")

    try:
        if int(quantity) <= 0:
            errors.append("Invalid quantity")
    except ValueError:
        errors.append("Invalid quantity")

    try:
        if Decimal(unit_price) < 0:
            errors.append("Invalid unit_price")
    except InvalidOperation:
        errors.append("Invalid unit_price")

    return errors


samples = [
    {"order_id": "1001", "customer_id": "C101",
     "quantity": "2", "unit_price": "150"},
    {"order_id": "1002", "customer_id": "",
     "quantity": "0", "unit_price": "200"},
    {"order_id": "1003", "customer_id": "C103",
     "quantity": "3", "unit_price": "-50"},
]

for row in samples:
    issues = validate_order(row)
    print(row["order_id"], "PASS" if not issues else "REJECTED", issues)
