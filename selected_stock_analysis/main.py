# -*- coding: utf-8 -*-

# 自选股分析监控
# 对自选股进行分组：上升通道，下降通道，低价股，绩优股，筹码集中
# 对不同组的股票按需进行监控  均线，极值点，

import pandas as pd
import numpy as np
import pandas as pd
from docx.shared import Cm

from analysis_util.output_document import Doc
from analysis_util.plot_k_line import save_k_line
from selected_stock_analysis.stock_classification import get_up_trend_stocks


def output_doc(df, file_path):
    # doc文档
    doc = Doc()
    for line in df.values:
        print(line)
        doc.add_heading('，'.join(line))
        symbol = line[0]

        # 画出其最近100天，300天，1000天日线图
        save_k_line(symbol, 100, './resources/kline100.png')
        save_k_line(symbol, 300, './resources/kline300.png')
        save_k_line(symbol, 1000, './resources/kline1000.png')
        doc.add_picture('./resources/kline100.png', width=Cm(10))
        doc.add_picture('./resources/kline300.png', width=Cm(10))
        doc.add_picture('./resources/kline1000.png', width=Cm(10))

    # 保存文档
    doc.save(file_path)


if __name__ == '__main__':
    # 获取股票池
    # file = 'stock_pool2023.txt'
    file = '自选股.csv'

    path = './classification/'

    # 先进行自选股分组
    # 上升通道股票
    get_up_trend_stocks(file)

    # 超短线上升通道
    df = pd.read_csv(path + '超短线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '超短线上升通道%s.docx' % (file.split('.')[0]))

    # 短线上升通道
    df = pd.read_csv(path + '短线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '短线上升通道%s.docx' % (file.split('.')[0]))

    # 中线上升通道
    df = pd.read_csv(path + '中线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '中线上升通道%s.docx' % (file.split('.')[0]))

    # 中长线上升通道
    df = pd.read_csv(path + '中长线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '中长线上升通道%s.docx' % (file.split('.')[0]))

    # 长线上升通道
    df = pd.read_csv(path + '长线上升通道%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '长线上升通道%s.docx' % (file.split('.')[0]))

    # 中期反弹
    df = pd.read_csv(path + '中期反弹%s.csv' % (file.split('.')[0]), dtype={'symbol': np.str})
    # 输出到文档
    output_doc(df, path + '中期反弹%s.docx' % (file.split('.')[0]))