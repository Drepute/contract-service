import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger

from common.utils import success_response
from db import db
from errors import errors


from fake_apm import FakeAPM
import redis
from logging_config import configure_logging
from pymongo import MongoClient
from event.models import *
# from event.views import event


def create_app(service_name="server"):
    print(service_name)
    app = Flask(__name__)
    app_config = os.environ.get("CONFIG", "local")
    app.config.from_object(f"config.{app_config}")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SERVICE_NAME"] = f"contract-{service_name}"

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    app.redis_connection = redis.StrictRedis(host=app.config['REDIS_URL']['HOST'],
                                             port=app.config['REDIS_URL']['PORT'],
                                             db=app.config['REDIS_URL']['DB'],
                                             password=app.config['REDIS_URL']['PASSWORD'],
                                             socket_timeout=2,
                                             socket_connect_timeout=2)

    app.mongo_client = MongoClient(app.config["MONGO_URI"])

    if app_config != "local":
        from elasticapm.contrib.flask import ElasticAPM
        apm = ElasticAPM(
            app,
            service_name='contract-service',
        )
        app.apm = apm
    else:
        app.apm = FakeAPM()    

    base_url_prefix = "/contract_service"

    with app.app_context():
        # routes go here
        # app.register_blueprint(
        #     event, url_prefix=f"{base_url_prefix}/event")
        app.register_blueprint(errors)

    @app.route(f"{base_url_prefix}/ping")
    def ping():
        import structlog
        logger = structlog.get_logger("api_service")
        logger.info("ping")
        return success_response({"success": True})

    Swagger(app, config=app.config["SWAGGER"])
    
    return app


app = create_app()
jwt = JWTManager(app)
log_file_name = "app_log.json"
configure_logging(app, log_file_name)


