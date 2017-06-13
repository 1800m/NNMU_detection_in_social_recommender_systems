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
MovieLensのデータを読み込み，共通アイテムを2回以上評価しているユーザデータを取得する
"""
def createMovieLensDataItem(number):
    # 共通アイテムの評価多い順
    deleteTable("MatchIdTop"+str(number))
    # [0]：EachMovieのItemID
    # [1]：MovieLensのItemID
    # [2]：EachMovieの評価回数
    # [3]：MovieLensの評価回数
    create_table = "create table MatchIdTop"+str(number)+" (EM_ItemID int, ML_ItemID int, EM_RatingCount int, ML_RatingCount)"
    c.execute(create_table)

    deleteTable("MovieLensItem"+str(number))
    create_table = "create table MovieLensItem"+str(number)+" (IndexID int, ItemID int)"
    c.execute(create_table)

    input_path = "../data/exp1/matchIdTop"+str(number)+".csv"
    index = 0
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：EachMovieのItemID
        # [1]：MovieLensのItemID
        # [2]：EachMovieの評価回数
        # [3]：MovieLensの評価回数
        line_split = line.split(",")
        insert_data = (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n"))
        insert_sql = "insert into MatchIdTop"+str(number)+" (EM_ItemID, ML_ItemID, EM_RatingCount, ML_RatingCount) values (?, ?, ?, ?)"
        c.execute(insert_sql, insert_data)

        insert_data = (index, line_split[1])
        insert_sql = "insert into MovieLensItem"+str(number)+" (IndexID, ItemID) values (?, ?)"
        c.execute(insert_sql, insert_data)
        index = index + 1


    # 共通アイテム数でフィルタリングしたユーザデータを格納するテーブル
    deleteTable("MovieLensDataItem"+str(number))
    create_table = "create table MovieLensDataItem"+str(number)+" (UserID int, ItemID int, Rating int, Timestamp varchar(18))"
    c.execute(create_table)

    select_sql = "select * from MovieLensData inner join MatchIdTop"+str(number)+" on MovieLensData.ItemID = MatchIdTop"+str(number)+".ML_ItemID"    # 2個結合
    c1 = conn.cursor()

    i = 0   # ループ用変数
    output_path = "../data/exp1/ML_UserData_Item"+str(number)+".csv"
    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])
        insert_sql = "insert into MovieLensDataItem"+str(number)+" (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (row[0], row[1], row[2], row[3])
        c1.execute(insert_sql, insert_data)

        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


    # ユーザの評価回数をテーブルに格納
    deleteTable("MovieLensUserCountItem"+str(number))
    create_table = "create table MovieLensUserCountItem"+str(number)+" (UserID int, RatingCount int)"
    c.execute(create_table)
    # ユーザの評価回数の取得
    sql = "select UserID, count(UserID) from MovieLensDataItem"+str(number)+" group by UserID;"
    output_path = "../data/exp1/ML_UserCount_Item"+str(number)+".csv"
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

        insert_sql = "insert into MovieLensUserCountItem"+str(number)+" (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0],row[1])
        c1.execute(insert_sql, insert_data)

    # 2回以上評価したユーザ
    deleteTable("MovieLensItem"+str(number)+"_2over")
    sql = "create table MovieLensItem"+str(number)+"_2over (UserID int, RatingCount int)"
    c.execute(sql)

    c1 = conn.cursor()
    sql = "select * from MovieLensUserCountItem"+str(number)+" where RatingCount > \"1\";"
    for row in c.execute(sql):
        insert_sql = "insert into MovieLensItem"+str(number)+"_2over (UserID, RatingCount) values (?, ?)"
        insert_data = row
        c1.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない



"""
テストセット毎のMovieLensのXtgtデータを出力する
MovieLensData:元の全データ
MovieLensUser500test:ユーザの読み替えID※逐次作成
MovieLensItem300:アイテムの読み替えID
"""
def getCoList_ML_Xtgt(number):
    print(number)
    # 943人から500人のユーザを選択して，IDを振り替える
    # ユーザリストの生成
    userListAll = list()
    index = 0
    # sql_select = "select UserID from MovieLensUserAll"
    sql_select = "select UserID from MovieLensItem"+str(number)+"_2over"
    for row in c.execute(sql_select):
        # print(row[0])
        # row[0]：ユーザID
        # row[1]：評価回数
        userListAll.insert(index, row[0])
        index = index + 1

    # print(len(userList))  # =943

    # テストセットを10回分出力
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

        output_path = "../data/exp1/test_ML_"+str(number)+"/user"+str(count)+".csv"
        for i in range(len(userList500)):
            out_data = str(userList500[i][0])+","+str(userList500[i][1])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    # 補助評価値行列用データセットの出力処理
    for count in range(10):
        # テスト用のuserファイルを読み込んで，テーブルに格納
        sql = "create table MovieLensUser500test"+str(count)+" (IndexID int, UserID)"
        c.execute(sql)

        input_path = "../data/exp1/test_ML_"+str(number)+"/user"+str(count)+".csv"
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
        output_path = "../data/exp1/test_ML_"+str(number)+"/userData"+str(count)+".csv"

        sql = "select * from (MovieLensData inner join MovieLensUser500test"+str(count)+" on MovieLensData.UserID = MovieLensUser500test"+str(count)+".UserID) inner join MovieLensItem"+str(number)+" on MovieLensData.ItemID = MovieLensItem"+str(number)+".ItemID"    # 3個結合
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


"""
EachMovieのデータを読み込み，共通アイテムを評価しているユーザデータを取得する
"""
def createEachMovieDataItem(number):
    # 共通アイテムの評価多い順
    deleteTable("MatchIdTop"+str(number))
    # [0]：EachMovieのItemID
    # [1]：MovieLensのItemID
    # [2]：EachMovieの評価回数
    # [3]：MovieLensの評価回数
    create_table = "create table MatchIdTop"+str(number)+" (EM_ItemID int, ML_ItemID int, EM_RatingCount int, ML_RatingCount)"
    c.execute(create_table)

    deleteTable("EachMovieItem"+str(number))
    create_table = "create table EachMovieItem"+str(number)+" (IndexID int, ItemID int)"
    c.execute(create_table)

    input_path = "../data/exp1/matchIdTop"+str(number)+".csv"
    index = 0
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,でスプリット
        # [0]：EachMovieのItemID
        # [1]：MovieLensのItemID
        # [2]：EachMovieの評価回数
        # [3]：MovieLensの評価回数
        line_split = line.split(",")
        insert_data = (line_split[0],line_split[1],line_split[2],line_split[3].rstrip("\n"))
        insert_sql = "insert into MatchIdTop"+str(number)+" (EM_ItemID, ML_ItemID, EM_RatingCount, ML_RatingCount) values (?, ?, ?, ?)"
        c.execute(insert_sql, insert_data)

        insert_data = (index, line_split[0])
        insert_sql = "insert into EachMovieItem"+str(number)+" (IndexID, ItemID) values (?, ?)"
        c.execute(insert_sql, insert_data)
        index = index + 1


    # 共通アイテム数でフィルタリングしたユーザデータを格納するテーブル
    deleteTable("EachMovieDataItem"+str(number))
    create_table = "create table EachMovieDataItem"+str(number)+" (UserID int, ItemID int, Rating int, Timestamp varchar(18))"
    c.execute(create_table)

    select_sql = "select * from EachMovieData inner join MatchIdTop"+str(number)+" on EachMovieData.ItemID = MatchIdTop"+str(number)+".EM_ItemID"    # 2個結合
    c1 = conn.cursor()

    i = 0   # ループ用変数
    output_path = "../data/exp1/EM_UserData_Item"+str(number)+".csv"
    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])
        insert_sql = "insert into EachMovieDataItem"+str(number)+" (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (row[0], row[1], row[2], row[3])
        c1.execute(insert_sql, insert_data)

        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)


    # ユーザの評価回数をテーブルに格納
    deleteTable("EachMovieUserCountItem"+str(number))
    create_table = "create table EachMovieUserCountItem"+str(number)+" (UserID int, RatingCount int)"
    c.execute(create_table)
    # ユーザの評価回数の取得
    sql = "select UserID, count(UserID) from EachMovieDataItem"+str(number)+" group by UserID;"
    output_path = "../data/exp1/EM_UserCount_Item"+str(number)+".csv"
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

        insert_sql = "insert into EachMovieUserCountItem"+str(number)+" (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0],row[1])
        c1.execute(insert_sql, insert_data)

    # 30回だけ評価したユーザ
    deleteTable("EachMovieItem"+str(number)+"_30")
    sql = "create table EachMovieItem"+str(number)+"_30 (UserID int, RatingCount int)"
    c.execute(sql)

    c1 = conn.cursor()
    sql = "select * from EachMovieUserCountItem"+str(number)+" where RatingCount = \"30\";"
    for row in c.execute(sql):
        insert_sql = "insert into EachMovieItem"+str(number)+"_30 (UserID, RatingCount) values (?, ?)"
        insert_data = row
        c1.execute(insert_sql, insert_data)

    conn.commit()   # commit()しないと変更がかからない




"""
テストセット毎のEachMovieのXtgtデータを出力する
EachMovieData:元の全データ
EachMovieUser500test:ユーザの読み替えID※逐次作成
EachMovieItem300:アイテムの読み替えID
"""
def getCoList_EM_Xtgt(number):
    print(number)
    # 共通アイテムnumberを30回評価しているユーザを出力
    # ユーザリストの生成
    userListAll = list()
    index = 0
    sql_select = "select UserID from EachMovieItem"+str(number)+"_30"   # 共通アイテム中の30アイテムを評価しているユーザリスト
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

        output_path = "../data/exp1/test_EM_"+str(number)+"/user"+str(count)+".csv"
        for i in range(len(userList500)):
            out_data = str(userList500[i][0])+","+str(userList500[i][1])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)

    # 補助評価値行列用データセットの出力処理
    for count in range(10):
        # テスト用のuserファイルを読み込んで，テーブルに格納
        sql = "create table EachMovieUser500test"+str(count)+" (IndexID int, UserID)"
        c.execute(sql)

        input_path = "../data/exp1/test_EM_"+str(number)+"/user"+str(count)+".csv"
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
        output_path = "../data/exp1/test_EM_"+str(number)+"/userData"+str(count)+".csv"
        sql = "select * from (EachMovieData inner join EachMovieUser500test"+str(count)+" on EachMovieData.UserID = EachMovieUser500test"+str(count)+".UserID) inner join EachMovieItem"+str(number)+" on EachMovieData.ItemID = EachMovieItem"+str(number)+".ItemID"    # 3個結合
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


if __name__ == "__main__":
    connectDB("database.db")    # DB接続

    deleteTable("MovieLensItem150")
    sql = "create table MovieLensItem150 (IndexID int, ItemID int)"
    c.execute(sql)
    input_path = "../data/exp1/matchIdTop150.csv"
    index = 0
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # ,(タブ)でスプリット
        # [0]：IndexID
        # [1]：UserID
        line_split = line.split(",")
        insert_sql = "insert into MovieLensItem150 (IndexID, ItemID) values (?, ?)"
        insert_data = (index, line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1

    print("MLの処理")
    createMovieLensDataItem(150)
    getCoList_ML_Xtgt(150)
    createMovieLensDataItem(200)
    getCoList_ML_Xtgt(200)
    createMovieLensDataItem(300)
    getCoList_ML_Xtgt(300)

    print("EMの処理")
    createEachMovieDataItem(150)
    getCoList_EM_Xtgt(150)
    createEachMovieDataItem(200)
    getCoList_EM_Xtgt(200)
    createEachMovieDataItem(300)
    getCoList_EM_Xtgt(300)
