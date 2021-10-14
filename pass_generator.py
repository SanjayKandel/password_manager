import random,bcrypt,sqlite3,os,base64,getpass
from sqlite3 import Error
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt

def display_table(master_key,data):
    table = Table(title="Your details")
    table.add_column("Id", justify="right", style="red", no_wrap=True)
    table.add_column("Username", style="cyan",)
    table.add_column("Website",style="magenta")
    table.add_column("Password",justify="right",style="green")
    for row in data:
           table.add_row(str(row[0]),row[1],row[2],decrypt(master_key,row[3]))
    return table

def generate_password():
    choices= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()/\~`[]"
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
            ''' , a)
    except Error:
        print(Error)
    finally:
        conn.close()

    # unhashed_passw= a.encode('utf-8') 
    # hashed_passw = bcrypt.hashpw(unhashed_passw,bcrypt.gensalt())
def Show(master_key,conn):
    try:
        cur = conn.cursor()
        data = cur.execute("SELECT * from PERSONAL WHERE ID>1")
        table=display_table(master_key,data)
        console = Console()
        console.print(table)
    except Error:
        print(Error)
    finally:
        conn.close()

def encrypt(master_key,user_password):
    #we will get this main pass form data base
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,salt=salt,iterations=100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f= Fernet(key)
    encrypted = f.encrypt(user_password)
    return encrypted

def decrypt(master_key,encrypted_pass):
    salt = b'\xd0O\xb3\xeb\xa7\x87\x8dg!\x93\xf7\\\xd5\xb0\x15\xd6'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,salt=salt,iterations=100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f= Fernet(key)
    decrypted = f.decrypt(encrypted_pass)
    return decrypted.decode()

def main():
    print("1. Generate New Password \n2. Show My Saved Passwords")
    a = Prompt.ask("Enter Your Choice", choices=["1","2"])

    if a=="1":
        global master_key
        master_key = getpass.getpass("Enter your master-key: ")
        conn = sql_connection()
        cur= conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed=cur.fetchone()[0]
        
        if bcrypt.checkpw(master_key.encode(),hashed.encode()):
            username = input("Enter Username: ")
            site = input("Enter Website: ")
            passw = generate_password() #random generated password
            temp = encrypt(master_key,passw)
            items = (username,site,temp)
            rprint("[bold cyan]"+"Your Password is : "+passw.decode())
            print("ADDING TO DATABASE")
            Insert(conn, items) #adding element to db
            rprint("[bold red]Done! Please Copy your password")
        else :
            rprint("[bold red]Enter Valid Password!")
        
    elif a=="2":
        master_key = getpass.getpass("Enter your master-key: ")
        conn =sql_connection()
        cur= conn.cursor()
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed=cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(),hashed.encode()):
            Show(master_key,conn)
        else:
             rprint("[bold red]Enter Valid Password!")

    else:
        print("Enter valid choice")

    exit = input('Want to stay on the application?(y/n) ')
    if exit == 'y':
        main()

if __name__ == '__main__':
    main()
