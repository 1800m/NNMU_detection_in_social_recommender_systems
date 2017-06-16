#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Created by Chihiro Miyamoto (2017)
#
# WWW13のNNMU検出の実装
#


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
from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import pylab
###############################################################################



"""
補助評価値行列の生成
ユーザIDに関して降順
@INPUT:
    input_path
@OUTPUT:
    Xaux : a auxiliary matrix of dimension N x M
"""
def getAuxiliaryMatrix(N,M,number):
    # movieLensXaux = list()
    # # MovieLensユーザデータ読み込み
    # index = 0   # インデックス用変数
    # input_path = "../data/exp1/auxiliary/ML_Auxiliary_"+str(N)+"x"+str(M)+".csv"
    # for line in codecs.open(input_path, 'r', 'utf-8'):
    #     # ,でスプリット
    #     # [0]：UserID
    #     # [1]：ItemID
    #     # [2]：Rating
    #     # [3]：Timestamp
    #     # [4]：Co-User Index
    #     # [5]：UserID
    #     # [6]：Co-Item Index
    #     # [7]：ItemID
    #     line_split = line.split(",")
    #     movieLensXaux.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
    #     index = index + 1

    auxiliaryMatrix = np.ones([N,M])    # 0で補助評価値行列を初期化
    # 補助評価値行列の生成
    # for i in range(len(movieLensXaux)):
    #     auxiliaryMatrix[int(movieLensXaux[i][4])][int(movieLensXaux[i][6])] = movieLensXaux[i][2]
    #
    # output_path = "../data/exp1/auxiliary/Xaux"+str(number)+".csv"
    # for i in range(len(auxiliaryMatrix)):
    #     out_data = auxiliaryMatrix[i]
    #     if(i == 0): # 1行目書き込み
    #         f = open(output_path, "w")
    #         i += 1
    #         print(out_data, end="\n", file=f)
    #     else:       # 2行目以降の追記
    #         f = open(output_path, "a")
    #         print(out_data, end="\n", file=f)

    return auxiliaryMatrix

"""
MLのターゲット評価値行列の生成
@INPUT:
    input_path
@OUTPUT:
    Xtgt : an target matrix of dimension N x M
"""
def getTargetMatrixML(N,M,number,count):
    # movieLensXtgt = list()   # 3結合の対応表を保持
    #
    # index = 0   # インデックス用変数
    # input_path = "../data/exp1/test_ML_"+str(number)+"/userData"+str(count)+".csv"
    # for line in codecs.open(input_path, 'r', 'utf-8'):
    #     # ,でスプリット
    #     # [0]：UserID
    #     # [1]：ItemID
    #     # [2]：Rating
    #     # [3]：Timestamp
    #     # [4]：Co-User Index
    #     # [5]：UserID
    #     # [6]：Co-Item Index
    #     # [7]：ItemID
    #     line_split = line.split(",")
    #     movieLensXtgt.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
    #     index = index + 1

    targetMatrix = np.ones([N,M])    # 0でターゲット評価値行列を初期化

    # # 補助評価値行列の生成
    # # ここで，100人にノイズを加える
    # for i in range(len(movieLensXtgt)):
    #     if i < N-100: # noise-free
    #         targetMatrix[int(movieLensXtgt[i][4])][int(movieLensXtgt[i][6])] = movieLensXtgt[i][2]
    #     else:   # NNMU
    #         if movieLensXtgt[i][2] != 0:
    #             while True: # ノイズが範囲内になるまで繰り返す
    #                 noise = random.randint(-4,4)
    #                 if noise != 0:
    #                     noisy_rating = int(movieLensXtgt[i][2]) + noise    # -4〜4の整数でノイズをのせる
    #                     # 評価値の範囲内か判定
    #                     if noisy_rating >= 1:
    #                         if noisy_rating <= 5:
    #                             targetMatrix[int(movieLensXtgt[i][4])][int(movieLensXtgt[i][6])] = noisy_rating
    #                             break
    #         else:
    #             targetMatrix[int(movieLensXtgt[i][4])][int(movieLensXtgt[i][6])] = 0
    #
    # output_path = "../data/exp1/result_ML_"+str(number)+"/Xtgt_ML"+str(count)+".csv"
    # for i in range(len(targetMatrix)):
    #     out_data = targetMatrix[i]
    #     if(i == 0): # 1行目書き込み
    #         f = open(output_path, "w")
    #         i += 1
    #         print(out_data, end="\n", file=f)
    #     else:       # 2行目以降の追記
    #         f = open(output_path, "a")
    #         print(out_data, end="\n", file=f)

    return targetMatrix

