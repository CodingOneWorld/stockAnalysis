# -*- coding: utf-8 -*-
import datetime
import sqlite3
import pandas as pd
import mplfinance as mpf

from analysis_util.general_utils import get_stock_name, get_stock_code
from trade_data.get_trade_data import get_stock_trade_data, get_stock_trade_data_latestdays


def load_data(code, start_date, end_date):
    stock_trade_data = get_stock_trade_data(code, start_date, end_date)
    # print(stock_trade_data.head())
    stock_trade_data=stock_trade_data[stock_trade_data.trade_date>=start_date][stock_trade_data.trade_date<=end_date]
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    # print(stock_trade_data)
    return stock_trade_data


def load_data_latestdays(code, latest_days):
    # 连接sqlite数据库
    # conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    # table_name = 'S' + stock + '_daily'
    # stock_trade_data = pd.read_sql('select * from ' + table_name, conn)[-latest_days:]
    stock_trade_data = get_stock_trade_data_latestdays(code, latest_days)
    # print(stock_trade_data.head())
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(
        lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
    stock_trade_data.set_index("trade_date", inplace=True)
    stock_trade_data = stock_trade_data[["open", "high", "close", "low", "vol"]]
    stock_trade_data.rename(columns={'vol': 'volume'}, inplace=True)
    print(','.join([str(x) for x in stock_trade_data['close'].values]))
    return stock_trade_data


def plot_k_line_latestdays(symbol, latest_days):
    stock_trade_data = load_data_latestdays(symbol, latest_days)
    # OHLC图
    # # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
    # my_color = mpf.make_marketcolors(up='r',
    #                                  down='g',
    #                                  edge='inherit',
    #                                  wick='inherit',
    #                                  volume='inherit')
    # # 设置图表的背景色
    # my_style = mpf.make_mpf_style(marketcolors=my_color,
    #                               figcolor='(0.82, 0.83, 0.85)',
    #                               gridcolor='(0.82, 0.83, 0.85)')
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    # mpf.plot(stock_trade_data, type='candle', style=my_style, mav=(5, 10, 20, 30, 60, 140), volume=True)
    mpf.plot(stock_trade_data, type='candle', mav=(5, 10, 20, 30, 60, 140), volume=True)


# 起止日，到终止日
def plot_k_line(code, start_date, end_date, mav=None):
    if mav is None:
        mav = [5, 10, 20, 30, 40, 60, 140]
    stock_trade_data = load_data(code, start_date, end_date)
    # OHLC图
    # # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
    # my_color = mpf.make_marketcolors(up='r',
    #                                  down='b',
    #                                  edge='inherit',
    #                                  wick='inherit',
    #                                  volume='inherit')
    # # 设置图表的背景色
    # my_style = mpf.make_mpf_style(marketcolors=my_color,
    #                               figcolor='(0.82, 0.83, 0.85)',
    #                               gridcolor='(0.82, 0.83, 0.85)')
    # mpf.plot(stock_trade_data)
    # K线图，附带均线，成交量
    # mpf.plot(stock_trade_data, type='candle', style=my_style, mav=mav, volume=True)
    mpf.plot(stock_trade_data, type='candle', mav=mav, volume=True)


def save_k_line(code, latest_days, save_path):
    stock_trade_data = load_data_latestdays(code, latest_days)
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
    mpf.plot(stock_trade_data, type='candle', style=my_style, mav=(10, 20, 30, 60, 140), volume=True, savefig=save_path)


if __name__ == '__main__':
    s = get_stock_code('澳柯玛')
    plot_k_line_latestdays(s, 250)
    # plot_k_line(s,'20220929','20230531')
