# 股票分析项目

一个基于 Python 的 A 股量化分析系统，实现从数据获取、技术分析、选股筛选到买点检测的完整流程，最终输出 K 线图表、CSV 和 Word 分析报告。

---

## 项目架构

```
stockAnalysis/
├── trade_data/              # 数据获取层：拉取日线数据存入 SQLite
├── analysis_util/           # 分析层：趋势/均线/极值点/K线可视化
├── fundamental_data/        # 基本面层：收入、利润数据获取与分析
├── stock_select/            # 选股层：按收入/利润增长/趋势/价格筛股
├── selected_stock_analysis/ # 自选股监控层：分类 + 买点检测
├── main/                    # 调度层：定时更新数据 + 执行检测
├── util/                    # 工具层：日期/数学/数据库工具
├── constants/               # 常量配置
├── stock_analysis/          # 单股分析脚本
├── news_analysis/           # 新闻分析（研究中）
└── Learn/                   # 学习调研脚本
```

---

## 各模块说明

### trade_data/ — 数据获取
- 数据源：**AKShare（腾讯，主力）+ Tushare Pro（备用）**，均为前复权日线数据
- `data_source.py`：双数据源封装，AKShare 失败自动切换 Tushare
- `get_stock_basic_list.py`：获取 A 股股票列表（排除创业板/科创板/北交所）
- `get_trade_data.py`：获取日线数据并写入 SQLite 数据库
- `main_mac.py`：macOS 上的数据更新入口，每日定时（17:00）触发全量更新

### analysis_util/ — 技术分析
- `cal_stock_trend.py`：趋势分析，对收盘价做线性回归，计算 N 日斜率
- `cal_mean_line.py`：计算 60/88/120/140/180 日移动均线
- `cal_key_price.py`：用 scipy 识别局部极大/极小值（压力位/支撑位）
- `cal_hist_price.py`：计算历史高低点、回撤幅度
- `plot_k_line.py`：用 mplfinance 绘制 K 线图（蜡烛图 + 均线 + 成交量）
- `output_document.py`：将分析结果（含 K 线图）输出为 Word 文档

### fundamental_data/ — 基本面数据
- `get_income.py`：获取历年营业收入数据
- `get_profit.py`：获取历年净利润数据
- `get_ST_stocks.py`：获取 ST 股票列表

### stock_select/ — 选股策略
- `select_by_income.py`：筛选近 5 年收入持续增长（≥10%）的股票
- `select_by_profit.py`：筛选近 5 年净利润持续增长（≥10%）的股票
- `select_by_trend.py`：筛选最近 N 天趋势向上（斜率 ≥ 0.3）的股票
- `select_by_price.py`：筛选从历史高点回撤 ≥ 50% 且长期趋势向上的股票

### selected_stock_analysis/ — 自选股监控
- `stock_classification.py`：将自选股按时间周期分类为超短线/短线/中线/长线上升通道
- `rebound_classification.py`：识别反弹股（短期开始上涨但中长期仍下降）
- `buy_point_detect.py`：检测三类买点
  1. 上升通道回调（接近 5/10/20/30 日均线）
  2. 下降通道前低（接近历史极小值）
  3. 下降通道关键均线（接近 60/140/250 日均线）
- `key_price_compare.py`：当前价格与各均线的距离分析

---

## 数据库设计

数据库路径：`/Users/zhangqi21/DB/stock_data.db`（SQLite）

| 表名 | 内容 |
|---|---|
| `stock_list` | 股票基础信息（ts_code, symbol, name, list_date） |
| `S{code}_daily` | 单股前复权日线数据（trade_date, open, high, low, close, vol, amount, name） |
| `income_all_stocks` | 历年营业收入数据 |
| `profit_all_stocks` | 历年净利润数据 |

---

## 核心算法

| 算法 | 说明 |
|---|---|
| 趋势判断 | 线性回归斜率，≥0.3 为上升，<-0.1 为下降 |
| 均线分析 | 移动平均，判断股价是否在均线上方（允许 10% 天数低于均线） |
| 极值识别 | scipy.signal.argrelmin / argrelmax |
| 买点检测 | 当前价在均线/支撑位的 ±1% 范围内 |
| 反弹识别 | k5>0 且 k10>0，但 k20<-0.05 且 k100<0 |

---

## 运行环境

- Python：`/opt/miniconda3/bin/python`（Python 3.13，miniconda base）
- 主要依赖：`akshare`, `tushare`, `pandas`, `numpy`, `scipy`, `scikit-learn`, `mplfinance`, `matplotlib`, `sqlalchemy`, `python-docx`, `schedule`, `gitpython`

安装依赖：
```bash
pip install akshare tushare pandas numpy scipy scikit-learn mplfinance matplotlib sqlalchemy python-docx schedule gitpython
```

---

## 运行方式

### 启动每日数据更新（每天 17:00 自动触发）
```bash
cd /Users/zhangqi21/PyCharmMiscProject/stockAnalysis
/opt/miniconda3/bin/python -m trade_data.main_mac
```

### 立即执行一次数据更新
取消 `main_mac.py` 末尾 `update_trade_data2db(DB_PATH)` 的注释，直接运行即可。

---

## 参数名约定

| 参数名 | 含义 | 示例 |
|---|---|---|
| `code` | 6 位股票代码 | `000001` |
| `ts_code` | 带交易所标识的代码 | `000001.SZ` |
| `stock_name` | 股票名称 | `平安银行` |
| `trade_date` | 交易日期（字符串） | `20230101` |

---

## 修改记录

详见 [CHANGELOG.md](CHANGELOG.md)


