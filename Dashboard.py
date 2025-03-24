import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Frame, Label, scrolledtext, Scrollbar
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master, fg_color="#FFFFFF")
        self.master = master
        self.user_id = user_id  
        self.assets_path = Path("./assets/dashboard_assets")
        self.selected_account_id = None
        self.accounts_frame = None
        self.transactions_frame = None
        self.balance_text_id = None
        self.transactions_text_id = None
        self.create_widgets()
        self.load_user_data()
        
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
        
    def create_widgets(self):
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
        
        # Background Image
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(640.0, 360.0, image=self.image_image_1)
        
        # --- Text "Sélectionner un compte" ---
        self.canvas.create_text(
            905.0,
            330.0,
            anchor="nw",
            text="Sélectionner un compte",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # Account List Frame
        self.accounts_frame = Frame(self, bg="#14171F")
        self.accounts_frame.place(x=925, y=370, width=300, height=300)
        
        # --- Text 'Mes dernières Transactions' ---
        self.canvas.create_text(
            320.0,
            310.0,
            anchor="nw",
            text="Mes dernières Transactions",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # Transaction history Frame
        self.transactions_frame = Frame(self, bg="#14171F")
        self.transactions_frame.place(x=160, y=350, width=700, height=325)
        
        # --- Text 'Bonjour, {Name} {Firstname}' ---
        self.greeting_text_id = self.canvas.create_text(
            167.0,
            168.0,
            anchor="nw",
            text="Bonjour, ...",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        # --- Text 'solde du compte' ---
        self.balance_text_id = self.canvas.create_text(
            816.0,
            129.0,
            anchor="nw",
            text="Solde du Compte: ...",
            fill="#FFFFFF",
            font=("Inter SemiBold", -32)
        )
        
        self.balance_amount_id = self.canvas.create_text(
            900.0,
            200.0,
            anchor="nw",
            text="0.00 €",
            fill="#14171F",
            font=("Inter SemiBold", -48)
        )
        
        # Button Home
        self.button_home_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_home = Button(
            self,
            image=self.button_home_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_home,
            relief="flat",
            cursor="hand2"
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
            command=lambda: self.master.show_dashboard_charts(self.user_id),
            relief="flat",
            cursor="hand2"
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
            relief="flat",
            cursor="hand2"
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
            relief="flat",
            cursor="hand2"
        )
        self.button_logout.place(
            x=53.0,
            y=631.0,
            width=49.0,
            height=55.0
        )
    
    def load_user_data(self):
        """Charge les données de l'utilisateur et affiche le premier compte par défaut"""
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM user WHERE id = %s", (self.user_id,))
            user_data = cursor.fetchone()
            
            cursor.execute("SELECT * FROM bank_account WHERE id_user = %s", (self.user_id,))
            accounts = cursor.fetchall()
            
            cursor.close()
            db.close()
            
            if user_data:
                greeting = f"Bonjour, {user_data['name']} {user_data['forename']}"
                self.canvas.itemconfig(self.greeting_text_id, text=greeting)
            
            if accounts:
                self.selected_account_id = accounts[0]['id']
                self.update_account_display(self.selected_account_id)
            
            self.refresh_accounts_list()
            
        except mysql.connector.Error as err:
            print("Erreur de base de données:", err)
    

    def refresh_accounts_list(self):
        """Rafraîchit la liste des comptes bancaires de l'utilisateur avec défilement"""
        for widget in self.accounts_frame.winfo_children():
            widget.destroy()
        
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("SELECT id, account_balance FROM bank_account WHERE id_user = %s", (self.user_id,))
            accounts = cursor.fetchall()
            
            if not accounts:
                no_accounts_label = Label(
                    self.accounts_frame,
                    text="Aucun compte bancaire trouvé",
                    font=("Inter", 12),
                    bg="#FFFFFF",
                    fg="#555555"
                )
                no_accounts_label.pack(pady=20)
            else:
                # Accounts List Scrollable
                canvas = Canvas(self.accounts_frame, bg="#14171F", bd=0, highlightthickness=0)
                scrollbar = Scrollbar(self.accounts_frame, orient="vertical", command=canvas.yview)
                
                scrollable_frame = Frame(canvas, bg="#14171F")
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                scrollable_frame.configure(width=280)
                for account in accounts:
                    account_frame = Frame(scrollable_frame, bg="#1E212B", bd=1, relief="solid")
                    account_frame.pack(fill="x", padx=80, pady=5)
                    
                    account_label = Label(
                        account_frame,
                        text=f"Compte #{account['id']}",
                        font=("Inter Bold", 12),
                        bg="#1E212B",
                        fg="#333333"
                    )
                    account_label.pack(anchor="w", padx=5, pady=(5, 0))
                    
                    balance_label = Label(
                        account_frame,
                        text=f"Solde: {float(account['account_balance']):.2f} €",
                        font=("Inter", 11),
                        bg="#1E212B",
                        fg="#555555"
                    )
                    balance_label.pack(anchor="w", padx=5, pady=(0, 5))
                    
                    select_button = Button(
                        account_frame,
                        text="Sélectionner",
                        font=("Inter", 10),
                        bg="#6AB9FF",
                        fg="#FFFFFF",
                        relief="flat",
                        cursor="hand2",
                        command=lambda acc_id=account['id']: self.select_account(acc_id)
                    )
                    select_button.pack(anchor="e", padx=5, pady=5)
                
                canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
            
            cursor.close()
            db.close()
            
        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des comptes: {err}")
            error_label = Label(
                self.accounts_frame,
                text=f"Erreur: Impossible de charger les comptes\n{err}",
                font=("Inter", 10),
                bg="#FFFFFF",
                fg="#FF0000"
            )
            error_label.pack(pady=20)
    
    def select_account(self, account_id):
        
        self.selected_account_id = account_id
        self.update_account_display(account_id)
    
    def update_account_display(self, account_id):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM bank_account WHERE id = %s", (account_id,))
            account = cursor.fetchone()
            
            if account:
                self.canvas.itemconfig(self.balance_text_id, text=f"Solde du Compte #{account_id}")
                self.canvas.itemconfig(self.balance_amount_id, text=f"{float(account['account_balance']):.2f}€")
                
                cursor.execute(
                    """SELECT * FROM bank_transaction 
                       WHERE id_bank_account = %s 
                       ORDER BY date DESC LIMIT 10""", 
                    (account_id,)
                )
                transactions = cursor.fetchall()
                
                self.refresh_transactions_display(transactions)
            
            cursor.close()
            db.close()
            
        except mysql.connector.Error as err:
            print(f"Erreur lors de la mise à jour de l'affichage du compte: {err}")
    
    def refresh_transactions_display(self, transactions):
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        
        if not transactions:
            no_tx_label = Label(
                self.transactions_frame,
                text="Aucune transaction pour ce compte",
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#555555"
            )
            no_tx_label.pack(pady=20)
        else:
            tx_text = scrolledtext.ScrolledText(
                self.transactions_frame,
                width=48,
                height=15,
                font=("Inter", 10),
                bg="#FFFFFF",
                fg="#333333",
                wrap="word"
            )
            tx_text.pack(fill="both", expand=True)
            
            for tx in transactions:
                date_str = tx['date'].strftime('%Y-%m-%d %H:%M') if hasattr(tx['date'], 'strftime') else str(tx['date'])
                tx_type = tx['transaction_type']
                amount = float(tx['amount'])
                
                if tx_type == "debit":
                    tx_text.insert("end", f"{date_str} - {tx['reference']}\n", "date")
                    tx_text.insert("end", f"{tx['description']}\n", "desc")
                    tx_text.insert("end", f"-{amount:.2f} €\n\n", "debit")
                else:
                    tx_text.insert("end", f"{date_str} - {tx['reference']}\n", "date")
                    tx_text.insert("end", f"{tx['description']}\n", "desc")
                    tx_text.insert("end", f"+{amount:.2f} €\n\n", "credit")
            
            tx_text.tag_configure("date", foreground="#555555")
            tx_text.tag_configure("desc", foreground="#333333")
            tx_text.tag_configure("debit", foreground="#FF5555")
            tx_text.tag_configure("credit", foreground="#55AA55")
            
            tx_text.config(state="disabled")

    def on_home(self):
        """Rafraîchit le dashboard"""
        self.load_user_data()

    def on_charts(self):
        if hasattr(self.master, "show_dashboard_charts"):
            self.master.show_dashboard_charts(self.user_id)

    def on_transactions(self):
        if hasattr(self.master, "show_dashboard_transactions"):
            self.master.show_dashboard_transactions(self.user_id)

    def on_logout(self):
        print("Bouton Logout cliqué")
        if hasattr(self.master, "show_login_page"):
            self.master.show_login_page()