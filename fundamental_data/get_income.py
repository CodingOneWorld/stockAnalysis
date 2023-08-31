# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
from datetime import date
import sqlite3

from analysis_util.cal_stock_trend import cal_trend_common
from util.utils_common import code2ts_code, get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

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
def query_income_since(year1):
    year2 = date.today().year - 1

    # ts_code转化 code2ts_code(x)
    # 获取第一年的收入数据，只获取股票名称
    df_income = ts.get_profit_data(year1, 4).loc[:, ['code', 'name']]
    # df_Income['code'] = df_Income['code'].apply(lambda x: str(x))
    df_income['ts_code'] = df_income['code'].apply(lambda x: code2ts_code(x))

    for year in range(year1, year2):
        df1 = ts.get_profit_data(year, 4).loc[:, ['code', 'name', 'business_income']]
        # df1['code'] = df1['code'].apply(lambda x: str(x).split('.')[0])
        df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
        df1.rename(columns={'business_income': 'income_' + str(year)}, inplace=True)
        # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
        df_income = df_income.merge(df1, how="outer")
        # df_profile.drop_duplicates()
        print()
        print(df_income.head())
        df_income.drop_duplicates(['name'], inplace=True)

    # 最后一年数据可能不全，单独处理并做外连接
    df1 = ts.get_profit_data(year2, 4).loc[:, ['code', 'name', 'business_income']]
    df1['code'] = df1['code'].apply(lambda x: str(x))
    df1['ts_code'] = df1['code'].apply(lambda x: code2ts_code(x))
    df1.rename(columns={'business_income': 'income_' + str(year2)}, inplace=True)
    # df1.rename(columns={'net_profits': 'net_profits' + str(year)}, inplace=True)
    df_income = df_income.merge(df1, how="outer")
    df_income.drop_duplicates(['name'], inplace=True)

    # 缺失值处理，参考同一行中NaN前面的值来填充，其他再填充0
    df_income = df_income.fillna(method="backfill", axis=1)
    # df_income = df_income.fillna(method='pad', axis = 1)
    df_income = df_income.fillna(0)
    print(df_income[['code', 'name']])
    return df_income


# 获取最近n年收入数据  latest_years=n
def get_income_latest_years_online(latest_years):
    year2 = date.today().year - 1
    year1 = year2 - latest_years
    df_income = query_income_since(year1)
    return df_income


# 获取所有股票的全部历史收入信息,并写入数据库
def income_of_all_stocks2db():
    # 获取股票列表及其上市时间
    # pandas连接数据库
    year = 1989
    print(year)
    df_income = query_income_since(year)
    print(df_income)
    print(df_income.count())

    # 连接sqlite数据库
    conn = sqlite3.connect(DB_PATH)
    print("Open database successfully")
    df_income.to_sql('income_all_stocks', con=conn, if_exists='replace', index=False)
    print("insert database successfully")


def get_income_of_latest_years(code, latest_years):
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    stock_income_data = pd.read_sql('select * from income_all_stocks', conn)
    print(stock_income_data.columns)
    # 判断需要查的股票代码是否在数据库中
    stock_income_list = stock_income_data['code'].values
    if stock_income_list.__contains__(code):
        return stock_income_data[stock_income_data['code'] == code].iloc[:, -latest_years:].values[0]
        # print(income_data)
    else:
        return [0]


if __name__ == '__main__':
    # income_of_all_stocks2db()

    # get_income_latest_years_online(5)
    income = get_income_of_latest_years('002714', 5)
    print(income)

    # income_data = get_income_of_latest_years('002210', 6)
    # print(income_data)
    k = cal_trend_common(income)
    print(k)
    #
    # df_Income = ts.get_profit_data(2015, 4).loc[:, ['code', 'name', 'business_income']]
    # df = df_Income[df_Income['name']=='兆易创新']
    # print(df)

    # data = query_income_since(2019)
    # print(data)
    # data2 = data[data['code'] == '001207']
    # print(data2)
