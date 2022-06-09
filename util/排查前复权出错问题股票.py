# -*- coding: utf-8 -*-

# 遍历每一只股票，查找close与preclose对不上的股票

import sqlite3
import pandas as pd

from contants.common_contants import DB_PATH

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

conn = sqlite3.connect(DB_PATH)

# 读取股票列表
stock_list = pd.read_sql('select * from stockList' , conn)['symbol'].values
print(stock_list)
# stock_list=['000538']

for code in stock_list:
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    # print(stock_trade_data.head())
    pre_close=stock_trade_data['pre_close'].values[1:]
    close=stock_trade_data['close'].values[:-1]
    trade_date=stock_trade_data['trade_date'].values[:-1]
    # print(len(pre_close))
    # print(len(close))
    df=pd.DataFrame()
    df['trade_date']=trade_date
    df['pre_close']=pre_close
    df['close']=close
    df['dif']=abs(df['pre_close']-df['close'])
    df=df[df['dif']>1]
    if df['close'].count()>0:
        print(table_name)
        print("出错行")
        print(df)


