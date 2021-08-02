# -*- coding: utf-8 -*-
from price_data.calHistPrice import calHistPriceofStock


def cal_low_price_stock(stock):
    price = calHistPriceofStock(stock)
    # print(price)
    pct = (price[3] + price[2]) / price[1]
    if 0.2 < pct < 0.5:
        print(stock)