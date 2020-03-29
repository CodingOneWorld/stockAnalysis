# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

import time
import os
import sqlite3
from settings import conSqlite

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

# 数据库连接
conn = conSqlite('P:/Money/stocks.db')
print("Opened database successfully")
c = conn.cursor()

# 查询最新的股票列表
# 查询当前所有正常上市交易的股票列表-是ts_pro与ts的股票列表的交集
# ts_pro
stock_basic = pro.stock_basic(exchange='', list_status='L')
stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
# print(stock_basic)
stocks_tspro = stock_basic['ts_code'].values
print(stocks_tspro)

# ts
data = ts.get_stock_basics()
stocks_ts = set([])
for s in set(data.index):
    if s.startswith('0') or s.startswith('3'):
        stocks_ts.add(s + ".SZ")
    else:
        stocks_ts.add(s + ".SH")
# stocks_now = sorted(list(set(stocks_tspro).intersection(stocks_ts)))
stocks_now = set(stocks_tspro).intersection(stocks_ts)

print(stocks_now)
print(len(stocks_now))

# 查询数据库中已有的股票列表
cursor = c.execute("SELECT ts_code,name from stock_basic_list")
stocks_old = []
for row in cursor:
    stocks_old.append(row[0])
stocks_old=set(stocks_old)

print(stocks_old)
print(len(stocks_old))

stocks_inner=stocks_now.intersection(stocks_old)
print(len(stocks_inner))