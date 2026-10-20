
import psycopg
from getpass import getpass

# Database connection information
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "de_day1"
DB_USER = "postgres"

# Password code-এর মধ্যে লিখছি না
DB_PASSWORD = getpass("PostgreSQL password: ")

try:
    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5,
    ) as conn:

        with conn.cursor() as cur:
            # Database connection test
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]

            print("\nConnection successful!")
            print("Database:", DB_NAME)
            print("PostgreSQL version:", version.split(",")[0])

            # Sales data check
            cur.execute("""
                SELECT
                    COUNT(*) AS total_records,
                    COALESCE(
                        SUM(quantity * unit_price), 0
                    ) AS total_revenue
                FROM sales;
            """)

            total_records, total_revenue = cur.fetchone()

            print("Total records:", total_records)
            print("Total revenue:", total_revenue)

except psycopg.OperationalError as error:
    print("\nConnection failed.")
    print("Check the server, port, username, password, and database.")
    print("Error:", error)

except psycopg.Error as error:
    print("\nDatabase query failed.")
    print("Error:", error)