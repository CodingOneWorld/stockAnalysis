# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from constants.common_constants import DB_PATH


def get_ST_stocks():
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stock_basic_list', conn)
    # print(stock_list_data.head())
    stock_list = stock_list_data[['symbol', 'name']].values
    ST_list = []
    for stock in stock_list:
        # print(stock)
        if stock[1].__contains__('ST') and not stock[1].__contains__('退'):
            ST_list.append(stock[0])
            # print("1")
    # for s in ST_list:
    #     print(s)
    print("ST股票个数")
    print(len(ST_list))
    return ST_list


get_ST_stocks()
