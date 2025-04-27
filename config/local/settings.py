# config/local/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# API key (load it securely from environment variable or paste it here for local dev)
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# Airport code to filter departures (e.g., "JFK", "SFO", "LHR")
AIRPORT_CODE = "VIX"

BASE_DIR = Path(__file__).resolve().parents[2]

# Output directory for raw data
OUTPUT_DIR = str(BASE_DIR / "data" / "raw")
RAW_DATA_DIR = str(BASE_DIR / "data" / "raw")
DB_PATH = str(BASE_DIR / "data" / "processed" / "flights.db")
LOGS_DIR = str(BASE_DIR / "logs")