"""
EMのターゲット評価値行列の生成
@INPUT:
    input_path
@OUTPUT:
    Xtgt : an target matrix of dimension N x M
"""
def getTargetMatrixEM(N,M,number,count):
    # eachMovieXtgt = list()   # 3結合の対応表を保持
    #
    # index = 0   # インデックス用変数
    # input_path = "../data/exp1/test_EM_"+str(number)+"/userData"+str(count)+".csv"
    # for line in codecs.open(input_path, 'r', 'utf-8'):
    #     # ,でスプリット
    #     # [0]：UserID
    #     # [1]：ItemID
    #     # [2]：Rating
    #     # [3]：Timestamp
    #     # [4]：Co-User Index
    #     # [5]：UserID
    #     # [6]：Co-Item Index
    #     # [7]：ItemID
    #     line_split = line.split(",")
    #     eachMovieXtgt.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
    #     index = index + 1
    #
    targetMatrix = np.ones([N,M])    # 0でターゲット評価値行列を初期化

    # # 補助評価値行列の生成
    # # ここで，100人にノイズを加える
    # for i in range(len(eachMovieXtgt)):
    #     if i < N-100: # noise-free
    #         targetMatrix[int(eachMovieXtgt[i][4])][int(eachMovieXtgt[i][6])] = float(eachMovieXtgt[i][2])*5
    #     else:   # NNMU
    #         if eachMovieXtgt[i][2] != 0:
    #             while True: # ノイズが範囲内になるまで繰り返す
    #                 noise = random.randint(-4,4)
    #                 if noise != 0:
    #                     noisy_rating = float(eachMovieXtgt[i][2])*5 + noise    # -4〜4の整数でノイズをのせる
    #                     # 評価値の範囲内か判定
    #                     if noisy_rating >= 1:
    #                         if noisy_rating <= 5:
    #                             targetMatrix[int(eachMovieXtgt[i][4])][int(eachMovieXtgt[i][6])] = noisy_rating
    #                             break
    #         else:
    #             targetMatrix[int(eachMovieXtgt[i][4])][int(eachMovieXtgt[i][6])] = 0
    #
    # output_path = "../data/exp1/result_EM_"+str(number)+"/Xtgt_EM"+str(count)+".csv"
    # for i in range(len(targetMatrix)):
    #     out_data = targetMatrix[i]
    #     if(i == 0): # 1行目書き込み
    #         f = open(output_path, "w")
    #         i += 1
    #         print(out_data, end="\n", file=f)
    #     else:       # 2行目以降の追記
    #         f = open(output_path, "a")
    #         print(out_data, end="\n", file=f)

    return targetMatrix

"""
アイテム間類似度計算を行う
@INPUT:
    Xaux : a auxiliary matrix of dimension N x M
@OUTPUT:
    similarityMatrix : a similarity matrix of dimension M x M
"""
def getItemItemSimilarity(Xaux):
    # print(len(Xaux[0])) # アイテム数
    similarityMatrix = np.zeros([len(Xaux[0]), len(Xaux[0])])    # 0で類似度行列を初期化
    # print(len(Xaux))  # ユーザ数=500
    URave = np.zeros(len(Xaux))    # 0でユーザ毎の評価平均を格納する行列を初期化
    for i in range(len(Xaux)):
        URave[i] = sum(Xaux[i])/len(Xaux[i]) # ユーザの評価平均URaveを計算して格納

    # for i in range(len(URave)):
    #     print("URave[",i,"]=",URave[i])
    #
    # print("similarityMatrix=",len(similarityMatrix))    # アイテム数の300
    # print("similarityMatrix[0]=",len(similarityMatrix[0]))  # アイテム数の300

    # アイテム間類似度の対称行列を生成
    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            # print("ij = ", i,j)
            # if i == 298:
            #     if j == 221:
            #         print("ij =",i,j)
            #         print("item1 = ",Xaux[:,i])
            #         print("item2 = ",Xaux[:,j])
            #         print("URave = ",URave)

            if i == j:  # 同じアイテムへの類似度より１
                similarityMatrix[i][j] = 1
                # similarityMatrix[i][j] = adjusted_cosine(Xaux[:,i], Xaux[:,j], URave)
                break
            else:
                similarityMatrix[i][j] = adjusted_cosine(Xaux[:,i], Xaux[:,j], URave)
                if similarityMatrix[i][j] == 10:
                    print("similarityMatrix[",i,"][",j,"]はNaN値です")
                    similarityMatrix[i][j] = -1
                similarityMatrix[j][i] = similarityMatrix[i][j]
    return similarityMatrix

