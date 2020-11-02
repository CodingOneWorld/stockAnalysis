# -*- coding: utf-8 -*-

from tradeData.updateDailyData_tspro import updateDailyData_tspro
from tradeData.getStockBasicList import getStockBasicList

# 参数
update_date = "20201102"

# db path
filepath = 'E:/Money/stocks.db'

updateDailyData_tspro(update_date, filepath, 197, 0, 0)


