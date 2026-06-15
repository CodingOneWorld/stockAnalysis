# -*- coding: utf-8 -*-
import datetime

from analysis_util.cal_key_price import cal_extreme_min_value
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend
from analysis_util.output_document import output_doc
from selected_stock_analysis.up_classification import (
    compare2mean_window, cal_volume_ratio, cal_single_day_vol_ratio, cal_volume_trend,
)
from trade_data.get_trade_data import get_stock_trade_data
from util.math_util import List_util
import pandas as pd
import numpy as np

import warnings

warnings.filterwarnings("ignore")


def analysis():
    # 斜率分析
    # 一个正常的下跌通道
    return 0


def get_stocklist(file):
    df = pd.read_csv(file, dtype={'symbol': np.str_}, delimiter=',')
    stock_list = df.values
    return stock_list


def compare2exmin(his_price_df):
    # 获取股票历史价格
    his_price = his_price_df['close'].values
    print('极小值：')
    # 仅计算极小值有问题，需要加上最左边的值（防止最左边没有极小值，但股价很低）
    left = his_price[0]
    ex_mins = cal_extreme_min_value(his_price[-10:])[1]
    ex_mins = [left] + ex_mins
    if len(ex_mins) < 2:
        ex_mins = ex_mins + his_price[-1]
    print(ex_mins)
    is_true = List_util.isAZ(ex_mins)
    # is_true=True
    print(is_true)
    return is_true


# 短线（10d）反弹的股票
# 最近 lookback 天数据内，最近 20 天股价斜率 < 0，最近 10 天斜率 > 0
# 最近 10 天股价极低值一个比一个高
# 最近 10 天均在 5 日均线上
def get_l10_rebound_stock(file, path, lookback_days: int = 200):
    """
    lookback_days : 拉取历史数据的天数（默认 200 天，动态取最近数据，
                    不再硬编码固定日期区间）
    """
    # 动态计算结束日期（今天）和开始日期
    end_date = datetime.date.today().strftime('%Y%m%d')
    start_date = (datetime.date.today() - datetime.timedelta(days=lookback_days * 2)
                  ).strftime('%Y%m%d')  # 多取一倍保证足够行数

    stock_list = get_stocklist(file)
    selected_stock = []
    for s in stock_list:
        print(s)
        code = s[0]
        # 获取最近 lookback_days 个交易日数据
        his_price_df = get_stock_trade_data(code, start_date, end_date)
        if his_price_df is None or len(his_price_df) < 20:
            continue
        his_price_df = his_price_df.tail(lookback_days)  # 取最近 N 行
        his_price = his_price_df['close'].values

        # 归一化斜率（单位：收益率/天，可跨股票比较）
        k5   = cal_stock_price_trend(his_price, 5)
        k10  = cal_stock_price_trend(his_price, 10)
        k20  = cal_stock_price_trend(his_price, 20)
        k100 = cal_stock_price_trend(his_price, 100)
        print(f'  斜率 k5={k5:.4f} k10={k10:.4f} k20={k20:.4f} k100={k100:.4f}')

        # 确保有下降通道背景（k20 < -0.002，k100 < 0），且短期反弹（k5/k10 > 0）
        # 归一化后阈值：0.002 ≈ 日均 0.2%；-0.002 ≈ 日均 -0.2%
        if k5 > 0 and k10 > 0 and k20 < -0.002 and k100 < 0:
            # 反弹确认：最近 10 天均在 5 日均线上方
            is_true = compare2mean_window(5, his_price_df.copy(), 10)
            if not is_true:
                continue

            # ── 成交量过滤 ──────────────────────────────────────────
            # 1. 近5日量比（vs 前15日均量）> 1.2：要求近期有放量信号，
            #    说明资金真实介入，而非虚假反弹
            vol_ratio = cal_volume_ratio(his_price_df, recent_days=5, base_days=20)
            # 2. 量趋势斜率：近10日成交量整体方向 > 0（量在逐步放大）
            vol_trend = cal_volume_trend(his_price_df, days=10)
            # 3. 当日量比 > 1.0：最后一根 K 线不能是极度萎缩成交
            today_vr  = cal_single_day_vol_ratio(his_price_df, base_days=5)
            print(f'  量比 vol_ratio={vol_ratio:.2f}  量趋势={vol_trend:.4f}  当日量比={today_vr:.2f}')

            # 满足：近期放量（OR 量趋势上升）且当日量不萎缩
            vol_ok = (vol_ratio > 1.2 or vol_trend > 0) and today_vr > 0.8
            if vol_ok:
                print(f'  >> 入选：{s}')
                selected_stock.append(s)
            else:
                print(f'  >> 量能不足，跳过：vol_ratio={vol_ratio:.2f}')

    if len(selected_stock) > 0:
        print(selected_stock)
        df = pd.DataFrame(selected_stock, columns=['code', 'name'])
        output_doc(df, path)


if __name__ == '__main__':
    # stock_list=['600660']
    # file = 'stock_pool2023.txt'
    file = '自选股202308.csv'

    file_name = file.split('.')[0]
    path = file_name + '_10日短线反弹股票.docx'

    get_l10_rebound_stock(file, path)
