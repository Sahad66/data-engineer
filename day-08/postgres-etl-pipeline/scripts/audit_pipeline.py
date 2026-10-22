
import csv
import getpass
import logging
import os
import sys
from decimal import Decimal
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = DATA_DIR / "orders.csv"
CLEAN_FILE = DATA_DIR / "clean_orders.csv"
REJECTED_FILE = DATA_DIR / "rejected_orders.csv"

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    password = getpass.getpass("PostgreSQL password: ")
    run_id = None

    connection_settings = {
        "dbname": os.getenv("PGDATABASE", "day8_etl"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": password,
        "host": os.getenv("PGHOST", "localhost"),
        "port": os.getenv("PGPORT", "5432"),
    }

    try:
        # Create the audit record first, so the run can be tracked.
        with psycopg.connect(**connection_settings) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO etl_audit (pipeline_name, status, message)
                    VALUES (%s, %s, %s)
                    RETURNING run_id
                    """,
                    ("day8_orders_pipeline", "RUNNING", "Pipeline started"),
                )
                run_id = cur.fetchone()[0]

        logger.info("Pipeline started; run_id=%s", run_id)

        input_rows = read_csv(INPUT_FILE)
        clean_rows = read_csv(CLEAN_FILE)
        rejected_rows = read_csv(REJECTED_FILE)

        input_count = len(input_rows)
        clean_count = len(clean_rows)
        rejected_count = len(rejected_rows)

        if input_count != clean_count + rejected_count:
            raise ValueError(
                f"Reconciliation failed: input={input_count}, "
                f"clean={clean_count}, rejected={rejected_count}"
            )

        inserted_count = 0

        with psycopg.connect(**connection_settings) as conn:
            with conn.cursor() as cur:
                for row in clean_rows:
                    cur.execute(
                        """
                        INSERT INTO clean_orders
                            (order_id, customer_id, quantity, unit_price)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (order_id) DO NOTHING
                        """,
                        (
                            int(row["order_id"]),
                            row["customer_id"].strip(),
                            int(row["quantity"]),
                            Decimal(row["unit_price"]),
                        ),
                    )
                    inserted_count += cur.rowcount

                cur.execute(
                    """
                    UPDATE etl_audit
                    SET finished_at = CURRENT_TIMESTAMP,
                        input_rows = %s,
                        clean_rows = %s,
                        rejected_rows = %s,
                        inserted_rows = %s,
                        status = 'SUCCESS',
                        message = %s
                    WHERE run_id = %s
                    """,
                    (
                        input_count,
                        clean_count,
                        rejected_count,
                        inserted_count,
                        "Reconciliation passed",
                        run_id,
                    ),
                )

        logger.info(
            "Pipeline successful; run_id=%s input=%s clean=%s "
            "rejected=%s inserted=%s",
            run_id, input_count, clean_count,
            rejected_count, inserted_count,
        )

        print(f"Run ID: {run_id}")
        print(f"Input rows: {input_count}")
        print(f"Clean rows: {clean_count}")
        print(f"Rejected rows: {rejected_count}")
        print(f"Inserted rows: {inserted_count}")
        print("Reconciliation: PASS")
        print("Status: SUCCESS")

    except Exception as error:
        logger.exception("Pipeline failed; run_id=%s", run_id)

        if run_id is not None:
            try:
                with psycopg.connect(**connection_settings) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            UPDATE etl_audit
                            SET finished_at = CURRENT_TIMESTAMP,
                                status = 'FAILURE',
                                message = %s
                            WHERE run_id = %s
                            """,
                            (str(error)[:2000], run_id),
                        )
            except Exception:
                logger.exception("Could not update failure audit record")

        print(f"Pipeline failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
