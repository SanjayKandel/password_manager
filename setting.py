import sqlite3
import bcrypt
import sys
import getpass
import os


def createDB():
    try:
        conn = sqlite3.connect('main.db')
        return conn
    except sqlite3.Error as e:
        print(type(e).__name__)


def createTB(conn):
    try:
        cur = conn.cursor()
        with conn:
            cur.execute('''CREATE TABLE PERSONAL(ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            USERNAME CHAR(50) NOT NULL, 
            WEBSITE CHAR(50) NOT NULL,
            PASSWORD CHAR(100) NOT NULL);
            ''')
    except sqlite3.Error as e:
        print(type(e).__name__)


def addMasterKey(conn, main_password):
    hashed = bcrypt.hashpw(main_password.encode('utf-8'), bcrypt.gensalt())
    temp = ('Masterkey', 'Masterkey', hashed.decode())
    try:
        cur = conn.cursor()
        with conn:
            cur.execute('''INSERT INTO PERSONAL(USERNAME, WEBSITE, PASSWORD) VALUES (?, ?, ?)
            ''', temp)
    except sqlite3.Error as e:
        print(type(e).__name__)
    finally:
        conn.close()


def setMasterKey():
    main_password = getpass.getpass("Enter Master Password: ")
    reenter = getpass.getpass("Re-Enter Master Password: ")
    if main_password == reenter:
        return main_password
    else:
        print("Re-Entered password was not the same as Master Password\nRe-Enter your Password")
        setMasterKey()


def main():
    print("It is your first time setting the database")
    a = input("Do you want to create database(y/n): ").lower()
    if a == 'y':
        if os.path.exists('main.db'):
            print("Database already exists!")
            print("If you continue then your old database will be deleted.")
            x = input("Do you want to continue?(y/n):").lower()
            if x == 'n':
                sys.exit()
            else:
                os.remove('main.db')
        print("Creating database.....")
        conn = createDB()
        print("Creating Table....")
        createTB(conn)
        print("Database Successfully created!")
        main_password = str(setMasterKey())
        addMasterKey(conn, main_password)
    else:
        print("See you Soon")
        sys.exit()


if __name__ == '__main__':
    main()
