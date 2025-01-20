from analysis_util.cal_stock_trend import cal_trend_common
from selected_stock_analysis.buy_point_detect import buy_point_detect
from trade_data.get_trade_data import get_stock_trade_data_latestdays

import pandas as pd
import numpy as np

if __name__ == '__main__':
    # 买点检测
    # for i in range(60):
    #     buy_point_detect(60-i)
    buy_point_detect()


    # # 效果追踪
    # # 获取买点csv文件中数据的日期，计算下一天的涨跌
    # df = pd.read_csv('上升通道回调.csv', dtype={'code': np.str_})
    # print(df.head())
    #
    # mm_l = []
    # for l in df.values[:]:
    #     code = l[0]
    #     name = l[1]
    #     desc = l[2]
    #     date = l[3]
    #     # 获取价格
    #     trade_df = get_stock_trade_data_latestdays(code, 100)
    #     trade_df = trade_df[trade_df.trade_date >= str(date)]
    #     print(trade_df)
    #     k1 = cal_trend_common(trade_df['close'].values[0:2])
    #     print('k1: ', k1)
    #     k2 = cal_trend_common(trade_df['close'].values)
    #     print('k2: ', k2)
    #
    #     if '5' in desc:
    #         mm_l.append([code, name, date,'m5',k1, k2])
    #     if '10' in desc:
    #         mm_l.append([code, name, date,'m10',k1, k2])
    #     if '20' in desc:
    #         mm_l.append([code, name, date,'m20',k1, k2])
    #     if '30' in desc:
    #         mm_l.append([code, name, date,'m30',k1, k2])
    #
    # df_effect=pd.DataFrame(mm_l,columns=['code','name','date','mean','k1','k2'])
    # print(df_effect)




