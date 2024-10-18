# -*- coding: utf-8 -*-

# 自选股分析监控
# 对自选股进行分组：上升通道，下降通道，低价股，绩优股，筹码集中
# 对不同组的股票按需进行监控  均线，极值点，

import pandas as pd
import numpy as np
import pandas as pd
from docx.shared import Cm

from analysis_util.output_document import Doc, output_doc
from analysis_util.plot_k_line import save_k_line
from selected_stock_analysis.rebound_classification import get_l10_rebound_stock
from selected_stock_analysis.stock_classification import get_up_trend_stocks
from selected_stock_analysis.up_classification import get_l10_up_stock

if __name__ == '__main__':
    # 获取股票池
    files = []
    file = 'stock_pool2023.txt'
    files.append(file)
    file = '自选股.csv'
    files.append(file)

    path = './classification/'

    for file in files:
        # 先进行自选股分组
        # 上升通道股票
        get_up_trend_stocks(file)

        # 超短线上升通道
        df = pd.read_csv(path + '超短线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '超短线上升通道%s.docx' % (file.split('.')[0]))

        # 短线上升通道
        df = pd.read_csv(path + '短线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '短线上升通道%s.docx' % (file.split('.')[0]))

        # 中线上升通道
        df = pd.read_csv(path + '中线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '中线上升通道%s.docx' % (file.split('.')[0]))

        # 中长线上升通道
        df = pd.read_csv(path + '中长线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '中长线上升通道%s.docx' % (file.split('.')[0]))

        # 长线上升通道
        df = pd.read_csv(path + '长线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '长线上升通道%s.docx' % (file.split('.')[0]))

        # 中期反弹
        df = pd.read_csv(path + '中期反弹%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str_})
        # 输出到文档
        output_doc(df, path + '中期反弹%s.docx' % (file.split('.')[0]))

        # 10日短期反弹
        get_l10_rebound_stock(file, path + '%s_10日短线反弹股票.docx' % (file.split('.')[0]))

        # 10日短线上升通道
        # get_l10_up_stock(file, path + '%s_10日短线上升通道股票.docx' % (file.split('.')[0]))
