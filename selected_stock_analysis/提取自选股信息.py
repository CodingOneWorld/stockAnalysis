# -*- coding: utf-8 -*-
import os
import pandas as pd

from analysis_util.general_utils import get_stock_name


def extract_stock_from_file(file_path):
    fr = open(file_path, 'r')
    # fw=open("自选股2.csv",'w')
    s_set = set([])
    for line in fr:
        # print(line)
        i = 0
        while i < len(line):
            # print(line[i])
            if line[i].isdigit():
                s_set.add(line[i:i + 6])
                i = i + 7
                # print(s_list)
            else:
                i = i + 1
    print(s_set)
    print(len(s_set))

    return s_set


def create_df(s_s):
    zxg = []
    for s in s_s:
        s_name = get_stock_name(s)
        zxg.append([s, s_name])
        # print([s, s_name])
    df = pd.DataFrame(zxg, columns=['symbol', 'stock_name'])
    print(df)
    return df


# 提取全部的代码，并写入文件
def get_all_stocks():
    s_s = set([])
    for root, dirs, files in os.walk('./meta_selected_stocks/'):
        for file in files:
            # 获取文件所属目录
            print(root)
            # 获取文件路径
            file_path = os.path.join(root, file)
            print(file_path)
            s = extract_stock_from_file(file_path)
            s_s = s_s.union(s)

    print(s_s)
    df=create_df(s_s)
    df.to_csv('自选股.csv', index=0)


# 提取代码，并写入文件
def get_file_stocks(file_path):
    ss = extract_stock_from_file(file_path)
    print(ss)
    df = create_df(ss)
    print(df)
    file_name = file_path.split('/')[-1].split('.')[0]
    df.to_csv(file_name + '.csv', index=0)



if __name__ == '__main__':
    s=set([])

    file_path='./meta_selected_stocks/绩优股.sel'
    ss1 = extract_stock_from_file(file_path)
    s=s.union(ss1)

    file_path = './meta_selected_stocks/绩优股2.sel'
    ss2 = extract_stock_from_file(file_path)
    s=s.union(ss2)

    file_path = './meta_selected_stocks/板块29.sel'
    ss3 = extract_stock_from_file(file_path)
    s=s.union(ss3)

    df=create_df(s)
    df.to_csv('绩优股.csv', index=0)




