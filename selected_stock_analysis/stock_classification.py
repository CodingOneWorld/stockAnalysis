# -*- coding: utf-8 -*-

# 将股票进行分类，即自选股分板块，如上升通道，低价股等等

import pandas as pd
import numpy as np

from analysis_util.cal_hist_price import cal_price_pct
from analysis_util.cal_stock_trend import cal_stock_price_trend, get_stock_price

# 获取上升通道股票
from analysis_util.plot_k_line import plot_k_line


def get_up_trend_stocks(file):
    # 获取自选股票池
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)
    grad1 = 0.1
    grad2 = 0.2
    grad3 = 0.3

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

    # 反弹股
    # 刚开始反弹
    rebound_stocks_l = []
    # 中期反弹
    rebound_stocks_m = []
    # 晚期反弹
    rebound_stocks_h = []

    for line in stock_list:
        print(line)
        s = line[0]
        # 获取股票历史价格
        stock_price = get_stock_price(s, 'close')
        k3 = cal_stock_price_trend(stock_price, 3)
        k5 = cal_stock_price_trend(stock_price, 5)
        k10 = cal_stock_price_trend(stock_price, 10)
        k30 = cal_stock_price_trend(stock_price, 30)
        k60 = cal_stock_price_trend(stock_price, 60)
        k90 = cal_stock_price_trend(stock_price, 90)
        k120 = cal_stock_price_trend(stock_price, 120)
        # k180 = cal_stock_price_trend(s, 180)
        # k300 = cal_stock_price_trend(s, 300)
        k3000 = cal_stock_price_trend(stock_price, 4000)

        # 上升趋势
        if k3 > grad2 and k5 > grad2:
            super_short_stocks.append(line)
        if k5 > grad2 and k10 > grad2:
            short_stocks.append(line)
        if k30 > grad2 and k10 > grad2:
            medium_stocks.append(line)
        if k60 > grad2 and k120 > grad2:
            medium_long_stocks.append(line)
        if k3000 > grad1:
            long_stock.append(line)

        # 反弹
        if k30 < 0 and k5 > grad1:
            rebound_stocks_l.append(line)
        if k60 < 0 and k10 > grad1:
            rebound_stocks_m.append(line)
        if k90 < 0 and k30 > grad1:
            rebound_stocks_h.append(line)
    print("趋势股：")
    print("超短线上升通道：")
    super_short_stocks = pd.DataFrame(super_short_stocks, columns=['symbol', 'stock_name'])
    super_short_stocks.to_csv('超短线上升通道' + file.split('.')[0] + '.csv', index=0)
    print(super_short_stocks)
    print("短线上升通道：")
    short_stocks = pd.DataFrame(short_stocks, columns=['symbol', 'stock_name'])
    short_stocks.to_csv('短线上升通道' + file.split('.')[0] + '.csv', index=0)
    print(short_stocks)
    print("中线上升通道：")
    medium_stocks = pd.DataFrame(medium_stocks, columns=['symbol', 'stock_name'])
    medium_stocks.to_csv('中线上升通道' + file.split('.')[0] + '.csv', index=0)
    print(medium_stocks)
    print("中长线上升通道：")
    medium_long_stocks = pd.DataFrame(medium_long_stocks, columns=['symbol', 'stock_name'])
    medium_long_stocks.to_csv('中长线上升通道' + file.split('.')[0] + '.csv', index=0)
    print(medium_long_stocks)
    print("长线上升通道：")
    long_stock = pd.DataFrame(long_stock, columns=['symbol', 'stock_name'])
    long_stock.to_csv('长线上升通道' + file.split('.')[0] + '.csv', index=0)
    print(long_stock)

    print("反弹股：")
    print("开始反弹：")
    rebound_stocks_l = pd.DataFrame(rebound_stocks_l, columns=['symbol', 'stock_name'])
    rebound_stocks_l.to_csv('开始反弹' + file.split('.')[0] + '.csv', index=0)
    print(rebound_stocks_l)
    print("中期反弹：")
    rebound_stocks_m = pd.DataFrame(rebound_stocks_m, columns=['symbol', 'stock_name'])
    rebound_stocks_m.to_csv('中期反弹' + file.split('.')[0] + '.csv', index=0)
    print(rebound_stocks_m)
    print("晚期反弹：")
    rebound_stocks_h = pd.DataFrame(rebound_stocks_h, columns=['symbol', 'stock_name'])
    rebound_stocks_h.to_csv('晚期反弹' + file.split('.')[0] + '.csv', index=0)
    print(rebound_stocks_h)


# 获取低价股
def get_low_price_stocks(df,latestdays=3000):
    stock_list = df.values
    print(stock_list)
    cheap_stocks=[]
    for line in stock_list:
        print(line)
        s = line[0]
        # 计算股票当前价格在最低价到最高价的那个百分比位置
        pct=cal_price_pct(s,latestdays)
        if pct<0.5:
            cheap_stocks.append(line)
    cheap_stocks = pd.DataFrame(cheap_stocks, columns=['symbol', 'stock_name'])
    cheap_stocks.to_csv('低价股.csv', index=0)


# 获取反弹股
if __name__ == '__main__':
    # file = '自选股.csv'
    # file = 'stock_pool.txt'
    # get_up_trend_stocks(file)

    line= ['002600','领益智造']
    stock_price = get_stock_price(line[0], 'close')
    k60 = cal_stock_price_trend(stock_price, 60)
    k120 = cal_stock_price_trend(stock_price, 120)
    plot_k_line(line[0],500)
    print(k60)
    print(k120)