# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


filepath="E:/Money/stocks.db"

if __name__ == '__main__':
    # pandas连接数据库
    conn = sqlite3.connect(filepath)
    # 读取相应的交易数据表
    table_name = 'S000001_daily'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    stock_trade_data['close'].plot.line()
    plt.show()
