# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from contants.commonContants import DB_PATH

if __name__ == '__main__':
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    # 读取相应的交易数据表
    table_name = 'incomeSince1989'
    # 读取股票基本信息表
    stock_trade_data = pd.read_sql('select * from ' + table_name, conn)
    print(stock_trade_data.head())
    # stock_trade_data=stock_trade_data[stock_trade_data['trade_date']>20191215]
    print(stock_trade_data[stock_trade_data['name'] == '平安银行'].iloc[:,3:stock_trade_data.shape[1]]).plot.line()
    # stock_trade_data[stock_trade_data['name'] == '平安银行'].iloc[:,[2,stock_trade_data.shape(1)]].plot.line()
    plt.show()
