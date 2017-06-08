#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Created by Chihiro Miyamoto (2017)
#
# 補助評価値行列の要素数だとか色々な検査用

try:
    import sys
except:
    print("This implementation requires the sys module.")
    exit(0)
try:
    import random
except:
    print("This implementation requires the random module.")
    exit(0)
try:
    import numpy as np
except:
    print("This implementation requires the numpy module.")
    exit(0)
try:
    import codecs
except:
    print("This implementation requires the codecs module.")
    exit(0)
try:
    import cvxopt
    from cvxopt import matrix
except:
    print("This implementation requires the cvxopt module.")
    exit(0)


"""
補助評価値行列の生成
ユーザIDに関して降順
@INPUT:
    N : ユーザ数
    M : アイテム数
    number : 共通アイテム数
@OUTPUT:
    Xaux : a auxiliary matrix of dimension N x M
"""
def getAuxiliaryMatrix(N,M,number):
    movieLensXaux = list()
    # MovieLensユーザデータ読み込み
    index = 0   # インデックス用変数
    input_path = "../data/exp1/auxiliary/ML_Auxiliary_"+str(N)+"x"+str(M)+".csv"
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        # [4]：Co-User Index
        # [5]：UserID
        # [6]：Co-Item Index
        # [7]：ItemID
        line_split = line.split(",")
        movieLensXaux.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
        index = index + 1

    auxiliaryMatrix = np.zeros([N,M])    # 0で補助評価値行列を初期化
    # 補助評価値行列の生成
    for i in range(len(movieLensXaux)):
        auxiliaryMatrix[int(movieLensXaux[i][4])][int(movieLensXaux[i][6])] = movieLensXaux[i][2]

    output_path = "../data/exp1/auxiliary/Xaux"+str(number)+".csv"
    for i in range(len(auxiliaryMatrix)):
        out_data = auxiliaryMatrix[i]
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    return auxiliaryMatrix


if __name__ == "__main__":
    Xaux = getAuxiliaryMatrix(500, 300, 150)
    print(Xaux)
