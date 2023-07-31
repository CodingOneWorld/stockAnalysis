# -*- coding: utf-8 -*-

#个股要求
# 1：涨停板是60天内最高价，这个代表正在走主升浪或者有走主升浪的可能性，涨停代表强势。
# 2：涨停时间距离今天8天以内，代表关注度还可以。
# 3：涨停以来每天收盘价都大于5日均线，这个代表股票正在稳定角度上升。
# 4：涨停成交额大于7亿，资金容纳量大，稳定性高，一般不会极端开盘。
# 5：每个票只操作一次


from analysis_util.cal_stock_trend import get_stock_price
from trade_data.get_stock_basic_list import get_stock_basic_list
from trade_data.get_trade_data import get_stock_trade_data_latestdays
import pandas as pd

from util.date_util import date_diff

import warnings
warnings.filterwarnings("ignore")

def list_format(l):
    print(','.join(l))
    return ','.join(l)


def super_short_stock_select(stock_list):
    s_list = []

    for s in stock_list:
    # for s in [000625,000656,000750,002508,600030,600155,600266,600340,600369,601127,601162,601375,601555,601677]:
        # 获取股票交易数据
        trade_data = get_stock_trade_data_latestdays(s, 100)
        # 计算5日均线
        trade_data['m5'] = trade_data['close'].rolling(window=5).mean().fillna(0)
        trade_data = trade_data[-60:].reset_index(drop=True)
        # print(trade_data)
        # print(trade_data.index)
        # trade_data['latestdays']=[60]*60-trade_data.index
        # print(trade_data)
        trade_data['moreM5'] = trade_data['close'] - trade_data['m5']
        trade_data_8 = trade_data[-8:]
        print(trade_data_8)
        # 8天以内有涨停
        if len(trade_data_8[trade_data_8.pct_chg > 9]) > 0:
            # 涨停板是60天内最高价
            # 涨停板价格
            pct9_price = trade_data_8[trade_data_8.pct_chg > 9]['close'].values[0]
            print(pct9_price)
            # 计算涨停板前的最高价格
            pct9 = trade_data_8[trade_data_8.pct_chg > 9]['pct_chg'].values[0]
            la60_pct = list(trade_data['pct_chg'].values)
            # print(la60_pct)
            pct9_index = la60_pct.index(pct9)
            # print(pct9_index)
            trade_data_before_pct9 = trade_data[:pct9_index]
            # print(trade_data_before_pct9)
            max_price60 = max(trade_data_before_pct9['close'].values)
            # 计算最近60天的最高价格
            # max_price60 = max(trade_data['close'].values)
            print(max_price60)
            if pct9_price >= max_price60:
                la8_pct = list(trade_data_8['pct_chg'].values)
                pct9_index = la8_pct.index(pct9)
                print(pct9_index)
                # 涨停时的成交额大于7亿
                print(trade_data_8.iloc[pct9_index,].loc['amount'])
                if trade_data_8.iloc[pct9_index,].loc['amount'] / 100000 >= 7:
                    print('成交额大于7亿')
                    # 获取涨停后的数据
                    trade_data_after_pct9 = trade_data_8[pct9_index + 1:]
                    print(trade_data_after_pct9)
                    # 计算涨停后收盘价是否大于5日线
                    trade_data_after_pct9['moreM5_tag'] = trade_data_after_pct9['moreM5'].apply(
                        lambda x: 1 if x > 0 else 0)
                    if trade_data_after_pct9['moreM5_tag'].sum() >= len(trade_data_after_pct9):
                        print(s + '满足条件')
                        s_list.append(s)
    return s_list


if __name__ == '__main__':
    # 股票列表
    stock_basic=get_stock_basic_list('DB')
    # 不看最近一年上市的股票
    stock_basic = stock_basic[stock_basic['list_date'] <= '20220701']
    stock_list=stock_basic['symbol'].values
    print(stock_list)

    s_list=super_short_stock_select(stock_list)

    l = ['000625',
         '000656',
         '000750',
         '002508',
         '600030',
         '600155',
         '600266',
         '600340',
         '600369',
         '601127',
         '601162',
         '601375',
         '601555',
         '601677']

    list_format(l)





