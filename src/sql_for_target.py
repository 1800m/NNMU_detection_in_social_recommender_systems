# -*- coding: utf-8 -*-

import sqlite3
import codecs
import random

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
movieLensUserCountAllを読み込み，MovieLensの全UserIDと評価回数を保持
"""
def createMovieLensUserAll():
    create_table = "create table MovieLensUserAll (UserID int, RatingCount int)"
    c.execute(create_table)

    input_path = '../data/movieLensUserCountAll.csv'
    # MovieLensのデータ読み込み
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,(タブ)でスプリット
        # [0]：UserID
        # [1]：評価回数
        line_split = line.split(",")
        insert_sql = "insert into MovieLensUserAll (UserID, RatingCount) values (?, ?)"
        insert_data = (line_split[0],line_split[1].rstrip("\n"))
        c.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない

"""
MovieLensのテストセットを自動生成(x10)
アウトプット
・500ユーザ対応表
"""
def getDatasetML():
    # ユーザリストの生成
    userListAll = list()
    index = 0
    sql_select = "select UserID from MovieLensUserAll"
    for row in c.execute(sql_select):
        # print(row[0])
        userListAll.insert(index, row[0])
        index = index + 1

    # print(len(userList))  # =943

    # テストセットを10分出力
    for count in range(10):
        # 500人のリストのランダム選択
        userList500 = list()
        userListTemp = random.sample(userListAll, 500)
        # print(userList500)
        # print(len(userList500))

        # userList500[i]：リスト型
        # [0]読み替え用Index
        # [1]UserID
        for i in range(len(userListTemp)):
            userList500.insert(i, (i,userListTemp[i]))
        # print(userList500)
        # print(len(userList500))

        output_path = "../data/exp1/test_ML/user"+str(count)+".csv"
        for i in range(len(userList500)):
            out_data = str(userList500[i][0])+","+str(userList500[i][1])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

"""
テストセット毎のMovieLensのXtgtデータを出力する
MovieLensData:元の全データ
MovieLensUser500test:ユーザの読み替えID※逐次作成
MovieLensItem300:アイテムの読み替えID
"""
def getCoList_ML_Xtgt():
    for count in range(10):
        # テスト用のuserファイルを読み込んで，テーブルに格納
        sql = "create table MovieLensUser500test"+str(count)+" (IndexID int, UserID)"
        c.execute(sql)

        input_path = "../data/exp1/test_ML/user"+str(count)+".csv"
        # テストデータ読み込んでランダムに選ばれたユーザ情報をテーブルに格納
        for line in codecs.open(input_path, 'r', 'utf-8'):
            # ,(タブ)でスプリット
            # [0]：IndexID
            # [1]：UserID
            line_split = line.split(",")
            insert_sql = "insert into MovieLensUser500test"+str(count)+" (IndexID, UserID) values (?, ?)"
            insert_data = (line_split[0],line_split[1].rstrip("\n"))
            c.execute(insert_sql, insert_data)

        # 3個のテーブル結合させて，対応表を出力する
        output_path = "../data/exp1/test_ML/userData"+str(count)+".csv"
        sql = "select * from (MovieLensData inner join MovieLensUser500test"+str(count)+" on MovieLensData.UserID = MovieLensUser500test"+str(count)+".UserID) inner join MovieLensItem300 on MovieLensData.ItemID = MovieLensItem300.ItemID"    # 3個結合
        i = 0   # ループ用変数
        for row in c.execute(sql):
            # print(row)
            out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

        sql = "MovieLensUser500test"+str(count)
        deleteTable(sql)


# """
# EachMovieのデータを読み込み，全ユーザID毎の評価回数を取得する
# これ全ユーザでやっちゃったから，関係なさげ
# """
# def createEachMovieUserCountAll():
#     # ユーザの評価回数の取得
#     # sql = "select UserID, count(UserID) from EachMovieData group by UserID;"
#     # output_path = "../data/eachMovieUserCountAll.csv"
#     # i = 0
#     # for row in c.execute(sql):
#     #     # print(row[0])
#     #     out_data = str(row[0])+","+str(row[1])
#     #     if(i == 0): # 1行目書き込み
#     #         f = open(output_path, "w")
#     #         i += 1
#     #         print(out_data, end="\n", file=f)
#     #     else:       # 2行目以降の追記
#     #         f = open(output_path, "a")
#     #         print(out_data, end="\n", file=f)
#
#     # ユーザの評価回数をテーブルに格納
#     create_table = "create table EachMovieUserAll (UserID int, RatingCount int)"
#     c.execute(create_table)
#
#     input_path = '../data/eachMovieUserCountAll.csv'
#     # MovieLensのデータ読み込み
#     for line in codecs.open(input_path, 'r', 'utf-8'):
#         # ,(タブ)でスプリット
#         # [0]：UserID
#         # [1]：評価回数
#         line_split = line.split(",")
#         insert_sql = "insert into EachMovieUserAll (UserID, RatingCount) values (?, ?)"
#         insert_data = (line_split[0],line_split[1].rstrip("\n"))
#         c.execute(insert_sql, insert_data)
#
#     conn.commit()   # commit()しないと変更がかからない



