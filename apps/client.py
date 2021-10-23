import bcrypt
import sys
import getpass
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console

sys.path.append('../')

from model import sql_connection, Insert, delete, Show, update
from pass_generator import generate_password, encrypt, decrypt

def display_table(master_key, data):
    table = Table(title="Your details")
    table.add_column("Id", justify="right", style="red", no_wrap=True)
    table.add_column("Username", style="cyan",)
    table.add_column("Website", style="magenta")
    table.add_column("Password", justify="right", style="green")
    for row in data:
        table.add_row(str(row[0]), row[1], row[2], decrypt(master_key, row[3]))
    return table


def main():
    print("1. Generate New Password \n2. Show My Saved Passwords\n3. Delete a saved password\n4. Update a password\n")
    a = Prompt.ask("Enter Your Choice", choices=["1", "2", "3", "4"])
    conn = sql_connection()
    cur = conn.cursor()

    if a == "1":
        global master_key
        master_key = getpass.getpass("Enter your master-key: ")
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]

        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            username = input("Enter Username: ")
            site = input("Enter Website: ")
            passw = generate_password()  # random generated password
            temp = encrypt(master_key, passw)
            items = (username, site, temp)
            rprint("[bold cyan]"+"Your Password is : "+passw.decode())
            print("ADDING TO DATABASE")
            Insert(conn, items)  # adding element to db
            rprint("[bold red]Done! Please Copy your password")
        else:
            rprint("[bold red]Enter Valid Password!")

    elif a == "2":
        master_key = getpass.getpass("Enter your master-key: ")
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            data = Show(master_key, conn)
            table = display_table(master_key, data)
            console = Console()
            console.print(table)
        else:
            rprint("[bold red]Enter Valid Password!")
    elif a == "3":
        master_key = getpass.getpass("Enter your master-key: ")
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            Show(master_key, conn)
            pass_id = int(input("Enter the id of the password to delete: "))
            delete(master_key, conn, pass_id)
        else:
            rprint("[bold red]Enter Valid Password!")
    elif a == '4':
        master_key = getpass.getpass("Enter your master-key: ")
        cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
        hashed = cur.fetchone()[0]
        if bcrypt.checkpw(master_key.encode(), hashed.encode()):
            pass_id = int(input("Enter the id of the password to update: "))
            passw = generate_password()  # random generated password

            update(master_key, conn, pass_id, passw)
        else:
            rprint("[bold red]Enter Valid Password!")
    else:
        print("Enter valid choice")

    exit = input('Want to stay on the application?(y/n) ')
    if exit == 'y':
        main()
    else:
        conn.close()
        sys.exit()


if __name__ == '__main__':
    main()
