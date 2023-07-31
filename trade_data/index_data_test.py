# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


# 获取指数基本信息
pro = ts.pro_api()
df = pro.index_basic(market='SW')
# market 枚举
# 0        OTH
# 1        SSE
# 167      CSI
# 445     CICC
# 507     MSCI
# 2206    SZSE
# 2647     CNI
# 4125      SW
# 6136      NH
print(df)

df = pro.index_daily(ts_code='399300.SZ')
print(df)
