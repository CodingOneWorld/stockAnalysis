# -*- coding: utf-8 -*-
import datetime
import sqlite3
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import pinyin

from analysis_util.general_utils import get_stock_name, get_stock_code
from constants.common_constants import DB_PATH
from trade_data.get_trade_data import get_stock_trade_data, get_stock_trade_data_latestdays


def load_data(stock, latest_days):
    # 连接sqlite数据库
    # conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    # table_name = 'S' + stock + '_daily'
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[-latest_days:]
    stock_trade_data = get_stock_trade_data_latestdays(stock, latest_days)
    # print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    # print(stock_trade_data.head())
    return stock_trade_data


def plot_k_line(stock, latest_days):
    stock_trade_data = load_data(stock, latest_days)
    stock_name = get_stock_name(stock)
    # OHLC图
    # 解决mplfinance绘制输出中文乱码
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # s = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.family': 'SimHei'})
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    mpf.plot(stock_trade_data, type='candle', title=pinyin.get(stock_name, delimiter=" "),
             mav=(10, 20, 30, 60, 140),
             volume=True,
             # style=s
             )


if __name__ == '__main__':
    s = get_stock_code('克来机电')
    plot_k_line(s, 10)