"""
adjusted cosine類似度を計算する
アイテムベクトルiとjのどちらかが0だったり，
アイテムiとjを同時に評価しているユーザが居なかったりすると，
NaN値になので10を返す
@INPUT:
    item1 : a vector of item i
    item2 : a vector of item j
    URave : a vector of each user average rating
@OUTPUT:
    similarity : a similarity between item i and item j
"""
def adjusted_cosine(item1, item2, URave):
    # print("item1 = ",item1)
    # print("item2 = ",item2)
    # print("URave = ",URave)

    sum_numerator = 0
    sum_denominator1 = 0
    sum_denominator2 = 0

    for i in range(len(URave)):
        if item1[i] != 0:   # Ui∧Ujの条件
            if item2[i] != 0:
                sum_numerator = sum_numerator + (item1[i] - URave[i]) * (item2[i] - URave[i])
                sum_denominator1 = sum_denominator1 + np.square(item1[i] - URave[i])
                sum_denominator2 = sum_denominator2 + np.square(item2[i] - URave[i])

    similarity = sum_numerator/(np.sqrt(sum_denominator1) * np.sqrt(sum_denominator2))
    if similarity != similarity:    # NaNかチェック
        similarity = 10
    return similarity

"""
重み計算を行う
@INPUT:
    S : a similarity matrix of dimension M x M
@OUTPUT:
    weightMatrix : a weight matrix of dimension M x M
"""
def getWeight(S):
    weightMatrix = np.zeros((len(S), len(S[0])))    # 行列の初期化
    for i in range(len(S)):
        for j in range(len(S[i])):
            if i == j:
                weightMatrix[i][j] = 0
            else:
                weightMatrix[i][j] = (S[i][j] + 1)/2

    return weightMatrix

"""
ワンステップ遷移行列の計算を行う
@INPUT:
    W : a weight matrix of dimension M x M
@OUTPUT:
    P : a transition matrix of dimension M x M
"""
def getTransition(W):
    P = np.zeros((len(W), len(W[0])))    # 行列の初期化
    for i in range(len(W)):
        for j in range(len(W[i])):
            if i == j:
                P[i][j] = 0
            else:
                P[i][j] = W[i][j]/sum(W[i,:])
                if P[i][j] != P[i][j]:  # NaN判定用
                    P[i][j] = 0
    return P

