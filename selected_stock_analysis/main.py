# -*- coding: utf-8 -*-

# 自选股分析监控
# 对自选股进行分组：上升通道，下降通道，低价股，绩优股，筹码集中
# 对不同组的股票按需进行监控  均线，极值点，

import pandas as pd

if __name__ == '__main__':
    # 上升通道股票
    # 判断当前价格是否靠近均线，靠近之前的极值点
    # 获取股票池
    df = pd.read_csv('自选股.csv', dtype={'symbol': np.str})
