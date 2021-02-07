import sqlite3,bcrypt,sys,getpass
from sqlite3 import Error

def createDB():
    try:
        conn = sqlite3.connect('main.db')
        return conn
    except sqlite3.Error as e:
        print(type(e).__name__)

def createTB(conn):
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE PERSONAL(ID INTEGER PRIMARY KEY AUTOINCREMENT,USERNAME CHAR(50) NOT NULL,WEBSITE CHAR(50) NOT NULL,PASSWORD CHAR(100) NOT NULL);''')
        conn.commit()
    except sqlite3.Error as e:
        print(type(e).__name__)

def addMasterKey(conn,main_password):
    hashed = bcrypt.hashpw(main_password.encode('utf-8'),bcrypt.gensalt())
    temp=('Masterkey','Masterkey',hashed.decode())
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO PERSONAL(USERNAME, WEBSITE,PASSWORD) VALUES (?,?,?)",temp)
        conn.commit()
    except sqlite3.Error as e:
        print(type(e).__name__)
    finally:
        conn.close()
    

def setMasterKey():
    main_password= getpass.getpass("Enter Master Password: ")
    reenter = getpass.getpass("Re-Enter Master Password: ")
    if main_password == reenter:
        return main_password
    else:
        print("Re-Entered password was not the same as Master Password\nRe-Enter your Password")
        setMasterKey()

def main():
    print("It is your first time setting the database")
    a = input("Do you want to create database(y/n): ")
    if(a=='y' or a=='Y'):
        print("Creating database.....")
        conn = createDB()
        print("Creating Table....")
        createTB(conn)
        print("All Done!")
        main_password = str(setMasterKey())
        addMasterKey(conn,main_password)
    else:
        sys.exit()
        print("See you Soon")

if __name__ == '__main__':
    main()
