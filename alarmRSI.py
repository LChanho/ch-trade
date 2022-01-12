import pyupbit
import pandas
import datetime
import time
import telepot
from decimal import *

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

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_avg_buy_price(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0

def get_profit_price(ticker):
    price = round(get_current_price(ticker)*1.01)
    price = price - (price % get_hoga(price))
    return price

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_hoga(cur_price):
    try:
        # 호가 단위
        if Decimal(str(cur_price)) < 10:
            hoga_val = 0.01
        elif Decimal(str(cur_price)) < 100:
            hoga_val = 0.1
        elif Decimal(str(cur_price)) < 1000:
            hoga_val = 1
        elif Decimal(str(cur_price)) < 10000:
            hoga_val = 5
        elif Decimal(str(cur_price)) < 100000:
            hoga_val = 10
        elif Decimal(str(cur_price)) < 500000:
            hoga_val = 50
        elif Decimal(str(cur_price)) < 1000000:
            hoga_val = 100
        elif Decimal(str(cur_price)) < 2000000:
            hoga_val = 500
        else:
            hoga_val = 1000
        return hoga_val
    except Exception:
        raise

tickers = pyupbit.get_tickers(fiat='KRW')

token = '5008461782:AAEqAxUVEIKOYhZAr4gvj1UIqNkN1tCvD7k'
mc = '1950703241'
bot = telepot.Bot(token)

access = "4eBjPLU8uWxUxE1Axi59axxzHG2AXZZENSJgYJ65"
secret = "88SvYJoj9em7w7XlV9DCqjNItfXuZtpjJxdfZ91n"
upbit = pyupbit.Upbit(access, secret)

while 1:
    for i in range(len(tickers)):
        data = pyupbit.get_ohlcv(ticker=tickers[i], interval="minute5")
        now_rsi = rsi(data, 14).iloc[-1]
        if now_rsi < 30 and tickers[i] != 'KRW-BTT' and get_balance(tickers[i]) < 5000:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order(tickers[i], 100000)
        if get_balance(tickers[i]) > 0 and get_current_price(tickers[i]) > get_avg_buy_price(tickers[i]) * 1.02:
            upbit.sell_market_order(tickers[i], get_balance(tickers[i]))
            bot.sendMessage(mc, tickers[i] + '익절')
        elif get_balance(tickers[i]) > 0 and get_current_price(tickers[i]) < get_avg_buy_price(tickers[i]) * 0.98:
            upbit.sell_market_order(tickers[i], get_balance(tickers[i]))
            bot.sendMessage(mc, tickers[i] + '손절')
                #target_price = get_profit_price(tickers[i]) # +1%
                #upbit.sell_limit_order(tickers[i], target_price, get_balance(tickers[i][4:]))
            #print(datetime.datetime.now(), now_rsi)
            #bot.sendMessage(mc, tickers[i])
            #print(tickers[i])
            #print('RSI : ', now_rsi)
        time.sleep(0.05)
