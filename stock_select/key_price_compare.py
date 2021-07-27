# -*- coding: utf-8 -*-

# 判断股票的关键价位
# 如支撑位，压力位，均线位置等
# 计算当前价格最高值，最低值，以及均线数据，进行比较
from analysis_util.cal_mean_line import cal_mean_line
from analysis_util.cal_stock_trend import get_stock_price, cal_stock_price_trend

def mean_price_compare(stock_code):
    # 计算股票趋势
    k = 1 if cal_stock_price_trend(stock_code, 3)>0 else -1
    print(k)

    # 获取股票最近的价格
    stock_price = 0
    if k > 0:
        stock_price = get_stock_price(stock_code, 'high')[-1]
        print(stock_price)

    elif k < 0:
        stock_price = get_stock_price(stock_code, 'low')[-1]
        print(stock_price)

    # 计算均线值
    mean_dict = cal_mean_line(stock_code, 3000)
    print(mean_dict)

    # 股价与均线值比较
    stock_mean_list=[]
    for mean in mean_dict.keys():
        if stock_price>=mean_dict.get(mean)*0.95 and stock_price<=mean_dict.get(mean)*1.05:
            stock_mean_list.append(mean)

    return stock_code+'/'+str(k)+'/'+','.join(stock_mean_list)

if __name__ == '__main__':
    stock_mean=mean_price_compare('000002')
    print(stock_mean)













