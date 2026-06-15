# -*- coding: utf-8 -*-
"""
双数据源封装层
- 主力：AKShare（腾讯数据源，免费无限制，前复权）
- 备用：Tushare Pro（有频次限制，前复权）

对外统一输出字段：
  ts_code, trade_date, open, high, low, close, vol, amount, name
  trade_date 格式：YYYYMMDD（字符串）
  数据按 trade_date 升序排列
"""

import os
import time
import traceback

# ── 必须在 akshare 之前设置，禁止 akshare 内部的 tqdm 进度条输出 ──
os.environ['TQDM_DISABLE'] = '1'

# 用 disable=True 子类覆盖 tqdm，保留迭代功能但不输出进度条
import tqdm as _tqdm_module
_real_tqdm_init = _tqdm_module.tqdm.__init__
def _silent_tqdm_init(self, *args, **kwargs):
    kwargs['disable'] = True
    _real_tqdm_init(self, *args, **kwargs)
_tqdm_module.tqdm.__init__ = _silent_tqdm_init

import pandas as pd
import tushare as ts
import akshare as ak

# Tushare token
_TS_TOKEN = 'ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f'

# ──────────────────────────────────────────────
# 内部工具
# ──────────────────────────────────────────────

def _code_to_akshare_symbol(ts_code: str) -> str:
    """将 Tushare 格式 ts_code（如 000001.SZ）转为 AKShare 腾讯格式（如 sz000001）"""
    code, market = ts_code.split('.')
    prefix = 'sh' if market == 'SH' else 'sz'
    return prefix + code


def _normalize_akshare_df(df: pd.DataFrame, ts_code: str, name: str = '') -> pd.DataFrame:
    """
    将 AKShare 腾讯数据源返回的 DataFrame 标准化为项目统一格式。
    AKShare 腾讯字段: date, open, close, high, low, amount
    """
    code = ts_code.split('.')[0]
    df = df.copy()
    # date -> trade_date (YYYYMMDD 格式字符串)
    df['trade_date'] = pd.to_datetime(df['date']).dt.strftime('%Y%m%d')
    df['ts_code'] = ts_code
    df['name'] = name
    # amount 在腾讯接口里实际是成交量（手），对应原来的 vol
    df.rename(columns={'amount': 'vol'}, inplace=True)
    df['amount'] = None  # 腾讯接口不提供成交额，置空

    cols = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'name']
    # 只保留存在的列
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    df = df.sort_values('trade_date').reset_index(drop=True)
    return df


def _normalize_tushare_df(df: pd.DataFrame, name: str = '') -> pd.DataFrame:
    """将 Tushare pro_bar 返回的 DataFrame 标准化为项目统一格式。"""
    df = df.copy()
    df['name'] = name
    # Tushare 返回降序，转为升序
    df = df.sort_values('trade_date').reset_index(drop=True)
    cols = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'name']
    cols = [c for c in cols if c in df.columns]
    return df[cols]


# ──────────────────────────────────────────────
# 股票列表
# ──────────────────────────────────────────────

def get_stock_list_ak() -> pd.DataFrame:
    """
    AKShare 获取 A 股股票列表。
    返回字段：ts_code, symbol, name
    """
    df = ak.stock_info_a_code_name()  # 字段: code, name
    df = df.copy()
    df.rename(columns={'code': 'symbol'}, inplace=True)
    # 补充 ts_code 和 list_date（腾讯接口无上市日期，置空）
    df['ts_code'] = df['symbol'].apply(
        lambda c: c + '.SH' if c.startswith('6') else c + '.SZ'
    )
    df['list_date'] = ''
    return df[['ts_code', 'symbol', 'name', 'list_date']]


def get_stock_list_ts() -> pd.DataFrame:
    """
    Tushare 获取 A 股股票列表（备用）。
    返回字段：ts_code, symbol, name, list_date
    """
    ts.set_token(_TS_TOKEN)
    pro = ts.pro_api(_TS_TOKEN)
    df = pro.stock_basic(exchange='', list_status='L',
                         fields='ts_code,symbol,name,list_date')
    return df


