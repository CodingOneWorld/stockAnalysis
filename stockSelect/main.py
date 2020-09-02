# -*- coding: utf-8 -*-


from stockSelect.selectByIncome import selectByIncome
from stockSelect.selectByprofit import selectByProfit

stocksOfIncome = selectByIncome()
stocksOfProfit = selectByProfit()

stocks = set(stocksOfIncome).intersection(set(stocksOfProfit))

print(len(stocks))

for s in stocks:
    print(s)
