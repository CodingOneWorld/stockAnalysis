# -*- coding: utf-8 -*-

import sqlite3
import sqlalchemy as sqla


def code2ts_code(code):
    if str(code).startswith('0') or str(code).startswith('3'):
        return code + ".SZ"
    else:
        return code + ".SH"


# 连接数据库
def conSqlite(path):
    conn = sqlite3.connect(path)
    return conn


# pandas连接数据库
def get_engine(path):
    engine = sqla.create_engine(path)
    return engine
