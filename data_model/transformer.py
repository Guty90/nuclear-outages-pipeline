import logging
import pandas as pd

logger = logging.getLogger(__name__)

UNIT_COLS = ["capacity-units", "outage-units", "percentOutage-units"]


def create_facilities(facility_df: pd.DataFrame) -> pd.DataFrame:
    """Extract unique plants from facility outages"""
    facilities = facility_df[["facility", "facilityName"]].drop_duplicates()

    facilities = facilities.rename(columns={
        "facility":     "facility_id",
        "facilityName": "facility_name",
    })

    facilities = facilities.sort_values("facility_id").reset_index(drop=True)

    logger.info(f"Created facilities table with {len(facilities)} unique plants")
    return facilities


def clean_facility_outages(facility_df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to snake_case and drop redundant unit columns"""
    df = facility_df.rename(columns={
        "facility":      "facility_id",
        "facilityName":  "facility_name",
        "percentOutage": "percent_outage",
    })

    df = df.drop(columns=[col for col in UNIT_COLS if col in df.columns])
    df = df.sort_values(["period", "facility_id"], ascending=[False, True])
    df = df.reset_index(drop=True)

    logger.info(f"Cleaned facility outages: {len(df)} records")
    return df


def clean_generator_outages(generator_df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to snake_case and drop redundant unit columns"""
    df = generator_df.rename(columns={
        "facility":      "facility_id",
        "facilityName":  "facility_name",
        "generator":     "generator_id",
        "percentOutage": "percent_outage",
    })

    df = df.drop(columns=[col for col in UNIT_COLS if col in df.columns])
    df = df.sort_values(
        ["period", "facility_id", "generator_id"],
        ascending=[False, True, True]
    )
    df = df.reset_index(drop=True)

    logger.info(f"Cleaned generator outages: {len(df)} records")
    return df