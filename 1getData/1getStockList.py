# -*- coding: utf-8 -*-

# 获取所有正常上市的股票列表

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# 查询当前所有正常上市交易的股票列表
stock_basic = pro.stock_basic(exchange='', list_status='L')
# stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
print(stock_basic)
stock_basic = stock_basic.values
# print(stock_basic)


# 连接sqlite数据库
conn = sqlite3.connect('P:/Money/stocks.db')
print("Opened database successfully")

c = conn.cursor()
table_name = 'stock_basic_list'
c.execute('''CREATE TABLE ''' + table_name + '''
                       (ts_code  TEXT PRIMARY KEY NOT NULL,
                       symbol     TEXT,
                       name     TEXT,
                       area        TEXT,
                       industry     TEXT,
                       market   TEXT,
                       list_date   INT)''')
conn.commit()
for i in range(len(stock_basic)):
    print("Table created successfully")
    c.execute(
        "INSERT INTO " + table_name +
        " (ts_code,symbol,name,area,industry,market,list_date) VALUES \
        ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(
            stock_basic[i][0], stock_basic[i][0], stock_basic[i][1],
            stock_basic[i][2], stock_basic[i][3],
            stock_basic[i][4], stock_basic[i][5],
            stock_basic[i][6]))
    conn.commit()
