# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np

from analysis_util.cal_hist_price import cal_price_pct
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from constants.common_constants import DB_PATH
from fundamental_data.get_ST_stocks import get_ST_stocks


if __name__ == '__main__':
    # 读取股票池
    file = 'stock_pool2023.txt'

    # 遍历股票池，计算当前股价所处的位置
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)

    low_price_s=[]

    for line in stock_list:
        print(line)
        s = line[0]
        # 获取股票历史价格
        pct=cal_price_pct(s,3000)
        # 计算趋势
        stock_price = get_stock_price(s, 'close')['close'].values
        k = cal_stock_price_trend(stock_price, 3000)
        if pct<0.5 and k>0.01:
            print('符合要求')
            low_price_s.append(list(line))

    print(low_price_s)






    # # pandas连接数据库
    # conn = sqlite3.connect(DB_PATH)
    # # 读取股票基本信息表
    # stock_price_df = pd.read_sql('select * from stockHistoryPrice', conn)
    # # stock_price_df = calHistPriceofAllStocks()
    # stock_price_df['position'] = stock_price_df['current_price'] / (
    #         stock_price_df['max_price'] - stock_price_df['min_price'])
    # low_price_stock = stock_price_df[stock_price_df['position'] < 0.1]
    # print(low_price_stock.head())
    # low_price_stock = list(low_price_stock['code'])
    # set_low_price_stock = set(low_price_stock)
    # print(set_low_price_stock)
    # ST_sets = set(get_ST_stocks())
    # low_price_stock = set_low_price_stock.difference(ST_sets)
    # for line in low_price_stock:
    #     print(line)