"""
ユーザプロファイルをyLとyUに並べ替える
@INPUT:
    y : an user profile vector of dimension 1 x M
@OUTPUT:
    yL : an user profile for rated items of dimension 1 x K
    yU : an user profile for unrated items of dimension 1 x (M-K)
    yIndex : an user profile index for yL + yU of dimension 1 x M
"""
def replaceUserProfile(y,flag):
    global K_index  # 0行だとエラー
    global U_index
    global yL
    global yU
    global yIndex
    # K_index = U_index = yL = yU = yIndex = np.array()

    K = 0   # ユーザの評価してるアイテム数
    U = 0   # ユーザが評価してないアイテム数

    # 初期化判定用フラグ
    K_flag = False
    U_flag = False

    # K_index = list()
    # U_index = list()
    # yL = list()
    # yU = list()
    # K_count = U_count = 0
    #
    # for i in range(len(y)):
    #     if 0 != y[i]:   # rated itemの処理
    #         K_index.insert(K_count, i)   # rated itemのインデックスを保持
    #         yL.insert(K_count,y[i])
    #         K_count = K_count + 1
    #     else:   # unrated itemの処理
    #         U_index.insert(U_count, i)   # unrated itemのインデックスを保持
    #         yU.insert(U_count,y[i])
    #         U_count = U_count + 1
    #
    # if flag == 1:
    #     return (K_index, U_index)
    # else:
    #     yIndex = np.zeros([1,K+U])   # アイテムのインデックス格納用
    #     # print("yIndex=",yIndex)
    #     # print("K_index=",K_index)
    #     for i in range(len(y)):
    #         if i < K:
    #             yIndex[0][i] = K_index[i]
    #         else:
    #             if U != 1:    # アイテムが1つだけのときの処理
    #                 yIndex[0][i] = U_index[i-K]
    #             else:
    #                 yIndex[0][i] = U_index
    #
    #     return (yL, yU, yIndex)

    for i in range(len(y)):
        if 0 != y[i]:   # rated itemの処理
            if(K_flag != True): # 1個目
                K_index = np.array(i)   # rated itemのインデックスを保持
                K_flag = True
                yL = np.array(y[i])
            else:
                K_index = np.append(K_index, i)
                yL = np.append(yL, y[i])
            K += 1
        else:   # unrated itemの処理
            if(U_flag != True): # 1個目
                U_index = np.array(i)   # unrated itemのインデックスを保持
                U_flag = True
                yU = np.array(y[i])
            else:
                U_index = np.append(U_index, i)
                yU = np.append(yU, y[i])
            U += 1

    if flag == 1:
        return (K_index, U_index)
    else:
        yIndex = np.zeros([1,K+U])   # アイテムのインデックス格納用
        # print("yIndex=",yIndex)
        # print("K_index=",K_index)
        for i in range(len(y)):
            if i < K:
                yIndex[0][i] = K_index[i]
            else:
                if U != 1:    # アイテムが1つだけのときの処理
                    yIndex[0][i] = U_index[i-K]
                else:
                    yIndex[0][i] = U_index

        return (yL, yU, yIndex)

"""
ワンステップ遷移確率行列の置き換えを行う
@INPUT:
    P : a transition matrix of dimension M x M
@OUTPUT:
    Prep : a replaced transition matrix of dimension M x M
"""
def replaceTransition(P, y):
    # K_index:評価済みアイテムのインデックス
    # U_index:未評価のアイテムのインデックス
    K_index, U_index = replaceUserProfile(y,1)
    try:
        K = len(K_index)
    except:
        K = 1
        temp = K_index.copy()
        print("K_index = ",K_index)
        K_index = list()
        K_index.insert(0,temp)
        print("K_index = ",K_index)
        print("U_index = ", U_index)
        print("K = ",K)


    # 代入処理
    tempPrep = np.zeros((len(P), len(P[0])))    # 行列の初期化
    for i in range(len(P)):
        for j in range(len(P[i])):
            if y[i] != 0:   # [I O]の代入
                if i == j:
                    tempPrep[i][j] = 1
                else:
                    tempPrep[i][j] = 0
            else:       # 式(3)の代入
                tempPrep[i][j] = P[i][j]

    # print(tempPrep)

    Prep = np.zeros((len(P), len(P[0])))    # 行列の初期化
    # 並べ替え処理
    # 行について
    for i in range(len(Prep)):
        if i < K:
            Prep[i,:] = tempPrep[K_index[i],:]
        else:
            try:
                Prep[i,:] = tempPrep[U_index[i - K],:]
            except:
                Prep[i,:] = tempPrep[U_index,:]
    # print("行入れ替えtempPrep")
    # print(Prep)
    tempPrep = Prep.copy()  # 深いコピー
    # 列について
    for j in range(len(Prep[0])):
        # print("j = ", j)
        if j < K:
            # print("K_index[j]=",K_index[j])
            Prep[:,j] = tempPrep[:,K_index[j]]
        else:
            try:
                Prep[:,j] = tempPrep[:,U_index[j - K]]
                # print("U_index[j]=",U_index[j-K])
                # print("tempPrep[:,U_index[j - K]] = ",tempPrep[:,U_index[j - K]])
            except:
                Prep[:,j] = tempPrep[:,U_index]
                # print("U_index[j]=",U_index)
                # print("tempPrep[:,U_index[j - K]] = ",tempPrep[:,U_index])
        # print(Prep)

    # yrep = np.zeros(len(y))
    # for i in range(len(y)):
    #     if i < len(K_index):
    #         yrep[i] = y[K_index[i]]
    #     else:
    #         print("yrep =",yrep)
    #         break
    # print("P.dot(y)=\n",P.dot(y))
    # print("Prep.dot(yrep)=\n",Prep.dot(yrep))
    return Prep


