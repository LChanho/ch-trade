import time
import pyupbit
import datetime
import schedule
import telepot
from decimal import *

access = "4eBjPLU8uWxUxE1Axi59axxzHG2AXZZENSJgYJ65"
secret = "88SvYJoj9em7w7XlV9DCqjNItfXuZtpjJxdfZ91n"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

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

def get_profit_price(ticker):
    price = round(get_current_price(ticker)*1.02)
    price = price - (price % get_hoga(price))
    return price

def get_stop_loss_price(ticker):
    price = round(get_current_price(ticker)*0.95)
    price = price - (price % get_hoga(price))
    return price

token = '5008461782:AAEqAxUVEIKOYhZAr4gvj1UIqNkN1tCvD7k'
mc = '1950703241'

bot = telepot.Bot(token)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

ticker_dict = {"KRW-NEAR" : {}, "KRW-BTC" : {}, "KRW-SAND" : {}, "KRW-SXP" : {}, "KRW-XRP" : {}, "KRW-POWR" : {}, "KRW-BORA" : {}, "KRW-HUM" : {}, "KRW-ELF" : {}, "KRW-ATOM" : {}, "KRW-ETH" : {}, "KRW-MATIC" : {}}
#ticker_dict = {"KRW-NEAR" : {}, "KRW-BTC" : {}}

keys = list(ticker_dict.keys())
for i in range(len(keys)):
    ticker_dict[keys[i]]['status'] = 'ready'
    ticker_dict[keys[i]]['target_price'] = 0
    ticker_dict[keys[i]]['buy_uuid'] = ''
    ticker_dict[keys[i]]['stop_loss_price'] = 0

#schedule.every().day.at("09:00").do(init_data)

# 자동매매 시작
while 1:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ADA") # 09:00
        end_time = start_time + datetime.timedelta(days=1) # 09:00 + 1일

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            for i in range(len(keys)) :
                if ticker_dict[keys[i]]['status'] == "ready" and get_target_price(keys[i], 0.4) < get_current_price(keys[i]) :
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(keys[i], 100000)
                        time.sleep(1)

                        target_price = get_profit_price(keys[i]) # +2%
                        stop_loss_price = get_stop_loss_price(keys[i]) # -5%

                        ticker_dict[keys[i]]['target_price'] = target_price
                        ticker_dict[keys[i]]['stop_loss_price'] = stop_loss_price
                        ticker_dict[keys[i]]['uuid'] = upbit.sell_limit_order(keys[i], ticker_dict[keys[i]]['target_price'], get_balance(keys[i][4:])*0.9995)
                        ticker_dict[keys[i]]['status'] = 'hold'
                if ticker_dict[keys[i]]['status'] == "hold" and (get_current_price(keys[i]) < ticker_dict[keys[i]]['stop_loss_price']):
                    upbit.cancel_order(ticker_dict[keys[i]]['uuid'])
                    time.sleep(1)
                    ticker_balance = get_balance(keys[i])
                    if ticker_balance > 0.00008 :
                        upbit.sell_market_order(keys[i], ticker_balance*0.9995)
        else:
            for i in range(len(keys)) :
                ticker_balance = get_balance(keys[i])
                if ticker_balance > 0.00008 :
                    upbit.sell_market_order(keys[i], ticker_balance*0.9995)
                    ticker_dict[keys[i]]['target_price'] = 0
                    ticker_dict[keys[i]]['stop_loss_price'] = 0
                    ticker_dict[keys[i]]['uuid'] = ''
                    ticker_dict[keys[i]]['status'] = 'ready'
        time.sleep(1)
    except Exception as e:
        print(e)
        bot.sendMessage(mc, e)
        time.sleep(1)