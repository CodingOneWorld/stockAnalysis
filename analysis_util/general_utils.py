# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from contants.common_contants import DB_PATH


def get_stock_name(stock_code):
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stockList', conn)
    return stock_list_data[stock_list_data['symbol']==stock_code]['name'].values[0]


def get_stock_code(stock_name):
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stockList', conn)
    return stock_list_data[stock_list_data['name']==stock_name]['symbol'].values[0]


# if __name__ == '__main__':
    # print(get_stock_code('金盘科技'))
