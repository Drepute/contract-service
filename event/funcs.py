from event.models import Subscription
from web3 import Web3
import json
from common.utils import get_rpc
from flask import current_app as app
from bson.binary import Binary
from db import db
from common.error_codes import *
from common.error_codes import *


def subscribe(address, abi, chain_id, topic, from_block, to_block, block_difference):
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
        block_difference = block_difference
    )
    db.session.add(subscription)
    db.session.commmit()
    return True, {'subscription_id': subscription.id}


def run_task_subscriptions(chain_id):
    from event.tasks import fetch_event_logs
    current_block_numbers_map = {}

    rpc = get_rpc(chain_id)
    if rpc is None:
        return False, NOT_FOUND
    web3 = Web3(Web3.HTTPProvider(rpc))
    if not chain_id in current_block_numbers_map.keys():
        current_block_numbers_map[chain_id] = web3.eth.block_number
    current_block_number = current_block_numbers_map[chain_id]
    subscriptions = Subscription.query.filter_by(chain_id=chain_id).all()
    for subscription in subscriptions:
        if subscription.last_synced_block < current_block_number:
            continue
        fetch_event_logs.apply_async(args=[subscription.id, current_block_number])


def fetch_event_logs(subscription_id):
    from event.tasks import fetch_event_logs
    subscription = Subscription.query.filter_by(id=subscription_id).first()

    rpc = get_rpc(subscription.chain_id)
    web3 = Web3(Web3.HTTPProvider(rpc))
    current_block_number = web3.eth.block_number
    print(current_block_number)
    
    contract = web3.eth.contract(address=subscription.address, abi=subscription.abi['data'])
    logs = eval(f'contract.events.{subscription.topic}.get_logs(fromBlock=subscription.last_synced_block+1)')
    last_synced_block = logs[-1].blockNumber if len(logs) > 0 else current_block_number
    if len(logs) > 0:
        insert_logs(subscription, logs)

    subscription.last_synced_block = last_synced_block
    db.session.commit()

    if last_synced_block < current_block_number:
        fetch_event_logs.apply_async(args=[subscription.id])
    return logs

def insert_logs(subscription, logs):
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
    collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
    collection.insert_many(formatted_logs)


def get_topic_input_types(subscription):
    topic_inputs = [event['inputs'] for event in json.loads(subscription.abi['data']) if event.get('name') == subscription.topic][0]
    topic_input_types = {input['name']: input['type'] for input in topic_inputs}
    return topic_input_types





######## AGGREGATION LOGIC ###########

def sum(cursor, key, key_type):
    res = 0
    for record in cursor:
        if key_type == 'uint256':
            print(int.from_bytes(record['args'][key], byteorder='big', signed=False))
            res = res + int.from_bytes(record['args'][key], byteorder='big', signed=False)
    return res

def count(cursor, key, key_type):
    res = 0
    for _ in cursor:
        res = res + 1
    return res

def average(cursor, key, key_type):
    return sum(cursor, key, key_type) / count(cursor, key, key_type)

agg_func = {
    'sum': sum,
    'count': count,
    'average': average
}


def aggregate(collection_name, key, aggregator, filter_options={}, sort_options={}):
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
    collection = db[collection_name]
    cursor = collection.find(filter_options).sort(sort_options)
    print(agg_func[aggregator])
    return True, {'result': agg_func[aggregator](cursor, key, topic_input_types[key])}
    

