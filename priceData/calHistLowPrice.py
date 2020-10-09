# -*- coding: utf-8 -*-

# 遍历数据库，查询股票的价格数据，最低价，最高价，当前价格
import sqlite3

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

filepath = 'E:/Money/stocks.db'


def calHistPrice():
    # pandas连接数据库
    conn = sqlite3.connect(filepath)
    # 读取股票基本信息表
    stockListData = pd.read_sql('select * from stock_basic_list', conn)
    print(stockListData.head())
    stockList=stockListData['symbol'].values
    print(stockList)
    # 遍历读取每一个股票的日交易数据，计算其最低价，最高价，上市日期等
    # for stock in stockList:
    #     table_name=


def calHistPriceofStock(ts_code):
    # pandas连接数据库
    conn = sqlite3.connect(filepath)
    # 读取相应的交易数据表
    table_name = 'S' + ts_code.split('.')[0] + '_daily'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from '+table_name, conn)
    print(stock_trade_data.head())
    stock_price = stock_trade_data['close'].values
    print(stock_price)

calHistPriceofStock('000001.SZ')