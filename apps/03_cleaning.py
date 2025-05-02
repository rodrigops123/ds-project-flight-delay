# apps/cleaning.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import sqlite3
from pathlib import Path

from config.local.settings import LOGS_DIR
from src.utils.logger import get_logger
from src.utils.db_connection import connect_db

# Set up logger
logger = get_logger("cleaning_logger", str(Path(LOGS_DIR) / "cleaning.log"))

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
    conn = connect_db()
    
    # Run SQL cleaning
    clean_data_sql(conn)
    
    conn.close()
    logger.info("[END] SQL Data cleaning pipeline completed.")

if __name__ == "__main__":
    main()