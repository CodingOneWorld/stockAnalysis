# -*- coding: utf-8 -*-

import sqlite3

import pandas as pd
from sklearn import linear_model  # 表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np
import matplotlib.pyplot as plt

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from contants.commonContants import DB_PATH

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


def cal_stock_trend(stock,latest_days):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + str(stock) + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_price = stock_trade_data['close'].values
    # 构建线性回归样本，计算斜率
    latest_days=latest_days if len(stock_price)>latest_days else len(stock_price)
    x=[i for i in range(1,latest_days+1)]
    start_index=len(stock_price)-latest_days if (len(stock_price)-latest_days)>0 else 0
    y=stock_price[start_index:len(stock_price)]
    x=np.array(x).reshape(-1,1)
    y=np.array(y).reshape(-1,1)

    model = linear_model.LinearRegression()
    model.fit(x, y)
    print(model.intercept_)  # 截距
    print(model.coef_[0][0])  # 线性模型的系数
    y2 = model.predict(x)

    # 绘制散点图与拟合直线图
    # plt.plot(x, y, 'k.')
    # plt.plot(x, y2, 'g-')
    # plt.show()
    return model.coef_[0][0]



cal_stock_trend('000001',5000)