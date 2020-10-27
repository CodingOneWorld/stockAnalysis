# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

filepath = 'E:/Money/stocks.db'


def get_ST_stocks():
    # pandas连接数据库
    conn = sqlite3.connect(filepath)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stock_basic_list', conn)
    # print(stock_list_data.head())
    stock_list = stock_list_data[['symbol', 'name']].values
    ST_list = []
    for stock in stock_list:
        if stock[1].find('ST') > 0:
            ST_list.append(stock[0])
    # for s in ST_list:
    #     print(s)
    print("ST股票个数")
    print(len(ST_list))
    return ST_list


get_ST_stocks()
