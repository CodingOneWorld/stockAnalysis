# -*- coding: utf-8 -*-

from priceData.calHistPrice import calHistPriceofAllStocks

if __name__ == '__main__':
    stock_price_df=calHistPriceofAllStocks()
    stock_price_df['position']=stock_price_df['current_price']/(stock_price_df['max_price']-stock_price_df['min_price'])
    low_price_stock=stock_price_df[stock_price_df['position']<0.1]
    print(low_price_stock)