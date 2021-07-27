# -*- coding: utf-8 -*-

# 导入包
import pandas as pd
import sqlite3
from contants.commonContants import DB_PATH
import matplotlib.pyplot as plt

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


def cal_mean_line(code, latest_days):
    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(lambda x: str(x))
    stock_trade_data.set_index("trade_date", inplace=True)

    latest_days = latest_days if len(stock_trade_data.close) > latest_days else len(stock_trade_data.close)
    start_days = len(stock_trade_data.close) - latest_days + 1
    stock_trade_data = stock_trade_data.iloc[start_days:len(stock_trade_data.close), :]

    # 绘制交易金额曲线
    stock_trade_data.loc[:, 'low'].plot.line()

    # 计算移动均线，根据收盘价
    df_mean = stock_trade_data.close.rolling(window=10).mean().fillna(0)
    # print(df_mean)
    mean_10_latest = df_mean.values[-1]
    # print(mean_10_latest)

    df_mean = stock_trade_data.close.rolling(window=20).mean().fillna(0)
    # print(df_mean)
    mean_20_latest = df_mean.values[-1]
    # print(mean_20_latest)

    df_mean = stock_trade_data.close.rolling(window=30).mean().fillna(0)
    # print(df_mean)
    mean_30_latest = df_mean.values[-1]
    # print(mean_30_latest)

    df_mean = stock_trade_data.close.rolling(window=60).mean().fillna(0)
    # print(df_mean)
    mean_60_latest = df_mean.values[-1]
    # print(mean_60_latest)

    df_mean = stock_trade_data.close.rolling(window=88).mean().fillna(0)
    mean_88_latest = df_mean.values[-1]
    # print(mean_88_latest)

    df_mean = stock_trade_data.close.rolling(window=120).mean().fillna(0)
    mean_120_latest = df_mean.values[-1]
    # print(mean_120_latest)

    df_mean = stock_trade_data.close.rolling(window=140).mean().fillna(0)
    mean_140_latest = df_mean.values[-1]
    # print(mean_140_latest)

    df_mean = stock_trade_data.close.rolling(window=180).mean().fillna(0)
    mean_180_latest = df_mean.values[-1]
    # print(mean_180_latest)

    # 存入字典
    mean_dict = {}
    mean_dict['10'] = mean_10_latest
    mean_dict['20'] = mean_20_latest
    mean_dict['30'] = mean_30_latest
    mean_dict['60'] = mean_60_latest
    mean_dict['88'] = mean_88_latest
    mean_dict['120'] = mean_120_latest
    mean_dict['140'] = mean_140_latest
    mean_dict['180'] = mean_180_latest
    return mean_dict


def plot_mean_line(code, latest_days):
    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'S' + code + '_daily'
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    stock_trade_data['trade_date'] = stock_trade_data['trade_date'].apply(lambda x: str(x))
    stock_trade_data.set_index("trade_date", inplace=True)

    latest_days = latest_days if len(stock_trade_data.close) > latest_days else len(stock_trade_data.close)
    start_days = len(stock_trade_data.close) - latest_days + 1
    stock_trade_data = stock_trade_data.iloc[start_days:len(stock_trade_data.close), :]

    # 绘制交易金额曲线
    stock_trade_data.loc[:, 'low'].plot.line()

    # 计算移动均线，根据收盘价
    df_mean = stock_trade_data.close.rolling(window=60).mean().fillna(0)
    # print(df_mean)
    df_mean.plot.line()

    df_mean = stock_trade_data.close.rolling(window=140).mean().fillna(0)
    # print(df_mean)
    df_mean.plot.line()
    #
    # df_mean = stock_trade_data.close.rolling(window=88).mean().fillna(0)
    # # print(df_mean)
    # df_mean.plot.line()
    #
    # df_mean = stock_trade_data.close.rolling(window=120).mean().fillna(0)
    # # print(df_mean)
    # df_mean.plot.line()
    #
    # df_mean = stock_trade_data.close.rolling(window=140).mean().fillna(0)
    # # print(df_mean)
    # df_mean.plot.line()

    # df_mean = stock_trade_data.close.rolling(window=180).mean().fillna(0)
    # # print(df_mean)
    # df_mean.plot.line()

    plt.show()


if __name__ == '__main__':
    mean_list = cal_mean_line('000001', 300)
    print(mean_list)
