
import csv
import logging
import getpass
from pathlib import Path
from datetime import date
from decimal import Decimal

import psycopg


# 1. Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "sales.csv"
LOG_DIR = PROJECT_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)


# 2. Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "sales_pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)


# 3. Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "de_day1",
    "user": "postgres",
}


# 4. Read and validate CSV
def read_sales_csv():
    records = []

    required_columns = {
        "sale_id",
        "sale_date",
        "product",
        "category",
        "quantity",
        "unit_price",
        "city",
    }

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV is missing required columns")

        for row in reader:
            sale_id = int(row["sale_id"])
            sale_date = date.fromisoformat(row["sale_date"])
            product = row["product"].strip()
            category = row["category"].strip()
            quantity = int(row["quantity"])
            unit_price = Decimal(row["unit_price"])
            city = row["city"].strip()

            if sale_id <= 0:
                raise ValueError("sale_id must be positive")

            if not product or not category or not city:
                raise ValueError("Product, category and city are required")

            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            if unit_price < 0:
                raise ValueError("Unit price cannot be negative")

            records.append((
                sale_id,
                sale_date,
                product,
                category,
                quantity,
                unit_price,
                city,
            ))

    if not records:
        raise ValueError("CSV contains no sales records")

    logger.info("CSV validated: %s records", len(records))
    return records


# 5. Insert or update sales data
def load_sales(password, records):
    insert_sql = """
        INSERT INTO sales (
            sale_id, sale_date, product, category,
            quantity, unit_price, city
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (sale_id) DO UPDATE SET
            sale_date = EXCLUDED.sale_date,
            product = EXCLUDED.product,
            category = EXCLUDED.category,
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price,
            city = EXCLUDED.city;
    """

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        with conn.cursor() as cur:
            cur.executemany(insert_sql, records)

    logger.info("Sales data loaded successfully")


# 6. Write pipeline run details to audit table
def write_audit(password, status, rows_processed, error_message=None):
    audit_sql = """
        INSERT INTO pipeline_audit (
            pipeline_name,
            status,
            rows_processed,
            error_message
        )
        VALUES (%s, %s, %s, %s);
    """

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute(
                audit_sql,
                (
                    "sales_csv_to_postgres",
                    status,
                    rows_processed,
                    error_message,
                ),
            )

    logger.info("Audit saved: status=%s", status)


# 7. Run the pipeline
def main():
    password = getpass.getpass("PostgreSQL password: ")
    rows_processed = 0

    logger.info("Pipeline started")

    try:
        records = read_sales_csv()
        load_sales(password, records)

        # Number of records processed in this run
        rows_processed = len(records)

        write_audit(
            password,
            "SUCCESS",
            rows_processed
        )

        logger.info("Pipeline completed successfully")

    except Exception as error:
        logger.exception("Pipeline failed")

        try:
            write_audit(
                password,
                "FAILED",
                rows_processed,
                str(error)[:2000]
            )
        except Exception:
            logger.exception("Could not save failure audit")

        raise


if __name__ == "__main__":
    main()