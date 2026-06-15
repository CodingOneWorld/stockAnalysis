# -*- coding: utf-8 -*-

# 获取所有正常上市的股票列表
# 数据源：AKShare（主力） + Tushare（备用）

import pandas as pd
import numpy as np
import time
import sqlite3

from util.utils_common import get_dbpath_by_repo
from trade_data.data_source import get_stock_list

DB_PATH = get_dbpath_by_repo()

# 显示所有行(参数设置为None代表显示所有行，也可以自行设置数字)
pd.set_option('display.max_columns', None)
# 显示所有列
pd.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pd.set_option('max_colwidth', 200)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pd.set_option('expand_frame_repr', False)


def get_stock_basic_list(source='DB'):
    """
    获取股票基础列表（去除创业板300、科创板688）。
    source='DB'  : 从数据库读取
    source='file': 从 stock_list.csv 读取
    """
    if source == 'file':
        stock_basic = pd.read_csv('stock_list.csv', dtype={'symbol': np.str_}, delimiter=',')
    elif source == 'DB':
        conn = sqlite3.connect(DB_PATH)
        stock_basic = pd.read_sql('select * from stock_list', conn)
        conn.close()
    else:
        raise ValueError(f'未知 source 参数: {source}')

    # 去除创业板（300/301开头）、科创板（688开头）、北交所（920）
    mask = (
        (~stock_basic.symbol.str.startswith('3')) &
        (~stock_basic.symbol.str.startswith('688'))&
        (~stock_basic.symbol.str.startswith('920'))
    )
    stock_basic = stock_basic[mask]
    return stock_basic


def get_stock_basic_list_2DB(source='DB'):
    """
    获取股票列表并写入数据库。
    source='DB'     : 直接从数据库读取（不请求网络）
    source='online' : 从 AKShare/Tushare 拉取最新列表并写库
    返回：去除了创业板、科创板、北交所的股票列表 DataFrame
    """
    conn = sqlite3.connect(DB_PATH)

    if source == 'DB':
        stock_basic = pd.read_sql('select * from stock_list', conn)
    else:
        # 调用双数据源获取最新股票列表
        stock_basic = get_stock_list()
        # 写入数据库
        stock_basic.to_sql('stock_list', con=conn, if_exists='replace', index=False)
        print(f'[股票列表] 已写入数据库，共 {len(stock_basic)} 条')

    conn.close()

    # 过滤：只保留上市日期早于今天的（list_date 可能为空，兼容处理）
    localdate = time.strftime('%Y%m%d', time.localtime())
    if 'list_date' in stock_basic.columns:
        stock_basic = stock_basic[
            stock_basic['list_date'].isna() |
            (stock_basic['list_date'] == '') |
            (stock_basic['list_date'] < localdate)
        ]

    # 去除创业板（300/301开头）、科创板（688开头）、北交所（BJ）
    mask = (
        (~stock_basic.symbol.str.startswith('3')) &
        (~stock_basic.symbol.str.startswith('688'))&
        (~stock_basic.symbol.str.startswith('920'))
    )
    if 'ts_code' in stock_basic.columns:
        mask = mask & (~stock_basic.ts_code.str.contains('BJ'))
    stock_basic = stock_basic[mask]

    stock_basic = stock_basic.reset_index(drop=True)
    print(stock_basic.head())
    print(f'[股票列表] 过滤后共 {len(stock_basic)} 条')
    return stock_basic


if __name__ == '__main__':
    df = get_stock_basic_list_2DB('online')
    print(df.head())
    print(len(df))