"""
最適化問題を解いて，各ユーザのノイズを示すスラック変数ξの値を返す
ξの要素数は評価を付けたアイテム数K
@INPUT:
    Prep : a replaced transition matrix of dimension M x M
    userplofile : an user profile vector of dimension 1 x M
    L : the Laplacian matrix of G
@OUTPUT:
    Xi : the optimal slack variables of dimension K x 1
"""
def calculateOptimizationProblem(Prep, userplofile, L):
    # 変数の初期化
    IO = RQ = 0
    Xi = I = O = R = Q = 0
    flag = False
    M = len(Prep)   # 行列のサイズ

    # ユーザプロファイルを分割してyLとyUを取得
    yL, yU, yIndex = replaceUserProfile(userplofile,0)
    # print("userplofile = ",userplofile)   # 元のユーザプロファイル
    # print("yL = ",yL) # ユーザが付けた評価値
    # print("yU = ",yU) # 未評価（0）
    # print("yIndex = ",yIndex) # yL→yUの順に並べ替えたユーザプロファイル(インデックス)

    # for i in range(len(Prep)):
    #     print("Prep =",Prep[i])
    temp = yL.copy()
    yL = np.zeros([1,len(temp)])
    for i in range(len(temp)):
        yL[0][i] = temp[i]


    # PrepのI，O，R，Qへの分割処理
    for i in range(M):
        if Prep[i][i] != 1: # 一部を評価していた場合
            I = np.identity(i)    # 単位行列Iの初期化
            O = np.zeros([i,M-i]) # ゼロ行列Oの初期化
            R = np.zeros([M-i,i]) # 1ステップ遷移確率行列の初期化from an unrated item to a rated item
            Q = np.zeros([M-i,M-i]) # 1ステップ遷移確率行列の初期化from an unrated item to an unrated item
            RQ = np.zeros([M-i,M])
            break
        else:   # 全て評価していた場合
            if i == (M-1):
                i = i + 1
                I = np.identity(i)    # 単位行列Iの初期化
                O = np.zeros([i,M-i]) # ゼロ行列Oの初期化
                R = np.zeros([M-i,i]) # 1ステップ遷移確率行列の初期化from an unrated item to a rated item
                Q = np.zeros([M-i,M-i]) # 1ステップ遷移確率行列の初期化from an unrated item to an unrated item
                RQ = np.zeros([M-i,M])
                flag = True

    K = len(I)  # 単位行列Iのサイズ

    # print("flag = ",flag)

    # [R Q]の代入とRとQへの分割処理
    if flag == False:
        for i in range(M-K):    # RQの代入
            RQ[i,:] = Prep[i+K,:]
        for i in range(M):
            if i < K:
                R[:,i] = RQ[:,i]    # Rへの分割
            else:
                Q[:,i-K] = RQ[:,i]  # Qへの分割

    # # 確認用
    # print("RQ =")
    # print(RQ)
    # print("I =")
    # print(I)
    # print("O =")
    # print(O)
    # print("R =")
    # print(R)
    # print("Q =")
    # print(Q)

    print(np.identity(M-K))
    # AとBの初期化
    A = np.zeros([M,K])
    B = np.zeros([M,1])
    IQinvR = (np.linalg.inv(np.identity(M-K)-Q)).dot(R)
    IQinvRyL = IQinvR.dot(yL.T)
    print("IQinvR =",IQinvR)
    print("yL =",yL)
    # print("IQinvRyL =",IQinvRyL)
    print("yU =",IQinvRyL)
    for i in range(M):
        if i < K:
            A[i,:] = I[i,:]
            # if 0 == len(yL):
            #     B[i,:] = yL
            # else:
            #     B[i,:] = yL[i,:]
            B[i][0] = yL[0][i]
        else:
            A[i,:] = IQinvR[i-K,:]
            if 1 == len(IQinvRyL):
                B[i][0] = IQinvRyL
            else:
                B[i][0] = IQinvRyL[i-K][0]
    print()
    print("A = ")
    print(A)
    print("B = ")
    print(B)

    print()
    tALA = ((A.T).dot(L)).dot(A)
    print("tALA =\n",tALA)

    val_lambda = 100    # トレードオフ
    Rmin = 1
    Rmax = 5
    optP = tALA+val_lambda*I
    optq = ((A.T).dot(L)).dot(B)
    optA = np.ones([1,K])
    optb = np.zeros([1,1])
    optG = np.zeros([2*K,K])
    opth = np.zeros([2*K,1])
    for i in range(2*K):
        if i < K:
            optG[i,:] = -1
            opth[i][0] = yL.T[i] - Rmin
        else:
            optG[i,:] = 1
            opth[i][0] = Rmax - yL.T[i - K]

    # optG = np.zeros([K,K])
    # opth = np.zeros([K,1])
    # for i in range(K):
    #     optG[i,:] = 1
    #     opth[i][0] = Rmax - yL.T[i]

    # for i in range(K):
    #     optG[i,:] = -1
    #     opth[i][0] = yL.T[i] - Rmin

    print("optP =")
    print(optP)
    print("\ntALB =\n",((A.T).dot(L)).dot(B))
    print("optq =")
    print(optq)
    # print("len(optq) =", len(optq))
    # print("optA = ")
    # print(optA)
    # print("optb = ")
    # print(optb)
    # print("optG = ")
    # print(optG)
    # print("opth = ")
    # print(opth)

    # cvxoptの独自matrixクラス
    cvxoptP = 2*matrix(optP)
    cvxoptq = matrix(optq)
    cvxoptG = matrix(optG)
    cvxopth = matrix(opth)
    cvxoptA = matrix(optA)
    cvxoptb = matrix(optb)

    print("cvxoptP =")
    print(cvxoptP)
    print("cvxoptq =")
    print(cvxoptq)
    print("cvxoptA =")
    print(cvxoptA)
    print("cvxoptb =")
    print(cvxoptb)
    print("cvxoptG =")
    print(cvxoptG)
    print("cvxopth =")
    print(cvxopth)

    opts = {'maxiters' : 200}
    sol = cvxopt.solvers.qp(cvxoptP,cvxoptq,cvxoptG,cvxopth,cvxoptA,cvxoptb,options = opts)
    print("sol[x]\n",sol["x"])
    print("sol[primal objective]\n",sol["primal objective"])
    Xi = sol["x"]

    return Xi

