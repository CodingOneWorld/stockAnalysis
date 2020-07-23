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
profitData = pd.read_sql('select * from profitIn5years', conn)
print(profitData.head())

# 计算每年的收入增长幅度
# 计算每年的收入增长率
for i in range(4):
    # 收入增长幅度
    profitData['change' + str(i + 1)] = profitData['net_profits' + str(2015 + i + 1)] - profitData[
        'net_profits' + str(2015 + i)]
    # 收入增长率
    profitData['pct_change' + str(i + 1)] = (profitData['net_profits' + str(2015 + i + 1)] - profitData[
        'net_profits' + str(2015 + i)]) / profitData['net_profits' + str(2015 + i)]
print(profitData.head())

# 筛选近五年收入持续增长的股票
data = \
    profitData.loc[profitData['change1'] > 0].loc[profitData['change2'] > 0].loc[
        profitData['change3'] > 0].loc[
        profitData['change4'] > 0]
print(data.count())

data2 = \
    data.loc[data['pct_change4'] > data['pct_change3']].loc[data['pct_change3'] > data['pct_change2']].loc[
        data['pct_change2'] > data['pct_change1']]
print(data2)
