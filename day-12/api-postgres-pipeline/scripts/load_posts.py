
import os

import psycopg

from fetch_api import fetch_posts
from transform_posts import transform_posts

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "day12_api_db",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
    "connect_timeout": 5,
}


def load_posts():
    # Step 1: Fetch API data
    raw_posts = fetch_posts()

    # Step 2: Validate and transform
    clean_posts, rejected_posts = transform_posts(raw_posts)

    if not clean_posts:
        raise ValueError("No valid records to load")

    insert_sql = """
        INSERT INTO posts (post_id, user_id, title, body)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (post_id) DO NOTHING
    """

    inserted_count = 0

    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for post in clean_posts:
                    cur.execute(
                        insert_sql,
                        (
                            post["post_id"],
                            post["user_id"],
                            post["title"],
                            post["body"],
                        ),
                    )

                    # With DO NOTHING, rowcount is 0 for duplicates
                    inserted_count += cur.rowcount

        print("Database load successful!")
        print("Valid records:", len(clean_posts))
        print("Rejected records:", len(rejected_posts))
        print("Newly inserted rows:", inserted_count)
        print("Skipped existing IDs:", len(clean_posts) - inserted_count)

    except psycopg.Error as error:
        print("Database load failed:", error)
        raise


if __name__ == "__main__":
    load_posts()
