# -*- coding: utf-8 -*-

# 遍历数据库，查询股票的价格数据，最低价，最高价，当前价格
import sqlite3

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from constants.common_constants import DB_PATH
from trade_data.get_stock_basic_list import get_stock_basic_list
from trade_data.get_trade_data import get_stock_trade_data

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

def cal_hist_price_of_stock(stock,latest_days=10000):
    # # pandas连接数据库
    # conn = sqlite3.connect(DB_PATH)
    # # 读取相应的交易数据表
    # table_name = 'S' + str(stock) + '_daily'
    # # 读取股票基本信息表
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_trade_data=get_stock_trade_data(stock)

    # print(stock_trade_data.head())
    # stock_trade_data['close'].plot.bar()
    # plt.show()
    stock_price = stock_trade_data['close'].values
    # print(len(stock_price))
    latest_days = latest_days if len(stock_price) > latest_days else len(stock_price)
    start_index = len(stock_price) - latest_days
    stock_price = stock_price[start_index:len(stock_price)]
    # print(len(stock_price))
    # print(stock_price)
    # for i in stock_price:
    #     print(i)
    max_price = max(stock_price)
    # print(max_price)
    min_price = min(stock_price)
    # print(min_price)
    current_price = stock_price[len(stock_price) - 1]
    # print(current_price)
    print([stock, max_price, min_price, current_price])
    return [stock, max_price, min_price, current_price]


def cal_hist_price_of_all_stocks():
    # # pandas连接数据库
    # conn = sqlite3.connect(DB_PATH)
    # # 读取股票基本信息表
    # stock_list_data = pd.read_sql('select * from stockList', conn)

    stock_list_data=get_stock_basic_list()
    print(stock_list_data.head())
    stock_list = stock_list_data['symbol'].values
    print(stock_list)
    # 遍历读取每一个股票的日交易数据，计算其最低价，最高价，上市日期等
    price_array = []
    for stock in stock_list:
        price = cal_hist_price_of_stock(stock)
        print(price)
        price_array.append(price)
    df = pd.DataFrame(price_array, columns=['code', 'max_price', 'min_price', 'current_price'])
    print(df.head())
    return df


def cal_hist_price_of_all_stocks2sql():
    # # pandas连接数据库
    # conn = sqlite3.connect(DB_PATH)
    # # 读取股票基本信息表
    # stock_list_data = pd.read_sql('select * from stockList', conn)

    stock_list_data = get_stock_basic_list()
    print(stock_list_data.head())
    stock_list = stock_list_data['symbol'].values
    print(stock_list)
    # 遍历读取每一个股票的日交易数据，计算其最低价，最高价，上市日期等
    price_array = []
    for stock in stock_list:
        price = cal_hist_price_of_all_stocks(stock)
        print(price)
        price_array.append(price)
    df = pd.DataFrame(price_array, columns=['code', 'max_price', 'min_price', 'current_price'])
    print(df.head())

    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    print("Open database successfully")
    df.to_sql('stockHistoryPrice', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# 计算股票当前价格在最低价到最高价的那个百分比位置
def cal_price_pct(stock,latestdays=3000):
    price = cal_hist_price_of_stock(stock,latestdays)
    # print(price)
    pct = (price[3] - price[2]) / (price[1] - price[2])
    return pct


# 计算股票当前价格对最高价格的回撤幅度
def cal_price_withdraw_pct(stock,latestdays=3000):
    price = cal_hist_price_of_stock(stock,latestdays)
    # print(price)
    pct = (price[1] - price[3]) / price[1]
    return pct


if __name__ == '__main__':
    cal_hist_price_of_stock('601398',3000)
    # cal_hist_price_of_all_stocks()
    # cal_hist_price_of_all_stocks2sql()

