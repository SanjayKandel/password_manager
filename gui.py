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
        tk.Label(master=frame, text='*' * 10, fg='black', bg='snow').pack(side=tk.LEFT, anchor=tk.SW)
        tk.Button(master=frame, text='Copy password', fg='snow', bg='green', command=copy_password).pack(side=tk.LEFT,
                                                                                                         anchor=tk.SE)
        frame.pack(side=tk.LEFT, anchor=tk.NW)

    def set_website_and_password(self, website: str, password: str):
        self.website_name_label['text'] = website
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


mainloop = root.mainloop
