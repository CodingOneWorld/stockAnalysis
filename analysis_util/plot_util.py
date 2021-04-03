# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from contants.commonContants import DB_PATH

# 绘制股票历史交易收盘价曲线
def plot_price_line(code,start_day,end_day):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S'+code+'_daily'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_trade_data.set_index("trade_date",inplace=True)
    print(stock_trade_data.head())
    stock_trade_data=stock_trade_data.loc[(stock_trade_data['trade_date']>start_day) & (stock_trade_data['trade_date']<end_day)]
    stock_trade_data.loc[:,'close'].plot.line()
    plt.show()


# 绘制
def plot_income_line(stock_name):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'income_since1989'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    stock_trade_data[stock_trade_data['name'] == stock_name].iloc[:, 3:stock_trade_data.shape[1]].T.plot.line()
    plt.show()


# 绘制
def plot_profit_line(stock_name):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'profit_since1989'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    stock_trade_data[stock_trade_data['name'] == stock_name].iloc[:, 3:stock_trade_data.shape[1]].T.plot.line()
    plt.show()

# plot_price_line('000001',20200101,20201231)
# plot_income_line("潍柴重机")
# plot_profit_line("潍柴重机")


