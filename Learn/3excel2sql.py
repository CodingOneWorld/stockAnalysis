# -*- coding: utf-8 -*-

import sqlite3

# 连接sqlite数据库
conn=sqlite3.connect('D:/Money/stocks.db')
print("Opened database successfully")

# 创建表
c = conn.cursor()
c.execute('''CREATE TABLE ts_code
       (trade_date INT PRIMARY KEY     NOT NULL,
       ts_code  TEXT,
       name     TEXT,
       open     DOUBLE,
       high	    DOUBLE,
       low	    DOUBLE,
       close	DOUBLE,
       pre_close	DOUBLE,
       change	DOUBLE,
       pct_chg	DOUBLE,
       vol	    DOUBLE,
       amount   DOUBLE)''')
print("Table created successfully")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");
conn.commit()
conn.close()