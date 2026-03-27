# LOAD (cargar)

import os
import logging
import pandas as pd
from pathlib import Path
from config import DATA_DIR, DATASETS

logger = logging.getLogger(__name__)


def save_to_parquet(records: list[dict], dataset: str):
    """Save records to a parquet file"""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    path = os.path.join(DATA_DIR, DATASETS[dataset]["file"])
    pd.DataFrame(records).to_parquet(path, index=False)

    logger.info(f"[{dataset}] Saved {len(records)} records → {path}")