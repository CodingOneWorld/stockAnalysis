# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts

from analysis_util.general_utils import get_stock_code
from analysis_util.plot_k_line import plot_k_line, plot_k_line_latestdays
from analysis_util.cal_stock_trend import cal_stock_price_trend, cal_trend_common, get_stock_price

if __name__ == '__main__':
    # 给定一只股票，尝试分析

    s = get_stock_code('云赛智联')
    # 计算趋势
    stock_price = get_stock_price(s, 'close')['close'].values
    k=cal_stock_price_trend(stock_price, 3000)
    print(k)

    # k线图
    # plot_k_line_latestdays(s,200)
    plot_k_line(s,'20220801','20230601')





