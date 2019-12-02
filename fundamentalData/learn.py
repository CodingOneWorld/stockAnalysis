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

# 业绩报告
# code,代码
# name,名称
# esp,每股收益
# eps_yoy,每股收益同比(%)
# bvps,每股净资产
# roe,净资产收益率(%)
# epcf,每股现金流量(元)
# net_profits,净利润(万元)
# profits_yoy,净利润同比(%)
# distrib,分配方案
# report_date,发布日期
df=ts.get_report_data(2019,3)

# 盈利能力
# code,代码
# name,名称
# roe,净资产收益率(%)
# net_profit_ratio,净利率(%)
# gross_profit_rate,毛利率(%)
# net_profits,净利润(百万元)
# esp,每股收益
# business_income,营业收入(百万元)
# bips,每股主营业务收入(元)
# df=ts.get_profit_data(2019,3)

# 成长能力
# code,代码
# name,名称
# mbrg,主营业务收入增长率(%)
# nprg,净利润增长率(%)
# nav,净资产增长率
# targ,总资产增长率
# epsg,每股收益增长率
# seg,股东权益增长率
# df=ts.get_growth_data(2019,3)
print()
print(df.head())