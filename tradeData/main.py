# -*- coding: utf-8 -*-
import sqlite3

from contants.commonContants import DB_PATH
from tradeData.updateDailyTradeData import updateDailyData_tspro
from tradeData.getStockBasicList import getStockBasicList_tspro
import pandas as pd
import datetime

# 参数
# db path

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

updateDailyData_tspro(update_date, DB_PATH, 0, 0, 0)
getStockBasicList_tspro(DB_PATH)
