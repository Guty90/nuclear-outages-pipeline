import pytest
import pandas as pd


@pytest.fixture
def sample_facility_df():
    """Fake facility outages data for testing"""
    return pd.DataFrame([
        # Facility 1 — activa, con outages
        {"facility": 1, "facilityName": "Plant A", "period": "2026-03-27", "capacity": 1000.0, "outage": 200.0, "percentOutage": 20.0},
        {"facility": 1, "facilityName": "Plant A", "period": "2026-03-26", "capacity": 1000.0, "outage": 100.0, "percentOutage": 10.0},
        {"facility": 1, "facilityName": "Plant A", "period": "2026-03-25", "capacity": 1000.0, "outage":   0.0, "percentOutage":  0.0},

        # Facility 2 — activa, sin outages
        {"facility": 2, "facilityName": "Plant B", "period": "2026-03-27", "capacity": 2000.0, "outage":   0.0, "percentOutage":  0.0},
        {"facility": 2, "facilityName": "Plant B", "period": "2026-03-26", "capacity": 2000.0, "outage":   0.0, "percentOutage":  0.0},

        # Facility 3 — inactiva (último reporte hace más de 90 días)
        {"facility": 3, "facilityName": "Plant C", "period": "2020-01-01", "capacity": 500.0,  "outage": 500.0, "percentOutage": 100.0},
    ])