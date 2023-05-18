# -*- coding: utf-8 -*-

import sqlite3
import sqlalchemy as sqla


def code2ts_code(symbol):
    if str(symbol).startswith('0') or str(symbol).startswith('3'):
        return symbol + ".SZ"
    else:
        return symbol + ".SH"


# 连接数据库
def conSqlite(path):
    conn = sqlite3.connect(path)
    return conn


# pandas连接数据库
def get_engine(path):
    engine = sqla.create_engine(path)
    return engine
