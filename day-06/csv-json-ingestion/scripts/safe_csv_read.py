
import csv
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
csv_file = PROJECT_DIR / "data" / "missing_orders.csv"

try:
    with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))
        logging.info("CSV loaded successfully: %s rows", len(rows))

except FileNotFoundError:
    logging.error("CSV file not found: %s", csv_file)

except PermissionError:
    logging.error("Permission denied: %s", csv_file)

except csv.Error:
    logging.exception("CSV parsing failed")
