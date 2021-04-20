# ch06/06_16.py
import time
import pyupbit
import datetime

#5일 이동평균선
def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]

#변동성 돌파 전략에서 목표가
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    print(df)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target



if __name__ == "__main__":
    # now = datetime.datetime.now()
    # mid = datetime.datetime(now.year, now.month, now.day, 9,00,00) + datetime.timedelta(1)
    # target_price = get_target_price("KRW-META")

    # while True:
    #     now = datetime.datetime.now()
    #     if mid < now < mid + datetime.delta(seconds=10) : 
    #         target_price = get_target_price("KRW-META")
    #         mid = datetime.datetime(now.year, now.month, now.day, 9, 00, 00) + datetime.timedelta(1)


    #     current_price = pyupbit.get_current_price("META")
    #     print(current_price)

    #     time.sleep(1)
    print(get_target_price("META"))


