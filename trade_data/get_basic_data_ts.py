# -*- coding: utf-8 -*-

# 获取股票的基础数据，按天来存储
# 只输出正常上市的股票

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from contants.common_contants import DB_PATH

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

data = ts.get_stock_basics()
# print(data)

# 连接sqlite数据库
conn = sqlite3.connect(DB_PATH)
print("Opened database successfully")

# 创建表
table_name = 'stocks_basic'
c = conn.cursor()
c.execute('''CREATE TABLE ''' + table_name + '''
                       (code     TEXT   PRIMARY KEY,
                       name     TEXT,
                       industry TEXT,
                       area     TEXT,
                       pe       DOUBLE,
                       outstanding  DOUBLE,
                       totals       DOUBLE,
                       totalAssets  DOUBLE,
                       liquidAssets DOUBLE,
                       fixedAssets  DOUBLE,
                       reserved DOUBLE,
                       reservedPerShare DOUBLE,
                       esp   DOUBLE,
                       bvps    DOUBLE,
                       pb  DOUBLE,
                       timeToMarket      TEXT,
                       undp  DOUBLE,
                       perundp     DOUBLE,
                       rev   DOUBLE,
                       profit    DOUBLE,
                       gpr   DOUBLE,
                       npr    DOUBLE,
                       holders INT )''')
conn.commit()

code = data.index
data = data.values
print(data[0])
for i in range(len(data)):
    print("Table created successfully")
    c.execute(
        "INSERT INTO " + table_name +
        " (code,name, industry, area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
        esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
        ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',\
                                      '{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}')".format(
            code[i], data[i][0], data[i][1],
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
conn.close()
