
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

def test_connection():
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]

                cur.execute("SELECT current_database();")
                database_name = cur.fetchone()[0]

                print("Connection successful!")
                print("Database:", database_name)
                print("PostgreSQL version:", version)

    except psycopg.OperationalError as error:
        print("Connection failed!")
        print("Check server, port, database, username, and password.")
        print("Error:", error)

    except psycopg.Error as error:
        print("PostgreSQL error:", error)


if __name__ == "__main__":
    test_connection()
