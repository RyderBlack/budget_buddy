import tkinter as tk
from ttkbootstrap import *
from tkinter import messagebox
import mysql.connector
import os
from dotenv import load_dotenv
from passlib.hash import bcrypt
import re
import subprocess  # To launch dashboard.py

# Load environment variables
load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Global variable to store logged-in user ID
logged_in_user_id = None


def validate_name_forename(name_forename):
    return bool(re.match(r"^[a-zA-Zéèàêâîôûçëïöüà-ÿ\s]+$", name_forename))


def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


def validate_password(password):
    return bool(re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>])[A-Za-z\d!@#$%^&*(),.?\":{}|<>]{10,}$", password))


def register():
    """Register a new user in the database."""
    name = entry_name.get()
    forename = entry_forename.get()
    password = entry_password.get()
    email = entry_email.get()

    if not name or not forename or not password or not email:
        messagebox.showerror("Error", "Please fill out the form!")
        return

    if not validate_name_forename(name) or not validate_name_forename(forename):
        messagebox.showerror("Error", "Name and forename must contain only letters and accents!")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    if not validate_password(password):
        messagebox.showerror("Error", "Password must be at least 10 characters long, contain an uppercase letter, a number, and a special character!")
        return

    try:
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
            cursor.execute(
                "INSERT INTO user (name, forename, email, password) VALUES (%s, %s, %s, %s)",
                (name, forename, email, hashed_password),
            )
            db.commit()
            messagebox.showinfo("Success", "You have successfully registered!")

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"MySQL Error: {e}")
    finally:
        cursor.close()
        db.close()


def login():
    """Authenticate the user and allow account or dashboard access."""
    global logged_in_user_id

    email = entry_email.get()
    password = entry_password.get()

    if not email or not password:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            database="budget_buddy",
        )
        cursor = db.cursor()

        cursor.execute("SELECT id, password FROM user WHERE email = %s", (email,))
        account = cursor.fetchone()

        if account and bcrypt.verify(password, account[1]):
            logged_in_user_id = account[0]
            messagebox.showinfo("Success", "Login successful!")
            open_bank_account_window()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"MySQL Error: {e}")
    finally:
        cursor.close()
        db.close()


def create_bank_account():
    """Crée un compte bancaire pour l'utilisateur connecté et ajoute le nom à la base de données."""
    global logged_in_user_id
    if not logged_in_user_id:
        messagebox.showerror("Erreur", "Vous devez d'abord vous connecter!")
        return

    # Récupérer le nom du compte depuis le champ d'entrée
    account_name = entry_account_name.get()
    initial_balance = 0  # Solde initial du compte

    # Vérifier que le nom du compte n'est pas vide
    if not account_name:
        messagebox.showerror("Erreur", "Veuillez entrer un nom pour le compte!")
        return

    try:
        # Connexion à la base de données
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            database="budget_buddy",
        )
        cursor = db.cursor()

        # Insérer le nouveau compte dans la table `bank_account`
        cursor.execute(
            "INSERT INTO bank_account (account_balance, id_user, account_name) VALUES (%s, %s, %s)",
            (initial_balance, logged_in_user_id, account_name),
        )
        db.commit()  # Enregistrer les changements dans la base

        # Afficher un message de confirmation
        messagebox.showinfo(
            "Succès", f"Compte bancaire '{account_name}' créé avec succès!"
        )

        # Lancer le tableau de bord après la création
        open_dashboard(account_name)

    except mysql.connector.Error as e:
        # Gérer les erreurs MySQL
        messagebox.showerror("Erreur", f"Erreur MySQL : {e}")
    finally:
        # Fermer la connexion et le curseur
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals() and db.is_connected():
            db.close()



def open_bank_account_window():
    """Ouvre une fenêtre pour permettre à l'utilisateur de créer un nouveau compte ou de sélectionner un compte existant."""
    global logged_in_user_id

    if not logged_in_user_id:
        messagebox.showerror("Erreur", "Vous devez d'abord vous connecter!")
        return

    bank_account_window = tk.Toplevel(root)
    bank_account_window.title("Options de Compte Bancaire")

    # En-tête
    tk.Label(bank_account_window, text="Créer un nouveau compte :").pack()

    # Champ pour saisir le nom du compte
    tk.Label(bank_account_window, text="Nom du compte :").pack()
    global entry_account_name
    entry_account_name = tk.Entry(bank_account_window)
    entry_account_name.pack()

    # Bouton pour créer un nouveau compte
    create_account_button = tk.Button(
        bank_account_window, text="Créer un compte bancaire", command=create_bank_account
    )
    create_account_button.pack()

    # Séparateur
    tk.Label(bank_account_window, text="ou").pack()

    # Liste des comptes existants
    tk.Label(bank_account_window, text="Sélectionner un compte existant :").pack()
    existing_accounts_list = tk.Listbox(bank_account_window, width=50, height=10)
    existing_accounts_list.pack()

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            database="budget_buddy",
        )
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, account_name, account_balance FROM bank_account WHERE id_user = %s",
            (logged_in_user_id,),
        )
        accounts = cursor.fetchall()

        for account in accounts:
            existing_accounts_list.insert(
                tk.END, f"ID: {account[0]} - Nom: {account[1]} - Solde: {account[2]} €"
            )

    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Erreur MySQL : {e}")
    finally:
        cursor.close()
        db.close()

    def select_account():
        """Gestion de la sélection d'un compte existant."""
        selected = existing_accounts_list.curselection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un compte bancaire!")
            return

        account_details = accounts[selected[0]]
        account_id = account_details[0]  # Récupérer l'ID du compte sélectionné

        # Lancer le tableau de bord avec l'ID du compte sélectionné
        open_dashboard(account_id)

    # Bouton pour confirmer la sélection
    select_account_button = tk.Button(
        bank_account_window, text="Sélectionner un compte bancaire", command=select_account
    )
    select_account_button.pack()


def open_dashboard(account_id):
    """Launch dashboard.py with the selected account ID."""
    messagebox.showinfo(
        "Redirecting", f"Opening Dashboard for Account ID {account_id}..."
    )
    subprocess.Popen(["python", "dashboard.py", str(account_id)])  # Pass account ID


# Main Window
root = tk.Tk()
style = Style(theme="superhero")
root.title("User Registration & Login")

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Forename:").pack()
entry_forename = tk.Entry(root)
entry_forename.pack()

tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

register_button = tk.Button(root, text="Register", command=register)
register_button.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

root.mainloop()
