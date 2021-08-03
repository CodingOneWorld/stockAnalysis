# -*- coding: utf-8 -*-
from price_data.cal_hist_price import cal_hist_price_of_stock


def cal_low_price_stock(stock):
    price = cal_hist_price_of_stock(stock)
    # print(price)
    pct = (price[3] + price[2]) / price[1]
    if 0.2 < pct < 0.5:
        print(stock)