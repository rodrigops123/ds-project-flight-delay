# apps/load_to_db.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import json
import sqlite3
from pathlib import Path
from datetime import datetime

from config.local.settings import DB_PATH, RAW_DATA_DIR, LOGS_DIR
from src.utils.logger import get_logger

logger = get_logger("load_to_db_logger", str(Path(LOGS_DIR) / "load_to_db.log"))

def get_latest_raw_file(raw_data_dir: str) -> Path:
    """Find the latest raw JSON file."""
    raw_path = Path(raw_data_dir)
    json_files = list(raw_path.glob("flights_raw_*.json"))
    if not json_files:
        raise FileNotFoundError(f"No raw JSON files found in {raw_data_dir}")
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"Latest raw file found: {latest_file}")
    return latest_file

def parse_flights_data(json_path: Path) -> list:
    """Parse the JSON file and extract flight data."""
    with open(json_path, "r") as f:
        data = json.load(f)
    
    flights = data.get("data", [])
    
    parsed_records = []
    for flight in flights:
        record = {
            "flight_date": flight.get("flight_date"),
            "flight_status": flight.get("flight_status"),
            "departure_airport": flight.get("departure", {}).get("airport"),
            "departure_scheduled": flight.get("departure", {}).get("scheduled"),
            "arrival_airport": flight.get("arrival", {}).get("airport"),
            "arrival_scheduled": flight.get("arrival", {}).get("scheduled"),
            "airline_name": flight.get("airline", {}).get("name"),
            "flight_number": flight.get("flight", {}).get("number"),
            "flight_depart_delay": flight.get("departure", {}).get("delay"),
            "flight_arrival_delay": flight.get("arrival", {}).get("delay"),
        }
        parsed_records.append(record)
    
    logger.info(f"Parsed {len(parsed_records)} flight records")
    return parsed_records

def create_flights_table(conn: sqlite3.Connection) -> None:
    """Create the flights_raw table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS flights_raw (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_date TEXT,
        flight_status TEXT,
        departure_airport TEXT,
        departure_scheduled TEXT,
        arrival_airport TEXT,
        arrival_scheduled TEXT,
        airline_name TEXT,
        flight_number TEXT,
        flight_depart_delay INTEGER,
        flight_arrival_delay INTEGER
    );
    """
    conn.execute(create_table_sql)
    conn.commit()
    logger.info("flights_raw table ready")

def insert_flights_data(conn: sqlite3.Connection, records: list) -> None:
    """Insert parsed flight records into the database."""
    insert_sql = """
    INSERT INTO flights_raw (
        flight_date,
        flight_status,
        departure_airport,
        departure_scheduled,
        arrival_airport,
        arrival_scheduled,
        airline_name,
        flight_number,
        flight_depart_delay,
        flight_arrival_delay
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    values = [
        (
            r["flight_date"],
            r["flight_status"],
            r["departure_airport"],
            r["departure_scheduled"],
            r["arrival_airport"],
            r["arrival_scheduled"],
            r["airline_name"],
            r["flight_number"],
            r["flight_depart_delay"],
            r["flight_arrival_delay"]
        )
        for r in records
    ]
    
    conn.executemany(insert_sql, values)
    conn.commit()
    logger.info(f"Inserted {len(records)} records into flights_raw")


def drop_duplicates_in_raw_table(conn: sqlite3.Connection) -> None:
    """Remove duplicate records from the flights_raw table."""
    delete_duplicates_sql = """
    DELETE FROM flights_raw
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM flights_raw
        GROUP BY flight_date, flight_status, departure_airport, arrival_airport, airline_name, flight_number
    );
    """
    conn.execute(delete_duplicates_sql)
    conn.commit()
    logger.info("Duplicates removed from flights_raw table")


def main():
    """Main script to load raw JSON into SQLite."""
    logger.info("[START] Loading raw JSON into database")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Prepare DB
    create_flights_table(conn)
    
    # Load latest raw JSON
    latest_file = get_latest_raw_file(RAW_DATA_DIR)
    
    # Parse and insert data
    flight_records = parse_flights_data(latest_file)
    insert_flights_data(conn, flight_records)
    
    drop_duplicates_in_raw_table(conn)
    
    conn.close()
    logger.info("[END] Database loading completed.")

if __name__ == "__main__":
    main()
