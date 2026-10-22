
import os
import sys
import getpass

import psycopg


def main():
    db_name = os.getenv("PGDATABASE", "day7_etl")
    db_user = os.getenv("PGUSER", "postgres")
    db_host = os.getenv("PGHOST", "localhost")
    db_port = os.getenv("PGPORT", "5432")

    password = getpass.getpass("PostgreSQL password: ")

    try:
        with psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=password,
            host=db_host,
            port=db_port,
            connect_timeout=5,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT current_database(), current_user;"
                )
                database, user = cur.fetchone()

                print("Connection successful!")
                print(f"Database: {database}")
                print(f"User: {user}")

    except psycopg.Error as error:
        print(f"Connection failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
