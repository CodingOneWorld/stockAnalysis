# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np
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


# 获取某年到现在的年净利润数据
def getProfitSince(year1):
    year2 = date.today().year - 1

    # ts_code转化 code2ts_code(x)
    # 获取第一年的收入数据
    df_profit = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    df_profit['ts_code'] = df_profit['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'net_profits']]
        df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
        df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_profit = df_profit.merge(df1, how="right")
        # df_profile.drop_duplicates()
        print()
        print(df_profit.head())
        df_profit.drop_duplicates(['name'], inplace=True)

    # 最后一年数据可能不全，单独处理并做外连接
    df1 = ts.get_profit_data(year2, 4).loc[:, ['code', 'name', 'net_profits']]
    # df1['code'] = df1['code'].apply(lambda x: str(x))
    df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
    df1.rename(columns={'net_profits': 'net_profits' + str(year2)}, inplace=True)
    # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
    df_profit = df_profit.merge(df1, how="outer")
    df_profit.drop_duplicates(['name'], inplace=True)

    # 缺失值处理，先向后填充，再填充0
    df_profit = df_profit.fillna(method="backfill", axis=1)
    df_profit = df_profit.fillna(0)
    print(df_profit[['code', 'name']])
    return df_profit


# 获取最近5年的年收入数据
def getProfitOf5Year(filepath):
    year2 = date.today().year - 1
    year1 = year2 - 4

    # 获取第一年的收入数据
    df_profit = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    df_profit['ts_code'] = df_profit['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2 + 1):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'net_profits']]
        # df1.rename(columns={'business_income': 'business_income' + str(year)}, inplace=True)
        df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_profit = df_profit.merge(df1)
        print()
        print(df_profit.head())
    df_profit.drop_duplicates()
    print(df_profit.head())

    # 连接sqlite数据库
    conn = sqlite3.connect(filepath)
    print("Open database successfully")
    df_profit.to_sql('profitIn5years', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# 获取所有股票的全部历史净利润信息
def getProfitofALLStocks():
    # 获取股票列表及其上市时间
    # pandas连接数据库
    year = 1989
    print(year)
    df_profit = getProfitSince(year)

    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    print("Open database successfully")
    df_profit.to_sql('profit_since1989', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


# getProfitOf5Year(filepath)
getProfitofALLStocks()
