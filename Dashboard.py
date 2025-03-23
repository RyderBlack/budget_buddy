import customtkinter as ctk
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox

class Dashboard(ctk.CTkFrame):
        
    def __init__(self, master):
        super().__init__(master, width=1280, height=720)
        self.master = master
        ctk.CTkLabel(self, text="Bienvenue sur votre tableau de bord").pack()
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