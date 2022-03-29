from tkinter import *
from tkinter import messagebox
import password_generator
import pyperclip

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 200
TIMES_FONT = ("Times New Roman", 12, "normal")

saved_username = "i_still_use_aol@aol.com"

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
    formatted_data = f"{website} | {username} | {password}\n"
    return formatted_data


def add_entries_to_file():
    data = format_entries()
    with open("data.txt", "a") as file:
        file.write(data)


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

site_entry = Entry(width=50)
site_entry.grid(column=1, row=1, columnspan=2)

user_name_entry = Entry(width=50)
user_name_entry.grid(column=1, row=2, columnspan=2)
user_name_entry.insert(END, saved_username)

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

gen_password_button = Button(text="Get Password", command=create_new_password)
gen_password_button.grid(column=2, row=3)

save_password_button = Button(text="Save Password", width=43, overrelief="solid", command=handle_msgbox_input)
save_password_button.grid(column=1, row=4, columnspan=2)



window.mainloop()
