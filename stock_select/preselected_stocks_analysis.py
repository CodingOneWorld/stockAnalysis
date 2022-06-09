# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# 对预筛选出的股票池中的股票做分析
from stock_select.get_low_price_stock import cal_price_pct

df=pd.read_csv('stock_pool.txt',delimiter=',',dtype={'symbol': np.str})
print(df.head())
stock_list=df.values

# 价格分析
def price_analysis():
    stock_01 = []
    stock_12 = []
    stock_23 = []
    stock_34 = []
    stock_45 = []
    stock_56 = []
    stock_67 = []
    stock_78 = []
    stock_89 = []
    stock_910 = []
    for stock in stock_list:
        print(stock)
        # 0.1-0.2
        pct = cal_price_pct(stock[0])
        if 0 < pct <= 0.1:
            stock_01.append(stock)
        if 0.1 < pct <= 0.2:
            stock_12.append(stock)
        if 0.2 < pct <= 0.3:
            stock_23.append(stock)
        if 0.3 < pct <= 0.4:
            stock_34.append(stock)
        if 0.4 < pct <= 0.5:
            stock_45.append(stock)
        if 0.5 < pct <= 0.6:
            stock_56.append(stock)
        if 0.6 < pct <= 0.7:
            stock_67.append(stock)
        if 0.7 < pct <= 0.8:
            stock_78.append(stock)
        if 0.8 < pct <= 0.9:
            stock_89.append(stock)
        if 0.9 < pct <= 1:
            stock_910.append(stock)

    stock_01 = pd.DataFrame(stock_01, columns=['symbol', 'stock_name'])
    stock_12 = pd.DataFrame(stock_12, columns=['symbol', 'stock_name'])
    stock_23 = pd.DataFrame(stock_23, columns=['symbol', 'stock_name'])
    stock_34 = pd.DataFrame(stock_34, columns=['symbol', 'stock_name'])
    stock_45 = pd.DataFrame(stock_45, columns=['symbol', 'stock_name'])
    stock_56 = pd.DataFrame(stock_56, columns=['symbol', 'stock_name'])
    stock_67 = pd.DataFrame(stock_67, columns=['symbol', 'stock_name'])
    stock_78 = pd.DataFrame(stock_78, columns=['symbol', 'stock_name'])
    stock_89 = pd.DataFrame(stock_89, columns=['symbol', 'stock_name'])
    stock_910 = pd.DataFrame(stock_910, columns=['symbol', 'stock_name'])

    stock_01.to_csv('./price/stock_01.txt', index=0)
    stock_12.to_csv('./price/stock_12.txt', index=0)
    stock_23.to_csv('./price/stock_23.txt', index=0)
    stock_34.to_csv('./price/stock_34.txt', index=0)
    stock_45.to_csv('./price/stock_45.txt', index=0)
    stock_56.to_csv('./price/stock_56.txt', index=0)
    stock_67.to_csv('./price/stock_67.txt', index=0)
    stock_78.to_csv('./price/stock_78.txt', index=0)
    stock_89.to_csv('./price/stock_89.txt', index=0)
    stock_910.to_csv('./price/stock_910.txt', index=0)


# 基本面分析