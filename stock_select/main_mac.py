# -*- coding: utf-8 -*-


from stock_select.selectByIncome import selectByIncome
from stock_select.selectByprofit import selectByProfit
from price_data.calHistPrice import calHistPriceofStock

stocksOfIncome = selectByIncome()
stocksOfProfit = selectByProfit()

stocks = set(stocksOfIncome).intersection(set(stocksOfProfit))

print("基本面较好的股票")
print(len(stocks))
# for s in stocks:
#     print(s)

for s in stocks:
    s = str(s)
    if not s.startswith('3'):
        price = calHistPriceofStock(s)
        # print(price)
        pct = (price[3] + price[2]) / price[1]
        if 0.2 < pct < 0.5:
            print(s)
