
from decimal import Decimal, InvalidOperation


def convert_order(row):
    """Convert raw CSV strings into appropriate Python types."""
    return {
        "order_id": int(row["order_id"].strip()),
        "customer_id": row["customer_id"].strip(),
        "quantity": int(row["quantity"].strip()),
        "unit_price": Decimal(row["unit_price"].strip()),
    }


if __name__ == "__main__":
    sample = {
        "order_id": "1001",
        "customer_id": " C101 ",
        "quantity": "2",
        "unit_price": "150.00",
    }

    try:
        result = convert_order(sample)
        print(result)
        print("Quantity type:", type(result["quantity"]).__name__)
        print("Price type:", type(result["unit_price"]).__name__)
    except (ValueError, InvalidOperation) as error:
        print(f"Conversion failed: {error}")
