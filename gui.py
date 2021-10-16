import tkinter as tk
from pyperclip import copy

# Creating window
root = tk.Tk()
root.wm_title('Password manager')
root.resizable(False, False)


# The widgets
class saved_passwords_display:
    def __init__(self):
        frame = tk.Frame(master=root)
        self.listbox = tk.Listbox(master=frame)
        self.listbox.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(master=frame)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        frame.pack(side=tk.LEFT, anchor=tk.NW)

    def set_websites(self, websites: list):
        for website in websites:
            self.listbox.insert(tk.END, website)

    def on_website_select(self, command):
        def event_handler(event):
            curselection = event.widget.curselection()
            if curselection:
                curselection = int(curselection[0])
            else:
                curselection = 0
            command(event.widget.get(curselection))

        self.listbox.bind('<<ListboxSelect>>', event_handler)


class password_viewer:
    def __init__(self):
        frame = tk.Frame(master=root)
        self.password = None

        def copy_password():
            if self.password:
                copy(self.password)

        self.website_name_label = tk.Label(master=frame, text='', bg='snow', fg='black')
        self.username_label = tk.Label(master=frame, text='', bg='snow', fg='black')
        self.website_name_label.grid(row=0, column=0)
        self.username_label.grid(row=0, column=1)
        tk.Label(master=frame, text='*' * 10, fg='black', bg='snow').grid(row=1, column=0)
        tk.Button(master=frame, text='Copy password', fg='snow', bg='green', command=copy_password).grid(row=1,
                                                                                                         column=1)
        frame.pack(side=tk.LEFT, anchor=tk.NW)

    def set_website_username_and_password(self, website: str, username: str, password: str):
        self.website_name_label['text'] = f'Website: {website}'
        self.username_label['text'] = f'Username: {username}'
        self.password = password


class new_password_window:
    def __init__(self, command):
        window = tk.Tk()
        window.resizable(False, False)
        form_frame = tk.Frame(master=window)
        tk.Label(master=form_frame, text='Website: ', bg='snow', fg='black').grid(row=0, column=0)
        tk.Label(master=form_frame, text='Username: ', bg='snow', fg='black').grid(row=1, column=0)
        tk.Label(master=form_frame, text='Password: ', bg='snow', fg='black').grid(row=2, column=0)
        website_entry = tk.Entry(master=form_frame)
        website_entry.grid(row=0, column=1)
        username_entry = tk.Entry(master=form_frame)
        username_entry.grid(row=1, column=1)
        password_entry = tk.Entry(master=form_frame, show='*')
        password_entry.grid(row=2, column=1)
        form_frame.pack()

        def save():
            command(website=website_entry.get(), username=username_entry.get(), password=password_entry.get())

        tk.Button(master=window, text='Save', command=save).pack()
        window.mainloop()


websites_and_usernames_display = saved_passwords_display()
set_websites = websites_and_usernames_display.set_websites
on_website_select = websites_and_usernames_display.on_website_select
pass_viewer = None


def set_website_username_and_password(website: str, username: str, password: str):
    global pass_viewer
    if not pass_viewer:
        pass_viewer = password_viewer()
    pass_viewer.set_website_username_and_password(website, username, password)


def set_add_password_command(command):
    def button_command():
        new_password_window(command)

    tk.Button(master=root, text='Add a new password', command=button_command).pack(side=tk.LEFT, anchor=tk.SE)


mainloop = root.mainloop
