# -*- coding: utf-8 -*-

'''
买入点检测
上升通道回调
下降通道到关键点位
'''

import pandas as pd
import numpy as np
import pandas as pd

from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import cal_trend_common
from analysis_util.general_utils import get_stock_code
from analysis_util.plot_k_line import plot_k_line, plot_k_line_df
from selected_stock_analysis.key_price_compare import mav_compare_df
from selected_stock_analysis.up_classification import is_up_stock, compare2mean_window
from trade_data.get_trade_data import get_stock_trade_data

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    # 给定一只股票
    s = get_stock_code('三一重工')
    # 测试数据
    d1 = '20230601'
    d2 = '20240416'
    # plot_k_line(s, '20240101', '20240417')

    df = get_stock_trade_data(s,d1, d2)
    # print(df.head())

    # 检测上升通道
    # 斜率，32日均线上为上升通达，检测接近均线
    # for i in range(205,212):
    #     df2=df[0:i]
    #     # 检测斜率 最近10天的斜率>0
    #     k=cal_trend_common(df2['close'][-10:])
    #     print('k:',k)
    #     # 检测均线 10 20 30
    #     tag32 = compare2mean_window(32, df2[-200:], 10)
    #     print('tag30:',tag32)
    #
    #     if tag32>0:
    #         # 检测买点
    #         # m5 m10 m20 m30
    #         mean_near_list=[]
    #         for mav in [5,10,20,30]:
    #             mean_tag = mav_compare_df(df2, mav)
    #             if mean_tag==1:
    #                 mean_near_list.append(mav)
    #         if len(mean_near_list)>0:
    #             print(mean_near_list)
    #     plot_k_line_df(df2)

    # 检测前低
    # 检测前低，与当前价格比较   检测前100天的极低点
    data=df['low'].values[0:200]
    y = cal_extreme_min_value(data)
    y2 = cal_extreme_min_value(y[1])
    print(y2)





