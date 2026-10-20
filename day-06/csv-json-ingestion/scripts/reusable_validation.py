
from decimal import Decimal, InvalidOperation


def validate_order(row):
    """Return a list of data quality issues for one order."""
    issues = []

    if not str(row.get("customer_id") or "").strip():
        issues.append("Missing customer_id")

    try:
        order_id = int(row["order_id"])
        quantity = int(row["quantity"])
        price = Decimal(str(row["unit_price"]))

        if order_id <= 0:
            issues.append("Invalid order_id")

        if quantity <= 0:
            issues.append("Invalid quantity")

        if not price.is_finite() or price < 0:
            issues.append("Invalid unit_price")

    except (ValueError, TypeError, KeyError, InvalidOperation):
        issues.append("Invalid or missing numeric field")

    return issues


sample = {
    "order_id": "6001",
    "customer_id": "C601",
    "quantity": "2",
    "unit_price": "125.50",
}
bad_order = {
    "order_id": "6002",
    "customer_id": "",
    "quantity": "0",
    "unit_price": "-10",
}

print(validate_order(bad_order))

issues = validate_order(sample)

if issues:
    print("FAIL:", issues)
else:
    print("PASS: Order is valid")
