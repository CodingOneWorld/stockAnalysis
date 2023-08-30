# -*- coding: utf-8 -*-
from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from analysis_util.output_document import output_doc
from trade_data.get_trade_data import get_stock_trade_data
from util.math_util import List_util
import pandas as pd
import numpy as np
import math

# 中线（20d）上升通道的股票
# 最近20天 股价斜率大于0
# 最近20天 股价均高于20日均线
# 最近20天 股价极低值一个比一个高


# 计算某短时间股价是否大于某一均线
def compare2mean(mav,his_price_df,latest_days):
    '''
    :param mav: 几日均线
    :param his_price_df: 股票历史交易数据
    :return: 股价在某一均线上返回True  否则False
    '''
    his_price_df['mean'+str(mav)] = his_price_df.close.rolling(window=mav).mean().fillna(0)
    his_price_df['dev'] = his_price_df['close'] - his_price_df['mean'+str(mav)]
    his_price_df['tag'] = his_price_df['dev'].apply(lambda x: 1 if x < 0 else 0)
    mav_dev_tag = his_price_df['tag'][-latest_days:].sum()

    # 允许latest_days中，有十分之一天的股价低于均线
    if mav_dev_tag <=math.ceil(latest_days*0.1):
        return True
    else:
        return False


if __name__ == '__main__':
    stock_list=['002918']
    # file = 'stock_pool2023.txt'
    # file = '自选股.csv'

    # file_name = file.split('.')[0]
    # path = file_name + '_10日短线上升通道股票.docx'

    # get_l10_up_stock(file,path)

    for code in stock_list:
        # 获取股票历史价格
        his_price_df = get_stock_trade_data(code,'20220901','20230531')
        his_price = his_price_df['close'].values
