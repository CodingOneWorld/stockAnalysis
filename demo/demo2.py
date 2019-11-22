# -*- coding: utf-8 -*-

import tushare as ts


# 查询股票的基本信息数据-tushare
data = ts.get_stock_basics()
stocks_ts=set(data.index)
for s in stocks_ts:
    if s.startswith('0') or s.startswith('3'):
        s=s+".SZ"
        print(s)
    else:
        s=s+".SH"
print(stocks_ts)