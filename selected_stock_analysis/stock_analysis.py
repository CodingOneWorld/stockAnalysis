# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts

from analysis_util.plot_k_line import plot_k_line
from constants.common_constants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_price_trend, cal_trend_common, get_stock_price

if __name__ == '__main__':
    # plot_k_line('300760')
    # k=cal_stock_price_trend('000895', 3)
    # print(k)

    # 给定一只股票，尝试分析
    # 计算趋势
    stock_price = get_stock_price('000895', 'close')
    k=cal_stock_price_trend(stock_price, 50)
    print(k)




