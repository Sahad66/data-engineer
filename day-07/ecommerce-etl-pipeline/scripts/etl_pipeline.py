import csv
import logging
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

INPUT_FILE = DATA_DIR / "orders.csv"
CLEAN_FILE = DATA_DIR / "clean_orders.csv"
REJECTED_FILE = DATA_DIR / "rejected_orders.csv"
AUDIT_FILE = LOG_DIR / "etl_audit.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


def extract_rows():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Source file missing: {INPUT_FILE}")

    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        required = {
            "order_id", "customer_id", "quantity", "unit_price"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Required CSV columns are missing")

        rows = list(reader)

    logging.info("Extracted %s input rows", len(rows))
    return rows


def transform_row(row):
    errors = []
    order_id = row.get("order_id", "").strip()
    customer_id = row.get("customer_id", "").strip()
    quantity_text = row.get("quantity", "").strip()
    price_text = row.get("unit_price", "").strip()

    try:
        order_id = int(order_id)
    except ValueError:
        errors.append("Invalid order_id")

    if not customer_id:
        errors.append("Missing customer_id")

    try:
        quantity = int(quantity_text)
        if quantity <= 0:
            errors.append("Invalid quantity")
    except ValueError:
        quantity = None
        errors.append("Invalid quantity")

    try:
        price = Decimal(price_text)
        if not price.is_finite() or price < 0:
            errors.append("Invalid unit_price")
    except InvalidOperation:
        price = None
        errors.append("Invalid unit_price")

    if errors:
        return None, "; ".join(errors)

    clean_row = {
        "order_id": order_id,
        "customer_id": customer_id,
        "quantity": quantity,
        "unit_price": format(price, ".2f"),
    }
    return clean_row, None


def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_audit(input_count, clean_count, rejected_count, status, message):
    columns = [
        "input_rows", "clean_rows", "rejected_rows", "status", "message"
    ]
    new_file = not AUDIT_FILE.exists()

    with AUDIT_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "input_rows": input_count,
            "clean_rows": clean_count,
            "rejected_rows": rejected_count,
            "status": status,
            "message": message,
        })


def main():
    rows = []
    clean_rows = []
    rejected_rows = []

    try:
        rows = extract_rows()

        for row in rows:
            cleaned, reason = transform_row(row)
            if reason:
                rejected_rows.append({
                    **row,
                    "rejection_reason": reason,
                })
            else:
                clean_rows.append(cleaned)

        if len(rows) != len(clean_rows) + len(rejected_rows):
            raise RuntimeError("Row reconciliation failed")

        write_csv(
            CLEAN_FILE,
            clean_rows,
            ["order_id", "customer_id", "quantity", "unit_price"],
        )
        write_csv(
            REJECTED_FILE,
            rejected_rows,
            [
                "order_id", "customer_id", "quantity",
                "unit_price", "rejection_reason",
            ],
        )

        write_audit(
            len(rows), len(clean_rows), len(rejected_rows),
            "SUCCESS", "Extract and transform completed",
        )
        logging.info(
            "Pipeline SUCCESS | input=%s clean=%s rejected=%s",
            len(rows), len(clean_rows), len(rejected_rows),
        )

        print("Pipeline status: SUCCESS")
        print("Input rows:", len(rows))
        print("Clean rows:", len(clean_rows))
        print("Rejected rows:", len(rejected_rows))
        print("Reconciliation:", len(rows) == len(clean_rows) + len(rejected_rows))

    except Exception as error:
        logging.exception("Pipeline FAILURE")
        try:
            write_audit(
                len(rows), len(clean_rows), len(rejected_rows),
                "FAILURE", str(error),
            )
        except OSError:
            logging.exception("Could not write failure audit")

        print("Pipeline status: FAILURE")
        print("Error:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
