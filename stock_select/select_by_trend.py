# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import numpy as np

from constants.common_constants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_price_trend, get_stock_price


# 选取最近n天呈上涨趋势的股票
def select_up_trend_stocks(stock_list,latest_days):
    # print(stock_list)
    # 遍历读取每一个股票的日交易数据，计算其最低价，最高价，上市日期等
    stock_array = []
    for stock in stock_list:
        # print(stock)
        stock_price = get_stock_price(stock[0], 'close')
        k=cal_stock_price_trend(stock_price,latest_days)
        if k>=0.3:
            print(stock[0]+":"+str(k))
            stock_array.append(stock)
    return stock_array


if __name__ == '__main__':
    df = pd.read_csv('stock_pool.txt', delimiter=',', dtype={'symbol': np.str})
    print(df.head())
    stock_list = list(df.values)
    stock_array=select_up_trend_stocks(stock_list,50)
    stock_array=pd.DataFrame(stock_array,columns=['symbol','stock_name'])
    print(stock_array)
