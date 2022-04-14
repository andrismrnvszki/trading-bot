from datetime import datetime
import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70  #TODO to 75
RSI_OVERSOLD = 30    #TODO to 25
TRADE_SYMBOL = 'ETHUSDT'
crypto='ETH'
TRADE_QUANTITY = 0.004
TRADE_QUANTITY_SELL=0
TIME_PERIOD='5m' #TODO

closes = []
in_position = True

client = Client(config.API_KEY, config.API_SECRET)
print("Logged in!")

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("Order failed - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('Cpened connection')

def on_close(ws):
    print('Closed connection')

def on_message(ws, message):
    global closes, in_position
    
    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("Candle closed at {}".format(close))
        closes.append(float(close))
        #print("closes")
        #print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            #print("all rsis calculated so far")
            #print(rsi)
            now = datetime.now()
            current_time= now.strftime("%Y-%m-%d %H:%M:%S")
            last_rsi = rsi[-1]
            print("The current RSI is {} at {} \n \n ".format(last_rsi, current_time))


            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    #FIXME
                    #balance=client.get_asset_balance(asset=crypto)['free']
                    #if balance > TRADE_QUANTITY:
                    #    TRADE_QUANTITY_SELL=TRADE_QUANTITY
                    #else:
                    #    TRADE_QUANTITY_SELL=balance
                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY_SELL, TRADE_SYMBOL)
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                    else:
                        print("No trade for you")
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!" )
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
                    else:
                        print("No trade for you")

            #if 70 >= last_rsi >= 50:
            #    in_position = True

            #if 50 > last_rsi >= 30:
            #    in_position = False

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

