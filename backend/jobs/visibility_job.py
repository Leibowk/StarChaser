from services.site_service import SiteService
from enums.time_visibility import TimeVisibility
import logging

logger = logging.getLogger(__name__)

def run_visibility_job():
    logger.info("Starting visibility precompute job")

    try:
        site_service = SiteService()

        time_buckets = [
            TimeVisibility.TONIGHT,
            TimeVisibility.TOMORROW_NIGHT,
            TimeVisibility.NIGHTS_3_FROM_NOW,
        ]

        site_service.precompute_visibility(time_buckets)

        logger.info("Finished visibility precompute job")
    except Exception as e:
        logger.error(f"Error in visibility precompute job: {e}")
        raise