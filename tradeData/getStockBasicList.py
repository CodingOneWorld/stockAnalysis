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


def getStockBasicList(filepath):
    # ts_pro token
    pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

    # 连接sqlite数据库
    conn = sqlite3.connect(filepath)
    print("Opened database successfully")

    # 查询当前所有正常上市交易的股票列表
    stock_basic = pro.stock_basic(exchange='', list_status='L')
    # stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
    # 删除当前日期之后的股票信息
    # 获取当前日期
    localdate = time.strftime("%Y%m%d", time.localtime())
    stock_basic = stock_basic[stock_basic['list_date'] < localdate]
    print(stock_basic)
    # print(stock_basic)
    # 获取ts_pro的股票列表
    stocks_pro = stock_basic['symbol'].values
    stocks_pro = set(stocks_pro)
    # 部分股票信息在该列表里
    # ts_code  symbol    name  area industry market list_date
    stock_basic = stock_basic.values

    # 查询股票的基本信息数据-tushare
    data = ts.get_stock_basics()
    stocks_ts = set(data.index)
    s_stocks = stocks_pro.intersection(stocks_ts)

    c = conn.cursor()
    table_name = 'stock_basic_list'
    c.execute("drop table " + table_name)
    conn.commit()
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
                           undp  DOUBLE,
                           perundp     DOUBLE,
                           rev   DOUBLE,
                           profit    DOUBLE,
                           gpr   DOUBLE,
                           npr    DOUBLE,
                           holders INT)''')
    conn.commit()
    print("Table created successfully")
    batchdata = []
    for i in range(len(stock_basic)):
        print(stock_basic[i])
        code = stock_basic[i][1]
        if code in s_stocks:
            # line = data.loc[code].values
            # data.append([stock_basic[i][0], stock_basic[i][1], stock_basic[i][2], stock_basic[i][3], stock_basic[i][4],
            #              stock_basic[i][5], stock_basic[i][6], line[3], line[4], line[5],
            #              line[6], line[7], line[8], line[9], line[10], line[11],
            #              line[12], line[13], line[15], line[16], line[17],
            #              line[18], line[19], line[20], line[21]])
            # c.execute(
            #     "INSERT INTO " + table_name +
            #     " (ts_code,symbol,name,area,industry,market,list_date,pe,outstanding,\
            #     totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
            #     esp,bvps,pb,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
            #     ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',\
            #     '{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}')".format(
            #         stock_basic[i][0], stock_basic[i][1], stock_basic[i][2], stock_basic[i][3], stock_basic[i][4],
            #         stock_basic[i][5], stock_basic[i][6], line[3], line[4], line[5],
            #         line[6], line[7], line[8], line[9], line[10], line[11],
            #         line[12], line[13], line[15], line[16], line[17],
            #         line[18], line[19], line[20], line[21]))

            # 批量插入
            line = data.loc[code].values
            batchdata.append(
                [stock_basic[i][0], stock_basic[i][1], stock_basic[i][2], stock_basic[i][3], stock_basic[i][4],
                 stock_basic[i][5], stock_basic[i][6], line[3], line[4], line[5],
                 line[6], line[7], line[8], line[9], line[10], line[11],
                 line[12], line[13], line[15], line[16], line[17],
                 line[18], line[19], line[20], line[21]])
    sql = "INSERT INTO " + table_name + \
          " (ts_code,symbol,name,area,industry,market,list_date,pe,outstanding,\
          totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
          esp,bvps,pb,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
          (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    c.executemany(sql, batchdata)
    conn.commit()
    conn.close()

# filepath = 'E:/Money/stocks.db'
# getStockBasicList(filepath)
