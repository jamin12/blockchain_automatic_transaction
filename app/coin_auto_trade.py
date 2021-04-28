from os import path as op
from sys import path as sp

sp.append(op.dirname(op.dirname(__file__)))

from app.common.consts import ACCESS, SCERET

import pyupbit
import datetime
import time

access = ACCESS
secret = SCERET
# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


def get_balance(ticker):
    """
    잔고 조회
    """
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0


def get_start_time(ticker):
    """
    시작 시간 조회
    """
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_yesterday_ma5(ticker):
    """
    5일 이동평균선
    """
    df = pyupbit.get_ohlcv(ticker)
    close = df["close"]
    ma = close.rolling(window=5).mean()
    return ma[-2]


def get_target_price(ticker):
    """
    목표가
    """
    df = pyupbit.get_ohlcv(ticker)

    yesterday = df.iloc[-2]
    today_open = yesterday["close"]
    yesterday_high = yesterday["high"]
    yesterday_low = yesterday["low"]
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


if __name__ == "__main__":
    try:
        while True:
            now = datetime.datetime.now()
            start_time = get_start_time("META")
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price("META")
                current_price = pyupbit.get_current_price("META")
                ma5 = get_yesterday_ma5("META")
                if target_price < current_price and target_price < ma5:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-META", krw * 0.9995)
            else:
                meta = get_balance("META")
                if meta > 50:
                    upbit.sell_market_order("KRW-META", meta * 0.9995)
    except Exception as e:
        print(e)
        time.sleep(1)
