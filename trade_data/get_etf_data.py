# -*- coding: utf-8 -*-
"""
ETF 行情数据获取与持久化
- 获取 ETF 列表，写入 SQLite 表 etf_list
- 并发拉取每只 ETF 的前复权日线数据，写入 SQLite 表 E{code}_daily
- 对外查询接口：get_etf_trade_data()

数据源：AKShare 东方财富（免费，无频次限制）
字段规范与股票日线表一致：
  ts_code, trade_date, open, high, low, close, vol, amount, name
  trade_date 格式：YYYYMMDD（字符串），升序排列
"""

import sqlite3
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from trade_data.data_source import get_etf_list_ak, get_etf_daily_ak
from trade_data.get_trade_data import RateLimiter
from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 200)
pd.set_option('expand_frame_repr', False)

# ETF 专用限速器（东方财富接口实测限速约 30只/分钟，保守设置避免被断连）
_etf_rate_limiter = RateLimiter(max_per_min=30)


# ──────────────────────────────────────────────
# ETF 列表
# ──────────────────────────────────────────────

def get_etf_list_2DB(source: str = 'online') -> pd.DataFrame:
    """
    获取 ETF 基础列表并写入数据库。
    source='online' : 从 AKShare 拉取最新列表并写库（默认）
    source='DB'     : 直接从数据库读取，不请求网络

    数据库表名：etf_list
    返回字段：code, name, ts_code
    """
    conn = sqlite3.connect(DB_PATH)

    if source == 'DB':
        try:
            df = pd.read_sql('SELECT * FROM etf_list', conn)
            print(f'[ETF列表] 从数据库读取，共 {len(df)} 条')
        except Exception:
            print('[ETF列表] 数据库中无 etf_list 表，尝试在线获取...')
            df = get_etf_list_ak()
            df.to_sql('etf_list', con=conn, if_exists='replace', index=False)
            print(f'[ETF列表] 已写入数据库，共 {len(df)} 条')
    else:
        df = get_etf_list_ak()
        df.to_sql('etf_list', con=conn, if_exists='replace', index=False)
        print(f'[ETF列表] 在线获取并写入数据库，共 {len(df)} 条')

    conn.close()
    return df.reset_index(drop=True)


# ──────────────────────────────────────────────
# 单只 ETF 拉取并写库（线程任务）
# ──────────────────────────────────────────────

