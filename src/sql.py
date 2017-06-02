# -*- coding: utf-8 -*-

import sqlite3
import codecs

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
MovieLensのテーブル作成
UserID,ItemID,Rating,Timestamp(UNIX)
"""
def createMovieLensData():
    create_table = "create table MovieLensData (UserID int, ItemID int, Rating int, Timestamp int)"
    c.execute(create_table)
    input_path = '../data/MovieLens/u.data'
    # MovieLensのデータ読み込み
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # \t(タブ)でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [3]：Timestamp
        line_split = line.split("\t")
        insert_sql = "insert into MovieLensData (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (line_split[0],line_split[1],line_split[2], line_split[3].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1
    conn.commit()   # commit()しないと変更がかからない

"""
MovieLensのアイテムIDとタイトルのテーブル作成
ItemID, Title
"""
def createMovieLensTitle():
    create_table = "create table MovieLensTitle (ItemID int,  Title varchar(50))"
    c.execute(create_table)

    input_path = '../data/MovieLens/u.item'
    # MovieLensのデータ読み込み
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # |でスプリット
        # [0]：ItemID
        # [1]：Title
        line_split = line.split("|")
        print(line_split)
        insert_sql = "insert into MovieLensTitle (ItemID, Title) values (?, ?)"
        insert_data = (line_split[0], line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1
    conn.commit()   # commit()しないと変更がかからない


"""
EachMovieのテーブル作成
UserID,ItemID,Rating,Timestamp(Date Time)
"""
def createEachMovieData():
    create_table = "create table EachMovieData (UserID int, ItemID int, Rating int, Timestamp varchar(18))"
    c.execute(create_table)
    input_path = '../data/EachMovie/Vote.txt'
    # EachMovieのデータ読み込み
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # \t(タブ)でスプリット
        # [0]：UserID
        # [1]：ItemID
        # [2]：Rating
        # [4]：Timestamp Date/Time
        line_split = line.split("\t")
        insert_sql = "insert into EachMovieData (UserID, ItemID, Rating, Timestamp) values (?, ?, ?, ?)"
        insert_data = (line_split[0],line_split[1],line_split[2], line_split[4].rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1
    conn.commit()   # commit()しないと変更がかからない

"""
EachMovieのアイテムIDとタイトルのテーブル作成
ItemID, Title
"""
def createEachMovieTitle():
    create_table = "create table EachMovieTitle (ItemID int,  Title varchar(50))"
    c.execute(create_table)

    input_path = '../data/EachMovie/Movie.txt'
    # EachMovieのデータ読み込み
    index = 0   # インデックス用変数
    for line in codecs.open(input_path, 'r', 'utf-8'):
        # \t(タブ)でスプリット
        # [0]：ItemID
        # [1]：Title
        line_split = line.split("\t")
        insert_sql = "insert into EachMovieTitle (ItemID, Title) values (?, ?)"
        insert_data = (line_split[0], line_split[1])
        c.execute(insert_sql, insert_data)
        index = index + 1
    conn.commit()   # commit()しないと変更がかからない


"""
EachMovieTitleをMovieLensと部分一致させて，比較結果をテーブルに格納
matchTable
[0]:EachMovie ItemID
[1]:MovieLens ItemID
"""
def compareTitle():
    create_table = "create table MatchID (EM_ItemID int, ML_ItemID int)"
    c.execute(create_table)

    c.execute(u"select * from EachMovieTitle")
    c2 = conn.cursor()
    c3 = conn.cursor()
    for row1 in c: # rowはtuple
        for row2 in c2.execute("select * from MovieLensTitle where Title like \""+row1[1]+"%\""):
            insert_sql = "insert into MatchID (EM_ItemID, ML_ItemID) values (?, ?)"
            insert_data = (row1[0], row2[0])
            c3.execute(insert_sql, insert_data)

    conn.commit()

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



"""
MovieLensの上位500人分のユーザデータの対応表
[0]:IndexID
[1]:UserID
"""
def createMovieLensUser500():
    create_table = "create table MovieLensUser500 (IndexID int, UserID int)"
    c.execute(create_table)

    input_path = '../data/exp1/movieLensUser500.csv'
    # MovieLensのデータ読み込み
    index = 0

    for line in codecs.open(input_path, 'r', 'utf-8'):
        insert_sql = "insert into MovieLensUser500 (IndexID, UserID) values (?, ?)"
        insert_data = (index,line.rstrip("\n"))
        c.execute(insert_sql, insert_data)
        index = index + 1

    conn.commit()   # commit()しないと変更がかからない

"""
共通アイテムの上位300のMovieLensアイテムIDの対応表
[0]:IndexID
[1]:ItemID
"""
def createMovieLensItem300():
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

    conn.commit()   # commit()しないと変更がかからない



"""
メイン関数
"""
if __name__ == "__main__":
    connectDB("database.db")    # DB接続
    # 削除用
    # deleteTable("MovieLensData")
    # createMovieLensData() # MovieLensData

    # deleteTable("MovieLensTitle")
    # createMovieLensTitle() # MovieLensTitle

    # deleteTable("EachMovieData")
    # createEachMovieData() # EachMovieData

    # deleteTable("EachMovieTitle")
    # createEachMovieTitle()    # EachMovieTitle

    # deleteTable("MatchID")
    # compareTitle()  # MatchID

    # deleteTable("MovieLensData_Item300")
    # createMovieLensData_Item300() MovieLensData_Item300

    # deleteTable("MovieLensUser500")
    # createMovieLensUser500()

    # deleteTable("MovieLensItem300")
    # createMovieLensItem300()




    # 確認用
    i = 0   # ループ用変数
    output_path = "../data/exp1/ML_UserData_500x300.csv"
    # select_sql = 'select * from MovieLensData_Item300 inner join MovieLensUser500 on MovieLensData_Item300.UserID = MovieLensUser500.UserID'  # 2個結合
    select_sql = 'select * from (MovieLensData_Item300 inner join MovieLensUser500 on MovieLensData_Item300.UserID = MovieLensUser500.UserID) inner join MovieLensItem300 on MovieLensData_Item300.ItemID = MovieLensItem300.ItemID'    # 3個結合
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



    conn.close()
