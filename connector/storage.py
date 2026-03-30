import os
import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime, date
from config import DATA_DIR, DATASETS, METADATA_FILE, MERGE_KEYS

logger = logging.getLogger(__name__)


def read_metadata() -> dict | None:
    """Read metadata.json to get last extraction info"""
    if not os.path.exists(METADATA_FILE):
        return None
    with open(METADATA_FILE) as f:
        return json.load(f)


def save_metadata(facility_count: int, generator_count: int, refresh_count: int) -> None:
    """Update metadata.json after each extraction"""
    metadata = {
        "last_extraction_date": date.today().strftime("%Y-%m-%d"),
        "last_run_at":          datetime.now().isoformat(),
        "facility_records":     facility_count,
        "generator_records":    generator_count,
        "refresh_count":        refresh_count,
    }
    Path(METADATA_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Metadata updated → {METADATA_FILE}")


def save_to_parquet(records: list[dict], dataset: str) -> None:
    """Save records to a parquet file"""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    path   = os.path.join(DATA_DIR, DATASETS[dataset]["file"])
    new_df = pd.DataFrame(records)
    keys   = MERGE_KEYS[dataset]

    # Nothing to save
    if new_df.empty:
        logger.info(f"[{dataset}] No new records to save, skipping.")
        return

    if not os.path.exists(path):
        # First run → create parquet
        new_df.to_parquet(path, index=False)
        logger.info(f"[{dataset}] Saved {len(new_df)} records → {path}")
    else:
        # Next runs → merge avoiding duplicates
        existing_df = pd.read_parquet(path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df = combined_df.drop_duplicates(
            subset=keys,
            keep="last"
        )
        combined_df.to_parquet(path, index=False)
        logger.info(
            f"[{dataset}] Merged {len(new_df)} new records "
            f"(total: {len(combined_df)}) → {path}"
        )