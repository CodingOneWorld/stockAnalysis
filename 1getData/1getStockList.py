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
# 获取所有正常上市的
stocks = stock_basic['ts_code'].values
stocks=[x[0:7] for x in stocks]
print(stocks)

# 查询股票的基本信息数据-tushare
data = ts.get_stock_basics()
data=data.values


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
                       list_date   INT,
                       pe       DOUBLE,
                       pb  DOUBLE,
                       outstanding  DOUBLE,
                       totals       DOUBLE,
                       totalAssets  DOUBLE,
                       liquidAssets DOUBLE,
                       fixedAssets  DOUBLE,
                       reserved DOUBLE,
                       reservedPerShare DOUBLE,
                       esp   DOUBLE,
                       bvps    DOUBLE,
                       timeToMarket      TEXT,
                       undp  DOUBLE,
                       perundp     DOUBLE,
                       rev   DOUBLE,
                       profit    DOUBLE,
                       gpr   DOUBLE,
                       npr    DOUBLE,
                       holders INT)''')
conn.commit()
for i in range(len(stock_basic)):
    print("Table created successfully")
    c.execute(
        "INSERT INTO " + table_name +
        " (ts_code,symbol,code,name,area,industry,market,list_date,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
        esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
        ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',\
                                      '{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}')".format(
            stock_basic[i][0],data[i][0], data[i][1],
            data[i][2], data[i][3],
            data[i][4], data[i][5],
            data[i][6], data[i][7],
            data[i][8], data[i][9],
            data[i][10], data[i][11],
            data[i][12], data[i][13],
            data[i][14], data[i][15],
            data[i][16], data[i][17],
            data[i][18], data[i][19],
            data[i][20], data[i][21]))
    conn.commit()
