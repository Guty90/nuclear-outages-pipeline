import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_model.aggregator import create_facility_summary, create_seasonality, create_us_total


# ── Facility Summary ──────────────────────────────────────────────

def test_facility_summary_columns(sample_facility_df):
    """Summary must have all required columns"""
    result = create_facility_summary(sample_facility_df)
    expected_cols = [
        "facility_id", "avg_percent_outage", "max_percent_outage",
        "total_mw_lost", "days_with_outage", "avg_capacity_factor",
        "total_records", "last_reported", "is_active",
    ]
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"


def test_facility_summary_capacity_factor(sample_facility_df):
    """Capacity factor must be calculated correctly"""
    result = create_facility_summary(sample_facility_df)
    plant_a = result[result["facility_id"] == 1].iloc[0]

    # Plant A: capacity=1000, outages=[200,100,0] → avg outage=100 → avg capacity factor=90%
    assert plant_a["avg_capacity_factor"] == pytest.approx(90.0, abs=0.1)


def test_facility_summary_active_status(sample_facility_df):
    """Plants with no recent reports must be marked as inactive"""
    result = create_facility_summary(sample_facility_df)

    plant_a = result[result["facility_id"] == 1].iloc[0]
    plant_c = result[result["facility_id"] == 3].iloc[0]

    assert plant_a["is_active"] == True
    assert plant_c["is_active"] == False


def test_facility_summary_sorted_by_outage(sample_facility_df):
    """Summary must be sorted by avg_percent_outage descending"""
    result = create_facility_summary(sample_facility_df)
    outages = result["avg_percent_outage"].tolist()
    assert outages == sorted(outages, reverse=True)


def test_facility_summary_total_mw_lost(sample_facility_df):
    """Total MW lost must be sum of all outages per facility"""
    result = create_facility_summary(sample_facility_df)
    plant_a = result[result["facility_id"] == 1].iloc[0]

    # Plant A: 200 + 100 + 0 = 300
    assert plant_a["total_mw_lost"] == pytest.approx(300.0, abs=0.1)


def test_facility_summary_days_with_outage(sample_facility_df):
    """Days with outage must count only days where outage > 0"""
    result = create_facility_summary(sample_facility_df)
    plant_a = result[result["facility_id"] == 1].iloc[0]

    # Plant A: días con outage > 0 son 2 (200 y 100), el día con 0 no cuenta
    assert plant_a["days_with_outage"] == 2


# ── Seasonality ───────────────────────────────────────────────────

def test_seasonality_has_all_months(sample_facility_df):
    """Seasonality must return one row per month present in the data"""
    result = create_seasonality(sample_facility_df)
    assert "month" in result.columns
    assert len(result) >= 1


def test_seasonality_columns(sample_facility_df):
    """Seasonality must have all required columns"""
    result = create_seasonality(sample_facility_df)
    expected_cols = ["month", "avg_percent_outage", "avg_mw_offline", "total_mw_lost", "record_count"]
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"


def test_seasonality_avg_is_correct(sample_facility_df):
    """Average percent outage per month must be calculated correctly"""
    result = create_seasonality(sample_facility_df)

    # Marzo tiene 5 registros con percentOutage=[20,10,0,0,0] → avg=6.0
    march = result[result["month"] == 3].iloc[0]
    assert march["avg_percent_outage"] == pytest.approx(6.0, abs=0.1)


# ── US Total ──────────────────────────────────────────────────────

def test_us_total_columns(sample_facility_df):
    """US total must have all required columns"""
    result = create_us_total(sample_facility_df)
    expected_cols = ["period", "total_capacity", "total_mw_offline", "active_facilities", "percent_offline"]
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"


def test_us_total_sums_correctly(sample_facility_df):
    """US total must sum capacity and outage across all facilities per day"""
    result = create_us_total(sample_facility_df)

    # 2026-03-27: facility 1 (cap=1000, out=200) + facility 2 (cap=2000, out=0)
    day = result[result["period"] == "2026-03-27"].iloc[0]
    assert day["total_capacity"]   == pytest.approx(3000.0, abs=0.1)
    assert day["total_mw_offline"] == pytest.approx(200.0,  abs=0.1)


def test_us_total_percent_offline(sample_facility_df):
    """Percent offline must be calculated correctly"""
    result = create_us_total(sample_facility_df)

    # 2026-03-27: 200 offline / 3000 total = 6.67%
    day = result[result["period"] == "2026-03-27"].iloc[0]
    assert day["percent_offline"] == pytest.approx(6.67, abs=0.1)


def test_us_total_sorted_by_date_desc(sample_facility_df):
    """US total must be sorted by period descending (most recent first)"""
    result = create_us_total(sample_facility_df)
    periods = result["period"].tolist()
    assert periods == sorted(periods, reverse=True)