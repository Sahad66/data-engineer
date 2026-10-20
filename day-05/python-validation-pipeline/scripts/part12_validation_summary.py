def validate_order(order):
    errors = []

    # Rule 1: Order ID
    try:
        order_id = order.get("order_id")

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
    try:
        quantity = order.get("quantity")

        if quantity is None or str(quantity).strip() == "":
            raise ValueError

        if int(quantity) <= 0:
            raise ValueError

    except (ValueError, TypeError):
        errors.append("INVALID_QUANTITY")

    # Rule 4: Unit price
    try:
        unit_price = order.get("unit_price")

        if unit_price is None or str(unit_price).strip() == "":
            raise ValueError

        if float(unit_price) <= 0:
            raise ValueError

    except (ValueError, TypeError):
        errors.append("INVALID_UNIT_PRICE")

    # Rule 5: Status
    allowed_statuses = {"Pending", "Shipped", "Delivered"}
    status = order.get("status")

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

# Summary counters
total_orders = len(orders)
passed_orders = 0
failed_orders = 0

print("===== ORDER VALIDATION REPORT =====")

for order in orders:
    errors = validate_order(order)

    if errors:
        failed_orders += 1

        print(
            f"Order {order.get('order_id')}: FAIL"
        )
        print(f"  Issues: {', '.join(errors)}")

    else:
        passed_orders += 1
        print(f"Order {order['order_id']}: PASS")

# Final summary
print("\n===== VALIDATION SUMMARY =====")
print(f"Total Orders : {total_orders}")
print(f"Passed       : {passed_orders}")
print(f"Failed       : {failed_orders}")

if failed_orders == 0:
    print("Overall      : PASS")
else:
    print("Overall      : FAIL")
