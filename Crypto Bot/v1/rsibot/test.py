from symtable import Symbol
from binance.client import Client
from binance.enums import *
import websocket, pprint, numpy as np, datetime
import config

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

TRADE_SYMBOL = 'ETHUSDT'

client = Client(config.API_KEY, config.API_SECRET)

def on_open(ws):
    print('Cpened connection')

order = client.get_asset_balance(asset='ETH')['free']
print(order)

order = client.get_trade_fee(symbol='ETHUSDT')
print(order)

historical_klines = client.get_historical_klines(symbol=TRADE_SYMBOL, interval='1m', limit=50)
pprint(historical_klines['close'])

now = datetime.now()

end_time_str= now.strftime("%Y-%m-%d %H:%M:%S")
print(end_time_str)
closes = []
historical_klines = np.array(client.get_historical_klines(TRADE_SYMBOL, client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"))
historical_klines_nparray=np.array(historical_klines)

for i in range(len(historical_klines_nparray)-200, len(historical_klines_nparray)):
    closes.append(round(float(historical_klines_nparray[i][4]),2))

# """ 
# order = {
#     "symbol": "BTCUSDT",
#     "orderId": 28,
#     "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#     "transactTime": 1507725176595,
#     "price": "0.12341234",
#     "origQty": "10.00000000",
#     "executedQty": "10.00000000",
#     "cummulativeQuoteQty": "10.00000000",
#     "status": "FILLED",
#     "timeInForce": "GTC",
#     "type": "MARKET",
#     "side": "SELL"
# }

# print(order["price"]) """

#import tkinter
#tkinter._test()