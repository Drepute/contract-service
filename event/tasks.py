from flask import current_app as app
from celery_worker import celery
from functools import wraps
from db import db
from datetime import datetime as dt
import structlog
from celery.utils.log import get_task_logger
logger = structlog.wrap_logger(get_task_logger('celery_service'))


@celery.task(name="event.tasks.run_task_subscriptions", bind=True)
def run_task_subscriptions(self):
    logger.info(f"[run_task_subscriptions] started")
    try:
        logger.info(f"[run_task_subscriptions] executing")
        from event.funcs import run_task_subscriptions

        run_task_subscriptions()
        logger.info(f"[run_task_subscriptions] completed")
    except Exception as e:
        app.apm.capture_exception()
        logger.error("[run_task_subscriptions][Unknown Exception]", exc_info=e)

@celery.task(name="event.tasks.fetch_event_logs", bind=True)
def fetch_event_logs(self, subscription_id):
    logger.info(f"[fetch_event_logs] started")
    try:
        logger.info(f"[fetch_event_logs] executing")
        from event.funcs import fetch_event_logs

        fetch_event_logs(subscription_id)
        logger.info(f"[fetch_event_logs] completed")
    except Exception as e:
        app.apm.capture_exception()
        logger.error("[fetch_event_logs][Unknown Exception]", exc_info=e)