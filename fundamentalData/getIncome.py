# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
from datetime import date
import sqlite3

from contants.commonContants import DB_PATH
from util.utilsCommon import code2ts_code

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


# 获取收入数据
# 获取某年到现在的年收入数据
def getIncomeSince(year1):
    year2 = date.today().year - 1

    # ts_code转化 code2ts_code(x)
    # 获取第一年的收入数据
    df_Income = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    df_Income['ts_code'] = df_Income['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2+1):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'business_income']]
        df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
        df1.rename(columns={'business_income': 'business_income' + str(year)}, inplace=True)
        # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_Income = df_Income.merge(df1, how="outer")
        # df_profile.drop_duplicates()
        print()
        print(df_Income.head())
        df_Income.drop_duplicates()
    df_Income = df_Income.fillna(method="backfill", axis=1)
    df_Income = df_Income.fillna(method="pad", axis=1)
    df_Income = df_Income.drop_duplicates(['code'])
    print(df_Income)
    return df_Income


# getIncomeSince(2016)


# 获取最近5年的年收入数据
def getIncomeOf5Year(filepath):
    year2 = date.today().year - 1
    year1 = year2 - 4

    # ts_code转化 code2ts_code(x)
    # 获取第一年的收入数据
    df_Income = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    df_Income['ts_code'] = df_Income['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2 + 1):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'business_income']]
        df1.rename(columns={'business_income': 'business_income' + str(year)}, inplace=True)
        # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_Income = df_Income.merge(df1)
        df_Income.drop_duplicates()
        print()
        print(df_Income.head())

    df_Income.drop_duplicates()
    print(df_Income.head())

    # 连接sqlite数据库
    conn = sqlite3.connect(filepath)
    print("Open database successfully")
    df_Income.to_sql('incomeIn5years', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# 获取所有股票的全部历史收入信息
def getIncomeofALLStocks():
    # 获取股票列表及其上市时间
    # pandas连接数据库
    year = 1989
    print(year)
    df_Income = getIncomeSince(year)

    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    print("Open database successfully")
    df_Income.to_sql('incomeSince1989', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# getIncomeOf5Year(filepath)
getIncomeofALLStocks()

# df_Income = ts.get_profit_data(2019, 4).loc[:, ['code', 'name']]
# print(df_Income.shape)