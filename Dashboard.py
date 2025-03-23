import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv('.env')
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, user_id):
        """
        :param master: La fenêtre principale
        :param user_id: L'identifiant de l'utilisateur connecté
        """
        super().__init__(master, width=1280, height=720)
        self.master = master
        self.user_id = user_id
        # Chemin des assets pour le dashboard
        self.assets_path = Path("./assets/dashboard_assets")
        self.create_widgets()
        self.pack(fill="both", expand=True)
        
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
        
    def create_widgets(self):
        # Création du canvas principal
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Image de fond
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(640.0, 360.0, image=self.image_image_1)
        
        # Récupération des données depuis la base MySQL
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)
            
            # Récupérer les informations de l'utilisateur
            cursor.execute("SELECT * FROM user WHERE id = %s", (self.user_id,))
            user_data = cursor.fetchone()
            
            # Récupérer les comptes bancaires associés à l'utilisateur
            cursor.execute("SELECT * FROM bank_account WHERE id_user = %s", (self.user_id,))
            accounts = cursor.fetchall()
            
            # Récupérer les 5 dernières transactions de l'utilisateur
            cursor.execute(
                "SELECT * FROM bank_transaction WHERE id_user = %s ORDER BY date DESC LIMIT 5", 
                (self.user_id,)
            )
            transactions = cursor.fetchall()
            
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print("Erreur de base de données:", err)
            user_data = None
            accounts = []
            transactions = []
        
        # Construction des textes dynamiques

        # 1. Texte de salutation : "Bonjour, {Name} {Firstname}"
        if user_data:
            greeting = f"Bonjour, {user_data['name']} {user_data['forename']}"
        else:
            greeting = "Bonjour, Utilisateur"
        
        # 2. Pour le solde du compte, on prend le premier compte bancaire s'il existe
        if accounts:
            default_account = accounts[0]
            # Comme la table bank_account ne contient pas de nom, nous utilisons "Compte bancaire <ID>"
            account_label = f"Compte bancaire {default_account['id']}"
            account_balance = default_account['account_balance']
            solde_text = f"Solde du Compte {account_label}: {account_balance} €"
        else:
            solde_text = "Aucun compte bancaire trouvé"
        
        # 3. Historique des transactions
        if transactions:
            transactions_text = ""
            # Position de départ pour l'affichage, la police choisie est plus petite pour les détails
            for tx in transactions:
                # On affiche la date (formatée), la référence et le montant
                # On suppose que tx['date'] est un objet datetime, sinon adapter la conversion
                date_str = tx['date'].strftime('%Y-%m-%d') if hasattr(tx['date'], 'strftime') else str(tx['date'])
                transactions_text += f"{date_str} - {tx['reference']} : {tx['amount']} €\n"
        else:
            transactions_text = "Aucune transaction"
        
        # 4. Liste des comptes bancaires
        if accounts:
            accounts_text = ""
            for acct in accounts:
                accounts_text += f"Compte {acct['id']} - Solde: {acct['account_balance']} €\n"
        else:
            accounts_text = "Aucun compte bancaire"
        
        
        # --- Text "Sélectionner un compte" ---
        self.canvas.create_text(
            905.0,
            330.0,
            anchor="nw",
            text="Sélectionner un compte",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        # Display Accounts List
        self.canvas.create_text(
            905.0,
            380.0,
            anchor="nw",
            text=accounts_text,
            fill="#FFFFFF",
            font=("Inter Regular", -20)
        )
        
        # --- Text 'Mes dernières Transactions' ---
        self.canvas.create_text(
            320.0,
            310.0,
            anchor="nw",
            text="Mes dernières Transactions",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # Transactions History
        self.canvas.create_text(
            320.0,
            370.0,
            anchor="nw",
            text=transactions_text,
            fill="#FFFFFF",
            font=("Inter Regular", -20)
        )
        
        # --- Text 'Bonjour, {Name} {Firstname}'---
        self.canvas.create_text(
            167.0,
            168.0,
            anchor="nw",
            text=greeting,
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # --- Text 'solde du compte' ---
        self.canvas.create_text(
            816.0,
            129.0,
            anchor="nw",
            text=solde_text,
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # Button Home
        self.button_home_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_home = Button(
            self,
            image=self.button_home_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_home,
            relief="flat"
        )
        self.button_home.place(
            x=46.0,
            y=132.0,
            width=59.0,
            height=56.0
        )
        
        # Button Charts
        self.button_charts_image = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_charts = Button(
            self,
            image=self.button_charts_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_charts,
            relief="flat"
        )
        self.button_charts.place(
            x=48.0,
            y=227.0,
            width=55.0,
            height=55.0
        )
        
        # Button Transactions
        self.button_transactions_image = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_transactions = Button(
            self,
            image=self.button_transactions_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_transactions,
            relief="flat"
        )
        self.button_transactions.place(
            x=43.0,
            y=317.0,
            width=65.0,
            height=65.0
        )
        
        # Button Logout
        self.button_logout_image = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_logout = Button(
            self,
            image=self.button_logout_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_logout,
            relief="flat"
        )
        self.button_logout.place(
            x=53.0,
            y=631.0,
            width=49.0,
            height=55.0
        )
    
    def on_home(self):
        print("Bouton Home cliqué")
        # Vous pouvez ajouter ici une redirection ou une action spécifique

    def on_charts(self):
        print("Bouton Charts cliqué")
        # Action ultérieure

    def on_transactions(self):
        print("Bouton Transactions cliqué")
        # Action ultérieure

    def on_logout(self):
        print("Bouton Logout cliqué")
        if hasattr(self.master, "show_login_page"):
            self.master.show_login_page()