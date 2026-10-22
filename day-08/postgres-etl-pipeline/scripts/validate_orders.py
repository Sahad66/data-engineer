
import csv
from decimal import Decimal, InvalidOperation


def validate_order(row):
    reasons = []

    try:
        order_id = int(row.get("order_id", "").strip())
    except (ValueError, AttributeError):
        order_id = None
        reasons.append("Invalid order_id")

    customer_id = (row.get("customer_id") or "").strip()
    if not customer_id:
        reasons.append("Missing customer_id")

    try:
        quantity = int(row.get("quantity", "").strip())
        if quantity <= 0:
            reasons.append("Invalid quantity")
    except (ValueError, AttributeError):
        quantity = None
        reasons.append("Invalid quantity")

    try:
        price_text = row.get("unit_price", "").strip()
        unit_price = Decimal(price_text)

        if not unit_price.is_finite() or unit_price < 0:
            reasons.append("Invalid unit_price")
    except (InvalidOperation, ValueError, AttributeError):
        unit_price = None
        reasons.append("Invalid unit_price")

    clean_row = {
        "order_id": order_id,
        "customer_id": customer_id,
        "quantity": quantity,
        "unit_price": unit_price,
    }

    return clean_row, reasons


if __name__ == "__main__":
    with open(
        "data/orders.csv", "r", encoding="utf-8-sig", newline=""
    ) as file:
        for row in csv.DictReader(file):
            converted, reasons = validate_order(row)
            if reasons:
                print(converted, "| REJECT:", "; ".join(reasons))
            else:
                print(converted, "| VALID")
