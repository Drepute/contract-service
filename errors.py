from flask import Blueprint, Response
from flask import current_app as app
import json
from common import error_codes
from sqlalchemy.exc import SQLAlchemyError
from common.utils import error_response
from db import db
from common import error_codes
import traceback

import structlog
logger = structlog.get_logger()

class RequestsError(ConnectionError):
    def __init__(self, message, exc_info=None, error_code=None, error_text=None):
        super().__init__(message)
        if error_code:
            self.error_code = error_code
        else:
            self.error_code = error_codes.REQUESTS_ERROR.error_code

        if error_text:
            self.error_text = error_text
        else:
            self.error_text = error_codes.REQUESTS_ERROR.message

        if exc_info:
            self.__exc_info__ = exc_info[0:3]

    def print_traceback(self):
        traceback.print_exception(self.__exc_info__[0], self.__exc_info__[1], self.__exc_info__[2])

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(RequestsError)
def handle_requests_error(error):
    app.apm.capture_exception()
    response = Response()
    to_return = {'success': False,
                 'errors': [
                     {'code': error.error_code, 'text': error.error_text}
                 ]
                 }
    response.data = json.dumps(to_return)
    response.headers['Content-type'] = 'application/json'
    response.status_code = 200
    return response


@errors.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    app.apm.capture_exception()
    logger.error("DB Error", exc_info=error)
    return error_response(error_codes.DB_ERROR)


@errors.app_errorhandler(Exception)
def handle_unknown_error(error):
    app.apm.capture_exception()
    logger.error("Unknown Exception", exc_info=error)
    db.session.rollback()
    return error_response(error_codes.UNKNOWN, error_message=[str(x) for x in error.args])
