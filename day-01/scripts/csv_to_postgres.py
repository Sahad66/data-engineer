
import csv
from pathlib import Path
from datetime import date
from decimal import Decimal

project_dir = Path(__file__).resolve().parent.parent
csv_file = project_dir / "data" / "sales.csv"

required_columns = {
    "sale_id", "sale_date", "product", "category",
    "quantity", "unit_price", "city"
}

records = []

with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
        raise ValueError("CSV header is missing required columns.")

    for line_number, row in enumerate(reader, start=2):
        try:
            if any(not row[col] or not row[col].strip()
                   for col in required_columns):
                raise ValueError("Missing required value")

            sale_id = int(row["sale_id"])
            sale_date = date.fromisoformat(row["sale_date"])
            product = row["product"].strip()
            category = row["category"].strip()
            quantity = int(row["quantity"])
            unit_price = Decimal(row["unit_price"])
            city = row["city"].strip()

            if sale_id <= 0 or quantity <= 0 or unit_price < 0:
                raise ValueError("Invalid ID, quantity, or price")

            records.append((
                sale_id, sale_date, product, category,
                quantity, unit_price, city
            ))

        except (ValueError, ArithmeticError) as error:
            raise ValueError(
                f"Invalid data at CSV line {line_number}: {error}"
            ) from error

print("CSV records read:", len(records))
print("Data validation: PASSED")


import psycopg
from getpass import getpass

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "de_day1"
DB_USER = "postgres"

DB_PASSWORD = getpass("PostgreSQL password: ")

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

with psycopg.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    connect_timeout=5,
) as conn:
    with conn.cursor() as cur:
        cur.executemany(insert_sql, records)

        cur.execute("""
            SELECT
                COUNT(*) AS total_records,
                SUM(quantity * unit_price) AS total_revenue
            FROM sales;
        """)

        total_records, total_revenue = cur.fetchone()

print("Load completed successfully!")
print("Rows processed:", len(records))
print("Database total records:", total_records)
print("Database total revenue:", total_revenue)

import logging
log_dir = project_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(
            log_dir / "sales_pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)
logger.info("Sales pipeline started")

logger.info("CSV records read: %s", len(records))
logger.info("Data validation passed")


logger.info("Rows processed: %s", len(records))
logger.info("Database total records: %s", total_records)
logger.info("Database total revenue: %s", total_revenue)
logger.info("Sales pipeline completed")