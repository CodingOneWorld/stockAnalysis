# -*- coding: utf-8 -*-
import sqlite3
import sqlalchemy as sqla


# 连接数据库
def conSqlite():
    conn = sqlite3.connect('P:/Money/stocks.db')
    c = conn.cursor()
    return c

# pandas连接数据库
def get_engine(path):
    engine=sqla.create_engine(path)
    return engine