# -*- coding: utf-8 -*-

# 计算股票交易价格序列中的极值点（高点，低点）

from scipy.signal import argrelextrema, argrelmin, argrelmax, savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
from scipy.misc import derivative


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
    data = np.array(
        [
            6.3331, 6.096, 6.1256, 6.1059, 6.2047, 6.2146, 6.096, 6.0071, 6.0762, 6.1256, 6.175, 6.1158, 6.017, 6.0762,
            6.0762, 6.0071, 5.8589, 5.6415, 5.6218, 5.6909, 5.7403, 5.6415, 5.5625, 5.5625, 5.77, 5.9577, 5.849, 5.6119,
            5.5724, 5.5328, 5.6218, 5.6514, 5.7304, 5.7798, 5.7304, 5.6415, 5.5724, 5.5526, 5.3945, 5.4439, 5.4834,
            5.4538, 5.4834, 5.3254, 5.434, 5.5131, 5.5131, 5.5625, 5.602, 5.5822, 5.602, 5.602, 5.6712, 5.6613, 5.7304,
            5.7304, 5.7403, 5.7403, 5.7206, 5.681, 5.6514, 5.6613, 5.6415, 5.6514, 5.7502, 5.7502, 5.7403, 5.7403,
            5.8589, 5.849, 5.8391, 5.8391, 5.8984, 5.7601, 5.7798, 5.7798, 5.8095, 5.7107, 5.5822, 5.5921, 5.523,
            5.4439, 5.4637, 5.4933, 5.5427, 5.4637, 5.3649, 5.4044, 5.5131, 5.5625, 5.5822, 5.5427, 5.5526, 5.5526,
            5.5724, 5.5724, 5.6218, 5.77, 5.77, 5.7897, 5.9182, 5.8984, 5.9182, 5.9083, 5.9676, 5.9478, 5.928, 6.1355,
            6.2936, 6.1454, 6.175, 6.175, 6.175, 6.2343, 6.2146, 6.1454, 6.096, 6.1948, 6.2541, 6.2343, 6.2343, 6.1948,
            6.1355, 6.175, 6.2442, 6.2047, 6.2146, 6.1849, 6.0268, 6.0466, 6.0071, 5.8885, 5.8095, 5.6909, 5.7601,
            5.6909, 5.7403, 5.7798, 5.8292, 5.8786, 5.8391, 5.8688, 5.8786, 5.8984, 5.8391, 5.8885, 5.8984, 5.9676,
            5.8589, 5.77, 5.7996, 5.6712, 5.6909, 5.7206, 5.6415, 5.602, 5.7304, 5.849, 5.9379, 6.0762, 5.9972, 5.8589,
            5.6909, 5.681, 5.7107, 5.849, 5.7601, 5.6514, 5.6909, 5.602, 5.523, 5.5328, 5.5427, 5.5328, 5.4538, 5.4637,
            5.5328, 5.5526, 5.5625, 5.5032, 5.4637, 5.4439, 5.4044, 5.3846, 5.3846, 5.3451, 5.4044, 5.5328, 5.5328,
            5.4143, 5.3945, 5.3846, 5.4637, 5.5822, 5.5328, 5.5822, 5.602, 5.6316, 5.5526, 5.5724, 5.5526, 5.6218,
            5.7304, 5.7107, 5.77, 5.76, 5.76, 5.8, 5.8, 5.79, 5.76, 5.78, 5.81, 5.74, 5.75, 5.72, 5.75, 5.82, 5.82,
            5.72, 5.71, 5.69, 5.81, 5.76, 5.73, 5.8, 5.87, 5.87, 5.88, 5.88, 5.82, 5.78, 5.74, 5.68, 5.67, 5.55, 5.57,
            5.55, 5.5, 5.58, 5.49, 5.43, 5.44, 5.35, 5.3, 5.22, 5.34, 5.4, 5.51, 6.06
        ]
    )

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
