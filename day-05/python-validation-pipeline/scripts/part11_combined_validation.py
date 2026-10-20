
def validate_order(order):
    errors = []

    # Rule 1: Order ID
    order_id = order.get("order_id")

    try:
        if order_id is None or str(order_id).strip() == "":
            raise ValueError

        if int(order_id) <= 0:
            raise ValueError

    except (ValueError, TypeError):
        errors.append("INVALID_ORDER_ID")

    # Rule 2: Customer ID
    customer_id = order.get("customer_id")

    if customer_id is None or str(customer_id).strip() == "":
        errors.append("MISSING_CUSTOMER_ID")

    # Rule 3: Quantity
    quantity = order.get("quantity")

    try:
        if quantity is None or str(quantity).strip() == "":
            raise ValueError

        if int(quantity) <= 0:
            raise ValueError

    except (ValueError, TypeError):
        errors.append("INVALID_QUANTITY")

    # Rule 4: Unit price
    unit_price = order.get("unit_price")

    try:
        if unit_price is None or str(unit_price).strip() == "":
            raise ValueError

        price = float(unit_price)

        if price <= 0:
            raise ValueError

    except (ValueError, TypeError):
        errors.append("INVALID_UNIT_PRICE")

    # Rule 5: Order status
    status = order.get("status")
    allowed_statuses = {"Pending", "Shipped", "Delivered"}

    if not isinstance(status, str) or status.strip() not in allowed_statuses:
        errors.append("INVALID_STATUS")

    return errors


orders = [
    {
        "order_id": 1001,
        "customer_id": "C101",
        "quantity": 2,
        "unit_price": 150,
        "status": "Delivered"
    },
    {
        "order_id": 1002,
        "customer_id": "",
        "quantity": 0,
        "unit_price": -50,
        "status": "Unknown"
    },
    {
        "order_id": 1003,
        "customer_id": "C103",
        "quantity": "five",
        "unit_price": "abc",
        "status": "Pending"
    }
]

for order in orders:
    errors = validate_order(order)

    if errors:
        print(
            f"Order {order.get('order_id')}: "
            f"FAIL - {', '.join(errors)}"
        )
    else:
        print(f"Order {order['order_id']}: PASS")
