# -*- coding: utf-8 -*-


from stock_select.select_by_income import select_by_income
from stock_select.select_by_profit import select_by_profit
from price_data.cal_hist_price import cal_hist_price_of_stock

stocksOfIncome = select_by_income()
stocksOfProfit = select_by_profit()

stocks = set(stocksOfIncome).intersection(set(stocksOfProfit))

print("基本面较好的股票")
print(len(stocks))
# for s in stocks:
#     print(s)

for s in stocks:
    s = str(s)
    if not s.startswith('3'):
        price = cal_hist_price_of_stock(s)
        # print(price)
        pct = (price[3] + price[2]) / price[1]
        if 0.2 < pct < 0.5:
            print(s)
