# -*- coding: utf-8 -*-

fr=open("自选股.csv",'r')
fw=open("自选股2.csv",'w')
for line in fr:
    line=line.replace(" 融 ",",")
    line=line.replace(" ",",")
    print(line)
    fw.write(line)
fw.flush()
fw.close()

