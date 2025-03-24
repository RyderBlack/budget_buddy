import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Entry, Frame, Label, messagebox, StringVar, OptionMenu
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class DashboardTransactions(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master, fg_color="#FFFFFF")
        self.master = master
        self.user_id = user_id
        self.selected_account_id = None
        self.assets_path = Path("./assets/dashboard_transactions_assets")
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

 
        
        self.canvas.create_text(
            156.0,
            129.0,
            anchor="nw",
            text="Sélectionner un compte",
            fill="#FFFFFF",
            font=("Inter SemiBold", 16 * -1)
        )
        
        self.account_var = StringVar(self)
        self.account_var.set("Sélectionner un compte")  
        self.account_dropdown = OptionMenu(
            self,
            self.account_var,
            "Chargement des comptes...",  # Placeholder
            command=self.on_account_selected
        )
        
        self.account_dropdown.configure(
            bg="#6AB9FF", 
            fg="#FFFFFF",
            activebackground="#4A99FF", 
            activeforeground="#FFFFFF",
            font=("Inter", 12),
            highlightthickness=0,
            bd=0
        )
        self.account_dropdown["menu"].configure(
            bg="#1E212B",
            fg="#FFFFFF",
            activebackground="#4A99FF",
            activeforeground="#FFFFFF",
            font=("Inter", 12)
        )
        self.account_dropdown.place(x=156.0, y=159.0, width=300, height=40)

        # Text - Account Balance
        self.canvas.create_text(
            750.0,
            117.0,
            anchor="nw",
            text="Solde du Compte",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )
        
        self.balance_amount_id = self.canvas.create_text(
            900.0,
            170.0,
            anchor="n",
            text="0.00 €",
            fill="#FFFFFF",
            font=("Inter SemiBold", -48)
        )

        # Text - Deposit
        self.canvas.create_text(
            156.0,
            309.0,
            anchor="nw",
            text="Faire un dépôt de :",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )

        # TextBox Deposit Amount
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(672.0, 337.0, image=self.entry_image_1)
        self.entry_deposit = Entry(
            self,
            bd=0,
            bg="#DEDEDE",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14)
        )
        self.entry_deposit.place(x=538.0, y=309.0, width=268.0, height=54.0)

        # Button Submit Deposit transaction
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_hover_1 = PhotoImage(file=self.relative_to_assets("button_hover_1.png"))
        self.button_deposit = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.make_deposit,
            relief="flat",
            cursor="hand2"
        )
        self.button_deposit.place(x=659.0, y=398.0, width=161.0, height=57.0)
        self.button_deposit.bind('<Enter>', lambda e: self.button_deposit.config(image=self.button_image_hover_1))
        self.button_deposit.bind('<Leave>', lambda e: self.button_deposit.config(image=self.button_image_1))

        # Text - Withdraw
        self.canvas.create_text(
            161.0,
            531.0,
            anchor="nw",
            text="Faire un retrait de :",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )

        # TextBox - Withdraw
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(672.0, 559.0, image=self.entry_image_2)
        self.entry_withdraw = Entry(
            self,
            bd=0,
            bg="#DEDEDE",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14)
        )
        self.entry_withdraw.place(x=538.0, y=531.0, width=268.0, height=54.0)

        # Button Submit Withdrawn Amount
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_hover_2 = PhotoImage(file=self.relative_to_assets("button_hover_2.png"))
        self.button_withdraw = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.make_withdrawal,
            relief="flat",
            cursor="hand2"
        )
        self.button_withdraw.place(x=660.0, y=600.0, width=161.0, height=57.0)
        self.button_withdraw.bind('<Enter>', lambda e: self.button_withdraw.config(image=self.button_image_hover_2))
        self.button_withdraw.bind('<Leave>', lambda e: self.button_withdraw.config(image=self.button_image_2))

        # Text - Transfer money
        self.canvas.create_text(
            875.0,
            292.0,
            anchor="nw",
            text="Faire un virement de :",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )

        # TextBox - Transfer Money
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(1044.0, 390.0, image=self.entry_image_3)
        self.entry_transfer_amount = Entry(
            self,
            bd=0,
            bg="#DEDEDE",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14)
        )
        self.entry_transfer_amount.place(x=910.0, y=362.0, width=268.0, height=54.0)

        # Text - Transfer to (Account to send money to)
        self.canvas.create_text(
            910.0,
            441.0,
            anchor="nw",
            text="vers le compte:",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )
        
        # TextBox -  Transfer to
        self.entry_image_4 = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(1046.0, 550.0, image=self.entry_image_4)
        self.entry_transfer_to = Entry(
            self,
            bd=0,
            bg="#DEDEDE",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14)
        )
        self.entry_transfer_to.place(x=912.0, y=522.0, width=268.0, height=54.0)
        
        
        
        self.entry_transfer_to.insert(0, "Entrez l'ID du compte destinataire")
        self.entry_transfer_to.bind("<FocusIn>", lambda e: self.clear_placeholder(self.entry_transfer_to, "Entrez l'ID du compte destinataire"))
        self.entry_transfer_to.bind("<FocusOut>", lambda e: self.restore_placeholder(self.entry_transfer_to, "Entrez l'ID du compte destinataire"))

        help_text = Label(
            self,
            text="(Exemple: pour le compte #5, entrez simplement 5)",
            font=("Inter", 10),
            bg="#14171F",  
            fg="#AAAAAA"
        )
        help_text.place(x=912.0, y=580.0, width=268.0)

        # Button Submit Transfer money
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_image_hover_3 = PhotoImage(file=self.relative_to_assets("button_hover_3.png"))
        self.button_transfer = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.make_transfer,
            relief="flat",
            cursor="hand2"
        )
        self.button_transfer.place(x=963.0, y=600.0, width=161.0, height=57.0)
        self.button_transfer.bind('<Enter>', lambda e: self.button_transfer.config(image=self.button_image_hover_3))
        self.button_transfer.bind('<Leave>', lambda e: self.button_transfer.config(image=self.button_image_3))

        # Button Home
        self.button_home_image = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_home = Button(
            self,
            image=self.button_home_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_home,
            relief="flat",
            cursor="hand2"
        )
        self.button_home.place(x=46.0, y=132.0, width=59.0, height=56.0)

        # Button Charts
        self.button_charts_image = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_charts = Button(
            self,
            image=self.button_charts_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_charts,
            relief="flat",
            cursor="hand2"
        )
        self.button_charts.place(x=48.0, y=227.0, width=55.0, height=55.0)

        # Button Transactions (active)
        self.button_transactions_image = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_transactions = Button(
            self,
            image=self.button_transactions_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Already on transactions view"),
            relief="flat",
            cursor="hand2"
        )
        self.button_transactions.place(x=43.0, y=317.0, width=65.0, height=65.0)

        # Button Logout
        self.button_logout_image = PhotoImage(file=self.relative_to_assets("button_7.png"))
        self.button_logout = Button(
            self,
            image=self.button_logout_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_logout,
            relief="flat",
            cursor="hand2"
        )
        self.button_logout.place(x=53.0, y=631.0, width=49.0, height=55.0)
        
    
    def clear_placeholder(self, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg="#000716")

    def restore_placeholder(self, entry, placeholder_text):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="#999999")

    
    

    def select_account_from_window(self, account_id, account_balance):
        self.selected_account_id = account_id
        self.update_account_display(account_id, account_balance)
        self.account_selection_window.destroy()
        

    def load_user_data(self):
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

            cursor.close()
            db.close()

            
            if accounts:
                account_menu = self.account_dropdown["menu"]
                account_menu.delete(0, "end")
                self.account_options = {}
                
                for account in accounts:
                    account_id = account['id']
                    account_balance = account['account_balance']
                    display_text = f"Compte #{account_id} - {float(account_balance):.2f} €"
                    self.account_options[display_text] = (account_id, account_balance)
                    account_menu.add_command(
                        label=display_text, 
                        command=lambda txt=display_text: self.on_account_selected(txt)
                    )
                
                self.selected_account_id = accounts[0]['id']
                self.update_account_display(accounts[0]['id'], accounts[0]['account_balance'])
                first_account_text = list(self.account_options.keys())[0]
                self.account_var.set(first_account_text)

      
            else:
                messagebox.showinfo("Information", "Aucun compte bancaire trouvé. Veuillez d'abord créer un compte.")
                self.on_home()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des comptes: {err}")
            messagebox.showerror("Erreur", f"Impossible de charger les comptes: {err}")

    def update_account_display(self, account_id, account_balance):
        # self.canvas.itemconfig(self.account_text_id, text=f"Compte Actuel: #{account_id}")
        self.canvas.itemconfig(self.balance_amount_id, text=f"{float(account_balance):.2f} €")

    def validate_amount(self, amount_str):
        if not amount_str:
            messagebox.showerror("Erreur", "Veuillez entrer un montant.")
            return False

        amount_str = amount_str.replace(',', '.')

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif.")
                return False
            return amount
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre valide.")
            return False
        
        
    def refresh_accounts_dropdown(self):
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
            
            cursor.close()
            db.close()
            
            if accounts:
                current_selected_id = self.selected_account_id
                
                account_menu = self.account_dropdown["menu"]
                account_menu.delete(0, "end")
                self.account_options = {}
                
                for account in accounts:
                    account_id = account['id']
                    account_balance = account['account_balance']
                    display_text = f"Compte #{account_id} - {float(account_balance):.2f} €"
                    self.account_options[display_text] = (account_id, account_balance)
                    account_menu.add_command(
                        label=display_text, 
                        command=lambda txt=display_text: self.on_account_selected(txt)
                    )
                
                for display_text, (acc_id, acc_balance) in self.account_options.items():
                    if acc_id == current_selected_id:
                        self.account_var.set(display_text)
                        break
            
        except mysql.connector.Error as err:
            print(f"Erreur lors du rafraîchissement des comptes: {err}")
            messagebox.showerror("Erreur", f"Impossible de rafraîchir la liste des comptes: {err}")

    def make_deposit(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Aucun compte sélectionné.")
            return

        amount = self.validate_amount(self.entry_deposit.get())
        if not amount:
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor()

            cursor.execute(
                "UPDATE bank_account SET account_balance = account_balance + %s WHERE id = %s",
                (amount, self.selected_account_id)
            )

            now = datetime.now()
            reference = f"DEP{now.strftime('%Y%m%d%H%M%S')}"
            cursor.execute(
                "INSERT INTO bank_transaction (reference, description, amount, date, transaction_type, id_user, id_bank_account) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (reference, "Dépôt", amount, now, "deposit", self.user_id, self.selected_account_id)
            )

            db.commit()

            cursor.execute("SELECT account_balance FROM bank_account WHERE id = %s", (self.selected_account_id,))
            new_balance = cursor.fetchone()[0]

            cursor.close()
            db.close() 
            
            self.update_account_display(self.selected_account_id, new_balance)
            self.entry_deposit.delete(0, 'end')
            messagebox.showinfo("Succès", f"Dépôt de {amount:.2f}€ effectué avec succès.")
            self.refresh_accounts_dropdown()

        except mysql.connector.Error as err:
            print(f"Erreur lors du dépôt: {err}")
            messagebox.showerror("Erreur", f"Impossible d'effectuer le dépôt: {err}")

    def make_withdrawal(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Aucun compte sélectionné.")
            return

        amount = self.validate_amount(self.entry_withdraw.get())
        if not amount:
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor()

            cursor.execute("SELECT account_balance FROM bank_account WHERE id = %s", (self.selected_account_id,))
            current_balance = cursor.fetchone()[0]

            if float(current_balance) < amount:
                messagebox.showerror("Erreur", "Solde insuffisant pour effectuer ce retrait.")
                cursor.close()
                db.close()
                return

            cursor.execute(
                "UPDATE bank_account SET account_balance = account_balance - %s WHERE id = %s",
                (amount, self.selected_account_id)
            )

            now = datetime.now()
            reference = f"WDR{now.strftime('%Y%m%d%H%M%S')}"
            cursor.execute(
                "INSERT INTO bank_transaction (reference, description, amount, date, transaction_type, id_user, id_bank_account) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (reference, "Retrait", -amount, now, "withdrawal", self.user_id, self.selected_account_id)
            )

            db.commit()

            cursor.execute("SELECT account_balance FROM bank_account WHERE id = %s", (self.selected_account_id,))
            new_balance = cursor.fetchone()[0]

            cursor.close()
            db.close()

            self.update_account_display(self.selected_account_id, new_balance)
            self.entry_withdraw.delete(0, 'end')
            messagebox.showinfo("Succès", f"Retrait de {amount:.2f}€ effectué avec succès.")
            self.refresh_accounts_dropdown()

        except mysql.connector.Error as err:
            print(f"Erreur lors du retrait: {err}")
            messagebox.showerror("Erreur", f"Impossible d'effectuer le retrait: {err}")

    def make_transfer(self):
        if not self.selected_account_id:
            messagebox.showerror("Erreur", "Aucun compte source sélectionné.")
            return

        amount = self.validate_amount(self.entry_transfer_amount.get())
        if not amount:
            return

        dest_account_str = self.entry_transfer_to.get().strip()
        if not dest_account_str:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de compte de destination.")
            return

        try:
            dest_account_id = int(dest_account_str)
        except ValueError:
            messagebox.showerror("Erreur", "Le numéro de compte de destination doit être un nombre.")
            return

        if dest_account_id == self.selected_account_id:
            messagebox.showerror("Erreur", "Impossible de faire un virement vers le même compte.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor()

            cursor.execute("SELECT id FROM bank_account WHERE id = %s", (dest_account_id,))
            if not cursor.fetchone():
                messagebox.showerror("Erreur", "Le compte de destination n'existe pas.")
                cursor.close()
                db.close()
                return

            cursor.execute("SELECT account_balance FROM bank_account WHERE id = %s", (self.selected_account_id,))
            current_balance = cursor.fetchone()[0]

            if float(current_balance) < amount:
                messagebox.showerror("Erreur", "Solde insuffisant pour effectuer ce virement.")
                cursor.close()
                db.close()
                return

            cursor.execute(
                "UPDATE bank_account SET account_balance = account_balance - %s WHERE id = %s",
                (amount, self.selected_account_id)
            )

            cursor.execute(
                "UPDATE bank_account SET account_balance = account_balance + %s WHERE id = %s",
                (amount, dest_account_id)
            )

            now = datetime.now()
            reference = f"TRF{now.strftime('%Y%m%d%H%M%S')}"
            cursor.execute(
                "INSERT INTO bank_transaction (reference, description, amount, date, transaction_type, id_user, id_bank_account) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (reference, f"Virement vers compte #{dest_account_id}", -amount, now, "transfer", self.user_id, self.selected_account_id)
            )

            cursor.execute(
                "INSERT INTO bank_transaction (reference, description, amount, date, transaction_type, id_user, id_bank_account) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (reference, f"Virement depuis compte #{self.selected_account_id}", amount, now, "transfer", self.user_id, dest_account_id)
            )

            db.commit()

            cursor.execute("SELECT account_balance FROM bank_account WHERE id = %s", (self.selected_account_id,))
            new_balance = cursor.fetchone()[0]

            cursor.close()
            db.close()

            self.update_account_display(self.selected_account_id, new_balance)
            self.entry_transfer_amount.delete(0, 'end')
            self.entry_transfer_to.delete(0, 'end')
            messagebox.showinfo("Succès", f"Virement de {amount:.2f}€ vers le compte #{dest_account_id} effectué avec succès.")
            self.refresh_accounts_dropdown()
            
        except mysql.connector.Error as err:
            print(f"Erreur lors du virement: {err}")
            messagebox.showerror("Erreur", f"Impossible d'effectuer le virement: {err}")

    def on_account_selected(self, selection):
        if selection in self.account_options:
            account_id, account_balance = self.account_options[selection]
            self.selected_account_id = account_id
            self.update_account_display(account_id, account_balance)
            print(f"Compte sélectionné: #{account_id} avec solde: {account_balance}") # Pour déboguer
            self.account_var.set(selection)
    
    def on_home(self):
        if hasattr(self.master, "show_dashboard"):
            self.master.show_dashboard(self.user_id)

    def on_charts(self):
        if hasattr(self.master, "show_dashboard_charts"):
            self.master.show_dashboard_charts(self.user_id)

    def on_logout(self):
        if hasattr(self.master, "show_login_page"):
            self.master.show_login_page()



#     root.mainloop()