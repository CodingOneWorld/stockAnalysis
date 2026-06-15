# 修改记录

## 2026-06-10

### stock_select 模块：重构为两层串联选股架构（宽进严出）

**背景**：原来预筛选（`stock_pre_select.py`）和精筛选（`main.py`）是并行的两条独立流程，互不依赖，职责重叠且效率低（预筛选逐只查财务数据）。重构为明确的上下游两层架构。

**新架构**

```
第一层：预筛选（stock_pre_select.py → build_stock_pool()）
  只做资格审查，不查财务，速度快
  条件：主板（0/6开头）+ 排除ST/退市 + 排除近3年新股
  输出：stock_pool.txt（候选池，约1500只）

第二层：精筛选（main.py → run_full_pipeline()）
  读入 stock_pool.txt 候选池
  select_by_income(symbol_list)：近5年收入增速≥10%
  select_by_profit(symbol_list)：近5年净利润增速≥10%
  取交集 → 输出：基本面好的股票.txt
```

**修改文件**

- `stock_select/stock_pre_select.py`：逻辑改写为 `build_stock_pool()` 函数，去掉逐只财务查询，只做资格过滤；可被 `main.py` 调用，也可独立运行

- `stock_select/select_by_income.py`：新增 `symbol_list` 参数（可选），传入时只在候选池范围内扫财务库，不传则扫全库（兼容独立运行场景）

- `stock_select/select_by_profit.py`：同上

- `stock_select/main.py`：完全重写为 `run_full_pipeline()` 函数，串联两层流程；新增 `rebuild_pool` 参数（False 时复用已有候选池，节省时间）

**运行方式**

```bash
cd /Users/zhangqi21/PyCharmMiscProject/stockAnalysis
python -m stock_select.main   # 全流程：先预筛选再精筛选
python -m stock_select.stock_pre_select  # 只生成候选池
python -m stock_select.select_by_income  # 独立精筛选（扫全库）
```

---

### stock_select/stock_pre_select.py：修复预筛选逻辑三处问题

**问题1：`list_date` 上市日期过滤年份硬编码**
- 原代码 `stock_list_data[stock_list_data['list_date'] <= '20200101']` 写死了 2020 年，随着时间推移不再符合"排除近3年新股"的原意
- 修复：动态计算 `datetime.date.today() - timedelta(days=3*365)`，每次运行自动取准确截止日期

**问题2：ST 股过滤靠字符串匹配不健壮**
- 原代码逐行 `i[1].__contains__('ST')` 只匹配了 `ST` 字样，`*ST`/`退市` 等格式覆盖不全
- 修复：改为 pandas 向量化 `name.str.contains('ST|退', na=False)`，覆盖所有变体，同时用 Tushare `stock_basic` 补充 `list_date`（AKShare 无此字段）

**问题3：`list_date` 字段实际全为空**
- AKShare 不提供上市日期，数据库中 `list_date` 全为空字符串，对空字符串做 `<=` 比较会意外通过
- 修复：通过 Tushare `stock_basic` 补充真实 `list_date`；同时对 `list_date` 为空/NaN 的股票保守处理（保留，不误删）

**其他改进**
- 新增 `_get_stock_list_with_listdate()` 函数，封装"数据库列表 + Tushare 日期补充"的拼接逻辑
- 过滤步骤全部向量化，按步骤打印过滤后数量，便于追踪

---

### stock_select 模块：修复多个历史遗留问题

**修改文件**

- `stock_select/select_by_income.py`（完全重写）
  - 年份硬编码（2017~2021）→ 从数据库列名动态解析，自动使用最新 n 年数据
  - 新增参数 `n_years`（默认5年）、`min_growth_pct`（默认10%增速门槛）
  - 移除顶层直接执行代码 `stocks = select_by_income()`，移入 `if __name__ == '__main__':`，避免 import 时触发数据库查询
  - 统一使用 `pandas` 向量化 mask 筛选，替代多层 `.loc[]` 链式调用

