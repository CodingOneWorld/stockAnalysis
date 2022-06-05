# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from analysis_util.cal_stock_trend import cal_trend_common
from contants.common_contants import DB_PATH
from fundamental_data.get_income import get_income_of_latest_years
from fundamental_data.get_profit import get_profit_of_latest_years

if __name__ == '__main__':
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    stock_list_data = pd.read_sql('select * from stockList', conn)
    print(stock_list_data.head())

    # 暂不考虑近3年刚上市的股票
    stock_list_data=stock_list_data[stock_list_data['list_date']<='20190101']

    stock_list = stock_list_data.loc[:, ['symbol', 'name']].values
    print(stock_list)
    print(len(stock_list))

    # 去除创业板和st股
    stock_array = []
    count = 0
    for i in stock_list:
        print(i)
        if (i[0].startswith('0') or i[0].startswith('6')) and not i[1].__contains__('ST') and not i[1].__contains__('退'):
            count += 1
            stock_array.append([i[0],i[1]])
            print('满足条件')
    print("去除创业板和st股后剩余股票数")
    print(count)

    # 去除收入和净利润近5年没有持续增长的股票
    for s in stock_array:
        print(s)
        # 计算最近5年的收入和净利润
        # 收入
        income_data = get_income_of_latest_years(s[0], 5)
        k1 = cal_trend_common(income_data)
        # 净利润
        profit_data = get_profit_of_latest_years(s[0], 5)
        k2 = cal_trend_common(profit_data)
        if k1 < 0 or k2 < 0:
            print('remove')
            stock_array.remove(s)
    print("去除收入和净利润近5年没有持续增长的股票后剩余股票数")
    print(stock_array.__len__())

    # 输出到文本文件中
    fw=open("stock_pool.txt",'w')
    fw.write("symbol,stock_name" + '\n')
    for s in stock_array:
        print(s[0]+","+s[1])
        fw.write(s[0]+","+s[1]+'\n')
    fw.flush()
    fw.close()

