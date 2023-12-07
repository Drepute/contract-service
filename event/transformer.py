from flask import current_app as app


class AmountToUSDAmountAdapter:
    db = app.mongo_client.price

    """
    params:
        key: args.key
        symbol: Token Symbol (ETH, BTC etc)
        blockNumber: "latest" or block number (blockNumber will be of record if key not found)

    """
    def process(records, params):
        for record in records:
            record['args'][params['key']] = record['args'][params['key']] * \
                AmountToUSDAmountAdapter.get_price(
                    params['symbol'], 
                    params.get('blockNumber', record['blockNumber']),
                    params.get('frequency', 30)
                )

    def get_price(self, symbol, block_number):
        # TODO
        collection = self.db['symbol']
        return collection.find()


class Transformer:
    adapters = {
        'usd_volume': AmountToUSDAmountAdapter
    }

    def __init__(self, options):
        self.adapters = options.get('adapters')
        self.params_list = options.get('params_list', {})

    
    def transform(self, records):
        in_process_records = records
        for i, adapter in enumerate(self.adapters):
            in_process_records = self.adapters.get(adapter['name']).process(in_process_records, self.params_list[i])
        return in_process_records
