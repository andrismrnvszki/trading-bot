from ctypes import sizeof
from datetime import datetime
import websocket, json, pprint, talib, numpy as np
import config
from binance.client import Client
from binance.enums import *

TIME_PERIOD='1h' #TODO


SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_"+TIME_PERIOD

client = Client(config.API_KEY, config.API_SECRET)
print('\nLogged in!')

