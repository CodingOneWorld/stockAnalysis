# -*- coding: utf-8 -*-

# 将股票进行分类，即自选股分板块，如上升通道，低价股等等

import pandas as pd
import numpy as np

# 获取短期上升通道股票，5
from analysis_util.cal_stock_trend import cal_stock_price_trend


def get_latest_rising_stocks():
    grad1 = 0.1
    grad2 = 0.2
    grad3 = 0.3
    # 获取自选股票池
    df = pd.read_csv('自选股.csv', dtype={'symbol': np.str})
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)
    # 趋势筛选，处于上升趋势
    # 超短线，最近3、5日处于上升趋势
    super_short_stocks = []
    # 短线，最近5、10日处于上升趋势
    short_stocks = []
    # 中线，最近10，30日处于上升趋势
    medium_stocks = []
    # 中长线，最近3个月，6个月处于上升通道
    medium_long_stocks = []
    # 长线
    long_stock = []
    for line in stock_list:
        print(line)
        s = line[0]
        k3 = cal_stock_price_trend(s, 3)
        k5 = cal_stock_price_trend(s, 5)
        k10 = cal_stock_price_trend(s, 10)
        k30 = cal_stock_price_trend(s, 30)
        k60 = cal_stock_price_trend(s, 60)
        # k90 = cal_stock_price_trend(s, 90)
        k120 = cal_stock_price_trend(s, 120)
        # k180 = cal_stock_price_trend(s, 180)
        # k300 = cal_stock_price_trend(s, 300)
        k3000 = cal_stock_price_trend(s, 4000)
        if k3 > grad2 and k5 > grad2:
            super_short_stocks.append(line)
        if k5 > grad2 and k10 > grad2:
            short_stocks.append(line)
        if k30 > grad2 and k10 > grad2:
            medium_stocks.append(line)
        if k60 > grad2 and k120 > grad2:
            medium_long_stocks.append(line)
        if k3000 > 0.1:
            long_stock.append(line)
    print("趋势股：")
    print("超短线上升通道：")
    super_short_stocks = pd.DataFrame(super_short_stocks, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('超短线上升通道.csv',index=0)
    print(super_short_stocks)
    print("短线上升通道：")
    short_stocks = pd.DataFrame(short_stocks, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('短线上升通道.csv',index=0)
    print(short_stocks)
    print("中线上升通道：")
    medium_stocks = pd.DataFrame(medium_stocks, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('中线上升通道.csv',index=0)
    print(medium_stocks)
    print("中长线上升通道：")
    medium_long_stocks = pd.DataFrame(medium_long_stocks, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('中长线上升通道.csv',index=0)
    print(medium_long_stocks)
    print("长线上升通道：")
    long_stock = pd.DataFrame(long_stock, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('长线上升通道.csv',index=0)
    print(long_stock)


get_latest_rising_stocks()
