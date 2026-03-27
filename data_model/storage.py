import os
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(BASE_DIR, "data", "processed")

OUTPUT_FILES = {
    "facilities":        "facilities.parquet",
    "facility_outages":  "facility_outages_clean.parquet",
    "generator_outages": "generator_outages_clean.parquet",
}


def save_table(df: pd.DataFrame, table: str) -> None:
    """Save a DataFrame to a parquet file"""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join(DATA_DIR, OUTPUT_FILES[table])
    df.to_parquet(path, index=False)
    logger.info(f"Saved {len(df)} records → {path}")