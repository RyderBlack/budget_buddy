from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
from Login import LoginScreen


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/register_assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class RegisterScreen(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        


        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 558,
            width = 864,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        canvas.pack(fill="both", expand=True)
        
        # Left Side Image
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            216.0,
            279.0,
            image=image_image_1
        )

        #  Right Side Rectangle
        canvas.create_rectangle(
            432.0001220703125,
            0.0,
            864.0001220703125,
            558.5,
            fill="#1E1E1E",
            outline="")

        # Title
        canvas.create_text(
            432.4000244140625,
            12.099853515625,
            anchor="nw",
            text="Budget Buddy",
            fill="#6AB9FF",
            font=("Italianno Regular", 64 * -1)
        )


        # Label Nom
        canvas.create_text(
            475.4000244140625,
            111.099853515625,
            anchor="nw",
            text="Nom",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )

        # TextBox Nom
        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            653.9000244140625,
            154.099853515625,
            image=entry_image_1
        )
        entry_1 = Entry(
            master=self,
            font="Inter 16",
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=475.4000244140625,
            y=135.099853515625,
            width=357.0,
            height=36.0
        )

        # Label Prenom
        canvas.create_text(
            475.4000244140625,
            187.099853515625,
            anchor="nw",
            text="Prenom",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )

        # TextBox Prenom
        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            653.9000244140625,
            230.099853515625,
            image=entry_image_2
        )
        entry_2 = Entry(
            master=self,
            font="Inter 16",
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=475.4000244140625,
            y=211.099853515625,
            width=357.0,
            height=36.0
        )

        # Label Email
        canvas.create_text(
            475.4000244140625,
            263.099853515625,
            anchor="nw",
            text="Adresse Email ",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )

        #  TextBox email
        entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            653.9000244140625,
            306.099853515625,
            image=entry_image_3
        )
        entry_3 = Entry(
            master=self,
            font="Inter 16",
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_3.place(
            x=475.4000244140625,
            y=287.099853515625,
            width=357.0,
            height=36.0
        )

        # Label Password
        canvas.create_text(
            475.4000244140625,
            339.099853515625,
            anchor="nw",
            text="Mot de Passe",
            fill="#FFFFFF",
            font=("Inter Italic", 20 * -1)
        )

        # TextBox Password
        entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            653.9000244140625,
            382.099853515625,
            image=entry_image_4
        )
        entry_4 = Entry(
            master=self,
            font="Inter 16",
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            show="*"
        )
        entry_4.place(
            x=475.4000244140625,
            y=363.099853515625,
            width=357.0,
            height=36.0
        )

        # Register Button
        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            cursor="hand2"
        )
        button_1.place(
            x=545,
            y=425,
            width=220.0,
            height=73.0
        )

        button_image_hover_1 = PhotoImage(
            file=relative_to_assets("button_hover_1.png"))

        def button_1_hover(e):
            button_1.config(
                image=button_image_hover_1
            )
        def button_1_leave(e):
            button_1.config(
                image=button_image_1
            )

        button_1.bind('<Enter>', button_1_hover)
        button_1.bind('<Leave>', button_1_leave)
        
        button_2 = Button(
            self,
            text="Back to Login",
            command=lambda: controller.show_frame(LoginScreen)
        )

