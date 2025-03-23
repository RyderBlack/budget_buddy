import customtkinter as ctk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage

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

        # Bouton "Créer un compte bancaire"
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1,
            relief="flat"
        )
        self.button_1.place(x=298.0, y=308.0, width=289.0, height=85.0)

        # Bouton "Accéder au(x) compte(s)"
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_2,
            relief="flat"
        )
        self.button_2.place(x=693.0, y=310.0, width=286.0, height=82.0)

    def on_button_1(self):
        print("Bouton 1 (Créer un compte bancaire) cliqué")
        if hasattr(self.master, "show_dashboard"):
            self.master.show_dashboard(self.user_id)

    def on_button_2(self):
        print("Bouton 2 (Accéder au(x) compte(s)) cliqué")
        if hasattr(self.master, "show_dashboard"):
            self.master.show_dashboard(self.user_id)