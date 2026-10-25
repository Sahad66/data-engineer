import csv
import logging
from pathlib import Path

import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
LOG_DIR = PROJECT_DIR / "logs"

OUTPUT_FILE = DATA_DIR / "posts_clean.csv"
LOG_FILE = LOG_DIR / "api_pipeline.log"

URL = "https://jsonplaceholder.typicode.com/posts"

FIELDS = [
    "post_id",
    "user_id",
    "title",
    "title_length",
    "body_length",
]

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True,
)

logger = logging.getLogger(__name__)


def fetch_data():
    logger.info("Fetching data from API")

    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("API response must be a list")

    logger.info("Received %s raw records", len(data))
    return data


def transform_data(raw_records):
    transformed = []
    rejected = 0

    for record in raw_records:
        post_id = record.get("id")
        user_id = record.get("userId")
        title = record.get("title")
        body = record.get("body")

        valid_id = (
            isinstance(post_id, int)
            and not isinstance(post_id, bool)
            and post_id > 0
        )

        valid_user = (
            isinstance(user_id, int)
            and not isinstance(user_id, bool)
            and user_id > 0
        )

        valid_title = (
            isinstance(title, str)
            and bool(title.strip())
        )

        valid_body = (
            isinstance(body, str)
            and bool(body.strip())
        )

        if not all([valid_id, valid_user, valid_title, valid_body]):
            rejected += 1
            continue

        title = title.strip()
        body = body.strip()

        transformed.append({
            "post_id": post_id,
            "user_id": user_id,
            "title": title,
            "title_length": len(title),
            "body_length": len(body),
        })

    logger.info(
        "Transformation completed | clean=%s | rejected=%s",
        len(transformed),
        rejected,
    )

    return transformed, rejected


def save_and_validate(records):
    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    with OUTPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        saved_records = list(csv.DictReader(file))

    if len(records) != len(saved_records):
        raise ValueError("Saved record count does not match")

    return len(saved_records)


def main():
    logger.info("Pipeline started")

    try:
        raw_records = fetch_data()
        clean_records, rejected = transform_data(raw_records)
        saved_count = save_and_validate(clean_records)

        logger.info(
            "Pipeline SUCCESS | raw=%s | clean=%s | rejected=%s | saved=%s",
            len(raw_records),
            len(clean_records),
            rejected,
            saved_count,
        )

        print("Pipeline status: SUCCESS")
        print("Raw records:", len(raw_records))
        print("Clean records:", len(clean_records))
        print("Rejected records:", rejected)
        print("Saved records:", saved_count)
        print("CSV:", OUTPUT_FILE)
        print("Log:", LOG_FILE)

    except Exception:
        logger.exception("Pipeline FAILURE")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Pipeline failed:", error)
        print("See log file for details.")