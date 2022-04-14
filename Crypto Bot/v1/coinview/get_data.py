import config, csv
from binance.client import Client
from datetime import datetime

client = Client(config.API_KEY, config.API_SECRET)

# prices = client.get_all_tickers()

# for price in prices:
#     print(price)

csvfile = open(r'C:\Users\marin\Python\Crypto Bot\v1\coinview\data\ETHUSDT_2021-_5minutes.csv', 'w', newline='') 
candlestick_writer = csv.writer(csvfile, delimiter=',')

#candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jan, 2020", "23 Jan, 2022")
candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan 2021")
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "12 Jul, 2020")

for candlestick in  candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvfile.close()


# C:\Users\marin\Python\Crypto Bot\v1\coinview\data\ETHUSDT_2020-_1hour.csv