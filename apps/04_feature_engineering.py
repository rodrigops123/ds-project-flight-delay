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
logger = get_logger("feat_eng_logger", str(Path(LOGS_DIR) / "feat_eng.log"))

def clean_data_sql(conn: sqlite3.Connection) -> None:
    """Perform all feature engineering steps directly using SQL."""
    logger.info("Starting SQL-based data feature engineering")

    with open("src/features/feature_engineering.sql", "r") as f:
        feature_engineering_script = f.read()

    cursor = conn.cursor()
    cursor.executescript(feature_engineering_script)
    conn.commit()

    logger.info("SQL feature engineering script applied and flights_transformed table created")

def main():
    logger.info("[START] SQL Data feature engineering pipeline")
    
    # Connect to DB
    conn = connect_db()
    
    # Run SQL feature engineering
    clean_data_sql(conn)
    
    conn.close()
    logger.info("[END] SQL Data feature engineering pipeline completed.")

if __name__ == "__main__":
    main()