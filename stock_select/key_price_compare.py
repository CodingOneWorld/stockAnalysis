# -*- coding: utf-8 -*-

# 判断股票的关键价位
# 如支撑位，压力位，均线位置等
# 计算当前价格最高值，最低值，以及均线数据，进行比较
from analysis_util.cal_mean_line import cal_mean_line

if __name__ == '__main__':
    mean_list = cal_mean_line('000001', 3000)
    print(mean_list)

    # 获取股票最近的价格




