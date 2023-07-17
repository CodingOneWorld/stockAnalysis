# -*- coding: utf-8 -*-

# 获取增量数据，并写入数据库
import datetime

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

import time
import os
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from trade_data.get_stock_basic_list import get_stock_basic_list
from trade_data.trade_data_utils import createDailyTableonOneStock
from util.date_util import get_today_date, date_add
from util.utils_common import code2ts_code

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


def get_stock_trade_data(code, start_date='', end_date=''):
    # ts token
    ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
    ts_code = code2ts_code(code)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
    df = df.dropna(axis=0, subset=["close"])
    df2 = df.sort_index(ascending=False)
    df2.reset_index(drop=True, inplace=True)
    print(df2.head())
    return df2


def get_stock_trade_data_latestdays(code, latestdays):
    # ts token
    ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
    ts_code = code2ts_code(code)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq')
    df = df.dropna(axis=0, subset=["close"])
    df2 = df.sort_index(ascending=False)
    if latestdays > len(df2['ts_code']):
        latestdays = len(df2['ts_code'])
    # df2 = df2.iloc[-latestdays:]
    df2 = df2[-latestdays:]
    df2.reset_index(drop=True, inplace=True)
    print(df2)
    return df2


# 获取股票的日线数据-前复权数据 ts_pro
# 全量更新
def get_daily_data_tspro2DB(filepath, cou_new, cou_del):
    # ts token
    ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
    pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
    # 数据库连接
    conn = sqlite3.connect(filepath)
    print("Opened database successfully")
    c = conn.cursor()
    # 查询数据库中已有的股票列表
    cursor = c.execute("SELECT ts_code,name from stock_list")
    stocks_old = []
    for row in cursor:
        stocks_old.append(row[0])
    print("数据库中已有股票数")
    print(len(stocks_old))

    # 查询最新的股票列表，并写入数据库
    stock_basic = get_stock_basic_list('file')
    # print(stock_basic)
    stocks_tspro = stock_basic['ts_code'].values
    print("ts_pro中最新股票列表数")
    stocks_now = set(stocks_tspro)
    print(len(stocks_now))

    # 写入数据库
    conn = sqlite3.connect(filepath)
    print("Open database successfully")
    stock_basic.to_sql('stock_list', con=conn, if_exists='replace', index=False)
    print("insert database successfully")

    # ts_pro中最新股票列表，全量更新
    # 基础积分每分钟内最多调取200次，每次4000条数据
    # 加入计数和睡眠
    stocks_new = sorted(list(stocks_now))
    # count = 99
    for i in range(cou_new, len(stocks_new)):
        print('stocks_now:' + str(i))
        ts_code = stocks_new[i]
        print(ts_code)
        # count -= 1
        # if count < 0:
        #     time.sleep(30)
        #     count = 99
        name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
        print(name)
        df = ts.pro_bar(ts_code=ts_code, adj='qfq')
        if df is None:
            continue
        df = df.dropna(axis=0, subset=["close"])
        df2 = df.sort_index(ascending=False)
        # print(df2)
        df2.reset_index(drop=True, inplace=True)
        df2['name'] = [name] * len(df2)
        print(df2.head())
        print(df2[-5:])
        # 表名
        table_name = 'S' + ts_code.split('.')[0] + '_daily'
        # 写入数据库
        df2.to_sql(table_name, con=conn, if_exists='replace', index=False)
        print(table_name + ' done')

    # 针对原有的已退市的股票，删表
    stocks_del = list(set(stocks_old).difference(set(stocks_now)))
    print("已退市股票：")
    print(len(stocks_del))
    for i in range(cou_del, len(stocks_del)):
        print('stocks_del:' + stocks_del[i])
        table_name = 'S' + stocks_del[i].split('.')[0] + '_daily'
        c.execute("drop table " + table_name)

    conn.close()


if __name__ == '__main__':
    # get_stock_trade_data('000001','20180101')
    get_stock_trade_data_latestdays('000001', 50)