def _fetch_etf_and_save(code: str, name: str, filepath: str) -> dict:
    """
    拉取单只 ETF 日线数据并写入数据库（线程安全，每次独立建连接）。
    表名格式：E{code}_daily（与股票 S{code}_daily 区分）
    返回 dict: {code, success, rows, error}
    """
    _etf_rate_limiter.acquire()  # 限速：先拿令牌再发请求
    table_name = 'E' + code + '_daily'

    try:
        df = get_etf_daily_ak(code, name=name)
        if df is None or df.empty:
            return {'code': code, 'success': False, 'rows': 0, 'error': '数据为空'}

        conn = sqlite3.connect(filepath, check_same_thread=False, timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=NORMAL')
        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
        conn.close()
        return {'code': code, 'success': True, 'rows': len(df), 'error': ''}

    except Exception as e:
        return {
            'code': code,
            'success': False,
            'rows': 0,
            'error': str(e) + '\n' + traceback.format_exc()
        }


# ──────────────────────────────────────────────
# 主入口：全量更新 ETF 日线数据
# ──────────────────────────────────────────────

def update_etf_data_2DB(filepath: str = None,
                         source: str = 'online',
                         max_workers: int = 4,
                         max_per_min: int = 30):
    """
    获取全量 ETF 日线数据并写入 SQLite 数据库（ETF 独立入口）。

    流程：
      1. 获取 ETF 列表（并写库）
      2. 并发拉取每只 ETF 的前复权日线数据
      3. 写入数据库，表名 E{code}_daily

    filepath    : 数据库路径，默认使用项目全局 DB_PATH
    source      : 'online' 在线获取 ETF 列表；'DB' 从库中读取列表
    max_workers : 并发线程数（默认 8）
    max_per_min : 每分钟最大请求次数（默认 60）
    """
    if filepath is None:
        filepath = DB_PATH

    print(f'[ETF更新] 数据库路径：{filepath}')
    print(f'[ETF更新] source={source}, 并发线程={max_workers}, 限速={max_per_min}次/分钟')

    # 调整限速器速率
    _etf_rate_limiter._interval = 60.0 / max_per_min

    # Step 1：获取 ETF 列表
    etf_list = get_etf_list_2DB(source=source)
    total = len(etf_list)
    print(f'[ETF更新] 待更新 ETF 数：{total}')

    # Step 2：并发拉取日线数据
    done = 0
    failed = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _fetch_etf_and_save,
                row['code'],
                row['name'],
                filepath
            ): row['code']
            for _, row in etf_list.iterrows()
        }

        for future in as_completed(futures):
            result = future.result()
            done += 1
            elapsed = time.time() - start_time
            rate = done / elapsed * 60  # 实际速率（只/分钟）
            eta = (total - done) / (done / elapsed) if done > 0 else 0

            if result['success']:
                print(f'[{done}/{total}] ✓ {result["code"]} '
                      f'{result["rows"]}条 | '
                      f'速率:{rate:.1f}只/分 | '
                      f'剩余:{eta / 60:.1f}分钟')
            else:
                failed.append(result['code'])
                print(f'[{done}/{total}] ✗ {result["code"]} '
                      f'失败: {result["error"][:80]}')

    # 汇总
    total_elapsed = time.time() - start_time
    print(f'\n[ETF更新] 完成！共 {total} 只，成功 {total - len(failed)} 只，'
          f'失败 {len(failed)} 只，耗时 {total_elapsed / 60:.1f} 分钟')
    if failed:
        print(f'[ETF更新] 失败列表: {failed}')


# ──────────────────────────────────────────────
# 对外查询接口
# ──────────────────────────────────────────────

def get_etf_trade_data(code: str,
                        start_date: str = '',
                        end_date: str = '',
                        mode: str = 'DB') -> pd.DataFrame:
    """
    获取单只 ETF 的历史日线数据（前复权）。
    mode='DB'    : 从数据库读取（默认）
    mode='online': 从网络实时获取（AKShare）

    返回字段：ts_code, trade_date, open, high, low, close, vol, amount, name
    数据按 trade_date 升序排列
    """
    if mode == 'online':
        # 尝试从数据库的 etf_list 表查找 name，避免 name 字段为空
        name = ''
        try:
            conn = sqlite3.connect(DB_PATH)
            result = pd.read_sql(
                f"SELECT name FROM etf_list WHERE code='{code}' LIMIT 1", conn
            )
            conn.close()
            if not result.empty:
                name = result.iloc[0]['name']
        except Exception:
            pass
        df = get_etf_daily_ak(code, name=name, start_date=start_date, end_date=end_date)
    else:
        conn = sqlite3.connect(DB_PATH)
        table_name = 'E' + str(code) + '_daily'
        try:
            df = pd.read_sql('SELECT * FROM ' + table_name, conn)
        except Exception:
            conn.close()
            return pd.DataFrame()
        conn.close()

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.dropna(axis=0, subset=['close'])
    if start_date:
        df = df[df['trade_date'] >= start_date]
    if end_date:
        df = df[df['trade_date'] <= end_date]
    df = df.sort_values('trade_date').reset_index(drop=True)
    return df


def get_etf_trade_data_latestdays(code: str, latestdays: int) -> pd.DataFrame:
    """获取最近 latestdays 天的 ETF 日线数据（从数据库）"""
    df = get_etf_trade_data(code)
    if df.empty:
        return df
    if latestdays > len(df):
        latestdays = len(df)
    return df[-latestdays:].reset_index(drop=True)


# ──────────────────────────────────────────────
# 测试入口
# ──────────────────────────────────────────────

if __name__ == '__main__':
    # 测试单只 ETF 在线获取
    print('=== 测试单只 ETF 日线（510300 沪深300ETF）===')
    df = get_etf_trade_data('510300', mode='online')
    print(df.tail(10))
