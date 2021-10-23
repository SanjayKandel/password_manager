import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror
from pyperclip import copy
from tkscrolledframe import ScrolledFrame
import sys
import bcrypt

sys.path.append('../')
from model import sql_connection, Insert, delete, Show, update, get_password_from_id
from pass_generator import generate_password, encrypt, decrypt

# Creating window
root = tk.Tk()
root.wm_title('Password manager')
root.resizable(False, False)


def get_weaknesses_in_password(password: str):
    result = ''
    if len(password) < 8:
        result += f'\u2022 Password contains {len(password)} characters, a minimum of 8 characters is recommended\n'
    small_letter_found = False
    cap_letter_found = False
    num_found = False
    for letter in password:
        if letter.islower():
            small_letter_found = True
            break
    for letter in password:
        if letter.isupper():
            cap_letter_found = True
            break
    for letter in password:
        if letter.isdigit():
            num_found = True
            break
    if not small_letter_found:
        result += '\u2022Password contains no small letters\n'
    if not cap_letter_found:
        result += '\u2022Password contains no capital letters\n'
    if not num_found:
        result += '\u2022Password contains no numbers'
    return result.strip('\n')


# Widgets
class Entry:
    def __init__(self, label_text, master):
        frame = tk.Frame(master=master)
        tk.Label(master=frame, text=label_text, bg='snow', fg='black').pack(side=tk.LEFT)
        entry = tk.Entry(master=frame)
        entry.pack(side=tk.RIGHT)
        self.grid = frame.grid
        self.get = entry.get


class PassEntry:
    def __init__(self, master, label_text='Password: '):
        frame = tk.Frame(master=master)
        tk.Label(master=frame, text=label_text, bg='snow', fg='black').pack(side=tk.LEFT)
        show_or_hide_password_button = tk.Button(master=frame, text='Show')
        show_or_hide_password_button.pack(side=tk.RIGHT)
        entry = tk.Entry(master=frame, show='*')
        entry.pack(side=tk.RIGHT)

        def show_or_hide_password():
            if entry['show'] == '*':  # If password is hidden
                entry['show'] = ''  # Show password
                show_or_hide_password_button['text'] = 'Hide'
            elif entry['show'] == '':  # Elif password is shown
                entry['show'] = '*'  # Hide password
                show_or_hide_password_button['text'] = 'Show'

        show_or_hide_password_button['command'] = show_or_hide_password
        self.grid = frame.grid
        self.get = entry.get


saved_passwords_viewer_scrolled_frame = ScrolledFrame()
saved_passwords_viewer_scrolled_frame.bind_scroll_wheel(root)
saved_passwords_viewer_scrolled_frame.bind_arrow_keys(root)
saved_passwords_viewer_frame = saved_passwords_viewer_scrolled_frame.display_widget(tk.Frame)
row = 0
already_added_rows_ids = []


