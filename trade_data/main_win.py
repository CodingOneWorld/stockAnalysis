# -*- coding: utf-8 -*-

import sqlite3
from trade_data.update_daily_trade_data import update_daily_data_tspro
from trade_data.get_stock_basic_list import get_stock_basic_list_tspro
import pandas as pd
import datetime
import schedule
import time


def update_trade_data2_database(DB_PATH):
    # 从数据库中直接推算日期参数
    # update_date = "20201118"
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S000001_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    trade_date_arr = sorted(stock_trade_data['trade_date'].values, reverse=True)
    day0 = datetime.datetime.strptime(str(trade_date_arr[0]), '%Y%m%d')
    delta_1d = datetime.timedelta(days=1)
    update_date = (day0 + delta_1d).strftime('%Y%m%d')
    print(update_date)

    update_daily_data_tspro(update_date, DB_PATH, 0, 0, 0)
    get_stock_basic_list_tspro(DB_PATH)


if __name__ == '__main__':
    DB_PATH = "E:/Money/stocks.db"
    # schedule.every().day.at("18:00").do(update_trade_data2_database,DB_PATH)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    update_trade_data2_database(DB_PATH)
