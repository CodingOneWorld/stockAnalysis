# -*- coding: utf-8 -*-

import tushare as ts
import matplotlib.pyplot as plt
import sqlite3

# 连接sqlite数据库
conn=sqlite3.connect('D:/Money/stocks.db')
print("Opened database successfully")

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
df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='19920101', end_date='20191021')
df2=df.sort_index(ascending=False)
df2.reset_index(drop=True, inplace=True)
#df2['open'].plot()
#plt.show()
data=df2.values
print(data)

for line in data:
    # 创建表
    c = conn.cursor()
    c.execute('''CREATE TABLE 000001SZ
               (trade_date INT PRIMARY KEY     NOT NULL,
               ts_code  TEXT,
               open     DOUBLE,
               high	    DOUBLE,
               low	    DOUBLE,
               close	DOUBLE,
               pre_close	DOUBLE,
               change	DOUBLE,
               pct_chg	DOUBLE,
               vol	    DOUBLE,
               amount   DOUBLE)''')
    conn.commit()
    print("Table created successfully")
    c.execute("INSERT INTO 000001SZ (ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount) \
              VALUES ({},{},{},'{},'{}','{}','{}','{}')".format(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10]));
    conn.commit()
    conn.close()
