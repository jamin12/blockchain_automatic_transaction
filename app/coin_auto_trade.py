import pyupbit
import datetime
import time


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

    while True:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-ETH")
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price("KRW-ETH")
                current_price = pyupbit.get_current_price("KRW-ETH")
                ma5 = get_yesterday_ma5("KRW-ETH")
                if target_price < current_price and target_price < ma5:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-ETH", krw * 0.9995)
            else:
                meta = get_balance("KRW-ETH")
                if meta > 50:
                    upbit.sell_market_order("KRW-ETH", meta * 0.9995)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
