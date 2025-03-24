import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, messagebox, simpledialog
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class AccountPage(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master, width=1280, height=720)
        self.master = master
        self.user_id = user_id
        self.assets_path = Path("./assets/account_assets")
        self.create_widgets()

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

        # Background
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(640.0, 360.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(103.0, 623.0, image=self.image_image_2)

        # Title
        self.canvas.create_text(
            443.0,
            22.0,
            anchor="nw",
            text="Budget Buddy",
            fill="#6AB9FF",
            font=("Dune_Rise", -64)
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.create_bank_account,
            relief="flat",
            cursor="hand2"
        )
        self.button_1.place(x=298.0, y=308.0, width=289.0, height=85.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.access_bank_accounts,
            relief="flat",
            cursor="hand2"
        )
        self.button_2.place(x=693.0, y=310.0, width=286.0, height=82.0)
            
    # Create/Access Bank Account Logic  
    def create_bank_account(self):
        """
        Cette méthode crée un compte bancaire pour l'utilisateur connecté
        avec un solde initial spécifié par l'utilisateur.
        """
        initial_balance = simpledialog.askfloat("Solde initial", "Entrez le solde initial du compte:", 
                                               minvalue=0, initialvalue=0)
        
        if initial_balance is None:  
            return
            
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor()
            query = "INSERT INTO bank_account (account_balance, id_user) VALUES (%s, %s)"
            cursor.execute(query, (initial_balance, self.user_id))
            db.commit()
            messagebox.showinfo("Succès", f"Compte bancaire créé avec succès avec un solde initial de {initial_balance}€ !")
            
            cursor.close()
            db.close()
            
            self.access_bank_accounts()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte bancaire: {err}")
        
    def access_bank_accounts(self):
        if hasattr(self.master, "show_dashboard"):
            self.master.show_dashboard(self.user_id)