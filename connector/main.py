import logging
from config import DATASETS, validate_api_key
from fetcher import fetch_all_pages
from validator import validate_records
from storage import save_to_parquet, save_metadata, read_metadata

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def extract_dataset(dataset: str) -> int:
    """Fetch → Validate → Save for one dataset"""
    logger.info(f"[{dataset}] Starting extraction...")

    records = fetch_all_pages(dataset)
    valid   = validate_records(records, dataset)
    save_to_parquet(valid, dataset)
    
    logger.info(f"[{dataset}] Done ✓")
    return len(valid)


def main():
    logger.info("=" * 50)
    logger.info("Nuclear Outages - Data Extraction")
    logger.info("=" * 50)

    try:
        validate_api_key()
    except ValueError as e:
        logger.error(str(e))
        return

    counts = {}
    for dataset in DATASETS:
        try:
            counts[dataset] = extract_dataset(dataset)
        except ValueError as e:
            logger.error(str(e))
            return
        except Exception as e:
            logger.error(f"[{dataset}] Unexpected error: {e}")
            counts[dataset] = 0

    # Update metadata
    metadata      = read_metadata()
    refresh_count = (metadata or {}).get("refresh_count", 0) + 1

    save_metadata(
        facility_count=counts.get("facility", 0),
        generator_count=counts.get("generator", 0),
        refresh_count=refresh_count,
    )

    logger.info("=" * 50)
    logger.info("Extraction complete ✓")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()