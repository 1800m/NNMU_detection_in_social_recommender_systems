#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Created by Chihiro Miyamoto (2017)
#
# WWW13のNNMU検出の実装
#


try:
    import numpy as np
except:
    print("This implementation requires the numpy module.")
    exit(0)

import cvxopt
from cvxopt import matrix


###############################################################################

"""
アイテム間類似度計算を行う
@INPUT:
    Xaux : a auxiliary matrix of dimension N x K
@OUTPUT:
    similarityMatrix : a similarity matrix of dimension N x K
"""
def getItemItemSimilarity(Xaux):
    similarityMatrix = np.zeros((len(Xaux[0]), len(Xaux[0])))    # 0で類似度行列を初期化
    URave = np.zeros(len(Xaux))    # 0でユーザ毎の評価平均を格納する行列を初期化
    for i in range(len(Xaux)):
        URave[i] = sum(Xaux[i])/len(Xaux[i]) # ユーザの評価平均を計算して格納

    # アイテム間類似度の対称行列を生成
    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            print("ij = ", i,j)
            if i == j:  # 同じアイテムへの類似度より１
                # similarityMatrix[i][j] = 1
                similarityMatrix[i][j] = adjusted_cosine(Xaux[:,i], Xaux[:,j], URave)
                break
            else:
                similarityMatrix[i][j] = adjusted_cosine(Xaux[:,i], Xaux[:,j], URave)
                similarityMatrix[j][i] = similarityMatrix[i][j]
    return similarityMatrix

"""
adjusted cosine類似度を計算する
@INPUT:
    item1 : a vector of item i
    item2 : a vector of item j
    URave : a vector of each user average rating
@OUTPUT:
    similarity : a similarity between item i and item j
"""
def adjusted_cosine(item1, item2, URave):
    print("item1 = ",item1)
    print("item2 = ",item2)
    print("URave = ",URave)

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
    return P


# # アイテムアイテム相関グラフの可視化
# def itemItemCorrelationGraphConstruction():
#
#     return


###############################################################################


# メイン関数
if __name__ == "__main__":
    # X = [[1.0, 5.0, 4.0]]
    # Y = [[2.0, 5.0, 5.0]]
    # N = [[3.0, 3.5, 4.0]]
    # print(adjusted_cosine(X, Y, N))

    N = int(4)
    M = int(4)
    Xaux = np.zeros((N, M))    # N*M行列の初期化
    # Xaux = np.random.rand(N,M)
    Xaux = np.array([[3.0, 5.0, 1.0, 0.0], [0.0, 2.0, 4.0, 0.0], [0.0, 1.0, 0.0, 2.0], [3.0, 4.0, 5.0, 2.0]])
    print("Xaux = ")
    print(Xaux)

    similarityMatrix = getItemItemSimilarity(Xaux)
    print("similarityMatrix = ")
    print(similarityMatrix)

    W = getWeight(similarityMatrix)
    print("W = ")
    print(W)
    P = getTransition(W)
    print("P = ")
    print(P)

    D = np.zeros((M,M))
    for i in range(M):
        for j in range(M):
            if i == j:
                D[i][j] = sum(W[i,:])
    print("D = ")
    print(D)
    invD = np.linalg.inv(D)
    print("invD = ")
    print(invD)
    print("invDxW = ")
    print(invD.dot(W))
    print()

    # """
    # 最適化問題サンプル
    # """
    # P=matrix(np.diag([1.0,0.0]))
    # q=matrix(np.array([3.0,4.0]))
    # G=matrix(np.array([[-1.0,0.0],[0,-1.0],[-1.0,-3.0],[2.0,5.0],[3.0,4.0]]))
    # h=matrix(np.array([0.0,0.0,-15.0,100.0,80.0]))
    #
    # sol=cvxopt.solvers.qp(P,q,G,h)
    #
    # print(sol)
    # print(sol["x"])
    # print(sol["primal objective"])
