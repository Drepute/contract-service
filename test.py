address = "0xC74063fdb47fe6dCE6d029A489BAb37b167Da57f"
chain_id = 137
_abi_data = '[{"inputs":[{"internalType":"address","name":"_admin","type":"address"},{"internalType":"contract IPortalsMulticall","name":"_multicall","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"outputAmount","type":"uint256"},{"internalType":"uint256","name":"minOutputAmount","type":"uint256"}],"name":"InsufficientBuy","type":"error"},{"inputs":[],"name":"InvalidShortString","type":"error"},{"inputs":[{"internalType":"string","name":"str","type":"string"}],"name":"StringTooLong","type":"error"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}, \
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},\
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"inputToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"inputAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"outputToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"outputAmount","type":"uint256"},{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"broadcaster","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":true,"internalType":"address","name":"partner","type":"address"}],"name":"Portal","type":"event"} \
    ,{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"domainSeparator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"invalidateNextOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"minOutputAmount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IPortalsRouter.Order","name":"order","type":"tuple"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"amountIndex","type":"uint256"}],"internalType":"struct IPortalsMulticall.Call[]","name":"calls","type":"tuple[]"}],"internalType":"struct IPortalsRouter.OrderPayload","name":"orderPayload","type":"tuple"},{"internalType":"address","name":"partner","type":"address"}],"name":"portal","outputs":[{"internalType":"uint256","name":"outputAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"minOutputAmount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IPortalsRouter.Order","name":"order","type":"tuple"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"amountIndex","type":"uint256"}],"internalType":"struct IPortalsMulticall.Call[]","name":"calls","type":"tuple[]"}],"internalType":"struct IPortalsRouter.OrderPayload","name":"orderPayload","type":"tuple"},{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"bool","name":"splitSignature","type":"bool"},{"internalType":"bool","name":"daiPermit","type":"bool"}],"internalType":"struct IPortalsRouter.PermitPayload","name":"permitPayload","type":"tuple"},{"internalType":"address","name":"partner","type":"address"}],"name":"portalWithPermit","outputs":[{"internalType":"uint256","name":"outputAmount","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"minOutputAmount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IPortalsRouter.Order","name":"order","type":"tuple"},{"internalType":"bytes32","name":"routeHash","type":"bytes32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint64","name":"deadline","type":"uint64"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct IPortalsRouter.SignedOrder","name":"signedOrder","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"amountIndex","type":"uint256"}],"internalType":"struct IPortalsMulticall.Call[]","name":"calls","type":"tuple[]"}],"internalType":"struct IPortalsRouter.SignedOrderPayload","name":"signedOrderPayload","type":"tuple"},{"internalType":"address","name":"partner","type":"address"}],"name":"portalWithSignature","outputs":[{"internalType":"uint256","name":"outputAmount","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"minOutputAmount","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IPortalsRouter.Order","name":"order","type":"tuple"},{"internalType":"bytes32","name":"routeHash","type":"bytes32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint64","name":"deadline","type":"uint64"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct IPortalsRouter.SignedOrder","name":"signedOrder","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"amountIndex","type":"uint256"}],"internalType":"struct IPortalsMulticall.Call[]","name":"calls","type":"tuple[]"}],"internalType":"struct IPortalsRouter.SignedOrderPayload","name":"signedOrderPayload","type":"tuple"},{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"bool","name":"splitSignature","type":"bool"},{"internalType":"bool","name":"daiPermit","type":"bool"}],"internalType":"struct IPortalsRouter.PermitPayload","name":"permitPayload","type":"tuple"},{"internalType":"address","name":"partner","type":"address"}],"name":"portalWithSignatureAndPermit","outputs":[{"internalType":"uint256","name":"outputAmount","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"tokenAmount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"recoverToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
abi = {'data': _abi_data}
topic = 'Portal'
from_block = 50806663 # 44652322 #
block_difference = 5



from event.models import Subscription
from db import db
subscription = Subscription.query.filter_by(id=1).first()
subscription.address = address
subscription.chain_id = chain_id
subscription.abi = abi
subscription.topic = topic
subscription.from_block = from_block
subscription.block_difference = block_difference
db.session.commit()


subscription_id = 1
from event.funcs import fetch_event_logs
x = fetch_event_logs(subscription_id)

import json
subscription_id = 1
subscription = Subscription.query.filter_by(id=1).first()
db = app.mongo_client.event_log
collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
collection.drop()

topic_inputs = [event['inputs'] for event in json.loads(subscription.abi['data']) if event.get('name') == subscription.topic][0]
topic_input_types = {input['name']: input['type'] for input in topic_inputs}
data_types = [param['type'] for param in next(event['inputs'] for event in subscription.abi['data'] if event['name'] == subscription.topic)['inputs']]

c = 0
for e in x:
    if e.args.partner == '0xF2F2F2FE93A744EcE90133F58F783f86C5b50FcF1B':
        c = c + 1

# print(c)

# from flask import current_app as app
# db = app.mongo_client.event_log
# collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
# collection.insert_many(formatted_logs)


# for f_log in formatted_logs[2:]:
#     print(f_log)
#     collection.insert_one(f_log).inserted_id


filter_key = "some_key"

# Aggregation pipeline with a $match stage
pipeline = [
    {
        "$match": {
            "args.partner": "0xF2F2FE93A744EcE90133F58F783f86C5b50FcF1B" ,
            "args.inputToken": "0x0000000000000000000000000000000000000000"
        }
    },
    {
        "$group": {
            "_id": None,
            "totalAmount": {"$sum": {'$toInt': {'$binary': "args.inputToken", '$type': 'long'}}}
        }
    }
]

from flask import current_app as app
subscription_id = 1
subscription = Subscription.query.filter_by(id=1).first()
db = app.mongo_client.event_log
collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
# Execute the aggregation pipeline
result = list(collection.aggregate(pipeline))

# Extract the sum from the result
total_amount = result[0]["totalAmount"] if result else 0


from flask import current_app as app
subscription_id = 1
subscription = Subscription.query.filter_by(id=1).first()
db = app.mongo_client.event_log
collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
c = collection.find({
        "args.partner": "0xF2F2FE93A744EcE90133F58F783f86C5b50FcF1B", 
        "args.inputToken": "0x0000000000000000000000000000000000000000"
    }).sort({"blockNumber":  1})

for e in c:
    amount = int.from_bytes(e['args']['inputAmount'], byteorder='big', signed=False)
    print(amount)
    

subscription_id = 1
subscription = Subscription.query.filter_by(id=1).first()
db = app.mongo_client.event_log
collection = db[f"{subscription.address}-{subscription.chain_id}-{subscription.topic}"]
from event.funcs import aggregate
sum = aggregate(
    f"{subscription.address}-{subscription.chain_id}-{subscription.topic}", 
    "inputAmount", 
    "sum",
    {"args.partner": "0xF2F2FE93A744EcE90133F58F783f86C5b50FcF1B","args.inputToken": "0x0000000000000000000000000000000000000000"},
    {"blockNumber":  1}
)