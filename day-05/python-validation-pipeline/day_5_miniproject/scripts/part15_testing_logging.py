
import csv
import logging
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "data" / "orders.csv"
LOG_DIR = PROJECT_DIR / "logs"
LOG_PATH = LOG_DIR / "validation.log"

# Create logs folder if needed
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
    "status"
}


def validate_order(order):
    errors = []

    # Validate order ID
    try:
        if int(order.get("order_id", "")) <= 0:
            errors.append("INVALID_ORDER_ID")
    except (ValueError, TypeError):
        errors.append("INVALID_ORDER_ID")

    # Validate customer ID
    if not order.get("customer_id", "").strip():
        errors.append("MISSING_CUSTOMER_ID")

    # Validate quantity
    try:
        if int(order.get("quantity", "")) <= 0:
            errors.append("INVALID_QUANTITY")
    except (ValueError, TypeError):
        errors.append("INVALID_QUANTITY")

    # Validate unit price
    try:
        if float(order.get("unit_price", "")) <= 0:
            errors.append("INVALID_UNIT_PRICE")
    except (ValueError, TypeError):
        errors.append("INVALID_UNIT_PRICE")

    # Validate status
    allowed_statuses = {"Pending", "Shipped", "Delivered"}

    if order.get("status", "").strip() not in allowed_statuses:
        errors.append("INVALID_STATUS")

    return errors


def main():
    logging.info("VALIDATION_STARTED")

    total = 0
    passed = 0
    failed = 0

    try:
        with CSV_PATH.open(
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV is empty or has no header")

            # Clean header spaces
            reader.fieldnames = [
                name.strip() if name else ""
                for name in reader.fieldnames
            ]

            missing = REQUIRED_COLUMNS - set(reader.fieldnames)

            if missing:
                raise ValueError(
                    f"Missing CSV columns: {sorted(missing)}"
                )

            for order in reader:
                total += 1
                errors = validate_order(order)

                if errors:
                    failed += 1
                    logging.warning(
                        "Order %s FAIL: %s",
                        order.get("order_id"),
                        ", ".join(errors)
                    )
                else:
                    passed += 1
                    logging.info(
                        "Order %s PASS",
                        order.get("order_id")
                    )

        logging.info(
            "SUMMARY total=%d passed=%d failed=%d",
            total,
            passed,
            failed
        )

        if total == 0:
            logging.warning("NO_DATA_FOUND")
        elif failed == 0:
            logging.info("VALIDATION_SUCCESS")
        else:
            logging.warning("VALIDATION_COMPLETED_WITH_FAILURES")

    except (FileNotFoundError, PermissionError, ValueError, csv.Error):
        logging.exception("VALIDATION_PIPELINE_FAILED")
        return

    logging.info("VALIDATION_FINISHED")


if __name__ == "__main__":
    main()
