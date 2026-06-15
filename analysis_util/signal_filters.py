# -*- coding: utf-8 -*-
"""
signal_filters.py — 买点信号特征过滤函数库
==========================================
所有函数都是**纯函数**（输入 DataFrame / 参数，输出标量或枚举值），
彼此独立，可自由组合成不同策略。

函数分类
---------
[市场环境]
  market_regime(index_df)               → 'bull' / 'sideways' / 'bear'

[趋势特征]
  ma_alignment(df)                      → 'bull' / 'mixed' / 'bear'
  ma_compressed(df, tol)                → bool（均线收敛）
  price_pct_rank(df, window)            → float 0~1（价格历史分位数）
  relative_strength(stock_df, mkt_df, days) → float（个股 vs 大盘相对强弱）

[量能特征]  （已在 up_classification.py 中定义，此处重新封装便于统一导入）
  vol_ratio_filter(df, recent, base)    → float
  vol_trend_filter(df, days)            → float
  vol_single_day(df, base)              → float

[基本面特征]
  fundamental_quality(code)             → 'good' / 'ok' / 'bad' / 'unknown'
  profit_growth_rate(code, years)       → float（最近 N 年净利润复合增速 CAGR）

[综合评分]
  score_signal(df, code, mkt_df)        → dict（各维度得分汇总，供调试）
"""

import sqlite3
import warnings

import numpy as np
import pandas as pd

from analysis_util.cal_stock_trend import cal_trend_common
from util.utils_common import get_dbpath_by_repo

warnings.filterwarnings("ignore")

DB_PATH = get_dbpath_by_repo()


# ═══════════════════════════════════════════════════════════════
# 市场环境
# ═══════════════════════════════════════════════════════════════

def market_regime(index_df: pd.DataFrame,
                  fast: int = 20,
                  slow: int = 60) -> str:
    """
    判断大盘所处状态。
    输入为大盘指数的日线 DataFrame（需含 'close' 列）。

    Parameters
    ----------
    index_df : 大盘指数历史数据（如上证 000001，沪深300 000300）
    fast     : 短期斜率窗口（默认 20 日）
    slow     : 长期斜率窗口（默认 60 日）

    Returns
    -------
    'bull'      : 短期 & 长期均向上（多头市场，适合做多）
    'sideways'  : 短期向上但长期不明，或短期弱但长期向上
    'bear'      : 短期 & 长期均向下（空头市场，谨慎做多）
    """
    if index_df is None or len(index_df) < slow:
        return 'unknown'
    close = index_df['close'].values.astype(float)
    k_fast = cal_trend_common(close[-fast:])
    k_slow = cal_trend_common(close[-slow:])
    if k_fast > 0.0005 and k_slow > 0:
        return 'bull'
    if k_fast < -0.0005 and k_slow < 0:
        return 'bear'
    return 'sideways'


# ═══════════════════════════════════════════════════════════════
# 趋势特征
# ═══════════════════════════════════════════════════════════════

def ma_alignment(df: pd.DataFrame,
                 windows: tuple = (5, 10, 20, 60)) -> str:
    """
    判断均线排列状态。

    Parameters
    ----------
    df      : 股票日线 DataFrame（含 'close'）
    windows : 均线周期列表（从小到大）

    Returns
    -------
    'bull'  : 所有均线从小到大依次递增（MA5 > MA10 > MA20 > MA60）
    'bear'  : 所有均线从小到大依次递减
    'mixed' : 其他（部分交叉）
    """
    close = df['close']
    if len(close) < max(windows):
        return 'unknown'
    mas = [close.rolling(w).mean().iloc[-1] for w in windows]
    if all(mas[i] > mas[i + 1] for i in range(len(mas) - 1)):
        return 'bull'
    if all(mas[i] < mas[i + 1] for i in range(len(mas) - 1)):
        return 'bear'
    return 'mixed'


