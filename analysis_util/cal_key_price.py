# -*- coding: utf-8 -*-

# 计算股票交易价格序列中的极值点（高点，低点）

from scipy.signal import argrelextrema, argrelmin, argrelmax, savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
from scipy.misc import derivative

from analysis_util.cal_stock_trend import get_stock_price
from analysis_util.general_utils import get_stock_code


# 计算最小值
def cal_min_value(list):
    return min(list)


# 计算极大值
def cal_extreme_max_value(list):
    print(argrelmax(list))

    plt.plot(range(0, len(list)), list)
    plt.scatter(
        argrelmax(list),
        list[argrelmax(list)],
        c='black'
    )

    plt.show()

    return list[argrelmax(list)]


# 计算极小值
def cal_extreme_min_value(list):
    # print(argrelmin(list))
    # print(list[argrelmin(list)])

    plt.plot(range(0, len(list)), list)
    plt.scatter(
        argrelmin(list),
        list[argrelmin(list)],
        c='red'
    )

    plt.show()

    # return [argrelmin(list), x[argrelmin(list)]]
    return [argrelmin(list), list[argrelmin(list)]]


# 计算极大值另一种方法（废弃）
def cal_extreme_max_value2(list):
    peaks, _ = signal.find_peaks(list, distance=5)  # distance表示极大值点两两之间的距离至少大于等于5个水平单位

    print(peaks)
    # print(len(peaks))  # the number of peaks

    plt.figure(figsize=(20, 5))
    plt.plot(list)
    plt.scatter(
        peaks,
        list[peaks],
        c='red'
    )
    # for i in range(len(peaks)):
    #     plt.plot(peaks[i], list[peaks[i]], '*', markersize=10)
    plt.show()

    # return [peaks, x[peaks]]
    return list[peaks]


if __name__ == '__main__':
    code = get_stock_code('新日股份')
    his_price=get_stock_price(code,'low')['low'].values
    data=his_price[-100:]
    # print(data)

    min_v=cal_min_value(data)
    print(min_v)


    # # 计算极大值，极小值
    y = cal_extreme_min_value(data)
    # y = cal_extreme_max_value(data)
    # print(y)
    y2 = cal_extreme_min_value(y[1])
    y3 = cal_extreme_min_value(y2[1])
    # print(y2)

    # 计算股价变化趋势
    # cal_dydx(y)
