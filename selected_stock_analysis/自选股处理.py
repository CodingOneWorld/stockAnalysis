# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# 对自选股列表  股票池列表进行处理


if __name__ == '__main__':
    file = './meta_selected_stocks/自选股202308.csv'
    df = pd.read_csv(file, dtype={'symbol': np.str}, delimiter=',')
    print(df)

    df['symbol']=df['symbol'].apply(lambda x:x[2:])

    print(df)

    df.to_csv('自选股202308.csv',index=0)