def add_row(id_: str, username: str, website: str, password: str, master_key=None, conn=None, copy_button=True,
            edit_button=True, hide=True):
    global row
    already_added = False
    for already_added_row_id in already_added_rows_ids:
        if id_ == already_added_row_id:
            already_added = True
            break
    if not already_added:
        widgets = []
        column = 0
        widgets.append(tk.Label(master=saved_passwords_viewer_frame, text=id_, fg='black', bg='snow'))
        widgets.append(tk.Label(master=saved_passwords_viewer_frame, text=username, fg='black', bg='snow'))
        widgets.append(tk.Label(master=saved_passwords_viewer_frame, text=website, fg='black', bg='snow'))
        password_label = tk.Label(master=saved_passwords_viewer_frame, text='*' * 10, fg='black', bg='snow')
        widgets.append(password_label)
        if hide:
            show_or_hide_button = tk.Button(master=saved_passwords_viewer_frame, text='Show')
            widgets.append(show_or_hide_button)

            def show_or_hide():
                if show_or_hide_button['text'] == 'Show':  # If shown
                    password_label['text'] = get_password_from_id(master_key, conn, id_)
                    show_or_hide_button['text'] = 'Hide'
                elif show_or_hide_button['text'] == 'Hide':  # Elif Hidden
                    password_label['text'] = '*' * 10
                    show_or_hide_button['text'] = 'Show'

            show_or_hide_button['command'] = show_or_hide
        else:
            password_label['text'] = password
        if copy_button:
            def copy_password():
                copy(password)

            widgets.append(tk.Button(master=saved_passwords_viewer_frame, text='Copy', command=copy_password))
        if edit_button:
            def edit_password():
                new_password = str(askstring(title='Update password', prompt='Enter new password', show='*'))
                weaknesses_in_password = get_weaknesses_in_password(new_password)
                if new_password:
                    if weaknesses_in_password:
                        showerror('Weak password',
                                  f'Your password has the following weakness:\n{weaknesses_in_password}\nLeave the '
                                  f'password field blank if you want to auto-generate password')
                    else:
                        update(master_key, conn, id_, new_password.encode())
                        if not password_label['text'] == '*' * 10:
                            password_label['text'] = get_password_from_id(master_key, conn, id_)
                else:
                    update(master_key, conn, id_, generate_password())
                    if not password_label['text'] == '*' * 10:
                        password_label['text'] = get_password_from_id(master_key, conn, id_)
            widgets.append(tk.Button(master=saved_passwords_viewer_frame, text='Edit', command=edit_password))
        if master_key and conn:
            def delete_():
                delete(master_key, conn, id_)
                for widget_ in widgets:
                    widget_.grid_forget()

            widgets.append(tk.Button(master=saved_passwords_viewer_frame, text='Delete', fg='snow', bg='red',
                                     command=delete_))

        row += 1
        already_added_rows_ids.append(id_)
        for widget in widgets:
            widget.grid(row=row, column=column, padx=2)
            column += 1


add_row('Id', 'Username', 'Website', 'Password', copy_button=False, edit_button=False, hide=False)
saved_passwords_viewer_scrolled_frame.grid(row=0, column=0)

add_password_frame = tk.Frame(master=root)
website_entry = Entry(label_text='Website: ', master=add_password_frame)
username_entry = Entry(label_text='Username: ', master=add_password_frame)
password_entry = PassEntry(master=add_password_frame)
website_entry.grid(row=0, column=0)
username_entry.grid(row=1, column=0)
password_entry.grid(row=2, column=0)
add_password_button = tk.Button(master=add_password_frame, text='Add password!', fg='snow', bg='green')
add_password_button.grid(row=3, column=0)


def set_add_password_command(command):
    def button_command():
        command(website=website_entry.get(), username=username_entry.get(), password=password_entry.get())

    add_password_button.configure(command=button_command)


add_password_frame.grid(row=0, column=1)


def get_master_password():
    return askstring(title='Master password', prompt='Password: ', show='*')


def show_wrong_master_password_error():
    showerror(title='Incorrect password', message='Wrong master password')


def display_table(master_key, data, conn):
    for row_ in data:
        add_row(str(row_[0]), row_[1], row_[2], decrypt(master_key, row_[3]), conn=conn, master_key=master_key)


def main():
    conn = sql_connection()
    cur = conn.cursor()
    master_key = get_master_password()
    cur.execute("SELECT PASSWORD FROM PERSONAL WHERE ID=1")
    hashed = cur.fetchone()[0]
    if bcrypt.checkpw(master_key.encode(), hashed.encode()):
        def refresh_table():
            data = Show(master_key, conn)
            display_table(master_key, data, conn)

        def add_password(website: str, username: str, password: str):
            weaknesses_in_password = get_weaknesses_in_password(password)
            if password:
                if weaknesses_in_password:
                    showerror('Weak password',
                              f'Your password has the following weakness:\n{weaknesses_in_password}\nLeave the '
                              f'password field blank if you want to auto-generate password')
                else:
                    temp = encrypt(master_key, password.encode())
                    items = (username, website, temp)
                    Insert(conn, items)  # adding element to db
                    refresh_table()
            else:
                password = generate_password()
                temp = encrypt(master_key, password)
                items = (username, website, temp)
                Insert(conn, items)  # adding element to db
                refresh_table()

        set_add_password_command(add_password)
        refresh_table()
        root.mainloop()
    else:
        show_wrong_master_password_error()


if __name__ == '__main__':
    main()
