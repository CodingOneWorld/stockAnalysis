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
from analysis_util.output_document import output_doc
from analysis_util.plot_k_line import plot_k_line, plot_k_line_df
from selected_stock_analysis.key_price_compare import mav_compare_df
from selected_stock_analysis.up_classification import is_up_stock, compare2mean_window
from trade_data.get_trade_data import get_stock_trade_data

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    # 遍历股票，检测买点，输出到doc
    # 获取自选股票池
    file='自选股202308.csv'
    df = pd.read_csv(file, dtype={'symbol': np.str_}, delimiter=',')
    stock_list = df.values
    print(stock_list)

    up_trend_correction_ls=[]       # 上升通道回调
    down_trend_key_mav_ls=[]        # 下降通道关键均线
    down_trend_pre_lowest_ls=[]     # 下降通道前低
    for line in stock_list:
        print(line)
        s = line[0]
        # 获取交易数据
        df = get_stock_trade_data(s)[-300:]

        # 上升通道回调
        # 检测均线 10 20 30
        tag32 = compare2mean_window(32, df, 10)
        print('tag32:',tag32)

        if tag32>0:
            # 检测买点
            # m5 m10 m20 m30
            mean_near_list=[]
            for mav in [5,10,20,30]:
                mean_tag = mav_compare_df(df, mav)
                if mean_tag==1:
                    mean_near_list.append(mav)
            if len(mean_near_list)>0:
                res = '接近均线%s' % (','.join([str(i) for i in mean_near_list]))
                print(res)
                up_trend_correction_ls.append([line[0],line[1],res])
                print(up_trend_correction_ls)
        # plot_k_line_df(df)


        # 下降通道到关键点位（前低、60，140日均线）
        # 计算最近n天斜率，斜率<0
        k5 = cal_trend_common(df['close'][-5:])
        k20 = cal_trend_common(df['close'][-20:])
        print('k:', k5,k20)
        if k5 < 0 and k20<0:
            # 计算极低点，比较
            data = df['low'].values
            y = cal_extreme_min_value(data)
            y2 = cal_extreme_min_value(y[1])
            exm_min_list = y2[1]
            pre_lowest_ls=[]
            for tag in exm_min_list:
                cur_price=df['low'].values[-1]
                if tag * 0.99 <= cur_price <= tag * 1.01:
                    pre_lowest_ls.append(tag)
            if len(pre_lowest_ls)>0:
                res = '接近前低%s' % (','.join([str(i) for i in pre_lowest_ls]))
                print(res)
                down_trend_pre_lowest_ls.append([line[0], line[1], res])
                print(down_trend_pre_lowest_ls)

            # 计算60，140均线，比较
            key_mav_ls=[]
            for mav in [60,140]:
                mean_tag = mav_compare_df(df, mav)
                if mean_tag==1:
                    key_mav_ls.append(mav)
            if len(key_mav_ls)>0:
                res = '接近均线%s' % (','.join([str(i) for i in key_mav_ls]))
                print(res)
                down_trend_key_mav_ls.append([line[0], line[1], res])
                print(down_trend_key_mav_ls)

    # 保存文档
    path = '上升通道回调.docx'
    df = pd.DataFrame(up_trend_correction_ls, columns=['code', 'name', 'desc'])
    output_doc(df, path)

    path = '下降通道到前低.docx'
    df = pd.DataFrame(down_trend_pre_lowest_ls, columns=['code', 'name', 'desc'])
    output_doc(df, path)

    path = '下降通道到关键均线.docx'
    df = pd.DataFrame(down_trend_key_mav_ls, columns=['code', 'name', 'desc'])
    output_doc(df, path)






