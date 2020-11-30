# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

import time
import os
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# ts token
ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# 查询最新的股票列表
# 查询当前所有正常上市交易的股票列表-是ts_pro与ts的股票列表的交集
# ts_pro
# stock_basic = pro.stock_basic(exchange='', list_status='L')
stock_basic = pro.query('stock_basic', exchange='', list_status='L')
# stock_basic = stock_basic[stock_basic['list_date'] < '20201129']
print(stock_basic)
stocks_tspro = stock_basic['ts_code'].values
print(stocks_tspro)

# # 查询数据库中已有的股票列表
# # 数据库连接
# filepath = 'E:/Money/stocks.db'
# conn = sqlite3.connect(filepath)
# print("Opened database successfully")
# c = conn.cursor()
# cursor = c.execute("SELECT ts_code,name from stock_basic_list")
# stocks_old = []
# for row in cursor:
#     stocks_old.append(row[0])
# stocks_old=set(stocks_old)
#
# print(stocks_old)
# print(len(stocks_old))