- `stock_select/select_by_profit.py`（完全重写）
  - 同上：年份动态化、参数化、移除顶层执行代码、向量化筛选
  - 参数：`n_years`（默认5年）、`min_growth_pct`（默认10%）

- `stock_select/select_by_trend.py`
  - `dtype={'symbol': np.str}` → `dtype={'symbol': str}`（`np.str` 在 Python 3.10+ 已废弃）

- `stock_select/select_by_price.py`
  - 同上：`dtype={'symbol': np.str}` → `dtype={'symbol': str}`

- `stock_select/stock_pre_select.py`
  - 修复在 `for s in stock_array` 迭代过程中直接调用 `stock_array.remove(s)` 的 bug（会跳过元素）
  - 改为先收集满足条件的股票到 `qualified` 列表，循环结束后统一赋值

---

## 2026-06-09

### trade_data/data_source.py — 彻底消除 akshare 内部 tqdm 进度条输出

**问题**：运行 `get_daily_data_tspro2DB` 时，控制台出现大量 akshare 内部的 tqdm 进度条（如 `63%|██████▎   | 22/35 [00:11<00:08,  1.48it/s]`），原有的 `TQDM_DISABLE` 环境变量在部分入口场景下不生效。

**修复**：在 `data_source.py` 顶部（`import akshare` 之前）采用双重禁用策略：

1. `os.environ['TQDM_DISABLE'] = '1'`：强制写入环境变量（不用 `setdefault`，确保覆盖）
2. monkey-patch `tqdm.tqdm.__init__`：将所有 tqdm 实例的 `disable` 参数强制设为 `True`，保留迭代功能但不输出进度条（避免替换整个类导致 akshare 内部迭代器失效）

```python
os.environ['TQDM_DISABLE'] = '1'

import tqdm as _tqdm_module
_real_tqdm_init = _tqdm_module.tqdm.__init__
def _silent_tqdm_init(self, *args, **kwargs):
    kwargs['disable'] = True
    _real_tqdm_init(self, *args, **kwargs)
_tqdm_module.tqdm.__init__ = _silent_tqdm_init
```

**验证**：单只/并发拉取股票、ETF 列表均无任何进度条输出，数据正确返回。

---

## 2026-06-08

### 修复 etf_main.py 无法直接运行 + PyMiniRacer 崩溃问题

#### 1. `trade_data/etf_main.py` — 修复直接运行时 ModuleNotFoundError

**问题**：直接运行 `python trade_data/etf_main.py` 时，Python `sys.path` 中不包含项目根目录，导致 `from util.utils_common import ...` 报 `ModuleNotFoundError: No module named 'util'`。

**修复**：在文件顶部加入项目根目录自动注入逻辑，通过 `pathlib.Path(__file__).parent.parent` 动态定位根目录并插入 `sys.path`，无论从哪个目录运行均可正常启动。

```python
_PROJECT_ROOT = pathlib.Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
```

#### 2. `trade_data/data_source.py` — 修复 PyMiniRacer 崩溃（退出码 133）

**问题**：`get_etf_list_ak()` 使用东方财富接口 `fund_etf_spot_em`，该接口内部依赖 `PyMiniRacer`（V8 JS 引擎）解析数据。`PyMiniRacer` 在 macOS Apple Silicon 上存在内存池初始化冲突的已知 bug，触发 `FATAL: address_pool_manager.cc Check failed: !pool->IsInitialized()`，进程被 signal 5 SIGTRAP 杀死，退出码 133。

**修复**：将 `get_etf_list_ak()` 改为使用新浪接口 `fund_etf_category_sina`，该接口纯 HTTP 请求，无需 JS 引擎，在 macOS 上稳定运行。新浪接口 ETF 覆盖数量（1547 只）多于东方财富（1494 只）。

