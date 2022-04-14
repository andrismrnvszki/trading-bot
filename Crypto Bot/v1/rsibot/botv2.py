from datetime import datetime
import websocket, json, pprint, talib, numpy as np, math
import config
from binance.client import Client
from binance.enums import *

RSI_PERIOD = 14
RSI_OVERBOUGHT = 80  #TODO to 75
RSI_OVERSOLD = 20  #TODO to 25
TRADE_SYMBOL = 'ETHUSDT'
crypto = 'ETH'
TRADE_QUANTITY = 0.01
TRADE_QUANTITY_SELL = 0
TIME_PERIOD = '5m'  #TODO

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_" + TIME_PERIOD

client = Client(config.API_KEY, config.API_SECRET)
print('\nLogged in!')

in_position = True
already_bought = False
already_sold = False
average_price = 2807
open_positions = 9

now = datetime.now()

end_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(end_time_str)
closes = []
historical_klines = np.array(
    client.get_historical_klines(TRADE_SYMBOL, client.KLINE_INTERVAL_5MINUTE,
                                 "1 week ago UTC"))
historical_klines_nparray = np.array(historical_klines)

for i in range(
        len(historical_klines_nparray) - 200, len(historical_klines_nparray)):
    closes.append(round(float(historical_klines_nparray[i][4]), 2))

print("Historical data loaded!")
print("The profit is {} %.".format(round(((closes[-1]/average_price)*100)-100, 2)))


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    global open_positions, average_price
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol,
                                    side=side,
                                    type=order_type,
                                    quantity=quantity)
        #order = client.create_test_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
        print("The price was {}".format(
            round(float(order['fills'][0]['price']), 2)))
        if side == SIDE_BUY:
            tmp = float(open_positions)
            open_positions = open_positions + 1
            average_price = (average_price * tmp + float(
                order['fills'][0]['price'])) / open_positions
            print('The new average price is {}'.format(
                round(float(average_price), 2)))
        else:
            if open_positions != 0:
                open_positions = open_positions - 1
            if open_positions == 0:
                average_price = 0
            print('The average price is {}'.format(
                round(float(average_price), 2)))
    except Exception as e:
        print("Order failed - {}".format(e))
        return False

    return True


def on_open(ws):
    print('Opened connection')


def on_close(ws):
    print('Closed connection')


def on_message(ws, message):
    global closes, already_sold, already_bought, open_positions, average_price

    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = round(float(candle['c']), 2)

    if is_candle_closed:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("\nCandle closed at {} at {}".format(close, current_time))
        closes.append(float(close))
        closes.pop(0)
        #print(len(closes))
        #print(closes[0])
        #print(closes[1])
        #print(closes[-1])
        #now = datetime.now()
        #current_time= now.strftime("%Y-%m-%d %H:%M:%S")
        #print(current_time)

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            last_rsi = rsi[-1]
            #SMA_RSI = np.average(rsi[-14:])
            #SMA_slow = np.average(closes[-200:])
            #SMA_fast = np.average(closes[-50:])
            #print("The current RSI is {}, SMA_RSI is {}, slow SMA is {}, fast SMA is {}. \nThe average price is {}, and there is {} open position(s)".format(
            #    round(last_rsi, 2), round(SMA_RSI, 2), round(SMA_slow, 2), round(SMA_fast, 2), math.ceil(average_price), open_positions))
            #print('The average price is {}'.format(average_price))

            #BUYING
            if average_price == 0 and last_rsi < 25 or average_price * (1 - ( open_positions / 50 )) > closes[-1] and last_rsi < 25: # or average_price * (0.98 - open_positions / 100) > closes[-1]:
                #if ((SMA_RSI < 35 and last_rsi < 30 and average_price == 0 or last_rsi < 30 and average_price * 0.99 > close[-1]) and closes[-1] < SMA) or average_price * 0.95 > closes[-1] and last_rsi < 30 or average_price * 0.90 > closes[-1]:
                print('Buyerino pepperino')

                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    already_bought = True
                    print('The buy was succesfull')
                else:
                    print("No trade for you")

            #SELLING
            elif last_rsi > 75 and average_price * 1.4 < closes[-1]:# and not already_sold or last_rsi > 75 and SMA_RSI > 70 and average_price * 1.011 < closes[-1]:# or last_rsi >= 95 and SMA_RSI >= 85:# or last_rsi>85 and SMA_RSI>70 and average_price * 1.002 < closes[-1]:
                #if ((SMA_RSI > 65 and last_rsi > 70 and not already_sold or last_rsi > 85 or last_rsi > 80 and SMA_RSI > 70) and average_price * 1.003 < closes[-1]):
                #and average_price * 1.011 < closes[-1]
                print('Sellerino pepperino')

                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY,
                                        TRADE_SYMBOL)
                if order_succeeded:
                    already_sold = True
                    print('The sell was succesfull')
                else:
                    print("No trade for you")
            else:
                print("The current RSI is {}.\nThe average price is {}, there is {} open position(s), the profit is {} %.".format(
                    round(last_rsi, 2), math.ceil(average_price), open_positions, round(((closes[-1]/average_price)*100)-100, 2)))
            #print('The average price is {}'.format(average_price))


            #if last_rsi <= 65:
            #    already_sold = False

            #if last_rsi >= 40:
            #    already_bought = False


ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_close=on_close,
                            on_message=on_message)
ws.run_forever()