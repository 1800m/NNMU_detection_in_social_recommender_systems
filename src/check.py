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

from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import pylab
import sqlite3

"""
データベースとの接続
"""
def connectDB(dbname):
    global conn
    global c
    # データベースに接続
    conn = sqlite3.connect(dbname)  # Connectionオブジェクトが作成
    c = conn.cursor()   # SQL文を実行するには，ConnectionオブジェクトからさらにCursorオブジェクトを作成

"""
テーブルの削除
"""
def deleteTable(tbname):
    sql = "drop table "+tbname
    c.execute(sql)

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
EachMovieTitleをMovieLensと部分一致させた比較結果(MatchID.csv)を読み込みテーブルに格納
MatchID
[0]:EachMovie ItemID
[1]:MovieLens ItemID
"""
def readMatchID():
    deleteTable("MatchID")
    create_table = "create table MatchID (EM_ItemID int, ML_ItemID int)"
    c.execute(create_table)

    input_path = ""
    sql = ""
    index = 0   # インデックス用変数
    for line in execute():
        # ,でスプリット
        # [0]：EM_ItemID
        # [1]：ML_ItemID
        line_split = line.split(",")
        insert_sql = "insert into MatchID (EM_ItemID, ML_ItemID) values (?, ?)"
        insert_data = (line_split[0],line_split[1].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1
    conn.commit()   # commit()しないと変更がかからない

"""
EachMovieTitleをMovieLensの共通アイテム数300でのMovieLensの全ユーザデータ
[0]:UserID
[1]:ItemID
[2]:Rating
[3]:Timestamp
"""
def createMovieLensData_Item300():
    create_table = "create table MovieLensData_Item300 (UserID int, ItemID int, Rating int, Timestamp int)"
    c.execute(create_table)

    input_path = '../data/exp1/movieLensUserData300.csv'
    # MovieLensのデータ読み込み
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        line_split = line.split(",")
        insert_sql = "insert into MovieLensData_Item300 (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (line_split[0],line_split[1],line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない




"""
EachMovieTitleをMovieLensの共通アイテム数300でのMovieLensの全ユーザデータ
[0]:UserID
[1]:ItemID
[2]:Rating
[3]:Timestamp
"""
def createMovieLensData_Item300():
    create_table = "create table MovieLensData_Item300 (UserID int, ItemID int, Rating int, Timestamp int)"
    c.execute(create_table)

    input_path = '../data/exp1/movieLensUserData300.csv'
    # MovieLensのデータ読み込み
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        line_split = line.split(",")
        insert_sql = "insert into MovieLensData_Item300 (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (line_split[0],line_split[1],line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない


if __name__ == "__main__":
    # Xaux = getAuxiliaryMatrix(500, 300, 300)
    # # print(Xaux)
    #
    # # 要素数を数える
    # print(len(Xaux))
    # print(len(np.where(Xaux != 0)[0]))

    # # Problem data.
    # n = 4
    # S = matrix([[ 4e-2,  6e-3, -4e-3,    0.0 ],
    #             [ 6e-3,  1e-2,  0.0,     0.0 ],
    #             [-4e-3,  0.0,   2.5e-3,  0.0 ],
    #             [ 0.0,   0.0,   0.0,     0.0 ]])
    # pbar = matrix([.12, .10, .07, .03])
    # G = matrix(0.0, (n,n))
    # G[::n+1] = -1.0
    # h = matrix(0.0, (n,1))
    # A = matrix(1.0, (1,n))
    # b = matrix(1.0)
    # print(G)
    #
    # # Compute trade-off.
    # N = 100
    # mus = [ 10**(5.0*t/N-1.0) for t in range(N) ]
    # portfolios = [ qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus ]
    # returns = [ dot(pbar,x) for x in portfolios ]
    # risks = [ sqrt(dot(x, S*x)) for x in portfolios ]
    #
    # # Plot trade-off curve and optimal allocations.
    # pylab.figure(1, facecolor='w')
    # pylab.plot(risks, returns)
    # pylab.xlabel('standard deviation')
    # pylab.ylabel('expected return')
    # pylab.axis([0, 0.2, 0, 0.15])
    # pylab.title('Risk-return trade-off curve (fig 4.12)')
    # pylab.yticks([0.00, 0.05, 0.10, 0.15])
    #
    # pylab.figure(2, facecolor='w')
    # c1 = [ x[0] for x in portfolios ]
    # c2 = [ x[0] + x[1] for x in portfolios ]
    # c3 = [ x[0] + x[1] + x[2] for x in portfolios ]
    # c4 = [ x[0] + x[1] + x[2] + x[3] for x in portfolios ]
    # pylab.fill(risks + [.20], c1 + [0.0], '#F0F0F0')
    # pylab.fill(risks[-1::-1] + risks, c2[-1::-1] + c1, facecolor = '#D0D0D0')
    # pylab.fill(risks[-1::-1] + risks, c3[-1::-1] + c2, facecolor = '#F0F0F0')
    # pylab.fill(risks[-1::-1] + risks, c4[-1::-1] + c3, facecolor = '#D0D0D0')
    # pylab.axis([0.0, 0.2, 0.0, 1.0])
    # pylab.xlabel('standard deviation')
    # pylab.ylabel('allocation')
    # pylab.text(.15,.5,'x1')
    # pylab.text(.10,.7,'x2')
    # pylab.text(.05,.7,'x3')
    # pylab.text(.01,.7,'x4')
    # pylab.title('Optimal allocations (fig 4.12)')
    # pylab.show()



    # 重複検証
    deleteTable("MatchIdTop100")
    create_table = "create table MatchIdTop100 (EM_ItemID int, ML_ItemID int, EM_Count int, ML_Count int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop100.csv'
    # MovieLensのデータ読み込み
    index = 0

    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：EachMovie ItemID
        # [1]：MovieLens ItemID
        # [2]：EachMovie ItemIDの被評価回数
        # [3]：MovieLens ItemIDの被評価回数
        # [3]について降順に並べている
        line_split = line.split(",")
        insert_sql = "insert into MatchIdTop100 (EM_ItemID, ML_ItemID, EM_Count, ML_Count) values (?, ?, ?, ?)"
        insert_data = (line_split[0], line_split[1], line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1
