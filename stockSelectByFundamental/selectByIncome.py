# -*- coding: utf-8 -*-

import pandas as pd
import tushare as ts
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

filepath = 'E:/Money/stocks.db'

# pandas连接数据库
conn = sqlite3.connect(filepath)
incomeData = pd.read_sql('select * from incomeIn5years', conn)
print(incomeData.head())
