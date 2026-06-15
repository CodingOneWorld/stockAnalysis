# -*- coding: utf-8 -*-
"""
基本面选股主入口（两层串联）

第一层：预筛选（stock_pre_select.build_stock_pool）
  → 资格过滤：主板 + 排除ST/退市 + 排除近3年新股
  → 输出 stock_pool.txt

第二层：精筛选（select_by_income + select_by_profit）
  → 基于候选池，筛选近5年收入和净利润增速均 >= 10% 的股票
  → 取交集，输出 基本面好的股票.txt

运行方式：
  cd /Users/zhangqi21/PyCharmMiscProject/stockAnalysis
  python -m stock_select.main
"""
import numpy as np
import os
import pandas as pd

from stock_select.stock_pre_select import build_stock_pool
from stock_select.select_by_income import select_by_income
from stock_select.select_by_profit import select_by_profit


def run_full_pipeline(pool_file: str = 'stock_pool2026.txt',
                      output_file: str = '基本面好的股票.txt',
                      n_years: int = 5,
                      min_growth_pct: float = 0.1,
                      rebuild_pool: bool = True):
    """
    执行两层串联选股流程。

    pool_file      : 预筛选候选池文件路径
    output_file    : 精筛选结果输出路径
    n_years        : 精筛选考察年数
    min_growth_pct : 精筛选最低年增速门槛
    rebuild_pool   : True=重新跑预筛选生成候选池；False=直接读取已有的 pool_file
    """
    # ── 第一层：预筛选 ─────────────────────────────────────────────
    if rebuild_pool or not os.path.exists(pool_file):
        print('=' * 50)
        print('【第一层】预筛选：资格过滤')
        print('=' * 50)
        pool_df = build_stock_pool(output_file=pool_file)
    else:
        pool_df = pd.read_csv(pool_file, dtype={'symbol': str})
        print(f'[主流程] 读取已有候选池 {pool_file}，共 {len(pool_df)} 只')

    symbol_list = pool_df['symbol'].tolist()

    # ── 第二层：精筛选 ─────────────────────────────────────────────
    print()
    print('=' * 50)
    print('【第二层】精筛选：财务质量过滤')
    print('=' * 50)
    income_symbols = select_by_income(
        n_years=n_years,
        min_growth_pct=min_growth_pct,
        symbol_list=symbol_list
    )
    profit_symbols = select_by_profit(
        n_years=n_years,
        min_growth_pct=min_growth_pct,
        symbol_list=symbol_list
    )

    # 取交集：收入和净利润均持续增长
    final_symbols = sorted(set(income_symbols) & set(profit_symbols))

    # 从候选池中获取股票名称
    name_map = dict(zip(pool_df['symbol'], pool_df['stock_name']))

    print()
    print('=' * 50)
    print(f'【结果】基本面双优股票：{len(final_symbols)} 只')
    print('=' * 50)
    with open(output_file, 'w', encoding='utf-8') as fw:
        fw.write('symbol,stock_name\n')
        for sym in final_symbols:
            name = name_map.get(sym, '')
            print(f'  {sym}  {name}')
            fw.write(f'{sym},{name}\n')

    print(f'\n[主流程] 结果已写入 {output_file}')
    return final_symbols


if __name__ == '__main__':
    # rebuild_pool=True：重新生成候选池（首次运行或股票列表有更新时使用）
    # rebuild_pool=False：直接复用已有 stock_pool.txt（候选池不变时节省时间）
    run_full_pipeline(rebuild_pool=True)
