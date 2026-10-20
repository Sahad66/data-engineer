
import csv
import logging
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / "data" / "orders.csv"
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "ingestion.log",
            encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
    force=True,
)

def main():
    logging.info("INGESTION_STARTED")

    try:
        with open(SOURCE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV header is missing")

            rows = list(reader)

        logging.info("INGESTION_SUCCESS rows=%s", len(rows))
        print("Total rows:", len(rows))

    except (OSError, csv.Error, ValueError):
        logging.exception("INGESTION_FAILED")
        raise

    finally:
        logging.info("INGESTION_FINISHED")

if __name__ == "__main__":
    main()
