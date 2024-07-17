from config.common_config import *
from secrets_manager import get_secret
from kombu import Queue

db_secret = get_secret("staging_mysql")
rpc_urls = get_secret("rpc_urls")


ENV = "staging"

MAIN_DB_SETTINGS = {
    "HOST": db_secret["host"],
    "PORT": db_secret["port"],
    "USER": db_secret["username"],
    "PASSWORD": db_secret["password"],
    "DB": "contract_service",
}

SQLALCHEMY_DATABASE_URI = "mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}".format(
    **MAIN_DB_SETTINGS,
)

mongo_secret = get_secret("staging_mongo")

MONGO_URI = mongo_secret["uri"]

JWT_TOKEN_LOCATION = ["headers"]
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"

SECRET_KEY = db_secret["password"]

REDIS_HOST = "staging-redis-cluster.x1kz4n.ng.0001.use1.cache.amazonaws.com"
REDIS_PORT = 6379



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

LOG_LEVEL = "INFO"

ELASTIC_APM = get_secret("ELASTIC_APM")
ELASTIC_APM["API_REQUEST_TIME"] = "5s"
ELASTIC_APM["ENVIRONMENT"] = ENV

ETHEREUM_RPC = rpc_urls["ALCHEMY_ETHEREUM"]
POLYGON_RPC = rpc_urls["ALCHEMY_POLYGON_MAIN"]
MUMBAI_RPC = rpc_urls["ALCHEMY_POLYGON_MUMBAI"]
AVALANCHE_RPC = rpc_urls["INFURA_AVALANCHE_C"]
BASE_RPC = rpc_urls["ALCHEMY_BASE"]