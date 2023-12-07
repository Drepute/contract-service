from celery.schedules import crontab

SERVICE_NAME = "contract_service"

# For SQLALCHEMY

SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERYBEAT_SCHEDULE = {
    "beat_schedule": {
        'add-every-300-seconds': {
            'task': 'event.tasks.run_task_subscriptions',
            'schedule': 300.0
        }
    }
}

SWAGGER = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/twitter_service/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/contract_service/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/contract_service/apidocs/"
}