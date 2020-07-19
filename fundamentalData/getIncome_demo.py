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


# 获取收入数据

# 获取最近5年的年收入数据
def getIncomeOf5Year():
    year2 = date.today().year - 1
    year1 = year2 - 4

    # 获取第一年的收入数据
    df_profile = ts.get_profit_data(year1, 1).loc[:, ['code', 'name']]
    df_profile['business_income_' + str(year1)]=0
    for mon in range(4):
        df1 = ts.get_profit_data(year1, mon + 1).loc[:, ['code', 'name', 'business_income']]
        df1.rename(columns={'business_income': 'business_income' + str(mon+1)}, inplace=True)
        print()
        print(df_profile.head())
        df_profile = df_profile.merge(df1)
        df_profile['business_income_' + str(year1)] += df_profile['business_income' + str(mon+1)]
    df_profile=df_profile.drop_duplicates()
    print(df_profile.head())


getIncomeOf5Year()
