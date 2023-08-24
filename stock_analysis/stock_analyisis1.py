# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tushare as ts
import sqlite3

from analysis_util.cal_stock_trend import get_stock_price
from analysis_util.plot_util import plot_price_line_latestdays
from trade_data.get_stock_basic_list import get_stock_basic_list
from util.utils_common import get_dbpath_by_repo

# 找出最近一年翻倍的股票，分析他们的走势

DB_PATH = get_dbpath_by_repo()

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

if __name__ == '__main__':
    # 股票列表
    # 股票列表
    # stock_basic = get_stock_basic_list('DB')
    # # 不看最近一年上市的股票
    # stock_basic = stock_basic[stock_basic['list_date'] <= '20220701']
    # stock_list = stock_basic[['symbol', 'name']].values

    file = '../selected_stock_analysis/自选股.csv'
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    # df['symbol']=df['symbol'].astype('string')
    stock_list = df.values
    print(stock_list)

    for l in stock_list:
    # for l in [['000002', '万科A']]:
        code = l[0]
        # 计算最近一年的最低价和最高价
        stock_price = list(get_stock_price(code, 'close')['close'].values[-200:])
        # print(stock_price)
        # plot_price_line_latestdays(code,200)
        min_p = np.min(stock_price)
        index_min = stock_price.index(min_p)
        # print(index_min)
        # print(min_p)
        max_p = max(stock_price)
        index_max = stock_price.index(max_p)
        # print(index_max)
        # print(max_p)
        if index_max > index_min and max_p / min_p > 2:
            print('符合条件：',l)
