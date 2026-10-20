
import logging
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
log_dir = project_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "sales_pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)

logger.info("Pipeline started")
logger.info("Logging setup successful")