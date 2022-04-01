# -*- coding: utf-8 -*-
import sqlite3

import tushare as ts
import pandas as pd

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
from contants.common_contants import DB_PATH

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# path




def createDailyTableonOneStock(ts_code, filepath):
    # ts token
    pro = ts.pro_api('ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f')

    # 连接sqlite数据库
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    # print("Opened database successfully")

    # 查询当前所有正常上市交易的股票列表
    stock_basic = pro.stock_basic(exchange='', list_status='L')
    stock_basic = stock_basic[['ts_code', 'name', 'list_date']]
    name = stock_basic['name'].loc[stock_basic['ts_code'] == ts_code].values[0]
    df = ts.pro_bar(ts_code=ts_code, adj='qfq')
    df2 = df.sort_index(ascending=False)
    # print(df2)
    df2.reset_index(drop=True, inplace=True)
    df2['name'] = [name] * len(df2)
    # print(df2)
    data = df2.values
    # 创建表
    table_name = 'S' + ts_code.split('.')[0] + '_daily'
    print("create new table: " + table_name)
    # c.execute('''CREATE TABLE ''' + table_name + '''
    #                        (trade_date INT PRIMARY KEY     NOT NULL,
    #                        ts_code  TEXT,
    #                        name     TEXT,
    #                        open     DOUBLE,
    #                        high        DOUBLE,
    #                        low     DOUBLE,
    #                        close   DOUBLE,
    #                        pre_close   DOUBLE,
    #                        change  DOUBLE,
    #                        pct_chg DOUBLE,
    #                        vol     DOUBLE,
    #                        amount   DOUBLE)''')
    # conn.commit()
    # # 批量插入数据
    # sql = "INSERT INTO " + table_name + " (ts_code,trade_date,open,high,low,close,pre_close," \
    #                                     "change,pct_chg,vol,amount,name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    # c.executemany(sql, data)
    # conn.commit()
    df2.to_sql(table_name, con=conn, if_exists='replace', index=False)
    print(table_name + ' done')


if __name__ == '__main__':
    # 股票代码
    ts_code = "830832.BJ"
    createDailyTableonOneStock(ts_code, DB_PATH)
