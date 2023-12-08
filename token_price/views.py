from flask import Blueprint, request

from common.decorators import log_api
from common.error_codes import BAD_PARAMS
from common.utils import error_response, success_response

token_price = Blueprint("token_price", __name__)


@token_price.route("/subscribe", methods=["POST"])
def tp_subscribe():
    """
    file: specs/subscribe.yml
    """
    req_json = request.get_json()
    symbol = req_json.get("symbol", None)
    decimals = req_json.get("decimals", 18)
    market = req_json.get("market")
    time_interval = req_json.get("time_interval")
    start_timestamp = req_json.get("start_timestamp")
    exchange = req_json.get("exchange", None)
    if not symbol or not market or not time_interval or not start_timestamp or not exchange:
        return error_response(BAD_PARAMS)

    from token_price.funcs import subscribe
    success, message = subscribe(symbol, decimals, market, time_interval, start_timestamp, exchange)
    if not success:
        return error_response(message)
    return success_response(message)
