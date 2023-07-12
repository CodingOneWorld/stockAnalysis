# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

from constants.common_constants import DB_PATH
from trade_data.get_stock_basic_list import get_stock_basic_list


def get_stock_name(stock_code,mode='file'):
    if mode == 'file':
        stock_list_data=get_stock_basic_list('file')
    elif mode=='DB':
        stock_list_data=get_stock_basic_list('DB')
    return stock_list_data[stock_list_data['symbol']==stock_code]['name'].values[0]


def get_stock_code(stock_name,mode='file'):
    if mode == 'file':
        stock_list_data=get_stock_basic_list('file')
    elif mode == 'DB':
        stock_list_data = get_stock_basic_list('DB')
    return stock_list_data[stock_list_data['name']==stock_name]['symbol'].values[0]


if __name__ == '__main__':
    print(get_stock_code('福耀玻璃'))
