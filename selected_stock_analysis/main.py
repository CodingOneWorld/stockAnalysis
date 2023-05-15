# -*- coding: utf-8 -*-

# 自选股分析监控
# 对自选股进行分组：上升通道，下降通道，低价股，绩优股，筹码集中
# 对不同组的股票按需进行监控  均线，极值点，

import pandas as pd
import numpy as np
import pandas as pd
from selected_stock_analysis.stock_classification import get_up_trend_stocks

if __name__ == '__main__':
    # 获取股票池
    df = pd.read_csv('自选股.csv', dtype={'symbol': np.str})

    # 先进行自选股分组
    # 上升通道股票
    get_up_trend_stocks(df)
    # 中线上升通道
    df = pd.read_csv('自选股.csv', dtype={'symbol': np.str})

