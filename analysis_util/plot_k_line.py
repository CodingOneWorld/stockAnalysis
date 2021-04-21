# -*- coding: utf-8 -*-
import datetime
import sqlite3

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
import mplfinance as mpf
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab

from contants.commonContants import DB_PATH


def load_data(code):
    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[:100]
    print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(lambda x: datetime.datetime.strptime(str(x),'%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data=stock_trade_data[["open","high","close","low","vol"]]
    print(stock_trade_data.head())
    return stock_trade_data

stock_trade_data=load_data('000001')
mpf.plot(stock_trade_data)