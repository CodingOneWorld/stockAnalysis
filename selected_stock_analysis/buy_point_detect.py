# -*- coding: utf-8 -*-

'''
买入点检测
上升通道回调
下降通道到关键点位
'''

import pandas as pd
import numpy as np
import pandas as pd

from analysis_util.cal_stock_trend import cal_trend_common
from analysis_util.general_utils import get_stock_code
from analysis_util.plot_k_line import plot_k_line
from trade_data.get_trade_data import get_stock_trade_data

if __name__ == '__main__':
    # 给定一只股票
    s = get_stock_code('三一重工')
    # 检测上升通道
    d1 = '20240101'
    d2 = '20240416'
    # plot_k_line(s, '20240101', '20240417')

    df = get_stock_trade_data(s,d1, d2)
    print(df.head())

    s_close=df['close'].values

    k = cal_trend_common(df['close'].values)
    print(k)
    # 检测下降通道