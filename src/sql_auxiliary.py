# -*- coding: utf-8 -*-
# 補助評価値行列求める

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
MovieLensの補助評価値行列用の500x100のデータセット作成
"""
def createAuxiliaryML500x100():
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

    # 共通アイテム100でフィルタリング
    # アイテムIDの対応表
    #[0]IndexID
    #[1]ItemID
    deleteTable("MovieLensItem100")
    create_table = "create table MovieLensItem100 (IndexID int, ItemID int)"
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
        insert_sql = "insert into MovieLensItem100 (IndexID, ItemID) values (?, ?)"
        insert_data = (index, line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得
    # [0]:UserID
    # [1]:RatingCount
    deleteTable("ML_UserCount_Item100")
    create_table = "create table ML_UserCount_Item100 (UserID int, RatingCount int)"
    c.execute(create_table)

    sql = "select MovieLensData.UserID, count(MovieLensData.UserID) from MovieLensData inner join MatchIdTop100 on MovieLensData.ItemID = MatchIdTop100.ML_ItemID group by MovieLensData.UserID;"
    c1 = conn.cursor()

    # 上位100アイテムへのユーザ毎の評価回数をテーブルに格納
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_UserCount_Item100 (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0], row[1])
        c1.execute(insert_sql, insert_data)

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得(上位500人)のID振り替え
    # [0]:IndexID
    # [1]:UserID
    deleteTable("ML_Item100_User500")
    create_table = "create table ML_Item100_User500 (IndexID int, UserID int)"
    c.execute(create_table)

    sql = "select * from ML_UserCount_Item100 order by RatingCount desc;"
    c1 = conn.cursor()
    count = 0
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_Item100_User500 (IndexID, UserID) values (?, ?)"
        insert_data = (count, row[0])
        c1.execute(insert_sql, insert_data)
        count = count + 1
        if count == 500:    # 上位500人分
            break

    # 補助評価値行列500x100用のデータセットを得る
    i = 0   # ループ用変数
    output_path = "../data/exp1/auxiliary/ML_Auxiliary_500x100.csv"
    select_sql = 'select * from (MovieLensData inner join ML_Item100_User500 on MovieLensData.UserID = ML_Item100_User500.UserID) inner join MovieLensItem100 on MovieLensData.ItemID = MovieLensItem100.ItemID'    # 3個結合

    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    conn.commit()   # commit()しないと変更がかからない



"""
MovieLensの補助評価値行列用の500x150のデータセット作成
"""
def createAuxiliaryML500x150():
    deleteTable("MatchIdTop150")
    create_table = "create table MatchIdTop150 (EM_ItemID int, ML_ItemID int, EM_Count int, ML_Count int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop150.csv'
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
        insert_sql = "insert into MatchIdTop150 (EM_ItemID, ML_ItemID, EM_Count, ML_Count) values (?, ?, ?, ?)"
        insert_data = (line_split[0], line_split[1], line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1

    # 共通アイテム100でフィルタリング
    # アイテムIDの対応表
    #[0]IndexID
    #[1]ItemID
    deleteTable("MovieLensItem150")
    create_table = "create table MovieLensItem150 (IndexID int, ItemID int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop150.csv'
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
        insert_sql = "insert into MovieLensItem150 (IndexID, ItemID) values (?, ?)"
        insert_data = (index, line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得
    # [0]:UserID
    # [1]:RatingCount
    deleteTable("ML_UserCount_Item150")
    create_table = "create table ML_UserCount_Item150 (UserID int, RatingCount int)"
    c.execute(create_table)

    sql = "select MovieLensData.UserID, count(MovieLensData.UserID) from MovieLensData inner join MatchIdTop150 on MovieLensData.ItemID = MatchIdTop150.ML_ItemID group by MovieLensData.UserID;"
    c1 = conn.cursor()

    # 上位100アイテムへのユーザ毎の評価回数をテーブルに格納
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_UserCount_Item150 (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0], row[1])
        c1.execute(insert_sql, insert_data)

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得(上位500人)のID振り替え
    # [0]:IndexID
    # [1]:UserID
    deleteTable("ML_Item100_User500")
    create_table = "create table ML_Item150_User500 (IndexID int, UserID int)"
    c.execute(create_table)

    sql = "select * from ML_UserCount_Item150 order by RatingCount desc;"
    c1 = conn.cursor()
    count = 0
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_Item150_User500 (IndexID, UserID) values (?, ?)"
        insert_data = (count, row[0])
        c1.execute(insert_sql, insert_data)
        count = count + 1
        if count == 500:    # 上位500人分
            break

    # 補助評価値行列500x100用のデータセットを得る
    i = 0   # ループ用変数
    output_path = "../data/exp1/auxiliary/ML_Auxiliary_500x150.csv"
    select_sql = 'select * from (MovieLensData inner join ML_Item150_User500 on MovieLensData.UserID = ML_Item150_User500.UserID) inner join MovieLensItem150 on MovieLensData.ItemID = MovieLensItem150.ItemID'    # 3個結合

    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    conn.commit()   # commit()しないと変更がかからない


"""
MovieLensの補助評価値行列用の500x200のデータセット作成
"""
def createAuxiliaryML500x200():
    deleteTable("MatchIdTop200")
    create_table = "create table MatchIdTop200 (EM_ItemID int, ML_ItemID int, EM_Count int, ML_Count int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop200.csv'
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
        insert_sql = "insert into MatchIdTop200 (EM_ItemID, ML_ItemID, EM_Count, ML_Count) values (?, ?, ?, ?)"
        insert_data = (line_split[0], line_split[1], line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1

    # 共通アイテム100でフィルタリング
    # アイテムIDの対応表
    #[0]IndexID
    #[1]ItemID
    deleteTable("MovieLensItem200")
    create_table = "create table MovieLensItem200 (IndexID int, ItemID int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop200.csv'
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
        insert_sql = "insert into MovieLensItem200 (IndexID, ItemID) values (?, ?)"
        insert_data = (index, line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1

    # MovieLensにおける共通アイテムの上位200のアイテムに対するユーザ毎の評価回数の取得
    # [0]:UserID
    # [1]:RatingCount
    deleteTable("ML_UserCount_Item200")
    create_table = "create table ML_UserCount_Item200 (UserID int, RatingCount int)"
    c.execute(create_table)

    sql = "select MovieLensData.UserID, count(MovieLensData.UserID) from MovieLensData inner join MatchIdTop200 on MovieLensData.ItemID = MatchIdTop200.ML_ItemID group by MovieLensData.UserID;"
    c1 = conn.cursor()

    # 上位100アイテムへのユーザ毎の評価回数をテーブルに格納
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_UserCount_Item200 (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0], row[1])
        c1.execute(insert_sql, insert_data)

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得(上位500人)のID振り替え
    # [0]:IndexID
    # [1]:UserID
    deleteTable("ML_Item200_User500")
    create_table = "create table ML_Item200_User500 (IndexID int, UserID int)"
    c.execute(create_table)

    sql = "select * from ML_UserCount_Item200 order by RatingCount desc;"
    c1 = conn.cursor()
    count = 0
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_Item200_User500 (IndexID, UserID) values (?, ?)"
        insert_data = (count, row[0])
        c1.execute(insert_sql, insert_data)
        count = count + 1
        if count == 500:    # 上位500人分
            break

    # 補助評価値行列500x100用のデータセットを得る
    i = 0   # ループ用変数
    output_path = "../data/exp1/auxiliary/ML_Auxiliary_500x200.csv"
    select_sql = 'select * from (MovieLensData inner join ML_Item200_User500 on MovieLensData.UserID = ML_Item200_User500.UserID) inner join MovieLensItem200 on MovieLensData.ItemID = MovieLensItem200.ItemID'    # 3個結合

    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    conn.commit()   # commit()しないと変更がかからない


"""
MovieLensの補助評価値行列用の500x300のデータセット作成
"""
def createAuxiliaryML500x300():
    deleteTable("MatchIdTop300")
    create_table = "create table MatchIdTop300 (EM_ItemID int, ML_ItemID int, EM_Count int, ML_Count int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop300.csv'
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
        insert_sql = "insert into MatchIdTop300 (EM_ItemID, ML_ItemID, EM_Count, ML_Count) values (?, ?, ?, ?)"
        insert_data = (line_split[0], line_split[1], line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1

    # 共通アイテム100でフィルタリング
    # アイテムIDの対応表
    #[0]IndexID
    #[1]ItemID
    deleteTable("MovieLensItem300")
    create_table = "create table MovieLensItem300 (IndexID int, ItemID int)"
    c.execute(create_table)

    input_path = '../data/exp1/matchIdTop300.csv'
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
        insert_sql = "insert into MovieLensItem300 (IndexID, ItemID) values (?, ?)"
        insert_data = (index, line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得
    # [0]:UserID
    # [1]:RatingCount
    deleteTable("ML_UserCount_Item300")
    create_table = "create table ML_UserCount_Item300 (UserID int, RatingCount int)"
    c.execute(create_table)

    sql = "select MovieLensData.UserID, count(MovieLensData.UserID) from MovieLensData inner join MatchIdTop300 on MovieLensData.ItemID = MatchIdTop300.ML_ItemID group by MovieLensData.UserID;"
    c1 = conn.cursor()

    # 上位100アイテムへのユーザ毎の評価回数をテーブルに格納
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_UserCount_Item300 (UserID, RatingCount) values (?, ?)"
        insert_data = (row[0], row[1])
        c1.execute(insert_sql, insert_data)

    # MovieLensにおける共通アイテムの上位100のアイテムに対するユーザ毎の評価回数の取得(上位500人)のID振り替え
    # [0]:IndexID
    # [1]:UserID
    deleteTable("ML_Item300_User500")
    create_table = "create table ML_Item300_User500 (IndexID int, UserID int)"
    c.execute(create_table)

    sql = "select * from ML_UserCount_Item300 order by RatingCount desc;"
    c1 = conn.cursor()
    count = 0
    for row in c.execute(sql):
        # [0]：MovieLens UserID
        # [1]：RatingCount
        insert_sql = "insert into ML_Item300_User500 (IndexID, UserID) values (?, ?)"
        insert_data = (count, row[0])
        c1.execute(insert_sql, insert_data)
        count = count + 1
        if count == 500:    # 上位500人分
            break

    # 補助評価値行列500x100用のデータセットを得る
    i = 0   # ループ用変数
    output_path = "../data/exp1/auxiliary/ML_Auxiliary_500x300.csv"
    select_sql = 'select * from (MovieLensData inner join ML_Item300_User500 on MovieLensData.UserID = ML_Item300_User500.UserID) inner join MovieLensItem300 on MovieLensData.ItemID = MovieLensItem300.ItemID'    # 3個結合

    for row in c.execute(select_sql):
        # print(row)
        out_data = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+","+str(row[7])
        if(i == 0): # 1行目書き込み
            f = open(output_path, "w")
            i += 1
            print(out_data, end="\n", file=f)
        else:       # 2行目以降の追記
            f = open(output_path, "a")
            print(out_data, end="\n", file=f)

    conn.commit()   # commit()しないと変更がかからない

"""
メイン関数
"""
if __name__ == "__main__":
    connectDB("database.db")    # DB接続

    # 補助評価値行列用データセット出力
    # createAuxiliaryML500x300()
    # createAuxiliaryML500x200()
    # createAuxiliaryML500x100()
    createAuxiliaryML500x150()