"""
EachMovieのデータを読み込み，共通アイテム300を評価しているユーザデータを取得する
"""
def createEachMovieDataItem300():
    deleteTable("EachMovieDataItem300")
    # 共通アイテム数300でフィルタリングしたユーザデータを格納するテーブル
    create_table = "create table EachMovieDataItem300 (UserID int, ItemID int, Rating int, Timestamp varchar(18))"
    c.execute(create_table)

    i = 0   # ループ用変数
    output_path = "../data/exp1/EM_UserData_Item300.csv"
    select_sql = "select * from EachMovieData inner join MatchID on EachMovieData.ItemID = MatchID.EM_ItemID"    # 2個結合
    c1 = conn.cursor()

    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])
        insert_sql = "insert into EachMovieDataItem300 (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (row[0], row[1], row[2], row[3])
        c1.execute(insert_sql, insert_data)

        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    conn.commit()   # commit()しないと変更がかからない



"""
共通アイテム数300でのEachMovieのデータを読み込み，ユーザID毎の評価回数を取得する
"""
def createEachMovieUserCountItem300():
    # ユーザの評価回数をテーブルに格納
    deleteTable("EachMovieUserCountItem300")
    create_table = "create table EachMovieUserCountItem300 (UserID int, RatingCount int)"
    c.execute(create_table)
    # ユーザの評価回数の取得
    sql = "select UserID, count(UserID) from EachMovieDataItem300 group by UserID;"
    output_path = "../data/exp1/EM_UserCount_Item300.csv"
    c1 = conn.cursor()
    i = 0
    for row in c.execute(sql):
        # print(row[0])
        out_data = str(row[0])+","+str(row[1])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

        insert_sql = "insert into EachMovieUserCountItem300 (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0],row[1])
        c1.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない

"""
共通アイテム数300でのEachMovieのデータを読み込み，ユーザID毎の評価回数を取得する
"""
def createEachMovieItem300_30():
    deleteTable("EachMovieItem300_30")
    sql = "create table EachMovieItem300_30 (UserID int, RatingCount int)"
    c.execute(sql)

    c1 = conn.cursor()
    sql = "select * from EachMovieUserCountItem300 where RatingCount = \"30\";"
    for row in c.execute(sql):
        insert_sql = "insert into EachMovieItem300_30 (UserID, RatingCount) values (?, ?)"
        insert_data = row
        c1.execute(insert_sql, insert_data)

"""
EachMovieのテストセットを自動生成(x10)
アウトプット
・500ユーザ対応表
"""
def getDatasetEM():
    # ユーザリストの生成
    userListAll = list()
    index = 0
    sql_select = "select UserID from EachMovieItem300_30"   # 共通アイテム300中の30アイテムを評価しているユーザリスト(664人)
    for row in c.execute(sql_select):
        # print(row[0])
        userListAll.insert(index, row[0])
        index = index + 1

    # print(len(userList))  # =664

    # テストセットを10分出力
    for count in range(10):
        # 500人のリストのランダム選択
        userList500 = list()
        userListTemp = random.sample(userListAll, 500)
        # print(userList500)
        # print(len(userList500))

        # userList500[i]：リスト型
        # [0]読み替え用Index
        # [1]UserID
        for i in range(len(userListTemp)):
            userList500.insert(i, (i,userListTemp[i]))
        # print(userList500)
        # print(len(userList500))

        output_path = "../data/exp1/test_EM/user"+str(count)+".csv"
        for i in range(len(userList500)):
            out_data = str(userList500[i][0])+","+str(userList500[i][1])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

"""
テストセット毎のEachMovieのXtgtデータを出力する
EachMovieData:元の全データ
EachMovieUser500test:ユーザの読み替えID※逐次作成
EachMovieItem300:アイテムの読み替えID
"""
def getCoList_EM_Xtgt():
    for count in range(10):
        # テスト用のuserファイルを読み込んで，テーブルに格納
        sql = "create table EachMovieUser500test"+str(count)+" (IndexID int, UserID)"
        c.execute(sql)

        input_path = "../data/exp1/test_EM/user"+str(count)+".csv"
        # テストデータ読み込んでランダムに選ばれたユーザ情報をテーブルに格納
        for line in codecs.open(input_path, 'r', 'utf-8'):
            # ,(タブ)でスプリット
            # [0]：IndexID
            # [1]：UserID
            line_split = line.split(",")
            insert_sql = "insert into EachMovieUser500test"+str(count)+" (IndexID, UserID) values (?, ?)"
            insert_data = (line_split[0],line_split[1].rstrip("\n"))
            c.execute(insert_sql, insert_data)

        # 3個のテーブル結合させて，対応表を出力する
        output_path = "../data/exp1/test_EM/userData"+str(count)+".csv"
        sql = "select * from (EachMovieData inner join EachMovieUser500test"+str(count)+" on EachMovieData.UserID = EachMovieUser500test"+str(count)+".UserID) inner join EachMovieItem300 on EachMovieData.ItemID = EachMovieItem300.ItemID"    # 3個結合
        i = 0   # ループ用変数
        for row in c.execute(sql):
            # print(row)
            out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

        sql = "EachMovieUser500test"+str(count)
        deleteTable(sql)



"""
メイン関数
"""
if __name__ == "__main__":
    connectDB("database.db")    # DB接続

    # MovieLensの全ユーザIDのテーブル作成
    # deleteTable("MovieLensUserAll")
    # createMovieLensUserAll()

    """
    MLのテスト用データセットの生成用メソッド
    """
    # getDatasetML()
    # getCoList_ML_Xtgt()


    """
    EMのテスト用データセットの生成用メソッド
    """
    # 下準備
    # create_table = "create table EachMovieUserAll (UserID int, RatingCount int)"
    # c.execute(create_table)

    # createEachMovieDataItem300()
    # createEachMovieUserCountItem300()
    # createEachMovieItem300_30()

    # データセット出力
    getDatasetEM()
    getCoList_EM_Xtgt()



    conn.close()
