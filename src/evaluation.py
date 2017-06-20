# -*- coding: utf-8 -*-
# 実験結果の評価を行う

import sqlite3
import codecs
import sys
import linecache

"""
実験1
10回分の実験結果を読み込み，1つのファイルにまとめる
"""
def getResultSummarizationExp1(input_path,N):
    # N = 100
    # result = list()
    index = 0
    count = 0

    # 各テストセットの値格納用
    sum0_NF = list()
    sum1_NF = list()
    sum2_NF = list()
    sum3_NF = list()
    sum4_NF = list()
    sum5_NF = list()
    sum6_NF = list()
    sum7_NF = list()
    sum8_NF = list()
    sum9_NF = list()

    sum0_NNMU = list()
    sum1_NNMU = list()
    sum2_NNMU = list()
    sum3_NNMU = list()
    sum4_NNMU = list()
    sum5_NNMU = list()
    sum6_NNMU = list()
    sum7_NNMU = list()
    sum8_NNMU = list()
    sum9_NNMU = list()

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

        if i < 400:
            sum0_NF.insert(i,float(sum_list[0][i][1]))
            sum1_NF.insert(i,float(sum_list[1][i][1]))
            sum2_NF.insert(i,float(sum_list[2][i][1]))
            sum3_NF.insert(i,float(sum_list[3][i][1]))
            sum4_NF.insert(i,float(sum_list[4][i][1]))
            sum5_NF.insert(i,float(sum_list[5][i][1]))
            sum6_NF.insert(i,float(sum_list[6][i][1]))
            sum7_NF.insert(i,float(sum_list[7][i][1]))
            sum8_NF.insert(i,float(sum_list[8][i][1]))
            sum9_NF.insert(i,float(sum_list[9][i][1]))
        else:
            sum0_NNMU.insert(i,float(sum_list[0][i][1]))
            sum1_NNMU.insert(i,float(sum_list[1][i][1]))
            sum2_NNMU.insert(i,float(sum_list[2][i][1]))
            sum3_NNMU.insert(i,float(sum_list[3][i][1]))
            sum4_NNMU.insert(i,float(sum_list[4][i][1]))
            sum5_NNMU.insert(i,float(sum_list[5][i][1]))
            sum6_NNMU.insert(i,float(sum_list[6][i][1]))
            sum7_NNMU.insert(i,float(sum_list[7][i][1]))
            sum8_NNMU.insert(i,float(sum_list[8][i][1]))
            sum9_NNMU.insert(i,float(sum_list[9][i][1]))

        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    out_data = ",,,,,,,,,"
    f = open(output_path, "a")
    print(out_data, end="\n", file=f)
    out_data = str(sum(sum0_NF)/len(sum0_NF))+","+str(sum(sum1_NF)/len(sum1_NF))+","+str(sum(sum2_NF)/len(sum2_NF))+","+str(sum(sum3_NF)/len(sum3_NF))+","+str(sum(sum4_NF)/len(sum4_NF))+","+str(sum(sum5_NF)/len(sum5_NF))+","+str(sum(sum6_NF)/len(sum6_NF))+","+str(sum(sum7_NF)/len(sum7_NF))+","+str(sum(sum8_NF)/len(sum8_NF))+","+str(sum(sum9_NF)/len(sum9_NF))
    f = open(output_path, "a")
    print(out_data, end="\n", file=f)
    out_data = str(sum(sum0_NNMU)/len(sum0_NNMU))+","+str(sum(sum1_NNMU)/len(sum1_NNMU))+","+str(sum(sum2_NNMU)/len(sum2_NNMU))+","+str(sum(sum3_NNMU)/len(sum3_NNMU))+","+str(sum(sum4_NNMU)/len(sum4_NNMU))+","+str(sum(sum5_NNMU)/len(sum5_NNMU))+","+str(sum(sum6_NNMU)/len(sum6_NNMU))+","+str(sum(sum7_NNMU)/len(sum7_NNMU))+","+str(sum(sum8_NNMU)/len(sum8_NNMU))+","+str(sum(sum9_NNMU)/len(sum9_NNMU))
    f = open(output_path, "a")
    print(out_data, end="\n", file=f)

    out_data = ",,,,,,,,,"
    f = open(output_path, "a")
    print(out_data, end="\n", file=f)

    sum_all = sum(sum0_NF)+sum(sum1_NF)+sum(sum2_NF)+sum(sum3_NF)+sum(sum4_NF)+sum(sum5_NF)+sum(sum6_NF)+sum(sum7_NF)+sum(sum8_NF)+sum(sum9_NF)
    sum_len_all = len(sum0_NF)*10
    out_data = "Noise-Free average,"+str(sum_all/sum_len_all)+",,,,,,,,"
    f = open(output_path, "a")
    print(out_data, end="\n", file=f)

    sum_all = sum(sum0_NNMU)+sum(sum1_NNMU)+sum(sum2_NNMU)+sum(sum3_NNMU)+sum(sum4_NNMU)+sum(sum5_NNMU)+sum(sum6_NNMU)+sum(sum7_NNMU)+sum(sum8_NNMU)+sum(sum9_NNMU)
    sum_len_all = len(sum0_NNMU)*10
    out_data = "NNMU average,"+str(sum_all/sum_len_all)+",,,,,,,,"
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
        loop_counter = 0    # 500行カウントアップ用
        for line in codecs.open(input_path+str(count)+".csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：Index
            # [1]：Noisy order
            line_split = line.split(",")
            tempResult.insert(index, (line_split[0],line_split[1].rstrip("\n")))
            loop_counter = loop_counter + 1
            if loop_counter == 500:
                break

        tempResult = sorted(tempResult, reverse=True, key=lambda x: float(x[1]))    # 降順
        # for i in range(len(tempResult)):
        #     print(tempResult[i])

        # 降順のTop100を調べる→tempResult[i][0]：元のIndexが400番以上か比較→閾値以上か比較→検出
        for i in range(N):
            if int(tempResult[i][0]) >= 400:
                # TP = TP + 1
                if float(tempResult[i][1]) > 0.3:
                    TP = TP + 1
        TPlist.insert(count, (TP/N)*100)

    return TPlist

"""
各result_summarization.csvを読み込み，平均値を返す
"""
def readResultSummarization(input_path):
    target_line = linecache.getline(input_path, 505).split(",")  # NF average
    NFave = target_line[1]

    target_line = linecache.getline(input_path, 506).split(",")  # NNMU average
    NNMUave = target_line[1]
    linecache.clearcache()

    # 確認用
    # print(NFave)
    # print(NNMUave)

    return (NFave,NNMUave)


"""
結果を1つの表にまとめる
"""
def generateResultTable(EM_NF, EM_NNMU, ML_NF, ML_NNMU, EM_prec, ML_prec):
    output_path = "../data/exp1/result_evaluation.csv"
    # print(EM_NF)
    # print(EM_NNMU)
    # print(ML_NF)
    # print(ML_NNMU)
    # print(EM_prec)
    # print(ML_prec)

    # out_data = ",,,,,"
    for i in range(11):
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            out_data = "noise average,,,intersection,,"
            print(out_data, end="\n", file=f)
        elif i == 1:       # 2行目の追記
            f = open(output_path, "a")
            out_data = ",,150,200,300,average"
            print(out_data, end="\n", file=f)
        elif i == 2:       # 3行目の追記
            f = open(output_path, "a")
            out_data = "EachMovie,Noise-Free,"+str(EM_NF[0])+","+str(EM_NF[1])+","+str(EM_NF[2])+","+str((float(EM_NF[0])+float(EM_NF[1])+float(EM_NF[2]))/len(EM_NF))
            print(out_data, end="\n", file=f)
        elif i == 3:       # 4行目の追記
            f = open(output_path, "a")
            out_data = ",NNMU,"+str(EM_NNMU[0])+","+str(EM_NNMU[1])+","+str(EM_NNMU[2])+","+str((float(EM_NNMU[0])+float(EM_NNMU[1])+float(EM_NNMU[2]))/len(EM_NNMU))
            print(out_data, end="\n", file=f)
        elif i == 4:       # 5行目の追記
            f = open(output_path, "a")
            out_data = "MovieLens,Noise-Free,"+str(ML_NF[0])+","+str(ML_NF[1])+","+str(ML_NF[2])+","+str((float(ML_NF[0])+float(ML_NF[1])+float(ML_NF[2]))/len(ML_NF))
            print(out_data, end="\n", file=f)
        elif i == 5:       # 6行目の追記
            f = open(output_path, "a")
            out_data = ",NNMU,"+str(ML_NNMU[0])+","+str(ML_NNMU[1])+","+str(ML_NNMU[2])+","+str((float(ML_NNMU[0])+float(ML_NNMU[1])+float(ML_NNMU[2]))/len(ML_NNMU))
            print(out_data, end="\n", file=f)
        elif i == 6:
            f = open(output_path, "a")
            out_data = ",,,,,"
            print(out_data, end="\n", file=f)
        elif i == 7:
            f = open(output_path, "a")
            out_data = "threshold,0.3,,,,"
            print(out_data, end="\n", file=f)
        elif i == 8:
            f = open(output_path, "a")
            out_data = "Prec@n,100% Noisy Rating,,intersection,,"
            print(out_data, end="\n", file=f)
        elif i == 9:
            f = open(output_path, "a")
            out_data = ",,150,200,300,"
            print(out_data, end="\n", file=f)
        else:
            f = open(output_path, "a")
            index = 0
            for j in range(4):
                if j == 0:
                    out_data = "EachMovie,Prec@10,"+str(EM_prec[index])+","+str(EM_prec[index+1])+","+str(EM_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                elif j == 1:
                    out_data = ",Prec@20,"+str(EM_prec[index])+","+str(EM_prec[index+1])+","+str(EM_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                elif j == 2:
                    out_data = ",Prec@50,"+str(EM_prec[index])+","+str(EM_prec[index+1])+","+str(EM_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                else:
                    out_data = ",Prec@100,"+str(EM_prec[index])+","+str(EM_prec[index+1])+","+str(EM_prec[index+2])+","
                    print(out_data, end="\n", file=f)

            index = 0
            for j in range(4):
                if j == 0:
                    out_data = "EachMovie,Prec@10,"+str(ML_prec[index])+","+str(ML_prec[index+1])+","+str(ML_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                elif j == 1:
                    out_data = ",Prec@20,"+str(ML_prec[index])+","+str(ML_prec[index+1])+","+str(ML_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                elif j == 2:
                    out_data = ",Prec@50,"+str(ML_prec[index])+","+str(ML_prec[index+1])+","+str(ML_prec[index+2])+","
                    print(out_data, end="\n", file=f)
                    index = index + 1
                else:
                    out_data = ",Prec@100,"+str(ML_prec[index])+","+str(ML_prec[index+1])+","+str(ML_prec[index+2])+","
                    print(out_data, end="\n", file=f)



if __name__ == "__main__":
    EM_NF = list()
    EM_NNMU = list()
    ML_NF = list()
    ML_NNMU = list()
    EM_prec = list()
    ML_prec = list()

    number = (150,200,300)
    n = (10,20,50,100)


    for i in range(len(number)):    # 150, 200, 300
        getResultSummarizationExp1("../data/exp1/result_EM_"+str(number[i])+"/",number[i])
        tempNF,tempNNMU = readResultSummarization("../data/exp1/result_EM_"+str(number[i])+"/result_summarization.csv")
        EM_NF.insert(i,tempNF)
        EM_NNMU.insert(i,tempNNMU)

        getResultSummarizationExp1("../data/exp1/result_ML_"+str(number[i])+"/",number[i])
        tempNF,tempNNMU = readResultSummarization("../data/exp1/result_ML_"+str(number[i])+"/result_summarization.csv")
        ML_NF.insert(i,tempNF)
        ML_NNMU.insert(i,tempNNMU)


    # prec@nの取得
    index = 0
    for i in range(len(n)):
        N = n[i]    # 10, 20, 50, 100
        for j in range(len(number)):    # 150, 200, 300
            # print("n = "+str(n[i]))
            input_path = "../data/exp1/result_EM_"+str(number[j])+"/test"
            TPlist = getResultExp1(input_path,N)
            # print("EM"+str(number[j]))
            # print(TPlist)
            aveTP = sum(TPlist)/len(TPlist)
            # print("EM prec@"+str(N)+" = ",aveTP)
            EM_prec.insert(index, aveTP)

            input_path = "../data/exp1/result_ML_"+str(number[j])+"/test"
            TPlist = getResultExp1(input_path,N)
            # print("ML"+str(number[j]))
            # print(TPlist)
            aveTP = sum(TPlist)/len(TPlist)
            # print("ML prec@"+str(N)+" = ",aveTP)
            ML_prec.insert(index, aveTP)

            index = index + 1

    # 結果をまとめる
    generateResultTable(EM_NF, EM_NNMU, ML_NF, ML_NNMU, EM_prec, ML_prec)

    # 確認用
    # print(EM_NF)
    # print(EM_NNMU)
    # print(ML_NF)
    # print(ML_NNMU)
    # print(EM_prec)
    # print(ML_prec)
