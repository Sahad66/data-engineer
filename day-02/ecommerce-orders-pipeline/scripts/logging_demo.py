
import logging
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
log_dir = project_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "logging_demo.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)

logging.info("Pipeline started.")
logging.info("CSV validation completed.")
logging.warning("Raw data contains known quality issues.")
logging.error("Demo error message.")
logging.info("Logging demonstration finished.")

print(f"Log file saved at: {log_file}")
