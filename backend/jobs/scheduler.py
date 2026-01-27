from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.visibility_job import run_visibility_job
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone="UTC")

def start_scheduler():
    logger.info("Starting scheduler")

    scheduler.add_job(
        run_visibility_job,
        CronTrigger(hour=16, minute=0),  # example: daily at 4pm UTC
        id="visibility_job",
        replace_existing=True,
    )

    scheduler.start()
