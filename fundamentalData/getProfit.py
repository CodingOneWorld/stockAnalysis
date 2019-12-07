# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


#

df1 = ts.get_profit_data(2018, 1).loc[:,['code', 'name', 'net_profits']]
df1.rename(columns={'net_profits':'net_profits181'},inplace = True)

df2 = ts.get_profit_data(2018, 2).loc[:,['code', 'name', 'net_profits']]
df2.rename(columns={'net_profits':'net_profits182'},inplace = True)

df3 = ts.get_profit_data(2018, 3).loc[:,['code', 'name', 'net_profits']]
df3.rename(columns={'net_profits':'net_profits183'},inplace = True)

df4 = ts.get_profit_data(2018, 4).loc[:,['code', 'name', 'net_profits']]
df4.rename(columns={'net_profits':'net_profits184'},inplace = True)

df5 = ts.get_profit_data(2019, 1).loc[:,['code', 'name', 'net_profits']]
df5.rename(columns={'net_profits':'net_profits191'},inplace = True)

df6 = ts.get_profit_data(2019, 2).loc[:,['code', 'name', 'net_profits']]
df6.rename(columns={'net_profits':'net_profits192'},inplace = True)

df7 = ts.get_profit_data(2019, 3).loc[:,['code', 'name', 'net_profits']]
df7.rename(columns={'net_profits':'net_profits193'},inplace = True)

df=pd.merge(df1,df2).merge(df3).merge(df4).merge(df5).merge(df6).merge(df7)
print()
print(df.head())

df2=df[df['net_profits181']>0&df['net_profits182']>0&df['net_profits183']>0&df['net_profits184']>0&df['net_profits191']>0&df['net_profits192']>0&df['net_profits193']>0]
print(df2)