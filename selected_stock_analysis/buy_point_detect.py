# -*- coding: utf-8 -*-

"""
买入点检测
==========
支持三类信号：
  1. 上升通道回调买点
  2. 下降通道到前低
  3. 下降通道到关键均线（60/140/250 日）

新增特征过滤（通过 signal_filters 模块）：
  - 大盘状态（bull / sideways / bear）
  - 均线多头排列
  - 价格历史分位数
  - 相对强弱（vs 大盘）
  - 基本面质量（净利润趋势）
  - 量能信号

用法：
  buy_point_detect(left_shift=0, use_filters=True, index_code='000300')
"""

import warnings

import numpy as np
import pandas as pd

from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import cal_trend_common
from analysis_util.output_document import output_doc
from analysis_util.signal_filters import (
    market_regime, score_signal,
    filter_up_trend_correction, filter_down_trend_rebound,
)
from selected_stock_analysis.key_price_compare import mav_compare_df
from selected_stock_analysis.up_classification import (
    compare2mean_window,
    cal_volume_ratio, cal_single_day_vol_ratio, cal_volume_trend,
)
from trade_data.get_trade_data import get_stock_trade_data

warnings.filterwarnings("ignore")


def buy_point_detect(left_shift: int = 0,
                     use_filters: bool = True,
                     index_code: str = '000300',
                     stock_file: str = '自选股202308.csv'):
    """
    Parameters
    ----------
    left_shift   : 向前回溯的 K 线根数（0 = 今日；10 = 模拟10日前的信号）
    use_filters  : 是否启用 signal_filters 特征过滤（默认 True）
    index_code   : 大盘指数代码（默认沪深300 '000300'；也可用上证 '000001'）
    stock_file   : 自选股 CSV 文件路径
    """

    # ── 加载股票池 ──────────────────────────────────────────────
    df_pool = pd.read_csv(stock_file, dtype={'symbol': np.str_}, delimiter=',')
    stock_list = df_pool.values

    # ── 加载大盘数据（供相对强弱 & 市场状态计算） ─────────────
    market_df = None
    regime    = 'unknown'
    if use_filters:
        market_df = get_stock_trade_data(index_code)
        if market_df is not None and left_shift > 0:
            market_df = market_df[:len(market_df) - left_shift]
        if market_df is not None:
            regime = market_regime(market_df)
    print(f'[buy_point_detect] 大盘状态={regime}  use_filters={use_filters}  left_shift={left_shift}')

    up_trend_correction_ls = []   # 上升通道回调
    down_trend_pre_low_ls  = []   # 下降通道到前低
    down_trend_key_mav_ls  = []   # 下降通道到关键均线

    for line in stock_list:
        code = str(line[0])
        name = str(line[1])
        print(f'[{code}] {name}')

        # ── 获取交易数据 ─────────────────────────────────────
        df = get_stock_trade_data(code)
        if df is None or len(df) < 30 + left_shift:
            print('  数据不足，跳过')
            continue
        if left_shift > 0:
            df = df[:len(df) - left_shift]
        df = df[-300:].copy()
        day_str = str(df['trade_date'].values[-1])

        # ── 量能指标（各策略共用） ───────────────────────────
        vol_ratio = cal_volume_ratio(df, recent_days=5, base_days=20)
        today_vr  = cal_single_day_vol_ratio(df, base_days=5)
        vol_trend = cal_volume_trend(df, days=10)
        print(f'  量比={vol_ratio:.2f}  当日量比={today_vr:.2f}  量趋势={vol_trend:.4f}')

        # ── 特征评分（use_filters=True 时才调用，避免慢查询） ─
        scores = None
        if use_filters:
            scores = score_signal(df, code, market_df)
            print(f'  MA排列={scores["ma_align"]}  价格分位={scores["price_rank"]:.0%}'
                  f'  RS20d={scores["rs_20d"]:.2f}  基本面={scores["fundamental"]}'
                  f'  利润CAGR={scores["profit_cagr_3y"]:.1%}')

        # ══════════════════════════════════════════════════════
        # 策略1：上升通道回调买点
        #   基础条件：最近10天在32日均线上方 + 接近短期均线
        #   量能标注：缩量回调 / 放量回调⚠
        #   过滤增强：大盘非熊 + 均线多头 + 价格不在顶部 + 基本面不差
        # ══════════════════════════════════════════════════════
        tag32 = compare2mean_window(32, df.copy(), 10)
        if tag32 > 0:
            mean_near = [m for m in [5, 10, 20, 30] if mav_compare_df(df, m) == 1]
            if mean_near:
                shrink = vol_ratio < 0.8 or today_vr < 0.8
                vol_tag = f'缩量回调 vol={vol_ratio:.2f}' if shrink else f'放量回调⚠ vol={vol_ratio:.2f}'
                mav_str = '/'.join(str(m) for m in mean_near)

                # 特征过滤
                filter_pass, filter_reason = True, 'OK'
                if use_filters and scores is not None:
                    filter_pass, filter_reason = filter_up_trend_correction(scores)

                label = f'接近均线{mav_str} [{vol_tag}]'
                if not filter_pass:
                    label += f' [过滤:{filter_reason}]'
                    print(f'  上升通道回调 → 过滤: {filter_reason}')
                else:
                    print(f'  上升通道回调 → 入选: {label}')
                up_trend_correction_ls.append(
                    [code, name, label, day_str, filter_pass, filter_reason])

        # ══════════════════════════════════════════════════════
        # 策略2 & 3：下降通道到前低 / 关键均线
        #   基础条件：k5<0 且 k20<0
        #   量能标注：量趋势回升 / 今日放量 / 量能未见底⚠
        #   过滤增强：价格历史低位 + 基本面 good/ok + 有量能信号
        # ══════════════════════════════════════════════════════
        k5  = cal_trend_common(df['close'].values[-5:])
        k20 = cal_trend_common(df['close'].values[-20:])
        if k5 < 0 and k20 < 0:
            if vol_trend > 0:
                vol_desc = '量趋势回升✓'
            elif today_vr > 1.2:
                vol_desc = '今日放量✓'
            else:
                vol_desc = '量能未见底⚠'

            filter_pass2, filter_reason2 = True, 'OK'
            if use_filters and scores is not None:
                filter_pass2, filter_reason2 = filter_down_trend_rebound(scores)

            # 策略2：接近前低
            data = df['low'].values
            y    = cal_extreme_min_value(data)
            y2   = cal_extreme_min_value(y[1])
            cur  = df['low'].values[-1]
            pre_lows = [t for t in y2[1] if cur * 0.99 <= t <= cur * 1.01]
            if pre_lows:
                low_str = '/'.join(str(round(t, 2)) for t in pre_lows)
                label = f'接近前低{low_str} [{vol_desc}]'
                if not filter_pass2:
                    label += f' [过滤:{filter_reason2}]'
                    print(f'  下降通道前低 → 过滤: {filter_reason2}')
                else:
                    print(f'  下降通道前低 → 入选: {label}')
                down_trend_pre_low_ls.append(
                    [code, name, label, day_str, filter_pass2, filter_reason2])

            # 策略3：接近关键均线
            for mav in [60, 140, 250]:
                if mav_compare_df(df, mav) == 1:
                    label = f'接近均线{mav} [{vol_desc}]'
                    if not filter_pass2:
                        label += f' [过滤:{filter_reason2}]'
                        print(f'  下降通道关键均线 → 过滤: {filter_reason2}')
                    else:
                        print(f'  下降通道关键均线 → 入选: {label}')
                    down_trend_key_mav_ls.append(
                        [code, name, label, day_str, filter_pass2, filter_reason2])
                    break   # 每只只取最近一条均线

    # ── 输出 ─────────────────────────────────────────────────
    _save_results(up_trend_correction_ls,  '上升通道回调')
    _save_results(down_trend_pre_low_ls,   '下降通道到前低')
    _save_results(down_trend_key_mav_ls,   '下降通道到关键均线')


