import websocket, datetime, json



SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

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

    if is_candle_closed:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Candle closed at {} at {}".format(close, current_time))



ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_close=on_close,
                            on_message=on_message)
ws.run_forever()