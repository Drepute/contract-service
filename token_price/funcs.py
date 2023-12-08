from token_price.models import TokenPriceSubscription
from flask import current_app as app
from db import db
from common.error_codes import *
import ccxt
import time


def subscribe(symbol, decimals, market, time_interval, start_timestamp, exchange):
    tp_subscription = TokenPriceSubscription.query.filter(
        TokenPriceSubscription.symbol == symbol,
        TokenPriceSubscription.time_interval == time_interval 
    ).first()
    if tp_subscription:
        return False, RESOURCE_EXISTS

    tp_subscription = TokenPriceSubscription(
        symbol = symbol,
        decimals = decimals,
        market = market,
        time_interval = time_interval,
        start_timestamp = start_timestamp,
        exchange = exchange
    )
    db.session.add(tp_subscription)
    db.session.commmit()
    return True, {'subscription_id': tp_subscription.id}


def run_task_subscriptions():
    from token_price.tasks import fetch_token_price
    tp_subscriptions = TokenPriceSubscription.query.filter_by(is_active=True).all()
    for tp_subscription in tp_subscriptions:
        if (tp_subscription.last_synced_timestamp/1000) + (tp_subscription.time_interval * 60) < int(time.time()):
            fetch_token_price.apply_async(args=[tp_subscription.id])


frequency_to_time_step = {
    60: "1h"
}

def fetch_token_price(subscription_id):
    tp_subscription = TokenPriceSubscription.query.filter_by(id=subscription_id).first()
    exchange = tp_subscription.exchange
    market = tp_subscription.market
    time_step = frequency_to_time_step[tp_subscription.time_interval]
    since = max(tp_subscription.start_timestamp, tp_subscription.last_synced_timestamp)
    
    ccxt_exchange = getattr(ccxt, exchange)()
    logs = ccxt_exchange.fetch_ohlcv(market, time_step, since=since)
    if len(logs) > 0:
        insert_ohlcv_logs(tp_subscription, logs)
    tp_subscription.last_synced_timestamp = logs[-1][0]
    db.session.commit()
    return logs


def insert_ohlcv_logs(tp_subscription, logs):
    db = app.mongo_client.token_log
    collection = db[f"{tp_subscription.symbol}-{tp_subscription.time_interval}"]
    formatted_logs = []
    for log in logs:
        f_log = {'timestamp': log[0], 'price': log[3]}
        formatted_logs.append(f_log)
    collection.insert_many(formatted_logs)