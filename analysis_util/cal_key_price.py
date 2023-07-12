# -*- coding: utf-8 -*-

# 计算股票交易价格序列中的极值点（高点，低点）

from scipy.signal import argrelextrema, argrelmin
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
from scipy.misc import derivative


def cal_max_value(list):
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


def cal_min_value(list):
    print(argrelmin(list))

    plt.plot(range(0, len(list)), list)
    plt.scatter(
        argrelmin(list),
        list[argrelmin(list)],
        c='red'
    )
    plt.show()

    # return [argrelmin(list), x[argrelmin(list)]]
    return list[argrelmin(list)]


if __name__ == '__main__':
    data = np.array(
        # [12.16, 12.4967, 12.6056, 13.0116, 12.8037, 12.9324, 13.071, 13.2097, 13.8137, 13.5563, 13.586, 13.7147, 13.5959,
        #  13.8632, 13.9226, 13.8533, 14.0613, 13.7543, 13.7048, 13.5563, 13.7444, 13.6157, 13.1008, 13.3087, 13.081, 12.675,
        #  12.8235, 12.8136, 12.6254, 12.7641, 12.8334, 12.7641, 12.7344, 12.4967, 12.3284, 12.4175, 12.7839, 12.8433,
        #  13.2691, 13.2097, 13.2889, 13.2196, 13.5464, 13.4869, 13.5563, 13.0215, 13.3681, 12.8037, 13.0909, 12.8928,
        #  13.2691, 12.9522, 13.0215, 13.8137, 13.6454, 13.5365, 12.4967, 12.4274, 12.3086, 11.7639, 11.9125, 11.5263,
        #  11.6649, 11.7837, 11.9224, 12.0709, 12.0115, 11.655, 11.5362, 11.8135, 12.9918, 12.9918, 12.7245, 12.9324, 12.972,
        #  13.1701, 12.6353, 12.9126, 12.9126, 12.8631, 12.7839, 12.5957, 12.2591, 11.8729, 11.6649, 11.4273, 11.5362,
        #  11.3282, 11.0807, 10.4964, 10.8925, 11.0114, 10.9916, 11.1203, 11.1401, 11.0609, 10.8727, 10.8727, 10.9222, 10.744,
        #  10.9123, 10.8925, 10.8925, 11.0114, 10.546, 10.4073, 9.7934, 9.9815, 9.833, 10.0211, 9.9518, 10.1202, 10.1499,
        #  10.1598, 9.8231, 9.7241, 8.7536, 8.1595, 8.516, 8.308, 8.7041, 8.922, 8.8923, 8.8824, 8.9616, 9.0507, 9.0111,
        #  9.1596, 9.1299, 9.1794, 9.229, 9.2091, 9.328, 9.3577, 8.9121, 9.1002, 9.1299, 9.1101, 9.1794, 9.3577, 9.427,
        #  9.6151, 9.6746, 9.5359, 9.4765, 9.2488, 9.4171, 9.6349, 9.5359, 9.6448, 9.7538, 9.8726, 9.932, 9.9518, 9.7736,
        #  10.1895, 10.1499, 10.14, 10.57, 10.32, 10.34, 10.17, 10.34, 10.08, 9.94, 10.03, 10.15, 9.84, 9.75, 9.9, 9.93, 9.9,
        #  10.2, 10.34, 10.31, 10.41, 10.33, 10.31, 10.25, 10.4, 10.66, 10.49, 10.74, 10.37, 10.37, 10.58, 10.86, 10.79,
        #  10.74, 10.75, 11.03, 11.02, 11.2, 11.23, 11.18, 11.44, 11.14, 11.15, 11.07, 10.52, 10.58, 10.4, 10.39, 10.38,
        #  10.31, 10.08, 10.31, 10.29, 10.41, 10.48, 10.3, 10.28, 10.17, 9.94, 9.64, 9.44, 9.23, 9.32, 9.34, 9.33, 9.17, 8.9,
        #  9.11, 8.84, 8.85, 8.72, 8.5, 8.63, 8.94, 9.06, 9.21, 9.34, 9.38, 9.32, 9.41, 9.36, 9.22, 9.25, 9.47, 9.56, 9.28,
        #  9.47, 9.62, 9.67, 9.67, 9.78, 9.74, 9.67, 9.64, 9.5, 9.55, 9.55, 9.86, 10.02, 10.19, 10.02, 10.03, 9.98, 9.98,
        #  9.89, 9.82, 9.72, 9.92, 9.86, 9.96, 9.92, 10.17, 10.13, 10.07, 10.07, 9.98, 10.0, 9.9, 9.92, 10.0, 9.77, 9.44,
        #  9.54, 9.49, 9.29, 9.24, 9.39, 9.42, 9.32, 9.27, 9.29, 9.54, 9.55, 9.58, 9.58, 9.61, 9.68, 9.54, 9.65, 9.65, 9.74,
        #  9.89, 9.9, 10.02, 10.01
        #  ]
        [
         5.57, 5.53, 5.3, 5.26, 5.3, 5.11, 4.97, 4.78, 4.71, 4.75, 4.76, 4.69, 4.63, 4.53, 4.65, 4.48, 4.42, 4.45, 4.32,
         4.37, 4.5, 4.55, 4.63, 4.72, 4.68, 4.61, 4.66, 4.62, 4.55, 4.57, 4.66, 4.75, 4.51, 4.73, 4.83, 4.89, 4.83, 4.9,
         4.94, 4.9, 4.83, 4.76, 4.79, 4.84, 5.0, 4.94, 4.98, 4.92, 4.95, 4.9, 4.88, 4.86, 4.83, 4.76, 4.88, 4.92, 4.93,
         4.92, 4.96, 4.97, 4.9, 4.84, 4.82, 4.88, 4.81, 4.78, 4.85, 4.81, 4.54, 4.59, 4.58, 4.5, 4.51, 4.58, 4.58, 4.53,
         4.52, 4.54, 4.62, 4.57, 4.67, 4.72, 4.8, 4.74, 4.71, 4.75, 4.75, 4.86, 4.88, 4.89, 4.99, 4.97, 5.47, 5.36,
         5.59, 5.6, 5.67, 5.59, 5.63, 5.65, 5.78, 5.79, 5.71, 5.79, 5.91, 5.79, 5.71, 5.78, 5.83, 5.82, 5.79, 5.72,
         5.67, 5.73, 5.82, 5.78, 5.77, 5.72, 5.6, 5.7, 5.73, 5.67, 5.71, 5.68, 5.74, 5.64, 5.73, 5.86, 6.02, 6.04, 6.14,
         6.25, 6.12, 6.08, 6.09, 6.13, 6.18, 6.23, 6.26, 6.35, 6.2, 6.24, 6.17, 6.27, 6.07, 6.12, 6.08, 6.01, 6.02, 6.1,
         5.77, 5.93, 5.72, 5.6, 5.57, 5.93, 6.0, 6.08, 6.03, 6.07, 6.05, 6.22, 5.87, 5.95, 5.94, 5.99
         ]
    )

    # y = cal_min_value(data)
    y = cal_max_value(data)
    print(y)
    x = [i for i in range(1, len(y) + 1)]
    print(x)
    # cal_min_value(x)

    # # Simple interpolation of x and y
    # f = interp1d(x, y)
    # x_fake = np.arange(1.1, len(y), 0.1)
    # print(type(x_fake[0]))
    # print(np.where(x_fake == 2.1))
    #
    # # derivative of y with respect to x
    # # df_dx = derivative(f, x_fake, dx=1e-6)
    # df_dx = derivative(f, x_fake, dx=1e-6)
    #
    # print(df_dx)
    #
    # # Plot
    # fig = plt.figure()
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212)
    #
    # ax1.errorbar(x, y, fmt="o", color="blue", label='Input data')
    # ax1.errorbar(x_fake, f(x_fake), label="Interpolated data", lw=2)
    # ax1.set_xlabel("x")
    # ax1.set_ylabel("y")
    #
    # ax2.errorbar(x_fake, df_dx, lw=2)
    # ax2.errorbar(x_fake, np.array([0 for i in x_fake]), ls="--", lw=2)
    # ax2.set_xlabel("x")
    # ax2.set_ylabel("dy/dx")
    #
    # leg = ax1.legend(loc=2, numpoints=1, scatterpoints=1)
    # leg.draw_frame(False)
    # plt.show()
