# -*- coding: utf-8 -*-

import sqlite3
from trade_data.get_trade_data import get_daily_data_tspro2DB
from trade_data.get_stock_basic_list import get_stock_basic_list_tspro2DB
import pandas as pd
import datetime
import schedule
import time

from util.utils_common import get_dbpath_by_repo


def update_trade_data2db(DB_PATH):
    # # 从数据库中直接推算日期参数
    # # update_date = "20201118"
    # # pandas连接数据库
    # conn = sqlite3.connect(db_path)
    # # 读取相应的交易数据表
    # table_name = 'S000001_daily'
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    # trade_date_arr = sorted(stock_trade_data['trade_date'].values, reverse=True)
    # day0 = datetime.datetime.strptime(str(trade_date_arr[0]), '%Y%m%d')
    # delta_1d = datetime.timedelta(days=1)
    # update_date = (day0 + delta_1d).strftime('%Y%m%d')
    # # update_date = '20220402'
    # print(update_date)

    get_daily_data_tspro2DB(DB_PATH, 0, 0)


if __name__ == '__main__':
    t1= datetime.datetime.now()
    DB_PATH = get_dbpath_by_repo()
    # schedule.every().day.at("17:00").do(update_trade_data2db, DB_PATH)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    update_trade_data2db(DB_PATH)

    t2= datetime.datetime.now()
    print(t2-t1)
