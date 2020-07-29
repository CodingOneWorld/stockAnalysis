# -*- coding: utf-8 -*-


from stockSelectByFundamental.selectByIncome import selectByIncome
from stockSelectByFundamental.selectByprofit import selectByProfit

stocksOfIncome = selectByIncome()
stocksOfProfit = selectByProfit()

stocks = set(stocksOfIncome).intersection(set(stocksOfProfit))

print(stocks.__len__())

for s in stocks:
    print(s)
