# 备忘录

交易数据获取限制
1、股票列表数据 每小时只能调用一次，限制非常严格
2、日线数据 有每分钟的调用次数限制  每日限制10000次

交易数据保存
将数据运行一次保存在本地，这样可以无限制调用
    股票列表数据，保存在文件中 stock_list.csv  // DB中 stock_list表
    日线数据 保存在DB中 S******_daily
更新策略
    每天更新 15点收盘，可以在16点左右更新，方便晚上使用
    在读取股票列表时，写入文件及DB，然后根据股票列表获取每个股票的日线数据，写入数据库

交易数据读取
    股票列表读取 只能在文件或DB中读取
    日线数据
        online 每日限制
        DB

    
    
    
