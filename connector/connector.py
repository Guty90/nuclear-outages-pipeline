import logging
from config import DATASETS, validate_api_key
from fetcher import fetch_all_pages
from validator import validate_records
from storage import save_to_parquet

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def extract_dataset(dataset: str):
    """Fetch → Validate → Save for one dataset"""
    logger.info(f"[{dataset}] Starting extraction...")

    records = fetch_all_pages(dataset)
    valid   = validate_records(records, dataset)
    save_to_parquet(valid, dataset)

    logger.info(f"[{dataset}] Done ✓")


def main():
    logger.info("=" * 50)
    logger.info("Nuclear Outages - Data Extraction")
    logger.info("=" * 50)

    try:
        validate_api_key()
    except ValueError as e:
        logger.error(str(e))
        return

    for dataset in DATASETS:
        try:
            extract_dataset(dataset)
        except ValueError as e:
            logger.error(str(e))
            return
        except Exception as e:
            logger.error(f"[{dataset}] Unexpected error: {e}")

    logger.info("=" * 50)
    logger.info("Extraction complete ✓")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()