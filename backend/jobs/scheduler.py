from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.visibility_job import run_visibility_job
import logging
import asyncio

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone="UTC")

def run_async_job(job_coro):
    asyncio.get_event_loop().create_task(job_coro())

def start_scheduler():
    logger.info("Starting scheduler")

    scheduler.add_job(
        lambda: run_async_job(run_visibility_job),
        CronTrigger(hour=16, minute=0),  # example: daily at 4pm UTC
        id="visibility_job",
        replace_existing=True,
    )

    scheduler.start()
