import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror
from pyperclip import copy
from tkscrolledframe import ScrolledFrame

# Creating window
root = tk.Tk()
root.wm_title('Password manager')
root.resizable(False, False)


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
saved_passwords_viewer_frame = saved_passwords_viewer_scrolled_frame.display_widget(tk.Frame)
row = 0
already_added_rows_ids = []


def add_row(id_: str, username: str, website: str, password: str, copy_button=True, hide=True):
    global row
    already_added = False
    for already_added_row_id in already_added_rows_ids:
        if id_ == already_added_row_id:
            already_added = True
            break
    if not already_added:
        tk.Label(master=saved_passwords_viewer_frame, text=id_, fg='black', bg='snow').grid(row=row, column=0,
                                                                                            padx=2)
        tk.Label(master=saved_passwords_viewer_frame, text=username, fg='black', bg='snow').grid(row=row, column=1,
                                                                                                 padx=2)
        tk.Label(master=saved_passwords_viewer_frame, text=website, fg='black', bg='snow').grid(row=row, column=2,
                                                                                                padx=2)
        password_label = tk.Label(master=saved_passwords_viewer_frame, text='*' * 10, fg='black', bg='snow')
        password_label.grid(row=row, column=3, padx=2)
        if hide:
            show_or_hide_button = tk.Button(master=saved_passwords_viewer_frame, text='Show')
            show_or_hide_button.grid(row=row, column=4)

            def show_or_hide():
                if show_or_hide_button['text'] == 'Show':  # If shown
                    password_label['text'] = password
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

            tk.Button(master=saved_passwords_viewer_frame, text='Copy', command=copy_password).grid(row=row, column=5,
                                                                                                    padx=2)
        row += 1
        already_added_rows_ids.append(id_)


add_row('Id', 'Username', 'Website', 'Password', copy_button=False, hide=False)
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

mainloop = root.mainloop


def get_master_password():
    return askstring(title='Master password', prompt='Password: ', show='*')


def show_wrong_master_password_error():
    showerror(title='Incorrect password', message='Wrong master password')
