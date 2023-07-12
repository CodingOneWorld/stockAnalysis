# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import tushare as ts

from analysis_util.plot_util import plot_price_line_latestdays
from constants.common_constants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_price_trend, get_stock_price

# f = open("自选股.sel", "r")
#
# stock_list = []
# for line in f:
#     line = line.split("")
#     for l in line:
#         l = l.split("\x07!")
#         # print(l)
#         for i in l:
#             i = i.split("\x07\x16")
#             # print(i)
#             for s in i:
#                 stock_list.append(s)
# print(stock_list)
#
# # 读取股票基本列表
# conn = sqlite3.connect(DB_PATH)
# # 读取股票基本信息表
# stock_list_data = pd.read_sql('select * from stockList', conn)
# print(stock_list_data.head())
#
# # 股票收入及利润
# # df1 = ts.get_profit_data(2021, 1).loc[:, ['code', 'name', 'business_income', 'net_profits']]
# # df1 = ts.get_profit_data(2021, 1)
# # print(df1)
#
# for s in stock_list:
#     # print(len(stock_list_data[stock_list_data["symbol"]==s].values))
#     k = cal_stock_price_trend(s, 10)
#     if k > 0:
#         print(s)


stock_price = get_stock_price('603129', 'close').values
# plot_price_line_latestdays('000001',300)
cal_stock_price_trend(stock_price,3000)

