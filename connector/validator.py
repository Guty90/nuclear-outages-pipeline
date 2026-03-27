# TRANSFORM (transformar)

import logging
from config import DATASETS

logger = logging.getLogger(__name__)


def convert_types(record: dict) -> dict:
    """Convert string values from API to correct Python types"""
    
    # facility ID → integer
    if "facility" in record and record["facility"] is not None:
        record["facility"] = int(record["facility"])
    
    # generator ID → integer (only in generator dataset)
    if "generator" in record and record["generator"] is not None:
        record["generator"] = int(record["generator"])

    # capacity → float (megawatts)
    if "capacity" in record and record["capacity"] is not None:
        record["capacity"] = float(record["capacity"])

    # outage → float (megawatts lost)
    if "outage" in record and record["outage"] is not None:
        record["outage"] = float(record["outage"])

    # percentOutage → float (percentage)
    if "percentOutage" in record and record["percentOutage"] is not None:
        record["percentOutage"] = float(record["percentOutage"])

    return record


def validate_records(records: list[dict], dataset: str) -> list[dict]:
    """Check required fields exist, convert types, skip invalid records"""
    required = DATASETS[dataset]["required"]
    valid = []

    for record in records:

        # Check for missing or null required fields
        missing = []
        for field in required:
            if field not in record or record[field] is None:
                missing.append(field)

        # If any field is missing, skip this record
        if missing:
            logger.warning(
                f"[{dataset}] Skipping record, missing fields: {missing}"
            )
            continue

        # Convert string values to correct types
        record = convert_types(record)

        # Add to valid list
        valid.append(record)

    return valid