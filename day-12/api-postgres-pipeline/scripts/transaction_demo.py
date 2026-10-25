
import os
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "day12_api_db",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
    "connect_timeout": 5,
}


def demonstrate_rollback():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Setup the temporary demo table and commit it
            cur.execute("""
                CREATE TEMP TABLE IF NOT EXISTS transaction_demo (
                    id INTEGER PRIMARY KEY
                )
            """)
            cur.execute("TRUNCATE transaction_demo")
        conn.commit()

        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO transaction_demo (id) VALUES (1)"
                    )
                    cur.execute(
                        "INSERT INTO transaction_demo (id) VALUES (2)"
                    )

                    # Intentional error for learning
                    cur.execute("SELECT 1 / 0")

        except psycopg.Error as error:
            print("Transaction failed:", type(error).__name__)
            print("Transaction rolled back")

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM transaction_demo")
            count = cur.fetchone()[0]

        print("Rows remaining:", count)


if __name__ == "__main__":
    demonstrate_rollback()
