import subprocess
import sys
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from config import APP_API_KEY, CONNECTOR_SCRIPT, DATA_MODEL_SCRIPT
from schemas import RefreshResponse

router = APIRouter()

# ── Auth ─────────────────────────────────────────────────────────
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)) -> str:
    if key != APP_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return key


# ── Endpoint ──────────────────────────────────────────────────────
@router.get("/refresh", response_model=RefreshResponse)
def refresh_data(key: str = Security(verify_api_key)):
    """
    Trigger a full data refresh:
    runs the connector then the data model pipeline.
    """
    try:
        # Run connector
        subprocess.run(
            [sys.executable, CONNECTOR_SCRIPT],
            check=True,
            capture_output=True,
        )

        # Run data model
        subprocess.run(
            [sys.executable, DATA_MODEL_SCRIPT],
            check=True,
            capture_output=True,
        )

        return RefreshResponse(
            status="success",
            message="Data refreshed successfully",
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Refresh failed: {e.stderr.decode()}"
        )