import pyupbit
import pandas as pd
import numpy as np
from collections import deque 
from functools import reduce 
import sys

#변동성 돌파 전략에서 목표가
def get_target_price(ticker):
    """
    목표가 구하기
    """
    target = []
    df = pyupbit.get_ohlcv(ticker)
    for i in range(2,len(df)+1):
        yesterday = df.iloc[-i]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target.append(round((today_open + (yesterday_high - yesterday_low) * 0.5),2))
    return target


def purchase_status(ticker):
    """
    수익률 계산
    """
    #배열의 곱 
    def multiply(arr):
        return reduce(lambda x, y: x * y, arr)

    #코인 정보 
    df = pyupbit.get_ohlcv(ticker)
    #목표주가 데이터 프레임에 추가
    target = deque(get_target_price(ticker))
    target.reverse()
    target.appendleft(sys.maxsize)
    df["target"] = target
    #수익률 데이터 프레임에 추가
    df["ror"] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
    ror = multiply(df.loc[:,"ror"])
    return ror



if __name__ == "__main__":
    print(purchase_status("META"))

