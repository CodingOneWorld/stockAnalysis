# -*- coding: utf-8 -*-

# 判断股票的关键价位
# 如支撑位，压力位，均线位置等
# 计算当前价格最高值，最低值，以及均线数据，进行比较
from analysis_util.cal_mean_line import cal_mean_line
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend

if __name__ == '__main__':
    # 计算股票趋势
    k=cal_stock_price_trend('000001',3)
    print(k)

    # 获取股票最近的价格，并与均线价格比较
    stock_price=0
    if k>0:
        stock_price = get_stock_price('000001', 'high')[-1]
        print(stock_price)

    elif k<0:
        stock_price = get_stock_price('000001', 'low')[-1]
        print(stock_price)

    # 计算均线值
    mean_list = cal_mean_line('000001', 3000)
    print(mean_list)

    #












