# -*- coding: utf-8 -*-

# 计算股票交易价格序列中的极值点（高点，低点）

from scipy.signal import argrelextrema, argrelmin, argrelmax,savgol_filter
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
    print(list[argrelmin(list)])

    # plt.plot(range(0, len(list)), list)
    # plt.scatter(
    #     argrelmin(list),
    #     list[argrelmin(list)],
    #     c='red'
    # )
    #
    # plt.show()

    # return [argrelmin(list), x[argrelmin(list)]]
    return list[argrelmin(list)]

# 求导，计算斜率的变化
def cal_dydx(y):
    # Simple interpolation of x and y
    x = [i for i in range(1, len(y) + 1)]
    f = interp1d(x, y)
    x_fake = np.arange(1.1, len(y), 0.1)
    print(type(x_fake[0]))
    print(np.where(x_fake == 2.1))

    # derivative of y with respect to x
    # df_dx = derivative(f, x_fake, dx=1e-6)
    df_dx = derivative(f, x_fake, dx=1e-6)

    print(df_dx)

    # Plot
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.errorbar(x, y, fmt="o", color="blue", label='Input data')
    ax1.errorbar(x_fake, f(x_fake), label="Interpolated data", lw=2)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    ax2.errorbar(x_fake, df_dx, lw=2)
    ax2.errorbar(x_fake, np.array([0 for i in x_fake]), ls="--", lw=2)
    ax2.set_xlabel("x")
    ax2.set_ylabel("dy/dx")

    leg = ax1.legend(loc=2, numpoints=1, scatterpoints=1)
    leg.draw_frame(False)
    plt.show()

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
        [70.6744, 72.22, 70.8725, 70.8428, 71.1896, 71.1599, 69.9313, 72.8244, 71.9525, 68.7621, 68.9206, 69.2179,
         68.663, 70.2483, 74.7961, 75.2222, 73.9143, 74.7169, 76.6985, 80.5626, 81.494, 81.4841, 80.8203, 80.7608,
         81.7913, 81.2463, 85.5068, 85.913, 85.5068, 83.6242, 83.218, 84.516, 85.804, 85.0114, 83.9215, 91.6894,
         91.9371,
         90.7085, 91.0652, 86.6561, 85.0312, 86.5769, 83.0199, 82.1479, 82.4947, 80.85, 80.21, 81.39, 81.25, 81.18,
         78.15, 76.55, 77.93, 79.2, 75.52, 74.17, 71.38, 71.86, 69.42, 69.1, 70.18, 70.78, 70.07, 69.86, 69.14, 70.4,
         72.28, 71.38, 71.48, 71.1, 69.91, 69.69, 70.05, 69.63, 69.09, 70.8, 71.15, 70.16, 69.6, 72.98, 73.3, 72.92,
         70.29, 70.92, 70.17, 70.28, 70.31, 70.42, 67.97, 67.82, 64.55, 65.29, 66.05, 64.82, 63.69, 62.87, 62.3, 64.99,
         63.52, 63.47, 62.72, 58.89, 59.4, 59.32, 61.31, 62.38, 62.68, 62.13, 61.2, 61.7, 60.83, 57.16, 57.55, 59.29,
         57.56, 55.38, 56.58, 61.19, 62.44, 62.01, 63.82, 63.94, 63.32, 62.6, 63.16, 63.59, 62.52, 64.04, 65.17, 64.77,
         65.26, 62.9, 63.15, 62.43, 61.8, 61.71, 61.68, 63.68, 62.7, 65.3, 65.73, 65.98, 68.58, 69.75, 69.48, 72.79,
         71.57, 73.55, 77.73, 77.3, 78.1, 78.3, 75.13, 78.0, 85.8, 89.94, 88.3, 89.69, 86.95, 85.91, 84.42, 82.53,
         82.66,
         85.12, 83.7, 85.79, 85.79, 85.58, 83.82, 85.8, 88.11, 87.9, 86.43, 83.58, 82.77, 83.01, 81.55, 81.13, 81.48,
         80.3, 78.48, 77.26, 76.5, 78.15, 81.0, 84.33, 85.26, 84.79, 85.75, 84.31, 85.6, 84.23, 85.93, 84.5, 83.72,
         82.89, 82.8, 83.18, 82.32, 81.68, 80.2, 78.3, 78.83, 77.8, 76.18, 78.0, 75.57, 74.11, 73.66, 72.1, 71.85,
         74.66,
         75.29, 76.43, 75.93, 75.3, 75.94, 75.7, 76.06, 75.33, 75.93, 76.26, 73.98, 74.4, 72.49, 71.3, 69.35, 69.84,
         68.34, 68.48, 68.45, 67.69, 66.68, 65.63, 64.76, 64.72, 63.69, 64.67, 65.55, 62.83, 62.88, 62.98, 62.85, 63.05,
         63.19, 61.63, 63.07, 62.0, 61.9, 61.57, 62.72, 64.06, 63.56, 62.0, 61.6, 61.55, 60.13, 59.73, 58.31, 58.62,
         59.48, 58.24, 58.75, 59.02, 58.54, 57.82, 61.0, 62.09, 63.84, 64.1, 64.75, 64.01, 63.29, 62.24, 61.28, 62.03,
         61.78, 59.54, 58.99, 61.85, 61.76, 61.1, 59.96, 59.9, 61.8, 61.75, 60.89, 63.75, 62.9, 62.64, 62.69, 63.0,
         62.4,
         64.43, 63.67, 67.48, 67.59, 68.21, 68.8, 75.34]

    )

    # 计算极大值，极小值
    # y = cal_extreme_min_value(data)
    y = cal_extreme_min_value(data)
    print(y)
    y2 = cal_extreme_min_value(y)
    print(y2)


