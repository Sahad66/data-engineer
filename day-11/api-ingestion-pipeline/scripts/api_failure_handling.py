import logging
from pathlib import Path

import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_DIR / "logs" / "api_pipeline.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True,
)

logger = logging.getLogger(__name__)

URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_posts():
    logger.info("API request started")

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        posts = response.json()

        if not isinstance(posts, list):
            raise ValueError("Expected a list from API")

        logger.info("API request successful: %s records", len(posts))
        return posts

    except (requests.exceptions.RequestException, ValueError):
        logger.exception("API ingestion failed")
        raise


if __name__ == "__main__":
    try:
        posts = fetch_posts()
        print("SUCCESS: Records received:", len(posts))

    except (requests.exceptions.RequestException, ValueError):
        print("FAILURE: Check logs/api_pipeline.log")