# -*- coding: utf-8 -*-

import sqlite3
import sqlalchemy as sqla
import os
from git_util import get_cur_repo


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

# 根据不同的仓库返回不同的DB_PATH
def get_dbpath_by_repo():
    # cur_repo=get_cur_repo()
    if 'beyond19' in os.getcwd():
        return "/Users/beyond19/DB/stock_data.db"
    elif 'beyond' in os.getcwd():
        return "/Users/beyond/DB/stock_data.db"
    else:
        return "E:/Money/stock_data.db"



if __name__ == '__main__':
    # print(get_dbpath_by_repo())

    cur_repo = get_cur_repo()
    print(cur_repo)