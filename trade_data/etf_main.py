# -*- coding: utf-8 -*-
"""
ETF 行情数据更新入口（独立于股票数据流程）

运行此脚本将：
  1. 在线获取全市场 ETF 列表，写入数据库 etf_list 表
  2. 并发拉取每只 ETF 的前复权日线数据，写入 E{code}_daily 表

数据库路径由 util.utils_common.get_dbpath_by_repo() 决定，与股票数据共用同一个库。
"""

import datetime
import sys
import pathlib

# 当直接运行此脚本时，将项目根目录加入 sys.path，确保 util、trade_data 等包可被正确导入
_PROJECT_ROOT = pathlib.Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from util.utils_common import get_dbpath_by_repo
from trade_data.get_etf_data import update_etf_data_2DB


def run_etf_update(source: str = 'online'):
    """
    执行 ETF 数据全量更新。
    source='online' : 在线获取 ETF 列表（默认）
    source='DB'     : 使用数据库中已有的 ETF 列表（跳过列表更新，直接更新日线数据）
    """
    DB_PATH = get_dbpath_by_repo()
    t1 = datetime.datetime.now()
    print(f'[ETF入口] 开始时间：{t1.strftime("%Y-%m-%d %H:%M:%S")}')

    update_etf_data_2DB(
        filepath=DB_PATH,
        source=source,
        max_workers=4,    # 东方财富接口并发不宜过高，避免被断连
        max_per_min=30,   # 保守限速，实测约 30只/分钟
    )

    t2 = datetime.datetime.now()
    print(f'[ETF入口] 结束时间：{t2.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'[ETF入口] 总耗时：{t2 - t1}')


if __name__ == '__main__':
    run_etf_update(source='online')
