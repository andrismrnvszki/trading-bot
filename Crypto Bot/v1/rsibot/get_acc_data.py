from datetime import datetime
import websocket, json, pprint, talib, numpy as np, math
import config
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET)
now = datetime.now()

try:
    print("Sending order")
    order = client.create_test_order(symbol='ETHUSDT',side='SELL',type=ORDER_TYPE_MARKET,quantity=1)
    #print(order)
    acc = client.get_account()
    #print(acc["balances"])
    for shit in acc["balances"]:
        if shit["asset"] == 'ETH':
            print("ETH: {}".format(shit['free']))
        if shit["asset"] == 'USDT':
            print("USDT: {}".format(shit['free']))
    
except Exception as e:
    print("Order failed - {}".format(e))
    