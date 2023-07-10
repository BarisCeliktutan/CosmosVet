from sqlite3 import *


def db(query, do):
    database = connect('my.db')
    database.row_factory = Row
    cur = database.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    if do == "fetch":
        database.close()
        return [dict(row) for row in rows]
    elif do == "commit":
        database.commit()
        database.close()


def select():
    db = connect('my.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM mytable')
    print(cur.fetchall())
    cur.close()


def insert():
    db = connect('my.db')
    cur = db.cursor()
    cur.execute('INSERT INTO mytable(id) VALUES(1)')
    db.commit()
    cur.close()

# db('CREATE TABLE pets (ID INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text, DOB date not null)', "commit")

# db("INSERT INTO pets (username, password, DOB) VALUES ('b', '1', '2022-12-13')", "commit")


print(db("SELECT * FROM pets", "fetch"))
