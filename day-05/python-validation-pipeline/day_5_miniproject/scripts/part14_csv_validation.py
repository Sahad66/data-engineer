
import csv
from pathlib import Path


def validate_order(order):
    errors = []

    # 1. Validate Order ID
    try:
        order_id = int(order.get("order_id", ""))

        if order_id <= 0:
            errors.append("INVALID_ORDER_ID")

    except (ValueError, TypeError):
        errors.append("INVALID_ORDER_ID")

    # 2. Validate Customer ID
    customer_id = order.get("customer_id", "")

    if not isinstance(customer_id, str) or not customer_id.strip():
        errors.append("MISSING_CUSTOMER_ID")

    # 3. Validate Quantity
    try:
        quantity_text = order.get("quantity", "").strip()

        if not quantity_text:
            raise ValueError("Quantity is empty")

        quantity = int(quantity_text)

        if quantity <= 0:
            errors.append("INVALID_QUANTITY")

    except (ValueError, TypeError, AttributeError):
        errors.append("INVALID_QUANTITY")

    # 4. Validate Unit Price
    try:
        price_text = order.get("unit_price", "").strip()

        if not price_text:
            raise ValueError("Unit price is empty")

        unit_price = float(price_text)

        if unit_price <= 0:
            errors.append("INVALID_UNIT_PRICE")

    except (ValueError, TypeError, AttributeError):
        errors.append("INVALID_UNIT_PRICE")

    # 5. Validate Status
    allowed_statuses = {"Pending", "Shipped", "Delivered"}
    status = order.get("status", "")

    if not isinstance(status, str) or status.strip() not in allowed_statuses:
        errors.append("INVALID_STATUS")

    return errors


def main():
    # Find project directory automatically
    project_dir = Path(__file__).resolve().parent.parent
    csv_path = project_dir / "data" / "orders.csv"

    print("===== CSV VALIDATION REPORT =====")
    print(f"Input file: {csv_path}")

    total = 0
    passed = 0
    failed = 0

    try:
        # Keep the file open while reading headers and rows
        with csv_path.open(
            mode="r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            # Access fieldnames while file is still open
            headers = reader.fieldnames

            if not headers:
                print("ERROR: CSV file is empty or has no header.")
                return

            # Remove whitespace from header names
            reader.fieldnames = [
                name.strip() if name else ""
                for name in headers
            ]

            required_columns = {
                "order_id",
                "customer_id",
                "quantity",
                "unit_price",
                "status"
            }

            actual_columns = set(reader.fieldnames)
            missing_columns = required_columns - actual_columns

            if missing_columns:
                print(
                    "ERROR: Missing required columns:",
                    ", ".join(sorted(missing_columns))
                )
                print("Found columns:", reader.fieldnames)
                return

            # Validate every row before closing the file
            for row_number, order in enumerate(reader, start=2):
                total += 1
                errors = validate_order(order)

                if errors:
                    failed += 1
                    print(
                        f"Row {row_number}, Order "
                        f"{order.get('order_id')}: FAIL - "
                        f"{', '.join(errors)}"
                    )
                else:
                    passed += 1
                    print(
                        f"Row {row_number}, Order "
                        f"{order['order_id']}: PASS"
                    )

    except FileNotFoundError:
        print(f"ERROR: CSV file not found: {csv_path}")
        return

    except PermissionError:
        print(f"ERROR: Permission denied: {csv_path}")
        return

    except csv.Error as error:
        print(f"ERROR: CSV reading problem: {error}")
        return

    # Print final summary
    print("\n===== VALIDATION SUMMARY =====")
    print(f"Total Orders : {total}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failed}")

    if total == 0:
        print("Overall      : NO DATA")
    elif failed == 0:
        print("Overall      : PASS")
    else:
        print("Overall      : FAIL")


if __name__ == "__main__":
    main()
