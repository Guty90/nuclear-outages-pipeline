import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from config import FACILITIES_FILE, FACILITY_FILE, GENERATOR_FILE, APP_API_KEY, SUMMARY_FILE, SEASONALITY_FILE, US_TOTAL_FILE
from schemas import DataResponse, Facility, FacilityOutage, GeneratorOutage, FacilitySummary, Seasonality, UsTotal

router = APIRouter()

# ── Auth ─────────────────────────────────────────────────────────
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)) -> str:
    if key != APP_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return key


# ── Load data ─────────────────────────────────────────────────────
def load_data_by_type(data_type: str) -> pd.DataFrame:
    """Load data based on type: facility, generator, or facilities"""
    if data_type == "facility":
        file_path = FACILITY_FILE
    elif data_type == "generator":
        file_path = GENERATOR_FILE
    elif data_type == "facilities":
        file_path = FACILITIES_FILE
    elif data_type == "summary":        
        file_path = SUMMARY_FILE
    elif data_type == "seasonality":    
        file_path = SEASONALITY_FILE
    elif data_type == "us_total":       
        file_path = US_TOTAL_FILE
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid type. Must be 'facility', 'generator', or 'facilities'."
        )

    # Validar que existe
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Data file not found. Run the connector and data model first."
        )

    return pd.read_parquet(file_path)


# ── Endpoint ──────────────────────────────────────────────────────
@router.get("/data", response_model=DataResponse)
def get_data(
    type:        str   = "facility", # facility, generator, facilities
    page:        int   = 1,
    limit:       int   = 100,
    facility_id: int   = None,
    start_date:  str   = None,
    end_date:    str   = None,
    key:         str   = Security(verify_api_key),
):
    """
    Return filtered outage data from the processed parquet.
    Supports pagination, facility filter, and date range filter.
    Types: 'facility', 'generator', 'facilities'
    """
    df = load_data_by_type(type)

    # Apply filters (skip for 'facilities' table)
    if type != "facilities":
        if facility_id:
            df = df[df["facility_id"] == facility_id]

        if start_date:
            df = df[df["period"] >= start_date]

        if end_date:
            df = df[df["period"] <= end_date]

    # Pagination
    total  = len(df)
    offset = (page - 1) * limit
    df     = df.iloc[offset: offset + limit]

    # Convert to list of dicts
    records = df.to_dict(orient="records")

    # Use appropriate schema based on type
    if type == "facility":
        schema_class = FacilityOutage
    elif type == "generator":
        schema_class = GeneratorOutage
    elif type == "summary":             
        schema_class = FacilitySummary
    elif type == "seasonality":         
        schema_class = Seasonality
    elif type == "us_total":            
        schema_class = UsTotal
    else:  # facilities
        schema_class = Facility

    return DataResponse(
        total=total,
        page=page,
        limit=limit,
        data=[schema_class(**r) for r in records],
    )