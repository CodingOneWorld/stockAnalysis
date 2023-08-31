# -*- coding: utf-8 -*-

import sqlite3
from trade_data.get_trade_data import get_daily_data_tspro2DB
from util.utils_common import get_dbpath_by_repo
import pandas as pd

import datetime
import schedule
import time


# def update_trade_data2_db_old(db_path):
#     # 从数据库中直接推算日期参数
#     # update_date = "20201118"
#     # pandas连接数据库
#     conn = sqlite3.connect(db_path)
#     # 读取相应的交易数据表
#     table_name = 'S000001_daily'
#     stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
#     trade_date_arr = sorted(stock_trade_data['trade_date'].values, reverse=True)
#     day0 = datetime.datetime.strptime(str(trade_date_arr[0]), '%Y%m%d')
#     delta_1d = datetime.timedelta(days=1)
#     update_date = (day0 + delta_1d).strftime('%Y%m%d')
#     # update_date = '20220422'
#     print(update_date)
#
#     update_daily_data_tspro(update_date, db_path, 0, 0, 0)
#     get_stock_basic_list_tspro(db_path)


def update_trade_data2db(DB_PATH):
    get_daily_data_tspro2DB(DB_PATH,0 , 0)
    # get_stock_basic_list_tspro2DB(DB_PATH)


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    DB_PATH = get_dbpath_by_repo()
    # print(DB_PATH)
    # schedule.every().day.at("19:00").do(update_trade_data2db, DB_PATH)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    update_trade_data2db(DB_PATH)

    t2 = datetime.datetime.now()
    print(t2 - t1)

