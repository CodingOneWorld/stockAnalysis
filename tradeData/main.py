# -*- coding: utf-8 -*-

from tradeData.updateDailyData_tspro import updateDailyData_tspro
from tradeData.getStockBasicList import getStockBasicList

# 参数
update_date = "20191128"

# db path
filepath = 'P:/Money/stocks.db'

updateDailyData_tspro(update_date,filepath)
getStockBasicList()