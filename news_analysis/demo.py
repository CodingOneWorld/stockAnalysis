# -*- coding: utf-8 -*-

import tushare as ts

# ts.get_latest_news(show_content=True) #默认获取最近80条新闻数据，只提供新闻类型、链接和标题
# ts.get_latest_news(top=5,show_content=True) #显示最新5条新闻，并打印出新闻内容

news = ts.get_notices()
print(news)

news = ts.guba_sina()
print(news)
print(news['title'][4]['content'])
