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


def _linear_slope(y_arr) -> float:
    """对 y_arr 做线性回归，返回斜率（内部工具函数）。"""
    n = len(y_arr)
    x = np.arange(1, n + 1).reshape(-1, 1)
    y = np.array(y_arr, dtype=float).reshape(-1, 1)
    model = linear_model.LinearRegression()
    model.fit(x, y)
    return float(model.coef_[0][0])


def cal_stock_price_trend(stock_price, latest_days, is_image=0):
    """
    计算股价趋势斜率（归一化为收益率斜率，单位：收益率/天）。

    【改进说明】原版直接对价格绝对值做线性回归，斜率单位是"元/天"，
    不同价格股票无法横向比较（茅台斜率可达平安银行 100 倍）。
    现改为先将价格序列转为以首日为基准的**累计收益率序列**，
    再做线性回归，斜率含义变为"日均收益率"，可跨股票使用同一阈值。

    例：k=0.005 → 平均每天上涨约 0.5%
        k=-0.003 → 平均每天下跌约 0.3%

    建议阈值参考（替换原 0.2 系列阈值）：
        强上升通道：k > 0.005  （日均 +0.5%，20日约 +10%）
        弱上升通道：k > 0.002
        强下降通道：k < -0.005
        弱下降通道：k < -0.002
    """
    latest_days = min(latest_days, len(stock_price))
    start_index = len(stock_price) - latest_days
    y_price = np.array(stock_price[start_index:], dtype=float)

    # 归一化：转换为累计收益率（以区间首日收盘价为基准）
    base = y_price[0]
    if base == 0:
        return 0.0
    y_ret = (y_price - base) / base  # 单位：相对收益率

    x = np.arange(1, latest_days + 1).reshape(-1, 1)
    y = y_ret.reshape(-1, 1)
    model = linear_model.LinearRegression()
    model.fit(x, y)

    if is_image == 1:
        plt.plot(x, y_ret, 'k.')
        plt.plot(x, model.predict(x), 'g-')
        plt.ylabel('累计收益率')
        plt.show()

    return float(model.coef_[0][0])


def cal_trend_common(data):
    """
    对任意数值序列计算线性回归斜率（归一化为相对斜率，单位：/天）。

    【改进说明】同 cal_stock_price_trend，将序列转换为相对于首值的
    累计变化率后再做回归，结果可跨序列比较。
    用于净利润趋势、收入趋势等场景时，首值为第一年数据。
    """
    y_arr = np.array(data, dtype=float)
    if len(y_arr) == 0:
        return 0.0
    base = y_arr[0]
    if base == 0:
        # 首值为 0 时（如净利润为负转正），退化为绝对斜率（无法归一化）
        return _linear_slope(y_arr)
    y_norm = (y_arr - base) / abs(base)
    return _linear_slope(y_norm)


if __name__ == '__main__':
    # stock_price = get_stock_price('002271', 'close','DB')['close'].values[-300:]
    # print(','.join([str(i) for i in stock_price]))
    # cal_stock_price_trend(stock_price, 300)

    code=get_stock_code('西部矿业')
    his_price_df = get_stock_trade_data(code, '20221026','20230829')
    print(his_price_df.shape)
    his_price=his_price_df['close'].values[-100:]
    cal_trend_common(his_price)

