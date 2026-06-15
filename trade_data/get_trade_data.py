# -*- coding: utf-8 -*-

# 获取增量数据，并写入数据库
# 数据源：AKShare（腾讯，主力，前复权） + Tushare（备用，前复权）
import datetime
import traceback
import pathlib
import threading
import queue
import time
import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# 禁用 tqdm 在多线程模式下的控制台输出（并发拉取时日志过多）
os.environ.setdefault('TQDM_DISABLE', '1')

from trade_data.get_stock_basic_list import get_stock_basic_list_2DB
from trade_data.data_source import get_daily_qfq
from util.utils_common import get_dbpath_by_repo

# 当前文件所在目录，用于定位 last_datetime.txt
_TRADE_DATA_DIR = pathlib.Path(__file__).parent

DB_PATH = get_dbpath_by_repo()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 200)
pd.set_option('expand_frame_repr', False)


# ──────────────────────────────────────────────
# 限速器：生产者-消费者令牌桶
# 专用线程按精确间隔投放令牌，工作线程直接从队列取，
# 彻底消除竞争锁/惊群问题。
# ──────────────────────────────────────────────

class RateLimiter:
    """
    生产者-消费者令牌桶，线程安全。
    一个后台线程以固定间隔向队列投放令牌；
    工作线程调用 acquire() 阻塞等待令牌，先到先得。
    max_per_min: 每分钟最多允许的请求次数
    """
    def __init__(self, max_per_min: int = 48):
        self._max = max_per_min
        self._interval = 60.0 / max_per_min
        # 队列最多缓冲 3 个令牌，防止任务少时过度预发
        self._q: queue.Queue = queue.Queue(maxsize=3)
        self._total_issued = 0
        self._lock = threading.Lock()
        self._producer_thread = threading.Thread(
            target=self._produce, daemon=True, name='RateLimiterProducer'
        )
        self._producer_thread.start()

    def _produce(self):
        """后台线程：按固定间隔投放令牌"""
        while True:
            time.sleep(self._interval)
            self._q.put(1)  # 队满则阻塞，自动背压

    def acquire(self):
        """阻塞直到获取一个令牌"""
        self._q.get()
        with self._lock:
            self._total_issued += 1

    @property
    def current_rate(self) -> int:
        """返回已发放的令牌总数"""
        return self._total_issued

    def reset(self, max_per_min: int = None):
        """重置限速参数（清空队列，更新速率）"""
        if max_per_min:
            self._max = max_per_min
            self._interval = 60.0 / max_per_min
        # 清空残余令牌
        while not self._q.empty():
            try:
                self._q.get_nowait()
            except queue.Empty:
                break
        with self._lock:
            self._total_issued = 0


# 全局限速器（45次/分钟，实测腾讯数据源服务器限速天花板约 37只/分）
_rate_limiter = RateLimiter(max_per_min=45)


# ──────────────────────────────────────────────
# 单只股票拉取并写入数据库（线程任务）
# ──────────────────────────────────────────────

