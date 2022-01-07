import pyupbit
import pandas
import datetime
import time
import telepot

def rsi(ohlc: pandas.DataFrame, period:int = 14) :
    delta = ohlc['close'].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    period = 14
    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

tickers = pyupbit.get_tickers(fiat='KRW')

token = '5008461782:AAEqAxUVEIKOYhZAr4gvj1UIqNkN1tCvD7k'
mc = '1950703241'

bot = telepot.Bot(token)

while 1:
    for i in range(len(tickers)):
        data = pyupbit.get_ohlcv(ticker=tickers[i], interval="minute5")
        now_rsi = rsi(data, 14).iloc[-1]
        if now_rsi < 40:
        #if now_rsi < 30 and tickers[i] != 'KRW-BTT':
            print(datetime.datetime.now(), now_rsi)
            bot.sendMessage(mc, tickers[i])
            print(tickers[i])
            print('RSI : ', now_rsi)
        time.sleep(0.1)
