from event.models import Subscription
from web3 import Web3
import json
from common.utils import get_rpc
from flask import current_app as app
from bson.binary import Binary
from db import db
from common.error_codes import *
from common.error_codes import *
from event.transformer import Transformer


def subscribe(address, abi, chain_id, topic, from_block, to_block, block_difference, cache_options):
    subscription = Subscription.query.filter(
        Subscription.address == address,
        Subscription.chain_id == chain_id, 
        Subscription.topic == topic, 
    ).first()
    if subscription:
        return False, RESOURCE_EXISTS

    subscription = Subscription(
        address = address,
        abi = abi,
        chain_id = chain_id,
        topic = db.Column(db.Text()),
        from_block = from_block,
        to_block = to_block,
        last_synced_block = 0,
        block_difference = block_difference,
        cache_options = cache_options
    )
    db.session.add(subscription)
    db.session.commmit()
    return True, {'subscription_id': subscription.id}


def run_task_subscriptions():
    from event.tasks import fetch_event_logs
    current_block_numbers_map = {}

    subscriptions = Subscription.query.filter_by(is_active=True).all()
    for subscription in subscriptions:
        if not subscription.chain_id in current_block_numbers_map.keys():
            rpc = get_rpc(subscription.chain_id)
            if not rpc:
                return False, NOT_FOUND
            provider = Web3(Web3.HTTPProvider(rpc))
            current_block_numbers_map[subscription.chain_id] = provider.eth.block_number

        current_block_number = current_block_numbers_map[subscription.chain_id]
        if subscription.last_synced_block < current_block_number:
            fetch_event_logs.apply_async(args=[subscription.id])


def fetch_event_logs(subscription_id):
    from event.tasks import fetch_event_logs
    subscription = Subscription.query.filter_by(id=subscription_id).first()

    rpc = get_rpc(subscription.chain_id)
    web3 = Web3(Web3.HTTPProvider(rpc))
    if subscription.chain_id in [137, 80001, 43114]:
        from web3.middleware import geth_poa_middleware
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    current_block_number = web3.eth.block_number
    
    contract = web3.eth.contract(address=subscription.address, abi=subscription.abi['data'])
    toBlock = min(subscription.last_synced_block+10000, current_block_number)
    logs = eval(f'contract.events.{subscription.topic}.get_logs(fromBlock=subscription.last_synced_block+1, toBlock=toBlock)')    
    last_synced_block = logs[-1].blockNumber if len(logs) > 0 else toBlock
    if subscription.cache_options and subscription.cache_options.get("blockNumberTime"):
        block_number_ts_map = get_block_logs(subscription.chain_id, format="block_number_ts_map")
        block_number_timestamp_logs = []
        for log in logs:
            block_number = log['blockNumber']
            if not block_number_ts_map.get(block_number):
                block = web3.eth.get_block(block_number)
                block_timstamp = block['timestamp']
                print({'blockNumber': block_number, 'timestamp': block_timstamp})
                block_number_timestamp_logs.append({'blockNumber': block_number, 'timestamp': block_timstamp})

        if len(block_number_timestamp_logs) > 0:
            insert_block_logs(subscription.chain_id, block_number_timestamp_logs)
    if len(logs) > 0:
        insert_event_logs(subscription, logs)
    subscription.last_synced_block = last_synced_block
    db.session.commit()

    if last_synced_block < current_block_number:
        fetch_event_logs.apply_async(args=[subscription.id], countdown=5)
    return logs

def insert_event_logs(subscription, logs):
    topic_input_types = get_topic_input_types(subscription)
    formatted_logs = []
    for log in logs:
        f_log = dict(log)
        f_log["args"] = dict(f_log["args"])
        for arg in f_log['args'].keys():
            if topic_input_types[arg] == 'uint256':
                f_log['args'][arg] = Binary(f_log['args'][arg].to_bytes(32, byteorder='big'), 0)
        formatted_logs.append(f_log)
    db = app.mongo_client.event_log
    collection = db[f"{subscription.uuid}"]
    collection.insert_many(formatted_logs)





def get_topic_input_types(subscription):
    topic_inputs = [event['inputs'] for event in json.loads(subscription.abi['data']) if event.get('name') == subscription.topic][0]
    topic_input_types = {input['name']: input['type'] for input in topic_inputs}
    return topic_input_types





######## AGGREGATION LOGIC ###########

def _sum(records, key):
    res = 0
    for record in records:
        res = res + record['args'][key]
    return res

def _count(records, key):
    res = 0
    for _ in records:
        res = res + 1
    return res

def _average(records, key):
    return sum(records, key) / _count(records, key)

def _max(records, key):
    res = records[0]['args'][key]
    for record in records:
        res = max(res, record['args'][key])
    return res

def _min(records, key):
    res = records[0]['args'][key]
    for record in records:
        res = min(res, record['args'][key])
    return res

agg_func = {
    'sum': _sum,
    'count': _count,
    'average': _average
}

# operations transform [key , adapter], aggregate [key, adapter], filter [key, operation]

def aggregate(collection_name, key, aggregator, filter_options, sort_options, transform_options):
    subscription_values = collection_name.split('-')
    subscription = Subscription.query.filter(
        Subscription.address == subscription_values[0],
        Subscription.chain_id == int(subscription_values[1]), 
        Subscription.topic == subscription_values[2], 
    ).first()
    if not subscription:
        return False, NOT_FOUND
    topic_input_types = get_topic_input_types(subscription)

    db = app.mongo_client.event_log
    collection = db[subscription.uuid]
    cursor = collection.find(filter_options).sort(sort_options)
    if aggregator == "count":
        return True, {"result": collection.count_documents(filter_options)}
    records = [record for record in cursor]

    if topic_input_types[key] == "uint256":
        transform_options["adapters"] = [{"name": "bin_data_int"}] + transform_options.get("adapters", [])
        transform_options["params_list"] = [{}] + transform_options.get("params_list", [])
    for i, param in enumerate(transform_options.get("params_list", [])):
        transform_options["params_list"][i] = {"key": key, **param}
    transformer = Transformer(subscription, transform_options)
    transformed_records = transformer.transform(records)


    return True, {'result': agg_func[aggregator](transformed_records, key)}
    



############# Block Logs ######################

def insert_block_logs(chain_id, logs):
    db = app.mongo_client.block_log
    collection = db[f"{chain_id}"]
    collection.insert_many(logs)

def get_block_logs(chain_id, format="default"):
    db = app.mongo_client.block_log
    collection = db[f"{chain_id}"]
    logs = collection.find()
    if format == "block_number_ts_map":
        block_number_ts = {}
        for log in logs:
            block_number_ts[log['blockNumber']] =  log['timestamp']
        return block_number_ts
    return logs