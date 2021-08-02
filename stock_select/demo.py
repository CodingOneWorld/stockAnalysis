# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from contants.commonContants import DB_PATH

if __name__ == '__main__':
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stockList', conn)
    print(stock_list_data.head())
    stock_list = stock_list_data.loc[:,['symbol','name']].values
    print(stock_list)
    print(len(stock_list))

    # 去除创业板和st股
    stock_array=[]
    count=0
    for i in stock_list:
        if (i[0].startswith('0') or i[0].startswith('6')) and  not i[1].__contains__('ST'):
            count+=1
            stock_array.append(i[0])

    print(count)

    # 去除业绩垫底股
    for s in stock_array:
        # 计算最近几年的收入和净利润



