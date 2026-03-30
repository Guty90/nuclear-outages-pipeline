import logging
from aggregator import create_facility_summary, create_seasonality, create_us_total
from loader      import load_data
from transformer import create_facilities, clean_facility_outages, clean_generator_outages
from storage     import save_table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 50)
    logger.info("Nuclear Outages - Data Model")
    logger.info("=" * 50)

    # Load
    facility_df, generator_df = load_data()

    # Transform
    facilities_df      = create_facilities(facility_df)
    clean_facility_df  = clean_facility_outages(facility_df)
    clean_generator_df = clean_generator_outages(generator_df)

    # Aggregate                                            
    summary_df     = create_facility_summary(facility_df)
    seasonality_df = create_seasonality(facility_df)
    us_total_df    = create_us_total(facility_df)

    # Save
    save_table(facilities_df,      "facilities")
    save_table(clean_facility_df,  "facility_outages")
    save_table(clean_generator_df, "generator_outages")
    save_table(summary_df,         "facility_summary")  
    save_table(seasonality_df,     "seasonality")       
    save_table(us_total_df,        "us_total")          

    logger.info("=" * 50)
    logger.info("Data model complete ✓")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()