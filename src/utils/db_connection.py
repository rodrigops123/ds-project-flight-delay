import sqlite3
from pathlib import Path
from config.local.settings import DB_PATH, LOGS_DIR
from src.utils.logger import get_logger

# Set up logger
logger = get_logger("db_connection_logger", str(Path(LOGS_DIR) / "db_connection.log"))


def connect_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Connect to SQLite database."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    logger.info(f"Connected to database at {db_path}")
    return conn
