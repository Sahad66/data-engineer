import csv
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "extraction.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "quantity",
    "unit_price",
}


def extract_csv(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV header is missing")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        rows = list(reader)

    return rows


def main():
    logging.info("CSV extraction started")

    try:
        file_path = BASE_DIR / "data" / "orders.csv"
        rows = extract_csv(file_path)

        logging.info("Extraction successful: %s rows", len(rows))
        print("Extraction successful")
        print("Total rows:", len(rows))

    except (FileNotFoundError, ValueError, OSError) as error:
        logging.exception("CSV extraction failed")
        print("Extraction failed:", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