def get_stock_list(retry: int = 3) -> pd.DataFrame:
    """
    获取 A 股股票列表，AKShare 优先，失败则切换 Tushare。
    返回字段：ts_code, symbol, name, list_date
    """
    for attempt in range(retry):
        try:
            df = get_stock_list_ak()
            print(f'[数据源] AKShare 获取股票列表成功，共 {len(df)} 条')
            return df
        except Exception as e:
            print(f'[数据源] AKShare 获取股票列表失败 (尝试 {attempt + 1}/{retry}): {e}')
            if attempt < retry - 1:
                time.sleep(2)

    print('[数据源] AKShare 全部失败，切换 Tushare 获取股票列表...')
    try:
        df = get_stock_list_ts()
        print(f'[数据源] Tushare 获取股票列表成功，共 {len(df)} 条')
        return df
    except Exception as e:
        print(f'[数据源] Tushare 获取股票列表也失败: {e}')
        raise


# ──────────────────────────────────────────────
# 日线数据（前复权）
# ──────────────────────────────────────────────

def get_daily_qfq_ak(ts_code: str, name: str = '',
                      start_date: str = '', end_date: str = '') -> pd.DataFrame:
    """
    AKShare 腾讯数据源获取前复权日线数据。
    ts_code: Tushare 格式，如 000001.SZ
    """
    symbol = _code_to_akshare_symbol(ts_code)
    df = ak.stock_zh_a_hist_tx(
        symbol=symbol,
        start_date=start_date if start_date else '19900101',
        end_date=end_date if end_date else '20991231',
        adjust='qfq'
    )
    if df is None or df.empty:
        return pd.DataFrame()
    return _normalize_akshare_df(df, ts_code, name)


def get_daily_qfq_ts(ts_code: str, name: str = '',
                      start_date: str = '', end_date: str = '') -> pd.DataFrame:
    """
    Tushare 获取前复权日线数据（备用）。
    ts_code: Tushare 格式，如 000001.SZ
    """
    ts.set_token(_TS_TOKEN)
    df = ts.pro_bar(
        ts_code=ts_code,
        adj='qfq',
        start_date=start_date,
        end_date=end_date
    )
    if df is None or df.empty:
        return pd.DataFrame()
    return _normalize_tushare_df(df, name)


def get_daily_qfq(ts_code: str, name: str = '',
                   start_date: str = '', end_date: str = '',
                   retry: int = 3, verbose: bool = False) -> pd.DataFrame:
    """
    获取前复权日线数据，AKShare 优先，失败则切换 Tushare。
    返回统一字段：ts_code, trade_date, open, high, low, close, vol, amount, name
    trade_date 格式：YYYYMMDD，升序排列

    verbose=False（默认）：只在失败/降级时打印警告，减少并发日志噪音
    verbose=True         ：打印每只成功信息（单只调试时使用）
    """
    for attempt in range(retry):
        try:
            df = get_daily_qfq_ak(ts_code, name, start_date, end_date)
            if not df.empty:
                if verbose:
                    print(f'[数据源] AKShare 获取 {ts_code} 日线成功，共 {len(df)} 条')
                return df
        except Exception as e:
            print(f'[数据源] AKShare 获取 {ts_code} 失败 (尝试 {attempt + 1}/{retry}): {e}')
            if attempt < retry - 1:
                time.sleep(1)

    print(f'[数据源] AKShare 全部失败，切换 Tushare 获取 {ts_code}...')
    try:
        df = get_daily_qfq_ts(ts_code, name, start_date, end_date)
        if not df.empty:
            print(f'[数据源] Tushare 获取 {ts_code} 日线成功，共 {len(df)} 条')
        return df
    except Exception as e:
        print(f'[数据源] Tushare 获取 {ts_code} 也失败: {e}')
        return pd.DataFrame()


# ──────────────────────────────────────────────
# ETF 数据获取与标准化
# ──────────────────────────────────────────────

