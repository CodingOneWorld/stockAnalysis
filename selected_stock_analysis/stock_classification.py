# -*- coding: utf-8 -*-

# 将股票进行分类，即自选股分板块，如上升通道，低价股等等

import os
import pathlib
import pandas as pd
import numpy as np

from analysis_util.cal_hist_price import cal_price_pct
from analysis_util.cal_stock_trend import cal_stock_price_trend, get_stock_price, cal_trend_common
from analysis_util.plot_k_line import plot_k_line

# 获取上升通道股票
# 以股价走势斜率判断上升通道

# 输出目录，自动创建（相对于当前工作目录）
path = './classification/'
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def get_up_trend_stocks(file):
    # 获取自选股票池
    df = pd.read_csv(file, dtype={'symbol': np.str_}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)
    # ── 归一化斜率阈值（单位：收益率/天）──────────────────────────
    # 斜率已归一化，可跨股票使用同一阈值：
    #   强上升通道 k > 0.005  （日均 +0.5%，20日约 +10%）
    #   弱上升通道 k > 0.002
    #   强下降通道 k < -0.005
    # 原版使用绝对价格斜率（0.1/0.2/0.3），已替换为归一化阈值
    grad_up_strong = 0.005   # 强上升信号（原 grad2=0.2）
    grad_up_weak   = 0.002   # 弱上升信号（原 grad1=0.1）
    grad_dn_weak   = -0.002  # 弱下降信号

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
        stock_price = get_stock_price(s, 'close').values
        k3   = cal_stock_price_trend(stock_price, 3)
        k5   = cal_stock_price_trend(stock_price, 5)
        k10  = cal_stock_price_trend(stock_price, 10)
        k30  = cal_stock_price_trend(stock_price, 30)
        k60  = cal_stock_price_trend(stock_price, 60)
        k90  = cal_stock_price_trend(stock_price, 90)
        k120 = cal_stock_price_trend(stock_price, 120)
        k3000 = cal_stock_price_trend(stock_price, 4000)

        # 上升趋势（使用归一化阈值）
        if k3 > grad_up_strong and k5 > grad_up_strong:
            super_short_stocks.append(line)
        if k5 > grad_up_strong and k10 > grad_up_strong:
            short_stocks.append(line)
        if k30 > grad_up_strong and k10 > grad_up_strong:
            medium_stocks.append(line)
        if k60 > grad_up_strong and k120 > grad_up_strong:
            medium_long_stocks.append(line)
        if k3000 > grad_up_weak:
            long_stock.append(line)

        # 反弹（中长期下降 + 短期上升）
        if k30 < grad_dn_weak and k5 > grad_up_weak:
            rebound_stocks_l.append(line)
        if k60 < grad_dn_weak and k10 > grad_up_weak:
            rebound_stocks_m.append(line)
        if k90 < grad_dn_weak and k30 > grad_up_weak:
            rebound_stocks_h.append(line)

    print("趋势股：")
    print("超短线上升通道：")
    super_short_stocks = pd.DataFrame(super_short_stocks, columns=['symbol', 'stock_name'])
    print(super_short_stocks)
    print("短线上升通道：")
    short_stocks = pd.DataFrame(short_stocks, columns=['symbol', 'stock_name'])
    print(short_stocks)
    print("中线上升通道：")
    medium_stocks = pd.DataFrame(medium_stocks, columns=['symbol', 'stock_name'])
    print(medium_stocks)
    print("中长线上升通道：")
    medium_long_stocks = pd.DataFrame(medium_long_stocks, columns=['symbol', 'stock_name'])
    print(medium_long_stocks)
    print("长线上升通道：")
    long_stock = pd.DataFrame(long_stock, columns=['symbol', 'stock_name'])
    print(long_stock)

    super_short_stocks.to_csv(path + '超短线上升通道' + file.split('.')[0] + '.csv', index=0)
    short_stocks.to_csv(path + '短线上升通道' + file.split('.')[0] + '.csv', index=0)
    medium_stocks.to_csv(path + '中线上升通道' + file.split('.')[0] + '.csv', index=0)
    medium_long_stocks.to_csv(path + '中长线上升通道' + file.split('.')[0] + '.csv', index=0)
    long_stock.to_csv(path + '长线上升通道' + file.split('.')[0] + '.csv', index=0)

    print("反弹股：")
    print("开始反弹：")
    rebound_stocks_l = pd.DataFrame(rebound_stocks_l, columns=['symbol', 'stock_name'])
    print(rebound_stocks_l)
    print("中期反弹：")
    rebound_stocks_m = pd.DataFrame(rebound_stocks_m, columns=['symbol', 'stock_name'])
    print(rebound_stocks_m)
    print("晚期反弹：")
    rebound_stocks_h = pd.DataFrame(rebound_stocks_h, columns=['symbol', 'stock_name'])
    print(rebound_stocks_h)

    rebound_stocks_l.to_csv(path + '开始反弹' + file.split('.')[0] + '.csv', index=0)
    rebound_stocks_m.to_csv(path + '中期反弹' + file.split('.')[0] + '.csv', index=0)
    rebound_stocks_h.to_csv(path + '晚期反弹' + file.split('.')[0] + '.csv', index=0)


# 获取低价股
def get_low_price_stocks(df, latestdays=3000):
    stock_list = df.values
    print(stock_list)
    cheap_stocks = []
    for line in stock_list:
        print(line)
        s = line[0]
        # 计算股票当前价格在最低价到最高价的那个百分比位置
        pct = cal_price_pct(s, latestdays)
        if pct < 0.5:
            cheap_stocks.append(line)
    cheap_stocks = pd.DataFrame(cheap_stocks, columns=['symbol', 'stock_name'])
    cheap_stocks.to_csv(path + '低价股.csv', index=0)


# 获取反弹股
if __name__ == '__main__':
    file = '自选股202308.csv'
    # file = 'stock_pool.txt'
    get_up_trend_stocks(file)

    # # 反弹
    # # 获取股票历史价格
    # s = '600660'
    # stock_price = get_stock_price(s, 'close')['close'].values
    # stock_price = stock_price[-200:]
    # print(stock_price)
    # l=[i for i in range(100)]
    # for i in list(reversed(l)):
    #     stock_price2=stock_price[:-i]
    #     length_s=len(stock_price2)
    #     cal_trend_common(stock_price2)
    #     k3 = cal_stock_price_trend(stock_price2, 3)
    #     k5 = cal_stock_price_trend(stock_price2, 5)
    #     k10 = cal_stock_price_trend(stock_price2, 10)
    #     k30 = cal_stock_price_trend(stock_price2, 30)
    #     if k30 < 0 and k5 > 0.1:
    #         print(s)
