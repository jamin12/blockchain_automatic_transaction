from os import path as op
from sys import path as sp
sp.append(op.dirname(op.dirname(__file__)))



import pyupbit

#변동성 돌파 전략에서 목표가
def get_target_price(ticker):
    target = []
    df = pyupbit.get_ohlcv(ticker)
    # df.to_excel("upbit.xlsx")
    for i in range(2,len(df)):
        yesterday = df.iloc[-i]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target.append(round((today_open + (yesterday_high - yesterday_low) * 0.5),2))
    return target


def purchase_status():
    ...



if __name__ == "__main__":
    a = get_target_price("META")
    print(a)

