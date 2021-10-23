import sqlite3
from sqlite3 import Error
from rich import print as rprint
from pass_generator import *


def sql_connection():
    try:
        conn = sqlite3.connect('../main.db')
        return conn
    except Error:
        print(Error)


def Insert(conn, a):
    try:
        cur = conn.cursor()
        with conn:
            cur.execute('''
            INSERT INTO PERSONAL (USERNAME, WEBSITE, PASSWORD) VALUES(?, ?, ?)
            ''', a)
        conn.commit()
    except Error:
        print(Error)

    # unhashed_passw= a.encode('utf-8')
    # hashed_passw = bcrypt.hashpw(unhashed_passw,bcrypt.gensalt())


def update(master_key, conn, id, passw):
    if id == 1:
        rprint("[bold red]You can't update the master key!")
        return
    try:
        cur = conn.cursor()
        with conn:
            pass_enc = encrypt(master_key, passw)
            cur.execute(
                'UPDATE PERSONAL SET PASSWORD=? WHERE ID=?', (pass_enc, id))
            print("Password Successfully Updated!")
            rprint("[bold cyan]"+"Your Password is : "+passw.decode())
            rprint("[bold red] Please Copy your password")
        conn.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))


def delete(master_key, conn, id):
    if id == 1:
        rprint("[bold red]You can't delete the master key!")
        return
    try:
        cur = conn.cursor()
        with conn:
            cur.execute('DELETE FROM PERSONAL WHERE ID = ?', (id,))
        conn.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))


def Show(master_key, conn):
    try:
        cur = conn.cursor()
        data = cur.execute("SELECT * from PERSONAL WHERE ID>1")
        return data
    except Error:
        print(Error)


def get_password_from_id(master_key, conn, id):
    data = Show(master_key, conn)
    for row in data:
        if row[0] == int(id):
            return decrypt(master_key, row[3])
