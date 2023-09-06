# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np

from analysis_util.cal_hist_price import cal_price_pct, cal_price_withdraw_pct
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from fundamental_data.get_ST_stocks import get_ST_stocks

if __name__ == '__main__':
    # 读取股票池
    file = 'stock_pool2023.txt'

    # 遍历股票池，计算当前股价所处的位置
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    # print(stock_list)

    low_price_s = []

    for line in stock_list:
    # for line in [['600031','三一重工']]:
        print(line)
        s = line[0]
        # 获取股票历史价格
        # pct=cal_price_pct(s,3000)
        # 计算股票回撤幅度
        pct = cal_price_withdraw_pct(s, 1000)
        # 计算趋势
        stock_price = get_stock_price(s, 'close')['close'].values
        k = cal_stock_price_trend(stock_price, 3000)
        print(pct,k)
        if pct >= 0.5 and k > 0:
            print('符合要求')
            low_price_s.append(list(line))

    print(low_price_s)

    df=pd.DataFrame(low_price_s,columns=['symbol','stock_name'])
    print(df)
    df.to_csv('大幅回撤股票2023.txt',index=0)