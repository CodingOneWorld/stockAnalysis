# -*- coding: utf-8 -*-
import datetime
import sqlite3
import pandas as pd
import mplfinance as mpf

from analysis_util.general_utils import get_stock_name, get_stock_code
from trade_data.get_trade_data import get_stock_trade_data, get_stock_trade_data_latestdays


def load_data(symbol,start_date, end_date):
    # 连接sqlite数据库
    # conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    # table_name = 'S' + stock + '_daily'
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[-latest_days:]
    stock_trade_data = get_stock_trade_data(symbol, start_date,end_date)
    # print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    # print(stock_trade_data.head())
    return stock_trade_data

def load_data_latestdays(symbol,latest_days):
    # 连接sqlite数据库
    # conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    # table_name = 'S' + stock + '_daily'
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[-latest_days:]
    stock_trade_data=get_stock_trade_data_latestdays(symbol,latest_days)
    # print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    # print(stock_trade_data.head())
    return stock_trade_data


def plot_k_line_latestdays(stock,latest_days):
    stock_trade_data = load_data_latestdays(stock,latest_days)
    # OHLC图
    # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    # 设置图表的背景色
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    mpf.plot(stock_trade_data, type='candle', style=my_style,mav=(5,10,20,30, 60, 140), volume=True)


# 起止日，到终止日
def plot_k_line(symbol, start_date, end_date):
    stock_trade_data = load_data(symbol, start_date, end_date)
    # OHLC图
    # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    # 设置图表的背景色
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    mpf.plot(stock_trade_data, type='candle', style=my_style, mav=(5,10, 20, 30, 60, 140), volume=True)


def save_k_line(symbol,latest_days,save_path):
    stock_trade_data = load_data_latestdays(symbol,latest_days)
    # OHLC图
    # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
    my_color = mpf.make_marketcolors(up='r',
                                     down='g',
                                     edge='inherit',
                                     wick='inherit',
                                     volume='inherit')
    # 设置图表的背景色
    my_style = mpf.make_mpf_style(marketcolors=my_color,
                                  figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    mpf.plot(stock_trade_data, type='candle', style=my_style,mav=(10,20,30, 60, 140), volume=True,savefig=save_path)


if __name__ == '__main__':
    s=get_stock_code('艾迪精密')
    plot_k_line_latestdays(s,300)
    # plot_k_line(s,'20190301','20201231')