def _fetch_and_save(ts_code: str, name: str, filepath: str) -> dict:
    """
    拉取单只股票日线数据并写入数据库（线程安全，每次独立建连接）。
    返回 dict: {ts_code, success, rows, error}
    """
    _rate_limiter.acquire()  # 限速：先拿令牌再发请求
    code = ts_code.split('.')[0]
    table_name = 'S' + code + '_daily'

    try:
        df = get_daily_qfq(ts_code, name=name, retry=2)
        if df is None or df.empty:
            return {'ts_code': ts_code, 'success': False, 'rows': 0, 'error': '数据为空'}

        # 每个线程独立建连接；开启 WAL 模式，减少多线程写锁等待
        conn = sqlite3.connect(filepath, check_same_thread=False, timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=NORMAL')
        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
        conn.close()
        return {'ts_code': ts_code, 'success': True, 'rows': len(df), 'error': ''}

    except Exception as e:
        return {'ts_code': ts_code, 'success': False, 'rows': 0,
                'error': str(e) + '\n' + traceback.format_exc()}


# ──────────────────────────────────────────────
# 对外接口：单只股票查询
# ──────────────────────────────────────────────

def get_stock_trade_data(code, start_date='', end_date='', mode='DB'):
    """
    获取单个股票的历史日线数据（前复权）。
    mode='DB'    : 从数据库读取（默认）
    mode='online': 从网络实时获取（AKShare 主 / Tushare 备）
    返回字段：ts_code, trade_date, open, high, low, close, vol, amount, name
    数据按 trade_date 升序排列
    """
    if mode == 'online':
        from util.utils_common import code2ts_code
        ts_code = code2ts_code(str(code))
        df = get_daily_qfq(ts_code, start_date=start_date, end_date=end_date)
    else:
        conn = sqlite3.connect(DB_PATH)
        table_name = 'S' + str(code) + '_daily'
        try:
            df = pd.read_sql('select * from ' + table_name, conn)
        except Exception:
            conn.close()
            return None
        conn.close()

    df2 = df.dropna(axis=0, subset=['close'])
    if start_date != '' and end_date != '':
        df2 = df2[df2.trade_date >= start_date][df2.trade_date <= end_date]
    df2 = df2.sort_values('trade_date').reset_index(drop=True)
    return df2


def get_stock_trade_data_latestdays(code, latestdays):
    """获取最近 latestdays 天的日线数据（从数据库）"""
    df2 = get_stock_trade_data(code)
    if latestdays > len(df2):
        latestdays = len(df2)
    df2 = df2[-latestdays:]
    df2.reset_index(drop=True, inplace=True)
    return df2


# ──────────────────────────────────────────────
# 全量更新（并发版）
# ──────────────────────────────────────────────

def get_daily_data_tspro2DB(filepath, cou_new, cou_del, source='online',
                             max_workers: int = 12, max_per_min: int = 45):
    """
    全量更新所有 A 股日线数据到 SQLite 数据库（并发版）。
    数据源：AKShare（腾讯，主力） + Tushare（备用），均为前复权数据。

    filepath    : 数据库路径
    cou_new     : 从第几个股票开始写入（断点续传用，正常传 0）
    cou_del     : 保留参数（暂未使用）
    source      : 'online' 从网络获取股票列表；'DB' 从数据库获取股票列表
    max_workers : 并发线程数（默认 12，实测腾讯数据源在此线程数下速率达到天花板 ~37只/分）
    max_per_min : 每分钟最大请求次数（默认 45，腾讯接口实测上限约 37只/分，
                  此值稍高于实际上限以不额外限制，同时留出安全余量）
    """
    print(f'Opened database: {filepath}')

    # 调整全局限速器
    _rate_limiter._interval = 60.0 / max_per_min

    # 从文件中查询上一次运行时间，决定是否在线拉取股票列表
    last_dt_file = _TRADE_DATA_DIR / 'last_datetime.txt'
    with open(last_dt_file, 'r') as f:
        dtime = datetime.datetime.strptime(f.readlines()[0], '%Y-%m-%d %H:%M:%S')
        dtime2 = datetime.datetime.now()
        print(f'上次运行：{dtime}，当前：{dtime2}')
        if (dtime2 - dtime).total_seconds() / 3600 < 1:
            source = 'DB'

    with open(last_dt_file, 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print(f'[数据更新] source={source}, 并发线程={max_workers}, 限速={max_per_min}次/分钟')

    # 获取股票列表
    stock_basic = get_stock_basic_list_2DB(source)
    name_map = dict(zip(stock_basic['ts_code'], stock_basic['name']))

    stocks_list = sorted(stock_basic['ts_code'].tolist())[cou_new:]
    total = len(stocks_list)
    print(f'[数据更新] 待更新股票数：{total}')

    # ── 并发执行 ──
    done = 0
    failed = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_fetch_and_save, ts_code, name_map.get(ts_code, ''), filepath): ts_code
            for ts_code in stocks_list
        }

        for future in as_completed(futures):
            result = future.result()
            done += 1
            elapsed = time.time() - start_time
            rate = done / elapsed * 60  # 实际速率（只/分钟）
            eta = (total - done) / (done / elapsed) if done > 0 else 0

            if result['success']:
                print(f'[{done}/{total}] ✓ {result["ts_code"]} '
                      f'{result["rows"]}条 | '
                      f'速率:{rate:.1f}只/分 | '
                      f'剩余:{eta/60:.1f}分钟')
            else:
                failed.append(result['ts_code'])
                print(f'[{done}/{total}] ✗ {result["ts_code"]} '
                      f'失败: {result["error"][:80]}')

    # 汇总
    total_elapsed = time.time() - start_time
    print(f'\n[数据更新] 完成！共 {total} 只，成功 {total - len(failed)} 只，'
          f'失败 {len(failed)} 只，耗时 {total_elapsed/60:.1f} 分钟')
    if failed:
        print(f'[数据更新] 失败列表: {failed}')


if __name__ == '__main__':
    # 测试单只股票读取
    df = get_stock_trade_data('000001', mode='online')
    print(df[-10:])
