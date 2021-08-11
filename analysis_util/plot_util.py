# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from contants.common_contants import DB_PATH


# 绘制股票历史交易收盘价曲线
def plot_price_line(code, start_day, end_day):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(lambda x: str(x))
    stock_trade_data = stock_trade_data.loc[
        (stock_trade_data['trade_date'] > start_day) & (stock_trade_data['trade_date'] < end_day)]
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data.loc[:, 'close'].plot.line()
    plt.show()


# 绘制收入曲线
# 参数是股票代码
def plot_income_line(stock_code,latest_year):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'income_all_stocks'
    stock_income_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_income_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    # stock_income_data[stock_income_data['name'] == stock_name].iloc[:, 3:stock_income_data.shape[1]].T.plot.line()
    stock_income_data[stock_income_data['code'] == stock_code].iloc[:, -latest_year:].T.plot.line()
    plt.show()


# 绘制净利润曲线
# 参数是股票代码
def plot_profit_line(stock_code,latest_year):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'profit_all_stocks'
    # 读取股票基本信息表
    stock_profit_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_profit_data.head())
    # stock_profit_data=stock_profit_data[stock_profit_data['trade_date']>20191215]
    # stock_profit_data[stock_profit_data['code'] == stock_code].iloc[:, 3:stock_profit_data.shape[1]].T.plot.line()
    stock_profit_data[stock_profit_data['code'] == stock_code].iloc[:, -latest_year:].T.plot.line()
    plt.show()


if __name__ == '__main__':
    # plot_price_line('688676', '20210401', '20210414')
    plot_income_line("000100",5)
    plot_profit_line("000100",5)

