# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np
from datetime import date
import sqlite3


# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


# 获取最近5年的年收入数据
def getIncomeOf5Year(filepath):
    year2 = date.today().year - 1
    year1 = year2 - 4

    # ts_code转化
    def code2ts_code(s):
        if s.startswith('0') or s.startswith('3'):
            return s + ".SZ"
        else:
            return s + ".SH"

    # 获取第一年的收入数据
    df_profile = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    df_profile['ts_code'] = df_profile['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2 + 1):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'net_profits']]
        # df1.rename(columns={'business_income': 'business_income' + str(year)}, inplace=True)
        df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_profile = df_profile.merge(df1)
        print()
        print(df_profile.head())
    df_profile.drop_duplicates()
    print(df_profile.head())

    # 连接sqlite数据库
    conn = sqlite3.connect(filepath)
    print("Open database successfully")
    df_profile.to_sql('profitIn5years', con=conn, if_exists='append', index=False)
    print("insert database successfully")


filepath = 'E:/Money/stocks.db'
getIncomeOf5Year(filepath)