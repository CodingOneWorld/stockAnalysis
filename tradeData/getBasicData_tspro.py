# -*- coding: utf-8 -*-

# 获取所有股票的代码，下载所有股票的日线信息

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import time
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from contants.commonContants import DB_PATH

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

# for循环
# 基础积分每分钟内最多调取200次，每次4000条数据
# 加入计数和睡眠，计数为200，睡眠1分钟
count = 40

conn = sqlite3.connect(DB_PATH)
# 连接sqlite数据库
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
    df = pro.daily_basic(ts_code=ts_code)
    if df is None:
        continue
    df2 = df.sort_index(ascending=False)
    # print(df2)
    df2.reset_index(drop=True, inplace=True)
    df2['name'] = [name] * len(df2)
    # print(df2)
    # 写入数据库
    # df2.to_csv("D:/Money/stocks/" + ts_code + ".csv",index=None)
    data = df2.values
    # 创建表
    table_name = 'S' + data[0][0].split('.')[0] + '_basic'
    print(table_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE ''' + table_name + '''
                       (trade_date TEXT PRIMARY KEY     NOT NULL,
                        ts_code  TEXT,
                        close    DOUBLE,
                        turnover_rate 	DOUBLE,
                        turnover_rate_f 	DOUBLE,
                        volume_ratio 	DOUBLE,
                        pe 	DOUBLE,
                        pe_ttm 	DOUBLE,
                        pb 	DOUBLE,
                        ps 	DOUBLE,
                        ps_ttm 	DOUBLE,
                        total_share 	DOUBLE,
                        float_share 	DOUBLE,
                        free_share 	DOUBLE,
                        total_mv 	DOUBLE,
                        circ_mv 	DOUBLE)''')
    conn.commit()
    # 批量插入数据
    sql = "INSERT INTO " + table_name + " (trade_date,ts_code,close,turnover_rate,turnover_rate_f,volume_ratio,pe," \
                                        "pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv) " \
                                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    c.executemany(sql, data)
    conn.commit()
    print(table_name + ' done')
conn.close()
