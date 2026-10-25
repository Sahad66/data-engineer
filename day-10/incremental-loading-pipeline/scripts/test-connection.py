import os
import psycopg

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not configured.")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), CURRENT_TIMESTAMP")
        result = cur.fetchone()

print("Database connection successful!")
print("Database:", result[0])
print("Current time:", result[1])
