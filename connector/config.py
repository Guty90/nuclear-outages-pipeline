import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

API_KEY    = os.getenv("EIA_API_KEY", "") 
BASE_URL   = "https://api.eia.gov/v2/nuclear-outages" 
PAGE_SIZE = 5000 # Number of records to fetch per API request (max allowed by EIA is 5000)
MAX_RETRIES = 3 # Maximum number of retries for API requests in case of failures
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# ── Date range ───────────────────────────────────────
START_YEAR  = 2015  
END_YEAR    = 2026

DATASETS = { 
    "facility": {
        "endpoint": "/facility-nuclear-outages/data/", # Specific endpoint for facility outages
        "file":     "facility_outages.parquet", # Output file name for facility outages
        "required": ["period", "facility", "facilityName", 
                     "capacity", "outage", "percentOutage"], # Required fields for facility outages dataset
    },
    "generator": {
        "endpoint": "/generator-nuclear-outages/data/",
        "file":     "generator_outages.parquet",
        "required": ["period", "facility", "facilityName",
                     "generator", "capacity", "outage", "percentOutage"],
    },
}

def validate_api_key(): # Function to validate that the API key is configured
    if not API_KEY:
        raise ValueError(
            "EIA_API_KEY is not configured. Please set the EIA_API_KEY environment variable with your EIA API key."
        )