def ma_compressed(df: pd.DataFrame,
                  windows: tuple = (5, 10, 20),
                  tol: float = 0.015) -> bool:
    """
    判断均线是否收敛（即将共振）。
    多条均线相互偏差 < tol，说明即将发生方向性突破。

    Parameters
    ----------
    df      : 日线 DataFrame（含 'close'）
    windows : 均线周期
    tol     : 偏差容忍度（默认 1.5%）

    Returns
    -------
    True 表示均线收敛，可能即将发力
    """
    close = df['close']
    if len(close) < max(windows):
        return False
    mas = [close.rolling(w).mean().iloc[-1] for w in windows]
    spread = (max(mas) - min(mas)) / min(mas)
    return spread < tol


def price_pct_rank(df: pd.DataFrame, window: int = 250) -> float:
    """
    当前收盘价在过去 window 日收盘价中的历史分位数（0~1）。

    < 0.2 → 历史低位，安全边际高
    > 0.8 → 历史高位，追高风险大

    Parameters
    ----------
    df     : 日线 DataFrame（含 'close'）
    window : 历史窗口（默认 250 日 ≈ 1年）
    """
    close = df['close'].values.astype(float)
    if len(close) < window:
        hist = close
    else:
        hist = close[-window:]
    cur = hist[-1]
    return float((hist < cur).sum() / len(hist))


def relative_strength(stock_df: pd.DataFrame,
                      market_df: pd.DataFrame,
                      days: int = 20) -> float:
    """
    个股近 days 日涨幅 / 大盘近 days 日涨幅。

    > 1.2 : 强于大盘（相对强势）
    0.8~1.2 : 与大盘同步
    < 0.8 : 弱于大盘（相对弱势）

    Parameters
    ----------
    stock_df  : 个股日线 DataFrame（含 'close'）
    market_df : 大盘日线 DataFrame（含 'close'）
    days      : 比较窗口
    """
    if stock_df is None or market_df is None:
        return 1.0
    if len(stock_df) < days + 1 or len(market_df) < days + 1:
        return 1.0
    s_ret = stock_df['close'].values[-1] / stock_df['close'].values[-days - 1] - 1
    m_ret = market_df['close'].values[-1] / market_df['close'].values[-days - 1] - 1
    # 大盘涨幅绝对值 < 0.3% 时，分母过小会导致 RS 溢出；改用固定基准
    if abs(m_ret) < 0.003:
        # 大盘近乎平盘：个股正收益算强势，负收益算弱势
        return 1.5 if s_ret > 0.003 else (0.5 if s_ret < -0.003 else 1.0)
    return float(s_ret / m_ret)


# ═══════════════════════════════════════════════════════════════
# 量能特征（封装 up_classification 中的函数，统一导入入口）
# ═══════════════════════════════════════════════════════════════

def vol_ratio_filter(df: pd.DataFrame,
                     recent_days: int = 5,
                     base_days: int = 20) -> float:
    """近 recent_days 日均量 / 前 (base_days-recent_days) 日均量。见 up_classification.cal_volume_ratio"""
    from selected_stock_analysis.up_classification import cal_volume_ratio
    return cal_volume_ratio(df, recent_days, base_days)


def vol_trend_filter(df: pd.DataFrame, days: int = 10) -> float:
    """近 days 天量的趋势斜率（归一化）。见 up_classification.cal_volume_trend"""
    from selected_stock_analysis.up_classification import cal_volume_trend
    return cal_volume_trend(df, days)


def vol_single_day(df: pd.DataFrame, base_days: int = 5) -> float:
    """当日量比（最后一根 K 线 / 前 base_days 日均量）。见 up_classification.cal_single_day_vol_ratio"""
    from selected_stock_analysis.up_classification import cal_single_day_vol_ratio
    return cal_single_day_vol_ratio(df, base_days)


# ═══════════════════════════════════════════════════════════════
# 基本面特征
# ═══════════════════════════════════════════════════════════════

