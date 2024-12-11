import datetime
import os
import time

import schedule

from selected_stock_analysis.buy_point_detect import buy_point_detect
from trade_data.get_trade_data import get_daily_data_tspro2DB
from util.utils_common import get_dbpath_by_repo


def schedule_run():
    '''
    需要定时运行的任务
    :return: null
    '''
    # 交易数据获取
    t1 = datetime.datetime.now()
    get_daily_data_tspro2DB(DB_PATH, 0, 0)
    t2 = datetime.datetime.now()
    print("耗时：", t2 - t1)

    # 买点检测
    buy_point_detect()



if __name__ == '__main__':
    DB_PATH = get_dbpath_by_repo()
    if 'beyond19' in os.getcwd():
        schedule.every().day.at("19:00").do(schedule_run, DB_PATH)
    else:
        schedule.every().day.at("17:00").do(schedule_run, DB_PATH)
    while True:
        schedule.run_pending()
        time.sleep(1)