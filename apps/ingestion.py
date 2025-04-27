# apps/ingestion.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import requests
import json
from datetime import datetime
from pathlib import Path

# Read config variables
from config.local.settings import API_KEY, AIRPORT_CODE, OUTPUT_DIR, LOGS_DIR
from src.utils.logger import get_logger

logger = get_logger("ingestion_logger", str(Path(LOGS_DIR) / "ingestion.log"))

def fetch_flights(api_key: str, airport_code: str) -> dict:
    """Fetch flight data for a specific airport using AviationStack API."""
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "dep_iata": airport_code,  # departure airport code
        "limit": 100,  # Max records per request (AviationStack free tier limits it anyway)
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        logger.info(f"Successfully fetched data for airport {airport_code}")
        return response.json()
    else:
        logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return {}

def save_raw_data(data: dict, output_dir: str) -> None:
    """Save raw JSON data into a timestamped file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"flights_raw_{timestamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    
    logger.info(f"Saved raw data to {output_path}")

def main():
    """Main ingestion pipeline."""
    logger.info("[START] Flight data ingestion pipeline")
    
    flights_data = fetch_flights(API_KEY, AIRPORT_CODE)
    
    if flights_data:
        save_raw_data(flights_data, OUTPUT_DIR)
    
    logger.info("[END] Ingestion pipeline completed.")

if __name__ == "__main__":
    main()