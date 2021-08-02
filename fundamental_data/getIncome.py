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
pd.set_option('max_colwidth', 1000)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)
# 设置显示宽度为1000，避免其换行
pd.set_option('display.width', 1000)


# 获取收入数据
# 获取某年到现在的年收入数据
def queryIncomeSince(year1):
    year2 = date.today().year - 1

    # ts_code转化 code2ts_code(x)
    # 获取第一年的收入数据，只获取股票名称
    df_Income = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    # df_Income['code'] = df_Income['code'].apply(lambda x: str(x))
    df_Income['ts_code'] = df_Income['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'business_income']]
        # df1['code'] = df1['code'].apply(lambda x: str(x).split('.')[0])
        df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
        df1.rename(columns={'business_income': 'business_income' + str(year)}, inplace=True)
        # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_Income = df_Income.merge(df1, how="right")
        # df_profile.drop_duplicates()
        print()
        print(df_Income.head())
        df_Income.drop_duplicates(['name'], inplace=True)

    # 最后一年数据可能不全，单独处理并做外连接
    df1 = ts.get_profit_data(year2, 4).loc[:, ['code', 'name', 'business_income']]
    # df1['code'] = df1['code'].apply(lambda x: str(x))
    df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
    df1.rename(columns={'business_income': 'business_income' + str(year2)}, inplace=True)
    # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
    df_Income = df_Income.merge(df1, how="outer")
    df_Income.drop_duplicates(['name'], inplace=True)

    # 缺失值处理，先向后填充，再填充0
    df_Income = df_Income.fillna(method="backfill", axis=1)
    df_Income = df_Income.fillna(0)
    print(df_Income[['code', 'name']])
    return df_Income


# 获取所有股票的全部历史收入信息,并写入数据库
def IncomeofALLStocks2sql():
    # 获取股票列表及其上市时间
    # pandas连接数据库
    year = 1989
    print(year)
    df_Income = queryIncomeSince(year)

    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    print("Open database successfully")
    df_Income.to_sql('income_all_stocks', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# getIncomeOf5Year(filepath)
IncomeofALLStocks2sql()

# df_Income = ts.get_profit_data(2019, 4).loc[:, ['code', 'name', 'business_income']]
# df=df_Income[['code','name']]
# print(df)
