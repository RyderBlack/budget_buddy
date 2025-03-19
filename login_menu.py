import tkinter as tk
from ttkbootstrap import *
from tkinter import messagebox
import mysql.connector
from dotenv import load_dotenv
import os
from passlib.hash import bcrypt
import re

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def login():
    email = entry_email.get()
    password = entry_password.get()

    
    if not email or not password:
        messagebox.showerror("Error", "Please fill out the form!")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DATABASE_PASSWORD,
        database="budget_buddy"
    )
    cursor = db.cursor()

    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    account = cursor.fetchone()
    
    if account:
        stored_hashed_password = account[4]
        if bcrypt.verify(password, stored_hashed_password):
            messagebox.showinfo("Success", "You have successfully logged in!")
        else:
            messagebox.showerror("Error", "Invalid password!")
    else:
        messagebox.showerror("Error", "Account not found!")

root = tk.Tk()
style = Style(theme="superhero")
root.title("Login Form")

label_email = tk.Label(root, text="Email:")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

root.mainloop()
