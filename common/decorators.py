import json
import os
import time
from functools import wraps

from flask import current_app as app
from flask import request
import structlog
logger = structlog.get_logger()


def log_api(func):
    @wraps(func)
    def log_wrapper(*args, **kwargs):
        endpoint = request.base_url
        method = request.method
        req_json, req_args = {}, {}
        try:
            req_args = json.dumps(request.args.to_dict())
            req_json = json.dumps(request.get_json())
        except Exception:
            pass

        logger.info(
            f"[REQUEST] [{func.__name__}] [{method}] {endpoint} [ARGS: {req_args}] [BODY: {req_json}]",
        )

        return func(*args, **kwargs)

    return log_wrapper


def retry_max(max_retries):
    def retry(func):
        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            # Assume retry_num to be the last argument in every function signature
            retry_num = args[-1]
            if int(retry_num) >= max_retries:
                raise Exception("MAX RETRIES REACHED ",
                                func.__name__, args, kwargs)
            return func(*args, **kwargs)
        return retry_wrapper
    return retry
