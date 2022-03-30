from tkinter import *
from tkinter import messagebox
import password_generator
import pyperclip
import json
import os

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 200
TIMES_FONT = ("Times New Roman", 12, "normal")
saved_username = "furby2000@aol.com"

def check_if_empty():
    return os.stat("data.json").st_size == 0

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def create_new_password():
    new_password = password_generator.generate_password()
    pyperclip.copy(new_password)
    insert_password = messagebox.askyesno(title="Insert New Password",
                                          message="A new password has been copied to the clipboard.\n"
                                                  "Paste new password?")
    if insert_password:
        password_entry.delete(0, END)
        password_entry.insert(0, pyperclip.paste())


# ---------------------------- SAVE PASSWORD ------------------------------- #
def format_entries():
    website = site_entry.get()
    username = user_name_entry.get()
    password = password_entry.get()
    formatted_data = {
        website: {
            'email': username,
            'password': password
        }
    }
    return formatted_data


def add_entries_to_file():
    json_data = format_entries()
    try:
        with open("data.json", "r") as file:
            if check_if_empty():
                raise FileNotFoundError
            file_data = json.load(file)

    except FileNotFoundError:
        with open("data.json", "w") as file:
            json.dump(json_data, file, indent=4)

    else:
        file_data.update(json_data)
        with open("data.json", "w") as file:
            json.dump(file_data, file, indent=4)

# --------------------------- FIND JSON DATA ------------------------ #
def search_for_existing_password():
    website = site_entry.get()
    if len(website) > 0 and not check_if_empty(): # check to see if file is created AND blank
        try:
            with open("data.json", "r") as file:
                contents = json.load(file)
        except FileNotFoundError:
            messagebox.showerror(title="File Not Found", message="Can not find data file.")
        else:
            if website in contents:
                email = contents[website]["email"]
                password = contents[website]["password"]
                messagebox.showinfo(title=f"{website.title()} Password", message=f"The password for {website} "
                                                                                 f"is {password}")
                password_entry.insert(0, password)
            else:
                messagebox.showerror(title="Password Not Found", message=f"No matching password found for {website}")
    else:
        messagebox.showerror(title="Error", message="Not enough information given.")

# ---------------------------- UI SETUP ------------------------------- #
def delete_entry_text():
    site_entry.delete(0, END)
    password_entry.delete(0, END)


def handle_msgbox_input():
    password = password_entry.get()
    title = site_entry.get()
    if len(password) > 0 and len(title) > 0:
        should_save = messagebox.askokcancel(title=title, message="Save information?")
        if should_save:
            add_entries_to_file()
            delete_entry_text()
    else:
        messagebox.showerror(title="Unexpected Entry", message="Please make sure to fill each entry.")


window = Tk()
window.title("Password Manager App")
window.config(padx=50, pady=50)

logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.create_image(int(CANVAS_WIDTH / 2), int(CANVAS_HEIGHT / 2), image=logo_img)
canvas.grid(column=1, row=0)

site_label = Label(text="Website:", font=TIMES_FONT)
site_label.grid(column=0, row=1, sticky="e")

user_name_label = Label(text="E-Mail/Username:", font=TIMES_FONT)
user_name_label.grid(column=0, row=2, sticky="e")

password_label = Label(text="Password:", font=TIMES_FONT)
password_label.grid(column=0, row=3, sticky="e")

site_entry = Entry(width=38)
site_entry.grid(column=1, row=1, sticky="w")

user_name_entry = Entry(width=52)
user_name_entry.grid(column=1, row=2, columnspan=2, sticky="w")
user_name_entry.insert(END, saved_username)

password_entry = Entry(width=38)
password_entry.grid(column=1, row=3, sticky="w")

gen_password_button = Button(text="Get Password", width=10, command=create_new_password)
gen_password_button.grid(column=2, row=3, padx=5)

save_password_button = Button(text="Save Password", width=44, overrelief="solid", command=handle_msgbox_input)
save_password_button.grid(column=1, row=4, columnspan=2, pady=4, sticky="w")


search_button = Button(text="Search", width=10, command=search_for_existing_password)
search_button.grid(column=2, row=1, padx=5)


window.mainloop()
