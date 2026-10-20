
import csv
import logging
from pathlib import Path
import sys

# 1. Project folder খুঁজে বের করা
project_dir = Path(__file__).resolve().parent.parent
csv_file = project_dir / "data" / "ecommerce_orders.csv"
#csv_file = project_dir / "data" / "missing_file.csv"
log_dir = project_dir / "logs"

# 2. Log folder তৈরি করা
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "safe_csv_pipeline.log"

# 3. Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)

def run_pipeline():
    logging.info("Pipeline started.")
    logging.info("Reading CSV: %s", csv_file)

    try:
        with open(
            csv_file,
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV header is missing.")

            required_columns = [
                "order_id",
                "customer_id",
                "quantity",
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in reader.fieldnames
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing columns: {missing_columns}"
                )

            rows = list(reader)

        logging.info("CSV schema validation passed.")
        logging.info("Total rows loaded: %s", len(rows))
        logging.info("Pipeline completed successfully.")

    except (FileNotFoundError, PermissionError, ValueError):
        logging.exception("Pipeline failed.")
        raise SystemExit(1)

    except OSError:
        logging.exception("Unexpected file operation error.")
        raise SystemExit(1)


if __name__ == "__main__":
    run_pipeline()
