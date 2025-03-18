import tkinter as tk
from ttkbootstrap import *
from tkinter import messagebox
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def register():
    name = entry_name.get()
    forename = entry_forename.get()
    password = entry_password.get()
    email = entry_email.get()

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password= DATABASE_PASSWORD,
        database="budget_buddy"
    )
    cursor = db.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    account = cursor.fetchone()
    if account:
        messagebox.showerror("Error", "Account already exists!")
    elif not name or not forename or not password or not email:
        messagebox.showerror("Error", "Please fill out the form!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO user (name, forename, email, password) VALUES (%s, %s, %s, %s)", (name, forename, email, password))
        db.commit()
        messagebox.showinfo("Success", "You have successfully registered!")

# Initialize the Tkinter and ttkbootstrap style
root = tk.Tk()
style = Style(theme="superhero")
root.title("Registration Form")

# Create the form fields
label_name = tk.Label(root, text="name:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_forename = tk.Label(root, text="forename:")
label_forename.pack()
entry_forename = tk.Entry(root)
entry_forename.pack()

label_email = tk.Label(root, text="email:")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()



# Create the register button
register_button = tk.Button(root, text="register", command=register)
register_button.pack()

root.mainloop()