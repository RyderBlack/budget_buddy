from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
import customtkinter as ctk
import mysql.connector
from dotenv import load_dotenv
import os
from passlib.hash import bcrypt
import re

# Charger les variables d'environnement
load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1280, height=720)
        self.master = master
        self.pack(fill="both", expand=True)
        
        # Définir le chemin des assets
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"./assets/login_assets")
        
        # Initialiser l'interface
        self.create_widgets()
        
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def create_widgets(self):
        # Créer le canvas principal
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

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(640.0, 360.0, image=self.image_image_1)
        
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(103.0, 623.0, image=self.image_image_2)
        
        # Title
        self.canvas.create_text(
            300.0,
            25.0,
            anchor="nw",
            text="Budget Buddy",
            fill="#6AB9FF",
            font=("Dune Rise", 64 * -1)
        )
        
        # Label Email
        self.canvas.create_text(
            570.0,
            220.0,
            anchor="nw",
            text="Adresse Email",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )
        
        # TextBox Email
        self.frame_email = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_email.place(x=459.0, y=250.0)
        self.frame_email.pack_propagate(False)
        
        self.entry_email = ctk.CTkEntry(
            self.frame_email,
            border_width=0,
            fg_color="#FFFFFF",
            text_color="#000716",
            width=360,
            height=40
        )
        self.entry_email.pack(fill="both", expand=True)
        
        # Label Password
        self.canvas.create_text(
            570.0,
            320.0,
            anchor="nw",
            text="Mot de Passe",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )
        
        # TextBox Password
        self.frame_password = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_password.place(x=459.0, y=350.0)
        self.frame_password.pack_propagate(False)

        self.entry_password = ctk.CTkEntry(
            self.frame_password,
            border_width=0,
            fg_color="#FFFFFF",
            text_color="#000716",
            width=360,
            height=40,
            show="•"
        )
        self.entry_password.pack(fill="both", expand=True)

        
        # Login Button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat",
            cursor="hand2"
        )   
        self.button_1.place(
            x=542.0,
            y=401.0,
            width=195.0,
            height=46.0
        )
        
        self.button_image_hover_1 = PhotoImage(file=self.relative_to_assets("button_hover_1.png"))
        
        def button_1_hover(e):
            self.button_1.config(image=self.button_image_hover_1)
            
        def button_1_leave(e):
            self.button_1.config(image=self.button_image_1)
        
        self.button_1.bind('<Enter>', button_1_hover)
        self.button_1.bind('<Leave>', button_1_leave)
        
        # Go to Register Page
        self.register_text_id = self.canvas.create_text(
            535.00,
            460.00,
            anchor="nw",
            text="Cliquez-ici pour vous inscrire",
            fill="#FFFFFF",
            font=("Inter Italic", 16 * -1)
        )
        
        self.canvas.tag_bind(self.register_text_id, "<Button-1>", self.on_register_text_click)
        self.canvas.tag_bind(self.register_text_id, "<Enter>", self.on_register_text_enter)
        self.canvas.tag_bind(self.register_text_id, "<Leave>", self.on_register_text_leave)
        
        # Link to Forgot Password
        self.forgot_password_text_id = self.canvas.create_text(
            560.00,
            500.00,
            anchor="nw",
            text="Mot de passe oublié ?",
            fill="#FFFFFF",
            font=("Inter Italic", 16 * -1)
        )
        
        self.canvas.tag_bind(self.forgot_password_text_id, "<Button-1>", self.on_forgot_password_click)
        self.canvas.tag_bind(self.forgot_password_text_id, "<Enter>", self.on_forgot_password_enter)
        self.canvas.tag_bind(self.forgot_password_text_id, "<Leave>", self.on_forgot_password_leave)
    
    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs !")
            return
            
        if not validate_email(email):
            messagebox.showerror("Erreur", "Format email invalide !")
            return
        
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=DATABASE_PASSWORD,
                database="budget_buddy"
            )
            cursor = db.cursor()
            
            # Requête pour vérifier les identifiants
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            account = cursor.fetchone()
            
            if account and bcrypt.verify(password, account[4]):
                messagebox.showinfo("Succès", "Connexion réussie !")
                # Rediriger vers la page principale après connexion
                self.master.show_account_page(account[0])  # Passer l'ID utilisateur
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects !")
            
            cursor.close()
            db.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur de base de données", f"Une erreur est survenue: {err}")
    
    # Gestion des événements pour le texte d'inscription
    def on_register_text_click(self, event):
        # Rediriger vers la page d'inscription
        self.master.show_register_page()
    
    def on_register_text_enter(self, event):
        self.canvas.config(cursor="hand2")
        self.canvas.itemconfig(self.register_text_id, fill="#6AB9FF")
    
    def on_register_text_leave(self, event):
        self.canvas.config(cursor="")
        self.canvas.itemconfig(self.register_text_id, fill="#FFFFFF")
    
    # Gestion des événements pour le texte de mot de passe oublié
    def on_forgot_password_click(self, event):
        messagebox.showinfo("Information", "Fonctionnalité de récupération de mot de passe à venir.")
        # Pour une implémentation future:
        # self.master.show_password_recovery_page()
    
    def on_forgot_password_enter(self, event):
        self.canvas.config(cursor="hand2")
        self.canvas.itemconfig(self.forgot_password_text_id, fill="#6AB9FF")
    
    def on_forgot_password_leave(self, event):
        self.canvas.config(cursor="")
        self.canvas.itemconfig(self.forgot_password_text_id, fill="#FFFFFF")


# # Exemple d'utilisation de la classe LoginPage
# if __name__ == "__main__":
#     # Créer une fenêtre principale
#     class App(Tk):
#         def __init__(self):
#             super().__init__()
#             self.title("Budget Buddy - Connexion")
#             self.geometry("1280x720")
#             self.resizable(False, False)
            
#             # Initialiser la page de connexion
#             self.login_page = LoginPage(self)
            
#         def show_register_page(self):
#             # Pour l'exemple, affiche simplement un message
#             print("Redirection vers la page d'inscription")
#             messagebox.showinfo("Navigation", "Redirection vers la page d'inscription")
            
#         def show_account_page(self, user_id):
#             # Pour l'exemple, affiche simplement un message
#             print(f"Redirection vers la page du compte utilisateur {user_id}")
#             messagebox.showinfo("Navigation", f"Redirection vers la page du compte utilisateur {user_id}")

#     app = App()
#     app.mainloop()