| 项目 | 原方案（东方财富） | 新方案（新浪） |
|---|---|---|
| AKShare 接口 | `fund_etf_spot_em` | `fund_etf_category_sina(symbol='ETF基金')` |
| 代码字段 | `代码`（纯数字） | `代码`（`sh`/`sz` + 6位数字，需截取后6位） |
| 依赖 JS 引擎 | 是（PyMiniRacer） | 否 |
| macOS Apple Silicon | 崩溃 | 正常 |
| ETF 数量 | ~1494 | ~1547 |

---

## 2026-06-06

### trade_data 模块：新增 ETF 行情数据获取与持久化

**背景**：原有数据流程只覆盖 A 股股票，不支持 ETF。新增独立的 ETF 数据流程，获取全市场 ETF 列表及历史前复权日线数据并写入 SQLite，与股票数据共用同一数据库，字段规范完全一致，后续分析模块可无缝复用。

**数据源**：AKShare 东方财富（`fund_etf_spot_em` + `fund_etf_hist_em`），免费、无频次限制。

**新增文件**

- `trade_data/get_etf_data.py`（ETF 核心数据流）

  | 函数 | 说明 |
  |---|---|
  | `get_etf_list_2DB(source)` | 获取 ETF 列表并写入数据库表 `etf_list`，支持 `online`/`DB` 两种 source |
  | `_fetch_etf_and_save(code, name, filepath)` | 线程任务：拉取单只 ETF 日线并写入 `E{code}_daily` 表 |
  | `update_etf_data_2DB(filepath, source, max_workers, max_per_min)` | **主入口**：并发全量更新所有 ETF 日线数据 |
  | `get_etf_trade_data(code, start_date, end_date, mode)` | 对外查询：从数据库或网络读取单只 ETF 日线；online 模式自动从 `etf_list` 表补充 name |
  | `get_etf_trade_data_latestdays(code, latestdays)` | 获取最近 N 天 ETF 日线数据 |

- `trade_data/etf_main.py`（ETF 独立运行入口）
  - `run_etf_update(source)` 封装完整更新流程，打印开始/结束时间与耗时
  - 直接运行即可触发全量更新：`python -m trade_data.etf_main`

**修改文件**

- `trade_data/data_source.py`：新增 3 个 ETF 相关函数

  | 函数 | 说明 |
  |---|---|
  | `get_etf_list_ak()` | `fund_etf_spot_em` 获取全市场 ETF 列表，输出 `code, name, ts_code` |
  | `_parse_etf_df(df, code, name)` | 内部工具：将 `fund_etf_hist_em` 返回字段标准化为项目统一格式 |
  | `get_etf_daily_ak(code, name, start_date, end_date, retry)` | 获取单只 ETF 前复权日线，新增自动重试（最多 3 次，指数退避：1s/2s/4s），捕获网络断连异常 |

**数据库表约定**

| 表名 | 内容 |
|---|---|
| `etf_list` | ETF 基础信息：`code, name, ts_code` |
| `E{code}_daily` | ETF 日线数据（`E` 前缀区分股票表的 `S` 前缀）：`ts_code, trade_date, open, high, low, close, vol, amount, name` |

**限速参数**（东方财富接口较腾讯更易断连，保守设置）

| 参数 | 值 |
|---|---|
| 并发线程数 `max_workers` | 4 |
| 限速 `max_per_min` | 30 次/分钟 |
| 单次失败重试 | 最多 3 次，指数退避 |

**运行方式**

```bash
cd /Users/zhangqi21/PyCharmMiscProject/stockAnalysis
/opt/miniconda3/bin/python -m trade_data.etf_main
```

---

## 2026-05-30

### selected_stock_analysis：加入成交量维度 + 回测模块完整实现

#### 1. `up_classification.py` — 新增成交量工具函数

新增三个纯工具函数，供各策略模块共享：

