import config, websocket, json, pprint, numpy as np, talib, math
from binance.client import Client
from binance.enums import *
from datetime import datetime

length = 20
mult = 2.0
lengthKC = 20
multKC = 1.5

TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.01
TRADE_BUY_PRICE = 3345
inTradeBool=True

closes = []
highs = []
lows = []

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1h"

client = Client(config.API_KEY, config.API_SECRET)
print('\nLogged in!')

now = datetime.now()

end_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(end_time_str)
closes = []
historical_klines = np.array(
    client.get_historical_klines(TRADE_SYMBOL, client.KLINE_INTERVAL_1HOUR,
                                 "9 day ago UTC"))
historical_klines_nparray = np.array(historical_klines)
#print(historical_klines_nparray)
for i in range(len(historical_klines_nparray) - 200, len(historical_klines_nparray)):
    closes.append(float(historical_klines_nparray[i][4]))
    highs.append(float(historical_klines_nparray[i][2]))
    lows.append(float(historical_klines_nparray[i][3]))

print("Historical data loaded!")
#print(closes)
#print(len(closes))


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    global TRADE_BUY_PRICE
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol,
                                    side=side,
                                    type=order_type,
                                    quantity=quantity)
        #order = client.create_test_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
        print("The price was {}".format(round(float(order['fills'][0]['price']), 2)))
        if (side == SIDE_BUY):
            TRADE_BUY_PRICE = round(float(order['fills'][0]['price']), 2)
        

    except Exception as e:
        print("Order failed - {}".format(e))
        return False

    return True

def on_open(ws):
    print('Opened connection\n')

def on_close(ws):
    print('Closed connection')

def on_message(ws, message):
    global inTradeBool, TRADE_BUY_PRICE
    json_message = json.loads(message)
    #pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = round(float(candle['c']), 2)
    high = round(float(candle['h']), 2)
    low = round(float(candle['l']), 2)
    

    if is_candle_closed:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Candle closed at {} at {}".format(close, current_time))
        closes.append(float(close))
        closes.pop(0)
        highs.append(float(high))
        highs.pop(0)
        lows.append(float(low))
        lows.pop(0)
        np_closes = np.array(closes)
        stdev = talib.STDDEV(np_closes, length, 1)
        sma = talib.SMA(np_closes, length)
        maxes = highs[-20:]
        mins = lows[-20:]
        h = np.array(sma[-20:])
        h = np.append(h, np.mean(np.append(mins, maxes)))
        h = np.mean(h)
        o = np_closes - h
        faszsetudjami = talib.LINEARREG_SLOPE(o,20)
        print(faszsetudjami[-2:])
        ema = talib.EMA(np.array(closes), 200)
        #print(sma)
        if (faszsetudjami[-1]-0.01 > 0 and faszsetudjami[-2]-0.01 < 0 and inTradeBool == False and ema[-1] < close):
            print("Buy bitches")

            order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
            if order_succeeded:
                inTradeBool = True
                print('The buy was succesfull')
            else:
                print("No trade for you")
            
        elif (faszsetudjami[-1]-0.01 < 0 and faszsetudjami[-2]-0.01 > 0 and inTradeBool == True and TRADE_BUY_PRICE < close):
            print("Sell bitches")

            order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
            if order_succeeded:
                inTradeBool = False
                print('The buy was succesfull')
                
                profit = ((round(float(order['fills'][0]['price']), 2))/(TRADE_BUY_PRICE))-1
                print("The profit was: {}%".format(profit))
            else:
                print("No trade for you")

        print("\n")
        
        
        



ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_close=on_close,
                            on_message=on_message)
ws.run_forever()