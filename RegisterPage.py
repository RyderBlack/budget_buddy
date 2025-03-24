import customtkinter as ctk
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
import mysql.connector
from dotenv import load_dotenv
import os
from passlib.hash import bcrypt
import re

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.assets_path = Path("./assets/register_assets")
        self.configure(width=1280, height=720)
        self.place(x=0, y=0)
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
        
        # BG image
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(640.0, 360.0, image=self.image_image_1)
        # Logo
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(103.0, 623.0, image=self.image_image_2)
        
        # Title
        self.canvas.create_text(
            300.0,
            25.0,
            anchor="nw",
            text="Budget Buddy",
            fill="#6AB9FF",
            font=("Dune Rise", -64)
        )
        
        # Label Nom
        self.canvas.create_text(
            461.0,
            173.0,
            anchor="nw",
            text="Nom",
            fill="#FFFFFF",
            font=("Inter Italic", -20)
        )
        # TextBox Nom
        self.frame_nom = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_nom.place(x=458.0, y=194.0)
        self.frame_nom.pack_propagate(False)
        self.entry_nom = ctk.CTkEntry(
            self.frame_nom,
            border_width=0,
            fg_color="#FFFFFF",
            text_color="#000716",
            width=360,
            height=40
        )
        self.entry_nom.pack(fill="both", expand=True)
        
        # Label Prenom
        self.canvas.create_text(
            461.0,
            261.0,
            anchor="nw",
            text="Prenom",
            fill="#FFFFFF",
            font=("Inter Italic", -20)
        )
        # TextBox Prenom
        self.frame_prenom = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_prenom.place(x=458.0, y=282.0)
        self.frame_prenom.pack_propagate(False)
        self.entry_prenom = ctk.CTkEntry(
            self.frame_prenom,
            border_width=0,
            fg_color="#FFFFFF",
            text_color="#000716",
            width=360,
            height=40
        )
        self.entry_prenom.pack(fill="both", expand=True)
        
        # Label Adresse Email
        self.canvas.create_text(
            461.0,
            349.0,
            anchor="nw",
            text="Adresse Email",
            fill="#FFFFFF",
            font=("Inter Italic", -20)
        )
        # TextBox Email
        self.frame_email = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_email.place(x=459.0, y=370.0)
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
        
        # Label Mot de Passe
        self.canvas.create_text(
            461.0,
            437.0,
            anchor="nw",
            text="Mot de Passe",
            fill="#FFFFFF",
            font=("Inter Italic", -20)
        )
        # TextBox Mot de Passe
        self.frame_password = ctk.CTkFrame(self, fg_color="#FFFFFF", width=362, height=40)
        self.frame_password.place(x=459.0, y=458.0)
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
        
        # Bouton Login
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_hover_1 = PhotoImage(file=self.relative_to_assets("button_hover_1.png"))
        self.button_register = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat",
            cursor="hand2"
        )
        self.button_register.place(x=538.0, y=524.0, width=204.0, height=55.0)
        self.button_register.bind('<Enter>', self.button_register_hover)
        self.button_register.bind('<Leave>', self.button_register_leave)
        
        # Link to login page
        self.login_text_id = self.canvas.create_text(
            535.0,
            600.0,
            anchor="nw",
            text="Cliquez-ici pour vous connecter",
            fill="#FFFFFF",
            font=("Inter Italic", -16)
        )
        self.canvas.tag_bind(self.login_text_id, "<Button-1>", self.on_login_text_click)
        self.canvas.tag_bind(self.login_text_id, "<Enter>", self.on_login_text_enter)
        self.canvas.tag_bind(self.login_text_id, "<Leave>", self.on_login_text_leave)
    
    def button_register_hover(self, event):
        self.button_register.config(image=self.button_image_hover_1)
    
    def button_register_leave(self, event):
        self.button_register.config(image=self.button_image_1)

    def on_login_text_click(self, event):
        if hasattr(self.master, "show_login_page"):
            self.master.show_login_page()
        else:
            print("Redirection vers la page de connexion")
    
    def on_login_text_enter(self, event):
        self.canvas.config(cursor="hand2")
        self.canvas.itemconfig(self.login_text_id, fill="#6AB9FF")
    
    def on_login_text_leave(self, event):
        self.canvas.config(cursor="")
        self.canvas.itemconfig(self.login_text_id, fill="#FFFFFF")
    
    # Register logic
    def register(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        if not nom or not prenom or not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs !")
            return
        
        if not validate_email(email):
            messagebox.showerror("Erreur", "Format email invalide !")
            return
        
        hashed_password = bcrypt.hash(password)
        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            database="budget_buddy"
        )
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO user (name, forename, email, password) VALUES (%s, %s, %s, %s)", 
                (nom, prenom, email, hashed_password)
            )
            db.commit()
            user_id = cursor.lastrowid
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            if hasattr(self.master, "show_account_page"):
                self.master.show_account_page(user_id)
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de l'inscription: {err}")
        
        cursor.close()
        db.close()


# if __name__ == "__main__":
#     ctk.set_appearance_mode("light")
#     ctk.set_default_color_theme("blue")
    
#     window = Tk()
#     window.geometry("1280x720")
#     window.configure(bg="#FFFFFF")
#     window.resizable(False, False)
    
#     register_page = RegisterPage(window)
    
#     window.mainloop()