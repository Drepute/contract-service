import json
import random
from datetime import date, datetime

from flask import Response

from common.error_codes import UNKNOWN
from flask import current_app as app


def generate_nonce(length=8):
    return "".join([str(random.randint(0, 9)) for i in range(length)])


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def error_response(error=UNKNOWN, error_message=None):
    response = Response()
    to_return = {
        "success": False,
        "errors": [
            {
                "code": error.error_code,
                "text": error_message if error_message else error.message,
            },
        ],
    }
    response.data = json.dumps(to_return, default=json_serial)
    response.headers["Content-type"] = "application/json"
    response.status_code = error.status_code
    return response


def success_response(return_dict=None):
    response = Response()
    to_return = {
        "success": True,
        "data": {} if return_dict is None else return_dict,
    }
    response.data = json.dumps(to_return, default=json_serial)
    response.headers["Content-type"] = "application/json"
    response.status_code = 200
    return response


def enum_contains(enum, value):
    return value in enum.__members__


def non_void_filtered_queryset(Model, filter_kwargs) -> bool:
    object = Model.query.filter_by(**filter_kwargs).first()
    if not object:
        return False
    return object


def return_empty_params(param_dict):
    return sum(bool(key) for key in param_dict if param_dict[key] is None)


def get_rpc(chain_id):
    chain_id_rpc_map = {
        1: app.config['ETHEREUM_RPC'],
        137: app.config['POLYGON_RPC'],
        43114: app.config["AVALANCHE_RPC"],
        80001: app.config['MUMBAI_RPC'],

    }
    return chain_id_rpc_map.get(chain_id)
