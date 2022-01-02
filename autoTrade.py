import time
import pyupbit
import datetime
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
 
    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

ticker_list = ["KRW-NEAR", "KRW-BTC", "KRW-SAND", "KRW-SXP", "KRW-XRP"]
ticker_status = ["sell", "sell", "sell", "sell", "sell"]
ticker_buy_uuid = ["", "", "", "", ""]
price_5percent = [0, 0, 0, 0, 0]

save_time = ""

# 자동매매 시작
while 1:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ADA") # 09:00
        end_time = start_time + datetime.timedelta(days=1) # 09:00 + 1일

        if save_time != start_time:
            for i in range(len(ticker_status)):
                ticker_status[i] = "sell"
                ticker_buy_uuid[i] = ""
                price_5percent[i] = 0
            save_time = start_time

        if start_time < now < end_time - datetime.timedelta(hours=3):
            for i in range(len(ticker_list)) :
                if ticker_status[i] != "hold" and get_target_price(ticker_list[i], 0.4) > get_current_price(ticker_list[i]) :
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(ticker_list[i], 100000)
                        time.sleep(5)
                        price_2percent = round(get_current_price(ticker_list[i])*1.02)
                        price_2percent = price_2percent - (price_2percent % get_hoga(price_2percent))

                        price_5percent[i] = round(get_current_price(ticker_list[i])*0.95)
                        price_5percent[i] = price_5percent[i] - (price_5percent[i] % get_hoga(price_5percent[i]))

                        ticker_buy_uuid[i] = upbit.sell_limit_order(ticker_list[i], price_2percent, get_balance(ticker_list[i][4:])*0.9995)
                        ticker_status[i] = "hold"
                if ticker_status[i] == "hold" and get_current_price(ticker_list[i]) < price_5percent[i]:
                    upbit.cancel_order(ticker_buy_uuid[i])
                    time.sleep(5)
                    ticker_balance = get_balance(ticker_list[i])
                    if ticker_balance > 0.00008 :
                        upbit.sell_market_order(ticker_list[i], ticker_balance*0.9995)
        else:
            for i in range(len(ticker_list)) :
                ticker_balance = get_balance(ticker_list[i])
                if ticker_balance > 0.00008 :
                    upbit.sell_market_order(ticker_list[i], ticker_balance*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)