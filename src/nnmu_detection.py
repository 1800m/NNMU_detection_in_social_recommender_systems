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
import pdb

###############################################################################



"""
補助評価値行列の生成
ユーザIDに関して降順
@INPUT:
    input_path
@OUTPUT:
    Xaux : a auxiliary matrix of dimension 500 x 300
"""
def getAuxiliaryMatrix(input_path):
    # movieLensXaux500x300 = list()
    # # MovieLensユーザデータ読み込み
    # index = 0   # インデックス用変数
    # for line in codecs.open(input_path, 'r', 'utf-8'):
    #     # ,でスプリット
    #     # [0]：UserID
    #     # [1]：ItemID
    #     # [2]：Rating
    #     # [3]：Timestamp
    #     line_split = line.split(",")
    #     movieLensXaux500x300.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n")))
    #     index = index + 1
    #
    # # ユーザIDの対応表
    # movieLensXaux500x300user = list()
    # # MovieLensユーザデータ読み込み
    # index = 0   # インデックス用変数
    # for line in codecs.open("../data/exp1/movieLensUser500.csv", 'r', 'utf-8'):
    #     # [0]：UserID
    #     if index == 0:
    #         movieLensXaux500x300user.insert(index, (index,line.rstrip("\n")))
    #         index = index + 1
    #     else:
    #         if movieLensXaux500x300user[index-1][1] != line.rstrip("\n"):
    #             movieLensXaux500x300user.insert(index, (index,line.rstrip("\n")))
    #             index = index + 1
    # # アイテムIDの対応表
    # movieLensXaux500x300item = list()
    # # MovieLensユーザデータ読み込み
    # index = 0   # インデックス用変数
    # for line in codecs.open("../data/exp1/item_taiou_Xaux.csv", 'r', 'utf-8'):
    #     # [0]：UserID
    #     if index == 0:
    #         movieLensXaux500x300item.insert(index, (index,line.rstrip("\n")))
    #         index = index + 1
    #     else:
    #         if movieLensXaux500x300item[index-1][1] != line.rstrip("\n"):
    #             movieLensXaux500x300item.insert(index, (index,line.rstrip("\n")))
    #             index = index + 1
    #
    # # print(movieLensXaux500x300)
    # # print(movieLensXaux500x300item)
    # # print(movieLensXaux500x300user)
    # # print(len(movieLensXaux500x300item))
    # # print(len(movieLensXaux500x300user))
    #
    # auxiliaryMatrix = np.zeros([500,300])    # 0で補助評価値行列を初期化
    # # 補助評価値行列の生成
    # for i in range(len(movieLensXaux500x300)):
    #     for j in range(len(movieLensXaux500x300user)):
    #         if movieLensXaux500x300[i][0] == movieLensXaux500x300user[j][1]:   # UserIDの比較
    #             break
    #     for k in range(len(movieLensXaux500x300item)):
    #         if movieLensXaux500x300[i][1] == movieLensXaux500x300item[k][1]:   # ItemID
    #             auxiliaryMatrix[int(movieLensXaux500x300user[j][0])][int(movieLensXaux500x300item[k][0])] = movieLensXaux500x300[i][2]
    #             break


    movieLensXaux500x300 = list()
    # MovieLensユーザデータ読み込み
    index = 0   # インデックス用変数
    input_path = "../data/exp1/ML_UserData_500x300.csv"
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
        movieLensXaux500x300.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
        index = index + 1

    auxiliaryMatrix = np.zeros([500,300])    # 0で補助評価値行列を初期化
    # 補助評価値行列の生成
    for i in range(len(movieLensXaux500x300)):
        auxiliaryMatrix[int(movieLensXaux500x300[i][4])][int(movieLensXaux500x300[i][6])] = movieLensXaux500x300[i][2]

    output_path = "../data/exp1/Xaux.csv"
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

"""
ターゲット評価値行列の生成
@INPUT:
    input_path
@OUTPUT:
    Xtgt : an target matrix of dimension 500 x 300
"""
def getTargetMatrix(input_path):
    movieLensXtgt900x300 = list()
    # MovieLensユーザデータ読み込み
    index = 0   # インデックス用変数
    input_path = "../data/exp1/ML_UserData_900x300.csv"
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
        movieLensXaux500x300.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6],line_split[7].rstrip("\n")))
        index = index + 1

    targetMatrix = np.zeros([900,300])    # 0でターゲット評価値行列を初期化
    # 補助評価値行列の生成
    for i in range(len(movieLensXtgt900x300)):
        targetMatrix[int(movieLensXtgt900x300[i][4])][int(movieLensXtgt900x300[i][6])] = movieLensXtgt900x300[i][2]

    output_path = "../data/exp1/Xtgt_ML.csv"
    for i in range(len(targetMatrix)):
        out_data = targetMatrix[i]
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    return targetMatrix

