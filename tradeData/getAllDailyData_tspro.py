# -*- coding: utf-8 -*-

# 获取所有股票的代码，下载所有股票的日线信息


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
stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
print(stock_basic)
stocks = stock_basic['ts_code'].values
print(stocks)

# 获取股票的日线数据-前复权数据
ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

# for循环
# 基础积分每分钟内最多调取200次，每次4000条数据
# 加入计数和睡眠，计数为200，睡眠1分钟
count = 40

# 连接sqlite数据库
conn = sqlite3.connect('P:/Money/stocks.db')
c = conn.cursor()
print("Opened database successfully")

for i in range(0, len(stocks)):
    ts_code = stocks[i]
    print(i)
    count -= 1
    if count < 0:
        time.sleep(30)
        count = 40
    name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
    print(name)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq')
    if df is None:
        continue
    df2 = df.sort_index(ascending=False)
    # print(df2)
    df2.reset_index(drop=True, inplace=True)
    df2['name'] = [name] * len(df2)
    # print(df2)
    # 写入csv
    # df2.to_csv("D:/Money/stocks/" + ts_code + ".csv",index=None)
    data = df2.values
    # 创建表
    table_name = 'S' + data[0][0].split('.')[0] + '_daily'
    print(table_name)
    c.execute('''CREATE TABLE ''' + table_name + '''
                       (trade_date INT PRIMARY KEY     NOT NULL,
                       ts_code  TEXT,
                       name     TEXT,
                       open     DOUBLE,
                       high        DOUBLE,
                       low     DOUBLE,
                       close   DOUBLE,
                       pre_close   DOUBLE,
                       change  DOUBLE,
                       pct_chg DOUBLE,
                       vol     DOUBLE,
                       amount   DOUBLE)''')
    conn.commit()
    # 插入数据
    # for line in data:
    #     print(line[1])
    #     c.execute("INSERT INTO " + table_name + " (ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount,name) \
    #               VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(line[0],
    #                                                                                                          line[1],
    #                                                                                                          line[2],
    #                                                                                                          line[3],
    #                                                                                                          line[4],
    #                                                                                                          line[5],
    #                                                                                                          line[6],
    #                                                                                                          line[7],
    #                                                                                                          line[8],
    #                                                                                                          line[9],
    #                                                                                                          line[10],
    #                                                                                                          line[11]))
    #     conn.commit()

    # 批量插入数据
    sql = "INSERT INTO " + table_name + " (ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount,name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    c.executemany(sql, data)
    conn.commit()
    print(table_name + ' done')
conn.close()
