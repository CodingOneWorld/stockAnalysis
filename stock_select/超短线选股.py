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

if __name__ == '__main__':
    # 股票列表
    stock_basic=get_stock_basic_list('DB')
    stock_list=stock_basic['symbol'].values
    print(stock_list)

    s_list=[]

    for s in stock_list[0:1]:
    # for s in ['000980']:
        # 获取股票交易数据
        trade_data=get_stock_trade_data_latestdays(s,100)
        # 计算5日均线
        trade_data['m5']=trade_data['close'].rolling(window=5).mean().fillna(0)
        trade_data=trade_data[-60:].reset_index(drop=True)
        trade_data['latestdays']=[60]*60-trade_data.index
        print(trade_data)
        trade_data['moreM5']=trade_data['close']-trade_data['m5']
        trade_data_8=trade_data[-8:]
        # 8天以内有涨停
        if len(trade_data_8[trade_data_8.pct_chg>9])>0:
            # 涨停板是60天内最高价
            pct9_price=trade_data_8[trade_data_8.pct_chg>9]['close'].values[0]
            print(pct9_price)
            la60_price = list(trade_data['close'].values)
            pct9_index = la60_price.index(pct9_price)
            trade_data_before_pct9 = trade_data[:pct9_index]
            max_price60=max(trade_data_before_pct9['close'].values)
            print(max_price60)
            if pct9_price>=max_price60:
                # 涨停以来每天收盘价都大于5日均线
                la8_price=list(trade_data_8['close'].values)
                pct9_index=la8_price.index(pct9_price)
                # 涨停时的成交额大于7亿
                if trade_data_8.iloc[pct9_index,].loc['amount']/100000>7:
                    print('成交额大于7亿')
                    # 获取涨停后的数据
                    trade_data_after_pct9 = trade_data_8[pct9_index + 1:]
                    print(trade_data_after_pct9)
                    # 计算涨停后收盘价是否大于5日线
                    trade_data_after_pct9['moreM5_tag'] = trade_data_after_pct9['moreM5'].apply(
                        lambda x: 1 if x > 0 else 0)
                    if trade_data_after_pct9['moreM5_tag'].sum() >= len(trade_data_after_pct9):
                        print(s+'满足条件')
                        s_list.append(s)

    for l in s_list:
        print(l)









        # 涨停时间距离今天8天以内
        # if len(trade_data[trade_data.pct_chg>9][trade_data.latestdays<8])>0:



