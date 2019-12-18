# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np
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
def getProfit(year1):
    year2 = date.today().year
    mon2 = date.today().month
    if mon2 == 12:
        mon2 = 3
    else:
        mon2 = mon2 // 3
    df_profit = ts.get_profit_data(year1, 1).loc[:, ['code']]
    if year1 < year2:
        for year in range(year1, year2):
            for mon in range(4):
                df1 = ts.get_profit_data(year1, mon + 1).loc[:, ['code', 'name', 'net_profits']]
                df1.rename(columns={'net_profits': 'net_profits' + str(year) + str(mon + 1)}, inplace=True)
                print()
                print(df1.head())
                df_profile = df_profit.merge(df1)
        for mon in range(mon2):
            df1 = ts.get_profit_data(year2, mon+1).loc[:, ['code', 'name', 'net_profits']]
            df1.rename(columns={'net_profits': 'net_profits' + str(year2) + str(mon+1)}, inplace=True)
            print()
            print(df1.head())
            df_profile = df_profit.merge(df1)
        print(df_profit.head())
    else:
        for mon in range(mon2):
            df1 = ts.get_profit_data(year2, mon + 1).loc[:, ['code', 'name', 'net_profits']]
            df1.rename(columns={'net_profits': 'net_profits' + str(year2) + str(mon+1)}, inplace=True)
            print()
            print(df1.head())
            df_profile = df_profit.merge(df1)
        print(df_profit.head())


# getProfit(2018)


# df2=df[(df['net_profits181']>0)&(df['net_profits182']>0)&(df['net_profits183']>0)&(df['net_profits184']>0)&(df['net_profits191']>0)&(df['net_profits192']>0)&(df['net_profits193']>0)]
# print(df2)

# 计算利润增长率
def calProfitRatio(year1):
    # 计算仅几年的利润增长率
    ratio=[]
    year2 = date.today().year
    mon2 = date.today().month
    if mon2 == 12:
        mon2 = 3
    else:
        mon2 = mon2 // 3
    # 计算year1的四季度利润
    df_profit = ts.get_profit_data(year1, 1).loc[:, ['code']]
    for mon in range(4):
        df1 = ts.get_profit_data(year1, mon + 1).loc[:, ['code', 'name', 'net_profits']]
        df1.rename(columns={'net_profits': 'net_profits' + str(year1) + str(mon + 1)}, inplace=True)
        print()
        # print(df1.head())
        df_profit = df_profit.merge(df1)
    year1_profit=np.array(df_profit.values)
    # 计算利润增长率，按年依次筛选增长率为正的股票
    for year in range(year1+1,year2):
        for mon in range(4):
            df1 = ts.get_profit_data(year1, mon + 1).loc[:, ['code', 'name', 'net_profits']]
            df1.rename(columns={'net_profits': 'net_profits' + str(year1) + str(mon + 1)}, inplace=True)
            print()
            # print(df1.head())
            df_profit = df_profit.merge(df1)
        year2_profit=df_profit.iloc[:,4:8].values
        year_ratio=(year2_profit-year1_profit)/year1_profit
        print(year_ratio)


calProfitRatio(2017)