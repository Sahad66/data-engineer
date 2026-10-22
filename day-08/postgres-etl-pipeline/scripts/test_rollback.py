
import getpass
import os

import psycopg
from psycopg import Error


def main():
    password = getpass.getpass("PostgreSQL password: ")

    try:
        with psycopg.connect(
            dbname=os.getenv("PGDATABASE", "day8_etl"),
            user=os.getenv("PGUSER", "postgres"),
            password=password,
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
        ) as conn:
            with conn.cursor() as cur:
                # This row is for testing only.
                cur.execute(
                    """
                    INSERT INTO clean_orders
                        (order_id, customer_id, quantity, unit_price)
                    VALUES (99001, 'TEST', 1, 10.00)
                    """
                )

                # Intentional duplicate causes a primary-key error.
                cur.execute(
                    """
                    INSERT INTO clean_orders
                        (order_id, customer_id, quantity, unit_price)
                    VALUES (99001, 'TEST', 1, 10.00)
                    """
                )

    except Error as error:
        print("Expected test failure:", error.__class__.__name__)
        print("Transaction rolled back.")

    with psycopg.connect(
        dbname=os.getenv("PGDATABASE", "day8_etl"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM clean_orders WHERE order_id = 99001"
            )
            count = cur.fetchone()[0]
            print(f"Test rows remaining: {count}")


if __name__ == "__main__":
    main()
