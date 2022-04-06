# -*- coding: utf-8 -*-

fr=open("自选股.sel",'r')
# fw=open("自选股2.csv",'w')
s_list=[]
for line in fr:
    print(line)
    i=0
    while i<len(line):
        print(line[i])
        if line[i].isdigit():
            s_list.append(line[i:i+6])
            i=i+7
            print(s_list)
        else:
            i=i+1
print(s_list)


