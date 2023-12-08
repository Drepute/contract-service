from celery import Celery, Task
from celery import states as celery_states
from celery.signals import (
    task_failure,
    task_prerun,
    task_postrun,
    worker_process_init,
    worker_process_shutdown,
    setup_logging,
    after_setup_logger
)
from logging_config import configure_logging

from app import create_app
from db import db
import structlog

class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

app = create_app(service_name="celery")
celery = Celery(app.name, task_cls=FlaskTask)
celery.config_from_object(app.config["CELERY"])
celery.set_default()
app.extensions["celery"] = celery
celery.autodiscover_tasks(
    ["event", "token_price"],
    force=True,
)


@setup_logging.connect
def on_setup_logging(**kwargs):
    print("logging setup in celery")
    log_file_name = "app_log.json"
    configure_logging(app, log_file_name)

@task_prerun.connect
def on_task_prerun(sender, task_id, task, args, kwargs, **_):
    structlog.contextvars.bind_contextvars(task_id=task_id, task_name=task.name)


@worker_process_init.connect
def init_worker(**kwargs):
    print("Initializing database connection for worker.")
    with app.app_context():
        db.init_app(app)
        db.reflect()


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    print("Removing database connection for worker.")
    with app.app_context():
        db.session.remove()


@task_failure.connect
def handle_task_failure(exception=None, traceback=None, **kwargs):
    from celery.utils.log import get_task_logger
    logger = structlog.wrap_logger(get_task_logger('celery_service'))
    with app.app_context():
        logger.error(exception)
        logger.error(traceback)
        app.apm.capture_exception()
        db.session.rollback()
        db.session.expire_all()


@task_postrun.connect
def cleanup_db(retval=None, state=None, task_id=None, **kwargs):
    from celery.utils.log import get_task_logger
    logger = structlog.wrap_logger(get_task_logger('celery_service'))
    with app.app_context():
        logger.info({"retval": retval, "state": state, "task_id": task_id})
        try:
            if state == celery_states.SUCCESS:
                db.session.rollback()
            else:
                db.session.rollback()

            db.session.expire_all()
            logger.info(db.session.connection().connection.thread_id())
        except Exception as e:
            logger.error(e)
            app.apm.capture_exception() 
