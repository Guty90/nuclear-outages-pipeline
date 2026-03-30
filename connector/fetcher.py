import time
import logging
import requests
from datetime import date
from config import API_KEY, BASE_URL, PAGE_SIZE, MAX_RETRIES, DATASETS, START_YEAR, END_YEAR
from storage import read_metadata

logger = logging.getLogger(__name__)


def get_year_ranges(dataset: str) -> list[tuple]:
    """
    Generate date ranges to fetch.
    If metadata exists → only fetch from last date to today.
    If not → fetch full history from START_YEAR.
    """
    metadata = read_metadata()

    if metadata:
        last_date = metadata["last_extraction_date"]
        today     = date.today().strftime("%Y-%m-%d")
        logger.info(f"[{dataset}] Incremental mode: {last_date} → {today}")
        return [(last_date, today)]
    else:
        logger.info(f"[{dataset}] Full mode: {START_YEAR} → {END_YEAR}")
        pairs = []
        for year in range(START_YEAR, END_YEAR + 1):
            pairs.append((f"{year}-01-01", f"{year}-12-31"))
        return pairs


def fetch_year(dataset: str, start: str, end: str, retries: int = 0) -> list[dict]:
    """Fetch all records for a specific year, retry on failure"""
    url = f"{BASE_URL}{DATASETS[dataset]['endpoint']}"
    params = {
        "api_key":            API_KEY,
        "frequency":          "daily",
        "data[]":             ["capacity", "outage", "percentOutage"],
        "sort[0][column]":    "period",
        "sort[0][direction]": "desc",
        "start":              start,
        "end":                end,
        "offset":             0,
        "length":             PAGE_SIZE,
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 403:
            raise ValueError("Invalid API credentials. Check your EIA_API_KEY.")

        response.raise_for_status()

        data    = response.json().get("response", {})
        records = data.get("data", [])
        total   = int(data.get("total", 0))

        # If year has more than PAGE_SIZE records, paginate within the year
        if total > PAGE_SIZE:
            logger.info(
                f"[{dataset}] {start[:4]} has {total} records, paginating..."
            )
            all_year_records = list(records)
            offset = PAGE_SIZE

            while offset < total:
                params["offset"] = offset
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
                page = r.json().get("response", {}).get("data", [])
                if not page:
                    break
                all_year_records.extend(page)
                offset += PAGE_SIZE
                time.sleep(0.3)

            return all_year_records

        return records

    except ValueError:
        raise

    except Exception as e:
        if retries < MAX_RETRIES:
            logger.warning(
                f"[{dataset}] Retrying {start[:4]}... "
                f"({retries + 1}/{MAX_RETRIES})"
            )
            time.sleep(3)
            return fetch_year(dataset, start, end, retries + 1)

        logger.error(f"[{dataset}] Failed for {start[:4]}: {e}")
        return []


def fetch_all_pages(dataset: str) -> list[dict]:
    """Fetch all data using incremental or full mode"""
    year_ranges = get_year_ranges(dataset)
    all_records = []

    for start, end in year_ranges:
        records = fetch_year(dataset, start, end)
        all_records.extend(records)
        logger.info(
            f"[{dataset}] {start} → {end}: "
            f"+{len(records)} records (total: {len(all_records)})"
        )
        time.sleep(0.5)

    return all_records
