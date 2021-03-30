# 利用tushare金融数据接口包

import tushare as ts
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

# 获取股票列表
data = ts.get_stock_basics()
print(data)

## 获取历史数据
# 参数说明：
# • code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
# • start：开始日期，格式YYYY-MM-DD
# • end：结束日期，格式YYYY-MM-DD
# • ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
# • retry_count：当网络异常后重试次数，默认为3
# • pause:重试时停顿秒数，默认为0
# 返回值说明：
# • date：日期
# • open：开盘价
# • high：最高价
# • close：收盘价
# • low：最低价
# • volume：成交量
# • price_change：价格变动
# • p_change：涨跌幅
# • ma5：5日均价
# • ma10：10日均价
# • ma20:20日均价
# • v_ma5:5日均量
# • v_ma10:10日均量
# • v_ma20:20日均量
# • turnover:换手率[注：指数无此项]
# 使用该接口并不能获取股票自上市以来的所有日线数据
data = ts.get_hist_data('300032')
print(data)
# print(data.info())
# data['close'].plot.bar()
# plt.show()

# 另外一个函数get_h_data用于获取股票历史数据 ##h好像已经不能用了
# 在不指定开始时间和结束时间时，该函数默认返回最近一年的日线数据，
# 返回值说明
# 开盘价（open）
# 最高价（high）
# 收盘价（close）
# 最低价（low）
# 成交量（volume）
# 成交金额（amount）
# data=ts.get_h_data('300032',start='2011-01-01',end='2011-05-01')
# print(data)

# 第三个获取K线数据的函数，get_k_data
# data=ts.get_k_data('300032')
# print(data)
# data['close'].plot(kind='line')
# plt.show()

##获取今日数据
# 获取实时行情数据get_today_all()
# 返回值说明：
# • code：代码
# • name:名称
# • changepercent:涨跌幅
# • trade:现价
# • open:开盘价
# • high:最高价
# • low:最低价
# • settlement:昨日收盘价
# • volume:成交量
# • turnoverratio:换手率
# • amount:成交量
# • per:市盈率
# • pb:市净率
# • mktcap:总市值
# • nmc:流通市值
# 该函数没有参数，直接调用即可
# data=ts.get_today_all()
# print(data)
