# -*- coding: utf-8 -*-
import datetime
import sqlite3
import pandas as pd
import mplfinance as mpf
from contants.common_contants import DB_PATH


def load_data(stock,latest_days):
    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + stock + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[-latest_days:]
    print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    print(stock_trade_data.head())
    return stock_trade_data


def plot_k_line(stock,latest_days):
    stock_trade_data = load_data(stock,latest_days)
    # OHLC图
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    mpf.plot(stock_trade_data, type='candle', mav=(10,20,30, 60, 140), volume=True)


if __name__ == '__main__':
    plot_k_line('c',100)


