from flask import current_app as app
from datetime import datetime as dt, timedelta


class BaseAdapter:
    def __init__(self, event_subscription):
        self.event_subscription = event_subscription

    def get_price(self, symbol, block_number, frequency):
        block_timestamp = self.get_block_ts(block_number)
        nearest_timestamp = self.get_nearest_ts(block_timestamp, frequency)
        db = app.mongo_client.token_log
        collection = db[f"{symbol}-{frequency}"]
        record = collection.find({'timestamp': nearest_timestamp*1000})[0]
        return record['price']
    
    def get_block_ts(self, block_number):
        db = app.mongo_client.block_log
        collection = db[f"{self.event_subscription.chain_id}"]
        record = collection.find({'blockNumber': block_number})[0]
        return record['timestamp']
    
    def get_nearest_ts(self, timestamp, frequency):
        if frequency == 60:
            dt_object = dt.fromtimestamp(timestamp)
            rounded_dt = dt_object.replace(minute=0, second=0, microsecond=0)
            # If the timestamp's minute component is greater than 30, round to the next hour
            if dt_object.minute >= 30:
                rounded_dt += timedelta(hours=1)
            return int(rounded_dt.timestamp())
        return timestamp
    


class BinDataIntAdapter(BaseAdapter):
    """
    params:
        key: args.key
        symbol: Token Symbol (ETH, BTC etc)
        decimals: decimals of symbol (18)
        blockNumber: "latest" or block number (blockNumber will be of record if key not found)
        frequency: fetch price of symbol rounded to the timestamp as per frequency (eg 60 means price at nearest hr mark)
    """
    def process(self, records, params):
        for record in records:
            record["args"][params['key']] = int.from_bytes(record['args'][params['key']], byteorder='big', signed=False)
        return records
    

class AmountToUSDAmountAdapter(BaseAdapter):
    """
    params:
        key: args.key
        symbol: Token Symbol (ETH, BTC etc)
        decimals: decimals of symbol (18)
        blockNumber: "latest" or block number (blockNumber will be of record if key not found)
        frequency: fetch price of symbol rounded to the timestamp as per frequency (eg 60 means price at nearest hr mark)
    """
    def process(self, records, params):
        for record in records:
            price = self.get_price(
                    params['symbol'], 
                    params.get('blockNumber', record['blockNumber']),
                    params.get('frequency', 60),
            )
            record['args'][params['key']] = (record['args'][params['key']] * price) / (10**params['decimals'])
        return records

class Transformer:
    adapter_name_cls_map = {
        'usd_volume': AmountToUSDAmountAdapter,
        "bin_data_int": BinDataIntAdapter
    }

    def __init__(self, event_subscription, options):
        self.event_subscription = event_subscription
        self.adapters = options.get('adapters')
        self.params_list = options.get('params_list', {})

    
    def transform(self, records):
        in_process_records = records
        for i, adapter in enumerate(self.adapters):
            adapter = self.adapter_name_cls_map.get(adapter['name'])(self.event_subscription)
            in_process_records = adapter.process(in_process_records, self.params_list[i])
        return in_process_records
