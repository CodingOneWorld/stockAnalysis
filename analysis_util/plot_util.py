# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model  # 表示，可以调用sklearn中的linear_model模块进行线性回归。

from analysis_util.cal_stock_trend import get_stock_price
from analysis_util.general_utils import get_stock_name
from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()


# 绘制股票历史交易收盘价曲线
# 起止日，到终止日
def plot_price_line(code, start_date, end_date):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(lambda x: str(x))
    stock_trade_data = stock_trade_data.loc[
        (stock_trade_data['trade_date'] > start_date) & (stock_trade_data['trade_date'] < end_date)]
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data.loc[:, 'close'].plot.line()
    # stock_trade_data.plot.line(x='trade_date',y='close')
    plt.show()


# 绘制股票历史交易收盘价曲线
# 最近n天数据
def plot_price_line_latestdays(code, latest_days=5000):
    # 获取股票历史价格
    stock_price_df = get_stock_price(code, 'close')
    stock_price_df = stock_price_df.iloc[-latest_days:, :]
    # print(stock_price_df)
    stock_price_df.plot.line()

    plt.show()

    # # 构建线性回归样本，计算斜率
    # latest_days=latest_days if len(stock_price)>latest_days else len(stock_price)
    # x=[i for i in range(1,latest_days+1)]
    # start_index=len(stock_price)-latest_days if (len(stock_price)-latest_days)>0 else 0
    # y=stock_price[start_index:len(stock_price)]
    # print(','.join([str(x) for x in y]))
    # x=np.array(x).reshape(-1,1)
    # y=np.array(y).reshape(-1,1)
    #
    # model = linear_model.LinearRegression()
    # model.fit(x, y)
    # # print(model.intercept_)  # 截距
    # # print(model.coef_[0][0])  # 线性模型的系数
    # y2 = model.predict(x)
    #
    # # 绘制散点图与拟合直线图
    # plt.plot(, y, 'k.')
    # plt.plot(x, y2, 'g-')
    # plt.show()


# 绘制收入曲线
# 参数是股票代码
def plot_income_line(code, latest_year):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'income_all_stocks'
    stock_income_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_income_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    # stock_income_data[stock_income_data['name'] == stock_name].iloc[:, 3:stock_income_data.shape[1]].T.plot.line()
    stock_income_data[stock_income_data['code'] == code].iloc[:, -latest_year:].T.plot.line()
    plt.show()


# 绘制净利润曲线
# 参数是股票代码
def plot_profit_line(code, latest_year):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'profit_all_stocks'
    # 读取股票基本信息表
    stock_profit_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_profit_data.head())
    # stock_profit_data=stock_profit_data[stock_profit_data['trade_date']>20191215]
    # stock_profit_data[stock_profit_data['code'] == stock_code].iloc[:, 3:stock_profit_data.shape[1]].T.plot.line()
    stock_profit_data[stock_profit_data['code'] == code].iloc[:, -latest_year:].T.plot.line()
    plt.show()


if __name__ == '__main__':
    # plot_price_line('688676', '20210401', '20210414')
    # plot_stock_price_line('002486',5000)
    plot_price_line_latestdays('002271', 100)
    # print(get_stock_name('000756'))
    # plot_stock_price_line('002594',100)
    # plot_income_line("000100",5)
    # plot_profit_line("000100",5)
