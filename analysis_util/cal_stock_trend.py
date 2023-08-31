# -*- coding: utf-8 -*-

import sqlite3

import pandas as pd
from sklearn import linear_model  # 表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np
import matplotlib.pyplot as plt

from analysis_util.general_utils import get_stock_code
from trade_data.get_trade_data import get_stock_trade_data

from util.utils_common import get_dbpath_by_repo
DB_PATH=get_dbpath_by_repo()


# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


# 获取某只股票的所有历史股价
# type取值 close，high,low，控制取最低价，还是最高价还是收盘价
def get_stock_price(code, type, mode='DB'):
    # 获取交易数据
    if mode == 'online':
        stock_trade_data = get_stock_trade_data(code)
    else:
        # pandas连接数据库
        conn = sqlite3.connect(DB_PATH)
        # 读取相应的交易数据表
        table_name = 'S' + str(code) + '_daily'
        stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_price = stock_trade_data[['trade_date', type]]
    stock_price.set_index('trade_date', inplace=True)
    # print(stock_price)
    return stock_price


def cal_stock_price_trend(stock_price, latest_days):
    # 构建线性回归样本，计算斜率
    latest_days = latest_days if len(stock_price) > latest_days else len(stock_price)
    x = [i for i in range(1, latest_days + 1)]
    start_index = len(stock_price) - latest_days if (len(stock_price) - latest_days) > 0 else 0
    y = stock_price[start_index:len(stock_price)]
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    # print(x)
    # print(y)

    model = linear_model.LinearRegression()
    model.fit(x, y)
    # print(model.intercept_)  # 截距
    # print(model.coef_[0][0])  # 线性模型的系数
    y2 = model.predict(x)

    # 绘制散点图与拟合直线图
    # plt.plot(x, y, 'k.')
    # plt.plot(x, y2, 'g-')
    # plt.show()
    # print(model.coef_[0][0])
    return model.coef_[0][0]


def cal_trend_common(data):
    x = [i for i in range(1, len(data) + 1)]
    y = data
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)

    model = linear_model.LinearRegression()
    model.fit(x, y)
    # print(model.intercept_)  # 截距
    # print(model.coef_[0][0])  # 线性模型的系数
    y2 = model.predict(x)

    # 绘制散点图与拟合直线图
    # plt.plot(x, y, 'k.')
    # plt.plot(x, y2, 'g-')
    # plt.show()
    # print(model.coef_[0][0])
    return model.coef_[0][0]


if __name__ == '__main__':
    # stock_price = get_stock_price('002271', 'close','DB')['close'].values[-300:]
    # print(','.join([str(i) for i in stock_price]))
    # cal_stock_price_trend(stock_price, 300)

    code=get_stock_code('西部矿业')
    his_price_df = get_stock_trade_data(code, '20221026','20230829')
    print(his_price_df.shape)
    his_price=his_price_df['close'].values[-100:]
    cal_trend_common(his_price)

