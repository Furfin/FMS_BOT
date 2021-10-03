import sqlite3 as db


def add_db(tgId,group):

    con = db.connect('myDb.db')
    group = group

    cur = con.cursor()
    cur.execute(f"SELECT * FROM users")
    data = cur.fetchall()

    if data:
        msg = 'You are already in db, bastard'
        cur.close()
    else:
        cur.execute( f'INSERT INTO users VALUES ({tgId},"{group}");')
        cur.close()
        msg = 'You are added to db'

    con.commit()
    return msg
