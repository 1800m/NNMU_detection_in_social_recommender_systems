#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Created by Chihiro Miyamoto (2017)
#
# WWW13のNNMU検出の実装
# データセット用

import codecs
import numpy as np
import sqlite3

class DataConstructor:
    """
    Class to construct noisy data from file and obtain relevant data structures
    """
    def __init__(self):
        """
        Constructor
        """
        self.eachMovies = list()
        self.movieLens = list()
        self.matchingIndex = list()

        self.movieLensItem = list()
        self.movieLensUserData = list()
        self.eachMovieUserData = list()

        self.movieLensUserData300Item = list()
        self.eachMovieUserData300Item = list()
        self.movieLensUserDataCount = list()
        self.eachMovieUserDataCount = list()

        self.countMovieLensItem = np.zeros(1683)    # アイテム1682種類（0を追加しているため+1の要素数）
        self.countEachMovieItem = np.zeros(1649)    # アイテム1629種類（0を追加しているため+1の要素数）
        self.countMovieLensUser = np.zeros(944)    # ユーザ943人（0を追加しているため+1の要素数）
        self.countEachMovieUser = np.zeros(74415)    # ユーザ72916人（0を追加しているため+1の要素数）
        self.movieLensXauxUser500 = list()
        self.movieLensXauxItem300 = list()

        self.movieLensXauxItem300Exp2 = list()
        self.movieLensXauxUser500Exp2 = list()
        self.movieLensXauxUser900Exp2 = list()
        self.movieLensUserData500x300 = list()
        self.movieLensUserData900x300 = list()


    def readFile(self, filename, flag):
        """
        Reads datas from a specified file
        """
        i = 0   # インデックス用変数
        if flag == 1:   # EachMovie用
            for line in codecs.open(filename, 'r', 'utf-8'):
                # タブでスプリット
                # [0]：MovieID
                # [1]：MovieTitle
                line_split = line.split("	")
                self.eachMovies.insert(i, (line_split[0],line_split[1]))
        else:           # MovieLens用
            for line in codecs.open(filename, 'r', 'utf-8'):
                # |でスプリット
                # [0]：MovieID
                # [1]：MovieTitle
                line_split = line.split("|")
                self.movieLens.insert(i, (line_split[0],line_split[1]))

    """
    EachMovieとMovieLensの共通アイテムのマッチング
    """
    def matchFile(self):
        index = 0   # インデックス用変数
        for i in range(len(self.eachMovies)):
            for j in range(len(self.movieLens)):
                if self.eachMovies[i][1] in self.movieLens[j][1]:
                    self.matchingIndex.insert(index, (self.eachMovies[i][0],self.movieLens[j][0]))
                    index = index + 1
                    break

    """
    同名のアイテム
    colume 0：EachMovieのアイテムID
    colume 1：MovieLensのアイテムID
    を出力
    """
    def writeMatchList(self, output_path):
        for i in range(len(self.matchingIndex)):
            out_data = str(self.matchingIndex[i][0]) + u',' + str(self.matchingIndex[i][1])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    """
    共通アイテムのインデックス読み込み
    """
    def readMatchingIndex(self, filename):
        i = 0   # インデックス用変数
        for line in codecs.open(filename, 'r', 'utf-8'):
            # ,でスプリット
            # [0]：MovieID
            # [1]：MovieTitle
            line_split = line.split(",")
            self.matchingIndex.insert(i, (line_split[0],line_split[1].rstrip("\n")))
            i = i + 1

    """
    MovieLensとEachMovieのユーザデータ読み込み
    """
    def readUserData(self):
        dc_file = '../data/'

        # MovieLensユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"MovieLens/u.data", 'r', 'utf-8'):
            # tabでスプリット
            # [0]：UserID
            # [1]：ItemID
            # [2]：Rating
            # [3]：Timestamp
            line_split = line.split("	")
            self.movieLensUserData.insert(i, (line_split[0],line_split[1], line_split[2],line_split[3].rstrip("\n")))
            i = i + 1

        # EachMovieユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"EachMovie/Vote.txt", 'r', 'utf-8'):
            # tabでスプリット
            # [0]：UserID
            # [1]：ItemID
            # [2]：Rating
            # [3]：Weight
            # [4]：Timestamp
            line_split = line.split("	")
            self.eachMovieUserData.insert(i, (line_split[0],line_split[1], line_split[2],line_split[4].rstrip("\n")))
            i = i + 1

    """
    MovieLensとEachMovieのユーザデータ読み込み
    """
    def readCountUserData(self):
        dc_file = '../data/'

        # MovieLensユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"movieLensItemCount.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：ItemID
            # [1]：被評価回数
            line_split = line.split(",")
            self.movieLensUserDataCount.insert(i, (line_split[0],line_split[1].rstrip("\n")))
            i = i + 1

        # EachMovieユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"eachMovieItemCount.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：ItemID
            # [1]：被評価回数
            line_split = line.split(",")
            self.eachMovieUserDataCount.insert(i, (line_split[0],line_split[1].rstrip("\n")))
            i = i + 1

    """
    MovieLensユーザデータから評価数が多いアイテムを取得
    """
    def getItemCountMovieLens(self):
        for i in range(len(self.movieLensUserData)):
            self.countMovieLens[int(self.movieLensUserData[i][1])] = self.countMovieLens[int(self.movieLensUserData[i][1])] + 1

        output_path = "../data/countMovieLens.data"
        for i in range(len(self.countMovieLens)):
            out_data = str(self.countMovieLens[i])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    """
    EachMovieユーザデータから評価数が多いアイテムを取得
    """
    def getItemCountEachMovie(self):
        for i in range(len(self.eachMovieUserData)):
            self.countEachMovie[int(self.eachMovieUserData[i][1])] = self.countEachMovie[int(self.eachMovieUserData[i][1])] + 1

        output_path = "../data/countEachMovie.csv"
        for i in range(len(self.countEachMovie)):
            out_data = str(self.countEachMovie[i])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    """
    MovieLensの評価数が多いアイテムに基づき，EachMovieとMovieLensからI∧=300のユーザデータを取得
    """
    def getMatchItemList(self):
        for i in range(len(300)):
            for j in range(len(self.matchingIndex)):
                if self.matchingIndex[j][1] == self.countMovieLens[i][0]:
                    print()
                    # for k in range(len(self.movieLensUserData)):
                    #     if
                    #     self.movieLensUserData300Item.insert(i,)

        output_path = "../data/movieLensUserData300Item.csv"
        for i in range(len(self.movieLensUserData300Item)):
            out_data = str(self.movieLensUserData300Item[i])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    """
    MovieLensからI∧＝300のアイテムを評価したユーザ抽出
    """
    def getMatchUserData300Item(self):
        indexML = 0   # MLインデックス用変数
        indexEM = 0   # EMインデックス用変数
        for i in range(300):
            for j in range(len(self.movieLensUserData)):
                if self.matchingIndex[i][1] == self.movieLensUserData[j][1]: # MLID
                    self.movieLensUserData300Item.insert(indexML, self.movieLensUserData[j])
                    indexML = indexML + 1

            for j in range(len(self.eachMovieUserData)):
                if self.matchingIndex[i][0] == self.eachMovieUserData[j][1]: # ELID
                    self.eachMovieUserData300Item.insert(indexEM, self.eachMovieUserData[j])
                    indexEM = indexEM + 1

    """
    MovieLensからI∧＝300のアイテムを評価したユーザの出力
    """
    def writeMatchUserData300Item(self):
        output_path = "../data/movieLensUserData300Item.csv"
        for i in range(len(self.movieLensUserData300Item)):
            out_data = self.movieLensUserData300Item[i][0]+","+self.movieLensUserData300Item[i][1]+","+self.movieLensUserData300Item[i][2]+","+self.movieLensUserData300Item[i][3]
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

        output_path = "../data/eachMovieUserData300Item.csv"
        for i in range(len(self.eachMovieUserData300Item)):
            out_data = self.eachMovieUserData300Item[i][0]+","+self.eachMovieUserData300Item[i][1]+","+self.eachMovieUserData300Item[i][2]+","+self.eachMovieUserData300Item[i][3]
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)



    """
    共通アイテム300のMovieLensとEachMovieのユーザデータ読み込み
    """
    def readCountUserData300(self):
        dc_file = '../data/'

        # MovieLensユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"movieLensUserData300Item.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：UserID
            # [1]：ItemID
            # [2]：Rating
            # [3]：Timestamp
            line_split = line.split(",")
            self.movieLensUserData300Item.insert(i, (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n")))
            i = i + 1

        # EachMovieユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"eachMovieUserData300Item.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：UserID
            # [1]：ItemID
            # [2]：Rating
            # [3]：Timestamp
            line_split = line.split(",")
            self.eachMovieUserData300Item.insert(i, (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n")))
            i = i + 1

    """
    ユーザの評価回数を数えて取得
    """
    def getUserCount300(self):
        # ML処理
        for i in range(len(self.movieLensUserData300Item)):
            self.countMovieLensUser[int(self.movieLensUserData300Item[i][0])] = self.countMovieLensUser[int(self.movieLensUserData300Item[i][0])] + 1

        output_path = "../data/movieLensUserCount300.csv"
        for i in range(len(self.countMovieLensUser)):
            out_data = str(self.countMovieLensUser[i])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

        # EM処理
        for i in range(len(self.eachMovieUserData300Item)):
            self.countEachMovieUser[int(self.eachMovieUserData300Item[i][0])] = self.countEachMovieUser[int(self.eachMovieUserData300Item[i][0])] + 1

        output_path = "../data/eachMovieUserCount300.csv"
        for i in range(len(self.countEachMovieUser)):
            out_data = str(self.countEachMovieUser[i])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)



    """
    MovieLensから抽出した
    500x300の補助評価値行列に必要なデータの読み込み
    movieLensXauxUser500
    [0]：UserID
    [1]：評価回数
    movieLensUserData300Item300
    [0]：UserID
    [1]：ItemID
    [2]：Rating
    [3]：Timestamp
    """
    def readAuxiliaryMatrixData(self):
        dc_file = '../data/'
        # MovieLensユーザデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"movieLensUserCount300.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：UserID
            # [1]：評価回数
            line_split = line.split(",")
            self.movieLensXauxUser500.insert(i, (line_split[0],line_split[1].rstrip("\n")))
            i = i + 1
            if i == 500:    # 上位500人分
                break

        dc_file = '../data/'
        # MovieLensデータ読み込み
        i = 0   # インデックス用変数
        for line in codecs.open(dc_file+"movieLensUserData300Item.csv", 'r', 'utf-8'):
            # ,でスプリット
            # [0]：UserID
            # [1]：ItemID
            # [2]：Rating
            # [3]：Timestamp
            line_split = line.split(",")
            self.movieLensUserData300Item.insert(i, (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n")))
            i = i + 1


    """
    MovieLensから抽出した
    500x300の補助評価値行列用データの取得
    """
    def getAuxiliaryMatrixData(self):
        index = 0
        for i in range(len(self.movieLensUserData300Item)):
            for j in range(len(self.movieLensXauxUser500)):
                if self.movieLensUserData300Item[i][0] == self.movieLensXauxUser500[j][0]:  # 上位500人のユーザならば追加
                    self.movieLensXauxItem300.insert(index, self.movieLensUserData300Item[i])
                    index = index + 1
                    break

        output_path = "../data/movieLensXaux500x300.csv"
        for i in range(len(self.movieLensXauxItem300)):
            out_data = self.movieLensXauxItem300[i][0]+","+self.movieLensXauxItem300[i][1]+","+self.movieLensXauxItem300[i][2]+","+self.movieLensXauxItem300[i][3]
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)




    """
    実験2の補助評価値行列用のcsv出力
    """
    def getAuxiliaryMatrixDataForExp2(self):
        # 上位300アイテム分の読み込み
        input_path = '../data/exp2/movieLensItemCountTop300.csv'
        # MovieLensの上位300アイテム読み込み
        index = 0   # インデックス用変数
        for line in codecs.open(input_path, 'r', 'utf-8'):
            # ,でスプリット
            # [0]：ItemID
            # [1]：評価回数
            line_split = line.split(",")
            self.movieLensXauxItem300Exp2.insert(index, (line_split[0],line_split[1].rstrip("\n")))
            index = index + 1

        # 上位900ユーザ分の読み込み
        input_path = '../data/exp2/movieLensUserCountTop900.csv'
        index = 0
        for line in codecs.open(input_path, 'r', 'utf-8'):
            # ,でスプリット
            # [0]：UserID
            # [1]：評価回数
            line_split = line.split(",")
            self.movieLensXauxUser900Exp2.insert(index, (line_split[0],line_split[1].rstrip("\n")))
            index = index + 1

        # print(self.movieLensXauxUserExp2)
        # print(len(self.movieLensXauxUserExp2))    # 300
        # print(self.movieLensXauxItemExp2)
        # print(len(self.movieLensXauxItemExp2))  # 900

        # アイテムIDを基に，900人分の評価値だけ抜き出す
        # self.movieLensXauxUser900Exp2
        # [0]：UserID
        # [1]：評価回数
        # self.movieLensXauxItem300Exp2
        # [0]：ItemID
        # [1]：評価回数
        # self.movieLensUserData
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        index = 0
        for i in range(len(self.movieLensXauxUser900Exp2)):    # 900人分
            for j in range(len(self.movieLensUserData)):  # 生データ
                if self.movieLensXauxUser900Exp2[i][0] == self.movieLensUserData[j][0]:    # 上位900のUserIDの比較
                    for k in range(len(self.movieLensXauxItem300Exp2)):
                        if self.movieLensXauxItem300Exp2[k][0] == self.movieLensUserData[j][1]:    # 上位300のItemIDの比較
                            self.movieLensUserData900x300.insert(index,self.movieLensUserData[j])
                            index = index + 1
                            break

        # print(self.movieLensUserData900x300)
        # print(len(self.movieLensUserData900x300)) # 29839

        # 出力
        output_path = "../data/exp2/movieLensUserData900x300.csv"
        for i in range(len(self.movieLensUserData900x300)):
            out_data = self.movieLensUserData900x300[i][0]+","+self.movieLensUserData900x300[i][1]+","+self.movieLensUserData900x300[i][2]+","+self.movieLensUserData900x300[i][3]
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)


"""
実験1の補助評価値行列用の共通アイテム300を評価している全ユーザの出力
"""
def getMLUserData300ForExp1():
    commonItemTop300 = list()   # 共通アイテムのIDを保持
    # 上位300の共通アイテムの読み込み
    input_path = '../data/exp1/matchIdTop300.csv'
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：EachMovieのItemID
        # [1]：MovieLensのItemID
        # [2]：EachMovieの評価回数
        # [3]：MovieLensの評価回数
        line_split = line.split(",")
        commonItemTop300.insert(index, (line_split[0],line_split[1]))
        index = index + 1

    # 共通アイテム300を含むMovieLensのユーザを抜き出す
    # self.movieLensUserData
    # [0]：UserID
    # [1]：ItemID
    # [2]：Rating
    # [3]：Timestamp
    index = 0
    movieLensUserData300 = list()
    for i in range(len(dc.movieLensUserData)):
        # commonItemTop300
        # [j][0]：EachMovie ItemID
        # [j][1]：MovieLens ItemID
        for j in range(len(commonItemTop300)):
            if dc.movieLensUserData[i][1] == commonItemTop300[j][1]: # アイテムIDの一致判定
                movieLensUserData300.insert(index,dc.movieLensUserData[i])
                index = index + 1
                break

    # print(movieLensUserData300)
    # print(len(movieLensUserData300)) # 47822

    # movieLensUserData300の出力
    output_path = "../data/exp1/movieLensUserData300.csv"
    for i in range(len(movieLensUserData300)):
        out_data = movieLensUserData300[i][0]+","+movieLensUserData300[i][1]+","+movieLensUserData300[i][2]+","+movieLensUserData300[i][3]
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


"""
実験1の補助評価値行列用のcsv出力
movieLensUserData500x300.csv
"""
def getAuxiliaryMatrixDataForExp1():
    movieLensUserCountAlldown = list()   # 評価しているユーザ情報の保持
    # 上位300の共通アイテムを評価しているユーザ情報の読み込み
    input_path = '../data/exp1/movieLensUserCountAlldown.csv'
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：UserID
        # [1]：評価回数
        line_split = line.split(",")
        movieLensUserCountAlldown.insert(index, (line_split[0],line_split[1].rstrip("\n")))
        index = index + 1

    movieLensUserData300 = list()   # 共通アイテム300を評価しているユーザ情報の保持
    # 上位300の共通アイテムを評価しているユーザ情報の読み込み
    input_path = '../data/exp1/movieLensUserData300down.csv'
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        line_split = line.split(",")
        movieLensUserData300.insert(index, (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n")))
        index = index + 1

    # 評価数が上位500人分格納
    user500 = np.zeros(500) # 500人分のID保存
    index = 0
    for i in range(len(movieLensUserCountAlldown)):
        flag = False
        for j in range(len(user500)):
            if user500[j] != 0:
                if user500[j] == movieLensUserCountAlldown[i][0]:
                    flag = True
                    break
            else:
                break
        if flag == False:
            user500[index] = movieLensUserCountAlldown[i][0]
            index = index + 1
        if index == 500:    # 500人格納済み
            break

    # movieLensUser500の出力
    output_path = "../data/exp1/movieLensUser500.csv"
    for i in range(len(user500)):
        out_data = int(user500[i])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


    # 共通アイテム300を含むMovieLensのユーザを500人抜き出す
    # 評価回数が多い順に見ていく
    # movieLensUserData300[i]
    # [0]：UserID
    # [1]：ItemID
    # [2]：Rating
    # [3]：Timestamp
    index = 0
    counter = 0 # 挿入が行われない回数を保持
    movieLensUserData500x300 = list()   # 500人分の保持
    for i in range(len(movieLensUserData300)):
        for j in range(len(user500)):    # 上位500人分まわす
            if movieLensUserData300[i][0] == user500[j]: # ユーザIDの一致判定
                movieLensUserData500x300.insert(index,movieLensUserData300[i])
                index = index + 1
                break


    # print(movieLensUserData500x300)
    # print(len(movieLensUserData500x300)) # 40586

    # movieLensUserData500x300の出力
    output_path = "../data/exp1/movieLensUserData500x300.csv"
    for i in range(len(movieLensUserData500x300)):
        out_data = movieLensUserData500x300[i][0]+","+movieLensUserData500x300[i][1]+","+movieLensUserData500x300[i][2]+","+movieLensUserData500x300[i][3]
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


"""
MLのユーザの評価回数を出力する
"""
def getUserCountML():
    countUserMLAll = np.zeros(943) # MLのユーザ毎の評価回数を格納
    # self.movieLensUserData
    # [0]：UserID
    # [1]：ItemID
    # [2]：Rating
    # [3]：Timestamp
    for i in range(len(dc.movieLensUserData)):
        countUserMLAll[int(dc.movieLensUserData[i][0]) - 1] = countUserMLAll[int(dc.movieLensUserData[i][0]) - 1] + 1

    output_path = "../data/movieLensUserCountAll.csv"
    for i in range(len(countUserMLAll)):
        out_data = str(i+1)+","+str(countUserMLAll[i])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


"""
MLとEMのマッチングの具体的な回数を返す
"""
def getMatchCountEMtoML():
    # マッチングデータの読み取り
    input_path = '../data/matchID.csv'
    matchID_num = list()
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：EachMovieのアイテムID
        # [1]：MovieLensのアイテムID
        line_split = line.split(",")
        matchID_num.insert(index, (line_split[0],line_split[1].rstrip("\n")))
        index = index + 1

    countMatchEMtoML = list() # MLのユーザ毎の評価回数を格納
    # self.movieLensUserData
    # [0]：UserID
    # [1]：ItemID
    # [2]：Rating
    # [3]：Timestamp
    # self.eachMovieUserData
    # [0]：UserID
    # [1]：ItemID
    # [2]：Rating
    # [3]：Timestamp

    for i in range(len(matchID_num)):
        countML = 0
        countEM = 0
        for j in range(len(dc.movieLensUserData)):
            if matchID_num[i][1] == dc.movieLensUserData[j][1]:
                countML = countML + 1
        for j in range(len(dc.eachMovieUserData)):
            if matchID_num[i][0] == dc.eachMovieUserData[j][1]:
                countEM = countEM + 1
        countMatchEMtoML.insert(i, (matchID_num[i],(countEM,countML)))

    output_path = "../data/matchID_and_Count_All.csv"
    for i in range(len(countMatchEMtoML)):
        out_data = str(countMatchEMtoML[i][0][0])+","+str(countMatchEMtoML[i][0][1])+","+str(countMatchEMtoML[i][1][0])+","+str(countMatchEMtoML[i][1][1])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


"""
メイン関数
"""
if __name__ == "__main__":
        dc = DataConstructor()
        dc_file = '../data/'

        """
        共通アイテムマッチング用
        """
        # dc.readFile(dc_file+"EachMovie/Movie.txt", 1)
        # dc.readFile(dc_file+"MovieLens/u.item", 2)
        # dc.matchFile()
        # dc.writeMatchList(dc_file+"matchID.csv")

        """
        データセット作成用
        """
        # dc.readMatchingIndex(dc_file+"matchID.csv") # 共通アイテム表の読み込み

        # MovieLensとEachMovieの全ユーザデータ読み込み
        # self.movieLensUserData
        # self.eachMovieUserData
        dc.readUserData()

        # MLの全ユーザの評価回数を返す
        # getUserCountML()
        # MLとEMのマッチングIDと回数をタプル((EMID,MLID),(EMcount,MLcount))で返す
        # getMatchCountEMtoML()

        # dc.readCountUserData()   # MovieLensとEachMovieの評価数読み込み
        # dc.getMatchUserData300Item()
        # dc.writeMatchUserData300Item()
        # dc.readCountUserData300()   # 共通アイテム300個のMovieLensとEachMovieの評価数読み込み
        # dc.getUserCount300()   # 共通アイテム300個のMovieLensとEachMovieの評価数読み込み

        # dc.readAuxiliaryMatrixData() # 補助評価値行列に必要なデータの読み込み
        # dc.getAuxiliaryMatrixData() # 補助評価値行列分のデータセット抽出

        # 実験１の補助評価値用csvを出力する
        getAuxiliaryMatrixDataForExp1()

        # 実験２の補助評価値行列用csvを出力する
        # dc.getAuxiliaryMatrixDataForExp2()




        """
        アイテム毎の評価数の取得
        """
        # dc.getItemCountMovieLens()
        # dc.getItemCountEachMovie()

        """
        確認用
        """
        # print(dc.matchingIndex)
        # print(dc.movieLensUserData)
        # print(dc.eachMovieUserData)
        # print(dc.countMovieLens)
        # print(dc.movieLensUserDataCount)