| 函数 | 说明 |
|---|---|
| `cal_volume_ratio(df, recent_days=5, base_days=20)` | 近 recent_days 日均量 / 前 (base_days−recent_days) 日均量；>1.5 放量，<0.7 缩量 |
| `cal_single_day_vol_ratio(df, base_days=5)` | 当日（最后一根K线）成交量 / 过去 base_days 日均量 |
| `cal_volume_trend(df, days=10)` | 近 days 天成交量的归一化趋势斜率（>0 量在放大） |

修复了 `base_days` 参数边界 bug（原版 `vol[-base_days:-recent_days]` 在数据正好等于 base_days 时返回空）。

#### 2. `rebound_classification.py` — 反弹买点加入放量确认

新增成交量三重过滤，在价格条件（k5>0、k10>0、k20<-0.002、k100<0、在5日均线上方）全部满足后：

```
vol_ratio = cal_volume_ratio(df, 5, 20)    # 近5日 vs 前15日均量
vol_trend = cal_volume_trend(df, 10)        # 近10日量趋势方向
today_vr  = cal_single_day_vol_ratio(df, 5) # 当日量比

vol_ok = (vol_ratio > 1.2 OR vol_trend > 0) AND today_vr > 0.8
```

逻辑：反弹必须有资金真实介入（放量或量趋势上升），且当日成交不能极度萎缩。

#### 3. `buy_point_detect.py` — 买点描述加入量能信息

- **上升通道回调**：计算 `vol_ratio` / `today_vr`，在信号描述中标注 `[缩量回调]` 或 `[放量回调⚠]`（提示风险），不硬过滤，保留策略人工判断空间
- **下降通道前低/关键均线**：计算量趋势和当日量比，在信号描述中标注 `量趋势回升✓` / `今日放量✓` / `量能未见底⚠`，辅助判断是否真正触底

#### 4. `buy_point_effect_tracking.py` — 完整实现历史信号回测统计

从空文件扩展为完整的回测分析模块：

**核心函数**

| 函数 | 功能 |
|---|---|
| `backtest_signal(code, signal_date, hold_days_list)` | 对单条信号，查询数据库计算各持有期收益率 |
| `backtest_signal_file(signal_file, hold_days_list, output_file)` | 批量回测信号 CSV，输出逐条回测结果 |
| `summarize_backtest(result_df, hold_days_list)` | 汇总统计：胜率、平均收益率、中位收益率、最大涨幅/跌幅 |
| `plot_return_distribution(result_df, hold_days, title)` | 绘制收益率分布直方图（保存为 PNG） |

**命令行使用示例**

```bash
# 回测"上升通道回调"信号，持有1/3/5/10日，并绘图
/opt/miniconda3/bin/python -m selected_stock_analysis.buy_point_effect_tracking \
    --signal-file 上升通道回调.csv \
    --hold-days 1 3 5 10 \
    --plot

# 同时回测多个信号文件
/opt/miniconda3/bin/python -m selected_stock_analysis.buy_point_effect_tracking \
    --signal-file 上升通道回调.csv 下降通道到前低.csv 下降通道到关键均线.csv
```

**输出文件**

| 文件 | 内容 |
|---|---|
| `上升通道回调_回测明细.csv` | 每条信号的各持有期收益率 |
| `上升通道回调_回测统计.csv` | 胜率/均值/中位数/最大涨幅跌幅汇总表 |
| `回测收益分布_N日.png` | 收益率分布直方图 |

---

## 2026-05-29（四）

### fundamental_data 模块重写：Tushare v1 → AKShare

**背景**：`get_income.py` / `get_profit.py` 依赖旧版 Tushare v1 免费接口（`ts.get_profit_data()`），该接口已停止服务，返回"获取失败，请检查网络"。改用 AKShare 新浪财务利润表接口（`stock_financial_report_sina`）重写，实现全量并发拉取。

**修改文件**

