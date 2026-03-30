import sys
import os
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
API_DIR = os.path.join(ROOT_DIR, "api")

# Ensure HTTP header value is ASCII-safe for TestClient/httpx.
os.environ["APP_API_KEY"] = "test-key"

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, API_DIR)

from api.main import app

API_KEY = os.getenv("APP_API_KEY", "test-key")
HEADERS = {"X-API-Key": API_KEY}
client  = TestClient(app)


# ── Auth ──────────────────────────────────────────────────────────

def test_no_api_key_returns_401():
    """Request without API key must return 401"""
    response = client.get("/data")
    assert response.status_code == 401


def test_wrong_api_key_returns_401():
    """Request with wrong API key must return 401"""
    response = client.get("/data", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_invalid_type_returns_400():
    """Request with invalid type must return 400"""
    response = client.get("/data?type=invalid", headers=HEADERS)
    assert response.status_code == 400


# ── /data endpoint ────────────────────────────────────────────────

def test_facility_data_returns_200():
    """Facility outages endpoint must return 200 with correct structure"""
    response = client.get("/data?type=facility&limit=5", headers=HEADERS)
    assert response.status_code == 200

    body = response.json()
    assert "total" in body
    assert "page"  in body
    assert "limit" in body
    assert "data"  in body
    assert isinstance(body["data"], list)


def test_pagination_works():
    """Pagination must return correct page and limit"""
    response = client.get("/data?type=facility&page=1&limit=10", headers=HEADERS)
    assert response.status_code == 200

    body = response.json()
    assert body["page"]  == 1
    assert body["limit"] == 10
    assert len(body["data"]) <= 10


def test_summary_returns_correct_fields():
    """Summary endpoint must return facility performance fields"""
    response = client.get("/data?type=summary", headers=HEADERS)
    assert response.status_code == 200

    first = response.json()["data"][0]
    assert "facility_id"         in first
    assert "avg_capacity_factor" in first
    assert "is_active"           in first
    assert "total_mw_lost"       in first


def test_seasonality_returns_12_months():
    """Seasonality must return exactly 12 months"""
    response = client.get("/data?type=seasonality", headers=HEADERS)
    assert response.status_code == 200

    body = response.json()
    assert body["total"] == 12


def test_us_total_returns_correct_fields():
    """US total must return system-wide fields"""
    response = client.get("/data?type=us_total", headers=HEADERS)
    assert response.status_code == 200

    first = response.json()["data"][0]
    assert "period"           in first
    assert "total_capacity"   in first
    assert "total_mw_offline" in first
    assert "percent_offline"  in first


def test_facility_filter_works():
    """Filtering by facility_id must return only that facility's records"""
    response = client.get("/data?type=facility&facility_id=1", headers=HEADERS)
    assert response.status_code == 200

    data = response.json()["data"]
    for row in data:
        assert row["facility_id"] == 1