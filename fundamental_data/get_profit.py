# -*- coding: utf-8 -*-
"""
获取全量 A 股历史年度净利润（归属于母公司），写入数据库 profit_all_stocks 表。
数据源：AKShare 东方财富年度利润表（stock_profit_sheet_by_yearly_em）
输出宽表格式：symbol, name, profits_YYYY, profits_YYYY+1, ...

对外接口：
  profit_of_all_stocks2db(max_workers)  全量并发写库（主入口）
  get_profit_of_latest_years(code, n)   从数据库取单只最近 n 年净利润数组
"""

import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import akshare as ak
import pandas as pd

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 200)
pd.set_option('expand_frame_repr', False)


# ──────────────────────────────────────────────
# 内部：拉取单只股票历史年度净利润
# ──────────────────────────────────────────────

def _fetch_profit_one(symbol: str, name: str) -> dict | None:
    """
    拉取单只股票所有年报归属于母公司净利润（PARENT_NETPROFIT）。
    返回 dict：{'symbol': ..., 'name': ..., 'profits_YYYY': float, ...}
    失败返回 None。
    symbol：6位纯数字代码，如 '000001'
    """
    prefix = 'SH' if symbol.startswith('6') else 'SZ'
    em_code = prefix + symbol
    try:
        df = ak.stock_profit_sheet_by_yearly_em(symbol=em_code)
        if df is None or df.empty:
            return None
        if 'REPORT_DATE' not in df.columns or 'PARENT_NETPROFIT' not in df.columns:
            return None

        # 只取年报（REPORT_DATE 月日为 12-31），避免 DataFrame 碎片化警告
        dates = pd.to_datetime(df['REPORT_DATE'])
        mask = (dates.dt.month == 12) & (dates.dt.day == 31)
        annual = df[mask].copy()
        annual_dates = dates[mask]
        if annual.empty:
            return None

        # 接口返回倒序（最新在前），需升序排列保证 year 列顺序正确
        sort_order = annual_dates.argsort()
        annual = annual.iloc[sort_order.values]
        annual_dates = annual_dates.iloc[sort_order.values]

        row = {'symbol': symbol, 'name': name}
        for idx, r in annual.iterrows():
            year = str(annual_dates[idx].year)
            val = r['PARENT_NETPROFIT']
            try:
                row[f'profits_{year}'] = float(val) if pd.notna(val) else 0.0
            except (ValueError, TypeError):
                row[f'profits_{year}'] = 0.0
        return row

    except Exception:
        return None


# ──────────────────────────────────────────────
# 全量并发写库
# ──────────────────────────────────────────────

def profit_of_all_stocks2db(max_workers: int = 10):
    """
    并发拉取全量 A 股历史年度净利润，写入数据库 profit_all_stocks 表。
    max_workers : 并发线程数（默认 10）
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        stock_list = pd.read_sql('SELECT symbol, name FROM stock_list', conn)
    except Exception:
        print('[get_profit] 读取 stock_list 失败，请先运行 trade_data 更新股票列表')
        conn.close()
        return
    conn.close()

    stocks = list(zip(stock_list['symbol'], stock_list['name']))
    total = len(stocks)
    print(f'[get_profit] 待拉取股票数：{total}，并发线程：{max_workers}')

    results = []
    done = 0
    failed = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_fetch_profit_one, sym, name): sym
            for sym, name in stocks
        }
        for future in as_completed(futures):
            done += 1
            try:
                row = future.result()
                if row:
                    results.append(row)
                else:
                    failed += 1
            except Exception:
                failed += 1

            if done % 50 == 0 or done == total:
                elapsed = time.time() - start_time
                rate = done / elapsed * 60
                eta = (total - done) / (done / elapsed) if done > 0 else 0
                print(f'[get_profit] [{done}/{total}] 成功:{done - failed} 失败:{failed} '
                      f'速率:{rate:.1f}只/分 剩余:{eta/60:.1f}分钟')

    if not results:
        print('[get_profit] 未获取到任何数据，退出')
        return

    df_all = pd.DataFrame(results)
    year_cols = sorted([c for c in df_all.columns if c.startswith('profits_')])
    df_all = df_all[['symbol', 'name'] + year_cols].fillna(0)

    conn = sqlite3.connect(DB_PATH)
    df_all.to_sql('profit_all_stocks', con=conn, if_exists='replace', index=False)
    conn.close()

    elapsed = time.time() - start_time
    print(f'\n[get_profit] 完成！写入 {len(df_all)} 只，历史年份：{len(year_cols)} 年，'
          f'耗时 {elapsed/60:.1f} 分钟')
    print(f'[get_profit] 年份范围：{year_cols[0] if year_cols else "无"} ~ {year_cols[-1] if year_cols else "无"}')


# ──────────────────────────────────────────────
# 对外查询接口（与原版兼容）
# ──────────────────────────────────────────────

def get_profit_of_latest_years(code: str, latest_years: int) -> list:
    """
    从数据库 profit_all_stocks 表取指定股票最近 latest_years 年的年度净利润列表。
    code：6位纯数字代码，如 '000001'
    返回：数值列表（升序），若无数据返回 [0]
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        # 只查当前股票行，不把全表加载到内存
        row_df = pd.read_sql(
            'SELECT * FROM profit_all_stocks WHERE symbol=?', conn,
            params=(code,)
        )
    except Exception:
        return [0]
    finally:
        conn.close()

    if row_df.empty:
        return [0]

    year_cols = sorted([c for c in row_df.columns if c.startswith('profits_')])
    values = row_df.iloc[0][year_cols].values.tolist()
    if len(values) >= latest_years:
        return [float(v) for v in values[-latest_years:]]
    return [float(v) for v in values] if values else [0]


if __name__ == '__main__':
    profit_of_all_stocks2db(max_workers=10)
