# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd

from contants.commonContants import DB_PATH
from technicalAnalysis.cal_stock_trend import cal_stock_trend


def select_up_trend_of_all_stocks(latest_days):
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stockList', conn)
    print(stock_list_data.head())
    stock_list = stock_list_data['symbol'].values
    print(stock_list)
    # 遍历读取每一个股票的日交易数据，计算其最低价，最高价，上市日期等
    stock_array = []
    for stock in stock_list:
        k=cal_stock_trend(stock,latest_days)
        if k>0:
            print(stock+":"+str(k))
            stock_array.append(stock)
    return stock_array


if __name__ == '__main__':
    up_trend_stocks=select_up_trend_of_all_stocks(5)
    print(up_trend_stocks)