import datetime

import numpy as np
import pandas as pd

from trade_data.get_trade_data import get_stock_trade_data
from util.date_util import date_add, get_today_date

'''
检测的买入点做效果追踪，追踪第二天的涨跌情况，做统计
当天是date,判断date-1天的结果的涨跌情况
'''


if __name__ == '__main__':
    today = get_today_date()
    today_1=date_add(today,-1)




