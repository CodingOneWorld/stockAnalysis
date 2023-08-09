# -*- coding: utf-8 -*-

# 计算股票交易价格序列中的极值点（高点，低点）

from scipy.signal import argrelextrema, argrelmin, argrelmax, savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
from scipy.misc import derivative


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
    return [argrelmin(list),list[argrelmin(list)]]


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
    data = np.array(
        [
        33.9661, 33.6191, 34.5926, 34.4673, 35.9806, 35.9709, 35.5179, 35.2866, 34.795, 34.2167, 33.3204, 33.2722,
         33.5228, 33.3204, 32.1059, 32.2216, 34.4481, 35.1999, 35.3734, 36.6938, 36.7613, 36.7227, 35.9613, 35.7493,
         35.9517, 36.0384, 36.4432, 35.9131, 35.5661, 35.3541, 34.795, 34.9203, 35.0264, 34.5734, 34.5155, 34.2167,
         34.8914, 35.7878, 36.0962, 35.4697, 35.8553, 35.7975, 36.077, 35.9228, 36.424, 35.1324, 34.9203, 34.824,
         35.5854, 35.3155, 34.824, 34.2746, 34.3902, 34.2071, 33.8119, 34.0047, 34.236, 33.7637, 33.7541, 33.8023,
         34.2167, 33.7926, 34.1975, 34.6987, 34.4095, 35.0071, 34.8722, 35.277, 34.6794, 35.9999, 35.4794, 35.5758,
         35.9709, 35.8071, 37.5227, 37.6288, 37.6866, 37.8794, 38.0239, 37.195, 37.2914, 37.1661, 37.2625, 36.8577,
         36.7613, 36.5203, 36.2505, 36.2697, 36.183, 36.289, 36.6167, 36.1637, 36.2023, 35.6914, 35.7493, 35.73,
         36.0673, 35.9999, 35.9613, 35.5758, 34.8529, 35.0553, 34.7758, 33.7348, 33.7059, 33.7444, 33.5324, 32.8866,
         32.8095, 33.0698, 33.3975, 33.33, 33.2432, 33.1469, 33.2625, 33.3107, 33.224, 33.2625, 33.5035, 33.5999,
         32.6938, 32.9348, 33.0408, 32.9445, 32.5685, 32.2698, 32.1155, 32.1926, 32.983, 33.0505, 32.7517, 32.6071,
         32.4336, 32.2698, 31.8842, 32.3276, 32.8095, 32.7228, 32.4914, 32.0192, 32.2119, 31.9613, 32.5396, 32.9541,
         32.636, 33.3589, 33.2914, 33.33, 33.13, 33.26, 33.4, 33.35, 33.14, 33.03, 33.19, 32.9, 32.81, 32.44, 32.28,
         33.23, 33.23, 32.81, 32.89, 32.83, 32.99,
         33.55, 33.6, 33.57, 34.36, 34.28, 34.41, 34.49, 34.38, 34.52, 34.51,
         34.91, 35.15, 35.85, 35.66, 36.06, 35.75, 35.72, 35.8, 35.67, 36.01, 36.55, 36.66, 36.2, 35.75, 36.21, 36.28,
         36.21, 36.1, 36.39, 37.06, 37.02, 36.95, 37.4, 37.88, 37.59
         ]
    )

    # # 计算极大值，极小值
    y = cal_extreme_min_value(data)
    # y = cal_extreme_max_value(data)
    # print(y)
    y2 = cal_extreme_min_value(y)
    # y3 = cal_extreme_min_value(y2)
    # print(y2)

    # 计算股价变化趋势
    # cal_dydx(y)
