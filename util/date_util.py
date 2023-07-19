# -*- coding: utf-8 -*-
import datetime

# 日期加减n天，返回字符串日期
def date_add(date, inc):
    date = str(date)
    date = datetime.datetime.strptime(date,'%Y%m%d')
    new_date = date + datetime.timedelta(days=inc)
    new_date = new_date.strftime('%Y%m%d')
    return new_date

#获取当日日期值
def get_today_date():
    return datetime.datetime.now().strftime('%Y%m%d')

# 增加日期
def date_add(date, inc):
    date = str(date)
    date = datetime.datetime.strptime(date, '%Y%m%d')
    new_date = date + datetime.timedelta(days=inc)
    new_date = int(new_date.strftime('%Y%m%d'))
    return new_date


# 日期差
def date_diff(start_date, end_date):
    start = datetime.datetime.strptime(str(start_date), '%Y%m%d')
    end = datetime.datetime.strptime(str(end_date), '%Y%m%d')
    return (end - start).days