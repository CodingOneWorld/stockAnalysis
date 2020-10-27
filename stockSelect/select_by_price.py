# -*- coding: utf-8 -*-

from priceData.calHistPrice import calHistPriceofAllStocks
from fundamentalData.get_ST_stocks import get_ST_stocks

if __name__ == '__main__':
    stock_price_df = calHistPriceofAllStocks()
    stock_price_df['position'] = stock_price_df['current_price'] / (
            stock_price_df['max_price'] - stock_price_df['min_price'])
    low_price_stock = stock_price_df[stock_price_df['position'] < 0.1]
    print(low_price_stock.head())
    low_price_stock = list(low_price_stock['code'])
    set_low_price_stock = set(low_price_stock)
    print(set_low_price_stock)
    ST_sets = set(get_ST_stocks())
    low_price_stock = set_low_price_stock.difference(ST_sets)
    print(low_price_stock)
