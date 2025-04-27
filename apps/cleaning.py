# apps/cleaning.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import sqlite3
from pathlib import Path

from config.local.settings import DB_PATH, LOGS_DIR
from src.utils.logger import get_logger

# Set up logger
logger = get_logger("cleaning_logger", str(Path(LOGS_DIR) / "cleaning.log"))

def connect_db(db_path: str) -> sqlite3.Connection:
    """Connect to SQLite database."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    logger.info(f"Connected to database at {db_path}")
    return conn

def clean_data_sql(conn: sqlite3.Connection) -> None:
    """Perform all cleaning steps directly using SQL."""
    logger.info("Starting SQL-based data cleaning")

    with open("src/preprocessing/cleaning.sql", "r") as f:
        cleaning_script = f.read()

    cursor = conn.cursor()
    cursor.executescript(cleaning_script)
    conn.commit()

    logger.info("SQL cleaning script applied and flights_clean table created")

def main():
    logger.info("[START] SQL Data cleaning pipeline")
    
    # Connect to DB
    conn = connect_db(DB_PATH)
    
    # Run SQL cleaning
    clean_data_sql(conn)
    
    conn.close()
    logger.info("[END] SQL Data cleaning pipeline completed.")

if __name__ == "__main__":
    main()