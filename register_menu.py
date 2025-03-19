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

def validate_name_forename(name_forename):
    return bool(re.match(r"^[a-zA-Zéèàêâîôûçëïöüà-ÿ\s]+$", name_forename))

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def validate_password(password):
    return bool(re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>])[A-Za-z\d!@#$%^&*(),.?\":{}|<>]{10,}$", password))

def register():
    name = entry_name.get()
    forename = entry_forename.get()
    password = entry_password.get()
    email = entry_email.get()

    # Vérifications des entrées
    if not name or not forename or not password or not email:
        messagebox.showerror("Error", "Please fill out the form!")
        return

    if not validate_name_forename(name):
        messagebox.showerror("Error", "Name contains invalid characters! Only letters and accents are allowed.")
        return

    if not validate_name_forename(forename):
        messagebox.showerror("Error", "Forename contains invalid characters! Only letters and accents are allowed.")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    if not validate_password(password):
        messagebox.showerror("Error", "Password must be at least 10 characters long, with at least one uppercase letter, one number, and one special character!")
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
        messagebox.showerror("Error", "Account already exists!")
    else:
        hashed_password = bcrypt.hash(password)
        cursor.execute("INSERT INTO user (name, forename, email, password) VALUES (%s, %s, %s, %s)", (name, forename, email, hashed_password))
        db.commit()
        messagebox.showinfo("Success", "You have successfully registered!")

root = tk.Tk()
style = Style(theme="superhero")
root.title("Registration Form")

label_name = tk.Label(root, text="Name:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_forename = tk.Label(root, text="Forename:")
label_forename.pack()
entry_forename = tk.Entry(root)
entry_forename.pack()

label_email = tk.Label(root, text="Email:")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

register_button = tk.Button(root, text="Register", command=register)
register_button.pack()

root.mainloop()
