# -*- coding: utf-8 -*-

# 读取自选股文件
import sqlite3
import pandas as pd
import numpy as np
import tushare as ts
from contants.commonContants import DB_PATH
from analysis_util.cal_stock_trend import cal_stock_trend

fr=open('自选股.txt','r')
stock_list=[]
for line in fr:
    line=line.strip()
    line=line.split(',')
    stock_list.append(line)
stock_list=np.array(stock_list)
stock_list=stock_list[:,1]
print(stock_list)

# 读取股票基本列表
conn = sqlite3.connect(DB_PATH)
# 读取股票基本信息表
stock_list_data = pd.read_sql('select * from stockList', conn)
print(stock_list_data.head())

# 股票收入及利润
# df1 = ts.get_profit_data(2021, 1).loc[:, ['code', 'name', 'business_income', 'net_profits']]
# df1 = ts.get_profit_data(2021, 1)
# print(df1)

for s in stock_list:
    # print(len(stock_list_data[stock_list_data["symbol"]==s].values))
    k = cal_stock_trend(s, 10)
    if k > 0:
        print(s)