# 旧方法，保留已有数据，每次累加数据，会有错误，因为每次前复权的价格都是以当前价格重新进行的计算，累加数据会有错误
# 获取股票的日线数据-前复权数据 ts_pro
# 方法分为三部分
# cou_inner 对于已有的股票增量更新日线数据，如果在这运行出错，可以替换为出错的索引值；想跳过设为-1
# cou_new 对于新加的股票，新建表记录数据，如果在这运行出错，可以替换为出错的索引值；想跳过设为-1
# cou_del 对于已经没有的股票（退市）删表，如果在这运行出错，可以替换为出错的索引值；想跳过设为-1
# def update_daily_data_tspro(update_date, filepath, cou_inner, cou_new, cou_del):
#     # ts token
#     ts.set_token('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
#     pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')
#     # 数据库连接
#     conn = sqlite3.connect(filepath)
#     print("Opened database successfully")
#     c = conn.cursor()
#     # 查询数据库中已有的股票列表
#     # cursor = c.execute("SELECT ts_code,name from stockList")
#     stocks_old = []
#     # for row in cursor:
#     #     stocks_old.append(row[0])
#     # print("数据库中已有股票数")
#     # print(len(stocks_old))
#
#     # 查询最新的股票列表
#     # ts_pro
#     stock_basic = pro.stock_basic(exchange='', list_status='L')
#     stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
#     # 获取当前日期
#     localdate = time.strftime("%Y%m%d", time.localtime())
#     stock_basic = stock_basic[stock_basic['list_date'] < localdate]
#     # print(stock_basic)
#     stocks_tspro = stock_basic['ts_code'].values
#     print("ts_pro中最新股票列表数")
#     # print(stocks_tspro)
#     print(len(stocks_tspro))
#
#     stocks_now = set(stocks_tspro)
#
#     # 针对数据库中已有的股票，进行数据追加写入
#     # 最新股票列表与数据库中股票列表的交集
#     print("新老股票列表的交集：")
#     stocks_inter = sorted(list(stocks_now.intersection(set(stocks_old))))
#     print(len(stocks_inter))
#
#     # 基础积分每分钟内最多调取200次，每次4000条数据
#     # 加入计数和睡眠，计数为200，睡眠一段时间
#     count = 99
#     if cou_inner != -1:
#         for i in range(cou_inner, len(stocks_inter)):
#             print('stocks_inter:' + str(i))
#             count -= 1
#             if count < 0:
#                 time.sleep(30)
#                 count = 99
#             ts_code = stocks_inter[i]
#             print('ts_code:' + ts_code)
#             name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
#             print(name)
#             # 查询日线数据
#             print('update_date:' + update_date)
#             df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=update_date)
#             if df is None:
#                 continue
#             df2 = df.sort_index(ascending=False)
#             # print(df2)
#             df2.reset_index(drop=True, inplace=True)
#             df2['name'] = [name] * len(df2)
#             print(df2)
#             data = df2.values
#             # # 向表中插入数据
#             table_name = 'S' + ts_code.split('.')[0] + '_daily'
#             # 批量插入数据
#             sql = "INSERT INTO " + table_name + " (ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg" \
#                                                 ",vol,amount,name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
#             status = 0
#             try:
#                 c.executemany(sql, data)
#                 conn.commit()
#             except:
#                 status = 1
#             # 如果报错表不存在，则创建新表
#             if status == 1:
#                 createDailyTableonOneStock(ts_code, filepath)
#
#             # df2.to_sql(table_name, con=conn, if_exists='append', index=False)
#             print(table_name + ' done')
#
#     # 针对新上市的股票，建表，插入数据
#     stocks_new = sorted(list(stocks_now.difference(set(stocks_old))))
#     print("新上市股票：")
#     print(len(stocks_new))
#     if cou_new != -1:
#         for i in range(cou_new, len(stocks_new)):
#             print('stocks_new:' + str(i))
#             ts_code = stocks_new[i]
#             print(ts_code)
#             count -= 1
#             if count < 0:
#                 time.sleep(30)
#                 count = 99
#             name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
#             print(name)
#             df = ts.pro_bar(ts_code=ts_code, adj='qfq')
#             if df is None:
#                 continue
#             df = df.dropna(axis=0, subset=["close"])
#             df2 = df.sort_index(ascending=False)
#             # print(df2)
#             df2.reset_index(drop=True, inplace=True)
#             df2['name'] = [name] * len(df2)
#             print(df2)
#             data = df2.values
#             # 创建表
#             table_name = 'S' + ts_code.split('.')[0] + '_daily'
#             # print(table_name)
#             c.execute("drop table if exists " + table_name)
#             c.execute('''CREATE TABLE ''' + table_name + '''
#                                (trade_date INT PRIMARY KEY     NOT NULL,
#                                ts_code  TEXT,
#                                name     TEXT,
#                                open     DOUBLE,
#                                high        DOUBLE,
#                                low     DOUBLE,
#                                close   DOUBLE,
#                                pre_close   DOUBLE,
#                                change  DOUBLE,
#                                pct_chg DOUBLE,
#                                vol     DOUBLE,
#                                amount   DOUBLE)''')
#             conn.commit()
#             # 批量插入数据
#             sql = "INSERT INTO " + table_name + " (ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol," \
#                                                 "amount,name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
#             c.executemany(sql, data)
#             conn.commit()
#             print(table_name + ' done')
#
#     # 针对原有的已退市的股票，删表
#     stocks_del = list(set(stocks_old).difference(set(stocks_now)))
#     print("已退市股票：")
#     print(len(stocks_del))
#     for i in range(cou_del, len(stocks_del)):
#         print('stocks_del:' + stocks_del[i])
#         table_name = 'S' + stocks_del[i].split('.')[0] + '_daily'
#         c.execute("drop table " + table_name)
#
#     conn.close()
