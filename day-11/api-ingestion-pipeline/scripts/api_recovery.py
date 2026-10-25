import csv
import logging
from pathlib import Path

import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "api_pipeline.log"
OUTPUT_FILE = PROJECT_DIR / "data" / "posts_clean.csv"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True,
)

logger = logging.getLogger(__name__)

URL = "https://jsonplaceholder.typicode.com/posts"

FIELDS = [
    "post_id",
    "user_id",
    "title",
    "title_length",
    "body_length",
]


def run_pipeline():
    logger.info("Pipeline run started")

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Expected a list of posts")

        clean_records = []

        for post in posts:
            post_id = post.get("id")
            user_id = post.get("userId")
            title = post.get("title")
            body = post.get("body")

            if not isinstance(post_id, int) or isinstance(post_id, bool):
                continue

            if not isinstance(user_id, int) or isinstance(user_id, bool):
                continue

            if post_id <= 0 or user_id <= 0:
                continue

            if not isinstance(title, str) or not title.strip():
                continue

            if not isinstance(body, str) or not body.strip():
                continue

            title = title.strip()
            body = body.strip()

            clean_records.append({
                "post_id": post_id,
                "user_id": user_id,
                "title": title,
                "title_length": len(title),
                "body_length": len(body),
            })

        with OUTPUT_FILE.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(clean_records)

        with OUTPUT_FILE.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            saved_records = list(csv.DictReader(file))

        if len(clean_records) != len(saved_records):
            raise ValueError("CSV row count validation failed")

        logger.info(
            "Pipeline SUCCESS | processed=%s | saved=%s",
            len(clean_records),
            len(saved_records),
        )

        print("Pipeline status: SUCCESS")
        print("Records processed:", len(clean_records))
        print("Records saved:", len(saved_records))
        print("Output file:", OUTPUT_FILE)

    except Exception:
        logger.exception("Pipeline FAILURE")
        raise


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as error:
        print("Pipeline failed:", error)
        print("Check logs/api_pipeline.log")