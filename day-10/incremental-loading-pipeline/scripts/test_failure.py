import os
import psycopg

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not configured.")

try:
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM day10_incremental.table_that_does_not_exist"
            )

except Exception as error:
    print("Expected test failure captured.")
    print(type(error).__name__)
    print(error)