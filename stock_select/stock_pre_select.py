# -*- coding: utf-8 -*-
"""
股票预筛选（第一层：资格过滤）

只做"资格审查"，快速过滤掉明显不符合条件的股票，不查财务数据。
筛选条件：
  1. 只保留主板（symbol 以 0 或 6 开头）
  2. 排除 ST / 退市股（名称含 ST 或 退）
  3. 排除近3年上市的新股（上市日期通过 Tushare 补充，AKShare 无此字段）

输出：stock_pool.txt，格式为 symbol,stock_name
作为第二层精筛选（select_by_income / select_by_profit）的输入候选池。
"""
import datetime
import sqlite3

import pandas as pd
import tushare as ts

# 以下 import 供注释掉的财务过滤代码使用，重新启用时取消注释
# from fundamental_data.get_income import get_income_of_latest_years
# from fundamental_data.get_profit import get_profit_of_latest_years

from util.utils_common import get_dbpath_by_repo

DB_PATH = get_dbpath_by_repo()
_TS_TOKEN = 'ad065353df4c0c0be4cb76ee375140b21e37a434b33973a03ecd553f'


def build_stock_pool(output_file: str = 'stock_pool.txt',
                     exclude_new_years: int = 3) -> pd.DataFrame:
    """
    生成预筛选候选股票池。

    exclude_new_years : 排除最近 N 年内上市的新股（默认3年）
    output_file       : 结果输出路径
    返回              : 候选股票 DataFrame（symbol, name, list_date）
    """
    # ── Step 1：从数据库读取全部股票，过滤非主板 ──────────────────────
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT symbol, name FROM stock_list', conn)
    conn.close()

    # 只保留主板
    #   深市主板：000xxx / 001xxx / 002xxx / 003xxx
    #   沪市主板：600xxx / 601xxx / 603xxx / 605xxx
    # 排除：创业板（300/301）、科创板（688）、北交所（4/8/9开头）
    main_board_mask = (
        df['symbol'].str.startswith('000') |
        df['symbol'].str.startswith('001') |
        df['symbol'].str.startswith('002') |
        df['symbol'].str.startswith('003') |
        df['symbol'].str.startswith('600') |
        df['symbol'].str.startswith('601') |
        df['symbol'].str.startswith('603') |
        df['symbol'].str.startswith('605')
    )
    df = df[main_board_mask].reset_index(drop=True)
    print(f'[预筛选] 主板股票数：{len(df)} 只')

    # ── Step 2：排除 ST / 退市股（向量化，覆盖 *ST / ST / 退 等格式）──
    st_mask = df['name'].str.contains('ST|退', na=False)
    df = df[~st_mask].reset_index(drop=True)
    print(f'[预筛选] 排除 ST/退市后剩余：{len(df)} 只')

    # ── Step 3：补充 list_date，排除近N年新股 ─────────────────────────
    cutoff_date = (
        datetime.date.today() - datetime.timedelta(days=exclude_new_years * 365)
    ).strftime('%Y%m%d')
    print(f'[预筛选] 排除近{exclude_new_years}年新股，截止日期：{cutoff_date}')

    try:
        ts.set_token(_TS_TOKEN)
        pro = ts.pro_api()
        ts_df = pro.stock_basic(
            exchange='', list_status='L',
            fields='symbol,list_date'
        )
        df = df.merge(ts_df[['symbol', 'list_date']], on='symbol', how='left')

        # list_date 为空/NaN → 日期未知，保守保留；否则与截止日期比较
        date_ok = (
            df['list_date'].isna() |
            (df['list_date'] == '') |
            (df['list_date'] <= cutoff_date)
        )
        df = df[date_ok].reset_index(drop=True)
        print(f'[预筛选] 排除近{exclude_new_years}年新股后剩余：{len(df)} 只')
    except Exception as e:
        print(f'[预筛选] 获取上市日期失败，跳过新股过滤: {e}')
        df['list_date'] = ''

    # ── Step 4（已迁移至精筛选层）：收入和净利润近5年均 >= 0 ──────────────
    # 该逻辑已移至 select_by_income / select_by_profit（精筛选增速≥10%已包含此条件）
    # 如需在预筛选层做财务粗筛，取消以下注释并恢复顶部 import：
    #
    # stock_list = df[['symbol', 'name']].values
    # qualified = []
    # for s in stock_list:
    #     income_data = get_income_of_latest_years(s[0], 5)
    #     income_ok = all(v >= 0 for v in income_data)
    #     profit_data = get_profit_of_latest_years(s[0], 5)
    #     profit_ok = all(v >= 0 for v in profit_data)
    #     if income_ok and profit_ok:
    #         qualified.append({'symbol': s[0], 'name': s[1]})
    #     else:
    #         print(f'remove: {s[0]} {s[1]}')
    # df = pd.DataFrame(qualified)
    # print(f'[预筛选] 收入和净利润近5年均≥0 剩余：{len(df)} 只')

    # ── Step 5：写入结果文件 ──────────────────────────────────────────
    with open(output_file, 'w', encoding='utf-8') as fw:
        fw.write('symbol,stock_name\n')
        for _, row in df.iterrows():
            fw.write(f'{row["symbol"]},{row["name"]}\n')

    print(f'[预筛选] 候选股票池已写入 {output_file}，共 {len(df)} 只')
    return df[['symbol', 'name']].rename(columns={'name': 'stock_name'}).reset_index(drop=True)


if __name__ == '__main__':
    build_stock_pool()
