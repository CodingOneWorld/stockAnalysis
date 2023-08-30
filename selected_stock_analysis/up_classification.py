# -*- coding: utf-8 -*-
from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from analysis_util.output_document import output_doc
from trade_data.get_trade_data import get_stock_trade_data
from util.math_util import List_util
import pandas as pd
import numpy as np


# 计算某短时间股价是否大于某一均线
def compare2mean(mav, his_price_df, latest_days):
    '''
    :param latest_days: 需要比较均线的时间跨度
    :param mav: 几日均线
    :param his_price_df: 股票历史交易数据
    :return: 股价在某一均线上返回True  否则False
    '''
    his_price_df['mean' + str(mav)] = his_price_df.close.rolling(window=mav).mean().fillna(0)
    his_price_df['dev'] = his_price_df['close'] - his_price_df['mean' + str(mav)]
    his_price_df['tag'] = his_price_df['dev'].apply(lambda x: 1 if x < 0 else 0)
    mav_dev_tag = his_price_df['tag'][-latest_days:].sum()

    if mav_dev_tag <= 0:
        return 1
    else:
        return 0


# 短线上升通道（10d）
# 最近10天 股价斜率大于0，k20<0,k100<0
# 最近10天 股价均高于10日均线
# 最近10天 股价极低值一个比一个高
def get_l10_up_stock(code):
    # 股价
    # 获取股票历史价格
    his_price_df = get_stock_price(code, 'close')[-200:]
    his_price = his_price_df['close'].values
    # 斜率
    k10 = cal_stock_price_trend(his_price, 10)
    k20 = cal_stock_price_trend(his_price, 20)
    k100 = cal_stock_price_trend(his_price, 100)
    # print(k20)
    if k10 > 0 and k20 < 0 and k100 < 0:
        # 均线
        if compare2mean(10, his_price_df, 10):
            # 极低值
            ex_mins = cal_extreme_min_value(his_price[-10:])[1]
            is_true = List_util.isAZ(ex_mins)
            # print(is_true)
            if is_true is True:
                return 1
    return 0


def get_l10_up_stock_all(stock_list, path):
    selected_stock = []
    for s in stock_list:
        code = s[0]
        # 股价
        # 获取股票历史价格
        his_price_df = get_stock_price(code, 'close')[-200:]
        his_price = his_price_df['close'].values
        # 斜率
        k10 = cal_stock_price_trend(his_price, 10)
        k20 = cal_stock_price_trend(his_price, 20)
        k100 = cal_stock_price_trend(his_price, 100)
        # print(k20)
        if k10 > 0 and k20 < 0 and k100 < 0:
            # 均线
            if compare2mean(10, his_price_df, 10):
                # 极低值
                ex_mins = cal_extreme_min_value(his_price[-10:])[1]
                is_true = List_util.isAZ(ex_mins)
                # print(is_true)
                if is_true is True:
                    print(s)
                    selected_stock.append(s)

    if len(selected_stock) > 0:
        df = pd.DataFrame(selected_stock, columns=['code', 'name'])
        # 将股票列表写入数据库
        output_doc(df, path)


# 中线上升通道
def get_l100_up_stock(code):
    # 最近100天的斜率大于0
    # 获取股票历史价格
    his_price_df = get_stock_price(code, 'close')[-200:]
    his_price = his_price_df['close'].values
    # 斜率
    k100 = cal_stock_price_trend(his_price, 100)
    k200 = cal_stock_price_trend(his_price, 100)
    print(k100,k200)
    # 均线比较
    # mean_tag = compare2mean(60, his_price_df, 200)
    mean_tag=1

    if k100 > 0 and k200 > 0 and mean_tag == 1:
        return 1
    return 0


if __name__ == '__main__':
    # stock_list = ['002918']
    file = 'stock_pool2023.txt'
    # file = '自选股.csv'

    file_name = file.split('.')[0]

    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    # print(stock_list)

    l10_up_stock = []
    l10_path = file_name + '_10日短线上升通道股票.docx'

    l100_up_stock = []
    l100_path = file_name + '_100日长线上升通道股票.docx'
    for s in stock_list:
        print(s)
        code = s[0]
        # # 10日短线上升通道
        # tagl10 = get_l10_up_stock(code)
        # if tagl10 == 1:
        #     l10_up_stock.append(s)

        # l100,l200上升通道
        tagl100 = get_l100_up_stock(code)
        if tagl100 == 1:
            l100_up_stock.append(s)

    if len(l10_up_stock) > 0:
        df = pd.DataFrame(l10_up_stock, columns=['code', 'name'])
        # 将股票列表写入数据库
        output_doc(df, l10_path)

    if len(l100_up_stock) > 0:
        df = pd.DataFrame(l100_up_stock, columns=['code', 'name'])
        # 将股票列表写入数据库
        output_doc(df, l100_path)
