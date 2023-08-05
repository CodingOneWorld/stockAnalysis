# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime

import time
import os
import sqlite3

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)

with open('last_datetime.txt', 'r') as file:
    dtime=datetime.datetime.strptime(file.readlines()[0], "%Y-%m-%d %H:%M:%S")

print(dtime)
dtime2 = datetime.datetime.now()

print((dtime2-dtime).seconds/3600)

with open('last_datetime.txt', 'w') as file:
    file.write(dtime.strftime('%Y-%m-%d %H:%M:%S'))
file.close()


