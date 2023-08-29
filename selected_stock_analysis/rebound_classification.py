# -*- coding: utf-8 -*-
from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from analysis_util.output_document import output_doc
from selected_stock_analysis.up_classification import compare2mean
from trade_data.get_trade_data import get_stock_trade_data
from up_classification import compare2mean
from util.math_util import List_util
import pandas as pd
import numpy as np

import warnings

warnings.filterwarnings("ignore")


def analysis():
    # 斜率分析
    # 一个正常的下跌通道
    return 0


def get_stocklist(file):
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    stock_list = df.values
    return stock_list

def compare2exmin(his_price_df):
    # 获取股票历史价格
    his_price = his_price_df['close'].values
    print('极小值：')
    # 仅计算极小值有问题，需要加上最左边的值（防止最左边没有极小值，但股价很低）
    left = his_price[0]
    ex_mins = cal_extreme_min_value(his_price[-10:])[1]
    ex_mins = [left] + ex_mins
    if len(ex_mins) < 2:
        ex_mins = ex_mins + his_price[-1]
    print(ex_mins)
    is_true = List_util.isAZ(ex_mins)
    # is_true=True
    print(is_true)
    return is_true


# 短线（10d）反弹的股票
# 最近100天，最近20天 股价斜率小于0
# 最近10天 股价斜率大于0
# 最近10天 股价极低值一个比一个高
def get_l10_rebound_stock(file, path):
    stock_list = get_stocklist(file)
    selected_stock = []
    for s in stock_list:
        # for s in [['002107','沃华医药']]:
        print(s)
        code = s[0]
        # 股价
        # 获取股票历史价格
        his_price_df = get_stock_trade_data(code, '20220901', '20230817')
        his_price = his_price_df['close'].values
        # 斜率
        k5 = cal_stock_price_trend(his_price, 5)
        k10 = cal_stock_price_trend(his_price, 10)
        k20 = cal_stock_price_trend(his_price, 20)
        k100 = cal_stock_price_trend(his_price, 100)
        print('斜率：', k5, k10, k20, k100)
        # print(k20)
        # 确保反弹前的下降通道
        if k5 > 0 and k10 > 0 and k20 < -0.05 and k100 < 0:
            # 反弹，均在5日线上
            is_true = compare2mean(5, his_price_df)

            if is_true is True:
                print(s)
                selected_stock.append(s)

    if len(selected_stock) > 0:
        print(selected_stock)
        df = pd.DataFrame(selected_stock, columns=['code', 'name'])
        output_doc(df, path)


if __name__ == '__main__':
    # stock_list=['600660']
    # file = 'stock_pool2023.txt'
    file = '自选股.csv'

    file_name = file.split('.')[0]
    path = file_name + '_10日短线反弹股票.docx'

    get_l10_rebound_stock(file, path)
