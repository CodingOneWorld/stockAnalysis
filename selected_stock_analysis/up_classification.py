# -*- coding: utf-8 -*-
from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from selected_stock_analysis.main import output_doc
from util.math_util import List_util
import pandas as pd
import numpy as np

# 中线（20d）上升通道的股票
# 最近20天 股价斜率大于0
# 最近20天 股价均高于20日均线
# 最近20天 股价极低值一个比一个高

# 短线（10d）反弹股票
# 最近100天，最近20天 股价斜率小于0
# 最近10天 股价斜率大于0
# 最近10天 股价均高于20日均线
# 最近10天 股价极低值一个比一个高


if __name__ == '__main__':
    # stock_list=['600660']
    file = 'stock_pool2023.txt'
    # file = '自选股.csv'
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)

    selected_stock = []
    for s in stock_list:
        code = s[0]
        # 股价
        # 获取股票历史价格
        his_price_df = get_stock_price(code, 'close')[-200:]
        his_price = his_price_df['close'].values
        # 斜率
        k10 = cal_stock_price_trend(his_price, 20)
        k20 = cal_stock_price_trend(his_price, 20)
        k100 = cal_stock_price_trend(his_price, 100)
        # print(k20)
        if k10 > 0 and k20<0 and k100<0:
            # 均线
            his_price_df['mean_20'] = his_price_df.close.rolling(window=20).mean().fillna(0)
            his_price_df['dev'] = his_price_df['close'] - his_price_df['mean_20']
            his_price_df['tag'] = his_price_df['dev'].apply(lambda x: 1 if x < 0 else 0)
            mean_10_dev_tag = his_price_df['tag'][-10:].sum()
            # print(mean_20_dev_tag)
            if mean_10_dev_tag <= 0:
                # 极低值
                ex_mins = cal_extreme_min_value(his_price[-10:])[1]
                is_true = List_util.isAZ(ex_mins)
                # print(is_true)
                if is_true is True:
                    print(s)
                    selected_stock.append(s)

    if len(selected_stock)>0:
        df = pd.DataFrame(selected_stock, columns=['code', 'name'])
        output_doc(df, '股票池_10日短线反弹股票.docx')