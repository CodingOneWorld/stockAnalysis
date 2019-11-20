# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
# pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

#查询当前所有正常上市交易的股票列表
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# data = pro.stock_basic(exchange='', list_status='L')
# print(data)

# 获取历史日线数据，本接口是未复权行情
stockid='000001.SZ'
# df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
# df = pro.daily(ts_code='000001.SZ')
# print(df)

# 获取历史日线数据，包含前后复权数据
# 使用通用行情接口，pro_bar
df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20191116')
df2=df.sort_index(ascending=False)
df2.reset_index(drop=True, inplace=True)
#df2['open'].plot()
#plt.show()
df2.reset_index(drop=True, inplace=True)
print(df2)

data=df2.values
print(data)