- `fundamental_data/get_income.py`（完全重写）
  - 移除旧版 `tushare` 依赖
  - 新增 `_fetch_income_one(symbol, name)`：拉取单只股票所有年报营业收入，只保留年报（报告日 1231 结尾）
  - `income_of_all_stocks2db(max_workers=10)`：并发全量写库，每 50 只打印一次进度
  - `get_income_of_latest_years(code, n)`：接口签名与原版兼容，改用 `symbol` 字段查询
  - 宽表格式：`symbol, name, income_YYYY, income_YYYY+1, ...`，按年份列升序排列

- `fundamental_data/get_profit.py`（完全重写）
  - 移除旧版 `tushare` 依赖
  - 新增 `_fetch_profit_one(symbol, name)`：拉取单只股票所有年报归属于母公司净利润（优先"归属于母公司的净利润"，其次"净利润"）
  - `profit_of_all_stocks2db(max_workers=10)`：并发全量写库
  - `get_profit_of_latest_years(code, n)`：接口签名与原版兼容
  - 宽表格式：`symbol, name, profits_YYYY, profits_YYYY+1, ...`

- `fundamental_data/get_ST_stocks.py`（修复表名）
  - `stock_basic_list` → `stock_list`（与 trade_data 迁移后的实际表名对齐）

**数据源**

| 接口 | 返回内容 | 特点 |
|---|---|---|
| `ak.stock_financial_report_sina(stock, '利润表')` | 营业收入、净利润（逐期） | 免费，历史数据完整，支持年报/季报过滤 |

**功能验证（5只抽样测试）**

| 股票 | 营业收入（2024年） | 净利润（2024年） |
|---|---|---|
| 平安银行 | 1467.0亿 | 445.1亿 |
| 贵州茅台 | 1709.0亿 | 893.3亿 |
| 比亚迪 | 7771.0亿 | 415.9亿 |
| 招商银行 | 3374.9亿 | 1483.9亿 |

**get_ST_stocks 验证**：正确识别 253 只 ST 股票，表名修复生效。

---

## 2026-05-29（三）

### 并发参数优化 + 日志降噪

**背景**：实测腾讯数据源在 10~12 线程并发时速率达到服务器限速天花板约 37~39只/分，超过目标 35只/分。将之前设置的保守默认值（30线程、48次/分）调整为与实测匹配的合理值，同时消除并发时的 tqdm 进度条噪音。

**修改文件**

- `trade_data/get_trade_data.py`
  - `RateLimiter` 全局默认限速从 `48次/分` 调整为 **`45次/分`**（贴近服务器实际上限，避免过度等待）
  - `get_daily_data_tspro2DB()` 参数默认值：`max_workers` 从 30 改为 **12**，`max_per_min` 从 48 改为 **45**
  - 更新参数注释：说明 12 线程是实测达到速率天花板的最优线程数
  - 在模块顶部加入 `os.environ.setdefault('TQDM_DISABLE', '1')`，并发模式下禁用 akshare 内部的 tqdm 进度条，避免日志被多线程进度条污染

- `trade_data/data_source.py`
  - `get_daily_qfq()` 新增 `verbose: bool = False` 参数
  - 默认（`verbose=False`）：仅在 AKShare 失败/降级到 Tushare 时打印警告，不打印每只成功日志
  - 传入 `verbose=True`：打印每只成功日志（适合单只调试场景）
  - 效果：并发 50 只时终端输出干净，只显示 `get_trade_data.py` 的进度行

- `trade_data/main_mac.py`
  - 修复历史遗留值：`get_daily_data_tspro2DB(DB_PATH, 134, 0)` → `get_daily_data_tspro2DB(DB_PATH, 0, 0)`（`cou_new=134` 是当时断点续传的临时值，应从第 0 只开始全量更新）

**性能测试结果**（50 只股票，12 线程，限速 45次/分）

| 阶段 | 速率 |
|---|---|
| 启动预热（前 10 只） | 6~25 只/分 |
| 稳定阶段（30 只后） | **37~39 只/分** |
| 50 只整体平均 | **38.9 只/分** |
| 成功率 | **100%（50/50）** |

