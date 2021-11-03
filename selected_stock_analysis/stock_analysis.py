# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts
from contants.common_contants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_price_trend,cal_trend_common
from stock_select.get_low_price_stock import cal_low_price_stock

if __name__ == '__main__':
    # 获取自选股列表
    fr = open('自选股.txt', 'r',encoding='utf-8')
    stock_list = []
    for line in fr:
        line = line.strip()
        line = line.split(',')
        stock_list.append(line)
    # stock_list = np.array(stock_list)
    print(stock_list[0])

    # 趋势筛选，处于上升趋势
    # # 超短线，最近3、5日处于上升趋势
    # super_short_stocks=[]
    # # 短线，最近5、10日处于上升趋势
    short_stocks=[]
    # # 中线，最近10，30日处于上升趋势
    # medium_stocks=[]
    # # 中长线，最近3个月，6个月处于上升通道
    # medium_long_stocks=[]
    # 长线
    print("长线")
    long_stock=[]
    for line in stock_list:
        s=line[0]
    #     k3 = cal_stock_price_trend(s, 3)
        k5 = cal_stock_price_trend(s, 5)
        k10 = cal_stock_price_trend(s, 10)
    #     k30 = cal_stock_price_trend(s, 30)
        # k60 = cal_stock_price_trend(s, 60)
    #     k120 = cal_stock_price_trend(s, 120)
    #     k300 = cal_stock_price_trend(s, 300)
    #     k3000 = cal_stock_price_trend(s, 4000)
    #     if k3 > 0.3 and k5>0.3:
    #         # print(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #         super_short_stocks.append(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
        if k5 > 0.3 and k10>0.3:
            # print(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
            # short_stocks.append(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
            short_stocks.append(line[1])
            print(line)
    #     if k30 > 0.3 and k10>0.3:
    #         # print(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #         medium_stocks.append(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #     if k60 > 0.3 and k120>0.3:
    #         # print(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #         medium_long_stocks.append(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #     if k3000>0.1:
    #         # print(stock_list_data[stock_list_data["symbol"] == s]['name'].values[0])
    #         long_stock.append(line[1])
    #         print(line)
    # print("趋势股：")
    # print("超短线：")
    # print(super_short_stocks)
    print("短线：")
    print(short_stocks)
    # print("中线：")
    # print(medium_stocks)
    # print("中长线：")
    # print(medium_long_stocks)
    # print("长线数：")
    # print(len(long_stock))



