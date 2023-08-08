# -*- coding: utf-8 -*-
import sqlite3

import numpy as np
from sklearn.neighbors import KernelDensity

# 导出某股票的价格
# pandas连接数据库
import pandas as pd
import matplotlib.pyplot as plt

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

stock = '000001'
conn = sqlite3.connect(DB_PATH)
# 读取相应的交易数据表
table_name = 'S' + str(stock) + '_daily'
# 读取股票基本信息表
stock_trade_data = pd.read_sql('select * from ' + table_name + ' where trade_date>20220101', conn)
# print(stock_trade_data.head())
# stock_trade_data['close'].plot.bar()
# plt.show()
stock_price = stock_trade_data['close'].values
print(stock_price)


# 需要导入模块: from sklearn.neighbors import kde [as 别名]
# 或者: from sklearn.neighbors.kde import KernelDensity [as 别名]
def get_dist(data_list, method):
    Xnumpy = np.asarray(data_list)
    X = Xnumpy.reshape(-1, 1)
    dist = None
    if method == "raw":
        dist = data_list  # raw column data
    if method == "kd":
        kde = KernelDensity(
            kernel='gaussian', bandwidth=0.5
        ).fit(X)
        dist = kde.score_samples(X)
    return dist

dist=get_dist(stock_price,'kd')
print(dist)

plt.plot(stock_price)
plt.plot(dist)
plt.show()