def get_etf_list_ak() -> pd.DataFrame:
    """
    AKShare 新浪数据源获取全市场 ETF 列表。
    使用新浪接口（fund_etf_category_sina）代替东方财富接口（fund_etf_spot_em），
    避免后者依赖 PyMiniRacer JS 引擎导致在 macOS Apple Silicon 上崩溃。
    返回字段：code, name, ts_code
    """
    df = ak.fund_etf_category_sina(symbol='ETF基金')
    df = df.copy()
    # 新浪返回的代码格式为 sh510300 / sz159915，需拆分为纯数字 code
    df['code'] = df['代码'].str[-6:]
    df.rename(columns={'名称': 'name'}, inplace=True)
    # 补充 ts_code：沪市 5 开头 → .SH，其余（1/2/3 开头）→ .SZ
    df['ts_code'] = df['代码'].apply(
        lambda c: c[-6:] + '.SH' if c.startswith('sh') else c[-6:] + '.SZ'
    )
    return df[['code', 'name', 'ts_code']].reset_index(drop=True)


def _parse_etf_df(df: pd.DataFrame, code: str, name: str) -> pd.DataFrame:
    """
    将 fund_etf_hist_sina 返回的 DataFrame 标准化为项目统一格式。
    新浪接口字段：date, open, high, low, close, volume, amount（均为英文，无需中文映射）
    """
    df = df.copy()
    # 新浪接口 volume 对应成交量（手），对齐项目 vol 字段
    df.rename(columns={'volume': 'vol'}, inplace=True)
    ts_code = code + '.SH' if str(code).startswith('5') else code + '.SZ'
    df['trade_date'] = pd.to_datetime(df['date']).dt.strftime('%Y%m%d')
    df['ts_code'] = ts_code
    df['name'] = name
    cols = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'name']
    cols = [c for c in cols if c in df.columns]
    return df[cols].sort_values('trade_date').reset_index(drop=True)


def _sina_etf_symbol(code: str) -> str:
    """将纯数字代码转为新浪格式：510300 → sh510300，159915 → sz159915"""
    return ('sh' if str(code).startswith('5') else 'sz') + code


def get_etf_daily_ak(code: str, name: str = '',
                     start_date: str = '', end_date: str = '',
                     retry: int = 3) -> pd.DataFrame:
    """
    AKShare 新浪数据源获取单只 ETF 日线数据，支持自动重试。
    注意：新浪接口不支持 start_date/end_date 过滤，返回全量历史（由调用方过滤）。
    code  : 纯数字代码，如 '510300'
    retry : 失败后最大重试次数（默认 3）
    返回统一字段：ts_code, trade_date, open, high, low, close, vol, amount, name
    """
    symbol = _sina_etf_symbol(code)
    for attempt in range(retry):
        try:
            df = ak.fund_etf_hist_sina(symbol=symbol)
            if df is not None and not df.empty:
                result = _parse_etf_df(df, code, name)
                # 按日期范围过滤（新浪接口不支持服务端过滤，在客户端处理）
                if start_date:
                    result = result[result['trade_date'] >= start_date]
                if end_date:
                    result = result[result['trade_date'] <= end_date]
                return result.reset_index(drop=True)
            print(f'[数据源] ETF {code} 返回空数据 (尝试 {attempt + 1}/{retry})')
        except Exception as e:
            print(f'[数据源] ETF {code} 获取失败 (尝试 {attempt + 1}/{retry}): {e}')

        if attempt < retry - 1:
            wait = 2 ** attempt  # 指数退避：1s、2s、4s
            time.sleep(wait)

    return pd.DataFrame()


# ──────────────────────────────────────────────
# 测试入口
# ──────────────────────────────────────────────

if __name__ == '__main__':
    # 测试股票列表
    # print('=== 测试股票列表 ===')
    # stock_list = get_stock_list()
    # print(stock_list)

    etf_list=get_etf_list_ak()
    print(etf_list)

    # 测试日线数据
    # print('\n=== 测试日线数据（000001.SZ 平安银行）===')
    # df = get_daily_qfq('000001.SZ', name='平安银行',
    #                     start_date='20230101', end_date='20230110')
    # print(df)
