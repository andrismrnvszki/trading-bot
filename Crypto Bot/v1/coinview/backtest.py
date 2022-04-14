from matplotlib.pyplot import close
import numpy as np
import talib
from datetime import datetime
import websocket, json, pprint, talib, numpy as np, math
import config
from binance.client import Client
from binance.enums import *
from positions import Positions
from positions import Position
import csv


field_names = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
closes = []
current_closes = []

balance = 200
avg_price = 0
open_positions = 0
position_size = 0.01
commission = 0.001
no_of_trades = 0

RSI_PERIOD = 14

best_rsi_L = 0
best_rsi_H = 0
best_precent = 0
best_balance = 0
best_open_avg_mult = 0


def order(type, price):
    global open_positions, avg_price, balance, position_size, commission, no_of_trades
    if type == 'buy':
        if balance > price * position_size:
            avg_price = ( avg_price * open_positions + price ) / ( open_positions + 1 )
            open_positions = open_positions + 1
            balance = balance - ( price * position_size * ( 1 + commission ) )
            #print('We bought at {}, {} pieces, the balance is {}, the average is {}'.format(price, position_size, balance, avg_price))
    if type == 'sell' and open_positions > 0:
        balance = balance + ( price * position_size * ( 1 - commission ) )
        open_positions = open_positions -1 
        no_of_trades = no_of_trades  + 1
        #print('We sold at {}, {} pieces, the balance is {}'.format(price, position_size, balance))
        if open_positions == 0:
            avg_price = 0


with open(r'C:\Users\marin\Python\Crypto Bot\v1\coinview\data\ETHUSDT_2021-_5minutes.csv', 'r') as f:
        raw_data = csv.reader(f)
        for i in raw_data:
            closes.append(float(i[4]))


#for rsi_L in range(10, 30, 5):
    #for rsi_H in range(70, 90, 5):
        #for precent in range(0, 500, 5):
            #for open_avg_mult in range(50,300,50):
                #precent = precent/1000
current_closes = closes[:200]

for i in range(200, len(closes)):
                    current_closes.append(closes[i])
                    current_closes.pop(0)
                    np_current_closes = np.array(current_closes)

                    rsi = talib.RSI(np_current_closes, RSI_PERIOD)
                    last_rsi = rsi[-1]
                                #SMA_RSI = np.average(rsi[-14:])
                                #SMA_slow = np.average(np_current_closes[-200:])
                                #SMA_fast = np.average(np_current_closes[-50:])

                    if last_rsi < 25 and avg_price == 0 or avg_price * (1 - open_positions/50 ) > current_closes[-1]:
                        order('buy', current_closes[-1])

                    if last_rsi > 75 and avg_price * (1 + 0.4) < current_closes[-1]:
                        order('sell', current_closes[-1])

                            #print(balance)
                            #print(no_of_trades)
                            #print(open_positions*position_size*avg_price)

                # if balance > best_balance:
                #     best_rsi_L = rsi_L
                #     best_rsi_H = rsi_H
                #     best_precent = precent
                #     best_balance = balance
                #     best_open_avg_mult = open_avg_mult
                #print('The current best balance is {}, with rsi L {}, with rsi H {}, with precent {}, with drawdown multiplyer {}'.format(balance, rsi_L, rsi_H, precent, best_open_avg_mult))
print('The current best balance is {}'.format(balance))
print('No. of trades {}'.format(no_of_trades))
print('Crypto worth {}'.format(avg_price*open_positions*position_size))
                # balance = 200
                # avg_price = 0
                # open_positions = 0
                # current_closes = []

