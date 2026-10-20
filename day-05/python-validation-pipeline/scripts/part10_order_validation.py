
def validate_order(order):
    errors = []

    # Rule 1: Validate order_id
    order_id = order.get("order_id")

    if order_id is None or str(order_id).strip() == "":
        errors.append("INVALID_ORDER_ID")

    # Rule 2: Validate customer_id
    customer_id = order.get("customer_id")

    if customer_id is None or str(customer_id).strip() == "":
        errors.append("MISSING_CUSTOMER_ID")

    # Rule 3: Validate quantity
    quantity = order.get("quantity")

    if quantity is None or str(quantity).strip() == "":
        errors.append("INVALID_QUANTITY")

    else:
        try:
            number = int(quantity)

            if number <= 0:
                errors.append("INVALID_QUANTITY")

        except (ValueError, TypeError):
            errors.append("INVALID_QUANTITY")

    return errors


orders = [
    {
        "order_id": 1001,
        "customer_id": "C101",
        "quantity": 2
    },
    {
        "order_id": 1002,
        "customer_id": "",
        "quantity": 3
    },
    {
        "order_id": None,
        "customer_id": "C103",
        "quantity": 0
    },
    {
        "order_id": 1004,
        "customer_id": "C104",
        "quantity": "zero"
    },
    {
        "order_id": 1005,
        "customer_id": "C105",
        "quantity": -2
    },
    {
    "order_id": 1006,
    "customer_id": "C106",
    "quantity": "5"
}
]

for order in orders:
    errors = validate_order(order)

    if errors:
        print(f"Order {order.get('order_id')}: FAIL - {', '.join(errors)}")
    else:
        print(f"Order {order['order_id']}: PASS")
