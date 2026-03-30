import os
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# Files
FACILITIES_FILE = os.path.join(PROCESSED_DIR, "facilities.parquet")
FACILITY_FILE  = os.path.join(PROCESSED_DIR, "facility_outages_clean.parquet")
GENERATOR_FILE = os.path.join(PROCESSED_DIR, "generator_outages_clean.parquet")
SUMMARY_FILE    = os.path.join(PROCESSED_DIR, "facility_summary.parquet")    
SEASONALITY_FILE = os.path.join(PROCESSED_DIR, "seasonality.parquet")        
US_TOTAL_FILE   = os.path.join(PROCESSED_DIR, "us_total.parquet")            


# Auth
APP_API_KEY = os.getenv("APP_API_KEY", "")

# Scripts
CONNECTOR_SCRIPT  = os.path.join(BASE_DIR, "connector", "main.py")
DATA_MODEL_SCRIPT = os.path.join(BASE_DIR, "data_model", "main.py")