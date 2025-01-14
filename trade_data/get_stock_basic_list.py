# -*- coding: utf-8 -*-

# 获取所有正常上市的股票列表

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import sqlite3
import sys

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


# 股票基础信息表 最新 tspro
def get_stock_basic_list(source='DB'):
    if source == 'file':
        # stock_basic=pd.read_csv('stock_list.csv',dtype={'symbol': np.str}, delimiter=',')
        stock_basic = pd.read_csv('stock_list.csv', dtype={'symbol': np.str_}, delimiter=',')
        # 去除创业板和科创板
        stock_basic = stock_basic[stock_basic.symbol.str.startswith('3') == False][
            stock_basic.symbol.str.startswith('688') == False]
        # print(stock_basic.head())
    elif source == 'DB':
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        stock_basic = pd.read_sql('select * from stock_list', conn)
        # 去除创业板和科创板
        stock_basic = stock_basic[stock_basic.symbol.str.startswith('3') == False][
            stock_basic.symbol.str.startswith('688') == False]
    # 获取当前日期
    # localdate = int(time.strftime("%Y%m%d", time.localtime()))
    # stock_basic = stock_basic[stock_basic['list_date'] < localdate]
    return stock_basic


# 读取股票列表，写入数据库
# 这里的股票列表是全的，写入数据库的列表也是全的
def get_stock_basic_list_2DB(source='DB'):
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    if source == 'DB':
        stock_basic = pd.read_sql('select * from stock_list', conn)
    else:
        # ts token
        ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
        pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
        # 获取ts_pro股票列表
        stock_basic = pro.stock_basic(exchange='', list_status='L')
        # 在运行时写入文件
        stock_basic.to_csv('stock_list.csv', index=0)
        # 写入数据库
        stock_basic.to_sql('stock_list', con=conn, if_exists='replace', index=False)
    # 获取当前日期
    localdate = time.strftime("%Y%m%d", time.localtime())
    stock_basic = stock_basic[stock_basic['list_date'] < localdate]

    print(stock_basic.head())
    print(len(stock_basic))

    return stock_basic


if __name__ == '__main__':
    # getStockBasicList(filepath)
    # get_stock_basic_list_tspro2DB(DB_PATH)
    df = get_stock_basic_list('file')
    print(df.head())
    df = df[df.symbol.str.startswith('3') == False][
        df.symbol.str.startswith('688') == False][df.ts_code.str.contains('BJ') == False]
    # print(stock_basic)
    stocks_tspro = df['ts_code'].values
    print(len(df))

# 废弃 ts 获取股票基本信息表
# 获取股票的基础数据，按天来存储
# def get_stock_basic_data_ts():
#     data = ts.get_stock_basics()
#     # print(data)
#
#     # 连接sqlite数据库
#     conn = sqlite3.connect(DB_PATH)
#     print("Opened database successfully")
#
#     # 创建表
#     table_name = 'stocks_basic'
#     c = conn.cursor()
#     c.execute('''CREATE TABLE ''' + table_name + '''
#                            (code     TEXT   PRIMARY KEY,
#                            name     TEXT,
#                            industry TEXT,
#                            area     TEXT,
#                            pe       DOUBLE,
#                            outstanding  DOUBLE,
#                            totals       DOUBLE,
#                            totalAssets  DOUBLE,
#                            liquidAssets DOUBLE,
#                            fixedAssets  DOUBLE,
#                            reserved DOUBLE,
#                            reservedPerShare DOUBLE,
#                            esp   DOUBLE,
#                            bvps    DOUBLE,
#                            pb  DOUBLE,
#                            timeToMarket      TEXT,
#                            undp  DOUBLE,
#                            perundp     DOUBLE,
#                            rev   DOUBLE,
#                            profit    DOUBLE,
#                            gpr   DOUBLE,
#                            npr    DOUBLE,
#                            holders INT )''')
#     conn.commit()
#
#     code = data.index
#     data = data.values
#     print(data[0])
#     for i in range(len(data)):
#         print("Table created successfully")
#         c.execute(
#             "INSERT INTO " + table_name +
#             " (code,name, industry, area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
#             esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
#             ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',\
#                                           '{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}')".format(
#                 code[i], data[i][0], data[i][1],
#                 data[i][2], data[i][3],
#                 data[i][4], data[i][5],
#                 data[i][6], data[i][7],
#                 data[i][8], data[i][9],
#                 data[i][10], data[i][11],
#                 data[i][12], data[i][13],
#                 data[i][14], data[i][15],
#                 data[i][16], data[i][17],
#                 data[i][18], data[i][19],
#                 data[i][20], data[i][21]))
#         conn.commit()
#     conn.close()

