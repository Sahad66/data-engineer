import csv
from pathlib import Path

import requests

URL = "https://jsonplaceholder.typicode.com/posts"

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_DIR / "data" / "posts_clean.csv"

FIELDS = [
    "post_id",
    "user_id",
    "title",
    "title_length",
    "body_length",
]


def fetch_and_transform():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    posts = response.json()

    if not isinstance(posts, list):
        raise ValueError("Expected a list of posts")

    transformed = []

    for post in posts:
        post_id = post.get("id")
        user_id = post.get("userId")
        title = post.get("title")
        body = post.get("body")

        if not isinstance(post_id, int) or post_id <= 0:
            continue

        if not isinstance(user_id, int) or user_id <= 0:
            continue

        if not isinstance(title, str) or not title.strip():
            continue

        if not isinstance(body, str) or not body.strip():
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

    return transformed


def main():
    records = fetch_and_transform()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    with OUTPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        saved_records = list(csv.DictReader(file))

    print("Output file:", OUTPUT_FILE)
    print("Records processed:", len(records))
    print("Records saved:", len(saved_records))
    print("Validation:", "SUCCESS" if len(records) == len(saved_records) else "FAILED")


if __name__ == "__main__":
    try:
        main()
    except (
        requests.exceptions.RequestException,
        ValueError,
        OSError,
        csv.Error,
    ) as error:
        print("Pipeline failed:", error)