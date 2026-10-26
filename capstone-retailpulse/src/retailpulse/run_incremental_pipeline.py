import os
import sys
from pathlib import Path
from getpass import getpass

import psycopg


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_FILE = PROJECT_ROOT / "sql" / "incremental" / "02_first_incremental_load.sql"

PIPELINE_NAME = "retailpulse_incremental_demo"


def get_connection():
    """Connect to PostgreSQL using environment settings or user input."""

    password = os.getenv("PGPASSWORD")

    if not password:
        password = getpass("PostgreSQL password: ")

    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "retailpulse"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
    )


def log_failure(error_message):
    """Write a FAILED audit record in a separate transaction."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit.incremental_demo_runs (
                    pipeline_name,
                    completed_at,
                    status,
                    error_message
                )
                VALUES (
                    %s,
                    CURRENT_TIMESTAMP,
                    'FAILED',
                    %s
                );
                """,
                (PIPELINE_NAME, error_message[:2000]),
            )


def run_pipeline():
    """Execute the incremental SQL and report its outcome."""

    if not SQL_FILE.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

    sql_script = SQL_FILE.read_text(encoding="utf-8")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_script)

        print("Pipeline status: SUCCESS")
        print("Incremental SQL executed successfully.")

    except Exception as exc:
        print("Pipeline status: FAILED")
        print(f"Error: {exc}")

        try:
            log_failure(str(exc))
            print("Failure recorded in audit log.")
        except Exception as audit_exc:
            print(f"Could not write failure audit: {audit_exc}")

        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()