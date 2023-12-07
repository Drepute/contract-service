from flask import Blueprint, request

from common.decorators import log_api
from common.error_codes import BAD_PARAMS
from common.utils import error_response, success_response

event = Blueprint("event", __name__)


@event.route("/subscribe", methods=["POST"])
def like_tweet():
    """
    file: specs/subscribe.yml
    """
    req_json = request.get_json()
    address = req_json.get("address", None)
    abi = req_json.get("abi")
    chain_id = req_json.get("chain_id")
    topic = req_json.get("topic")
    from_block = req_json.get("from_block")
    to_block = req_json.get("to_block", None)
    block_difference = req_json.get("block_difference", 100)
    cache_options = eval(req_json.get("block_difference", '{}'))
    if not address or not abi or not chain_id or not topic or not from_block:
        return error_response(BAD_PARAMS)

    from event.funcs import subscribe
    success, message = subscribe(address, abi, chain_id, topic, from_block, to_block, block_difference, cache_options)
    if not success:
        return error_response(message)
    return success_response(message)


@event.route("/aggregate", methods=["GET"])
def aggregate():
    """
    file: specs/aggregate.yml
    """
    collection_name = request.args.get("collection_name")
    key = request.args.get("key"),
    aggregator = request.args.get("aggregator"),
    filter_options = eval(request.args.get("filter_options", '{}'))
    sort_options = eval(request.args.get("sort_options", '{}'))
    if not collection_name or not key or not aggregator:
        return error_response(BAD_PARAMS)

    from event.funcs import aggregate
    success, message = aggregate(collection_name, key, aggregator, filter_options, sort_options)
    if not success:
        return error_response(message)
    return success_response(message)
