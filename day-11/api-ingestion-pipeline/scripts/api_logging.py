import logging
from pathlib import Path

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

logger.info("API pipeline started")
logger.info("Requesting API data")
logger.info("API pipeline completed successfully")

print("Logging setup completed")
print("Log file:", LOG_FILE)