"""
ユーザプロファイルの平均ノイズの計算を行う
@INPUT:
    Xi : the optimal slack variables of dimension K x 1
@OUTPUT:
    rho : the average noise in the test user profile
"""
def getAverageNoise(Xi):
    sumXi = 0
    for i in range(len(Xi)):
        print("Xi["+str(i)+"] =",float(Xi[i]))
        sumXi = sumXi + abs(float(Xi[i]))

    print("sumXi =",sumXi)
    rho = sumXi/len(Xi)
    return rho

"""
ユーザプロファイルがNNMUか判定する
@INPUT:
    rho : the average noise in the test user profile
    threshold : threshold for NNMU detection
@OUTPUT:
    True or False
"""
def detectNNMU(rho, threshold):
    if rho > threshold:
        return True
    else:
        return False



###############################################################################


# メイン関数
if __name__ == "__main__":
    # X = [[1.0, 5.0, 4.0]]
    # Y = [[2.0, 5.0, 5.0]]
    # N = [[3.0, 3.5, 4.0]]
    # print(adjusted_cosine(X, Y, N))

#################################################
# 300
#################################################
    args = sys.argv
    # number = 100    # 共通アイテム数
    number = args[1]    # 共通アイテム数

    # N = int(500)    # ユーザ数
    # M = int(number)    # アイテム数
    N = int(4)    # ユーザ数
    M = int(4)    # アイテム数
    # Xaux = np.zeros([N, M])    # N*M行列の初期化
    # Xaux = np.random.rand(N,M)
    Xaux = np.array([[3.0, 5.0, 1.0, 0.0], [0.0, 2.0, 4.0, 0.0], [0.0, 1.0, 0.0, 2.0], [3.0, 4.0, 5.0, 2.0]])
    # 実験1の補助評価値行列
    print("補助評価値行列Xauxの取得")
    # Xaux = getAuxiliaryMatrix(N,M,number)
    # print("Xaux = ")
    # for i in range(len(Xaux)):
    #     print(Xaux[i])

    print("類似度行列の取得")
    similarityMatrix = getItemItemSimilarity(Xaux)
    # print("similarityMatrix = ")
    # for i in range(len(similarityMatrix)):
    #     print(similarityMatrix[i])

    print("重み行列Wの取得")
    W = getWeight(similarityMatrix)
    # print("W = ")
    # for i in range(len(W)):
    #     print(W[i])

    print("遷移確率行列Pの取得")
    P = getTransition(W)
    print("P = ")
    for i in range(len(P)):
        print(P[i])

    D = np.zeros([M,M])
    for i in range(M):
        for j in range(M):
            if i == j:
                D[i][j] = sum(W[i,:])
    # print("D = ")
    # for i in range(len(D)):
    #     print(D[i])

    # print("遷移確率行列Pの取得")
    # P = np.linalg.inv(D).dot(W)
    # print("P = ")
    # for i in range(len(P)):
    #     print(P[i])


    print("ラプラシアン行列Lの取得")
    L = D - W
    # print("L = ")
    # for i in range(len(W)):
    #     print(W[i])

    print("ターゲット評価値行列Xtgtの取得")
    # Xtgt_ML = getTargetMatrixML(N,M,number,count=0)
    # Xtgt_EM = getTargetMatrixEM(N,M,number,count=0)

    # Xtgt_ML = np.array([[3.0, 5.0, 1.0, 0.0], [0.0, 2.0, 4.0, 0.0], [0.0, 1.0, 0.0, 2.0], [3.0, 4.0, 5.0, 2.0]])
    Xtgt_ML = np.array([[3.0, 5.0, 1.0, 0.0], [0.0, 2.0, 4.0, 0.0], [0.0, 1.0, 0.0, 2.0], [3.0, 4.0, 5.0, 2.0]])

    print("ターゲット評価値行列の各ユーザプロファイルの評価値が含むノイズの取得")
    # 出力先のパス
    # output_path = "../data/exp1/result_ML_"+str(number)+"/test"+str(count)+".csv"
    for i in range(len(Xtgt_ML)):
        print("Xtgt_ML["+str(i)+",:] =",Xtgt_ML[i,:])
        # print("ユーザプロファイルにもとづき遷移行列Pを変形")
        Prep = replaceTransition(P, Xtgt_ML[i,:])
        print("Prep",i,"= ")
        print(Prep)
        # print("各ユーザプロファイルの評価値が含むノイズを計算")
        Xi = calculateOptimizationProblem(Prep, Xtgt_ML[i,:],L)
        rho = getAverageNoise(Xi)
        nnmuFlag = detectNNMU(rho,threshold=0.4)
        # print("Xi = ", Xi)
        print("rho = ",rho)
        # if nnmuFlag == True:
        #     print("No.",i,"user is NNMU.")
        # else:
        #     print("No.",i,"user is not NNMU.")

        # out_data = str(i+1)+","+str(rho)
        # if(i == 0): # 1行目書き込み
        #     f = open(output_path, "w")
        #     i += 1
        #     print(out_data, end="\n", file=f)
        # else:       # 2行目以降の追記
        #     f = open(output_path, "a")
        #     print(out_data, end="\n", file=f)