"""
アイテム間類似度計算を行う
@INPUT:
    Xaux : a auxiliary matrix of dimension N x K
@OUTPUT:
    similarityMatrix : a similarity matrix of dimension N x K
"""
def getItemItemSimilarity(Xaux):
    # print(len(Xaux[0])) # アイテム数=300
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
            #     if j == 0:
            #         print("ij =",i,j)
            #         print("item1 = ",Xaux[:,i])
            #         print("item2 = ",Xaux[:,j])
            #         print("URave = ",URave)
            #
            # if i == 299:
            #     if j == 0:
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
                similarityMatrix[j][i] = similarityMatrix[i][j]
    return similarityMatrix

"""
adjusted cosine類似度を計算する
アイテムベクトルのどちらかが0だと，NaN値になるので−1を返す
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
        similarity = -1
        print("アイテムに誰も評価してないよ")
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
    K = len(K_index)

    # print("K_index = ",K_index)
    # print("U_index = ", U_index)
    # print("K = ",K)
    # print("U = ",U)

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
    print("最適化ステップ")
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

    # AとBの初期化
    A = np.zeros([M,K])
    B = np.zeros([M,1])
    IQinvR = np.linalg.inv(np.identity(M-K)-Q).dot(R)
    IQinvRyL = np.linalg.inv(np.identity(M-K)-Q).dot(R).dot(yL.T)
    # print("IQinvR =",IQinvR)
    # print("yL =",yL)
    # print("IQinvRyL =",IQinvRyL)
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
    # print("A = ")
    # print(A)
    # print("B = ")
    # print(B)

    val_lambda = 100
    Rmin = 1
    Rmax = 5
    optP = (A.T).dot(L).dot(A)+val_lambda*I
    optq = (A.T).dot(L.dot(B))
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

    # print("optP =")
    # print(optP)
    # print("optq =")
    # print(optq)
    # print("optA = ")
    # print(optA)
    # print(opth)
    # print(optG)

    # cvxoptの独自matrixクラス
    cvxoptP = matrix(optP)
    cvxoptq = matrix(optq)
    cvxoptG = matrix(optG)
    cvxopth = matrix(opth)
    cvxoptA = matrix(optA)
    cvxoptb = matrix(optb)

    sol = cvxopt.solvers.qp(cvxoptP,cvxoptq,cvxoptG,cvxopth,cvxoptA,cvxoptb)
    # print(sol["x"])
    # print(sol["primal objective"])
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
        sumXi = sumXi + abs(Xi[i])
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


    N = int(500)    # ユーザ数
    M = int(300)    # アイテム数
    Xaux = np.zeros([N, M])    # N*M行列の初期化
    # Xaux = np.random.rand(N,M)
    # Xaux = np.array([[3.0, 5.0, 1.0, 0.0], [0.0, 2.0, 4.0, 0.0], [0.0, 1.0, 0.0, 2.0], [3.0, 4.0, 5.0, 2.0]])
    # 実験1の補助評価値行列
    print("補助評価値行列の取得")
    Xaux = getAuxiliaryMatrix('../data/exp1/movieLensUserData500x300down.csv')
    # print("ターゲット評価値行列の取得")
    # Xaux = getTargetMatrix('../data/exp1/movieLensUserData900x300.csv')

    Xtgt = getAuxiliaryMatrix('../data/exp2/movieLensUserItemCount300.csv')   # 実験2

    print("類似度行列の取得")
    similarityMatrix = getItemItemSimilarity(Xaux)
    # print("similarityMatrix = ")
    # for i in range(len(similarityMatrix)):
    #     print("No.",i)
    #     print(similarityMatrix[i])

    print("重み行列の取得")
    W = getWeight(similarityMatrix)
    # print("W = ")
    # print(W)

    print("遷移確率行列の取得")
    P = getTransition(W)
    # print("P = ")
    # print(P)

    D = np.zeros([M,M])
    for i in range(M):
        for j in range(M):
            if i == j:
                D[i][j] = sum(W[i,:])
    # print("D = ")
    # print(D)

    print("ラプラシアン行列Lの取得")
    L = D - W
    # print("L = ")
    # print(L)
    # print(Xaux[0,:])

    print("各評価値が含むノイズの取得")
    for i in range(N):
        Prep = replaceTransition(P, Xtgt[i,:])
        # print("Prep",i,"= ")
        # print(Prep)
        Xi = calculateOptimizationProblem(Prep, Xtgt[i,:],L)
        rho = getAverageNoise(Xi)
        nnmuFlag = detectNNMU(rho,threshold=0.3)
        # print("Xi = ", Xi)
        # print("rho = ",rho)
        # if nnmuFlag == True:
        #     print("No.",i,"user is NNMU.")
        # else:
        #     print("No.",i,"user is not NNMU.")

        output_path = "../data/exp1/outputNNMU.csv"
        out_data = rho
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)
