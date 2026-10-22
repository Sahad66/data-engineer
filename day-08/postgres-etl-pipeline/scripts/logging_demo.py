
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Pipeline started")

    try:
        input_file = BASE_DIR / "data" / "orders.csv"

        if not input_file.exists():
            raise FileNotFoundError(f"Missing file: {input_file}")

        logger.info("Input CSV found")
        print("Input CSV found")
        logger.info("Pipeline check completed successfully")

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    main()
