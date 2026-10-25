
import os
from pathlib import Path

import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "day12_api_db",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
    "connect_timeout": 5,
}

SQL_FILE = (
    Path(__file__).resolve().parent.parent
    / "sql"
    / "create_tables.sql"
)

def create_table():
    try:
        sql = SQL_FILE.read_text(encoding="utf-8")

        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

        print("Table creation successful!")

    except FileNotFoundError:
        print("SQL file not found:", SQL_FILE)

    except psycopg.Error as error:
        print("Database operation failed:", error)

if __name__ == "__main__":
    create_table()
