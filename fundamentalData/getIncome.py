# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
from datetime import date

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# 获取净利润数据
def getIncome(year1):
    year2=date.today().year
    mon2=date.today().month
    if mon2==12:
        mon2=3
    else:
        mon2 = mon2 // 3
    df_profile = ts.get_profit_data(year1, 1).loc[:, ['code']]
    if year1<year2:
        for year in range(year1, year2):
            for mon in range(4):
                df1 = ts.get_profit_data(year1, mon + 1).loc[:, ['code', 'name', 'business_income']]
                df1.rename(columns={'business_income': 'business_income' + str(year) + str(mon + 1)}, inplace=True)
                print()
                print(df1.head())
                df_profile = df_profile.merge(df1)
        for mon in range(mon2):
            df1 = ts.get_profit_data(year2, mon2).loc[:, ['code', 'name', 'business_income']]
            df1.rename(columns={'business_income': 'business_income' + str(year2) + str(mon2)}, inplace=True)
            print()
            print(df1.head())
            df_profile = df_profile.merge(df1)
        print(df_profile.head())
    else:
        for mon in range(mon2):
            df1 = ts.get_profit_data(year2, mon+1).loc[:, ['code', 'name', 'business_income']]
            df1.rename(columns={'business_income': 'business_income' + str(year2) + str(mon+1)}, inplace=True)
            print()
            print(df1.head())
            df_profile = df_profile.merge(df1)
        print(df_profile.head())



getIncome(2018)