def _read_db_table(table: str, symbol: str) -> pd.Series | None:
    """
    从数据库读取单只股票的宽表行（通用内部函数）。
    使用 WHERE symbol=? 过滤，避免把 5000 只全表加载到内存。
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(
            f'SELECT * FROM {table} WHERE symbol=?', conn,
            params=(symbol,)
        )
        conn.close()
        if df.empty:
            return None
        return df.iloc[0]
    except Exception:
        return None


def fundamental_quality(code: str, years: int = 3) -> str:
    """
    基于数据库中的净利润数据判断基本面质量。
    需要已运行 get_profit.profit_of_all_stocks2db() 入库。

    Parameters
    ----------
    code  : 6 位纯数字股票代码，如 '000001'
    years : 比较最近 N 年（默认 3 年）

    Returns
    -------
    'good'    : 净利润连续增长且最新年为正
    'ok'      : 最新年净利润 > N年前（非连续增长）
    'bad'     : 净利润下降或亏损
    'unknown' : 数据库无数据
    """
    row = _read_db_table('profit_all_stocks', code)
    if row is None:
        return 'unknown'
    year_cols = sorted([c for c in row.index if c.startswith('profits_')])
    if len(year_cols) < 2:
        return 'unknown'
    # 取最近 years 年
    recent_cols = year_cols[-years:] if len(year_cols) >= years else year_cols
    profits = [float(row[c]) for c in recent_cols]
    latest = profits[-1]
    if latest <= 0:
        return 'bad'
    if all(profits[i] < profits[i + 1] for i in range(len(profits) - 1)):
        return 'good'
    if latest > profits[0]:
        return 'ok'
    return 'bad'


def profit_growth_rate(code: str, years: int = 3) -> float:
    """
    最近 years 年净利润复合年化增速（CAGR）。

    Parameters
    ----------
    code  : 6 位纯数字股票代码
    years : 计算 CAGR 的年数

    Returns
    -------
    float：CAGR，如 0.15 表示年化 +15%；数据不足返回 0.0
    """
    row = _read_db_table('profit_all_stocks', code)
    if row is None:
        return 0.0
    year_cols = sorted([c for c in row.index if c.startswith('profits_')])
    if len(year_cols) < years + 1:
        return 0.0
    start = float(row[year_cols[-(years + 1)]])
    end   = float(row[year_cols[-1]])
    if start <= 0 or end <= 0:
        return 0.0
    return float((end / start) ** (1.0 / years) - 1)


def revenue_growth_rate(code: str, years: int = 3) -> float:
    """
    最近 years 年营业收入复合年化增速（CAGR）。
    需要已运行 get_income.income_of_all_stocks2db() 入库。
    """
    row = _read_db_table('income_all_stocks', code)
    if row is None:
        return 0.0
    year_cols = sorted([c for c in row.index if c.startswith('income_')])
    if len(year_cols) < years + 1:
        return 0.0
    start = float(row[year_cols[-(years + 1)]])
    end   = float(row[year_cols[-1]])
    if start <= 0 or end <= 0:
        return 0.0
    return float((end / start) ** (1.0 / years) - 1)


# ═══════════════════════════════════════════════════════════════
# 综合评分（汇总各维度，便于调试和策略组合）
# ═══════════════════════════════════════════════════════════════

def score_signal(df: pd.DataFrame,
                 code: str,
                 market_df: pd.DataFrame | None = None) -> dict:
    """
    对一只股票的当前状态计算所有维度的特征值，返回字典供策略组合使用。

    Parameters
    ----------
    df         : 个股日线 DataFrame（含 close / vol）
    code       : 6 位纯数字股票代码
    market_df  : 大盘指数日线 DataFrame（可选，用于计算相对强弱和市场状态）

    Returns
    -------
    dict with keys:
        market          : 'bull'/'sideways'/'bear'/'unknown'
        ma_align        : 'bull'/'mixed'/'bear'/'unknown'
        ma_compress     : bool
        price_rank      : float 0~1
        rs_20d          : float（相对强弱20日）
        vol_ratio       : float
        vol_trend       : float
        vol_today       : float
        fundamental     : 'good'/'ok'/'bad'/'unknown'
        profit_cagr_3y  : float
        revenue_cagr_3y : float
    """
    result = {}

    # 市场环境
    result['market']         = market_regime(market_df) if market_df is not None else 'unknown'

    # 趋势
    result['ma_align']       = ma_alignment(df)
    result['ma_compress']    = ma_compressed(df)
    result['price_rank']     = price_pct_rank(df)
    result['rs_20d']         = relative_strength(df, market_df) if market_df is not None else 1.0

    # 量能
    result['vol_ratio']      = vol_ratio_filter(df)
    result['vol_trend']      = vol_trend_filter(df)
    result['vol_today']      = vol_single_day(df)

    # 基本面
    result['fundamental']    = fundamental_quality(code)
    result['profit_cagr_3y'] = profit_growth_rate(code)
    result['revenue_cagr_3y']= revenue_growth_rate(code)

    return result


# ═══════════════════════════════════════════════════════════════
# 预置策略过滤组合（直接返回 True/False）
# ═══════════════════════════════════════════════════════════════

def filter_up_trend_correction(scores: dict,
                                strict: bool = False) -> tuple[bool, str]:
    """
    上升通道回调买点过滤条件。

    硬过滤（必须满足）：
      1. 大盘不在 bear 状态
      2. 均线排列不为纯空头（bear）
      3. 价格历史分位 < 0.95（排除明显顶部）

    软过滤（strict=True 时启用，进一步提高质量）：
      4. 相对强弱 RS ≥ 0.7（个股不能大幅弱于大盘）
      5. 基本面不为 bad

    Parameters
    ----------
    scores : score_signal() 返回的特征字典
    strict : 是否启用软过滤（默认 False）

    Returns
    -------
    (passed: bool, reason: str)
    """
    checks = []

    # 硬过滤
    if scores['market'] == 'bear':
        checks.append('大盘熊市⚠')
    if scores['ma_align'] == 'bear':
        checks.append('均线空头⚠')
    if scores['price_rank'] > 0.95:
        checks.append(f'价格极高位({scores["price_rank"]:.0%})⚠')

    # 软过滤（strict=True）
    if strict:
        if scores['rs_20d'] < 0.7:
            checks.append(f'相对弱势RS={scores["rs_20d"]:.2f}⚠')
        if scores['fundamental'] == 'bad':
            checks.append('基本面差⚠')

    if checks:
        return False, ' | '.join(checks)
    return True, 'OK'


def filter_down_trend_rebound(scores: dict,
                               strict: bool = False) -> tuple[bool, str]:
    """
    下降通道前低/关键均线买点过滤条件。

    硬过滤（必须满足）：
      1. 价格历史分位 < 0.5（至少在历史中位线以下）
      2. 量能有触底信号（vol_trend > 0 或 vol_today > 1.2）

    软过滤（strict=True 时启用）：
      3. 基本面为 good 或 ok（排除垃圾股价值陷阱）
      4. 大盘不在深度 bear（市场整体抵抗力弱时慎做）

    Parameters
    ----------
    scores : score_signal() 返回的特征字典
    strict : 是否启用软过滤（默认 False）

    Returns
    -------
    (passed: bool, reason: str)
    """
    checks = []

    # 硬过滤
    if scores['price_rank'] > 0.5:
        checks.append(f'价格分位偏高({scores["price_rank"]:.0%})⚠')
    vol_signal = scores['vol_trend'] > 0 or scores['vol_today'] > 1.2
    if not vol_signal:
        checks.append('量能未见底⚠')

    # 软过滤（strict=True）
    if strict:
        if scores['fundamental'] == 'bad':
            checks.append('基本面差⚠')
        if scores['market'] == 'bear':
            checks.append('大盘熊市⚠')

    if checks:
        return False, ' | '.join(checks)
    return True, 'OK'
