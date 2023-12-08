from flask import current_app as app
from celery_worker import celery
from functools import wraps
from db import db
from datetime import datetime as dt
import structlog
from celery.utils.log import get_task_logger
logger = structlog.wrap_logger(get_task_logger('celery_service'))


@celery.task(name="token_price.tasks.run_token_price_task_subscriptions", bind=True)
def run_token_price_task_subscriptions(self):
    logger.info(f"[run_token_price_task_subscriptions] started")
    try:
        logger.info(f"[run_token_price_task_subscriptions] executing")
        from token_price.funcs import run_task_subscriptions

        run_task_subscriptions()
        logger.info(f"[run_token_price_task_subscriptions] completed")
    except Exception as e:
        app.apm.capture_exception()
        logger.error("[run_token_price_task_subscriptions][Unknown Exception]", exc_info=e)

@celery.task(name="token_price.tasks.fetch_token_price", bind=True)
def fetch_token_price(self, subscription_id):
    logger.info(f"[fetch_token_price] started")
    try:
        logger.info(f"[fetch_token_price] executing")
        from token_price.funcs import fetch_token_price

        fetch_token_price(subscription_id)
        logger.info(f"[fetch_token_price] completed")
    except Exception as e:
        app.apm.capture_exception()
        logger.error("[fetch_token_price][Unknown Exception]", exc_info=e)