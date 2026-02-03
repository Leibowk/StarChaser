from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.visibility_job import run_visibility_job
import logging
import asyncio

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone="UTC")

def run_async_job(job_coro):
    asyncio.get_event_loop().create_task(job_coro())

def start_scheduler(app):
    logger.info("Starting scheduler")
    site_service = app.state.site_service

    scheduler.add_job(
        lambda: run_async_job(lambda: run_visibility_job(site_service)),
        CronTrigger(hour=16, minute=0),  # example: daily at 4pm UTC
        id="visibility_job",
        replace_existing=True,
    )

    scheduler.start()
