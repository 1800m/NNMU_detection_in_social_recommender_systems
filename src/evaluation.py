# -*- coding: utf-8 -*-
# 実験結果の評価を行う

import sqlite3
import codecs

"""
実験1
10回分の実験結果を読み込み，1つのファイルにまとめる
"""
def getResultSummarizationExp1(input_path,N):
    # N = 100
    # result = list()
    index = 0
    count = 0
    sum_list = list()
    for count in range(10):
        TP = 0
        tempResult = list()
        for line in codecs.open(input_path+"test"+str(count)+".csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：Index
            # [1]：Noisy order
            line_split = line.split(",")
            tempResult.insert(index, (line_split[0],line_split[1].rstrip("\n")))
            index = index + 1

        sum_list.insert(count,tempResult)

    output_path = input_path+"result_summarization.csv"
    for i in range(len(sum_list[0])):
        out_data = str(sum_list[0][i][1])+","+str(sum_list[1][i][1])+","+str(sum_list[2][i][1])+","+str(sum_list[3][i][1])+","+str(sum_list[4][i][1])+","+str(sum_list[5][i][1])+","+str(sum_list[6][i][1])+","+str(sum_list[7][i][1])+","+str(sum_list[8][i][1])+","+str(sum_list[9][i][1])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)



"""
実験1
実験結果を読み込み，Prec@100の10回平均を返す．
"""
def getResultExp1(input_path, N):
    # N = 100
    # result = list()
    TPlist = list()

    index = 0
    count = 0

    for count in range(10):
        TP = 0
        tempResult = list()
        for line in codecs.open(input_path+str(count)+".csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：Index
            # [1]：Noisy order
            line_split = line.split(",")
            tempResult.insert(index, (line_split[0],line_split[1].rstrip("\n")))

        tempResult = sorted(tempResult, reverse=True, key=lambda x: float(x[1]))    # 降順
        # print(tempResult)

        # 降順のTop100を調べる→tempResult[i][0]：元のIndexが400番以上か比較→閾値以上か比較→検出
        for i in range(N):
            if int(tempResult[i][0]) >= 400:
                if float(tempResult[i][1]) > 0.4:
                    TP = TP + 1
        TPlist.insert(count, TP)

    return TPlist




if __name__ == "__main__":
    # getResultSummarizationExp1("../data/exp1/result_EM_150/",150)
    # getResultSummarizationExp1("../data/exp1/result_EM_200/",200)
    # getResultSummarizationExp1("../data/exp1/result_EM_300/",300)
    # getResultSummarizationExp1("../data/exp1/result_ML_150/",150)
    # getResultSummarizationExp1("../data/exp1/result_ML_200/",200)
    # getResultSummarizationExp1("../data/exp1/result_ML_300/",300)

    input_path = "../data/exp1/result_EM_150/test"
    TPlist = getResultExp1(input_path,100)
    print("EM150")
    print(TPlist)
    aveTP = sum(TPlist)/len(TPlist)
    print("EM prec@100 = ",aveTP)

    input_path = "../data/exp1/result_ML_150/test"
    TPlist = getResultExp1(input_path,100)
    print("ML150")
    print(TPlist)
    aveTP = sum(TPlist)/len(TPlist)
    print("ML prec@100 = ",aveTP)

    for i in range(2):
        input_path = "../data/exp1/result_EM_"+str((i+2)*100)+"/test"
        TPlist = getResultExp1(input_path,100)
        print("EM"+str((i+2)*100))
        print(TPlist)
        aveTP = sum(TPlist)/len(TPlist)
        print("EM prec@100 = ",aveTP)

        input_path = "../data/exp1/result_ML_"+str((i+2)*100)+"/test"
        TPlist = getResultExp1(input_path,100)
        print("ML"+str((i+2)*100))
        print(TPlist)
        aveTP = sum(TPlist)/len(TPlist)
        print("ML prec@100 = ",aveTP)