# 废弃
# 股票列表来自ts与ts_pro的股票列表的交集
# 股票的基本信息部分来自ts，部分来自ts_pro
# def getStockBasicList(filepath):
#     # ts_pro token
#     pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
#
#     # 连接sqlite数据库
#     conn = sqlite3.connect(filepath)
#     print("Opened database successfully")
#
#     # 查询ts_pro中当前所有正常上市交易的股票基本信息
#     # ts_pro中包含的需要的信息
#     # ts_code  symbol    name  area industry market list_date
#     stock_basic = pro.stock_basic(exchange='', list_status='L')
#     # stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
#     # 删除当前日期之后的股票信息
#     # 获取当前日期
#     localdate = time.strftime("%Y%m%d", time.localtime())
#     stock_basic = stock_basic[stock_basic['list_date'] < localdate]
#     # print(stock_basic)
#
#     # 获取ts_pro的股票列表
#     stocks_pro = stock_basic['symbol'].values
#
#     stocks_pro = set(stocks_pro)
#     print(len(stocks_pro))
#     print(stocks_pro)
#
#     # 将stock_basic变为数组
#     stock_basic = stock_basic.values
#     # print(stock_basic)
#
#     # 查询tushare中股票的基本信息数据
#     data = ts.get_stock_basics()
#
#     # 获取ts中的股票列表
#     stocks_ts = set(data.index)
#     print(len(stocks_ts))
#     print(stocks_ts)
#
#     # ts与ts_pro股票列表的交集
#     s_stocks = list(stocks_pro.intersection(stocks_ts))
#     print(len(s_stocks))
#     print(s_stocks)
#
#     c = conn.cursor()
#     table_name = 'stock_basic_list'
#     c.execute("drop table " + table_name)
#     conn.commit()
#     c.execute('''CREATE TABLE ''' + table_name + '''
#                            (ts_code  TEXT PRIMARY KEY NOT NULL,
#                            symbol     TEXT,
#                            name     TEXT,
#                            area        TEXT,
#                            industry     TEXT,
#                            market   TEXT,
#                            list_date   INT,
#                            pe       DOUBLE,
#                            pb  DOUBLE,
#                            outstanding  DOUBLE,
#                            totals       DOUBLE,
#                            totalAssets  DOUBLE,
#                            liquidAssets DOUBLE,
#                            fixedAssets  DOUBLE,
#                            reserved DOUBLE,
#                            reservedPerShare DOUBLE,
#                            esp   DOUBLE,
#                            bvps    DOUBLE,
#                            undp  DOUBLE,
#                            perundp     DOUBLE,
#                            rev   DOUBLE,
#                            profit    DOUBLE,
#                            gpr   DOUBLE,
#                            npr    DOUBLE,
#                            holders INT)''')
#     conn.commit()
#     print("Table created successfully")
#     batchdata = []
#     for i in range(len(stock_basic)):
#         print(stock_basic[i])
#         code = stock_basic[i][1]
#         if code in s_stocks:
#             # 批量插入
#             line = data.loc[code].values
#             batchdata.append(
#                 [stock_basic[i][0], stock_basic[i][1], stock_basic[i][2], stock_basic[i][3], stock_basic[i][4],
#                  stock_basic[i][5], stock_basic[i][6], line[3], line[4], line[5],
#                  line[6], line[7], line[8], line[9], line[10], line[11],
#                  line[12], line[13], line[15], line[16], line[17],
#                  line[18], line[19], line[20], line[21]])
#     sql = "INSERT INTO " + table_name + \
#           " (ts_code,symbol,name,area,industry,market,list_date,pe,outstanding,\
#           totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,\
#           esp,bvps,pb,undp,perundp,rev,profit,gpr,npr,holders) VALUES \
#           (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
#     # c.executemany(sql, batchdata)
#     conn.commit()
#     conn.close()
