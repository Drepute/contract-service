from config.common_config import *
from kombu import Queue

ENV = "LOCAL"

MAIN_DB_SETTINGS = {
    "HOST": "mysql",
    "PORT": 3306,
    "USER": "root",
    "PASSWORD": "root",
    "DB": "contract_service",
}

SQLALCHEMY_DATABASE_URI = "mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}".format(
    **MAIN_DB_SETTINGS,
)

MONGO_URI = "mongodb://mongo:27017/"

JWT_TOKEN_LOCATION = ["headers"]
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"

SECRET_KEY = "SECREYONLYIKNOW"


REDIS_HOST = "redis_db"
REDIS_PORT = 6379

CELERYBEAT_SCHEDULE = {
    "beat_schedule": {
        'event-subscriptions-every-10-seconds': {
            'task': 'event.tasks.run_task_subscriptions',
            'schedule': 10.0
        },
        'token-subscriptions-every-10-seconds': {
            'task': 'token_price.tasks.run_token_price_task_subscriptions',
            'schedule': 10.0
        }
    }
}

CELERY = {
        **CELERYBEAT_SCHEDULE,
        "broker_url": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        "result_backend": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        "task_default_queue": "contract_service_tasks_queue",
        "task_queues": (Queue("contract_service_tasks_queue", exchange_type="direct", routing_key="contract_service_tasks_queue"),),
        "task_default_exchange": "contract_service_tasks_queue",
        "task_default_exchange_type": "direct",
        "task_default_routing_key": "contract_service_tasks_queue",
        "task_routes": (
            [
                ("event.tasks.*", {"queue": "contract_service_tasks_queue"}),
                ("token_price.tasks.*", {"queue": "contract_service_tasks_queue"})
            ],
        ),
    }

USE_CACHE = True
REDIS_URL = {'HOST': REDIS_HOST, 'PORT': REDIS_PORT, 'DB': 0, 'PASSWORD': ""}

LOG_LEVEL = "DEBUG"

# ELASTIC_APM = get_secret("ELASTIC_APM")
# ELASTIC_APM["API_REQUEST_TIME"] = "5s"
# https://www.elastic.co/guide/en/apm/agent/python/6.x/troubleshooting.html#debug-mode
# ELASTIC_APM["DEBUG"] = False