import os
import logging
from pathlib import Path

import psycopg


# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "incremental_pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

PIPELINE_NAME = "python_orders_pipeline"


def run_pipeline():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not configured.")

    rows_processed = 0

    try:
        # autocommit lets us write the audit record
        # after the data transaction succeeds or fails.
        with psycopg.connect(
            database_url,
            autocommit=True,
        ) as conn:

            # Data changes and checkpoint update are atomic.
            with conn.transaction():
                with conn.cursor() as cur:

                    # 1. Read the previous checkpoint.
                    cur.execute(
                        """
                        SELECT last_loaded_at
                        FROM day10_incremental.etl_watermark
                        WHERE pipeline_name = %s
                        FOR UPDATE
                        """,
                        (PIPELINE_NAME,),
                    )

                    watermark_row = cur.fetchone()

                    if watermark_row is None:
                        raise ValueError(
                            "Watermark not found. "
                            "Initialize the checkpoint first."
                        )

                    last_loaded_at = watermark_row[0]

                    logger.info(
                        "Starting pipeline. Watermark: %s",
                        last_loaded_at,
                    )

                    # 2. Read new or changed source rows.
                    cur.execute(
                        """
                        SELECT order_id, customer_id, amount, updated_at
                        FROM day10_incremental.orders_source
                        WHERE updated_at > %s
                        ORDER BY updated_at, order_id
                        """,
                        (last_loaded_at,),
                    )

                    source_rows = cur.fetchall()

                    # 3. UPSERT into the target.
                    if source_rows:
                        cur.executemany(
                            """
                            INSERT INTO day10_incremental.orders_target
                                (order_id, customer_id, amount, updated_at)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (order_id)
                            DO UPDATE SET
                                customer_id = EXCLUDED.customer_id,
                                amount = EXCLUDED.amount,
                                updated_at = EXCLUDED.updated_at
                            WHERE EXCLUDED.updated_at >
                                  day10_incremental.orders_target.updated_at
                            """,
                            source_rows,
                        )

                        rows_processed = len(source_rows)

                        # 4. Advance checkpoint only after
                        # processing succeeds, in the same transaction.
                        new_watermark = max(
                            row[3] for row in source_rows
                        )

                        cur.execute(
                            """
                            UPDATE day10_incremental.etl_watermark
                            SET last_loaded_at = %s
                            WHERE pipeline_name = %s
                            """,
                            (new_watermark, PIPELINE_NAME),
                        )

            # Transaction committed successfully here.
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO day10_incremental.etl_audit
                        (pipeline_name, status, rows_processed)
                    VALUES (%s, %s, %s)
                    """,
                    (PIPELINE_NAME, "SUCCESS", rows_processed),
                )

        logger.info(
            "Pipeline SUCCESS. Rows processed: %s",
            rows_processed,
        )

    except Exception as exc:
        logger.exception("Pipeline FAILED")

        # Record failure after the failed data transaction
        # has been rolled back.
        try:
            with psycopg.connect(
                database_url,
                autocommit=True,
            ) as audit_conn:
                with audit_conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO day10_incremental.etl_audit
                            (pipeline_name, status,
                             rows_processed, error_message)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            PIPELINE_NAME,
                            "FAILURE",
                            rows_processed,
                            str(exc)[:4000],
                        ),
                    )

        except Exception:
            logger.exception("Could not write failure audit record")

        raise


if __name__ == "__main__":
    run_pipeline()