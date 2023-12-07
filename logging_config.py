import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import structlog
from elasticapm.handlers.structlog import structlog_processor
from flask.logging import default_handler



def configure_logging(app, log_file_name):
    # Create a console handler for logging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    

    APM_LOG_LEVEL = logging.INFO if app.config.get('ENV', "local") != "local" else logging.CRITICAL

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    logs_dir = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create a file handler for logging
    file_handler = RotatingFileHandler(
        filename=f"{logs_dir}/{log_file_name}",
        maxBytes=10 * 1024 * 1024,  # 10MiB
        backupCount=5,
    )
    file_handler.setLevel(APM_LOG_LEVEL)

    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog_processor,
        structlog.processors.EventRenamer("message"),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Set up the logging configuration
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[console_handler],
    )

    # Silence noisy loggers
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    if (app.config["SERVICE_NAME"] == 'contract-celery'):
        from celery.utils.log import get_task_logger
        logger = get_task_logger("celery_service")
        logger.addHandler(file_handler)

    else:
        logger = structlog.get_logger("api_service")
        logger.addHandler(file_handler)

    app.logger.removeHandler(default_handler)

    # Set the Flask app logger to the structlog logger
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.debug = app.logger.info

    return logger
