# -*- coding: utf-8 -*-
"""
买入点效果追踪与回测统计
=========================
功能：
  1. 对 buy_point_detect / rebound_classification 产出的历史信号（CSV）做回测
  2. 统计各类信号的次日涨跌胜率、平均收益、持有 N 日收益分布
  3. 输出汇总统计表到控制台，并保存到 CSV

使用方法：
  python -m selected_stock_analysis.buy_point_effect_tracking [--signal-file 上升通道回调.csv] [--hold-days 1 3 5 10]

信号 CSV 格式（buy_point_detect.py 输出）：
  code, name, desc, date
  date 格式为 YYYYMMDD（整数或字符串均可）
"""

import argparse
import datetime
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from trade_data.get_trade_data import get_stock_trade_data
from util.date_util import date_add, get_today_date

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────
# 核心工具函数
# ─────────────────────────────────────────────────────────────

def _get_close_on_date(df: pd.DataFrame, target_date: str) -> float | None:
    """
    从已获取的 trade_df 中取 target_date（YYYYMMDD 字符串）当日或之后最近一日的收盘价。
    用于信号触发日当天以及 N 日后的收盘价查找。
    """
    df = df.copy()
    df['trade_date'] = df['trade_date'].astype(str)
    df = df.sort_values('trade_date').reset_index(drop=True)
    # 取 >= target_date 的最近一行
    future = df[df['trade_date'] >= target_date]
    if future.empty:
        return None
    return float(future.iloc[0]['close'])


def backtest_signal(code: str, signal_date: str,
                    hold_days_list: list[int] = (1, 3, 5, 10)) -> dict | None:
    """
    对单个信号做回测，返回各持有周期的收益率。

    Parameters
    ----------
    code         : 股票代码（6位，如 '000001'）
    signal_date  : 信号触发日期，格式 YYYYMMDD（字符串或整数）
    hold_days_list: 持有天数列表

    Returns
    -------
    dict: {
        'code': ..., 'signal_date': ...,
        'ret_1d': ..., 'ret_3d': ..., ...   # 各持有期收益率（小数，None 表示数据不足）
    }
    """
    signal_date = str(signal_date)

    # 拉取信号日前后足够多的数据（前60天 + 后 max(hold_days)*2 天日历天）
    max_hold = max(hold_days_list)
    start_dt = (datetime.datetime.strptime(signal_date, '%Y%m%d')
                - datetime.timedelta(days=30)).strftime('%Y%m%d')
    end_dt   = (datetime.datetime.strptime(signal_date, '%Y%m%d')
                + datetime.timedelta(days=max_hold * 3)).strftime('%Y%m%d')

    df = get_stock_trade_data(code, start_dt, end_dt)
    if df is None or len(df) < 2:
        return None

    # 信号日（次日开始持有：以信号日收盘价为买入价）
    # 这里统一用信号日 >= signal_date 的最近一日收盘价作为"入场价"
    entry_price = _get_close_on_date(df, signal_date)
    if entry_price is None or entry_price == 0:
        return None

    result = {'code': code, 'signal_date': signal_date, 'entry_price': entry_price}

    df_sorted = df.copy()
    df_sorted['trade_date'] = df_sorted['trade_date'].astype(str)
    df_sorted = df_sorted.sort_values('trade_date').reset_index(drop=True)

    # 找 signal_date 对应的行索引
    signal_rows = df_sorted[df_sorted['trade_date'] >= signal_date]
    if signal_rows.empty:
        return None
    signal_idx = signal_rows.index[0]

    for n in hold_days_list:
        target_idx = signal_idx + n
        if target_idx < len(df_sorted):
            exit_price = float(df_sorted.iloc[target_idx]['close'])
            ret = (exit_price - entry_price) / entry_price
        else:
            ret = None
        result[f'ret_{n}d'] = ret

    return result


def backtest_signal_file(signal_file: str,
                         hold_days_list: tuple = (1, 3, 5, 10),
                         output_file: str | None = None) -> pd.DataFrame:
    """
    批量回测一个信号 CSV 文件，输出逐条回测结果 DataFrame。

    Parameters
    ----------
    signal_file   : 信号 CSV 路径，列包含 code / date（其余列忽略）
    hold_days_list: 持有天数列表
    output_file   : 若指定则将结果保存到此 CSV

    Returns
    -------
    pd.DataFrame: 每行对应一条信号的回测结果
    """
    if not Path(signal_file).exists():
        raise FileNotFoundError(f'信号文件不存在: {signal_file}')

    sig_df = pd.read_csv(signal_file, dtype=str)
    # 兼容 code / symbol 两种列名
    if 'code' not in sig_df.columns and 'symbol' in sig_df.columns:
        sig_df.rename(columns={'symbol': 'code'}, inplace=True)
    required = {'code', 'date'}
    missing = required - set(sig_df.columns)
    if missing:
        raise ValueError(f'信号文件缺少列: {missing}，现有列: {list(sig_df.columns)}')

    hold_days_list = list(hold_days_list)
    records = []
    total = len(sig_df)
    for i, row in sig_df.iterrows():
        code  = str(row['code']).strip().zfill(6)
        date  = str(int(float(row['date'])))  # 兼容 20230101.0 等格式
        print(f'  [{i+1}/{total}] 回测 {code}  信号日 {date}')
        res = backtest_signal(code, date, hold_days_list)
        if res:
            # 附加信号文件中的其他字段（如 name、desc）
            for col in sig_df.columns:
                if col not in ('code', 'date'):
                    res[col] = row.get(col, '')
            records.append(res)
        else:
            print(f'    数据不足，跳过')

    if not records:
        print('无有效回测记录。')
        return pd.DataFrame()

    result_df = pd.DataFrame(records)

    if output_file:
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f'\n回测明细已保存至: {output_file}')

    return result_df