全量更新 3500 只预计耗时约 **90 分钟**。

---

## 2026-05-29（二）

### get_trade_data.py：全量更新改为并发请求

**背景**：AKShare 单线程全量更新约 3500 只股票需要 5 小时，改为多线程并发后大幅提速。

**修改文件**

- `trade_data/get_trade_data.py`
  - 新增 `RateLimiter` 令牌桶限速器类，控制请求频率，线程安全
  - 新增 `_fetch_and_save()` 线程任务函数，每个线程独立建 SQLite 连接（避免多线程写冲突）
  - `get_daily_data_tspro2DB()` 改为 `ThreadPoolExecutor` 并发执行，默认 8 线程
  - 新增参数 `max_workers`（默认 8）、`max_per_min`（默认 48，每分钟请求次数上限）
  - 实时打印进度：完成数/总数、每分钟速率、预计剩余时间

**性能对比**（测试 10 只股票）

| 模式 | 平均耗时/只 | 速率 |
|---|---|---|
| 单线程（原） | ~6-9 秒 | ~10 只/分钟 |
| 8线程并发（新）| ~2.3 秒 | ~26 只/分钟 |

全量更新 3500 只预计从 5 小时缩短至约 **2.3 小时**（限速 48次/分钟保护下）。

---

## 2026-05-29

### 数据源迁移：Tushare → AKShare + Tushare 双数据源

**背景**：Tushare Pro 免费积分有频次限制（部分接口每小时仅能请求1次），影响数据更新效率。迁移至以 AKShare（腾讯数据源）为主力、Tushare 为备用的双数据源架构，获取数据均为前复权日线数据。

**新增文件**

- `trade_data/data_source.py`
  - 封装双数据源，对外提供统一接口
  - `get_stock_list()`：获取 A 股股票列表，AKShare 优先，失败自动切 Tushare，重试3次
  - `get_daily_qfq()`：获取前复权日线数据，AKShare 腾讯源优先，失败自动切 Tushare，重试3次
  - 统一输出字段：`ts_code, trade_date, open, high, low, close, vol, amount, name`
  - `trade_date` 格式：`YYYYMMDD`，数据按升序排列

**修改文件**

- `trade_data/get_stock_basic_list.py`
  - 移除 tushare 直接依赖
  - `get_stock_basic_list_2DB()` 改为调用 `data_source.get_stock_list()`
  - 修复 pandas 链式索引 `UserWarning`，改用 mask 方式过滤创业板/科创板/北交所

- `trade_data/get_trade_data.py`
  - 移除 tushare 直接依赖
  - `get_stock_trade_data()` online 模式改为调用 `data_source.get_daily_qfq()`
  - `get_daily_data_tspro2DB()` 改为调用 `data_source.get_daily_qfq()` 逐只写库
  - 修复 `last_datetime.txt` 相对路径问题，改用 `pathlib.Path(__file__).parent` 定位

- `trade_data/main_mac.py`
  - 注释掉 schedule 定时逻辑，改为直接调用 `update_trade_data2db()` 便于手动触发

- `util/utils_common.py`
  - `get_dbpath_by_repo()` 新增对 `zhangqi21` 用户的路径支持
  - 返回路径：`/Users/zhangqi21/DB/stock_data.db`

**环境依赖**

- 解释器：`/opt/miniconda3/bin/python`（Python 3.13，miniconda base 环境）
- 新增安装：`akshare`, `tushare`, `pandas`, `sqlalchemy`, `mplfinance`, `scipy`, `scikit-learn`, `python-docx`, `matplotlib`, `numpy`, `schedule`, `gitpython`
- 数据库路径：`/Users/zhangqi21/DB/stock_data.db`

**运行方式**

```bash
cd /Users/zhangqi21/PyCharmMiscProject/stockAnalysis
/opt/miniconda3/bin/python -m trade_data.main_mac
```
