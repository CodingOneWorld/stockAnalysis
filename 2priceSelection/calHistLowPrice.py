
# -*- coding: utf-8 -*-

# 选取低价

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# 获取所有股票列表
pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# 查询当前所有正常上市交易的股票列表
stock_basic = pro.stock_basic(exchange='', list_status='L')
stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
print(stock_basic)
stocks = stock_basic['ts_code'].values
print(stocks)

# 获取所有股票的所有收盘价数据,并计算股价数据，最高价，最低价
# path
filepath = 'D:/Money/stocks/'
for ts_code in stocks:
    filename = filepath + ts_code + ".csv"
    data=pd.read_csv(filename)
    print(data.head())