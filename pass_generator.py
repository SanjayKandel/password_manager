import random, bcrypt, sqlite3, base64
from sqlite3 import Error
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import gui


def display_table(master_key, data):
    for row in data:
        gui.add_row(str(row[0]), row[1], row[2], decrypt(master_key, row[3]))


def generate_password():
    choices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()/\~`[]"
    rand_password = [random.choice(choices) for i in range(25)]
    rand_password = "".join(rand_password)
    return rand_password.encode()


def sql_connection():
    try:
        conn = sqlite3.connect('main.db')
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
    except Error:
        print(Error)
    finally:
        conn.close()

    # unhashed_passw= a.encode('utf-8')
    # hashed_passw = bcrypt.hashpw(unhashed_passw,bcrypt.gensalt())


def Show(master_key, conn):
    try:
        cur = conn.cursor()
        data = cur.execute("SELECT * from PERSONAL WHERE ID>1")
        display_table(master_key, data)
    except Error:
        print(Error)
    finally:
        conn.close()


def encrypt(master_key, user_password):
    # we will get this main pass form data base
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    encrypted = f.encrypt(user_password)
    return encrypted


def decrypt(master_key, encrypted_pass):
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_pass)
    return decrypted.decode()


def main():
    master_key = gui.get_master_password()

    def refresh_saved_passwords():
        conn = sql_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            Show(master_key, conn)
        else:
            gui.show_wrong_master_password_error()

    def add_new_password(website: str, username: str, password: str):
        conn = sql_connection()
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if not password:
            password = generate_password()

        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            temp = encrypt(master_key, password.encode())
            items = (username, website, temp)
            Insert(conn, items)  # adding element to db
            refresh_saved_passwords()
        else:
            gui.show_wrong_master_password_error()

    if master_key:
        refresh_saved_passwords()
        gui.set_add_password_command(add_new_password)
        gui.mainloop()


if __name__ == '__main__':
    main()
