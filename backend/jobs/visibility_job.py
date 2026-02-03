from services.site_service import SiteService
from enums.time_visibility import TimeVisibility
import logging

logger = logging.getLogger(__name__)

async def run_visibility_job(site_service: SiteService):
    logger.info("Starting visibility precompute job")

    try:
        time_buckets = [
            TimeVisibility.TONIGHT,
            TimeVisibility.TOMORROW_NIGHT,
            TimeVisibility.NIGHTS_3_FROM_NOW,
        ]

        await site_service.precompute_visibility(time_buckets)

        logger.info("Finished visibility precompute job")
    except Exception as e:
        logger.error(f"Error in visibility precompute job: {e}")
        raise