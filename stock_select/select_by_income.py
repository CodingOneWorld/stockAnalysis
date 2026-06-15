# -*- coding: utf-8 -*-
"""
精筛选第一步：按营业收入增速筛选（第二层）

从财务数据库中筛选近 n_years 年收入持续增长的股票。
当传入 symbol_list 时，只在候选池范围内筛选（对接预筛选结果）；
不传则扫全库。
"""
import sqlite3
import pandas as pd

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 200)
pd.set_option('expand_frame_repr', False)


def select_by_income(n_years: int = 5,
                     min_growth_pct: float = 0.1,
                     symbol_list: list = None) -> list:
    """
    筛选近 n_years 年营业收入持续增长（每年增速 >= min_growth_pct）的股票。

    n_years        : 考察年数（默认5年）
    min_growth_pct : 最低年增速门槛（默认10%）
    symbol_list    : 候选股票代码列表（来自预筛选）；为 None 时扫全库

    返回：满足条件的股票代码列表（symbol）
    """
    conn = sqlite3.connect(DB_PATH)
    income_data = pd.read_sql('SELECT * FROM income_all_stocks', conn)
    conn.close()

    # 若传入候选池，只保留候选范围内的股票
    if symbol_list is not None:
        income_data = income_data[income_data['symbol'].isin(symbol_list)]
        print(f'[收入筛选] 候选池 {len(symbol_list)} 只 → 财务库匹配 {len(income_data)} 只')

    # 动态解析年份列
    year_cols = sorted([c for c in income_data.columns if c.startswith('income_')])
    years = [int(c.split('_')[1]) for c in year_cols]
    recent_year_cols = year_cols[-n_years:]
    recent_years = years[-n_years:]

    # 计算相邻年份增长幅度和增速
    for i in range(len(recent_years) - 1):
        col_cur  = f'income_{recent_years[i + 1]}'
        col_prev = f'income_{recent_years[i]}'
        income_data[f'change_{i + 1}']     = income_data[col_cur] - income_data[col_prev]
        income_data[f'pct_change_{i + 1}'] = income_data[f'change_{i + 1}'] / income_data[col_prev]

    change_cols     = [f'change_{i + 1}'     for i in range(len(recent_years) - 1)]
    pct_change_cols = [f'pct_change_{i + 1}' for i in range(len(recent_years) - 1)]

    # 筛选：每年增长幅度 > 0 且增速 >= min_growth_pct
    mask = pd.Series([True] * len(income_data), index=income_data.index)
    for c in change_cols:
        mask = mask & (income_data[c] > 0)
    for c in pct_change_cols:
        mask = mask & (income_data[c] >= min_growth_pct)

    result = income_data.loc[mask, ['symbol', 'name'] + recent_year_cols].reset_index(drop=True)
    print(f'[收入筛选] 近{n_years}年收入持续增长（增速≥{min_growth_pct:.0%}）：{len(result)} 只')
    result.to_csv('select_by_income.csv', index=False)
    return result['symbol'].tolist()


if __name__ == '__main__':
    # 独立运行时扫全库
    stocks = select_by_income()
    print(stocks)
