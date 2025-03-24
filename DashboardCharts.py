import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Frame, Label, messagebox, scrolledtext, Scrollbar
import mysql.connector
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class DashboardCharts(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master, fg_color="#FFFFFF")
        self.master = master
        self.user_id = user_id
        self.selected_account_id = None
        self.assets_path = Path("./assets/dashboard_charts_assets")
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
        
       
        # Text "Solde du Compte"
        self.balance_text_id = self.canvas.create_text(
            400.0,  
            132.5,
            anchor="n", 
            text="Solde du Compte : 0.00 €",
            fill="#FFFFFF",
            font=("Inter SemiBold", 32 * -1)
        )

        self.balance_amount_id = self.canvas.create_text(
            1100.0,  
            125,
            anchor="n",
            text="0.00 €",
            fill="#1E212B",
            font=("Inter SemiBold", -48)
        )


        # Text "Sélectionner un compte"
        self.canvas.create_text(
            960.0,
            210.0,
            anchor="nw",
            text="Sélectionner un compte",
            fill="#FFFFFF",
            font=("Inter SemiBold", 24 * -1)
        )

        # Accounts List Frame
        self.accounts_frame = Frame(self, bg="#14171F")
        self.accounts_frame.place(x=960, y=250, width=250, height=425)

        # Buton Home
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

        # Buton Charts
        self.button_charts_image = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_charts = Button(
            self,
            image=self.button_charts_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Already on charts view"),
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
            command= self.on_transactions,
            relief="flat",
            cursor="hand2"
        )
        self.button_transactions.place(
            x=43.0,
            y=317.0,
            width=65.0,
            height=65.0
        )

        # Buton Logout
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
                self.selected_account_id = accounts[0]['id']
                self.update_account_display(accounts[0]['account_balance'])

            self.refresh_accounts_list()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des comptes: {err}")
            messagebox.showerror("Erreur", f"Impossible de charger les comptes: {err}")

    def refresh_accounts_list(self):
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
                    bg="#14171F",
                    fg="#FFFFFF"
                )
                no_accounts_label.pack(pady=20)
            else:
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

                for account in accounts:
                    account_frame = Frame(scrollable_frame, bg="#1E212B", bd=1, relief="solid")
                    account_frame.pack(fill="x", padx=60, pady=5)

                    account_label = Label(
                        account_frame,
                        text=f"Compte #{account['id']}",
                        font=("Inter Bold", 12),
                        bg="#1E212B",
                        fg="#FFFFFF"
                    )
                    account_label.pack(anchor="w", padx=5, pady=(5, 0))

                    balance_label = Label(
                        account_frame,
                        text=f"Solde: {float(account['account_balance']):.2f} €",
                        font=("Inter", 11),
                        bg="#1E212B",
                        fg="#AAAAAA"
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
                        command=lambda acc_id=account['id'], acc_bal=account['account_balance']: self.select_account(acc_id, acc_bal)
                    )
                    select_button.pack(anchor="e", padx=5, pady=5)

                canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

            cursor.close()
            db.close()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des comptes: {err}")
            error_label = Label(
                self.accounts_frame,
                text=f"Erreur: Impossible de charger les comptes\n{err}",
                font=("Inter", 10),
                bg="#14171F",
                fg="#FF0000"
            )
            error_label.pack(pady=20)

    def select_account(self, account_id, account_balance):
        self.selected_account_id = account_id
        self.update_account_display(account_balance)      

        
        
        
    def update_account_display(self, account_balance):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT id FROM bank_account WHERE id = %s", (self.selected_account_id,))
            account = cursor.fetchone()

            if account:
                balance_text = f"Solde du Compte #{account['id']}"
                self.canvas.itemconfig(self.balance_text_id, text=balance_text)
                
                self.canvas.itemconfig(self.balance_amount_id, text=f"{float(account_balance):.2f} €")

            cursor.close()
            db.close()

            self.display_charts()

        except mysql.connector.Error as err:
            print(f"Erreur lors de la mise à jour des informations du compte: {err}")

    def display_charts(self):
        if self.selected_account_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un compte bancaire.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT c.category_type, SUM(bt.amount) AS total_amount
                FROM bank_transaction bt
                JOIN category c ON bt.id_category = c.id
                WHERE bt.id_bank_account = %s AND bt.transaction_type = 'expense'
                GROUP BY c.category_type
            """, (self.selected_account_id,))
            categories = cursor.fetchall()

            cursor.execute("""
                SELECT DATE_FORMAT(bt.date, '%Y-%m') AS month, SUM(bt.amount) AS total_expense
                FROM bank_transaction bt
                WHERE bt.id_bank_account = %s AND bt.transaction_type = 'expense'
                GROUP BY DATE_FORMAT(bt.date, '%Y-%m')
                ORDER BY month
            """, (self.selected_account_id,))
            monthly_expenses = cursor.fetchall()

            cursor.close()
            db.close()

            for widget in self.winfo_children():
                if isinstance(widget, Frame) and widget != self.accounts_frame:
                    widget.destroy()

            # Charts FRAME
            charts_frame = Frame(self, bg="#14171F")
            charts_frame.place(x=160, y=210, width=750, height=470)

            if categories:
                category_labels = [cat['category_type'] for cat in categories]
                category_amounts = [float(cat['total_amount']) for cat in categories]

                fig_pie, ax_pie = plt.subplots(figsize=(4, 3))
                ax_pie.pie(category_amounts, labels=category_labels, autopct='%1.1f%%', startangle=90)
                ax_pie.axis('equal')
                ax_pie.set_title("Répartition des Dépenses par Catégorie", fontsize=10)

                canvas_pie = FigureCanvasTkAgg(fig_pie, master=charts_frame)
                canvas_pie.draw()
                canvas_pie.get_tk_widget().pack(side="left", padx=20, pady=20)
            else:
                Label(charts_frame, text="Aucune donnée de dépense disponible.", font=("Inter", 12), fg="#FFFFFF",bg="#14171F").pack(pady=20)

            if monthly_expenses:
                months = [exp['month'] for exp in monthly_expenses]
                expenses = [float(exp['total_expense']) for exp in monthly_expenses]

                fig_bar, ax_bar = plt.subplots(figsize=(6, 3))
                ax_bar.bar(months, expenses, color="#6AB9FF")
                ax_bar.set_title("Dépenses Mensuelles", fontsize=10)
                ax_bar.set_xlabel("Mois")
                ax_bar.set_ylabel("Montant (€)")
                ax_bar.tick_params(axis='x', rotation=45)

                canvas_bar = FigureCanvasTkAgg(fig_bar, master=charts_frame)
                canvas_bar.draw()
                canvas_bar.get_tk_widget().pack(side="right", padx=20, pady=20)
            else:
                Label(charts_frame, text="Aucune donnée mensuelle disponible.", font=("Inter", 12), fg="#FFFFFF",bg="#14171F").pack(pady=20)

        except mysql.connector.Error as err:
            print(f"Erreur lors de la récupération des données pour les graphiques: {err}")
            messagebox.showerror("Erreur", f"Impossible de charger les données pour les graphiques: {err}")

    def on_home(self):
        if hasattr(self.master, "show_dashboard"):
            self.master.show_dashboard(self.user_id)
            
    def on_transactions(self):
        if hasattr(self.master, "show_dashboard_transactions"):
            self.master.show_dashboard_transactions(self.user_id)
            

    def on_logout(self):
        """Déconnecte l'utilisateur et retourne à la page de connexion."""
        if hasattr(self.master, "show_login_page"):
            self.master.show_login_page()