# ─────────────────────────────────────────────────────────────
# 统计汇总
# ─────────────────────────────────────────────────────────────

def summarize_backtest(result_df: pd.DataFrame,
                       hold_days_list: tuple = (1, 3, 5, 10)) -> pd.DataFrame:
    """
    对回测结果 DataFrame 做汇总统计，返回统计表。

    统计指标（每个持有期）：
      - 信号总数
      - 有效信号数（数据存在）
      - 胜率（收益 > 0 的比例）
      - 平均收益率
      - 中位收益率
      - 最大涨幅 / 最大跌幅
    """
    if result_df.empty:
        return pd.DataFrame()

    rows = []
    for n in hold_days_list:
        col = f'ret_{n}d'
        if col not in result_df.columns:
            continue
        series = result_df[col].dropna().astype(float)
        total  = len(result_df)
        valid  = len(series)
        win    = (series > 0).sum()
        win_rate    = win / valid if valid > 0 else float('nan')
        avg_ret     = series.mean()
        median_ret  = series.median()
        max_ret     = series.max()
        min_ret     = series.min()
        rows.append({
            '持有天数':    n,
            '信号总数':    total,
            '有效信号数':  valid,
            '胜率':        f'{win_rate:.1%}',
            '平均收益率':  f'{avg_ret:.2%}',
            '中位收益率':  f'{median_ret:.2%}',
            '最大涨幅':    f'{max_ret:.2%}',
            '最大跌幅':    f'{min_ret:.2%}',
        })

    summary_df = pd.DataFrame(rows)
    return summary_df


def print_summary(summary_df: pd.DataFrame, label: str = '') -> None:
    """格式化打印统计表"""
    title = f'===== 回测统计汇总 {label} ====='
    print('\n' + title)
    if summary_df.empty:
        print('（无数据）')
        return
    print(summary_df.to_string(index=False))
    print()


# ─────────────────────────────────────────────────────────────
# 收益分布直方图（可选，matplotlib）
# ─────────────────────────────────────────────────────────────

def plot_return_distribution(result_df: pd.DataFrame,
                             hold_days: int = 5,
                             title: str = '收益率分布') -> None:
    """绘制持有 N 日收益率直方图，显示胜率和均值。"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.rcParams['font.family'] = 'Heiti TC'
        matplotlib.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print('matplotlib 未安装，跳过绘图')
        return

    col = f'ret_{hold_days}d'
    if col not in result_df.columns:
        print(f'列 {col} 不存在，跳过绘图')
        return

    rets = result_df[col].dropna().astype(float) * 100  # 转为百分比
    if rets.empty:
        return

    win_rate = (rets > 0).mean()
    avg_ret  = rets.mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#e05c5c' if r > 0 else '#50b050' for r in rets]
    ax.hist(rets, bins=20, color='steelblue', edgecolor='white', alpha=0.8)
    ax.axvline(0, color='black', linewidth=1, linestyle='--')
    ax.axvline(avg_ret, color='orange', linewidth=1.5, linestyle='-',
               label=f'均值 {avg_ret:.2f}%')
    ax.set_xlabel(f'持有 {hold_days} 日收益率 (%)')
    ax.set_ylabel('信号数量')
    ax.set_title(f'{title}  （胜率 {win_rate:.1%}，共 {len(rets)} 条信号）')
    ax.legend()
    plt.tight_layout()
    out_path = f'回测收益分布_{hold_days}日.png'
    plt.savefig(out_path, dpi=150)
    print(f'收益分布图已保存: {out_path}')
    plt.show()


# ─────────────────────────────────────────────────────────────
# 命令行入口
# ─────────────────────────────────────────────────────────────

def _parse_args():
    parser = argparse.ArgumentParser(
        description='买入点信号回测统计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 回测"上升通道回调"信号，持有 1/3/5/10 日
  python -m selected_stock_analysis.buy_point_effect_tracking \\
      --signal-file 上升通道回调.csv \\
      --hold-days 1 3 5 10 \\
      --plot

  # 同时回测多个信号文件
  python -m selected_stock_analysis.buy_point_effect_tracking \\
      --signal-file 上升通道回调.csv 下降通道到前低.csv
""")
    parser.add_argument('--signal-file', nargs='+', default=['上升通道回调.csv'],
                        help='信号 CSV 文件路径（可传多个）')
    parser.add_argument('--hold-days', nargs='+', type=int, default=[1, 3, 5, 10],
                        help='持有天数列表（默认: 1 3 5 10）')
    parser.add_argument('--plot', action='store_true',
                        help='绘制收益率分布图（每个文件绘制持有天数最大的那档）')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    hold_days = tuple(sorted(args.hold_days))

    for sig_file in args.signal_file:
        print(f'\n{"=" * 60}')
        print(f'信号文件: {sig_file}')
        print(f'持有天数: {hold_days}')
        print('=' * 60)

        out_csv = sig_file.replace('.csv', '_回测明细.csv')
        try:
            result_df = backtest_signal_file(sig_file, hold_days, output_file=out_csv)
        except (FileNotFoundError, ValueError) as e:
            print(f'错误: {e}')
            continue

        summary = summarize_backtest(result_df, hold_days)
        print_summary(summary, label=Path(sig_file).stem)

        # 保存统计汇总
        summary_csv = sig_file.replace('.csv', '_回测统计.csv')
        summary.to_csv(summary_csv, index=False, encoding='utf-8-sig')
        print(f'统计汇总已保存至: {summary_csv}')

        if args.plot and not result_df.empty:
            plot_return_distribution(
                result_df,
                hold_days=max(hold_days),
                title=Path(sig_file).stem,
            )
