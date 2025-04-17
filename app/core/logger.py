import sys
from pathlib import Path
from loguru import logger

LOG_FILE = Path("app.log")

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, format="[{time}] [{level}] {message}", level="INFO")
    logger.add(LOG_FILE, format="[{time}] [{level}] {message}", rotation="10 MB", retention="14 days", level="DEBUG")
