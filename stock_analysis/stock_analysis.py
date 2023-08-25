# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts

from analysis_util.general_utils import get_stock_code
from analysis_util.plot_k_line import plot_k_line, plot_k_line_latestdays
from analysis_util.cal_stock_trend import cal_stock_price_trend, cal_trend_common, get_stock_price
from trade_data.get_trade_data import get_stock_trade_data

if __name__ == '__main__':
    # 给定一只股票，尝试分析

    s = get_stock_code('泛微网络')

    # k线图
    # plot_k_line_latestdays(s,400)

    d1='20220501'
    d2='20221011'

    # 上升通道持续时间
    df = get_stock_trade_data(s)
    df = df[df.trade_date >= d1][df.trade_date <= d2]
    print(len(df))

    k=cal_trend_common(df['close'].values)
    print(k)

    plot_k_line(s, d1, d2, mav=[5, 10, 20, 30, 40])










