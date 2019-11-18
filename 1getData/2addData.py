# -*- coding: utf-8 -*-

# 获取增量数据，并写入csv文件

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# path
filepath = 'D:/Money/stocks/'

pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# 查询当前所有正常上市交易的股票列表
stock_basic = pro.stock_basic(exchange='', list_status='L')
stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
print(stock_basic)
stocks = stock_basic['ts_code'].values
print(stocks)

# 获取股票的日线数据-前复权数据
ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# 基础积分每分钟内最多调取200次，每次4000条数据
# 加入计数和睡眠，计数为200，睡眠一段时间
count = 40
for i in range(len(stocks)):
    ts_code = stocks[i]
    print(i)
    count -= 1
    if count < 0:
        time.sleep(30)
        count = 40
    name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
    print(name)
    # 获取当前日期
    # yyyy/dd/mm格式
    start_date=time.strftime("%Y/%m/%d")
    print(start_date)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date)
    df2 = df.sort_index(ascending=False)
    # print(df2)
    df2.reset_index(drop=True, inplace=True)
    df2['name'] = [name] * len(df2)
    print(df2)
    # 写入本地
    filename = filepath + ts_code + ".csv"
    print(filename)
    if os.path.exists(filename):
        df2.to_csv(filename, mode='a', header=None)
    else:
        df2.to_csv(filename)
