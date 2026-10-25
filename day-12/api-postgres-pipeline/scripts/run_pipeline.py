
import os
import logging
from pathlib import Path
from collections import Counter

import psycopg

from fetch_api import fetch_posts
from transform_posts import transform_posts

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "day12_api_db",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
    "connect_timeout": 5,
}

INSERT_SQL = """
    INSERT INTO posts (post_id, user_id, title, body)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (post_id) DO NOTHING
"""


def run_pipeline():
    logging.info("Pipeline started")

    try:
        # 1. Fetch
        raw_posts = fetch_posts()
        logging.info("API records received: %s", len(raw_posts))

        # 2. Validate and transform
        clean_posts, rejected_posts = transform_posts(raw_posts)

        # Detect repeated IDs inside this API batch
        counts = Counter(post["post_id"] for post in clean_posts)
        duplicate_ids = {
            post_id for post_id, count in counts.items() if count > 1
        }

        # Keep only the first record for each post_id
        unique_posts = []
        seen_ids = set()

        for post in clean_posts:
            if post["post_id"] not in seen_ids:
                unique_posts.append(post)
                seen_ids.add(post["post_id"])

        logging.info("Valid records: %s", len(clean_posts))
        logging.info("Rejected records: %s", len(rejected_posts))
        logging.info("Duplicate IDs in API batch: %s", len(duplicate_ids))

        if not unique_posts:
            raise ValueError("No valid unique records to load")

        # 3. Load in one transaction
        inserted = 0

        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for post in unique_posts:
                    cur.execute(
                        INSERT_SQL,
                        (
                            post["post_id"],
                            post["user_id"],
                            post["title"],
                            post["body"],
                        ),
                    )
                    inserted += cur.rowcount

        # Connection context has committed successfully here.

        # 4. Verify after commit
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM posts")
                total_rows = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*)
                    FROM posts
                    WHERE post_id IS NULL
                       OR user_id IS NULL
                       OR title IS NULL
                       OR body IS NULL
                """)
                invalid_rows = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*)
                    FROM (
                        SELECT post_id
                        FROM posts
                        GROUP BY post_id
                        HAVING COUNT(*) > 1
                    ) AS duplicates
                """)
                duplicate_groups = cur.fetchone()[0]

        if invalid_rows != 0 or duplicate_groups != 0:
            raise ValueError("Post-load data quality check failed")

        logging.info(
            "SUCCESS | inserted=%s | total=%s | rejected=%s",
            inserted,
            total_rows,
            len(rejected_posts),
        )

        print("PIPELINE SUCCESS")
        print("API records:", len(raw_posts))
        print("Valid records:", len(clean_posts))
        print("Rejected records:", len(rejected_posts))
        print("Duplicates within API batch:", len(duplicate_ids))
        print("Newly inserted rows:", inserted)
        print("Total rows in database:", total_rows)
        print("Invalid rows:", invalid_rows)
        print("Duplicate ID groups:", duplicate_groups)

    except Exception:
        logging.exception("PIPELINE FAILURE")
        print("PIPELINE FAILED — check logs/pipeline.log")
        raise


if __name__ == "__main__":
    run_pipeline()
