# -*- coding: utf-8 -*-
from analysis_util.plot_util import plot_stock_price_line
from price_data.cal_hist_price import cal_hist_price_of_stock


# 计算股票当前价格在最低价到最高价的那个百分比位置
def cal_price_pct(stock):
    price = cal_hist_price_of_stock(stock)
    # print(price)
    pct = (price[3] - price[2]) / (price[1] - price[2])
    return pct
