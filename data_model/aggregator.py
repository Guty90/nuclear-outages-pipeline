import logging
import pandas as pd

logger = logging.getLogger(__name__)


def create_facility_summary(facility_df: pd.DataFrame) -> pd.DataFrame:
    """
    KPI: Facility performance ranking.
    Answers: Which plants are most problematic and how much energy have they lost?
    Includes capacity factor, total MW lost, and active/inactive status.
    """
    df = facility_df.rename(columns={
        "facility":      "facility_id",
        "percentOutage": "percent_outage",
    })

    # Capacity factor: what % of max capacity is actually being generated
    df["capacity_factor"] = (
        (df["capacity"] - df["outage"]) / df["capacity"] * 100
    ).round(2)

    # Detect active vs inactive/closed plants (no report in last 90 days)
    last_report = df.groupby("facility_id")["period"].max().reset_index()
    last_report.columns = ["facility_id", "last_reported"]
    cutoff = (pd.Timestamp.today() - pd.Timedelta(days=90)).strftime("%Y-%m-%d")
    last_report["is_active"] = last_report["last_reported"] >= cutoff

    summary = df.groupby("facility_id").agg(
        avg_percent_outage  = ("percent_outage",  "mean"),
        max_percent_outage  = ("percent_outage",  "max"),
        total_mw_lost       = ("outage",          "sum"),
        days_with_outage    = ("outage",          lambda x: (x > 0).sum()),
        avg_capacity_factor = ("capacity_factor", "mean"),
        total_records       = ("outage",          "count"),
    ).reset_index()

    summary = summary.merge(last_report, on="facility_id")
    summary["avg_percent_outage"]  = summary["avg_percent_outage"].round(2)
    summary["max_percent_outage"]  = summary["max_percent_outage"].round(2)
    summary["total_mw_lost"]       = summary["total_mw_lost"].round(1)
    summary["avg_capacity_factor"] = summary["avg_capacity_factor"].round(2)
    summary = summary.sort_values("avg_percent_outage", ascending=False).reset_index(drop=True)

    logger.info(f"Created facility summary with {len(summary)} facilities")
    return summary


def create_seasonality(facility_df: pd.DataFrame) -> pd.DataFrame:
    """
    KPI: Monthly outage pattern across all years and plants.
    Answers: Which months concentrate the most outages? Is there a maintenance pattern?
    """
    df = facility_df.rename(columns={
        "facility":      "facility_id",
        "percentOutage": "percent_outage",
    })

    df["month"] = pd.to_datetime(df["period"]).dt.month

    seasonality = df.groupby("month").agg(
        avg_percent_outage = ("percent_outage", "mean"),
        avg_mw_offline     = ("outage",         "mean"),
        total_mw_lost      = ("outage",         "sum"),
        record_count       = ("outage",         "count"),
    ).reset_index()

    seasonality["avg_percent_outage"] = seasonality["avg_percent_outage"].round(2)
    seasonality["avg_mw_offline"]     = seasonality["avg_mw_offline"].round(1)
    seasonality["total_mw_lost"]      = seasonality["total_mw_lost"].round(1)

    logger.info(f"Created seasonality table with {len(seasonality)} months")
    return seasonality


def create_us_total(facility_df: pd.DataFrame) -> pd.DataFrame:
    """
    KPI: Total US nuclear capacity offline per day.
    Answers: How much nuclear capacity is offline today? How has it trended over time?
    Note: The EIA publishes this via their us-nuclear-outages endpoint,
    but calculated here from facility-level data to demonstrate pipeline capability
    in scenarios where this aggregate is not available from the source.
    """
    df = facility_df.rename(columns={
        "facility":      "facility_id",
        "percentOutage": "percent_outage",
    })

    us_total = df.groupby("period").agg(
        total_capacity    = ("capacity",    "sum"),
        total_mw_offline  = ("outage",      "sum"),
        active_facilities = ("facility_id", "nunique"),
    ).reset_index()

    us_total["percent_offline"] = (
        us_total["total_mw_offline"] / us_total["total_capacity"] * 100
    ).round(2)

    us_total["total_capacity"]   = us_total["total_capacity"].round(1)
    us_total["total_mw_offline"] = us_total["total_mw_offline"].round(1)
    us_total = us_total.sort_values("period", ascending=False).reset_index(drop=True)

    logger.info(f"Created US total with {len(us_total)} daily records")
    return us_total