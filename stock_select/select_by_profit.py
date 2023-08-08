# -*- coding: utf-8 -*-

import pandas as pd
import tushare as ts
import sqlite3

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


def select_by_profit():
    # pandas连接数据库
    conn = sqlite3.connect(DB_PATH)
    profitData = pd.read_sql('select * from profit_all_stocks', conn)
    # print(profitData.head())

    # 计算每年的收入增长幅度
    # 计算每年的收入增长率
    for i in range(4):
        # 净利润增长幅度
        profitData['change' + str(i + 1)] = profitData['profits_' + str(2017 + i + 1)] - profitData[
            'profits_' + str(2017 + i)]
        # 净利润增长率
        profitData['pct_change' + str(i + 1)] = (profitData['profits_' + str(2017 + i + 1)] - profitData[
            'profits_' + str(2017 + i)]) / profitData['profits_' + str(2017 + i)]
    # print(profitData.head())

    # 筛选近五年净利润持续增长的股票
    data = \
        profitData.loc[profitData['change1'] > 0].loc[profitData['change2'] > 0].loc[
            profitData['change3'] > 0].loc[
            profitData['change4'] > 0]
    # print(data.count())
    # # 筛选5年净利润增长率持续增长的股票
    # data2 = \
    #     data.loc[data['pct_change4'] > data['pct_change3']].loc[data['pct_change3'] > data['pct_change2']].loc[
    #         data['pct_change2'] > data['pct_change1']]
    # 筛选5年净利润增长一直大于9%的股票
    data2 = \
        data.loc[data['pct_change4'] >= 0.1].loc[data['pct_change3'] >= 0.1].loc[
            data['pct_change2'] >= 0.1].loc[data['pct_change1'] >= 0.1]
    print(data2[['code','name','profits_2017','profits_2018','profits_2019','profits_2020','profits_2021']].reset_index(drop=True))
    data2[['code', 'name', 'profits_2017', 'profits_2018', 'profits_2019', 'profits_2020', 'profits_2021']].reset_index(
        drop=True).to_csv('select_by_profits.csv',index=0)
    return data2['code'].values


stocks = select_by_profit()
print(stocks)
# print(len(stocks))