def _save_results(records: list, label: str):
    """将信号列表保存为 Word 文档 + CSV（含过滤标记列）"""
    cols = ['code', 'name', 'desc', 'date', 'filter_pass', 'filter_reason']
    df   = pd.DataFrame(records, columns=cols)

    passed = df[df['filter_pass'] == True]
    all_   = df

    print(f'\n[{label}] 触发信号: {len(all_)} 只  通过过滤: {len(passed)} 只')

    # CSV：全量（含过滤未通过的，desc 里已有 [过滤:...] 标注）
    csv_path  = f'{label}.csv'
    # 回测用的 CSV 只保留 code/name/desc/date 四列，与 buy_point_effect_tracking 兼容
    all_[['code', 'name', 'desc', 'date']].to_csv(csv_path, index=False)

    # 严格版 CSV：只保留通过过滤的信号
    strict_csv = f'{label}_严格.csv'
    passed[['code', 'name', 'desc', 'date']].to_csv(strict_csv, index=False)

    # Word 文档：只输出通过过滤的
    try:
        output_doc(passed[['code', 'name', 'desc', 'date']], f'{label}.docx')
    except Exception as e:
        print(f'  Word 输出失败: {e}')


if __name__ == '__main__':
    # 示例1：今日信号（带过滤）
    buy_point_detect(use_filters=True)

    # 示例2：模拟10日前信号（不带过滤，用于对比回测）
    # buy_point_detect(left_shift=10, use_filters=False)

    # 示例3：只看大盘方向，不做基本面过滤
    # buy_point_detect(use_filters=True, index_code='000001')
