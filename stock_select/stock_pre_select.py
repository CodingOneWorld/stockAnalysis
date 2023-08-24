# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from analysis_util.cal_stock_trend import cal_trend_common
from fundamental_data.get_income import get_income_of_latest_years
from fundamental_data.get_profit import get_profit_of_latest_years
from trade_data.get_stock_basic_list import get_stock_basic_list
from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

if __name__ == '__main__':
    # 读取全部股票数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取股票基本信息表
    # stock_list_data = pd.read_sql('select * from stock_list', conn)
    stock_list_data = get_stock_basic_list()
    print(stock_list_data.head())

    # 暂不考虑近3年刚上市的股票
    stock_list_data = stock_list_data[stock_list_data['list_date'] <= '20200101']

    stock_list = stock_list_data.loc[:, ['symbol', 'name']].values
    print(stock_list)
    print(len(stock_list))

    # 去除创业板和st股
    stock_array = []
    count = 0
    for i in stock_list:
        print(i)
        if (i[0].startswith('0') or i[0].startswith('6')) and not i[1].__contains__('ST') and not i[1].__contains__(
                '退'):
            count += 1
            stock_array.append([i[0], i[1]])
            print('满足条件')
    print("去除创业板和st股后剩余股票数")
    print(count)

    # 收入和净利润近5年均大于0
    for s in stock_array:
        print(s)
        # 计算最近5年的收入和净利润
        # 收入
        income_data = get_income_of_latest_years(s[0], 5)
        print(income_data)
        tag1 = 0
        for income in income_data:
            if income < 0:
                tag1 = 1
        # k1 = cal_trend_common(income_data)
        # 净利润
        profit_data = get_profit_of_latest_years(s[0], 5)
        print(profit_data)
        tag2 = 0
        for profit in profit_data:
            if profit < 0:
                tag2 = 1
        # k2 = cal_trend_common(profit_data)
        if tag1 > 0 and tag2 > 0:
            # if k1 < 0 or k2 < 0:
            print('remove:', s)
            stock_array.remove(s)
    print("去除收入和净利润近5年没有持续增长的股票后剩余股票数")
    print(stock_array.__len__())

    # 输出到文本文件中
    fw = open("stock_pool2023.txt", 'w')
    fw.write("symbol,stock_name" + '\n')
    for s in stock_array:
        print(s[0] + "," + s[1])
        fw.write(s[0] + "," + s[1] + '\n')
    fw.flush()
    fw.close()
