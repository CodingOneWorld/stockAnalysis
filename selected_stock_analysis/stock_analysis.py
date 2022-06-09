# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts

from analysis_util.plot_k_line import plot_k_line
from contants.common_contants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_price_trend,cal_trend_common

if __name__ == '__main__':
    plot_k_line('300760')
    k=cal_stock_price_trend('000895', 3)
    print(k)



